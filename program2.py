from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QSpinBox, QCheckBox
from PyQt5 import uic
import sys
from time import sleep

import datetime
from number_pad import numberPopup





class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("program2.ui", self)
 
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
        UI.mouseReleaseEvent = self.onClick

        self.time.setValue(10)
        self.degree.setValue(10)
       
 
        self.show()
 
    def Start(self):
        print("start")

    def Edit1(self):
        self.exPopup = numberPopup(uic,self.time, "Time:", self.callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,600, 600)
        self.exPopup.show()
    def Edit2(self):
        self.exPopup = numberPopup(uic,self.degree, "Time:", self.callBackOnSubmit, "Argument 1", "Argument 2")
        self.exPopup.setGeometry(130, 320,600, 600)
        self.exPopup.show()
        

    def Stop(self):
        print("stop")

    def onClick(self,e):
        self.setEnabled(True)

    def callBackOnSubmit(self, arg1, arg2): 
        print("Function is called with args: %s & %s" % (arg1, arg2))

 
 
 
app = QApplication(sys.argv)
window = UI()
app.exec_()
