import RPi.GPIO as GPIO          
from time import sleep

###### start moter 1 ######

switchUP = 12 #pin limit switch1
switchDOWN = 16 #pin limit switch2

moter1_in1 = 24 # +
moter1_in2 = 23 # - 
moter1_en = 25 #pwm

#define output moter 
GPIO.setmode(GPIO.BCM)
GPIO.setup(moter1_in1,GPIO.OUT)
GPIO.setup(moter1_in2,GPIO.OUT)
GPIO.setup(moter1_en,GPIO.OUT)

GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  
GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  

#set status default
GPIO.output(moter1_in1,GPIO.LOW)
GPIO.output(moter1_in2,GPIO.LOW)
moter1_pwm=GPIO.PWM(moter1_en,1000)
moter1_pwm.start(25)
####### end moter 1#########


def moveMoter1(speed,timecount):
    GPIO.output(moter1_in1,GPIO.HIGH)
    GPIO.output(moter1_in2,GPIO.LOW)
    moter1_pwm.ChangeDutyCycle(speed)
    for cnt in range(timecount):
        sleep(1)
    return 0
def stopMoter1():
    GPIO.output(moter1_in1,GPIO.LOW)
    GPIO.output(moter1_in2,GPIO.LOW)
    return 0

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("")
print("\n")    

while(1):

    x=input()
    if x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....") 