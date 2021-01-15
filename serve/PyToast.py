# -*-  coding:utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer,Qt
from gui.cppUI.toast import *


import threading


class ToastDialog(QDialog):

    _instance_lock = threading.Lock()
    def __init__(self):
        super(ToastDialog,self).__init__()
        self.setWindowFlags(self.windowFlags()| Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.uiToast = Ui_Toast()
        self.uiToast.setupUi(self) 
        self.uiToast.label.setStyleSheet('color:white;background:black;font-size: 100px')

        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.toastClose)

    def __new__(cls, *args, **kwargs):
        if not hasattr(ToastDialog, "_instance"):
            with ToastDialog._instance_lock:
                if not hasattr(ToastDialog, "_instance"):
                    ToastDialog._instance = QDialog.__new__(cls)  
        return ToastDialog._instance


    def toastLabel(self,labelText,delay=1000):
        """
        docstring
        """
        
        self.uiToast.label.setText(labelText)
        self.showMaximized()
        self.timer1.timeout.connect(self.toastClose)
        self.timer1.start(delay)
        # print('显示通知{}'.format(delay))
        
    def toastClose(self):
        """
        docstring
        """
        self.close()
        self.timer1.stop()