import time
import luxor
import random
import os
import sys
import math
import numpy as np
import ast
luxor.refreshRate = .5
areasize = 10
snakelength = 1
lose = False
snake = [[math.floor(areasize/2),math.floor(areasize/2)] for x in range(snakelength)]
snakeholder = snake[:]
dx = 0
dy = 0
winflag = False
def snakeMovement():
    global snake
    global snakeholder
    global dx
    global dy
    global snakelength
    global lose
    global winflag
    if(snake[snakelength-1][0]+dx == luxor.spritex[1] and snake[snakelength-1][1]+dy == luxor.spritey[1]):
        snake.append([luxor.spritex[1],luxor.spritey[1]])
        snakelength = len(snake)
        luxor.sprite(luxor.spritex[1],luxor.spritey[1],"O",luxor.colors.magenta,snakelength+1, False)
        luxor.spritex[1] = math.floor(areasize*random.random())
        luxor.spritey[1] = math.floor(areasize*random.random())
        myflag = True
        if(dx == -1):
            luxor.spriteGraphical[len(snake)] = "O"
            luxor.spriteGraphical[len(snake)+1] = ">"
        elif(dx == 1):
            luxor.spriteGraphical[len(snake)] = "O"
            luxor.spriteGraphical[len(snake)+1] = "<"
        elif(dy == -1):
            luxor.spriteGraphical[len(snake)] = "O"
            luxor.spriteGraphical[len(snake)+1] = "V"
        elif(dy == 1):
            luxor.spriteGraphical[len(snake)] = "O"
            luxor.spriteGraphical[len(snake)+1] = "^"
        while(True):
            if(snakelength == areasize*areasize):
                winflag = True
                break
            for x in range(snakelength):
                if(snake[x][0] == luxor.spritex[1] and snake[x][1] == luxor.spritey[1]):
                    myflag = False
            if(myflag):
                break
            if(myflag == False):
                luxor.spritex[1] = math.floor(areasize*random.random())
                luxor.spritey[1] = math.floor(areasize*random.random())
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
            luxor.spritex[x+2] = snakeholder[x][0]
            luxor.spritey[x+2] = snakeholder[x][1]
        snake = snakeholder[:]
def customcontrols():
    global dx
    global dy
    if(luxor.key == 97 and dx != 1):
        dx = -1
        dy = 0
        luxor.spriteGraphical[len(snake)] = "O"
        luxor.spriteGraphical[len(snake)+1] = ">"
        luxor.key = 0
    elif(luxor.key == 100 and dx != -1):
        dx = 1
        dy = 0
        luxor.spriteGraphical[len(snake)] = "O"
        luxor.spriteGraphical[len(snake)+1] = "<"
        luxor.key = 0
    elif(luxor.key == 119 and dy != 1):
        dx = 0
        dy = -1
        luxor.spriteGraphical[len(snake)] = "O"
        luxor.spriteGraphical[len(snake)+1] = "V"
        luxor.key = 0
    elif(luxor.key == 115 and dy != -1):
        dx = 0
        dy = 1
        luxor.spriteGraphical[len(snake)] = "O"
        luxor.spriteGraphical[len(snake)+1] = "^"
        luxor.key = 0
luxor.changeScreen(areasize,areasize)
luxor.sprite(math.floor(areasize*random.random()),math.floor(areasize*random.random()),"0",luxor.colors.cyan,1, False)
luxor.sprite(1,1,"O",luxor.colors.magenta,2, False)
while(True):
    luxor.refreshbackground(" ", luxor.colors.green, backgroundcolor = luxor.backcolor.blue)
    luxor.speech1 = ""
    luxor.speech2 = ""
    customcontrols()
    snakeMovement()
    if(lose or winflag):
        break
    luxor.collisions()
    luxor.movement()
    luxor.graphics()
    if(luxor.key==27):
        break
print("your score is: "+str(len(snake)))
input("")