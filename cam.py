import sys
import os
import pygame
import time
import random
import picamera
import RPi.GPIO as GPIO


#GPIO Setup
Capture_Button = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(Capture_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Camera setup
camera = picamera.PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15				## look at this does this improve video cropping problem
camera.annotate_text_size = 160



 
class pyscope :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        #print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

	#Mouse Visablilty
	pygame.mouse.set_visible(0)

     
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        
	pygame.mouse.set_visible(0)
	# Render the screen
        pygame.display.update()
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
 
    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

    def CapturePreview(self):
	
	CapturePic = pygame.image.load('/home/pi/Pictures/foo.jpg')
	#Make Picture fit full screen while keeping ration
	RatioWidth  = pygame.display.Info().current_h * (float(4)/float(3))
	CapturePic = pygame.transform.scale(CapturePic, (int(RatioWidth), pygame.display.Info().current_h))	
	#Work out center of picture and work out center of displa	
	CapturePic_rect = CapturePic.get_rect(center = self.screen.get_rect().center)
	self.screen.blit(CapturePic, (CapturePic_rect))
	#Update display for 2 seconds
	pygame.display.update()
	time.sleep(2)
 
# Create an instance of the PyScope class

scope = pyscope()

b = 1
camera.start_preview()
time.sleep(.1)
	





while b is 1:
	pressed = GPIO.wait_for_edge(Capture_Button, GPIO.FALLING)
       	if pressed is Capture_Button:
               	camera.capture('/home/pi/Pictures/foo.jpg')
		camera.stop_preview()
		scope.CapturePreview()
		camera.start_preview()
		time.sleep(2)
		print(pressed)
               	b = 2


camera.close()
pygame.quit()


		
