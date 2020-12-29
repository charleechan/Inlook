# -*- coding: utf-8 -*-
from serve.PyMail import *
from serve.PyFileMan import *
from serve.PyExchange import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from exchangelib import EWSDateTime,EWSTimeZone,EWSDate

class PySlots(object):
    """
    所有槽函数
    """
    def __init__(self,ui_inlook,ui_loginpage,ui_addAgenda,timerRoutine,fileMan,listDialog,loginDialog,addAgendaDialog):
        self.ui_inlook = ui_inlook
        self.ui_loginpage = ui_loginpage
        self.ui_addAgenda = ui_addAgenda
        self.timerRoutine = timerRoutine
        self.fileMan = fileMan
        self.listDialog = listDialog
        self.loginDialog = loginDialog
        self.addAgendaDialog = addAgendaDialog
    def lgnPgSubmit(self):
        """
        
        """
        accTypeInput = self.ui_loginpage.lgnPgAccSelect.currentIndex()
        print('accTypeInput',accTypeInput)
        usernameInput = self.ui_loginpage.lgnPgUsernameInput.text()
        serverInput = self.ui_loginpage.lgnPgServerInput.text()
        passwordInput = self.ui_loginpage.lgnPgPasswordInput.text()
        website = self.ui_loginpage.lgnPgWebsiteInput.text()
        alias = self.ui_loginpage.lgnPgCName.text()

        if( not accTypeInput):
            mailAccount = MailAccount(serverInput,usernameInput,passwordInput)
            if(mailAccount.login()=='OK'):
                self.fileMan.UpdateConfigFile('mail',serverInput,usernameInput,passwordInput,website,alias)
                # self.ui.stackWgt.setCurrentIndex(1)
                self.timerRoutine.toastLabel('Email Account Login Success.',3000)
                self.loginDialog.close()
                self.listDialog.show()

                self.timerRoutine.unrdAutoUpdateTimerStart()
                self.timerRoutine.timer2.start()

            else:
                self.timerRoutine.toastLabel('Email Account Login Failed, Please check your info.',3000)
        else:
            exchAccount = ExchAccount(serverInput,usernameInput,passwordInput)
            if(exchAccount.login()=='OK'):
                self.fileMan.UpdateConfigFile('exchange',serverInput,usernameInput,passwordInput,website,alias)
                # self.ui.stackWgt.setCurrentIndex(1)
                self.timerRoutine.toastLabel('Exchange Account Login Success.',3000)
                self.loginDialog.close()
                self.listDialog.show()
                self.timerRoutine.unrdAutoUpdateTimerStart()
                self.timerRoutine.timer2.start()
            else:
                self.timerRoutine.toastLabel('Exchange Login Failed, Please check your info.',3000)
                
    def lgnPgCancel(self):
        """
        
        """
        acc = self.fileMan.initConfigFile()
        self.ui_loginpage.lgnPgUsernameInput.setText('')
        self.ui_loginpage.lgnPgServerInput.setText('')
        self.ui_loginpage.lgnPgPasswordInput.setText('')
        if(not acc[0]):
            self.listDialog.close()
            self.loginDialog.show()
            self.timerRoutine.toastLabel('Clear success.',2000)
        else:

            self.loginDialog.close()
            self.listDialog.show()
            self.timerRoutine.toastLabel('Cancel success.',2000)
    
    def addMailAcc(self):
        """

        """
        self.timerRoutine.unrdAutoUpdateTimerStop()
        self.timerRoutine.timer2.stop()
        self.listDialog.close()
        self.loginDialog.show()
    def agndFromDateInputChanged(self,dateTime):
        self.ui_addAgenda.agndToDateInput.setDateTime(dateTime)

    def agndFromTimeInputChanged(self,dateTime):
        self.ui_addAgenda.agndToTimeInput.setDateTime(dateTime)

    def agndAlarmEnableChanged(self):
        self.ui_addAgenda.agndAlarmInput.setEnabled(self.ui_addAgenda.agndAlarmEnableCheck.isChecked())
    def addAgenda(self):

        self.listDialog.close()
        self.ui_addAgenda.agndFromTimeInput.setDateTime(QDateTime.currentDateTime())
        self.ui_addAgenda.agndToTimeInput.setDateTime(QDateTime.currentDateTime())
        self.ui_addAgenda.agndFromDateInput.setDateTime(QDateTime.currentDateTime())
        self.ui_addAgenda.agndToDateInput.setDateTime(QDateTime.currentDateTime().addSecs(1800))
        self.ui_addAgenda.agndAlarmEnableCheck.setChecked(False)
        self.ui_addAgenda.agndAlarmInput.setEnabled(False)
         
        
        self.ui_addAgenda.agndFromDateInput.dateTimeChanged.connect(self.agndFromDateInputChanged)
        self.ui_addAgenda.agndFromTimeInput.dateTimeChanged.connect(self.agndFromTimeInputChanged)
        self.ui_addAgenda.agndAlarmEnableCheck.stateChanged.connect(self.agndAlarmEnableChanged)

        self.ui_addAgenda.agndFromDateInput.setCalendarPopup(True)
        self.ui_addAgenda.agndToDateInput.setCalendarPopup(True)

        self.addAgendaDialog.show()
        self.timerRoutine.unrdAutoUpdateTimerStop()
        self.timerRoutine.timer2.stop()
    
    def addAgendaSubmit(self):

        fromDate = self.ui_addAgenda.agndFromDateInput.date()
        fromTime = self.ui_addAgenda.agndFromTimeInput.time()
        toDate  = self.ui_addAgenda.agndToDateInput.date()
        toTime = self.ui_addAgenda.agndToTimeInput.time()

        fromDatetime = QDateTime(fromDate,fromTime, timeSpec = Qt.LocalTime)
        toDatetime = QDateTime(toDate,toTime, timeSpec = Qt.LocalTime)

        localTimeZone = EWSTimeZone.localzone()
        fromEWSDatetime = EWSDateTime.from_datetime(fromDatetime.toPyDateTime())
        toEWSDatetime = EWSDateTime.from_datetime(toDatetime.toPyDateTime())

        fromDT=fromEWSDatetime.astimezone(tz=localTimeZone)
        toDT = toEWSDatetime.astimezone(tz=localTimeZone)        

        location = self.ui_addAgenda.agndPosInput.text()
        subject = self.ui_addAgenda.agndSubjectInput.text()
        detail = self.ui_addAgenda.agndDetailInput.toPlainText()
        reminderEnable = self.ui_addAgenda.agndAlarmEnableCheck.isChecked()
        reminder = self.ui_addAgenda.agndAlarmInput.value()
        self.timerRoutine.exchAccount.login()
        self.timerRoutine.exchAccount.addAgenda(fromDT,toDT,location,subject,detail,reminderEnable,reminder)

        self.addAgendaDialog.close()
        self.listDialog.show()
        self.timerRoutine.unrdAutoUpdateTimerStart()
        self.timerRoutine.timer2.start()

    def addAgendaCancel(self):

        self.addAgendaDialog.close()
        self.listDialog.show()
        self.timerRoutine.unrdAutoUpdateTimerStart()
        self.timerRoutine.timer2.start()