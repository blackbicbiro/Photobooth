#!/bin/python

import RPi.GPIO as GPIO
import time
import os

#set GPIO pins up
shutdown_button = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(shutdown_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown_callback(channel):
	start_time = time.time()	
    	while GPIO.input(shutdown_button) == GPIO.LOW:
        	time.sleep(0.02)    # stop loop using 100% cpu
        	finish_time = time.time()
        	total_time = finish_time - start_time
        	#check if button has been held for long enough
	        if (total_time > 5):
			os.system("ssh 192.168.2.2 sudo shutdown -P 0")
			time.sleep(5)	
			os.system("sudo shutdown -h now")
			break

#set event handler to wait for button press
GPIO.add_event_detect(shutdown_button, GPIO.FALLING, callback = shutdown_callback, bouncetime = 2000)  





while True:

	time.sleep(2)
#	print("hello")



