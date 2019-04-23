import pygame
from pygame.locals import *
import sys, os
pygame.init()

Screen = max(pygame.display.list_modes())
Surface = pygame.display.set_mode(Screen,FULLSCREEN)

Font = pygame.font.Font("/home/pi/photo-video-booth-code/Countdown/font.ttf",512)

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

Time = [20]
OriginalTime = list(Time)

test = Font.render("0",True,(255,0,0))
width = test.get_width()
height = test.get_height()
totalwidth = 2 * width

def quit():
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)
    pygame.quit(); sys.exit()
def GetInput():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: quit()
mode = "counting"
def Update():
    global mode,Time
    if mode == "counting":
        Time[0] -= 1
        if Time[0] < 0:
            mode = "end"
    else:
            mode = "end"
def Draw():
    Surface.fill((0,0,0))
    t0 = str(Time[0])
    if len(t0) == 1: t0 = "0"+t0
    string = t0
    # End should be 100 for > 9 and 20 for <=9
    if Time[0] > 9:
        start_pos = (Screen[0]/2)-(totalwidth/2)-100
    else:
        start_pos = (Screen[0]/2)-(totalwidth/2)-20
    for character in string:
        if character != "1":
            pos = [start_pos,(Screen[1]/2)-(height/2)]
        else:
            pos = [start_pos+int(round((51.0/99.0)*width)),(Screen[1]/2)-(height/2)]
        Surface.blit(Font.render(character,True,(255,0,0)),pos)
        start_pos += width
        #start_pos_b += width
    pygame.display.flip()

def main():
    Clock = pygame.time.Clock()
    while True:
        GetInput()
        Update()
        Draw()
        Clock.tick(1)

if __name__ == '__main__': main()
