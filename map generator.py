import math
import random
import time
import numpy as np
import heapq
import pygame




pygame.init()

screen_width = 1000
screen_height = 1000
grid_size = 20

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption("Map generator")
pygame.display.set_icon(pygame.image.load("img/logo.png"))

tile_size = screen_height / grid_size

arr = [[0 for y in range(grid_size)] for x in range(grid_size)]
# fill borders
for i in range(0, grid_size):
    arr[i][0] = 1
    arr[0][i] = 1
    arr[i][grid_size - 1] = 1
    arr[grid_size - 1][i] = 1

#arr = []

def drawArray():
    global arr
    screen.fill((0,0,0))
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            x = j * tile_size
            y = i * tile_size
            color0 = (231,223,194)
            color1 = (86,67,43)
            color2 = (141,114,76)

            if arr[i][j] == 0:
                pygame.draw.rect(screen, color0, (x, y, tile_size, tile_size))
                pygame.draw.rect(screen, (255,255,255), (x - 1, y - 1, tile_size, tile_size), 2)
            else:
                pygame.draw.rect(screen, color1, (x, y, tile_size, tile_size))
                pygame.draw.rect(screen, color2, (x - 2, y - 2, tile_size, tile_size), 4)
            #pygame.draw.circle(screen, color0, (x, y), tile_size)

def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def gap():
    x, y = pygame.mouse.get_pos()
    i = int(map(y, 0, screen_height, 0, grid_size))
    j = int(map(x, 0, screen_height, 0, grid_size))
    arr[i][j] = 1 - arr[i][j]
    #arr[i][grid_size - j - 1] = arr[i][j]
    # arr[grid_size - i - 1][grid_size - j - 1] = arr[i][j]
    #arr[grid_size - i - 1][j] = arr[i][j]
    print(arr)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            gap()


    drawArray()
    pygame.display.update()


