# -*- coding: utf-8 -*-
import wmi
import time,os,subprocess
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QHostInfo
from PyQt5 import QtWidgets, QtGui,QtCore
from exchangelib import EWSTimeZone, EWSDateTime, EWSDate
import winsound
import json
import requests

from serve.PyMail import *
from serve.PyFileMan import *
from serve.PyExchange import *
import re
import psutil as p
from gui.cppUI.toast import *



class WorkThread(QtCore.QThread):
    sinOut = pyqtSignal(int)
    def __int__(self):
        super(WorkThread,self).__init__()
 
 
    def run(self ):
        global ip
        exit_code = subprocess.call('ping www.baidu.com -n 1', shell=True)
        if exit_code:
            # raise Exception('connect failed.')
            self.sinOut.emit(False)    #反馈信号出去
        else:
            self.sinOut.emit(True) #反馈信号出去


class PyTimerRoutine(object):
    trigger = QtCore.pyqtSignal()
    def __init__(self,unrdModel,exchModel,listDialog,ui_inlook,interval=60000):
        self.unrdModel = unrdModel
        self.exchModel = exchModel
        self.unrdAutoUpdateInterval = interval
        self.listDialog = listDialog
        self.ui_inlook = ui_inlook
        self.labelObj = ui_inlook.statusLabel
        self.toastDialog = 0
        self.netBefore = 0
        self.unrdAutoUpdateTimer = 0
        self.unrdAccCount = 0
        self.agndListItem = 0

        self.queto = False
        

        self.timer1 = QTimer()
        self.timer2 = QTimer()
        self.timer1.timeout.connect(self.toastClose)
        self.timer2.timeout.connect(self.labelMonitor)
        
        self.timer2.start(1000)
        
    def setUnrdAutoUpdateInterval(self,interval=60000):
        self.unrdAutoUpdateInterval = interval

    def getNetDelta(self):#获取下载变化值
        now = p.net_io_counters().bytes_recv
        delta = (now-self.netBefore)/1024 #变成K
        self.netBefore = now
        return  delta #返回改变量
    def toastLabel(self,labelText,delay=1000):
        """
        docstring
        """
        if not self.toastDialog:
            self.toastDialog = QDialog()
            self.toastDialog.setWindowFlags(self.toastDialog.windowFlags()| Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.toastDialog.setAttribute(Qt.WA_TranslucentBackground, True)
            self.uiToast = Ui_Toast()
            self.uiToast.setupUi(self.toastDialog) 
            self.uiToast.label.setStyleSheet('color:white;background:black;font-size: 100px')
        self.uiToast.label.setText(labelText)
        self.toastDialog.showMaximized()
        self.timer1.start(delay)
        
    def toastClose(self):
        """
        docstring
        """
        self.toastDialog.close()
        self.timer1.stop()
        
        
    def labelMonitor(self):
        tmp = self.getNetDelta() #得到下载字节数的变化值
        cpu_p=p.cpu_percent()#读取CPU使用百分比
        mem_p=p.virtual_memory().percent#读取内存使用百分比
        if tmp>1000:
            tmpStr = '{:.1f}MB/s'.format(tmp/1024)
        else:
            tmpStr = '{:.1f}KB/s'.format(tmp)
        # print(tmp,cpu_p,mem_p)
        self.labelObj.setText('{}: {} RAM: {}%'.format(chr(0x2193),tmpStr,mem_p))

    def unrdAutoUpdateTimerStart(self):
        if not self.unrdAutoUpdateTimer:
            self.unrdAutoUpdateTimer = QTimer()
            self.unrdAutoUpdateTimer.timeout.connect(self.unrdAutoUpdate)
        self.unrdAutoUpdateTimer.start(self.unrdAutoUpdateInterval)
    def unrdAutoUpdateTimerStop(self):
        self.unrdAutoUpdateTimer.stop()


    def pingBack(self,netStatus):
        if netStatus:
            if not self.queto:
                url = 'http://open.iciba.com/dsapi/'
                r = requests.get(url)
                obj = json.loads(r.text)
                self.ui_inlook.dayQuetoLabel.setText(obj['content'])
                self.ui_inlook.dayQuetoLabel.setToolTip(obj['note'])
                self.queto = True
            unrdAccInfo,exchAccInfo = PyFileMan().readConfigFile()
            self.exchAccount = []
            unrdAccCount = len(unrdAccInfo)
            if not  unrdAccCount == 0:
                if(not unrdAccCount== self.unrdModel.rowCount()):
                    # clear all data
                    self.unrdModel.removeRows(0,self.unrdModel.rowCount()) 
                    self.unrdModel.insertRows(0,unrdAccCount)
                    self.urndNum =[0 for x in range(0,unrdAccCount)] # 每个账户对应的未读数目

                for i in range(len(unrdAccInfo)):
                    unrdAccount=MailAccount(unrdAccInfo[i][0],unrdAccInfo[i][1],unrdAccInfo[i][2])
                    alias = unrdAccInfo[i][4]
                    retStatus = unrdAccount.login()
                    index = self.unrdModel.index(i)
                    curUnrdNum = unrdAccount.Update()
                    newData = ['{} has {} unread mails.'.format(alias,curUnrdNum),str(curUnrdNum),alias,unrdAccInfo[i][3]]
                    if(curUnrdNum > self.urndNum[i]):
                        self.listDialog.ptray.showMessage('Inlook inform you','your {} mailbox has {} unread mails.'.format(alias,curUnrdNum), QSystemTrayIcon.Information)
                    self.urndNum[i] = curUnrdNum
                    self.unrdModel.setData(index,newData)
                
                if(not self.unrdAccCount == unrdAccount):
                    self.unrdListViewHeight = unrdAccCount*31
                    self.ui_inlook.unrdListView.setMaximumHeight(self.unrdListViewHeight)
                    self.ui_inlook.unrdListView.resize(self.ui_inlook.unrdListView.width(),self.unrdListViewHeight)
                

            exchAccCount = len(exchAccInfo)
            if not exchAccCount ==0:
                self.exchAccount=ExchAccount(exchAccInfo[0][0],exchAccInfo[0][1],exchAccInfo[0][2])
                alias = exchAccInfo[0][4]
                retStatus = self.exchAccount.login()
                # print('{} login {}'.format(alias,retStatus))

                exchStr = self.exchAccount.Update()
                itemNum = len(exchStr)
                if(not itemNum== self.exchModel.rowCount()):
                    # clear all data
                    self.exchModel.removeRows(0,self.exchModel.rowCount()) 
                    self.exchModel.insertRows(0,itemNum)

                unseenNum = exchStr[0][0]
                index = self.exchModel.index(0)
                unseenStr = ['{} has {} unread mails.'.format(alias,unseenNum),unseenNum,alias,'outlook.live.com/mail']
                self.exchModel.setData(index,unseenStr)

                for i in range(1,itemNum):
                    index = self.exchModel.index(i)
                    newData = ['{}\n{}\n{}'.format(exchStr[i][0],exchStr[i][1],exchStr[i][2]),exchStr[i][3],alias,exchAccInfo[0][3]]
                    if exchStr[i][3]:
                        self.toastLabel('{}'.format(newData[0]),20000)
                        for j in range(5):
                            winsound.PlaySound('./sounds/Alarm.wav',flags=1)
                            self.listDialog.ptray.showMessage('Inlook inform you',newData[0], QSystemTrayIcon.Information)
                    self.exchModel.setData(index,newData)
                
                if(not self.agndListItem == itemNum):
                    self.agndListViewHeight=itemNum*81-50
                    self.ui_inlook.agndListView.setMaximumHeight(self.agndListViewHeight)
                    self.ui_inlook.agndListView.resize(self.ui_inlook.agndListView.width(),self.agndListViewHeight)
                

                if((not self.agndListItem == itemNum) or (not self.unrdAccCount == unrdAccount)):
                    self.listDialog.resize(self.listDialog.width(), self.unrdListViewHeight + self.agndListViewHeight+ 225)
                    self.listDialog.selfFlush()
                
                self.agndListItem = itemNum
                self.unrdAccCount = unrdAccount



                # if(curUnrdNum > self.urndNum[i]):
                #     self.diaglog.ptray.showMessage('Inlook inform you','your {} mailbox has {} unread mails.'.format(alias,curUnrdNum), QSystemTrayIcon.Information)
                # self.exchAccount.append()
        else:
            # 清空所有行
            self.unrdModel.removeRows(0,self.unrdModel.rowCount()) 
            # 添加一行
            self.unrdModel.insertRows(0,1)

            index = self.unrdModel.index(0)
            newData = ['Please connect the network.',str(1),'','ms-settings:network-ethernet']
            self.unrdModel.setData(index,newData)

            # 清空所有行
            self.exchModel.removeRows(0,self.unrdModel.rowCount()) 
            # 添加一行
            self.exchModel.insertRows(0,1)

            index = self.exchModel.index(0)
            newData = ['Please connect the network.',str(1),'','ms-settings:network-ethernet']
            self.unrdModel.setData(index,newData)

    def unrdAutoUpdate(self):
        '''
        Auto Update the unrdModel data
        '''
        self.unrdAutoUpdateTimerStart()
        # self.unrdAutoUpdateTimer.stop()
        # unrdAccount,self.exchAccount ,unrdAccount[0]=[server,username,password,website]

        
        
        self.wt = WorkThread()
        #开始执行run()函数里的内容
        self.wt.start()
        # # 收到信号
        self.wt.sinOut.connect(self.pingBack)  #将信号连接至pingBack函数
