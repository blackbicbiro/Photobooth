import signal
import sys
import os
import os.path
import pygame
import time
import random
import picamera
import RPi.GPIO as GPIO
import glob



#Saved File Directory
File_Directory = "/home/pi/Pictures"

#Check if direcotry exsists. if not make it.
if (os.path.exists(File_Directory)) == False:
    os.makedirs(File_Directory)



#GPIO Setup
Capture_Button = 23       #capture picture
Delete_Pic_Button = 25    #delete pictures from sd card
Exit_Button = 24        #exit python
# 7 seg display pins
seg_pin_1 = 1
seg_pin_2 = 2
seg_pin_3 = 3
seg_pin_4 = 4
seg_pin_5 = 5
seg_pin_6 = 6
seg_pin_7 = 7
seg_pin_8 = 8



#Shutdown_Button = 4     #used by shutdown.py script

GPIO.setmode(GPIO.BCM)
GPIO.setup(Capture_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Exit_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Delete_Pic_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(Shutdown_Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)         #used by shutown.py script

#Camera setup
camera = picamera.PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15               ## look at this does this improve video cropping problem
camera.annotate_text_size = 160


#colours
black = (0, 0, 0)
white = (255, 255, 255)


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

        self.screen.fill(black)        
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





#Called to clear screen to black when needed
def ClearScreen():
    scope.screen.fill((0, 0, 0))
    pygame.display.update()





#Display Captured Picture. Scaled picture to fit screen properly
def CapturePreview(File_Name):
    CapturePic = pygame.image.load(File_Directory + File_Name)
    #Make Picture fit full screen while keeping ration
    RatioWidth  = pygame.display.Info().current_h * (float(4)/float(3))
    CapturePic = pygame.transform.scale(CapturePic, (int(RatioWidth), pygame.display.Info().current_h)) 
    #Work out center of picture and work out center of displa   
    CapturePic_rect = CapturePic.get_rect(center = scope.screen.get_rect().center)
    scope.screen.blit(CapturePic, (CapturePic_rect))
    #Update display for 2 seconds
    pygame.display.update()
    time.sleep(2)
    ClearScreen()





def DeletingPicture():
    camera.stop_preview()
    font = pygame.font.Font(None, 36)
    black = (0, 0, 0)
    #clear sceren for next message
    ClearScreen()
       
    start_time = time.time()
    #finish_time = time.time()
    text = font.render("To delete all pictures hold delete button for 5 seconds", True, (255, 255, 255))
    scope.screen.blit(text,(10,10))
    pygame.display.update()
    time.sleep(2)

    while GPIO.input(Delete_Pic_Button) == GPIO.LOW:
        time.sleep(0.02)    # stop loop using 100% cpu
        finish_time = time.time()
        total_time = finish_time - start_time
        #check if button has been held for long enough
        if (total_time > 5):
            #clear sceren for next message
            ClearScreen()

            text = font.render("Deleting Pictures", True, (255, 255, 255))
            scope.screen.blit(text,(10,10))
            pygame.display.update()
            #delete files
            files = glob.glob(File_Directory + '*')
            for f in files:
                os.remove(f)
            time.sleep(2)
            #clear scrren for next message
            ClearScreen()
            text = font.render("ALL PICTURES HAVE BEEN REMOVED", True, (255, 255, 255))
            scope.screen.blit(text,(10 ,10))
            pygame.display.update()
            time.sleep(2)
            print("pictures deleted")
            break

    #clear screen and start preview again
    ClearScreen()
    camera.start_preview()


def CapturePicture():
    File_Name = Create_Capture_Name()
    camera.preview_alpha = 128 #Opacity of the preview image.
    font = pygame.font.Font(None, (int(scope.screen.get_rect().height/1.5)))

    #dispay SMILE on screen    
    text = font.render("SMILE", 1, (white))
    textpos = text.get_rect()
    textpos.centerx = scope.screen.get_rect().centerx
    textpos.centery = scope.screen.get_rect().centery
    scope.screen.blit(text, textpos)
    pygame.display.flip()
    time.sleep(1)


    #countdown till picture is taken
    for x in range (3,0,-1):
            scope.screen.fill(black)
            text = font.render(str(x), 1, white)
            textpos = text.get_rect()
            textpos.centerx = scope.screen.get_rect().centerx
            textpos.centery = scope.screen.get_rect().centery
            scope.screen.blit(text, textpos)
            pygame.display.flip()
            time.sleep(1)
    camera.stop_preview()
    camera.capture(File_Directory + File_Name)
    scope.screen.fill(white)
    pygame.display.flip()
    time.sleep(.1)
    scope.screen.fill(black)
    pygame.display.flip()
    #time.sleep(.1)
    CapturePreview(File_Name)
    camera.start_preview()








# Create an instance of the PyScope class
scope = pyscope()

#Start preview for the first time
camera.start_preview()

#main loop
running = True
while running is True:
    time.sleep(0.02)    # stop loop using 100% cpu

    # Check the buttons for a capture/exit/shutdown
    if GPIO.input(Capture_Button) == GPIO.LOW:
        CapturePicture()

    if GPIO.input(Exit_Button) == GPIO.LOW:
        print("Exit Triggered")
        running=False

    #delete pictures check
    if GPIO.input(Delete_Pic_Button) == GPIO.LOW:
         DeletingPicture()
#    print("got here")


#Keyboard interupt 
    try:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    # up key stops loop and exits
                    running=False

    except KeyboardInterrupt:                   #not working!
        running=False


GPIO.cleanup()
camera.close()
pygame.quit()


