# Magic-Mirror-Photo-and-Video-Booth
Python based magic mirror/photo and video booth aimed at running on a Raspberry Pi 3 using a Logitech HD Pro Webcam C920.  Photographs upload to a self hosted Lychee server (plus local copy) and video is output to YouTube, Twitch or similar online service - fast Internet connection required for successful use of video feature.

To date, this is the culmination of six months development work, originally written and successfully used for my wedding in February 2019.  You can access my own Lychee server to see examples of photographs taken at https://www.jason-and-lynsey.com.  See the album entitled "Wedding Magic Mirror Photobooth".

Code is very rough but hopefully people have some ideas on how to make it easier to manage the system - possibly a web based interface to change settings quickly for non coders.

Backend for photograph storage and browsing is running on a remote web server using Lychee https://github.com/LycheeOrg/Lychee
Photographs are uploaded to Lychee using lycheeupload https://github.com/r0x0r/lycheeupload

The Raspberry Pi 3 is underpowered for effective local processing and storage of video so I made use of online services such as YouTube Live to let them handle the video storage and processing.

Soon I hope to place a link here to a video of the booth in action.
