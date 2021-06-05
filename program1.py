from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QSpinBox, QCheckBox
from PyQt5 import uic
import sys
import RPi.GPIO as GPIO          
from time import sleep
import datetime
from number_pad import numberPopup



##### sensor moter 1 ######
switchUP = 12 #pin limit switch1
switchDOWN = 16 #pin limit switch2

##### sensor moter 3 ######
irUP = 14 #pin limit switch1


####### moter1 #######
moter1_in1 = 24 # +
moter1_in2 = 23 # - 
moter1_en = 25 #pwm

####### moter3 #######
moter3_in1 = 22 # +
moter3_in2 = 27 # - 
moter3_en = 17 #pwm

#define output moter 
GPIO.setmode(GPIO.BCM)
GPIO.setup(moter1_in1,GPIO.OUT)
GPIO.setup(moter1_in2,GPIO.OUT)
GPIO.setup(moter1_en,GPIO.OUT)

GPIO.setup(moter3_in1,GPIO.OUT)
GPIO.setup(moter3_in2,GPIO.OUT)
GPIO.setup(moter3_en,GPIO.OUT)

GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  
GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  
GPIO.setup(irUP, GPIO.IN)  # set pin as an input  

#set status default
GPIO.output(moter1_in1,GPIO.LOW)
GPIO.output(moter1_in2,GPIO.LOW)
moter1_pwm=GPIO.PWM(moter1_en,1000)
moter1_pwm.start(25)

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
        uic.loadUi("program1.ui", self)
 
        self.button2 = self.findChild(QPushButton, 'pushButton_2') # Find the button
        self.button2.clicked.connect(self.Start) # 
        self.button = self.findChild(QPushButton, 'pushButton') # Find the button
        self.button.clicked.connect(self.Stop) #
        
        self.button3 = self.findChild(QPushButton, 'pushButton_3') # Find the button
        self.button3.clicked.connect(self.Edit1) # 
        self.button4 = self.findChild(QPushButton, 'pushButton_4') # Find the button
        self.button4.clicked.connect(self.Edit2) # 

        self.time = self.findChild(QSpinBox, 'spinBox') # Find the button
        self.degree = self.findChild(QSpinBox, 'spinBox_2')
        self.shack = self.findChild(QCheckBox, 'checkBox')

        self.time.setValue(10)
        self.degree.setValue(10)
       
        
        self.showMaximized()

 
    def Start(self):
        #define output moter 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(moter1_in1,GPIO.OUT)
        GPIO.setup(moter1_in2,GPIO.OUT)
        GPIO.setup(moter1_en,GPIO.OUT)

        GPIO.setup(moter3_in1,GPIO.OUT)
        GPIO.setup(moter3_in2,GPIO.OUT)
        GPIO.setup(moter3_en,GPIO.OUT)

        GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  
        GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  
        GPIO.setup(irUP, GPIO.IN)  # set pin as an input  

      
        
        now= datetime.datetime.now()
        prevTime = int(now.minute)
        tmp = 0
        tmp_degree = 0
        time_count_degree= int((16/100)*self.degree.value())
        
        #range(20-30)
        if(20<self.degree.value()<30):
            time_count_degree = 2
        ##############
            
        if(self.degree.value()>80):
            time_count_degree = time_count_degree +2
        while True :
            now= datetime.datetime.now()
            print(self.time.value())
            print(self.degree.value())
            print(self.shack.isChecked())
            print(GPIO.input(switchUP))
            print(GPIO.input(switchDOWN))
            print(GPIO.input(irUP))
            print(time_count_degree)

           
            if(tmp==0):
                moveMoter1(100)
                sleep(2)
                tmp = tmp +1
            
           
            if((GPIO.input(switchDOWN) ==1 and GPIO.input(switchUP) ==1)):
                
                if(tmp_degree > time_count_degree):
                    print("stopp keep")
                    stopMoter1()              
                else:
                    moveMoter1(100)
                    tmp_degree = tmp_degree +1
                    
            else:
                stopMoter1()
            sleep(1)
           
                
            if(self.shack.isChecked() == True):
                moveMoter3(100)
           
#             
            print('Start',now.minute,":",now.second)
            if(abs(now.minute - prevTime) > self.time.value()):
                if(self.shack.isChecked() == True):
                    while True :
                        moveMoter3(100)
                        if(GPIO.input(irUP) ==1):
                            sleep(3)
                            stopMoter3()
                            break
                    
                sleep(2)
                self.Stop()
                break
            
        
        return 0 
    
    def Edit1(self):
        self.exPopup = numberPopup(uic,self.time, "Time:", self.callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,400, 400)
        self.exPopup.show()
    def Edit2(self):
        self.exPopup = numberPopup(uic,self.degree, "Time:", self.callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,400, 400)
        self.exPopup.show()
        
    def callBackOnSubmit(self, arg1, arg2): 
        print("Function is called with args: %s & %s" % (arg1, arg2))
        
    def Stop(self):
        print('Stop')
        tmp = 0
        while True :
            if(tmp==0):
                backMoter1(100)
                sleep(2)
                tmp = tmp +1
            
            if(GPIO.input(switchDOWN) ==1):
                backMoter1(100)
            else:
                stopMoter1()
                break
            if(GPIO.input(switchUP) ==1):
                backMoter1(self.degree.value())
            else:
                stopMoter1()
                break
        stopMoter1()
        GPIO.cleanup()
        
        return 0
 
    # def clickedBtn(self):
    #     self.textEdit.setPlainText("Please subscribe the channnel and like the videos")
 
 
 
 
 
 
app = QApplication(sys.argv)
window = UI()
app.exec_()