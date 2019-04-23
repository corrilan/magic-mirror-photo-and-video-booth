#!/bin/bash

# Twitch
/home/pi/photo-video-booth-code/FFmpeg/ffmpeg -thread_queue_size 512 -threads 3 -ar 44100 -ac 2 -f alsa -i hw:1,0 -f v4l2 -thread_queue_size 512 -itsoffset 1 -codec:v h264 -framerate 30 -video_size 1920x1080 -i /dev/video0 -copyinkf -codec:v copy -codec:a aac -ab 128k -g 10 -rtsp_transport tcp -t 42 -f flv rtmp://live-lhr.twitch.tv/app/live_your_own-live_key_here &

# YouTube
#/home/pi/photo-video-booth-code/FFmpeg/ffmpeg -thread_queue_size 512 -threads 3 -ar 44100 -ac 2 -f alsa -i hw:1,0 -f v4l2 -thread_queue_size 512 -itsoffset 1 -codec:v h264 -framerate 30 -video_size 1920x1080 -i /dev/video0 -copyinkf -codec:v copy -codec:a aac -ab 128k -g 10 -rtsp_transport tcp -t 42 -f flv rtmp://a.rtmp.youtube.com/live2/your_own-live_key_here &

# Periscope
#/home/pi/photo-video-booth-code/FFmpeg/ffmpeg -thread_queue_size 512 -threads 3 -ar 44100 -ac 2 -f alsa -i hw:1,0 -f v4l2 -thread_queue_size 512 -itsoffset 1 -codec:v h264 -framerate 30 -video_size 1920x1080 -i /dev/video0 -copyinkf -codec:v copy -codec:a aac -ab 128k -g 10 -rtsp_transport tcp -t 42 -f flv rtmp://ie.pscp.tv:80/your_own-live_key_here &
