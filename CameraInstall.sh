#!/bin/sh

# install packages
apt-get install update
apt-get install python-pip -y
apt-get install python-pygame -y
apt-get install python-picamera -y







# turn of Camera led

#GrepResult=$(grep -c "LED" config.test)
#GrepResult=2
#echo $GrepReult
#
#if  $GrepResult == 1
#	then
#		echo '#Disable Camera LED' >> config.test
#		echo 'disable_camera_led=1' >> config.test
#fi



