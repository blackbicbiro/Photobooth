import signal
import sys
import os
import os.path
import pygame
import time
import random
import picamera
import RPi.GPIO as GPIO

#Saved File Directory
File_Directory = "/home/pi/Pictures/"

#GPIO Setup
Capture_Button = 3
Exit_Button = 5
Shutdown_Button = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(Capture_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#Camera setup
camera = picamera.PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15               ## look at this does this improve video cropping problem
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

    def CapturePreview(self, File_Name):
        black = (0, 0, 0)
        CapturePic = pygame.image.load(File_Directory + File_Name)
        #Make Picture fit full screen while keeping ration
        RatioWidth  = pygame.display.Info().current_h * (float(4)/float(3))
        CapturePic = pygame.transform.scale(CapturePic, (int(RatioWidth), pygame.display.Info().current_h)) 
        #Work out center of picture and work out center of displa   
        CapturePic_rect = CapturePic.get_rect(center = self.screen.get_rect().center)
        self.screen.blit(CapturePic, (CapturePic_rect))
        #Update display for 2 seconds
        pygame.display.update()
        time.sleep(2)
        self.screen.fill(black)
        pygame.display.update()



     
# Create an instance of the PyScope class
scope = pyscope()







#Create capture name. make sure doesnt overwrite ( could be caused by Rasbery pi clock being wrong if powered down)    
def Create_Capture_Name():
    now = time.strftime("%d-%m-%Y-%H:%M:%S") #get the current date and time for the start of the filename
    capture_name = now
    file_count = 0
    capture_name_temp = capture_name
    if os.path.exists(File_Directory + capture_name_temp + '.jpg'):
        while os.path.exists(File_Directory + capture_name_temp + '.jpg'):
            capture_name_temp = capture_name + "(" + str(file_count) + ")"
            file_count = file_count+1   
        capture_name = capture_name_temp + '.jpg'
    else:
        capture_name = capture_name + '.jpg'

    return capture_name





def CapturePicture(Capture_Button):
    File_Name = Create_Capture_Name()
    camera.capture(File_Directory + File_Name)
    camera.stop_preview()
    scope.CapturePreview(File_Name)
    camera.start_preview()






#Start preview for the first time
camera.start_preview()
time.sleep(.1)
    
#Set up event capture for button
GPIO.add_event_detect(Capture_Button, GPIO.RISING, callback=CapturePicture, bouncetime=200)



#main loop
a = 1
while a is 1:
    time.sleep(0.02)
#    if GPIO.input(Capture_Button) == GPIO.LOW:
#        CapturePicture()
#    print("got here")


#Keyboard interupt 
    try:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    # up key stops loop and exits
                    a = 2
    except KeyboardInterrupt:                   #not working!
        a=2


GPIO.cleanup()
camera.close()
pygame.quit()


        