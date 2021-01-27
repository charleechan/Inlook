# -*- coding: utf-8 -*-
from configobj import ConfigObj

class PyFileMan(object):
    '''
    '''

    def initConfigFile(self):
        '''
        return bool1,bool2 : bool1-False: No mailAccount, bool2-False: No exchangeAccount
        '''
        self.config = ConfigObj("./data/config.ini",encoding='UTF8')
        keys = self.config.keys()

        if 'Position' in keys:
            pass
        else:
            self.config['Position'] = {}
            self.config['Position']['x'] = '900'
            self.config['Position']['y'] = '400'
            self.config['Position']['width'] = '360'
            self.config['Position']['height'] = '400'
            self.config['Token'] = ''
            
        returnValue = []
        items = ['mail','exchange']

        for item in items:
            if item in keys:
                if self.config[item]['number'] == '0':
                    returnValue.append(False) 
                else:
                    returnValue.append(True)
            else:
                self.config[item] = {}
                self.config[item]['number'] = '0'
                returnValue.append(False) 

        self.config.write()
        return returnValue
    def UpdateConfigFile(self,item,item_server,item_user,item_pswd,item_website,item_alias):
        num = int(self.config[item]['number'])
        self.config[item]['number']= num + 1
        self.config[item]['server{}'.format(num)] = item_server
        self.config[item]['username{}'.format(num)] = item_user
        self.config[item]['password{}'.format(num)] = item_pswd
        self.config[item]['website{}'.format(num)] = item_website
        self.config[item]['alias{}'.format(num)] = item_alias
        self.config.write()
    def readConfigFile(self):
        '''
        return unrdAccount,exchAccount
        unrdAccount[0]=[server,username,password,website]
        '''
        self.config = ConfigObj("./data/config.ini",encoding='UTF8')

        exchAccount = []
        unrdAccount = []
        
        num = int(self.config['mail']['number'])
        for i in range(num):
            unrdAccount.append([])
            unrdAccount[i].append(self.config['mail']['server{}'.format(i)])
            unrdAccount[i].append(self.config['mail']['username{}'.format(i)])
            unrdAccount[i].append(self.config['mail']['password{}'.format(i)])
            unrdAccount[i].append(self.config['mail']['website{}'.format(i)])
            unrdAccount[i].append(self.config['mail']['alias{}'.format(i)])

        num1 = int(self.config['exchange']['number'])
        for i in range(num1):
            exchAccount.append([])
            exchAccount[i].append(self.config['exchange']['server{}'.format(i)])
            exchAccount[i].append(self.config['exchange']['username{}'.format(i)])
            exchAccount[i].append(self.config['exchange']['password{}'.format(i)])
            exchAccount[i].append(self.config['exchange']['website{}'.format(i)])
            exchAccount[i].append(self.config['exchange']['alias{}'.format(i)])

        return unrdAccount,exchAccount
    def getConfigPos(self):
        self.config = ConfigObj("./data/config.ini",encoding='UTF8')
        x = int(self.config['Position']['x'])
        y = int(self.config['Position']['y'])
        width = int(self.config['Position']['width'])
        height = int(self.config['Position']['height'])
        return x,y,width,height

    def getConfigQueto(self):
        self.config = ConfigObj("./data/config.ini",encoding='UTF8')
        keys = self.config.keys()

        if 'Token' in keys:
            return self.config['Token']
            print("Found token!")
        else:
            print("No token")
            return '-1'
    def setConfigQueto(self,token):
        self.config = ConfigObj("./data/config.ini",encoding='UTF8')
        self.config['Token'] = token
        self.config.write()

    def setConfigPos(self,x,y,width,height):
        self.config = ConfigObj("./data/config.ini",encoding='UTF8')
        self.config['Position']['x'] = x
        self.config['Position']['y'] = y
        self.config['Position']['width'] = width
        self.config['Position']['height'] = height
        self.config.write()