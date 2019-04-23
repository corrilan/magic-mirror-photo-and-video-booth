#!/bin/bash
#set variable NOW to be the current date+time to be used for the recorded video filename
NOW=$(date +%Y-%m-%d-%H-%M-%S)
#capture video with raspivid, piping its output into ffmpeg, which will then be mixed with the ALSA audio input and saved as a mp4 file
#/usr/bin/raspivid -o - -t 10000 -w 1920 -h 1080 -fps 25 -b 3000000 -rot 180 -g 50 -f | /usr/bin/ffmpeg -thread_queue_size 20240 -f h264 -r 25 -i pipe: -itsoffset 5.3 -f alsa -thread_queue_size 20240 -ac 2 -i plughw:1,0 -vcodec copy -acodec aac -ar 44100 -ab 256k -f flv /home/pi/$NOW.mkv
#/usr/bin/ffmpeg -f v4l2 -s 640x480 -input_format h264 -i /dev/video0 -f alsa -ac 1 -i plughw:1,0 -acodec libmp3lame -ab 96k -async 1 file.mp4
#ffmpeg -f video4linux2 -s 320x240 -i /dev/video0 -f alsa -ac 1 -i hw:1,0 -acodec libmp3lame -ab 96k -async 1 camera.mp4
#ffmpeg -f video4linux2 -input_format h264 -video_size 640x480 -framerate 30 -i /dev/video0 -vcodec copy -an test.h264
raspivid -t 0 -w 960 -h 480 -fps 24 -b 5000000 -o - | ffmpeg -i - -f alsa -ac 1 -i hw:1,0 -map 0:0 -map 1:0 -vcodec copy -acodec aac -strict -2 test.flv

