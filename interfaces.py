from enum import Enum
import requests

class Choices(Enum):
    Choice1 = "Choice 1 sample text"
    Choice2 = "Choice 2 sample text" #words from the choice questions

class FormParameters(): # id of the questions on outlook
    Q1 = "QuestionId_r1 Outlook question id"
    Q2 = "QuestionId_r2 Outlook question id"
    Q3 = "QuestionId_r3 Outlook question id"
    Q4 = "QuestionId_r4 Outlook question id"

class DebugSettings():
    VERBOSE = False


class GlobalVariables():
    ADMINID = -1# insert telegram ID
    APIKEY = "TELEGRAM BOT KEY"
    WEBDRIVER = "./bin/chromedriver.exe"
    WEBSITE = "https://forms.office.com/Pages/ResponsePage.aspx?id=XXX" # Outlook form
    
def informTelegram(message,photo=None,telegramID=GlobalVariables.ADMINID): # inform admin/ user via telegram
    if photo:
        API = f"https://api.telegram.org/bot{GlobalVariables.APIKEY}/sendPhoto"
        requests.post(API,data={
            'chat_id':telegramID,
            'caption': message,
        },files={
            'photo': photo
        })
    else:
        API = f"https://api.telegram.org/bot{GlobalVariables.APIKEY}/sendMessage"
        requests.post(API,data={
            'chat_id':telegramID,
            'text': message
        })
