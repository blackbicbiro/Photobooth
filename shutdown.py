#!/bin/python

import RPi.GPIO as GPIO
import time
import os

#set GPIO pins up
shutdown_button = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(shutdown_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown_callback(channel):
	os.system("sudo shutdown -h now")


#set event handler to wait for button press
GPIO.add_event_detect(shutdown_button, GPIO.FALLING, callback = shutdown_callback, bouncetime = 2000)  





while True:

	time.sleep(2)
	print("hello")



