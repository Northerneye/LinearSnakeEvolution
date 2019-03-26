import time
import random
import os
import sys
import math
import numpy as np
import subprocess
generations = 100
generationsize = int(input("generation size: "))
areasize = 5
mutation_rate = int(input("mutation rate: "))
gain_buff = int(input("selective pressure: "))
scores = [0 for x in range(areasize*areasize)]
for generation in range(generations):
    for individual in range(generationsize):
        if(generation>1):
            os.remove(str(mutation_rate) +' '+ str(gain_buff) + ' ' + str(generationsize)+" generation"+str(generation-2)+" individual"+str(individual))
        os.system('start python snakeEvolution.py "' + str(mutation_rate) + ' ' + str(gain_buff) + ' ' + str(generationsize) +' generation'+ str(generation) +' individual'+ str(individual) +'" ')
    while(True):
        myflag = True
        for x in range(generationsize):
            if(os.path.isfile(str(mutation_rate) + ' ' + str(gain_buff) + ' ' + str(generationsize)+" generation"+str(generation)+" individual"+str(x)) == False):
                myflag = False
        if(myflag == True):
            break
    for individual in range(generationsize):
        gain = ""
        publickey = open(str(mutation_rate) + ' ' + str(gain_buff) + ' ' + str(generationsize)+" generation"+str(generation)+" individual"+str(individual), 'r')
        data = list(publickey.read())
        publickey.close()
        for x in range(3):
            if(data[x] == " "):
                break
            else:
                gain = gain + str(data[x])
                scores[int(gain)-1] = scores[int(gain)-1]+1
        print("generation:"+str(generation)+" individual:"+str(individual)+" gain:"+str(gain))
    print("Mutation Rate: "+str(mutation_rate))
    print("Selective Pressure: "+str(gain_buff))
    for x in range(areasize*areasize):
        print(str(x+1)+": "+str(scores[x]))
    for x in range(areasize*areasize):
        scores[x] = 0
    print("")
input("finished")

"""
mutation_chance = .1
mutation_rate = 5
mutation_strength = 2
parent_number = 2
gain_buff = 4
areasize = 3
"""