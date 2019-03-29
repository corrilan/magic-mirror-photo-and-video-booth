#!/usr/bin/python3

# Fonts used in GIMP created overlays are Chilanka and Courier 10 Pitch

# The following are just notes, not all packages may be required:

# apt-get install bc unclutter omxplayer python-picamera python3-picamera python-rpi-gpio feh python-imaging python-image-tk imagemagick python-matplotlib python-paramiko open-sshserver vim autossh screen
# pip3 install python-vlc
# pip3 install mysql-connector
# pip install pyrtlsdr
# pip3 install opencv-python and perhaps:
# apt-get install libatlas-base-dev
# apt-get install libjasper-dev
# apt-get install libqtgui4
# apt-get install python3-pyqt5
# apt-get install libqt4-test

from subprocess import call
import RPi.GPIO as GPIO  
import time
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from pygame import mixer
from numpy import random
import os
from datetime import datetime as dt
from threading import Thread
import threading
import cv2
from shutil import copyfile
import re

# Graphics initialization
WINDOW_WIDTH = 1016
WINDOW_HEIGHT = 1856
full_screen = False
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
pygame.init() 
if full_screen:
    surf = pygame.display.set_mode(window_size, HWSURFACE | FULLSCREEN | DOUBLEBUF | NOFRAME)
else:
    surf = pygame.display.set_mode(window_size)

# Options
CODE_PATH = "/home/pi/photo-video-booth-code"
PREVIEW = 0
EVENT = "CHRISTENING" # NONE WEDDING CHRISTMAS EASTER BIRTHDAY CHRISTENING MURDER-MYSTERY HALLOWEEN HENPARTY STAGPARTY FUNERAL BARMITZVA
OVERLAY_TEXT = "Lynsey & Jason 28/02/2019" # Not yet working, overlay text currently within GIMP created graphic file
MATRIX = "False"
GHOST = "False"
FOG = "False"
ZOMBIES = "False"
BALLOONS = "False"
TAKE_PHOTO_COUNT = 3
TAKE_VIDEO_CLIP_LENGTH = 20 # In seconds
BLUE_BUTTON_FOR_LYNSEY_SHORTS = "False" # Make blue button show short films if blue button is active
MINUTE_BASED_EFFECTS = "TRUE"
ACTIVE_BLUE_BUTTON = "FALSE" # Activate the blue button
#BOUNCETIME = 20000 # In milliseconds 

# Video Resolution
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
#VIDEO_WIDTH = 1280
#VIDEO_HEIGHT = 720

# Photo Resolution
PHOTO_WIDTH = 960
PHOTO_HEIGHT = 720
#PHOTO_WIDTH = 1920
#PHOTO_HEIGHT = 1080
#PHOTO_WIDTH = 1920
#PHOTO_HEIGHT = 1440
#PHOTO_WIDTH = 2592
#PHOTO_HEIGHT = 1944
#PHOTO_WIDTH = 1280
#PHOTO_HEIGHT = 720

# Button LED GPIO pins
RED_LED_PIN = 17 # Yellow cable
BLUE_LED_PIN = 19 # Yellow cable
RED_BUTTON_PIN = 18 # Red cable
BLUE_BUTTON_PIN = 16 # Red cable
# Connect the green cable to GND

# Global variables
cb_red = 0
cb_blue = 0
cb_blue_matrix_crash = 0
cb_blue_lynsey_shorts = 0
timestr = time.strftime("%Y%m%d-%H%M%S")
RUN_INSTRUCTIONS = "TRUE"
BUSY = "FALSE"
SHOW_RECORDING_INDICATOR = "FALSE"
Time = [20]
mode = "counting"

# Define the looped instructions screens which run until a button is pressed
def show_instructions():
    global cb_blue
    global cb_blue_matrix_crash
    global cb_blue_lynsey_shorts
    global ZOMBIES
    global FOG
    global GHOST
    global BALLOONS

    while True:
        if RUN_INSTRUCTIONS == "FALSE":
            return
        
        if MINUTE_BASED_EFFECTS == "TRUE":
            check_minutes_past_hour()
        
        if MATRIX == "True":
            GPIO.remove_event_detect(BLUE_BUTTON_PIN)
            cb_blue_matrix_crash = ButtonHandler(BLUE_BUTTON_PIN, matrix_crash, edge='falling', bouncetime=100)
            cb_blue_matrix_crash.start()
            GPIO.add_event_detect(BLUE_BUTTON_PIN, GPIO.FALLING, callback=cb_blue_matrix_crash) # Part of workaround
            #GPIO.add_event_detect(BLUE_BUTTON_PIN, GPIO.FALLING, callback = matrix_crash, bouncetime = BOUNCETIME) # Disabled as part of workaround
        else:
            if BLUE_BUTTON_FOR_LYNSEY_SHORTS == "False":
                if ACTIVE_BLUE_BUTTON == "TRUE":
                    GPIO.remove_event_detect(BLUE_BUTTON_PIN)
                    cb_blue = ButtonHandler(BLUE_BUTTON_PIN, take_video, edge='falling', bouncetime=100)
                    cb_blue.start()
                    GPIO.add_event_detect(BLUE_BUTTON_PIN, GPIO.FALLING, callback=cb_blue)
                    #GPIO.remove_event_detect(BLUE_BUTTON_PIN) # Turned off due to workaround
                    #GPIO.add_event_detect(BLUE_BUTTON_PIN, GPIO.FALLING, callback=cb_blue) # Part of workaround
                    #GPIO.add_event_detect(BLUE_BUTTON_PIN, GPIO.FALLING, callback = take_video, bouncetime = BOUNCETIME) # Turned off due to workaround
            if BLUE_BUTTON_FOR_LYNSEY_SHORTS == "True":
                GPIO.remove_event_detect(BLUE_BUTTON_PIN)
                cb_blue_lynsey_shorts = ButtonHandler(BLUE_BUTTON_PIN, lynsey_shorts, edge='falling', bouncetime=100)
                cb_blue_lynsey_shorts.start()
                GPIO.add_event_detect(BLUE_BUTTON_PIN, GPIO.FALLING, callback=cb_blue_lynsey_shorts)

        if RUN_INSTRUCTIONS == "FALSE":
            return

        surf.fill(pygame.Color("black"))
        pygame.display.update()

        if RUN_INSTRUCTIONS == "FALSE":
            return

        pygame.mouse.set_visible(0)

        if RUN_INSTRUCTIONS == "FALSE":
            return

        if EVENT == "CHRISTMAS":
            event_instructions_graphic("top")
        
        if RUN_INSTRUCTIONS == "FALSE":
            return

        if MATRIX == "True":
            text = ["This is your last chance.", "After this there is no", "turning back."]
            display_box(surf, text, 90, 0, 700, 255, 255, 255, False, False)
        else:
            text = ["Hello,"]
            display_box(surf, text, 150, 25, 200, 255, 255, 255, False, False)
            time.sleep(5)
            surf.fill(pygame.Color("black"))
            text = ["dress up"]
            display_box(surf, text, 100, 25, 400, 255, 255, 255, False, False)
            time.sleep(0.75)
            surf.fill(pygame.Color("black"))
            text = ["and leave a"]
            display_box(surf, text, 100, 25, 600, 255, 255, 255, False, False)
            time.sleep(0.75)
            surf.fill(pygame.Color("black"))
            text = ["photo for Leon."]
            display_box(surf, text, 100, 25, 800, 255, 255, 255, False, False)
            time.sleep(0.75)
            surf.fill(pygame.Color("black"))
       
        if RUN_INSTRUCTIONS == "FALSE":
            return

        #time.sleep(5)
        surf.fill(pygame.Color("black"))
    
        if RUN_INSTRUCTIONS == "FALSE":
            return

        if EVENT == "CHRISTMAS":
            event_instructions_graphic("christmas", "top")

        if RUN_INSTRUCTIONS == "FALSE":
            return

        if MATRIX == "True":
            text = ["You take the blue pill, the", "story ends. You wake up in your", "bed and believe whatever", "you want to", "believe."]
            display_box(surf, text, 75, 0, 100, 0, 0, 255, True, True)
            display_button_image(surf, "%s/media/big-blue-button.jpg" % CODE_PATH, 8)
            time.sleep(5)
            remove_button_image(surf, "%s/media/big-blue-button.jpg" % CODE_PATH, 8)
            surf.fill(pygame.Color("black"))
        else:
            text = ["press the big red button", "to take %s photos," % TAKE_PHOTO_COUNT ]
            display_box(surf, text, 75, 150, 400, 255, 0, 0, True, True)
            display_button_image(surf, "%s/media/big-red-button.jpg" % CODE_PATH, 5)
            time.sleep(5)
            remove_button_image(surf, "%s/media/big-red-button.jpg" % CODE_PATH, 5)
            surf.fill(pygame.Color("black"))

        if RUN_INSTRUCTIONS == "FALSE":
            return

        if MATRIX == "True":
            text = ["You take the red pill, you", "stay in Wonderland, and I show", "you how deep the rabbit-hole", "goes. Remember, all I am", "offering is %s photos." % TAKE_PHOTO_COUNT, "Nothing more."]
            display_box(surf, text, 75, 0, 100, 255, 0, 0, True, True)
            display_button_image(surf, "%s/media/big-red-button.jpg" % CODE_PATH, 5)
            time.sleep(5)
            remove_button_image(surf, "%s/media/big-red-button.jpg" % CODE_PATH, 5)
            surf.fill(pygame.Color("black"))
        else:
            if BLUE_BUTTON_FOR_LYNSEY_SHORTS == "False":
                if ACTIVE_BLUE_BUTTON == "TRUE":
                    text = ["press the big blue button", "to record a %s second video" % TAKE_VIDEO_CLIP_LENGTH , "message."]
                    display_box(surf, text, 75, 125, 200, 0, 0, 255, True, True)
                    display_button_image(surf, "%s/media/big-blue-button.jpg" % CODE_PATH, 8)
                    time.sleep(5)
                    remove_button_image(surf, "%s/media/big-blue-button.jpg" % CODE_PATH, 8)
                    surf.fill(pygame.Color("black"))
 
            if BLUE_BUTTON_FOR_LYNSEY_SHORTS == "True":
                text = ["press the big blue button", "to watch one of Lynsey's", "short films."]
                display_box(surf, text, 75, 125, 200, 0, 0, 255, True, True)
                display_button_image(surf, "%s/media/big-blue-button.jpg" % CODE_PATH, 8)
                time.sleep(5)
                remove_button_image(surf, "%s/media/big-blue-button.jpg" % CODE_PATH, 8)
                surf.fill(pygame.Color("black"))
        
        if RUN_INSTRUCTIONS == "FALSE":
            return

        if EVENT == "CHRISTMAS":
            event_instructions_graphic("christmas", "top")

        if RUN_INSTRUCTIONS == "FALSE":
            return

        text = ["   Download", "    your", "            photos", "              at"]

        if RUN_INSTRUCTIONS == "FALSE":
            return

        display_download_message(surf, text, 175, 8, 255, 255, 0, False, True)

        if RUN_INSTRUCTIONS == "FALSE":
            return

        time.sleep(2)
        surf.fill(pygame.Color("black"))

        if RUN_INSTRUCTIONS == "FALSE":
            return

        if EVENT == "CHRISTMAS":
            event_instructions_graphic("christmas", "bottom")

        if RUN_INSTRUCTIONS == "FALSE":
            return

        if EVENT == "WEDDING":
            event_instructions_graphic("wedding", "bottom")

        if EVENT == "CHRISTENING":
            event_instructions_graphic("christening", "bottom")

        if RUN_INSTRUCTIONS == "FALSE":
            return

        text = ["jason-and-lynsey.com"]

        if RUN_INSTRUCTIONS == "FALSE":
            return

        display_download_url(surf, text, 50, 2.5, 255, 255, 0, False, True)
        
        if RUN_INSTRUCTIONS == "FALSE":
            return

        time.sleep(3)
        surf.fill(pygame.Color("black"))
        pygame.display.update()

        if RUN_INSTRUCTIONS == "FALSE":
            return
        
        time.sleep(10)

        if FOG == "True":
            waiting_screen_video("fog")
            time.sleep(10)
            FOG = "False";

        if GHOST == "True":
            waiting_screen_video("ghost")
            time.sleep(10)
            GHOST = "False";

        if ZOMBIES == "True":
            waiting_screen_video("zombies")
            time.sleep(10)
            ZOMBIES = "False";

        if BALLOONS == "True":
            waiting_screen_video("balloons")
            time.sleep(10)
            BALLOONS = "False";

# Display random short film when blue button is pressed and feature is active
def lynsey_shorts(self):
    GPIO.remove_event_detect(RED_BUTTON_PIN)
    GPIO.remove_event_detect(BLUE_BUTTON_PIN)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)
    global RUN_INSTRUCTIONS
    global BUSY
    BUSY = "TRUE"
    RUN_INSTRUCTIONS = "FALSE"
    surf.fill(pygame.Color("black"))
    pygame.display.update()
    random_file = random.choice(os.listdir("%(CODE_PATH)s/media/lynseys-short-films" % {'CODE_PATH': CODE_PATH} ))
    movie_path = ("%(CODE_PATH)s/media/lynseys-short-films/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'random_file': random_file})
    if random_file == "08-night-of-the-living-wed-trailer.mp4":
        show_short_film_title(random_file, 75, 100)
    else: 
        text = ["Recorded for the Empire", "Done In 60 Seconds competition,", "recreating a known film in", "60 seconds."]
        display_box(surf, text, 60, 75, 100, 0, 0, 255, True, True)
    show_short_film_title(random_file, 100, 1500)
    call(["omxplayer", "--no-keys", "--no-osd", "--aspect-mode", "letterbox", movie_path])
    time.sleep(5)
    BUSY = "FALSE"

# Display the short film title as based on the file name
def show_short_film_title(random_file, x, y):
    #film_title_array = iter(re.split('[-.]', random_file))
    film_title_array = re.split('[-.]', random_file)
    title = ""
    #next(film_title_array)
    for word in film_title_array[1:-1]:
        title = title + word.capitalize() + " "
    text2 = ["Now showing:", title]
    display_box(surf, text2, 60, x, y, 0, 0, 255, True, True)

# If blue button is pressed within first minute of hour, show The Matrix related System Error video and then reboot for fun (part of film themed wedding scenario)
def matrix_crash(self):
    GPIO.remove_event_detect(RED_BUTTON_PIN)
    GPIO.remove_event_detect(BLUE_BUTTON_PIN)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)
    global RUN_INSTRUCTIONS
    global BUSY
    BUSY = "TRUE"
    RUN_INSTRUCTIONS = "FALSE"
    surf.fill(pygame.Color("black"))
    pygame.display.update()
    movie_path = ('%s/media/the-matrix-system-failure-with-sound.mp4' % CODE_PATH)
    call(["omxplayer", "--no-keys", "--no-osd", "--aspect-mode", "stretch", movie_path])
    call(["/sbin/reboot"])

def event_instructions_graphic(event, location):
    random_file = random.choice(os.listdir("%(CODE_PATH)s/media/%(event)s-instructions/%(location)s" % {'CODE_PATH': CODE_PATH, 'event': event, 'location': location} ))
    display_event_image(surf, "%(CODE_PATH)s/media/%(event)s-instructions/%(location)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'event': event, 'location': location, 'random_file': random_file}, location)

# Define how to play a video file at end of instructions sequence
def waiting_screen_video(theme):
    random_file = random.choice(os.listdir("%(CODE_PATH)s/media/waiting-screen-videos/%(event)s/%(theme)s" % {'CODE_PATH': CODE_PATH, 'event': EVENT.lower(), 'theme': theme}))
    movie_path = ('%(CODE_PATH)s/media/waiting-screen-videos/%(event)s/%(theme)s/%(file)s' % {'CODE_PATH': CODE_PATH, 'event': EVENT.lower(), 'theme': theme, 'file': random_file})
    mute_or_unmute = random_file.split('-')[0] # Whether to play audio or not  is defined in the filename
    aspect_mode = random_file.split('-')[1] # Aspect mode is defined in the filename
    orientation = random_file.split('-')[2] # Whether random or specific orientation is defined in the filename

    if (mute_or_unmute == "mute"):
        audio = "local"
    else:
        audio = "hdmi"

    if (orientation == "any"):
        random_orientation = random.choice(['0', '90', '180', '270'])
    else:
        random_orientation = "0"

    call(["/usr/bin/omxplayer", "--adev", audio, "--orientation", random_orientation, "--blank", "--no-keys", "--no-osd", "--aspect-mode", aspect_mode, movie_path])
    
# Need to improve the flip flop orientation code to reduce the code base size, how do I pass variable number of arguments to call though?
def photo_overlay():
    random_file = random.choice(os.listdir("%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'EVENT': EVENT.lower()}))
    plot_location = random_file.split('-')[0] # Where to plot the overlay is defined in the filename

    if (random_file == "center-magnifying-glass.png"):

        copyfile("%(CODE_PATH)s/media/%(EVENT)s-overlays/reset/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()},"%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()})
        
        random_orientation = random.choice(['', '-flip', '-flop', '-flip -flop'])
        
        if random_orientation == "":
            call(["convert", "%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()}, "%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()}])
        
        if random_orientation == "-flip -flop":
            call(["convert", "-flip", "-flop", "%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()}, "%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()}])
        
        if (random_orientation == "-flip") or (random_orientation == "-flop"):
            call(["convert", random_orientation, "%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()}, "%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()}])

    call(["convert", "%(CODE_PATH)s/photos/image-%(timestr)s.jpg" % {'CODE_PATH': CODE_PATH, 'timestr': timestr}, "%(CODE_PATH)s/media/%(EVENT)s-overlays/%(PHOTO_WIDTH)sx%(PHOTO_HEIGHT)s/%(random_file)s" % {'CODE_PATH': CODE_PATH, 'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT, 'random_file': random_file, 'EVENT': EVENT.lower()}, "-gravity", "%s" % plot_location, "-composite", "%(CODE_PATH)s/photos/image-%(timestr)s.jpg" % {'CODE_PATH': CODE_PATH, 'timestr': timestr}])

    if (EVENT == "MURDER-MYSTERY") and (random_file == "center-magnifying-glass.png"):
        if (random_orientation == ""):
            X = 331
            Y = 331

        if (random_orientation == "-flip"):
            X = 331
            Y = 392

        if (random_orientation == "-flop"):
            X = 629
            Y = 331

        if (random_orientation == "-flip -flop"):
            X = 629
            Y = 392

        call(["%(CODE_PATH)s/scripts/lupe.sh" % {'CODE_PATH': CODE_PATH}, "%(X)s,%(Y)s" % {'X': X, 'Y': Y}, "%(CODE_PATH)s/photos/image-%(timestr)s.jpg" % {'CODE_PATH': CODE_PATH, 'timestr': timestr}, "%(CODE_PATH)s/photos/image-%(timestr)s.jpg" % {'CODE_PATH': CODE_PATH, 'timestr': timestr}])

# Need to write this code to place a text message in the photograph
def text_overlay():
   return 

# Display the URL of where to download the photographs, shown within the instructions sequence
def display_download_url(screen, message, size, screen_divide, red, green, blue, bold, italic):
    fontobject=pygame.font.SysFont('Piboto', size, bold=bold, italic=italic)
    if len(message) != 0:
        label = []
        for line in message:
            for letter in line:
                label.append(fontobject.render(letter, 1, (red, green, blue)))
        for line in range(len(label)):
            screen.blit(label[line],((screen.get_width() / screen_divide) - 400 +(line*size), ((screen.get_height() / screen_divide))))
            time.sleep(0.05)
            pygame.display.update()

def display_footer_message(screen, message, size, screen_divide, red, green, blue, bold, italic):
    fontobject=pygame.font.SysFont('Piboto', size, bold=bold, italic=italic)
    if len(message) != 0:
        label = []
        for line in message:
            label.append(fontobject.render(line, 1, (red, green, blue)))
        for line in range(len(label)):
            screen.blit(label[line],((screen.get_width() / screen_divide) - 350 +(line*size), ((screen.get_height() / screen_divide) - 15)))
            #time.sleep(0.05)
            pygame.display.update()

def display_download_message(screen, message, size, screen_divide, red, green, blue, bold, italic):
    fontobject=pygame.font.SysFont('Piboto', size, bold=bold, italic=italic)
    if len(message) != 0:
        label = []
        for line in message:
            label.append(fontobject.render(line, 1, (red, green, blue)))
        for line in range(len(label)):
            screen.blit(label[line],((screen.get_width() / screen_divide) -(line*size), ((screen.get_height() / screen_divide) +(line*size)+(15*line+200))))
            time.sleep(0.4)
            pygame.display.update()

def display_box(screen, message, size, x, y, red, green, blue, bold, italic):
    fontobject=pygame.font.SysFont('Piboto', size, bold=bold, italic=italic)
    if len(message) != 0:
        label = []
        for line in message:
            label.append(fontobject.render(line, 1, (red, green, blue)))
        for line in range(len(label)):
            screen.blit(label[line],(x, y +(line*100)))
    pygame.display.update()

# Displays the arrow images pointing at where the camera is located
def display_arrow_image(screen, arrow, screen_divide, static):
    image = pygame.image.load(arrow)
    text = ["Look at the camera!"]
    time.sleep(1.5)
    if static == True:
        screen.blit(image,((screen.get_width() / screen_divide) -400, ((screen.get_height() / screen_divide) - 920)))
        display_box(screen, text, 75, 200, 400, 0, 255, 255, True, True)
        pygame.display.update()
    else:
        for i in range (4):
            screen.blit(image,((screen.get_width() / screen_divide) -400, ((screen.get_height() / screen_divide) - 920)))
            display_box(screen, text, 75, 200, 400, 0, 255, 255, True, True)
            pygame.display.update()
            time.sleep(0.5)
            screen.fill(pygame.Color("black"))
            pygame.display.update()
            time.sleep(0.5)

# Display remaining video recording time and flashing REC indicator
def display_recording_indicator_and_time(screen):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    FLASH_TIME = 0.5
    POSITION = (700, 1700)
    RADIUS = 40
    message = ["REC"]
    size = 75
    bold = True
    italic = False
    global SHOW_RECORDING_INDICATOR
    
    # Start code block for countdown timer
    Screen = max(pygame.display.list_modes())
    TIMER_FONT = pygame.font.Font("%(CODE_PATH)s/fonts/timer-font.ttf" % {'CODE_PATH': CODE_PATH},512)
    test = TIMER_FONT.render("0",True,(255,0,0))
    timer_width = test.get_width()
    timer_height = test.get_height()
    totalwidth = 2 * timer_width
    # End code block for countdown timer

    def Update():
        global mode,Time
        if mode == "counting":
            Time[0] -= 1
            if Time[0] <= 0:
                mode = "end"

    def Draw():
        screen.fill((0,0,0))
        t0 = str(Time[0])
        if len(t0) == 1: t0 = "0"+t0
        string = t0
        if Time[0] > 9:
            start_pos = (Screen[0]/2)-(totalwidth/2)-100
        else:
            start_pos = (Screen[0]/2)-(totalwidth/2)-20
        for character in string:
            if character != "1":
                pos = [start_pos,(Screen[1]/2)-(timer_height/2)]
            else:
                pos = [start_pos+int(round((51.0/99.0)*timer_width)),(Screen[1]/2)-(timer_height/2)]
            screen.blit(TIMER_FONT.render(character,True,(255,0,0)),pos)
            start_pos += timer_width
        
        if (Time[0] % 2) == 0:
            pygame.draw.circle(screen, RED, POSITION, RADIUS)
        else:
            pygame.draw.circle(screen, BLACK, POSITION, RADIUS)
        
        # Coordinates are for the dot, the timer and the arrow message respectively
        rect_list = [(650, 1650, 100, 100), (260, 775, 525, 360)]
        pygame.display.update(rect_list)

    # Place the word REC on the screen and its red rectangle
    def plot_rec():
        fontobject=pygame.font.SysFont('Piboto', size, bold=bold, italic=italic)
        if len(message) != 0:
            label = []
            for line in message:
                label.append(fontobject.render(line, 1, RED))
            for line in range(len(label)):
                screen.blit(label[line],(800, 1650))
        pygame.draw.rect(screen, RED, (600, 1600, 400, 200), 5)
        pygame.display.update((575, 1575, 450, 250))

    def main_countdown(self):
        Clock = pygame.time.Clock()
        global mode,Time
        Time = [20]
        mode = "counting"
        plot_rec()
        while mode == "counting":
            Update()
            Draw()
            Clock.tick(1)

    main_countdown('self')

def display_event_image(screen, graphic, location):
    image = pygame.image.load(graphic)
    if location == 'top':
        screen.blit(image,(screen.get_width() - WINDOW_WIDTH, screen.get_height() - WINDOW_HEIGHT))
    else:
        screen.blit(image,(screen.get_width() - WINDOW_WIDTH, screen.get_height() - image.get_height()))
    pygame.display.update()

# Display the photograph of the coloured plastic buttons
def display_button_image(screen, button, screen_divide):
    image = pygame.image.load(button)
    for i in range (50):
        image.set_alpha(i)
        screen.blit(image,((screen.get_width() / screen_divide) +250, ((screen.get_height() / screen_divide) +250)))
        pygame.display.update()

# Remove the photograph of the coloured plastic buttons
def remove_button_image(screen, button, screen_divide):
    image = pygame.image.load(button)
    for i in range (50):
        image.set_alpha(50 - i)
        screen.blit(image,((screen.get_width() / screen_divide) +250, ((screen.get_height() / screen_divide) +250)))
        pygame.display.update()

# Display the generated polaroid, they stack up as each photograph is taken
def show_polaroid(screen, screen_divide, count):
    for i in range(count):
        image = pygame.image.load("%(CODE_PATH)s/polaroids/polaroid-%(i)s.png" % {'CODE_PATH': CODE_PATH, 'i': i})
        screen.blit(image,((screen.get_width() / screen_divide) - 400, (screen.get_height() / screen_divide) - 900))
        pygame.display.update()
    time.sleep(5)

# Plays the audio of the camera click when a photograph is captured
def play_mp3(file):
    mixer.music.load(file)
    mixer.music.play()

# Run this code when the plastic button is pressed to take a photograph
def take_photo(self):
    GPIO.remove_event_detect(RED_BUTTON_PIN) # Disabled due to workaround
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    if ACTIVE_BLUE_BUTTON == "TRUE":
        GPIO.remove_event_detect(BLUE_BUTTON_PIN) # Disabled due to workaround
        GPIO.output(BLUE_LED_PIN, GPIO.LOW)
    global RUN_INSTRUCTIONS
    global BUSY
    BUSY = "TRUE"
    RUN_INSTRUCTIONS = "FALSE"

    for i in range(TAKE_PHOTO_COUNT):
        surf.fill(pygame.Color("black"))
        pygame.display.update()

        global timestr
        timestr = time.strftime("%Y%m%d-%H%M%S")
        movie_path = ('%(CODE_PATH)s/media/photo-countdown-with-sound.mp4' % {'CODE_PATH': CODE_PATH})

        #call(["/usr/bin/v4l2-ctl", "--set-fmt-video=width=%(PHOTO_WIDTH)s,height=%(PHOTO_HEIGHT)s,pixelformat=1" % {'PHOTO_WIDTH': PHOTO_WIDTH, 'PHOTO_HEIGHT': PHOTO_HEIGHT}])
        
        thread_arrows = Thread(target = display_arrow_image, args = (surf, "%(CODE_PATH)s/media/arrows.jpg" % {'CODE_PATH': CODE_PATH}, 2, False,))
        thread_arrows.start()
        call(["/usr/bin/omxplayer", "--no-keys", "--no-osd", "--aspect-mode", "letterbox", movie_path])
        thread_play_mp3 = Thread(target = play_mp3, args = ('%(CODE_PATH)s/media/camera-shutter.mp3' % {'CODE_PATH': CODE_PATH},))
        thread_play_mp3.start()
        
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH,PHOTO_WIDTH) # Set width
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT,PHOTO_HEIGHT) # Set height
        if PREVIEW == 1:
            while True:
                ret,img = cam.read()
                cv2.imshow("preview", cv2.flip(img,1))
                k = cv2.waitKey(10)
                if k == 27:
                    break
 
        s, img = cam.read() # Captures image
        cv2.imwrite('%(CODE_PATH)s/photos/image-%(timestr)s.jpg' % {'CODE_PATH': CODE_PATH, 'timestr': timestr}, img) # Writes image to disk
        cam.release()
        cv2.destroyAllWindows()

        if EVENT != "NONE":
            photo_overlay()

        # Need to work out how to say if i is one less than TAKE_PHOTO_COUNT instead of just i == 2 
        if (i == 2):
            os.system('python %(CODE_PATH)s/lycheeupload/lycheeupload.py -d %(CODE_PATH)s/photos/ --port 2222 --verbose user@jason-and-lynsey.com:/var/www/customersites/www.jason-and-lynsey.com/Lychee/ && mv %(CODE_PATH)s/photos/* %(CODE_PATH)s/photo-archive/ &' % {'CODE_PATH': CODE_PATH})
        
        call(["convert", "%(CODE_PATH)s/photos/image-%(timestr)s.jpg" % {'CODE_PATH': CODE_PATH, 'timestr': timestr}, "-thumbnail", "700x700", "-gravity", "center", "-background", "transparent", "-bordercolor", "white", "+polaroid", "%(CODE_PATH)s/polaroids/polaroid-%(i)s.png" % {'CODE_PATH': CODE_PATH, 'i': i}])
        show_polaroid(surf, 2, i+1)
    text = ["Download & view at jason-and-lynsey.com"]
    display_footer_message(surf, text, 50, 2.5, 255, 255, 255, False, False)
    time.sleep(5)
    BUSY = "FALSE"

# Run this code when the plastic button is pressed to record a video
def take_video(self):
    os.system("%(CODE_PATH)s/stream-to-twitch-or-youtube-or-periscope.sh" % {'CODE_PATH': CODE_PATH})
    GPIO.remove_event_detect(RED_BUTTON_PIN)
    GPIO.remove_event_detect(BLUE_BUTTON_PIN)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)
    global RUN_INSTRUCTIONS
    global BUSY
    global SHOW_RECORDING_INDICATOR
    BUSY = "TRUE"
    RUN_INSTRUCTIONS = "FALSE"
    SHOW_RECORDING_INDICATOR = "TRUE"

    surf.fill(pygame.Color("black"))
    pygame.display.update()

    timestr = time.strftime("%Y%m%d-%H%M%S")
    #movie_path = ('%(CODE_PATH)s/media/video-countdown-with-sound-extra-long.mp4' % {'CODE_PATH': CODE_PATH})
    movie_path = ('%(CODE_PATH)s/media/video-countdown-with-sound-cut-to-beep-at-end.mp4' % {'CODE_PATH': CODE_PATH})
    call(["/usr/bin/v4l2-ctl", "--set-fmt-video=width=640,height=480,pixelformat=1"])
    thread_arrows = Thread(target = display_arrow_image, args = (surf, "%(CODE_PATH)s/media/arrows.jpg" % {'CODE_PATH': CODE_PATH}, 2, True,))
    thread_arrows.start()
    time.sleep(9)
    # 11 secondish video
    call(["/usr/bin/omxplayer", "--no-keys", "--no-osd", "--aspect-mode", "letterbox", movie_path])
    thread_display_recording_indicator_and_time = Thread(target = display_recording_indicator_and_time, args = (surf,))
    thread_display_recording_indicator_and_time.start()
    time.sleep(23)
    
    surf.fill(pygame.Color("black"))
    pygame.display.update()
    # Need to add 2 seconds onto the timeout below
    #os.system("/usr/bin/timeout %(TAKE_VIDEO_CLIP_LENGTH)s /home/pi/photo-video-booth-code/record-video.sh %(TAKE_VIDEO_CLIP_LENGTH)s /home/pi/photo-video-booth-code/videos/video-%(timestr)s.mp4" % {'TAKE_VIDEO_CLIP_LENGTH': TAKE_VIDEO_CLIP_LENGTH, 'timestr': timestr})
    #os.system("/usr/bin/timeout %s /home/pi/photo-video-booth-code/stream-to-youtube.sh" % TAKE_VIDEO_CLIP_LENGTH)
    #os.system("%(CODE_PATH)s/stream-to-youtube.sh" % {'CODE_PATH': CODE_PATH})
    #os.system("%(CODE_PATH)s/stream-to-twitch.sh" % {'CODE_PATH': CODE_PATH})
    #cam = cv2.VideoCapture(0)
    #cam.set(cv2.CAP_PROP_FRAME_WIDTH,1920) # Set width
    #cam.set(cv2.CAP_PROP_FRAME_HEIGHT,1440) # Set height
    if PREVIEW == 1:
        while True:
            ret,img = cam.read()
            cv2.imshow("preview", cv2.flip(img,1))
            k = cv2.waitKey(10)
            if k == 27:
                break
 
    #s, im = cam.read() # Captures image
    #cv2.imwrite('/home/pi/photo-video-booth-code/videos/video-%s.mp4' % timestr) # Writes image to disk
    #cam.release()
    #cv2.destroyAllWindows()

    SHOW_RECORDING_INDICATOR = "FALSE"
    BUSY = "FALSE"

def setup():
    global cb_red
    global BUSY
    global PREVIEW
    while True:
        if BUSY == "FALSE":
            global RUN_INSTRUCTIONS
            RUN_INSTRUCTIONS = "TRUE"
            GPIO.output(RED_LED_PIN, GPIO.HIGH)
            if ACTIVE_BLUE_BUTTON == "TRUE":
                GPIO.output(BLUE_LED_PIN, GPIO.HIGH)
            #if PREVIEW == 1:
            #    camera.start_preview(fullscreen=False, alpha=255, window = (150, 800, 800, 600))
            #GPIO.add_event_detect(RED_BUTTON_PIN, GPIO.FALLING, callback = take_photo, bouncetime = BOUNCETIME) # Turned off due to workaround
            cb_red = ButtonHandler(RED_BUTTON_PIN, take_photo, edge='falling', bouncetime=100)
            cb_red.start()
            GPIO.add_event_detect(RED_BUTTON_PIN, GPIO.FALLING, callback = cb_red)
            
            show_instructions()
            BUSY = "TRUE"
        else:
            time.sleep(10)

mixer.init()

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RED_BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    if ACTIVE_BLUE_BUTTON == "TRUE":
        GPIO.setup(BLUE_BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

# Check time past the hour to enable varying special effects depending on mode
def check_minutes_past_hour():
    global MATRIX
    global FOG
    global GHOST
    global ZOMBIES
    global BALLOONS

    if EVENT == "WEDDING":
        # On the hour show The Matrix mode for 1 minute
        if (0 <= dt.now().minute <= 1):
            MATRIX = "True"
        else:
            MATRIX = "False"

        # Between 15 minutes and 25 minutes/35 minutes and 45 minutes show random fog
        if ((15 <= dt.now().minute <= 25) or (35 <= dt.now().minute <= 45)):
            FOG = "True"
        else:
            FOG = "False"
    
        # At 30 minutes past the hour show random ghost video for 1 minute
        if (30 <= dt.now().minute <= 31):
            GHOST = "True"
        else:
            GHOST = "False"

        # Between 10 minutes and 11 minutes/50 minutes and 51 minutes show zombies
        if ((10 <= dt.now().minute <= 11) or (50 <= dt.now().minute <= 51)):
            ZOMBIES = "True"
        else:
            ZOMBIES = "False"

    if EVENT == "CHRISTENING":
        if ((0 <= dt.now().minute <= 1) or (30 <= dt.now().minute <= 31) or (10 <= dt.now().minute <= 11) or (50 <= dt.now().minute <= 51) or (15 <= dt.now().minute <= 25) or (35 <= dt.now().minute <= 45)):
            BALLOONS = "True"
        else:
            BALLOONS = "False"
    
def key_listener(self):
    while True:
        time.sleep(3)
        choice = input("Press 1 to take 3 photographs, press 2 to record a 20 second video message...")
        if choice == "1":
            take_photo('self')
        if choice == "2":
            take_video('self')

class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)
        
        if (
            ((pinval == 0 and self.lastpinval == 1) and
            (self.edge in ['falling', 'both'])) or
            ((pinval == 1 and self.lastpinval == 0) and
            (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()

thread = Thread(target = key_listener, args = ("self",))
thread.start()
setup_gpio()
setup()
