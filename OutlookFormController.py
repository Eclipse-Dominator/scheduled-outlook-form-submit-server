from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from interfaces import informTelegram

class OutlookFormController:
    # Controller to handle simple outlook forms for organisations

    # takes chrome service driver location as input.
    def __init__(self,webdriverUrl:str,session_user:str=""):
        self.session_user = session_user
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options,executable_path=webdriverUrl)

        self.implicitWaitTime = 5
        self.wait = WebDriverWait(self.driver,15)
        self.driver.implicitly_wait(self.implicitWaitTime) 
    
    def endController(self,err=False,id=None): # if err == True, driver will take a screenshot before existing and send to the user with the telegram id
        if err:
            if id:
                informTelegram(self.session_user,self.driver.get_screenshot_as_png(),id)    
            informTelegram(self.session_user,self.driver.get_screenshot_as_png())
        else:
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        self.driver.quit()
    
    def loadForm(self, website:str):
        self.driver.get(website)

    def checkError(self,byError,timer = 1): # check for presence of any error message 
        try:
            self.driver.implicitly_wait(timer) 
            self.driver.find_element(*byError)
            self.driver.implicitly_wait(self.implicitWaitTime) 
            return True
        except:
            self.driver.implicitly_wait(self.implicitWaitTime) 
            return False
        
    
    def login(self,email:str,password:str):
        email_login = self.wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@type='email']")))
        email_login.send_keys(email)
        email_login.send_keys(Keys.RETURN)
        if self.checkError((By.ID,"usernameError")):
            print(self.driver.find_element_by_id("usernameError").text)
            return False
        
        
        password_login = self.wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@type='password']")))
        password_login.send_keys(password)
        password_login.send_keys(Keys.RETURN)
        if self.checkError((By.ID,"passwordError")):
            print(self.driver.find_element_by_id("passwordError").text)
            return False
        
        return True
        

    def fillTextQuestion(self, questionId:str, text:str):
        answerBox = self.driver.find_element_by_xpath("//div[@aria-labelledby='{}']//input".format(questionId))
        answerBox.send_keys(text)

    def fillChoiceQuestion(self, questionId:str, choice:str):
        answerBox = self.driver.find_element_by_xpath("//div[@aria-labelledby='{}']//span[text()='{}']".format(questionId,choice))
        answerBox.click()

    def getEmail(self):
        #office-form-email-receipt-checkbox-description
        checkBox = self.driver.find_element_by_xpath("//span[@class='office-form-email-receipt-checkbox-description']")
        checkBox.click()
        
    def submitForm(self):
        submitBtn = self.driver.find_element_by_xpath("//button[@title='Submit']")
        submitBtn.click()

        if self.checkError((By.CLASS_NAME,"thank-you-page-confirm"),2):
            print("Form Submitted")
            return True
        print("Form failed to submit")
        return False

    def nextForm(self):
        submitBtn = self.driver.find_element_by_xpath(By.XPATH,"//button[@title='Next']")
        submitBtn.click()
    


