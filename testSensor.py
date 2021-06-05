import RPi.GPIO as GPIO          
from time import sleep
import datetime

##### sensor moter 1 ######
switchUP = 12 #pin limit switch1
switchDOWN = 16 #pin limit switch2

##### sensor moter 2 ######
switchUP2 = 6 #pin limit switch1
switchDOWN2 = 5 #pin limit switch2
##### sensor IR ######
irUP = 14 #pin limit switch1
irCount = 18 #pin limit switch2
switchEmergency = 21


GPIO.setmode(GPIO.BCM)
GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  
GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input
GPIO.setup(switchUP2, GPIO.IN)  # set a pin as an input  
GPIO.setup(switchDOWN2, GPIO.IN)  # set pin as an input  
GPIO.setup(irUP, GPIO.IN)  # set pin as an input  
GPIO.setup(irCount, GPIO.IN)  # set pin as an input  
GPIO.setup(switchEmergency, GPIO.IN)  # set pin as an input  

while True:

    print("DOWN",GPIO.input(switchDOWN))
    print("UP",GPIO.input(switchUP))
    print("DOWN2",GPIO.input(switchDOWN2))
    print("UP2",GPIO.input(switchUP2))
    print("IR UP",GPIO.input(irUP))
    print("IR COUNT",GPIO.input(irCount))
    print("Emergency",GPIO.input(switchEmergency))
    print("------------------------")
    sleep(1)