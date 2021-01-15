# -*- coding: utf-8 -*-
import win32gui,win32con,win32api

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui,QtCore
import sys,os
from gui.cppUI.inlook import *
from gui.cppUI.aboutdialog import *


def _MyCallback( hwnd, extra ):
    retVar = extra
    defView=win32gui.FindWindowEx(hwnd, None, "SHELLDLL_DefView", None)
    if(defView):
        sysListView32=win32gui.FindWindowEx(defView, None, "SysListView32", None)
        if(sysListView32):
            retVar.append(sysListView32)

class TanslucentDialog(QWidget):
    """
    无边框窗口类
    """
    langChanged = pyqtSignal([str])
    def __init__(self):
        super(TanslucentDialog, self).__init__(None, Qt.FramelessWindowHint) # 设置为顶级窗口，无边框
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self._padding = 5 # 设置边界宽度为5
        self.changeFlag = False
        
        self.aboutDiag = 0
        self.langFlag = 'EN'
        
       
        # self.initLayout() # 设置框架布局
        self.setMinimumWidth(250)

        self.initDrag() # 设置鼠标跟踪判断默认值
        self.trayIcon()
        self.initMouseTrans()
        self.setMouseTracking(True)


    def initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False

    def initDragWidget(self,movButton,changeButton,bottomEdge,rightEdge,cornerEdge):
        self._MoveButton = movButton
        self._MoveButton.setMouseTracking(True)
        self._MoveButton.setCursor(Qt.SizeAllCursor)

        self.a3Text1 = self.tr('Disable mouse transparent')
        self.a3Text2 = self.tr('Enable mouse transparent')
        self.changeButText1 = self.tr('Unlock the size and postion')
        self.changeButText2 = self.tr('Lock the size and postion')
        
        self.qssStyle1='''
            QLabel#changeButton{
                border-image: url(./img/unlock.png);
                border-radius: 14px;
            } 
            '''
        self.qssStyle2='''
            QLabel#changeButton{
                border-image: url(./img/locked.png);
                border-radius: 14px;
            } 

            '''
            #QLabel#changeButton:hover{
            #    border-image: url(./img/locked_hover.png);
            #}

        self._ChangeButton = changeButton
        self._ChangeButton.setMouseTracking(True)
        self._ChangeButton.setStyleSheet(self.qssStyle2)
        self._ChangeButton.setToolTip('Unlock')
        self._ChangeButton.setToolTip(self.changeButText1)
        pixmap = QPixmap('./img/key.png')
        cursor = QCursor(pixmap)
        self._ChangeButton.setCursor(cursor)

        self._BottomEdge = bottomEdge
        self._BottomEdge.setCursor(QtCore.Qt.SizeVerCursor)
        self._RightEdge = rightEdge
        self._RightEdge.setCursor(QtCore.Qt.SizeHorCursor)
        self._CornerEdge = cornerEdge
        self._CornerEdge.setCursor(QtCore.Qt.SizeFDiagCursor)
        # self.langSwitch()

            


    def setRoutineAndConfigFile(self,timerRoutine,fileMan):
        self.timerRoutine = timerRoutine
        self.fileMan = fileMan

    def setChangeSize(self,enable):
        if enable:
            self._MoveButton.setMouseTracking(True) # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
            self._BottomEdge.setMouseTracking(True)
            self._RightEdge.setMouseTracking(True)
            self._CornerEdge.setMouseTracking(True)
            self._ChangeButton.setMouseTracking(True)
        else:
            self._MoveButton.setMouseTracking(False) # 设置标题栏标签鼠标跟踪（如不设，则标题栏内在widget上层，无法实现跟踪）
            self._BottomEdge.setMouseTracking(False)
            self._RightEdge.setMouseTracking(False)
            self._CornerEdge.setMouseTracking(False)
            self._ChangeButton.setMouseTracking(False)

    def selfFlush(self):
        self._right_rect = [QPoint(x, y) for x in range(self._RightEdge.x(), self._RightEdge.x()+self._RightEdge.width())
                                    for y in range(self._RightEdge.y(),self._RightEdge.y()+self._RightEdge.height())]
        self._bottom_rect = [QPoint(x, y) for x in range(self._BottomEdge.x(), self._BottomEdge.x()+self._BottomEdge.width())
                                    for y in range(self._BottomEdge.y(),self._BottomEdge.y()+self._BottomEdge.height())]
        self._corner_rect = [QPoint(x, y) for x in range(self._CornerEdge.x(), self._CornerEdge.x()+self._CornerEdge.width())
                                    for y in range(self._CornerEdge.y(),self._CornerEdge.y()+self._CornerEdge.height())]
        self._move_rect = [QPoint(x,y) for x in range(self._MoveButton.x(), self._MoveButton.x()+self._MoveButton.width())
                                    for y in range(self._MoveButton.y(),self._MoveButton.y()+self._MoveButton.height())]
        self._change_rect = [QPoint(x,y) for x in range(self._ChangeButton.x(), self._ChangeButton.x()+self._ChangeButton.width())
                                    for y in range(self._ChangeButton.y(),self._ChangeButton.y()+self._ChangeButton.height())]

    def resizeEvent(self, QResizeEvent):
        # 重新调整边界范围以备实现鼠标拖放缩放窗口大小，采用三个列表生成式生成三个列表
        self.selfFlush()
    def mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._change_rect):
            self.changeFlag = False if self.changeFlag else True

            if self.changeFlag:
                self._ChangeButton.setStyleSheet(self.qssStyle1)
                self._ChangeButton.setToolTip(self.changeButText2)
                pixmap = QPixmap('./img/locked_hover.png')
                cursor = QCursor(pixmap)
                self._ChangeButton.setCursor(cursor)
            else:
                self._ChangeButton.setStyleSheet(self.qssStyle2)
                self._ChangeButton.setToolTip(self.changeButText1)
                pixmap = QPixmap('./img/key.png')
                cursor = QCursor(pixmap)
                self._ChangeButton.setCursor(cursor)
            event.accept()
        else:
            if(self.changeFlag):
                if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
                    # 鼠标左键点击右下角边界区域
                    self._corner_drag = True
                    event.accept()
                elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
                    # 鼠标左键点击右侧边界区域
                    self._right_drag = True
                    event.accept()
                elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
                    # 鼠标左键点击下侧边界区域
                    self._bottom_drag = True
                    event.accept()

                elif (event.button() == Qt.LeftButton) and (event.pos() in self._move_rect):
                    # 鼠标左键点击标题栏区域
                    self.timerRoutine.unrdAutoUpdateTimerStop()
                    self.timerRoutine.timer2.stop()
                    self._move_drag = True
                    self.move_DragPosition = event.globalPos() - self.pos()
                    event.accept()
            else:
                event.accept()

    def getChangeFlag(self):
        return self.changeFlag
    def mouseMoveEvent(self, QMouseEvent):
        # 当鼠标左键点击不放及满足点击区域的要求后，分别实现不同的窗口调整
        # 没有定义左方和上方相关的5个方向，主要是因为实现起来不难，但是效果很差，拖放的时候窗口闪烁，再研究研究是否有更好的实现
        if Qt.LeftButton and self._right_drag:
            # 右侧调整窗口宽度
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._bottom_drag:
            # 下侧调整窗口高度
            if(QMouseEvent.pos().y()>400): #限制400
                self.resize(self.width(), QMouseEvent.pos().y())
                QMouseEvent.accept()
        elif Qt.LeftButton and self._corner_drag:
            # 右下角同时调整高度和宽度
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
            QMouseEvent.accept()
        elif Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()
        QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False
        self._corner_drag = False
        self._bottom_drag = False
        self._right_drag = False
        self.timerRoutine.unrdAutoUpdateTimerStart()
        self.timerRoutine.timer2.start()
        self.fileMan.setConfigPos(self.x(),self.y(),self.width(),self.height())


    def embed(self):
        # 获取桌面句柄
        retVar = []
        win32gui.EnumWindows(_MyCallback, retVar)
        # print("HWND: {} ".format(retVar[0]))
        win32gui.SetParent(int(self.winId()),retVar[0])

    def trayIcon(self):
        #托盘
        self.ptray = QSystemTrayIcon(self) #创建托盘
        self.ptray.setIcon(QIcon('./img/tray100.png'))  #设置托盘图标
                 
        # 弹出的信息被点击就会调用messageClicked连接的函数
        #self.ptray.messageClicked.connect(self.message)
         
        #托盘图标被激活
        #self.ptray.activated.connect(self.iconActivated)
        #设置提示信息
        self.ptray.setToolTip(u'Inlook')
  
 
        #创建托盘的右键菜单
        self.tpMenu = QMenu()
        self.a1 = QAction(QIcon('./img/about.png'), self.tr('About'), self) #添加一级菜单动作选项(关于程序)
        self.a1.triggered.connect(self.about)
        self.a2 = QAction(QIcon('./img/exit.png'), self.tr('Exit'), self) #添加一级菜单动作选项(退出程序)
        self.a2.triggered.connect(self.quit)
        self.a3 = QAction(QIcon('./img/check.png'), self.tr('Enable Mouse Transparent'), self)
        self.a3.triggered.connect(self.mouseTrans)

        self.a4 = QAction(QIcon('./img/cn.png'), '切换到中文', self)
        self.a4.triggered.connect(self.langSwitch)


        self.tpMenu.addAction(self.a4)
        self.tpMenu.addAction(self.a3)
        self.tpMenu.addAction(self.a1)
        self.tpMenu.addAction(self.a2)
        self.ptray.setContextMenu(self.tpMenu) #把tpMenu设定为托盘的右键菜单
 
        self.ptray.show()  #显示托盘   
         
    def langSwitch(self):
        self.langFlag = 'CN' if self.langFlag == 'EN' else 'EN'
        if self.langFlag == 'CN':
            self.a4.setIcon(QIcon('./img/en.png'))
            self.a4.setText('Switch to Endlish')

        else:
            self.a4.setIcon(QIcon('./img/cn.png'))
            self.a4.setText('切换到中文')
        self.langChanged[str].emit(self.langFlag)
    def aboutWebsite(self):
        win32api.ShellExecute(0,'open','https://charleechan.github.io/Github_Gitbook_Cnblogs/inlook.html','','',1)
    
    def reTranslate(self):
        self.a1.setText(self.tr('About'))
        self.a2.setText(self.tr('Exit'))
        self.a3.setText(self.tr('Enable Mouse Transparent'))
        if self.aboutDiag == 0:
            self.createAboutDialog()
        self.ui_aboutDiag.descLabel.setText(self.tr('Inlook is developed by Charleechan, employing mainly exchangelib, imaplib.'))
        self.ui_aboutDiag.verLabel.setText(self.tr('Inlook v1.0.0.0'))
        self.aboutDiag.setWindowTitle(self.tr('Inlook 1.0'))
        self.a3Text1 = self.tr('Disable mouse transparent')
        self.a3Text2 = self.tr('Enable mouse transparent')
        self.changeButText1 = self.tr('Unlock the size and postion')
        self.changeButText2 = self.tr('Lock the size and postion')

    def aboutClose(self):
        self.aboutDiag.close()
    def createAboutDialog(self):
        self.aboutDiag = QDialog()
        self.ui_aboutDiag = Ui_AboutDialog()
        self.ui_aboutDiag.setupUi(self.aboutDiag)
        self.ui_aboutDiag.iconLabel.setStyleSheet('border-image: url(./img/tray100.png);')
        self.ui_aboutDiag.descLabel.setText(self.tr('Inlook is developed by Charleechan, employing mainly exchangelib, imaplib.'))
        self.ui_aboutDiag.verLabel.setText(self.tr('Inlook v1.0.0.0'))
        self.ui_aboutDiag.webButton.clicked.connect(self.aboutWebsite)
        self.ui_aboutDiag.closeButton.clicked.connect(self.aboutClose)
        self.aboutDiag.setWindowTitle(self.tr('Inlook 1.0'))
        self.aboutDiag.setWindowFlags(self.aboutDiag.windowFlags() | Qt.WindowStaysOnTopHint& (~Qt.WindowMinMaxButtonsHint))

    def about(self):
        if self.aboutDiag == 0:
            self.createAboutDialog()
        self.aboutDiag.setAttribute(Qt.WA_TranslucentBackground, True)
        with open("./qss/black.qss",'r') as f:
            style=f.read()
            self.aboutDiag.setStyleSheet(style)
        self.aboutDiag.show()
    
    def initMouseTrans(self):
        self.mouseFlag = False
        self.a3.setIcon(QIcon('./img/check.png'))
        self.a3.setText('Enable mouse transparent')
        # self.setAttribute(Qt.WA_TransparentForMouseEvents,False)
        win32gui.SetWindowLong(self.winId(),win32con.GWL_EXSTYLE,win32gui.GetWindowLong(self.winId(),win32con.GWL_EXSTYLE)&(~win32con.WS_EX_TRANSPARENT)&(~win32con.WS_EX_LAYERED));


    def mouseTrans(self):
        self.mouseFlag = False if self.mouseFlag else True
        if(self.mouseFlag):
            #设置鼠标穿透
            self.a3.setIcon(QIcon('./img/uncheck.png'))
            self.a3.setText(self.a3Text1)
            # self.setAttribute(Qt.WA_TransparentForMouseEvents,True)
            win32gui.SetWindowLong(self.winId(),win32con.GWL_EXSTYLE,win32gui.GetWindowLong(self.winId(),win32con.GWL_EXSTYLE)|win32con.WS_EX_TRANSPARENT|win32con.WS_EX_LAYERED);
        else:
            self.a3.setIcon(QIcon('./img/check.png'))
            self.a3.setText(self.a3Text2)
            # self.setAttribute(Qt.WA_TransparentForMouseEvents,False)
            win32gui.SetWindowLong(self.winId(),win32con.GWL_EXSTYLE,win32gui.GetWindowLong(self.winId(),win32con.GWL_EXSTYLE)&(~win32con.WS_EX_TRANSPARENT)&(~win32con.WS_EX_LAYERED));

    def quit(self):
        self.close()
        sys.exit()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    
    window = TanslucentDialog()

    with open("./qss/black.qss",'r') as f:
        style=f.read()
        window.setStyleSheet(style)
    ui = Ui_InLook()

    ui.setupUi(window)
    window.initDragWidget(ui.pinPostionLabel,ui.bottomEdge,ui.rightEdge,ui.cornerEdge)
    window.setChangeSize(True)

    window.show()
    sys.exit(app.exec_())