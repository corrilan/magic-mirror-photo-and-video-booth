#!/bin/bash

/home/pi/magic-mirror-photo-and-video-booth/FFmpeg/ffmpeg -thread_queue_size 512 -threads 3 -ar 44100 -ac 2 -f alsa -i hw:1,0 -f v4l2 -thread_queue_size 512 -itsoffset 1 -codec:v h264 -framerate 30 -video_size 1920x1080 -i /dev/video0 -copyinkf -codec:v copy -codec:a aac -ab 128k -g 10 -rtsp_transport tcp -t 20 -f flv rtmp://live-lhr.twitch.tv/app/live_your_own-live_key_here
