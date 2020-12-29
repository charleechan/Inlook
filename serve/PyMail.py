# -*- coding: utf-8 -*-

import imaplib
class MailAccount():
  def __init__(self,host,username,password):
    self.host = host
    self.username = username
    self.password = password

  def login(self):
    imaplib.Commands['ID'] = ('AUTH')
    self.con = imaplib.IMAP4_SSL(self.host)
    status = self.con.login(self.username, self.password)
    returnStr = '{}'.format(status[0])
    return returnStr

  def Update(self):
    # 163 gmail requires uploading client ID information
    args = ("name","rmemailchecker","contact","charleechan@163.com","version","1.0.0","vendor","charleechan")
    typ, dat = self.con._simple_command('ID', '("' + '" "'.join(args) + '")')
    # print(con._untagged_response(typ, dat, 'ID'))
    
    self.con.select('INBOX', True)
    _, msgnums = self.con.search(None, '(UNSEEN)')
    self.con.close()
    self.con.logout()
    return len(msgnums[0].split())

def main():

  mailbox1 = MailAccount('imap.163.com','xxxx@163.com','xxxxxxx')
  print(mailbox1.login())
  print(mailbox1.Update())
if __name__=="__main__":
  main()

 