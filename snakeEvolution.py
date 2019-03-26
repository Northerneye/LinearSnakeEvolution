import time
import modifiedluxor
import random
import os
import sys
import math
import numpy as np
import ast
modifiedluxor.refreshRate = 0
mutation_chance = .1
mutation_rate = ""
gain_buff = ""
mutation_strength = 2
parent_number = 2
areasize = 5
snakelength = 1
lose = False
snake = [[math.floor(areasize/2),math.floor(areasize/2)] for x in range(snakelength)]
snakeholder = snake[:]
dx = 0
dy = 0
generationsize = ""
individualnumber = ""
passed_info = list(sys.argv[1])
name = ""
generationnumber = ""
winflag = False
for x in range(len(passed_info)):
    if(passed_info[x] == " "):
        for y in range(x+1):
            del passed_info[0]
        break
    else:
        mutation_rate += passed_info[x]
mutation_rate = int(mutation_rate)
for x in range(len(passed_info)):
    if(passed_info[x] == " "):
        for y in range(x+1):
            del passed_info[0]
        break
    else:
        gain_buff += passed_info[x]
gain_buff = int(gain_buff)
for x in range(len(passed_info)):
    if(passed_info[x] == " "):
        for y in range(x+1):
            del passed_info[0]
        break
    else:
        generationsize += passed_info[x]
generationsize = int(generationsize)
for x in range(len(passed_info)):
    if(passed_info[x] == " "):
        for y in range(x+1):
            del passed_info[0]
        break
    else:
        generationnumber += passed_info[x]
generationnumber = generationnumber.replace('generation','')
generationnumber = int(generationnumber)
for x in range(len(passed_info)):
    if(passed_info[x] == " "):
        for y in range(x+1):
            del passed_info[0]
        break
    else:
        individualnumber += passed_info[x]
individualnumber = individualnumber.replace('individual','')
individualnumber = int(individualnumber)
np.random.seed(math.floor(time.time())+1+individualnumber)
gain = np.array(["" for x in range(generationsize)])
syn0 = np.array([[0 for x in range(4)] for y in range(areasize*areasize+areasize*4+4)])
asyn0 = []
if(generationnumber > 0):
    for y in range(generationsize):
        weights = ""
        publickey = open(str(mutation_rate)+" "+str(gain_buff)+" "+str(generationsize)+" generation"+str(generationnumber-1)+" individual"+str(y), 'r')
        data = list(publickey.read())
        for x in range(3):
            if(data[x] == " "):
                for g in range(x+1):
                    del data[0]
                break
            else:
                gain[y] = gain[y] + str(data[x])
        gain[y] = int(gain[y])
        weights = "".join(data)
        weights = np.array(ast.literal_eval(weights))
        asyn0.append(weights[0][:])
    asyn0 = np.array(asyn0)
    publickey.close()
    totalgain = 0
    parentgain = 0
    parentArray = [0 for x in range(generationsize+2)]
    for x in range(generationsize):
        totalgain = totalgain+(int(gain[x])**gain_buff)
    for x in range(generationsize):
        if(x != 0):
            parentArray[x] = parentArray[x-1]+int(gain[x-1])**gain_buff/totalgain
        else:
            parentArray[x] = 0
    parentArray[generationsize] = 1
    for x in range(parent_number):
        holder = random.random()
        for y in range(generationsize):
            if(holder>=parentArray[y] and holder<=parentArray[y+1]):
                syn0 = syn0+asyn0[y]
                parentgain = parentgain+(int(gain[y])**gain_buff)
                break
    syn0 = syn0/parent_number
    for x in range(mutation_rate):
        if(random.random()<mutation_chance):
            syn0[math.floor(len(syn0)*random.random())][math.floor(len(syn0[0])*random.random())] += mutation_strength*(2*np.random.random()-1)
    syn0 = np.around(syn0, decimals = 5)
else:
    syn0 = np.around(2*np.random.random((areasize*areasize+areasize*4+4,4)) - 1, decimals = 5)
def nonlin(x,deriv=False):
	if(deriv==True):
		return x*(1-x)
	return 1/(1+np.exp(-x))
def snakeNN():
    global snake
    global areasize
    global syn0
    screen = [0 for x in range(areasize*areasize+areasize*4+4)]
    for x in range(snakelength-1):
        screen[snake[x][0]+snake[x][1]*areasize] = 1
    screen[areasize*areasize+modifiedluxor.spritex[1]-1] = 1
    screen[areasize*areasize+areasize+modifiedluxor.spritey[1]-1] = 1
    screen[areasize*areasize+areasize*2+modifiedluxor.spritex[snakelength+1]-1] = 1
    screen[areasize*areasize+areasize*3+modifiedluxor.spritey[snakelength+1]-1] = 1
    if(dx == 1):
        screen[areasize*areasize+areasize*4] = 1
    if(dx == -1):
        screen[areasize*areasize+areasize*4+1] = 1
    if(dy == 1):
        screen[areasize*areasize+areasize*4+2] = 1
    if(dy == -1):
        screen[areasize*areasize+areasize*4+3] = 1
    l0 = np.array(screen)
    l1 = nonlin(np.dot(l0,syn0))
    total = 0
    greatest = 0
    for x in range(4):
        total += l1[x]
    l1 = l1/total
    for x in range(4):
        if(l1[x] >= l1[greatest]):
            greatest = x
    fixedl1 = np.array([0 for x in range(4)])
    fixedl1[greatest] = 1
    return fixedl1
def snakeMovement():
    global snake
    global snakeholder
    global dx
    global dy
    global snakelength
    global lose
    global movecounter
    global winflag
    if(snake[snakelength-1][0]+dx == modifiedluxor.spritex[1] and snake[snakelength-1][1]+dy == modifiedluxor.spritey[1]):
        movecounter = 0
        snake.append([modifiedluxor.spritex[1],modifiedluxor.spritey[1]])
        snakelength = len(snake)
        modifiedluxor.sprite(modifiedluxor.spritex[1],modifiedluxor.spritey[1],"O",modifiedluxor.colors.magenta,snakelength+1, False)
        modifiedluxor.spritex[1] = math.floor(areasize*random.random())
        modifiedluxor.spritey[1] = math.floor(areasize*random.random())
        myflag = True
        while(True):
            if(snakelength == areasize*areasize):
                winflag = True
                break
            for x in range(snakelength):
                if(snake[x][0] == modifiedluxor.spritex[1] and snake[x][1] == modifiedluxor.spritey[1]):
                    myflag = False
            if(myflag):
                break
            if(myflag == False):
                modifiedluxor.spritex[1] = math.floor(areasize*random.random())
                modifiedluxor.spritey[1] = math.floor(areasize*random.random())
                myflag = True
    else:
        snakeholder = snake[:]
        if(snake[snakelength-1][0]+dx<0 or snake[snakelength-1][1]+dy<0 or snake[snakelength-1][0]+dx>areasize-1 or snake[snakelength-1][1]+dy>areasize-1):
            lose = True
        for x in range(snakelength):
            if(snake[snakelength-1][0]+dx == snake[x][0] and snake[snakelength-1][1]+dy == snake[x][1] and x != snakelength-1):
                lose = True
            if(x == snakelength-1):
                snakeholder[x] = [snake[x][0]+dx,snake[x][1]+dy]
            else:
                snakeholder[x] = snake[x+1]
            modifiedluxor.spritex[x+2] = snakeholder[x][0]
            modifiedluxor.spritey[x+2] = snakeholder[x][1]
        snake = snakeholder[:]
def customcontrols():
    global dx
    global dy
    output = snakeNN()
    if(output[0] == 1 and dx != 1):
        dx = -1
        dy = 0
        modifiedluxor.key = 0
    elif(output[1] == 1 and dx != -1):
        dx = 1
        dy = 0
        modifiedluxor.key = 0
    elif(output[2] == 1 and dy != 1):
        dx = 0
        dy = -1
        modifiedluxor.key = 0
    elif(output[3] == 1 and dy != -1):
        dx = 0
        dy = 1
        modifiedluxor.key = 0
modifiedluxor.changeScreen(areasize,areasize)
modifiedluxor.sprite(math.floor(areasize*random.random()),math.floor(areasize*random.random()),"0",modifiedluxor.colors.cyan,1, False)
modifiedluxor.sprite(1,1,"O",modifiedluxor.colors.magenta,2, False)
movecounter = 0
while(True):
    modifiedluxor.refreshbackground(" ", modifiedluxor.colors.green, backgroundcolor = modifiedluxor.backcolor.blue)
    modifiedluxor.speech1 = movecounter
    modifiedluxor.speech2 = ""
    customcontrols()
    snakeMovement()
    if(lose or movecounter>areasize*areasize+10 or winflag == True):
        modifiedluxor.key = 27
        break
    modifiedluxor.collisions()
    modifiedluxor.movement()
    modifiedluxor.graphics()
    movecounter += 1
    if(modifiedluxor.key==27):
        break
generation = ""
"""
if __name__ == "__main__":
    passed_info = sys.argv[1]
    print(passed_info)
    for x in range(len(passed_info)):
        if(passed_info[x] == " "):
            for y in range(x+1):
                del passed_info[0]
            break
        else:
            generation += passed_info[x]
            """
passed_info = sys.argv[1]
publickey = open(passed_info, 'w+')
publickey.write(str(len(snake))+" ")
publickey.write("[")
publickey.write("[")
for x in range(len(syn0)):
    publickey.write("[")
    for y in range(len(syn0[x])):
        publickey.write(str(syn0[x][y]))
        if(y != len(syn0[x])-1):
            publickey.write(",")
    publickey.write("]")
    if(x != len(syn0)-1):
        publickey.write(",")
publickey.write("]")
publickey.write("]")
publickey.close()
modifiedluxor.user_input.stop()