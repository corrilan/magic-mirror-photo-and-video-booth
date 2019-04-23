#!/bin/bash

#Get some required libraries and header files for x264 and OMX
sudo apt-get install libasound2-dev libvpx. libx264. libomxil-bellagio-dev -y

#Get FFMPEG source code
cd ~
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
cd ffmpeg
mkdir dependencies
cd dependencies/
mkdir output
cd ~

#Compile libx264
git clone http://git.videolan.org/git/x264.git
cd x264/
./configure --enable-static --prefix=/home/pi/ffmpeg/dependencies/output/
make -j4
make install
cd ~

#Compile ALSA
wget ftp://ftp.alsa-project.org/pub/lib/alsa ... .1.tar.bz2
tar xjf alsa-lib-1.1.1.tar.bz2
cd alsa-lib-1.1.1/
./configure --prefix=/home/pi/ffmpeg/dependencies/output
make -j4
make install
cd ~

#Compile FDK-AAC
sudo apt-get install pkg-config autoconf automake libtool -y
git clone https://github.com/mstorsjo/fdk-aac.git
cd fdk-aac
./autogen.sh
./configure --enable-shared --enable-static
make -j4
sudo make install
sudo ldconfig
cd ~

#Compile FFMPEG
cd ffmpeg
./configure --prefix=/home/pi/ffmpeg/dependencies/output --enable-gpl --enable-libx264 --enable-nonfree --enable-libfdk_aac --enable-omx --enable-omx-rpi --extra-cflags="-I/home/pi/ffmpeg/dependencies/output/include" --extra-ldflags="-L/home/pi/ffmpeg/dependencies/output/lib" --extra-libs="-lx264 -lpthread -lm -ldl"
make -j4
make install
cd ~
