# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(480, 342)
        self.gridLayout = QtWidgets.QGridLayout(AboutDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.mainWidget = QtWidgets.QWidget(AboutDialog)
        self.mainWidget.setObjectName("mainWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.mainWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setObjectName("mainLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mainLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.descLabel = QtWidgets.QLabel(self.mainWidget)
        self.descLabel.setText("")
        self.descLabel.setObjectName("descLabel")
        self.mainLayout.addWidget(self.descLabel, 4, 0, 1, 7)
        self.iconLabel = QtWidgets.QLabel(self.mainWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(100, 100))
        self.iconLabel.setMaximumSize(QtCore.QSize(100, 100))
        self.iconLabel.setText("")
        self.iconLabel.setObjectName("iconLabel")
        self.mainLayout.addWidget(self.iconLabel, 0, 2, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mainLayout.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem2, 1, 2, 1, 3)
        self.verLabel = QtWidgets.QLabel(self.mainWidget)
        self.verLabel.setText("")
        self.verLabel.setObjectName("verLabel")
        self.mainLayout.addWidget(self.verLabel, 2, 0, 1, 7)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem3, 3, 2, 1, 3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mainLayout.addItem(spacerItem4, 0, 6, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.mainLayout.addItem(spacerItem5, 0, 5, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem6, 5, 2, 1, 3)
        self.closeButton = QtWidgets.QPushButton(self.mainWidget)
        self.closeButton.setObjectName("closeButton")
        self.mainLayout.addWidget(self.closeButton, 6, 4, 1, 2)
        self.webButton = QtWidgets.QPushButton(self.mainWidget)
        self.webButton.setObjectName("webButton")
        self.mainLayout.addWidget(self.webButton, 6, 1, 1, 2)
        self.gridLayout_3.addLayout(self.mainLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.mainWidget, 0, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "Inlook 1.0"))
        self.closeButton.setText(_translate("AboutDialog", "close"))
        self.webButton.setText(_translate("AboutDialog", "Website"))
