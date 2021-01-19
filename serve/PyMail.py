# -*- coding: utf-8 -*-
import imaplib
from serve.PyToast import *
import sys
class MailAccount():
  def __init__(self,host,username,password):
    self.host = host
    self.username = username
    self.password = password
    # 163 gmail requires uploading client ID information

  def update(self,login_check = False):
    unrdNums = 0
    retStr = 'OK'

    try:
      imaplib.Commands['ID'] = ('AUTH')
      self.authArgs = ("name","rmemailchecker","contact","charleechan@163.com","version","1.0.0","vendor","charleechan")
      self.con = imaplib.IMAP4_SSL(self.host)
      status = self.con.login(self.username, self.password)

      typ, dat = self.con._simple_command('ID', '("' + '" "'.join(self.authArgs) + '")')
      # returnStr = '{}'.format(status[0])
      self.con.select('INBOX', True)
      _, msgnums = self.con.search(None, '(UNSEEN)')
      unrdNums = len(msgnums[0].split())
      self.con.close()
      self.con.logout()
    except Exception as e:
      if isinstance(e.args[0], bytes):
        errStr = e.args[0].decode('utf-8')
      else:
        errStr = '{}'.format(e)

      print(errStr)

      if(type(e) == ConnectionRefusedError):
        retStr = 'SERVER'
      elif('password' in  errStr):
        retStr = 'PASSWORD'
      else:
        retStr = 'ACCOUNT'
      unrdNums = -1

    if not login_check:
      return unrdNums
    else:
      return retStr

