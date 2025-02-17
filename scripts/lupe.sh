#!/bin/bash
#
# Developed by Fred Weinhaus 3/19/2008 .......... revised 12/8/2017
#
# ------------------------------------------------------------------------------
# 
# Licensing:
# 
# Copyright © Fred Weinhaus
# 
# My scripts are available free of charge for non-commercial use, ONLY.
# 
# For use of my scripts in commercial (for-profit) environments or 
# non-free applications, please contact me (Fred Weinhaus) for 
# licensing arrangements. My email address is fmw at alink dot net.
# 
# If you: 1) redistribute, 2) incorporate any of these scripts into other 
# free applications or 3) reprogram them in another scripting language, 
# then you must contact me for permission, especially if the result might 
# be used in a commercial or for-profit environment.
# 
# My scripts are also subject, in a subordinate manner, to the ImageMagick 
# license, which can be found at: http://www.imagemagick.org/script/license.php
# 
# ------------------------------------------------------------------------------
# 
####
#
# USAGE: lupe [cenx,ceny] [-m mag] [-s shape] [-l lenx,leny] [-r round] [-b border] [-c color] [-d distort] [-p pcolor] infile outfile
# USAGE: lupe [-h or -help]
#
# OPTIONS:
#
# centx,centy              coordinate in image for center of lupe;
#                          default is center of image
# -m      mag              magnification factor; float; mag>=1; 
#                          default=2
# -s      shape            shape is lupe (magnifying glass) shape;
#                          circle (ellipse) or square (rectangle); 
#                          default=circle
# -l      lenx,leny        radii (circle) or half-width (square);
#                          must be greater than 0; default=64,64;
#                          if only one value is provided, it will
#                          be used in both dimensions.
# -r      round            rounding radius for corners of square;
#                          round>=0; default=10
# -b      border           border thickness for lupe; border>=0;
#                          default=4
# -c      color            border color for lupe; default=white
# -d      distort          spherical distortion factor; float; 
#                          distort>=0; default=0
# -p      pcolor           color to use to pad the image so that 
#                          zooms near the edges can be used; 
#                          any valid IM color is allowed; default 
#                          is no pad                      
# 
###
#
# NAME: LUPE 
# 
# PURPOSE: To apply a magnifying glass effect in a local area of an image.
# 
# DESCRIPTION: LUPE applies a magnifying glass (lupe) effect in a local area 
# of an image. The normal mode is a simple magnification with no distortion. 
# However an option is provided to apply a spherical distortion. The lupe can 
# have either a circular/elliptical shape or a (rounded) square/rectangular 
# shape. The lupe border thickeness and color can also be specified.
# 
# 
# ARGUMENTS: 
# 
# centx,centy ... CENTX,CENTY are the coordinates in the image for the center 
# of the lupe. If not specified, then the center of the image will be provided.
# 
# -m mag ... MAG is the magnificiation factor. Values must be greater than or
# equal to 1. Values may be floating point numbers. The default is 2.
# 
# -s shape ... SHAPE is the shape of the lupe. The shape may be circle or square. 
# The default is circle.
# 
# -l lenx,leny ... LENX,LENY is either the radii for the circle/ellipse or the 
# half-width for the square/rectangle. Values must be integers greater than 0. 
# The default is 64,64.
# 
# -r round ... ROUND is the radius of the corner rounding for the shape=square 
# option. Values must be integers greater than or equal to zero. The default is 10.
# 
# -b border ... BORDER is the border thickness of the lupe. Values must be 
# integers greater than or equal to zero. The default=4.
# 
# -c color ... COLOR is the color of the border of the lupe. Color may be any 
# valid IM color specification. Be sure to enclose in double quotes if not 
# using a color name. The default=white.
# 
# -d distort ... DISTORT is the spherical distortion factor. Values may be floating 
# point numbers greater than or equal to 0. The default=0 (no distortion). When 
# values are greater than 0, the distortion is applied using -fx. Therefore, the 
# processing will be slower.
# 
# -p pcolor ... PCOLOR is the color to use to pad the image so that zooms near the 
# edges can be used. Any valid IM color is allowed. The default is no pad.                    
#
# CAVEAT: No guarantee that this script will work on all platforms, 
# nor that trapping of inconsistent parameters is complete and 
# foolproof. Use At Your Own Risk. 
# 
######
#

# set default value
mag=2
distort=0
lenx=180
leny=180
round=10
border=0
color="white"
border2=1
color2="black"
shape="circle"
centx="" 		# flag to use center of image for centx,centy
centy="" 		# flag to use center of image for centx,centy
pcolor=""

# set directory for temporary files
dir="."    # suggestions are dir="." or dir="/tmp"

# set up functions to report Usage and Usage with Description
PROGNAME=`type $0 | awk '{print $3}'`  # search for executable on path
PROGDIR=`dirname $PROGNAME`            # extract directory of program
PROGNAME=`basename $PROGNAME`          # base name of program
usage1() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^###/g;  /^#/!q;  s/^#//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}
usage2() 
	{
	echo >&2 ""
	echo >&2 "$PROGNAME:" "$@"
	sed >&2 -e '1,/^####/d;  /^######/g;  /^#/!q;  s/^#*//;  s/^ //;  4,$p' "$PROGDIR/$PROGNAME"
	}


# function to report error messages
errMsg()
	{
	echo ""
	echo $1
	echo ""
	usage1
	exit 1
	}


# function to test for minus at start of value of second part of option 1 or 2
checkMinus()
	{
	test=`echo "$1" | grep -c '^-.*$'`   # returns 1 if match; 0 otherwise
    [ $test -eq 1 ] && errMsg "$errorMsg"
	}

# test for correct number of arguments and get values
if [ $# -eq 0 ]
	then
	# help information
   echo ""
   usage2
   exit 0
elif [ $# -gt 19 ]
	then
	errMsg "--- TOO MANY ARGUMENTS WERE PROVIDED ---"
else
	while [ $# -gt 0 ]
		do
			# get parameter values
			case "$1" in
		  -h|-help)    # help information
					   echo ""
					   usage2
					   exit 0
					   ;;
				-s)    # get  shape
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID SHAPE SPECIFICATION ---"
					   checkMinus "$1"
					   shape="$1"
					   [ "$shape" != "circle" -a "$shape" != "square" ] && errMsg "--- INVALID SHAPE VALUE ---"
					   ;;
				-m)    # get  mag
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID MAGNIFICATION SPECIFICATION ---"
					   checkMinus "$1"
					   mag=`expr "$1" : '\([.0-9]*\)'`
					   [ "$mag" = "" ] && errMsg "--- MAG=$mag MUST BE A NON-NEGATIVE FLOATING POINT VALUE (with no sign) ---"
					   magtest=`echo "$mag < 0" | bc`
					   [ $magtest -eq 1 ] && errMsg "--- MAG=$mag MUST BE A NON-NEGATIVE FLOATING POINT VALUE ---"
					   ;;
				-l)    # get  lenx,leny
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID FORMAT SPECIFICATION ---"
					   checkMinus "$1"
		 			   len="$1"
		   			   lenx=`echo "$len" | cut -d, -f1`
		   			   leny=`echo "$len" | cut -d, -f2`
		   			   # leny = lenx automatically if second set does not exist
		 			   lenx=`expr "$lenx" : '\([.0-9]*\)'`
		 			   leny=`expr "$leny" : '\([.0-9]*\)'`
					   [ "$lenx" = "" -o "$leny" = "" ] && errMsg "--- LENX,LENY=${lenx},${leny} MUST BE TWO NON-NEGATIVE INTEGERS SEPARATED BY COMMAS ---"
					   ;;
				-r)    # get  round
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID ROUND SPECIFICATION ---"
					   checkMinus "$1"
					   round=`expr "$1" : '\([0-9]*\)'`
					   [ "$round" = "" ] && errMsg "--- ROUND=$round MUST BE A NON-NEGATIVE INTEGERS ---"
					   ;;
				-b)    # get  border
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID BORDER SPECIFICATION ---"
					   checkMinus "$1"
					   border=`expr "$1" : '\([0-9]*\)'`
					   [ "$border" = "" ] && errMsg "--- BORDER=$border MUST BE A NON-NEGATIVE INTEGERS ---"
					   ;;
				-c)    # get  color
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID BORDER COLOR SPECIFICATION ---"
					   checkMinus "$1"
					   color="$1"
					   ;;
				-p)    # get  pcolor
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID PAD COLOR SPECIFICATION ---"
					   checkMinus "$1"
					   pcolor="$1"
					   ;;
				-d)    # get  distort
					   shift  # to get the next parameter
					   # test if parameter starts with minus sign 
					   errorMsg="--- INVALID DISTORT SPECIFICATION ---"
					   checkMinus "$1"
					   distort=`expr "$1" : '\([.0-9]*\)'`
					   [ "$distort" = "" ] && errMsg "--- DISTORT=$distort MUST BE A NON-NEGATIVE FLOATING POINT VALUE (with no sign) ---"
					   distorttest=`echo "$distort < 0" | bc`
					   [ $distorttest -eq 1 ] && errMsg "--- DISTORT=$distort MUST BE A NON-NEGATIVE FLOATING POINT VALUE ---"
					   ;;
	 [0-9]*,[0-9]*)    # get centx,centy
					   # test size values
					   cent="$1"
					   [ "$cent" = "" ] && errMsg "CENTER=$cent IS NOT VALID"
					   centx=`echo "$cent" | cut -d, -f1`
					   centy=`echo "$cent" | cut -d, -f2`
					   ;;
				 -)    # STDIN and end of arguments
					   break
					   ;;
				-*)    # any other - argument
					   errMsg "--- UNKNOWN OPTION ---"
					   ;;
		     	 *)    # end of arguments
					   break
					   ;;
			esac
			shift   # next option
	done
	#
	# get infile and outfile
	infile="$1"
	outfile="$2"
fi

# test that infile provided
[ "$infile" = "" ] && errMsg "NO INPUT FILE SPECIFIED"

# test that outfile provided
[ "$outfile" = "" ] && errMsg "NO OUTPUT FILE SPECIFIED"

tmpA="$dir/lupe_$$.mpc"
tmpB="$dir/lupe_$$.cache"
tmp0="$dir/lupe_0_$$.miff"
tmp1="$dir/lupe_1_$$.miff"
tmp2="$dir/lupe_2_$$.miff"
trap "rm -f $tmpA $tmpB $tmp0 $tmp1 $tmp2;" 0
trap "rm -f $tmpA $tmpB $tmp0 $tmp1 $tmp2; exit 1" 1 2 3 15
trap "rm -f $tmpA $tmpB $tmp0 $tmp1 $tmp2; exit 1" ERR



if [ "$pcolor" != "" ]; then
	pproc="-bordercolor $pcolor -border ${lenx}x${leny}"
	tproc="-trim +repage"
else
	pproc=""
	tproc=""
fi


convert -quiet "$infile" $pproc +repage "$tmpA" || \
	errMsg "--- FILE $infile DOES NOT EXIST OR IS NOT AN ORDINARY FILE, NOT READABLE OR HAS ZERO SIZE ---"


# get width, height, center and bottom right pixel
width=`identify -format %w $tmpA`
height=`identify -format %h $tmpA`
lastx=`expr $width - 1`
lasty=`expr $height - 1`
if [ "$centx" = "" -o "$centy" = ""  ]
	then
	centx=`echo "scale=0; ($width-1) / 2" | bc`
	centy=`echo "scale=0; ($height-1) / 2" | bc`
elif [ "$pcolor" != "" ]; then
	centx=$((centx+lenx))
	centy=$((centy+leny))
fi

# get subsection
if [ "$shape" = "square" -a "$distort" != "0" ]
	then
	# outer rectange to ellipse bounding inner rectange are related by sqrt(2)
	# see http://www.math.uoc.gr/~pamfilos/eGallery/problems/MaximalRectInEllipse.html
	# use 1.5 rather than sqrt(2)=1.4 for a little buffer.
	lenx1=`echo "scale=0; (1.5 * $lenx) / 1" | bc`
	leny1=`echo "scale=0; (1.5 * $leny) / 1" | bc`
else
	lenx1=$lenx
	leny1=$leny
fi
ws=`expr 2 \* $lenx1`
hs=`expr 2 \* $leny1`
strtx=`echo "scale=0; ($centx - $lenx1) / 1" | bc`
strty=`echo "scale=0; ($centy - $leny1) / 1" | bc`
endx=`echo "scale=0; ($centx + $lenx1) / 1" | bc`
endy=`echo "scale=0; ($centy + $leny1) / 1" | bc`
if [ `echo "$strtx < 0" | bc` -eq 1 ]
	then
	ws=`expr $ws + $strtx`
	strtx=0
fi
if [ `echo "$strty < 0" | bc` -eq 1 ]
	then
	hs=`expr $hs + $strty`
	strty=0
fi
if [ `echo "$endx > $lastx" | bc` -eq 1 ]
	then
	ws=`expr $ws - $endx + $lastx`
	endx=$lastx
fi
if [ `echo "$strty < 0" | bc` -eq 1 ]
	then
	hs=`expr $hs - $endy + $lasty`
	endy=$lasty
fi
sub="${ws}x${hs}+${strtx}+${strty}"

# get subsection center
centsx=`echo "scale=0; ($centx - $strtx) / 1" | bc`
centsy=`echo "scale=0; ($centy - $strty) / 1" | bc`
xc=$centsx
yc=$centsy

# get inner and outer bevel distances
lenxi=`convert xc: -format "%[fx:ceil($lenx - $border/2)]" info:`
lenyi=`convert xc: -format "%[fx:ceil($leny - $border/2)]" info:`
lenxo=`convert xc: -format "%[fx:ceil($lenx + $border/2)]" info:`
lenyo=`convert xc: -format "%[fx:ceil($leny + $border/2)]" info:`
if [ "$shape" = "square" ]
	then
	shape1="roundrectangle"
	x1=`echo "scale=0; ($centsx - $lenx) / 1" | bc`
	y1=`echo "scale=0; ($centsy - $leny) / 1" | bc`
	x2=`echo "scale=0; ($centsx + $lenx) / 1" | bc`
	y2=`echo "scale=0; ($centsy + $leny) / 1" | bc`
	rx=$round
	coordss="$x1,$y1 $x2,$y2 $rx,$rx"
	x1=`echo "scale=0; ($centx - $lenx) / 1" | bc`
	y1=`echo "scale=0; ($centy - $leny) / 1" | bc`
	x2=`echo "scale=0; ($centx + $lenx) / 1" | bc`
	y2=`echo "scale=0; ($centy + $leny) / 1" | bc`
	coords="$x1,$y1 $x2,$y2 $rx,$rx"
	x1i=`echo "scale=0; ($centx - $lenxi) / 1" | bc`
	y1i=`echo "scale=0; ($centy - $lenyi) / 1" | bc`
	x2i=`echo "scale=0; ($centx + $lenxi) / 1" | bc`
	y2i=`echo "scale=0; ($centy + $lenyi) / 1" | bc`
	coordsi="$x1i,$y1i $x2i,$y2i $rx,$rx"
	x1o=`echo "scale=0; ($centx - $lenxo) / 1" | bc`
	y1o=`echo "scale=0; ($centy - $lenyo) / 1" | bc`
	x2o=`echo "scale=0; ($centx + $lenxo) / 1" | bc`
	y2o=`echo "scale=0; ($centy + $lenyo) / 1" | bc`
	coordso="$x1o,$y1o $x2o,$y2o $rx,$rx"
elif [ "$shape" = "circle" ]
	then
	shape1="ellipse"
	coordss="$centsx,$centsy $lenx,$leny 0,360"
	coords="$centx,$centy $lenx,$leny 0,360"
	coordsi="$centx,$centy $lenxi,$lenyi 0,360"
	coordso="$centx,$centy $lenxo,$lenyo 0,360"
fi

# get scale factor from mag, pi/2 and 2/pi
isf=`echo "scale=6; (1 / $mag)" | bc`
pid2=`echo "scale=6; 2*a(1)" | bc -l`
ipid2=`echo "scale=6; 1/$pid2" | bc`


# create mask
convert -size ${ws}x${hs} xc:black -fill white \
	-draw "$shape1 $coordss" $tmp0

# IM version trap for use of newer -fx hypot function
im_version=`convert -list configure | \
sed '/^LIB_VERSION_NUMBER */!d;  s//,/;  s/,/,0/g;  s/,0*\([0-9][0-9]\)/\1/g' | head -n 1`
if [ "$im_version" -ge "06030600" ]
	then 
	rd="rd=hypot(xd,yd);"
else
	rd="rd=sqrt(xd^2+yd^2);"
fi

# create magnified subsection
if [ "$distort" = "0" ]
	then
	# just use -distort SRT to magnify
	convert $tmpA[$sub] -distort SRT "$xc,$yc  $mag  0" +repage $tmp1

elif [ "$shape" = "square" ]
	then
echo "ffr"
	ffr="ffr=rd?($ipid2*asin(rd)/rd)^$distort:0;"
echo "fx"
	convert $tmpA[$sub] -alpha on -channel RGBA -virtual-pixel transparent -monitor -fx \
		"xd=(i-$xc)/$xc; yd=(j-$yc)/$yc; $rd $ffr xs=$isf*$xc*ffr*xd+$xc; ys=$isf*$yc*ffr*yd+$yc; (rd>1)?none:u.p{xs,ys}" \
		+repage $tmp1

elif [ "$shape" = "circle" ]
	then
echo "ffr"
	ffr="ffr=rd?($ipid2*asin(rd)/rd)^$distort:0;"
echo "fx"
	convert $tmpA[$sub] -alpha on -channel RGBA -virtual-pixel transparent -monitor -fx \
		"xd=(i-$xc)/$xc; yd=(j-$yc)/$yc; $rd $ffr xs=$isf*$xc*ffr*xd+$xc; ys=$isf*$yc*ffr*yd+$yc; (rd>1)?none:u.p{xs,ys}" \
		+repage $tmp1
fi

# composite mask onto magnified subsection so outside is transparent, then composite result into orginal
convert $tmpA \( $tmp1 $tmp0 -alpha off -compose copy_opacity -composite \) \
	-geometry $sub -compose over -composite $tmp2


# add border
if [ $border -ne 0 ]
	then
	convert $tmp2 \
	-stroke $color -strokewidth $border \
	-fill none -draw "$shape1 $coords" \
	-stroke $color2 -strokewidth $border2 \
	-fill none -draw "$shape1 $coordso" \
	-stroke $color2 -strokewidth $border2 \
	-fill none -draw "$shape1 $coordsi" \
	$tproc "$outfile"
else
	convert $tmp2 $tproc "$outfile"
fi
exit 0
