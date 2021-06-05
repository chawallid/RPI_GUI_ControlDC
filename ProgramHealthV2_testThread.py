from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QSpinBox, QCheckBox, QVBoxLayout ,QWidget, QLabel,QSlider
from PyQt5 import uic
import sys
from time import sleep, time
from PyQt5.QtCore import *
import datetime
from number_pad import numberPopup

countDegreeValue = 0
clickClose  = True
countClick = True

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
        
class Worker(QRunnable):
    @pyqtSlot()
    def run(self):
        while True:
            if not clickClose:
                break
            print("Working thread 2")
            sleep(1)

class Thread(QThread):
    def run(self):
        global countClick
        while True:
            if not countClick:
                break
            sleep(0.1)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main.ui", self)
        self.exit = self.findChild(QPushButton, 'exit') 
        self.exit.clicked.connect(self.close)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

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
        
 
        self.btnBack1 = self.window1.findChild(QPushButton, 'back') 
        self.btnBack1.clicked.connect(self.clickBack) 

        self.btnBack2 = self.window2.findChild(QPushButton, 'back') 
        self.btnBack2.clicked.connect(self.clickBack) 

        self.btnBack3 = self.window3.findChild(QPushButton, 'back') 
        self.btnBack3.clicked.connect(self.clickBack) 

        self.btnBack4 = self.window4.findChild(QPushButton, 'back') 
        self.btnBack4.clicked.connect(self.clickBack) 

    def clickBtn1(self):
        global countDegreeValue
        self.window1.showFullScreen()
        self.window2.hide()
        self.window3.hide()
        self.window4.hide()
        w.hide()
        self.button2 = self.window1.findChild(QPushButton, 'pushButton_2') # Find the button
        self.button2.clicked.connect(self.StartProgram1) # 
        self.button2.setStyleSheet("background-color: green")
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
        self.checkOpject = True

        worker = Worker()
        self.threadpool.start(worker)
        
        self.thread = Thread()
        self.thread.finished.connect(lambda: self.button2.setEnabled(True))
            
        self.time.setValue(10)
        self.degree.setValue(10)


        
    def StartProgram1(self):
        global countClick
        countClick = True
        self.button2.setEnabled(False)
        self.thread.start()

        for i in range(0,10):
            print(i)
            sleep(1)
        countClick = False
        
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
        return 0
 
        



   
        
        
    def clickBack(self):
        global clickClose
        clickClose = False
        w.showFullScreen()
        self.window1.hide()
        self.window2.hide()
        self.window3.hide()
        self.window4.hide()
        global countDegreeValue
        if(countDegreeValue >=1):
            self.timerCountDegree.stop()

    

app = QApplication(sys.argv)
w = MainWindow()
w.showFullScreen()
w.setWindowTitle('Program Knee support')
app.exec()