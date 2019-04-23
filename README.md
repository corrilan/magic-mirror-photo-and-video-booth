# Magic-Mirror-Photo-and-Video-Booth
Python based magic mirror/photo and video booth aimed at running on a Raspberry Pi 3 using a Logitech HD Pro Webcam C920.  Photographs upload to a self hosted Lychee server (plus local copy) and video is output to YouTube, Twitch or similar online service - fast Internet connection required for successful use of video feature.

To date, this is the culmination of six months development work, originally written and successfully used for my wedding in February 2019, with testing taking place at Christmas 2018 and a murder mystery night.  You can access my own Lychee server to see examples of photographs from these events at https://www.jason-and-lynsey.com.  See the album entitled "Wedding Magic Mirror Photobooth".

Links to specific gathering albums showing some differing overlays and effects on the photographs:

Friends Christmas gathering album:  https://www.jason-and-lynsey.com/#15443063109364

Family Christmas Day album:         https://www.jason-and-lynsey.com/#15456717649826

Murder mystery night album:         https://www.jason-and-lynsey.com/#15458187660284

Wedding album:                      https://www.jason-and-lynsey.com/#15486036679244

Code is very rough but hopefully people have some ideas on how to make it easier to manage the system - possibly a web based interface to change settings quickly for non coders.

The bulk of the code is contained in start-photo-video-booth-python3.py accompanied by a few helper Bash scripts.

Backend for photograph storage and browsing is running on a remote web server using Lychee https://github.com/LycheeOrg/Lychee

Photographs are uploaded to Lychee using lycheeupload https://github.com/r0x0r/lycheeupload

One of the photograph overlay options (murder mystery) uses a lupe.sh script created and released under GPL by Fred Weinhaus.

The Raspberry Pi 3 is underpowered for effective local processing and storage of video so I made use of online services such as YouTube Live to let them handle the video storage and processing.  (Bash script called for this procedure)

Soon I hope to place a link here to a video/photographs of the booth in action.

Objects such as some audio and video that is used cannot be uploaded due to copyright.  When I get time I will create alternative 'placeholder' media which can be replaced with your own creations/purchases.

I decided to splash out on a 2 way mirror and a nice picture frame surround but costs can be cut drastically if these are not imperative.  Make larger or smaller devices using for example an old TV or monitor you have lying around - I plan on making a more portable table top version in the future myself.
