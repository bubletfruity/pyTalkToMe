import numpy
import random
import json

MEMORIES_FILE = "memories.json"

with open(MEMORIES_FILE,"r") as file:
    memories = json.loads(file.read())

def printDistances(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()

def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))
    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1
    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
    a = 0
    b = 0
    c = 0
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1
    #printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)]

def getClosestMemory(token):
    closestMemoryKey = None
    closestMemorySolution = None
    closestDistance = numpy.inf
    for key in memories:
        distance = levenshteinDistanceDP(token,key)
        if distance < closestDistance:
            closestMemoryKey = key
            closestMemorySolution = memories[key]
            closestDistance = distance
    return closestMemoryKey, closestMemorySolution, closestDistance

messagesSentInSession = 0
lastComputerMessage = "hi"
print("cpu: " + lastComputerMessage)
while True:
    userInput = input("user: ").lower()
    messagesSentInSession += 1
    closestKey, possibleSolutions, closestDistance = getClosestMemory(userInput)
    chosenSolution = random.choice(possibleSolutions) #provide an answer
    #if the solution that the user gave was too unique
    if closestDistance/len(closestKey) > 0.1:
        #print("[cpu notes your unique response]")
        if lastComputerMessage in memories.keys():
            memories[lastComputerMessage].append(userInput) #append to a memory that's basically ":3":["that cool user input"]
        else:
            memories[lastComputerMessage] = [userInput] #append an entirely new memory that's basically ":3":["that cool user input"]
    if messagesSentInSession%5 == 0:
        print("SAVING TO MEMORIES...")
        with open(MEMORIES_FILE,"w") as file:
            file.write(json.dumps(memories))
    print("cpu: " + chosenSolution)
    lastComputerMessage = chosenSolution