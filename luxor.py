#!/usr/bin/python2.7
import threading
import time
from msvcrt import getch
import os
from pygame import mixer

global key
global speech1
global speech2
speech1 = ""
speech2 = ""
key = 0
refreshRate = .10
screenlength = 15
screenheight = 10
spritenumber = 100
Graphical = [["" for i in range(screenheight)] for j in range(screenlength)]
spriteGraphical = ["" for i in range(spritenumber)]
color = [["37" for i in range(screenheight)] for j in range(screenlength)]
spritecolor = ["37" for i in range(spritenumber)]
backgroundColor = [["40" for i in range(screenheight)] for j in range(screenlength)]
style = [["1" for i in range(screenheight)] for j in range(screenlength)] #1-bright 2-underlined 3-negative 4-underline
init = [False for y in range(spritenumber)]
spritex = [0 for x in range(spritenumber)]
spritey = [0 for y in range(spritenumber)]
collision = [0 for x in range(spritenumber)]
dx = [0 for x in range(spritenumber)]
dy = [0 for y in range(spritenumber)]

def clear():
    return os.system('cls')

def sleep(value):
    return time.sleep(value)

def user_input():
    while True:
        global key
        while(key == 0):
            key = ord(getch())
        if (key==27):
            break

def playsong(songname):
    mixer.init()
    mixer.music.load(songname)
    mixer.music.play()
def changeScreen(length,height):
    global Graphical
    global color
    global backgroundColor
    global style
    global screenheight 
    screenheight = height
    global screenlength
    screenlength = length
    Graphical = [["" for i in range(height)] for j in range(length)]
    color = [["37" for i in range(height)] for j in range(length)]
    backgroundColor = [["40" for i in range(height)] for j in range(length)]
    style = [["1" for i in range(height)] for j in range(length)] #1-bright 2-underlined 3-negative 4-underline

def collisions():
    for j in range(100):
        if(collision[j]):
            for i in range(100):
                if(collision[i]):
                    if(spritex[j]+dx[j] == spritex[i] and spritey[j]+dy[j] == spritey[i]):
                        dx[j] = 0
                        dy[j] = 0
        if(spritex[j]+dx[j]>screenlength-1 or spritex[j]+dx[j]<0 or spritey[j]+dy[j]>screenheight-1 or spritey[j]+dy[j]<0):
            dx[j] = 0
            dy[j] = 0

def controls():
    global key
    global dx
    global dy
    if(key == 97):
        dx[0] = -1
        dy[0] = 0
        key = 0
    elif(key == 100):
        dx[0] = 1
        dy[0] = 0
        key = 0
    elif(key == 119):
        dx[0] = 0
        dy[0] = -1
        key = 0
    elif(key == 115):
        dx[0] = 0
        dy[0] = 1
        key = 0
    else:
        dx[0] = 0
        dy[0] = 0

def movement():
    global spritex
    global spritey
    for j in range(100):
        spritex[j] += dx[j]
        spritey[j] += dy[j]

def graphics():
    global speech1
    global speech2
    global screenlength
    global screenheight
    global refreshRate
    for i in range(spritenumber):
        j = spritenumber-i-1
        if(init[j]):
            Graphical[spritex[j]][spritey[j]] = spriteGraphical[j] 
            color[spritex[j]][spritey[j]] = spritecolor[j] 
    clear()
    for y in range(screenheight):
        for x in range(screenlength):
            graphicString = "\033["+style[x][y]+";"+color[x][y]+";"+backgroundColor[x][y]+"m"+Graphical[x][y]+"\033[0;37;40m"
            print(graphicString, end="")
        print("")
    print(speech1)
    print(speech2)
    speech1 = ""
    speech2 = ""
    time.sleep(refreshRate)
    
threadcount = 0
thread_list = []
rawInputThread = threading.Thread(target=user_input)
thread_list.append(rawInputThread)
#userInputThread = threading.Thread(target=user_input)
#thread_list.append(userInputThread)
for thread in thread_list:
    thread.start()
# This blocks the calling thread until the thread whose join() method is called is terminated.
# From http://docs.python.org/2/library/threading.html#thread-objects
#for thread in thread_list:
#    if (threadcount==0):
#        thread.join()#makes the joined threads and the main code wait together until continuing
#    threadcount += 1

def refreshbackground(texturestuff, charcolor, **options):
    for x in range(len(Graphical)):
        for y in range(len(Graphical[x])):
            Graphical[x][y] = str(texturestuff)
            color[x][y] = charcolor
            if(options.get("backgroundcolor") != None):
                backgroundColor[x][y] = options.get("backgroundcolor")

def createborder(charcolor):
    for x in range(len(Graphical)):
        for y in range(len(Graphical[x])):
            if(x == 0 or x == screenlength-1):
                Graphical[x][y] = "|"
                color[x][y] = charcolor
            if(y == 0 or y == screenheight-1):
                Graphical[x][y] = "-"
                color[x][y] = charcolor
            Graphical[0][0] = "+"
            Graphical[0][screenheight-1] = "+"
            Graphical[screenlength-1][0] = "+"
            Graphical[screenlength-1][screenheight-1] = "+"
            color[0][0] = charcolor
            color[0][screenheight-1] = charcolor
            color[screenlength-1][0] = charcolor
            color[screenlength-1][screenheight-1] = charcolor

class colors:
    blue = "94"
    magenta = "35"
    cyan = "36"
    darkgray = "30"
    yellow = "93"
    red = "91"
    green = "0"
    purple = "1"
    white = "37"

class backcolor:
    black = "40"
    green = "42"
    red = "41"
    yellow = "43"
    blue = "44"
    pink = "45"
    cyan = "46"
    gray = "47"

class styles:
    dark = "0"
    bright = "1"
    underline = "4"

def sprite(x,y,character,charcolor,spriteid,collisions):
    if(init[spriteid] == False):
        init[spriteid] = True
        spritex[spriteid] = x
        spritey[spriteid] = y
        collision[spriteid] = collisions
        spriteGraphical[spriteid] = character
        spritecolor[spriteid] = charcolor

def onsprite(spriteid):
    if(spritex[0] == spritex[spriteid] and spritey[0] == spritey[spriteid]):
        return True
    else:
        return False

def spriteonsprite(spriteid1,spriteid2):
    if(spritex[spriteid1] == spritex[spriteid2] and spritey[spriteid1] == spritey[spriteid2]):
        return True
    else:
        return False

def nearsprite(spriteid):
    if(((spritex[0]==spritex[spriteid]-1 or spritex[0] == spritex[spriteid]+1) and spritey[0] == spritey[spriteid]) or ((spritey[0]==spritey[spriteid]-1 or spritey[0] == spritey[spriteid]+1) and spritex[0] == spritex[spriteid])):
        return True
    else:
        return False