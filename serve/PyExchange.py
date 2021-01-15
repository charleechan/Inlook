from exchangelib import DELEGATE, Account, Configuration, Credentials
from datetime import datetime, timedelta
from exchangelib import EWSTimeZone, EWSDateTime, EWSDate, CalendarItem
from exchangelib.items import MeetingRequest, MeetingCancellation, SEND_TO_ALL_AND_SAVE_COPY, SAVE_ONLY
import re





class ExchAccount():
    def __init__(self,host,username,password):
        self.host = host
        self.username = username
        self.password = password
        self.credentials = Credentials(username=self.username, password=self.password)
        self.config = Configuration(server=self.host, credentials=self.credentials)

    def login(self):

        returnStr = 'Ok'
        try:
            self.account = Account(primary_smtp_address=self.username, config=self.config,autodiscover=False, access_type=DELEGATE)
        except Exception as e:
            returnStr = 'ERROR:{}'.format(e)
        return returnStr

    def Update(self):
        localTimeZone = EWSTimeZone.localzone()
        nowDateTime = EWSDateTime.now(tz=localTimeZone)
        # print(EWSDateTime.now(tz=localTimeZone))
        items = self.account.calendar.view(
            start=nowDateTime - timedelta(days=1),
            end=nowDateTime + timedelta(days=6),
        )

        retStr = []

        unseenStr = []
        unseenMails = self.account.inbox.filter(is_read=False)
        unseenStr.append(('{}'.format(unseenMails.count())))
        retStr.append(unseenStr)

        for item in items:
            itemStr = []
            startTime = item.start.astimezone(tz=localTimeZone)
            endTime = item.end.astimezone(tz=localTimeZone)
            dataOffset = startTime - nowDateTime
            dateOffNum = dataOffset.days+ dataOffset.seconds/(24.0*60.0*60.0)
            dateOffStr = ('%3.2f' % (dateOffNum))+'天后' if(dateOffNum>0) else ('%3.2f' % (abs(dateOffNum)))+'天前'
            if startTime.date()== nowDateTime.date():
                dateOffStr=('今天')

            when = '{},{}-{}'.format(dateOffStr,startTime.strftime('%m/%d %H:%M'),endTime.strftime('%H:%M'))

            subject = (re.sub('(?s)([^<]*)(<.*>)(.*)', '\\1\\3', '{}'.format(item.subject))).replace('None','')
            detail = (re.sub('(?s)([^<]*)(<.*>)(.*)', '\\1\\3', ':{}'.format(item.body))).replace(':None','')

            reminderTime = startTime - timedelta(minutes=item.reminder_minutes_before_start)
            if(nowDateTime.strftime("%m/%d %H:%M") == reminderTime.strftime("%m/%d %H:%M")):
                remindNow = True
            else:
                remindNow = False

            reminder = ('{} min'.format(item.reminder_minutes_before_start if item.reminder_is_set else 'No remind'))
            location = ('@{}#{}'.format(item.location,reminder)).replace('None','')

            itemStr.append(when)
            itemStr.append('{}{}'.format(subject,detail))
            itemStr.append(location)
            itemStr.append(remindNow)
            retStr.append(itemStr)
        
        return retStr
    def addAgenda(self,fromDatetime,toDatetime,location,subject,detail,reminderSet,reminder):
        item = CalendarItem(
            account=self.account,
            folder=self.account.calendar,
            start=fromDatetime,
            end=toDatetime,
            subject=subject,
            body=detail,
            location=location,
            reminder_is_set=reminderSet,
            reminder_minutes_before_start=reminder
            # required_attendees=['anne@example.com', 'bob@example.com']
        )
        # item.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)
        item.save()
def main():

    exchAcc = ExchAccount('eas.outlook.com','******@outlook.com','********')
    exchAcc.login()
    localTimeZone = EWSTimeZone.localzone()
    nowDateTime = EWSDateTime.now(tz=localTimeZone)
    # print(EWSDateTime.now(tz=localTimeZone))
    items = exchAcc.account.calendar.view(start=nowDateTime - timedelta(days=1),end=nowDateTime + timedelta(days=6))

    for item in items:
        startTime = item.start.astimezone(tz=localTimeZone)
        endTime = item.end.astimezone(tz=localTimeZone)
        print(item.reminder_minutes_before_start)


if __name__=="__main__":
  main()
