# -*- coding: utf-8 -*-

from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import glob

from gui.cppUI.inlook import *
from gui.cppUI.loginpage import *
from gui.cppUI.addagenda import *
from gui.cppUI.toast import *
from gui.TranslucentDialog.TranslucentDialog import *

from serve.PyMail import *
from serve.PyExchange import *
from serve.PyFileMan import *
from serve.PyTimerRoutine import *
from serve.PySlots import *
from serve.ExchListModel import *
from serve.UnrdListModel import *


def connectSignalSlot(ui_inlook,ui_loginpage,ui_addAgenda,mSlots):
    ui_loginpage.lgnPgSubmitButton.clicked.connect(mSlots.lgnPgSubmit)
    ui_loginpage.lgnPgCancelButton.clicked.connect(mSlots.lgnPgCancel)
    ui_inlook.addMailAccButton.clicked.connect(mSlots.addMailAcc)
    ui_inlook.addAgndButton.clicked.connect(mSlots.addAgenda)
    ui_addAgenda.agndSubmitButton.clicked.connect(mSlots.addAgendaSubmit)
    ui_addAgenda.agndCancelButton.clicked.connect(mSlots.addAgendaCancel)




def main():
    """
    :main function, the entry of entire app
    :return: None
    """
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)

    primaryScreen = QApplication.primaryScreen()
    # screens = QApplication.screens()
    # for screen in screens:
    #     if not screen is primaryScreen:
    #         auxiliaryScreen = screen
    #         break
    #     else:
    #         auxiliaryScreen = None
    scrHei = primaryScreen.geometry().height()
    lineHei = int(scrHei/40)
    spaceHei = int(scrHei/180)
    viewSpacHei = int(scrHei/540)
    # print(auxiliaryScreen.geometry())

    dpi = int(primaryScreen.logicalDotsPerInch())
    # print(dpi)


    # 设置全局字体
    #font = glob.glob('./gui/DroidSansChinese.ttf')
    # fonts = glob.glob(‘poppins/Poppins*.otf’) # 获取所有字体
    # QtGui.QFontDatabase.addApplicationFont(fonts[0]) #
    QtGui.QFontDatabase.addApplicationFont('./gui/DroidSansChinese.ttf')
    font = QtGui.QFont('PingFang SC Regular',11) #Microsoft YaHei
    app.setFont(font)

    # Create a QDialog object
    listDialog = TanslucentDialog()
    listDialog.setWindowTitle('Inlook')
    loginDialog = QDialog()
    loginDialog.setWindowTitle('Login your Account...')
    loginDialog.setWindowFlags(loginDialog.windowFlags() | Qt.WindowMinimizeButtonHint |Qt.WindowStaysOnTopHint)
    addAgendaDialog = QDialog()
    addAgendaDialog.setWindowFlags(addAgendaDialog.windowFlags() | Qt.WindowMinimizeButtonHint | Qt.WindowStaysOnTopHint)
    addAgendaDialog.setWindowTitle('Add Agenda...')
    # Create a UI object
    ui_inlook = Ui_InLook(lineHei,spaceHei)
    ui_loginpage = Ui_LoginPage()
    ui_addAgenda = Ui_AddAgenda()

    

    ui_inlook.setupUi(listDialog)
    qssStyle='''
        QLabel#changeButton{
            border-image: url(./img/locked.png);
            border-radius: 14px;
        } 
        QLabel#changeButton:hover{
            border-image: url(./img/locked_hover.png);
        }
        '''
    listDialog.initDragWidget(ui_inlook.moveButton,ui_inlook.changeButton,ui_inlook.bottomEdge,ui_inlook.rightEdge,ui_inlook.cornerEdge)
    ui_inlook.changeButton.setStyleSheet(qssStyle)
    listDialog.setChangeSize(True)
    

    ui_loginpage.setupUi(loginDialog)
    ui_addAgenda.setupUi(addAgendaDialog)

    

    ui_inlook.unrdListView.setSpacing(viewSpacHei)
    ui_inlook.agndListView.setSpacing(viewSpacHei)
    # ui.statusLabel.setAlignment(Qt.AlignCenter)
    # curDir=os.path.dirname(os.path.abspath(__file__))
    

    fileMan = PyFileMan()
    unrdModel=UnrdListModel()
    exchModel = ExchListModel()
    timerRoutine = PyTimerRoutine(unrdModel,exchModel,listDialog,ui_inlook,lineHei,spaceHei,viewSpacHei,dpi)
    listDialog.setRoutineAndConfigFile(timerRoutine,fileMan)


    # create a custom Delagate obj
    unrdDelegate=UnrdDelegate()
    exchDelegate=ExchDelegate()

    ui_inlook.unrdListView.setModel(unrdModel)
    ui_inlook.unrdListView.setItemDelegate(unrdDelegate)
    ui_inlook.unrdListView.show()

    ui_inlook.agndListView.setModel(exchModel)
    ui_inlook.agndListView.setItemDelegate(exchDelegate)
    ui_inlook.agndListView.show()

    mSlots = PySlots(ui_inlook,ui_loginpage,ui_addAgenda, timerRoutine,fileMan,listDialog,loginDialog,addAgendaDialog)
    connectSignalSlot(ui_inlook,ui_loginpage,ui_addAgenda,mSlots)

    with open("./qss/black.qss",'r') as f:
        style=f.read()
        listDialog.setStyleSheet(style)
    listDialog.embed()
    
    ret = fileMan.initConfigFile()
    pos = fileMan.getConfigPos()
    posX = pos[0]
    posY = pos[1]
    width = pos[2]
    height = pos[3]
    listDialog.resize(width,height)
    listDialog.move(posX,posY)

    if ret[0] or ret[1]:
        # ui.stackWgt.setCurrentIndex(1)
        listDialog.show()
        listDialog.selfFlush()
        timerRoutine.accBatchLogin()
        
    else:
        loginDialog.show()
        ui_loginpage.lgnPgCancelButton.setText('Reset')

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()