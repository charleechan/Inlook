# -*- coding: utf-8 -*-
import wmi
import socket
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
from serve.PyToast import *
import re
import psutil as p





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
    def __init__(self,unrdModel,exchModel,listDialog,ui_inlook,lineHei,spaceHei,viewSpacHei,dpi,interval=60000):
        self.unrdModel = unrdModel
        self.exchModel = exchModel
        self.unrdAutoUpdateInterval = interval
        self.listDialog = listDialog
        self.ui_inlook = ui_inlook
        self.labelObj = ui_inlook.statusLabel
        self.toastDialog = ToastDialog()
        self.netBefore = 0
        self.unrdAutoUpdateTimer = 0
        self.mailAccNum = 0
        self.agndListItem = 0

        self.lineHei     =lineHei
        self.spaceHei    =spaceHei
        self.viewSpacHei =viewSpacHei
        self.dpi = dpi

        self.queto = False
        


        self.timer2 = QTimer()
        
        self.timer2.timeout.connect(self.labelMonitor)
        
        self.timer2.start(1000)
        
    def setUnrdAutoUpdateInterval(self,interval=60000):
        self.unrdAutoUpdateInterval = interval

    def getNetDelta(self):#获取下载变化值
        now = p.net_io_counters().bytes_recv
        delta = (now-self.netBefore)/1024 #变成K
        self.netBefore = now
        return  delta #返回改变量

        
        
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

    def accBatchLogin(self):
        self.unrdAccInfo,self.exchAccInfo = PyFileMan().readConfigFile()
        
        self.mailAcc = []
        self.mailAccStatus = []

        self.mailAccNum = len(self.unrdAccInfo)
        print(self.mailAccNum)
        if not  self.mailAccNum == 0:
            for i in range(self.mailAccNum):
                mailAccI = MailAccount(self.unrdAccInfo[i][0],self.unrdAccInfo[i][1],self.unrdAccInfo[i][2])
                self.mailAcc.append(mailAccI)
                try:
                    retStatus =  self.mailAcc[i].login()
                    self.mailAccStatus.append(retStatus)
                except socket.error as e:
                    self.toastDialog.toastLabel('Mail Account Login ERROR!',2000)
            
            
        self.exchAccCount = len(self.exchAccInfo)
        if not self.exchAccCount ==0:
            self.exchAccount=ExchAccount(self.exchAccInfo[0][0],self.exchAccInfo[0][1],self.exchAccInfo[0][2])
            try:
                retStatus = self.exchAccount.login()
            except socket.error as e:
                self.toastDialog.toastLabel('Exchange Account Login ERROR!',2000)

        self.unrdListViewHeight = self.mailAccNum*(self.lineHei + 2* self.viewSpacHei)
        self.ui_inlook.unrdListView.setMaximumHeight(self.unrdListViewHeight)
        self.ui_inlook.unrdListView.resize(self.ui_inlook.unrdListView.width(),self.unrdListViewHeight)

        self.listDialog.resize(self.listDialog.width(), self.unrdListViewHeight + self.ui_inlook.agndListView.height()+ 225)
        self.listDialog.selfFlush()

        self.unrdAutoUpdate()

        self.unrdAutoUpdateTimerStart()
        
    def accBatchLogout(self):
        self.unrdAutoUpdateTimerStop()
        if not  self.mailAccNum == 0:
            for i in range(self.mailAccNum):
                try:
                    retStatus =  self.mailAcc[i].logout()
                    self.mailAccStatus.append(retStatus)
                except socket.error as e:
                    self.toastDialog.toastLabel('Mail Account Logout ERROR!',2000)
        
        # self.exchAccount.logout()

    def pingBack(self,netStatus):
        if netStatus:
            if not self.queto:
                url = 'http://open.iciba.com/dsapi/'
                r = requests.get(url)
                obj = json.loads(r.text)
                self.ui_inlook.dayQuetoLabel.setText(obj['content'])
                self.ui_inlook.dayQuetoLabel.setToolTip(obj['note'])
                self.queto = True
            if not  self.mailAccNum == 0:
                if(not self.mailAccNum== self.unrdModel.rowCount()):
                    # clear all data
                    self.unrdModel.removeRows(0,self.unrdModel.rowCount()) 
                    self.unrdModel.insertRows(0,self.mailAccNum)
                    self.urndNum =[0 for x in range(0,self.mailAccNum)] # 每个账户对应的未读数目

                for i in range(self.mailAccNum):
                    alias = self.unrdAccInfo[i][4]
                    index = self.unrdModel.index(i)
                    try:
                        curUnrdNum = self.mailAcc[i].Update()
                    except socket.error as e:
                        self.toastDialog.toastLabel('Mail Account Connect ERROR!',2000)

                    newData = ['{} has {} unread mails.'.format(alias,curUnrdNum),str(curUnrdNum),alias,self.unrdAccInfo[i][3]]
                    if(curUnrdNum > self.urndNum[i]):
                        self.listDialog.ptray.showMessage('Inlook inform you','your {} mailbox has {} unread mails.'.format(alias,curUnrdNum), QSystemTrayIcon.Information)
                    self.urndNum[i] = curUnrdNum
                    self.unrdModel.setData(index,newData)
            exchAccCount = len(self.exchAccInfo)
            if not self.exchAccCount ==0:
                alias = self.exchAccInfo[0][4]
                
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
                    newData = ['{}\n{}\n{}'.format(exchStr[i][0],exchStr[i][1],exchStr[i][2]),exchStr[i][3],alias,self.exchAccInfo[0][3]]
                    if exchStr[i][3]:
                        self.toastDialog.toastLabel('{}'.format(newData[0]),20000)
                        for j in range(5):
                            winsound.PlaySound('./sounds/Alarm.wav',flags=1)
                            self.listDialog.ptray.showMessage('Inlook inform you',newData[0], QSystemTrayIcon.Information)
                    self.exchModel.setData(index,newData)
                
                if(not self.agndListItem == itemNum):
                    threeLineHei = int(4.2*11*self.dpi/72)
                    singleLineHei = int(threeLineHei/3)
                    otherLineHei = 6*self.lineHei + self.spaceHei*10+18
                    self.agndListViewHeight=itemNum*(threeLineHei+2*self.viewSpacHei)-singleLineHei*2
                    self.ui_inlook.agndListView.setMaximumHeight(self.agndListViewHeight)
                    self.ui_inlook.agndListView.resize(self.ui_inlook.agndListView.width(),self.agndListViewHeight)

                    self.listDialog.resize(self.listDialog.width(), self.ui_inlook.unrdListView.height() + self.agndListViewHeight+ otherLineHei)
                    self.listDialog.selfFlush()

                self.agndListItem = itemNum

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
        # self.unrdAutoUpdateTimerStart()
        # self.unrdAutoUpdateTimer.stop()
        # mailAcc,self.exchAccount ,mailAcc[0]=[server,username,password,website]

        
        
        self.wt = WorkThread()
        #开始执行run()函数里的内容
        self.wt.start()
        # # 收到信号
        self.wt.sinOut.connect(self.pingBack)  #将信号连接至pingBack函数
