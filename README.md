# Photobooth
Photobooth that takes photos and also slide shows on raspbery Pi's


PiCam:
	NTP Server
	PiCamera
	USBAuto mount and copy photos?
	Multi Button Press to clear all PHOTOS (press all buttons?
	wirless accespoint/DHCP server
	


PiDisplay:
	NTP client
	Slide show pictures





shut down button



# turn on power
# both Pi's boot up
# CamPi(camera pi) starts NTP time server (gets time from battery clock)
# CamDisplay(slide show) gets time from CamPi(NTP server)
# CamPi starts camera Captures script
# CamDisplay Starts slideshow

if Capture button pressed:
	count down with preivew	
	take photo
	display photo for a few seconds
	return to preview

if shutdown button pressed:
	shut down both Pi's (send via network or maybe shared button)

If Exit button pressed:
	Exit to terminal


