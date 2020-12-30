# -*-  coding:utf-8 -*-
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer,Qt
from gui.cppUI.toast import *
import threading


class ToastDialog(QDialog):

    _instance_lock = threading.Lock()
    def __init__(self):
        self.toastDialog = QDialog()
        self.toastDialog.setWindowFlags(self.toastDialog.windowFlags()| Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.toastDialog.setAttribute(Qt.WA_TranslucentBackground, True)
        self.uiToast = Ui_Toast()
        self.uiToast.setupUi(self.toastDialog) 
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
        self.toastDialog.showMaximized()
        self.timer1.start(delay)
        
    def toastClose(self):
        """
        docstring
        """
        self.toastDialog.close()
        self.timer1.stop()