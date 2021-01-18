# -*- coding: utf-8 -*-
import imaplib
from serve.PyToast import *
class MailAccount():
  def __init__(self,host,username,password):
    self.host = host
    self.username = username
    self.password = password
    # 163 gmail requires uploading client ID information
    imaplib.Commands['ID'] = ('AUTH')
    self.authArgs = ("name","rmemailchecker","contact","charleechan@163.com","version","1.0.0","vendor","charleechan")

    try:
      self.con = imaplib.IMAP4_SSL(self.host)
    except Exception as e:
      print('ERROR:{}'.format(e))

  def login(self):
    try:
      status = self.con.login(self.username, self.password)
      typ, dat = self.con._simple_command('ID', '("' + '" "'.join(self.authArgs) + '")')
      returnStr = '{}'.format(status[0])
    except Exception as e:
      print('ERROR:{}'.format(e))
      returnStr = 'ERROR:{}'.format(e)
    
    return returnStr

  def Update(self):

    # print(con._untagged_response(typ, dat, 'ID'))
    unrdNums = 0
    try:
      self.con.select('INBOX', True)
      _, msgnums = self.con.search(None, '(UNSEEN)')
      unrdNums = len(msgnums[0].split())
    except Exception as e:
      print('ERROR:{}'.format(e))
    return unrdNums

  def logout(self):
    self.con.close()
    self.con.logout()

def main():

  mailbox1 = MailAccount('imap.163.com','xxxx@163.com','xxxxxxx')
  print(mailbox1.login())
  print(mailbox1.Update())
if __name__=="__main__":
  main()

 