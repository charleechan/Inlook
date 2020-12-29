# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys,re
import win32api


class ExchListModel(QAbstractListModel):
    """
    custom list model class : inherits QAbstractListModel
    """
    def __init__(self,parent=None):
        '''
        Call the parent class __init__ and modify the _data.
        '''
        super(ExchListModel,self).__init__(parent)
        self._data=[]
        self.alarm=[]
        self.alias=[]
        self.websiteList = []

    def rowCount(self, parent=QModelIndex()):
        """
        return number of items.
        """
        return len(self._data)

    def data(self,index,role=Qt.DisplayRole):
        """
        @override data() function of QAbstractListModel
        return the data item of index when role is Qt.DisplayRole or Qt.EditRole
        """
        if not index.isValid() or not 0 <= index.row() < self.rowCount():
            return QVariant()
        # index :<->: row :<->: data
        row=index.row()
        # return the data of row
        if role==Qt.DisplayRole:
            return self._data[row]
        # return the data of row when role is Qt.EditRole
        if role==Qt.EditRole:
            return self._data[row]
        if role==Qt.BackgroundColorRole:
            # if self.alarm[index.row()]%2 ==0: 
            if index.row()%2 ==0:
               return QColor(0,255,0,50)
            else:
                return QColor(0,0,255,50)
        # return QVariant (0)
        return QVariant()

    def flags(self, index):
        """
        @override flags() function of QAbstractListModel
        get the flags which describe the status of data item
        """

        # Fetch the the status of data item from QAbstractListModel.flags()
        flag=super(ExchListModel,self).flags(index)

        # Add the ItemIsEditable flag
        # return flag | Qt.ItemIsEditable
        return flag

    def setData(self,index,value,role=Qt.EditRole):
        """
        @override setData() function of QAbstractListModel
        set the value of index only when role=Qt.EditRole, return the operation result
        """
        
        # set data only when the data item is Qt.EditRole
        if role == Qt.EditRole:
            # update the _data
            
            self._data[index.row()]=value[0]
            self.alarm[index.row()]=value[1]
            self.alias[index.row()]=value[2]
            self.websiteList[index.row()]=value[3]
            # emit the dataChanged signal to update the view.
            self.dataChanged.emit(index,index)
            # return the operation result
            return True
        else:
            return False
    
    def insertRows(self,row,count,parent=QModelIndex()):
        self.beginInsertRows(parent,0,count-1)
        for i in range(count):
            self.websiteList.append('')
            self.alias.append('')
            self.alarm.append(False)
            self._data.append('')
        self.endInsertRows()
    def removeRows(self,row,count,parent=QModelIndex()):
        self.beginRemoveRows(parent,0,count-1)
        self.websiteList = []
        self.alarm = []
        self.alias = []
        self._data = []
        self.endRemoveRows()

class ExchDelegate(QStyledItemDelegate):
    """
    custom Delegate class: inherits QStyledItemDelegate class
    control the view style
    """
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)


    def createEditor(self,parent,option,index):
        button = QPushButton(parent)
        button.setToolTip('Click to open the exchange')
        return button
    def setEditorData(self,editor,index):
        """
        设置编辑器数据
        """

        item_var=index.data(Qt.DisplayRole)
        #设置编辑器的数据为当前索引的值
        editor.setValue(item_int)
        editor.setValue(item_var)
    def setModelData(self,editor,model,index):
        """
        给model设置编辑后的数据
        """

        #获取编辑器的数据
        data_int=editor.value()
        #把数据封装为Qt类型
        data_var=QVariant(data_int)

        #设置Model的数据，当前索引与数据
        model.setData(index, data_var)

    def editorEvent(self,event,model,option,index):
        if (event.type() == QEvent.MouseButtonRelease):
            website = model.websiteList[index.row()]
            if(not re.split(":.",website)[0]=='ms-settings'):
                website = 'https://' + website
            win32api.ShellExecute(0,'open',website,'','',1)
            # webbrowser.open(model.websiteList[index.row()]) # 使用IE打开
            return True
        return True #返回True表示事件已处理


def main():
    print("Void Model")



if __name__ == "__main__":
    main()