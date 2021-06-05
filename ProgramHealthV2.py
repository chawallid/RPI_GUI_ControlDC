from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QSpinBox, QCheckBox, QVBoxLayout ,QWidget, QLabel,QSlider
from PyQt5 import uic
import sys
from time import sleep, time
import RPi.GPIO as GPIO          
from PyQt5.QtCore import *
import datetime
from number_pad import numberPopup

##### sensor moter 1 ######
switchUP = 12 #pin limit switch1
switchDOWN = 16 #pin limit switch2

##### sensor moter 2 ######
switchUP2 = 6 #pin limit switch1
switchDOWN2 = 5 #pin limit switch2

##### sensor moter 3 ######
irUP = 14 #pin ir motor3
irCount = 18 #pin ir motor1

switchEmergency = 21

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

countDegreeValue = 0
clickClose = True
checkOpject = True

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
GPIO.setup(irCount, GPIO.IN)  # set pin as an input  
GPIO.setup(switchEmergency, GPIO.IN)  # set pin as an input  


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

class Worker(QRunnable):
    @pyqtSlot()
    def run(self):
        global clickClose,countDegreeValue
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(irCount, GPIO.IN) 
        countDegreeValue = 0
        while True:
            global checkOpject
            if not clickClose:
                break
            if(checkOpject): #Count Each Round 
                if((GPIO.input(irCount) == 1)): #In range IR detect 
                    countDegreeValue = countDegreeValue +1
                    checkOpject = False
            else: 
                if((GPIO.input(irCount) == 0)): #Out range IR detect 
                    checkOpject = True
            sleep(0.01)

class Program1(QMainWindow):
    def __init__(self):
        super(Program1, self).__init__()
        uic.loadUi("program1.ui", self)

class Program2(QMainWindow):
    def __init__(self):
        super(Program2, self).__init__()
        uic.loadUi("program2.ui", self)    

class Program3(QMainWindow):
    def __init__(self):
        super(Program3, self).__init__()
        uic.loadUi("program3.ui", self)

class Program4(QMainWindow):
    def __init__(self):
        super(Program4, self).__init__()
        uic.loadUi("program4.ui", self)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main.ui", self)
        self.exit = self.findChild(QPushButton, 'exit') 
        self.exit.clicked.connect(self.close)

        self.btnReset = self.findChild(QPushButton, 'resetbtn') 
        self.btnReset.clicked.connect(self.reset)

        self.window1 = Program1()
        self.window1.setWindowTitle('Program1')
        self.window2 = Program2()
        self.window2.setWindowTitle('Program2')
        self.window3 = Program3()
        self.window3.setWindowTitle('Program3')
        self.window4 = Program4()
        self.window4.setWindowTitle('Program4')

        self.btnProgram1 = self.findChild(QPushButton, 'manu1') 
        self.btnProgram1.clicked.connect(self.clickBtn1) 
        
        self.btnProgram2 = self.findChild(QPushButton, 'manu2') 
        self.btnProgram2.clicked.connect(self.clickBtn2) 

        self.btnProgram3 = self.findChild(QPushButton, 'manu3') 
        self.btnProgram3.clicked.connect(self.clickBtn3) 

        self.btnProgram4 = self.findChild(QPushButton, 'manu4') 
        self.btnProgram4.clicked.connect(self.clickBtn4) 

        self.btnBack1 = self.window1.findChild(QPushButton, 'back') 
        self.btnBack1.clicked.connect(self.clickBack) 

        self.btnBack2 = self.window2.findChild(QPushButton, 'back') 
        self.btnBack2.clicked.connect(self.clickBack) 

        self.btnBack3 = self.window3.findChild(QPushButton, 'back') 
        self.btnBack3.clicked.connect(self.clickBack) 

        self.btnBack4 = self.window4.findChild(QPushButton, 'back') 
        self.btnBack4.clicked.connect(self.clickBack) 

    def clickBtn1(self):
        global countDegreeValue,checkOpject
        self.window1.showFullScreen()
        self.window2.hide()
        self.window3.hide()
        self.window4.hide()
        w.hide()

        self.button2 = self.window1.findChild(QPushButton, 'pushButton_2') # Find the button
        self.button2.clicked.connect(self.StartProgram1) # 
        self.button = self.window1.findChild(QPushButton, 'pushButton') # Find the button
        self.button.clicked.connect(self.StopProgram1) #
        
        self.button3 = self.window1.findChild(QPushButton, 'pushButton_3') # Find the button
        self.button3.clicked.connect(self.Edit1) # 
        self.button4 = self.window1.findChild(QPushButton, 'pushButton_4') # Find the button
        self.button4.clicked.connect(self.Edit2) # 

        self.time = self.window1.findChild(QSpinBox, 'spinBox') # Find the button
        self.degree = self.window1.findChild(QSpinBox, 'spinBox_2')
        self.shack = self.window1.findChild(QCheckBox, 'checkBox')
        self.shack.setStyleSheet("QCheckBox::indicator { width: 60px; height: 60px;}")

        countDegreeValue = 0 
        checkOpject = True
        
        self.time.setValue(10)
        self.degree.setValue(10)
        
    def StartProgram1(self):
        sleep(2)
        global countDegreeValue,clickClose
        clickClose = True
        countDegreeValue = 0
        print("Start Program1")
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.worker = Worker()
        self.threadpool.start(self.worker)
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
        GPIO.setup(switchEmergency, GPIO.IN)  # set pin as an input  

        now= datetime.datetime.now()
        prevTime = int(now.minute)

        tmp = True
        tmp_degree = 0
        valueDegree = int(self.degree.value())
        ratioRoundPerValue = 100/95
        if (valueDegree >= 80):
            ratioRoundPerValue = 100/87.5
        if (valueDegree >= 90):
            ratioRoundPerValue = 100/85
        if (valueDegree >= 100):
            ratioRoundPerValue = 100/76
            
        time_count_degree = int(ratioRoundPerValue*(valueDegree-14))
           
        if (valueDegree >= 105):
            time_count_degree = 115
        
        tmp_time = True
        
        while True :
           
            now= datetime.datetime.now()

            if(GPIO.input(switchEmergency) ==1):
                if(tmp==True and time_count_degree > 0):
                    moveMoter1(100)
                    sleep(1.5)
                    tmp = False
                if((GPIO.input(switchDOWN) ==1) and (GPIO.input(switchUP) ==1)):
                    if(tmp_degree >= time_count_degree):
                        print("Stop Motor1")
                        stopMoter1()
                        if tmp_time:
                            now= datetime.datetime.now()
                            prevTime = int(now.minute)
                            tmp_time = False
                        
                    else:
                        print("Move Motor1")
                        moveMoter1(90)
                        tmp_degree = countDegreeValue #Get ValueCount From Fucntion To Update
                else:
                    stopMoter1()
                
                if not tmp_time:   
                    if(abs(now.minute - prevTime) < self.time.value()):
                        #Move Motor3    
                        if(self.shack.isChecked() == True):
                            moveMoter3(100)
                    else: 
                        #Stop Motor3 and Check IR sensor
                        if(self.shack.isChecked() == True):
                            while True :
                                moveMoter3(100)
                                if(GPIO.input(irUP) ==1):
                                    sleep(3)
                                    stopMoter3()
                                    break
                        sleep(2)
                        self.StopProgram1()
                        break
            else:
                stopMoter1()
                stopMoter2()
                stopMoter3()
                break
            sleep(0.001)
        
        return 0 
    
    def Edit1(self):
        self.exPopup = numberPopup(uic,self.time, "Time:", self.callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,400, 400)
        self.exPopup.show()

    def Edit2(self):
        self.exPopup = numberPopup(uic,self.degree, "Time:", self.callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,400, 400)
        self.exPopup.show()

    def Edit3(self):
        self.exPopup = numberPopup(uic,self.degree_foot, "Time:", self.callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,400, 400)
        self.exPopup.show()
        
    def callBackOnSubmit(self, arg1, arg2): 
        print("Function is called with args: %s & %s" % (arg1, arg2))
        
    def StopProgram1(self):
        print('Stop Program1')
        global countDegreeValue,clickClose
        clickClose = False
        countDegreeValue = 0
        

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

        GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  motor1
        GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  motor1
        GPIO.setup(switchUP2, GPIO.IN)  # set a pin as an input motor2
        GPIO.setup(switchDOWN2, GPIO.IN)  # set pin as an input  motor2 
        GPIO.setup(irUP, GPIO.IN)  # set pin as an input  

        tmp = True
        while True :
            if((GPIO.input(switchDOWN) ==0)):
                if(tmp==True):
                    backMoter1(100)
                    sleep(2)
                    tmp = False

            if((GPIO.input(switchDOWN) ==1) and (GPIO.input(switchUP) ==1)):
                backMoter1(100)
            else:
                stopMoter1()
                break
        stopMoter1()
        GPIO.cleanup()

        return 0
 
    def clickBtn2(self):
        global countDegreeValue,checkOpject
        self.window1.hide()
        self.window2.showFullScreen()
        self.window3.hide()
        self.window4.hide()
        w.hide()
        
        self.button2 = self.window2.findChild(QPushButton, 'pushButton_2') # Find the button
        self.button2.clicked.connect(self.StartProgram2) # 
        self.button = self.window2.findChild(QPushButton, 'pushButton') # Find the button
        self.button.clicked.connect(self.StopProgram2) #
        
        self.button3 = self.window2.findChild(QPushButton, 'pushButton_3') # Find the button
        self.button3.clicked.connect(self.Edit1) # 
        self.button4 = self.window2.findChild(QPushButton, 'pushButton_4') # Find the button
        self.button4.clicked.connect(self.Edit2) # 
        
        self.slider = self.window2.findChild(QSlider, 'horizontalSlider')
        self.slider.valueChanged.connect(self.value_changed)

        self.textedit = self.window2.findChild(QLabel, 'label_4')
        self.time = self.window2.findChild(QSpinBox, 'spinBox') # Find the button
        self.degree = self.window2.findChild(QSpinBox, 'spinBox_2')
        self.shack = self.window2.findChild(QCheckBox, 'checkBox')
        self.shack.setStyleSheet("QCheckBox::indicator { width: 60px; height: 60px;}")

        self.time.setValue(10)
        self.degree.setValue(10)
        self.textedit.setText(str(1))

        countDegreeValue = 0 
        checkOpject = True

    def value_changed(self):
        self.textedit.setText(str(self.slider.value()))

    def SubProgramMove(self):
        global countDegreeValue,clickClose
        clickClose = True
        countDegreeValue = 0
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.worker = Worker()
        self.threadpool.start(self.worker)
        
        tmp = True
        tmp_degree = 0 
        valueDegree = int(self.degree.value())
        ratioRoundPerValue = 100/95

        #### calibrate degree ######
        if (valueDegree >= 80):
            ratioRoundPerValue = 100/87.5
        elif (valueDegree >= 90):
            ratioRoundPerValue = 100/85
        elif (valueDegree >= 100):
            ratioRoundPerValue = 100/76
        ###########################

        ###### Over Limit #########  
        if (valueDegree >= 105):
            time_count_degree = 115
        else:
            time_count_degree = int(ratioRoundPerValue*(valueDegree-14))
        ###########################

        stepSpeed= self.slider.value()
        speed = 60 #default speed
        if (stepSpeed ==1):
            speed = 100
        elif (stepSpeed ==2):
            speed = 90
        elif (stepSpeed ==3):
            speed = 80
        elif (stepSpeed ==4):
            speed = 70
        else:
            speed = 60

        while True :
            if(GPIO.input(switchEmergency) ==1):
                if(tmp==True and time_count_degree > 0):
                    countDegreeValue =0
                    moveMoter1(100)
                    sleep(1.5)
                    tmp = False
                if((GPIO.input(switchDOWN) ==1) and (GPIO.input(switchUP) ==1)):
                    if(tmp_degree >= time_count_degree):
                        print("Stop Motor1")
                        stopMoter1()
                        break              
                    else:
                        print("Move Motor1")
                        moveMoter1(speed)
                        tmp_degree = countDegreeValue
                else:
                    stopMoter1()
                    break
            else:
                break
            sleep(0.01)
        return 0 
        
    def SubProgramBack(self):
        global countDegreeValue,clickClose
        clickClose = False
        countDegreeValue = 0
        tmp = True
        stepSpeed= self.slider.value()
        speed = 60
        if (stepSpeed ==1):
            speed = 100
        elif (stepSpeed ==2):
            speed = 90
        elif (stepSpeed ==3):
            speed = 80
        elif (stepSpeed ==4):
            speed = 70
        else:
            speed = 60
        while True :
            if(tmp==True):
                backMoter1(speed)
                sleep(2)
                tmp = False
            
            if((GPIO.input(switchDOWN) ==1) and (GPIO.input(switchUP) ==1)):
                backMoter1(speed)
            else:
                stopMoter1()
                break
        stopMoter1()
        return 0

    def StartProgram2(self):
        sleep(1)
        print("Start Program2")
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(moter1_in1,GPIO.OUT)
        GPIO.setup(moter1_in2,GPIO.OUT)
        GPIO.setup(moter1_en,GPIO.OUT)

        GPIO.setup(moter3_in1,GPIO.OUT)
        GPIO.setup(moter3_in2,GPIO.OUT)
        GPIO.setup(moter3_en,GPIO.OUT)

        GPIO.setup(switchUP, GPIO.IN)  
        GPIO.setup(switchDOWN, GPIO.IN)  
        GPIO.setup(switchEmergency, GPIO.IN)  

        now= datetime.datetime.now()
        prevTime = int(now.minute)

        while True:
            now= datetime.datetime.now()
            if(GPIO.input(switchEmergency) ==1):
                if(abs(now.minute - prevTime) <= self.time.value()):
                    if(self.shack.isChecked() == True):
                        moveMoter3(100)
                    self.SubProgramMove()
                    self.SubProgramBack()
                else: 
                    if(self.shack.isChecked() == True):
                        while True :
                            moveMoter3(100)
                            if(GPIO.input(irUP) ==1):
                                sleep(3)
                                stopMoter3()
                                break
                    sleep(2)
                    break
            else:
                stopMoter1()
                stopMoter2()
                stopMoter3()
                break
            sleep(0.1)

    def StopProgram2(self):
        self.StopProgram1()
        print("Stop Program2")
        
    def clickBtn3(self):
        self.window1.hide()
        self.window2.hide()
        self.window3.showFullScreen()
        self.window4.hide()
        w.hide()
        
        self.button2 = self.window3.findChild(QPushButton, 'pushButton_2') # Find the button
        self.button2.clicked.connect(self.StartProgram3) # 
        self.button = self.window3.findChild(QPushButton, 'pushButton') # Find the button
        self.button.clicked.connect(self.StopProgram3) #
        
        self.button3 = self.window3.findChild(QPushButton, 'pushButton_3') # Find the button
        self.button3.clicked.connect(self.Edit1) # 
        self.button4 = self.window3.findChild(QPushButton, 'pushButton_4') # Find the button
        self.button4.clicked.connect(self.Edit2) #
        self.button5 = self.window3.findChild(QPushButton, 'pushButton_5') # Find the button
        self.button5.clicked.connect(self.Edit3) # 

        self.time = self.window3.findChild(QSpinBox, 'spinBox') # Find the button
        self.degree = self.window3.findChild(QSpinBox, 'spinBox_2')
        self.degree_foot = self.window3.findChild(QSpinBox, 'spinBox_3')
        self.shack = self.window3.findChild(QCheckBox, 'checkBox')
        self.shack.setStyleSheet("QCheckBox::indicator { width: 60px; height: 60px;}")


        global countDegreeValue,checkOpject
        countDegreeValue = 0 
        checkOpject = True

        self.time.setValue(10)
        self.degree.setValue(10)
        self.degree_foot.setValue(10)

    def StartProgram3(self):
        sleep(1) #Protect Press dubble
        print("Start Program3")
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

        GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  motor1
        GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  motor1
        GPIO.setup(switchUP2, GPIO.IN)  # set a pin as an input motor2
        GPIO.setup(switchDOWN2, GPIO.IN)  # set pin as an input  motor2 
        GPIO.setup(irUP, GPIO.IN)  # set pin as an input  
        GPIO.setup(switchEmergency, GPIO.IN)  # set pin as an input  

        global countDegreeValue,clickClose
        clickClose = True
        countDegreeValue = 0

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.worker = Worker()
        self.threadpool.start(self.worker)
        
        tmp = True
        tmp_degree = 0 
        valueDegree = int(self.degree.value())
        ratioRoundPerValue = 100/95

        #### calibrate degree ######
        if (valueDegree >= 80):
            ratioRoundPerValue = 100/87.5
        elif (valueDegree >= 90):
            ratioRoundPerValue = 100/85
        elif (valueDegree >= 100):
            ratioRoundPerValue = 100/76
        ###########################

        ###### Over Limit #########  
        if (valueDegree >= 105):
            time_count_degree = 115
        else:
            time_count_degree = int(ratioRoundPerValue*(valueDegree-14))
        ###########################

        now= datetime.datetime.now()
        prevTime = int(now.minute)

        tmp = True
        tmp_motor2 = True
        tmp_time  = True

        tmp_height = 0
        height_count_degree = int((26/40)*(self.degree_foot.value()-15))

        #Height Setting 
        if(self.degree_foot.value()<60):#Height cm.
            height_count_degree = int((26/40)*(self.degree_foot.value()-15)) -1 #Output is a Time unit

        

        while True :
            now= datetime.datetime.now()
            if(GPIO.input(switchEmergency) ==1):
                if(tmp==True and time_count_degree > 0):
                    countDegreeValue = 0
                    moveMoter1(100)
                    sleep(1.5)
                    tmp = False
                
                if((GPIO.input(switchDOWN) ==1 and GPIO.input(switchUP) ==1)):
                    
                    if(tmp_degree > time_count_degree):
                        stopMoter1()
                        ## start process motor 2 ##   
                        if(height_count_degree > 0):
                            if(tmp_motor2==True):
                                moveMoter2(100)
                                sleep(2)
                                tmp_motor2 = False

                        if((GPIO.input(switchDOWN2) ==1 and GPIO.input(switchUP2) ==1)):
                            if(tmp_height >= height_count_degree):
                                stopMoter2()
                                if tmp_time:
                                    now= datetime.datetime.now()
                                    prevTime = int(now.minute)
                                    tmp_time = False
                            else:
                                moveMoter2(100)
                                tmp_height = tmp_height +1
                                sleep(1)
                        else:
                            if tmp_time:
                                now= datetime.datetime.now()
                                prevTime = int(now.minute)
                                tmp_time = False

                            stopMoter2()
                                
                    else:
                        moveMoter1(100)
                        tmp_degree = countDegreeValue
                        
                else:
                    stopMoter1()
            else:
                stopMoter1()
                stopMoter2()
                stopMoter3()
                break       
            
            if not tmp_time:   
                if(abs(now.minute - prevTime) < self.time.value()):
                    #Move Motor3    
                    if(self.shack.isChecked() == True):
                        moveMoter3(100)
                else: 
                    #Stop Motor3 and Check IR sensor
                    if(self.shack.isChecked() == True):
                        while True :
                            moveMoter3(100)
                            if(GPIO.input(irUP) ==1):
                                sleep(3)
                                stopMoter3()
                                break
                    sleep(2)
                    self.StopProgram3()
                    break
            sleep(0.001)
        return 0 

    def StopProgram3(self):
        print('Stop Program3')
        global countDegreeValue,clickClose
        clickClose = False

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

        GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  motor1
        GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  motor1
        GPIO.setup(switchUP2, GPIO.IN)  # set a pin as an input motor2
        GPIO.setup(switchDOWN2, GPIO.IN)  # set pin as an input  motor2 
        GPIO.setup(irUP, GPIO.IN)  # set pin as an input  

        tmp = True
        tmp_motor2 = True

        while True :
            if(tmp_motor2==True):
                backMoter2(100)
                sleep(2)
                tmp_motor2 = False

            if((GPIO.input(switchDOWN2) ==1) and (GPIO.input(switchUP2) ==1)):
                backMoter2(100)
            else:
                stopMoter2()

                if((GPIO.input(switchDOWN) ==0)):
                    if(tmp==True):
                        backMoter1(100)
                        sleep(2)
                        tmp = False

                if((GPIO.input(switchDOWN) ==1) and (GPIO.input(switchUP) ==1)):
                    backMoter1(100)
                else:
                    stopMoter1()
                    break

        stopMoter1()
        stopMoter2()
        stopMoter3()
        GPIO.cleanup()
        
        return 0
           
    def clickBtn4(self):
        global countDegreeValue,checkOpject
        
        self.window1.hide()
        self.window2.hide()
        self.window3.hide()
        self.window4.showFullScreen()
        
        w.hide()
        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(irCount, GPIO.IN)  # set pin as an input  
        
        countDegreeValue = 0 
        checkOpject = True
  
        self.ActionLeft = False
        self.ActionRight = False
        self.ActionUp = False
        self.ActionOpen = False
        self.ActionDown = False
 
        self.BntLeft = self.window4.findChild(QPushButton, 'pushButton_4') # Find the button
        self.BntLeft.clicked.connect(self.Left) # 
        self.BntRight = self.window4.findChild(QPushButton, 'pushButton_3') # Find the button
        self.BntRight.clicked.connect(self.Right) #
        self.BntUp = self.window4.findChild(QPushButton, 'pushButton') # Find the button
        self.BntUp.clicked.connect(self.Up) # 
        self.BntDown = self.window4.findChild(QPushButton, 'pushButton_2') # Find the button
        self.BntDown.clicked.connect(self.Down) #
        self.BntOpen = self.window4.findChild(QPushButton, 'pushButton_5') # Find the button
        self.BntOpen.clicked.connect(self.Open) # 
        self.BntClose = self.window4.findChild(QPushButton, 'pushButton_6') # Find the button
        self.BntClose.clicked.connect(self.Close) # 
        self.textCount = self.window4.findChild(QLabel, 'label_2') # Find the button
          
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
    def Close(self):
        self.ActionOpen = False
    def recurring_timer(self):
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

        GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  motor1
        GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  motor1
        GPIO.setup(switchUP2, GPIO.IN)  # set a pin as an input motor2
        GPIO.setup(switchDOWN2, GPIO.IN)  # set pin as an input  motor2 
        GPIO.setup(irUP, GPIO.IN)  # set pin as an input        
        

        if(GPIO.input(switchDOWN) ==1):
            if(self.ActionLeft):
                print("ActionLeft")
                moveMoter1(90)
                sleep(0.1)
                stopMoter1()
                self.ActionLeft = False
          
        if(GPIO.input(switchUP) ==1):
            if(self.ActionRight):
                print("ActionRight")
                backMoter1(90)
                sleep(0.1)
                stopMoter1()
                self.ActionRight = False
                
        if(GPIO.input(switchUP2) ==1):
            if(self.ActionUp):
                print("ActionUp")
                moveMoter2(90)
                sleep(0.1)
                stopMoter2()
                self.ActionUp = False

        if(GPIO.input(switchDOWN2) ==1):
            if(self.ActionDown):
                print("ActionDown")
                backMoter2(90)
                sleep(0.1)
                stopMoter2()
                self.ActionDown = False
        
        if(self.ActionOpen):
            moveMoter3(100)
        else:
            stopMoter3()  
        
    def clickBack(self):
        global countDegreeValue,clickClose
        clickClose = False
        countDegreeValue = 0

        w.showFullScreen()
        self.window1.hide()
        self.window2.hide()
        self.window3.hide()
        self.window4.hide()
        
    def reset(self):
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

        GPIO.setup(switchUP, GPIO.IN)  # set a pin as an input  motor1
        GPIO.setup(switchDOWN, GPIO.IN)  # set pin as an input  motor1
        GPIO.setup(switchUP2, GPIO.IN)  # set a pin as an input motor2
        GPIO.setup(switchDOWN2, GPIO.IN)  # set pin as an input  motor2 
        GPIO.setup(irUP, GPIO.IN)  # set pin as an input  

        if((GPIO.input(switchDOWN) ==1) and (GPIO.input(switchUP) ==1)):
            self.StopProgram1()
        else:
            if((GPIO.input(switchDOWN2) ==1) and (GPIO.input(switchUP2) ==1)):
                self.StopProgram3()
            else:
                print("Reset ALL Complete")
        GPIO.cleanup()



app = QApplication(sys.argv)
w = MainWindow()
w.showFullScreen()
w.setWindowTitle('Program Knee support')
app.exec()