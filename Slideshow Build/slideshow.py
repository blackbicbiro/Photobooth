import os
import time

a=1
while a == 1:
        p = os.system("nc -vz 192.168.2.1 111")
        print(p)
        if p ==0:
                a = 2
        time.sleep(2)

p = os.system("nc -vz 192.168.2.1 111")

os.system("sudo mount 192.168.2.1:/home/pi/Pictures /home/pi/Pictures")
os.system("feh  -F -R 30 -z -D 5 /home/pi/Pictures/")


