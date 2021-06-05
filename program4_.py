from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QSpinBox, QCheckBox
from PyQt5 import uic
import sys
import RPi.GPIO as GPIO          
from time import sleep
from PyQt5.QtCore import *

import datetime


##### sensor moter 1 ######
switchUP = 12 #pin limit switch1
switchDOWN = 16 #pin limit switch2

##### sensor moter 2 ######
switchUP2 = 6 #pin limit switch1
switchDOWN2 = 5 #pin limit switch2

##### sensor moter 3 ######
irUP = 14 #pin limit switch1


####### moter1 #######
moter1_in1 = 24 # +
moter1_in2 = 23 # - 
moter1_en = 25 #pwm

####### moter2 #######
moter2_in1 = 26 # +
moter2_in2 = 19 # - 
moter2_en = 13 #pwm

####### moter3 #######
moter3_in1 = 22 # +
moter3_in2 = 27 # - 
moter3_en = 17 #pwm

#define output moter 
GPIO.setmode(GPIO.BCM)
GPIO.setup(moter1_in1,GPIO.OUT)
GPIO.setup(moter1_in2,GPIO.OUT)
GPIO.setup(moter1_en,GPIO.OUT)

GPIO.setup(moter2_in1,GPIO.OUT)
GPIO.setup(moter2_in2,GPIO.OUT)
GPIO.setup(moter2_en,GPIO.OUT)

GPIO.setup(moter3_in1,GPIO.OUT)
GPIO.setup(moter3_in2,GPIO.OUT)
GPIO.setup(moter3_en,GPIO.OUT)

GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  
GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input
GPIO.setup(switchUP2, GPIO.IN)  # set a pin as an input  
GPIO.setup(switchDOWN2, GPIO.IN)  # set pin as an input  
GPIO.setup(irUP, GPIO.IN)  # set pin as an input  

#set status default
GPIO.output(moter1_in1,GPIO.LOW)
GPIO.output(moter1_in2,GPIO.LOW)
moter1_pwm=GPIO.PWM(moter1_en,1000)
moter1_pwm.start(25)

GPIO.output(moter2_in1,GPIO.LOW)
GPIO.output(moter2_in2,GPIO.LOW)
moter2_pwm=GPIO.PWM(moter2_en,1000)
moter2_pwm.start(25)

GPIO.output(moter3_in1,GPIO.LOW)
GPIO.output(moter3_in2,GPIO.LOW)
moter3_pwm=GPIO.PWM(moter3_en,1000)
moter3_pwm.start(25)

####### end moter #########

def moveMoter1(speed):
    GPIO.output(moter1_in1,GPIO.HIGH)
    GPIO.output(moter1_in2,GPIO.LOW)
    moter1_pwm.ChangeDutyCycle(speed)
    return 0

def backMoter1(speed):
    GPIO.output(moter1_in1,GPIO.LOW)
    GPIO.output(moter1_in2,GPIO.HIGH)
    moter1_pwm.ChangeDutyCycle(speed)
    return 0

def stopMoter1():
    GPIO.output(moter1_in1,GPIO.LOW)
    GPIO.output(moter1_in2,GPIO.LOW)
    return 0

def moveMoter2(speed):
    GPIO.output(moter2_in1,GPIO.HIGH)
    GPIO.output(moter2_in2,GPIO.LOW)
    moter2_pwm.ChangeDutyCycle(speed)
    return 0

def backMoter2(speed):
    GPIO.output(moter2_in1,GPIO.LOW)
    GPIO.output(moter2_in2,GPIO.HIGH)
    moter2_pwm.ChangeDutyCycle(speed)
    return 0

def stopMoter2():
    GPIO.output(moter2_in1,GPIO.LOW)
    GPIO.output(moter2_in2,GPIO.LOW)
    return 0


def moveMoter3(speed):
    GPIO.output(moter3_in1,GPIO.HIGH)
    GPIO.output(moter3_in2,GPIO.LOW)
    moter3_pwm.ChangeDutyCycle(speed)
    return 0
def stopMoter3():
    GPIO.output(moter3_in1,GPIO.LOW)
    GPIO.output(moter3_in2,GPIO.LOW)
    return 0

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        uic.loadUi("program4.ui", self)
    
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        
        self.ActionLeft = False
        self.ActionRight = False
        self.ActionUp = False
#         self.ActionClose = False
        self.ActionOpen = False
        self.ActionDown = False
 
        self.BntLeft = self.findChild(QPushButton, 'pushButton_4') # Find the button
        self.BntLeft.clicked.connect(self.Left) # 
        self.BntRight = self.findChild(QPushButton, 'pushButton_3') # Find the button
        self.BntRight.clicked.connect(self.Right) #
        self.BntUp = self.findChild(QPushButton, 'pushButton') # Find the button
        self.BntUp.clicked.connect(self.Up) # 
        self.BntDown = self.findChild(QPushButton, 'pushButton_2') # Find the button
        self.BntDown.clicked.connect(self.Down) #
        self.BntOpen = self.findChild(QPushButton, 'pushButton_5') # Find the button
        self.BntOpen.clicked.connect(self.Open) # 
        self.BntClose = self.findChild(QPushButton, 'pushButton_6') # Find the button
        self.BntClose.clicked.connect(self.Close) # 
 
 
        self.showMaximized()
        
    def Left(self):
        self.ActionLeft = True
        self.ActionRight = False
    def Right(self):
        self.ActionLeft = False
        self.ActionRight = True
    def Up(self):
        self.ActionUp = True
        self.ActionDown = False
    def Down(self):
        self.ActionUp = False
        self.ActionDown = True
    def Open(self):
        self.ActionOpen = True
#         self.ActionClose = False
    def Close(self):
        self.ActionOpen = False
#         self.ActionClose = True
    
    def recurring_timer(self):      
        if(GPIO.input(switchDOWN) ==1):
#             print("test")
#             moveMoter1(100)
            if(self.ActionLeft):
                print("ActionLeft")
                moveMoter1(100)
                sleep(0.5)
                stopMoter1()
                self.ActionLeft = False
        
            
        if(GPIO.input(switchUP) ==1):
            if(self.ActionRight):
                print("ActionRight")
                backMoter1(100)
                sleep(0.5)
                stopMoter1()
                self.ActionRight = False
                
        if(GPIO.input(switchUP2) ==1):
            if(self.ActionUp):
                print("ActionUp")
                moveMoter2(100)
                sleep(0.5)
                stopMoter2()
                self.ActionUp = False
        
            
        if(GPIO.input(switchDOWN2) ==1):
            if(self.ActionDown):
                print("ActionDown")
                backMoter2(100)
                sleep(0.5)
                stopMoter2()
                self.ActionDown = False
        
    
            
        if(self.ActionOpen):
            moveMoter3(100)
        else:
            stopMoter3()

    
  

         
           
            
    

    
 
 
 
app = QApplication(sys.argv)
window = UI()
app.exec_()