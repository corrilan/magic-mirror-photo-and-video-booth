#!/bin/bash
/usr/bin/cvlc v4l2:///dev/video0:0hroma=h264:width=640:height=480 -A alsa,none --alsa-audio-device default :input-slave=alsa://hw:1,0 :v4l2-fps=25 --sout '#transcode{vcodec=h264,acodec=mp4a,ab=128,channels=2,samplerate=44100,threads=4,audio-sync=1}:standard{access=file,mux=mp4,dst='$2'}'
