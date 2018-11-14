# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:29:26 2018

@author: edwar
"""

from tkinter import *
from random import randint
from math import sqrt
import sys

screenWidth = 640
screenHeight = 480

screen = Tk()
screen.title("Lightning!")

screenCanvas = Canvas(screen, width=screenWidth, height=screenHeight)
screenCanvas.pack()

def findMidpoint(p1, p2):
    return( ( p1[0] + ( (p2[0] - p1[0]) / 2), p1[1] + ( (p2[1] - p1[1]) / 2) ) )
    
def findDist(p1, p2):
    return sqrt( ((p2[1]-p1[1])**2) + ((p2[0]-p1[0])**2) )

def createFractalPoints(startPoint, endPoint, maxDepth, offset):
    points = [startPoint, endPoint]
    for times in range(1,maxDepth+1):
        newPoints = []
        for point in range(len(points[:-1])):
            newPoints.append(points[point])
            nextPoint = list(points[point+1])
            randomOffset = randint(int(-(findDist(points[point],nextPoint)/offset)),int(findDist(points[point],nextPoint)/offset))
            if startPoint[0] == endPoint[0]:
                nextPoint[0] += randomOffset
            else:
                nextPoint[1] += randomOffset
            newPoints.append((findMidpoint(points[point],nextPoint)))
        newPoints.append(points[-1])
        points = newPoints
    
    return points

def drawPointsLightning(points, c):
    c.create_rectangle(0,0,screenWidth,screenHeight,fill="#000000")
    for point in range(len(points[:-1])):
        c.create_line(points[point][0], points[point][1], points[point+1][0], points[point+1][1], fill="#ffffff", width=1)
                    
def drawPointsHill(points, c):
    c.create_rectangle(0,0,screenWidth,screenHeight,fill="#7ec7ee")
    for point in points:
        c.create_line(point[0], point[1], point[0], screenHeight, fill = "#00ff00")

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        if int(sys.argv[1]) == 0:
            depth = 8
            startPointLightning = (screenWidth/2, 0)
            endPointLightning = (screenWidth/2, screenHeight)
            lightningOffset = 2
            pointsLightning = createFractalPoints(startPointLightning, endPointLightning, depth, lightningOffset)
            
            drawPointsLightning(pointsLightning, screenCanvas)
        elif int(sys.argv[1]) == 1:
    
            depth = 10
            startPointHill = (0, screenHeight/2)
            endPointHill = (screenWidth, screenHeight/2)
            hillOffset = 3
            
            pointsHill = createFractalPoints(startPointHill, endPointHill, depth, hillOffset)
            drawPointsHill(pointsHill, screenCanvas)
    else:
        depth = 8
        startPointLightning = (screenWidth/2, 0)
        endPointLightning = (screenWidth/2, screenHeight)
        lightningOffset = 2
        pointsLightning = createFractalPoints(startPointLightning, endPointLightning, depth, lightningOffset)
        
        drawPointsLightning(pointsLightning, screenCanvas)
    screen.mainloop()