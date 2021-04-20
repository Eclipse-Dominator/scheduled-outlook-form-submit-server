from OutlookFormController import OutlookFormController as FormCtrl
from interfaces import FormParameters,Choices,GlobalVariables,informTelegram,DebugSettings
import pickle
from random import uniform
from datetime import timedelta,datetime,time,date

class OutlookDB:
    def __init__(self,pickledData = None):
        if pickledData:
            self.users = [OutlookUser(userInfo) for userInfo in pickle.loads(pickledData)]
        else:
            self.users = []
        for user in self.users:
            print(user.userInfo)

    def dumpData(self,file):
        return pickle.dump([user.userInfo for user in self.users],file)

    def getAllTasks(self):
        return [user.getNextTaskTime() for user in self.users]
    
    def basicInfo(self,user): # hides password and other items 
        info = user.userInfo
        return info[:1]+info[4:]

    def getListofUsers(self): #  return the list of users with their important information hidden
        return [self.basicInfo(user) for user in self.users]

    def getUser(self,email:str): # get OutlookUser object from their email
        return next( (user for user in self.users if user.email == email), False)

    def removeUser(self,email): # removes user with specified email
        self.users = [user for user in self.users if user.email != email]

    def addUser(self, email:str,password:str,time1:str,time2:str,param1:str,param2:str,param3:str,telegramID = None): # create new outlook user and return the object
        if self.getUser(email): # reject if user already exist
            return False
        user_infos = [email,password,[time1,time2],param1,param2,param3,telegramID] 
        self.users.append(OutlookUser(user_infos)) # add the user
        return self.users[-1]


class OutlookUser:
    def __init__(self,args:list):
        self.userInfo = args

    @property
    def userInfo(self):
        return [self.email,self.password,self.datetime,self.param1,self.param2,self.param3,self.telegramID]

    @userInfo.setter
    def userInfo(self,details:list):
        '''
        index -> arg
        0 -> email
        1 -> password
        2 -> datetime to do task
        3 -> param1
        4 -> param2
        5 -> param3
        6 -> telegramID
        '''
        self.email = details[0]
        self.password = details[1]
        self.datetime = details[2]
        self.setAmPmTimeDelta() # time maniplation
        self.param1 = details[3]
        self.param2 = details[4]
        self.param3 = details[5]
        self.telegramID = details[6]

    def setAmPmTimeDelta(self):
        
        time1= time.fromisoformat(self.amPmTime[0])
        time2 = time.fromisoformat(self.amPmTime[1])

        self.time1Delta = datetime.combine(date.min,time1) - datetime.min
        self.time2Delta = datetime.combine(date.min,time2) - datetime.min
        

    def submitForm(self,Choice):
        formCtrl = FormCtrl(GlobalVariables.WEBDRIVER,self.email)
        formCtrl.loadForm(GlobalVariables.WEBSITE)
        try:
            
            if not formCtrl.login(self.email,self.password):    # if log in is required for form
                raise(ValueError("Invalid email or password"))
            
            ''' Fill form depending on the questions
            formCtrl.fillTextQuestion(FormParameters.Q1,self.param1)
            formCtrl.fillTextQuestion(FormParameters.Q2,self.param2)
            formCtrl.fillChoiceQuestion(FormParameters.Q3,param3)
            formCtrl.fillTextQuestion(FormParameters.Q4,param4)
            '''
            if not formCtrl.submitForm():
                raise(ValueError("Invalid/missing form information"))
        except:
            formCtrl.endController(err=True,id=self.telegramID)
            raise(ValueError("unable to submit form"))
        formCtrl.endController(err=DebugSettings.VERBOSE)

    def doTask(self,task):
        try:
            self.submitForm(task[-1])
            if self.telegramID:
                informTelegram(f"Unable to submit form for {self.email} at {task[0].ctime()}",telegramID=self.telegramID)
            print(f"Form submitted for {self.email} at {task[0].ctime()}")
        except:
            if self.telegramID:
                informTelegram(f"Unable to submit form for {self.email} at {task[0].ctime()}",telegramID=self.telegramID)
            informTelegram(f"Unable to submit form for {self.email} at {task[0].ctime()}")
            print(f"Unable to submit form for {self.email} at {task[0].ctime()}")
            return False
        return self.getNextTaskTime(task)
        

    def getNextTaskTime(self,prevTask=None)->tuple:
        # takes a prev task and return the time to do the next subsequent task
        # TASK STRUCTURE (timeToDo, options,email)
        oneDay = timedelta(days=1)

        if prevTask:
            prevTaskDay = datetime.combine(prevTask[0].date(), time.min)
            if prevTask[2] is Choices.Choice1:
                return (prevTaskDay + self.time2Delta,self.email , Choices.Choice2)
            else:
                return (prevTaskDay + self.time1Delta + oneDay,self.email, Choices.Choice1)

        today = datetime.combine(date.today(), time.min)
        if datetime.now() <= today + self.amDelta:
            return (today+self.time1Delta,self.email, Choices.Choice1)
        elif datetime.now() <= today + self.time2Delta:
            return (today+self.time2Delta,self.email, Choices.Choice2)
        else:
            return (today+oneDay+self.time1Delta,self.email, Choices.Choice1)
