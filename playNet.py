import time
import modifiedluxor
import random
import os
import sys
import math
import numpy as np
import ast
modifiedluxor.refreshRate = .5
areasize = 3
os.system('start python playerGame.py ')
generationnumber = int(input("generation: "))
individualnumber = int(input("individual: "))
x = 0
while(True):
    if(os.path.isfile(str(x)+" generation"+str(generationnumber)+" individual"+str(individualnumber))):
        generationsize = x
        break
    x += 1
snakelength = 1
lose = False
snake = [[math.floor(areasize/2),math.floor(areasize/2)] for x in range(snakelength)]
snakeholder = snake[:]
dx = 0
dy = 0
winflag = False
np.random.seed(math.floor(time.time())+1+individualnumber)
gain = np.array(["" for x in range(generationsize)])
syn0 = []
weights = ""
publickey = open(str(generationsize)+" generation"+str(generationnumber)+" individual"+str(individualnumber), 'r')
data = list(publickey.read())
for x in range(3):
    if(data[x] == " "):
        for g in range(x+1):
            del data[0]
        break
weights = "".join(data)
weights = np.array(ast.literal_eval(weights))
syn0.append(weights[0][:])
syn0 = np.array(syn0[0])
publickey.close()
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
        if(dx == -1):
            modifiedluxor.spriteGraphical[len(snake)] = "O"
            modifiedluxor.spriteGraphical[len(snake)+1] = ">"
        elif(dx == 1):
            modifiedluxor.spriteGraphical[len(snake)] = "O"
            modifiedluxor.spriteGraphical[len(snake)+1] = "<"
        elif(dy == -1):
            modifiedluxor.spriteGraphical[len(snake)] = "O"
            modifiedluxor.spriteGraphical[len(snake)+1] = "V"
        elif(dy == 1):
            modifiedluxor.spriteGraphical[len(snake)] = "O"
            modifiedluxor.spriteGraphical[len(snake)+1] = "^"
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
        modifiedluxor.spriteGraphical[len(snake)] = "O"
        modifiedluxor.spriteGraphical[len(snake)+1] = ">"
        modifiedluxor.key = 0
    elif(output[1] == 1 and dx != -1):
        dx = 1
        dy = 0
        modifiedluxor.spriteGraphical[len(snake)] = "O"
        modifiedluxor.spriteGraphical[len(snake)+1] = "<"
        modifiedluxor.key = 0
    elif(output[2] == 1 and dy != 1):
        dx = 0
        dy = -1
        modifiedluxor.spriteGraphical[len(snake)] = "O"
        modifiedluxor.spriteGraphical[len(snake)+1] = "V"
        modifiedluxor.key = 0
    elif(output[3] == 1 and dy != -1):
        dx = 0
        dy = 1
        modifiedluxor.spriteGraphical[len(snake)] = "O"
        modifiedluxor.spriteGraphical[len(snake)+1] = "^"
        modifiedluxor.key = 0
modifiedluxor.changeScreen(areasize,areasize)
modifiedluxor.sprite(math.floor(areasize*random.random()),math.floor(areasize*random.random()),"0",modifiedluxor.colors.cyan,1, False)
modifiedluxor.sprite(1,1,"O",modifiedluxor.colors.magenta,2, False)
movecounter = 0
while(True):
    modifiedluxor.refreshbackground(" ", modifiedluxor.colors.green, backgroundcolor = modifiedluxor.backcolor.blue)
    modifiedluxor.speech1 = ""
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
print(("score "+str(len(snake))))
input("press enter to exit")
modifiedluxor.user_input.stop()