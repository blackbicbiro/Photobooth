#!/bin/sh



# install packages
apt-get install update
apt-get install python-pip -y
apt-get install python-pygame -y
apt-get install python-picamera -y
apt-get install fbi -y
apt-get install usbmount -y
apt-get install dnsmasq -y		# DHCP server
apt-get install hostapd -y		#wirless AP
apt-get install samba -y
apt-get install samba-common-bin
apt-get install nfs-common
apt-get install nfs-kernel-server


mkdir /home/pi/Pictures


# setup wlan address to static. 192.168.0.1/24
# setup dhcp for wlan
# setup wireless access point using hostapd
#	ssid=Photobooth
#	password=smileyface!
#	ADD FOLLOWING TO NEW File /etc/hostapd/hostapd.conf:
#		interface=wlan0
#		driver=nl80211
#		ssid=Photobooth
#		hw_mode=g
#		channel=7
#		wmm_enabled=0
#		macaddr_acl=0
#		auth_algs=1
#		ignore_broadcast_ssid=0
#		wpa=2
#		wpa_passphrase=smileyface!
#		wpa_key_mgmt=WPA-PSK
#		wpa_pairwise=TKIP
#		rsn_pairwise=CCMP
#
# Change /etc/default/hostapd line daemon_conf="" line to the following:
#		DAEMON_CONF="/etc/hostapd/hostapd.conf"
#
# edit DHCP config to say the follwing:
#		interface=wlan0
#		# Use the require wireless interface - usually wlan0
#		dhcp-range=192.168.0.2,192.168.0.20,255.255.255.0,24h







# set up nfs - add following lines to /etc/exports ( shares directory to 2 diffrent networks)
#	/home/pi/Pictures 10.174.154.0/24(rw,sync,no_subtree_check)
#	/home/pi/Pictures 192.168.0.0/24(rw,sync,no_subtree_check)
# 


#set camera to start after loging, add following line to bottem of /etc/profile
#	sudo python /home/pi/Photobooth/cam.py
#	sudo python /home/pi/Photobooth/shutdown.py










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



