import threading
from Queue import PriorityQueue as PQ
from flask import Flask,request
from OutlookUser import OutlookDB
from waitress import serve
from interfaces import DebugSettings
import time

PICKLEFILE = 'data.pickle'
with open(PICKLEFILE,'rb') as f:
    db = OutlookDB(f.read())
    
POSTKEYS = ['email','password','time1','time2','FORM_PARAMETER1','FORM_PARAMETER2','FORM_PARAMETER3','telegram_id'] # insert values for what to retrieve

print("Adding Task for Users...")

pq = PQ(db.getAllTasks()) #priority queue
countdownTimer = None
currentTask = None

def updateQueue():
    global currentTask
    global countdownTimer
    nextTask = pq.nextTask
    if nextTask and nextTask != currentTask:
        currentTask = nextTask
        if countdownTimer != None:
            countdownTimer.cancel()
        countdownTimer = threading.Timer(timeToDoTask(currentTask),doTask(currentTask))
        countdownTimer.start()
    
    print(pq.queue)

def timeToDoTask(task):
    # takes in task return time in seconds before task is initiated
    # task: (datetime, email, options)
    return task[0].timestamp() - time.time()

def doTask(task):
    # task: (datetime, email, options)
    def loadedTask():
        user = db.getUser(task[1])
        if user:
            nextTask = user.doTask(task)
            if nextTask:
                pq.updateCompletedTask(nextTask)
                updateQueue()
                return
        pq.removeCompletedTask()
        updateQueue()
    return loadedTask
    
updateQueue()

app = Flask("Outlook Forms Server")
    
@app.route('/clients', methods=['GET', 'POST','DELETE'])
def clients():
    if request.method == 'DELETE':
        email = request.args.get('email')
        if email:
            db.removeUser(email)
            with open(PICKLEFILE,'wb') as f:
                db.dumpData(f)
            pq.removeTaskFromUser(email)
        return "ok"
    
    elif request.method == 'POST':
        form_data = []
        for key in POSTKEYS:
            content = request.form.get(key)
            print(key,content)
            if content != "" or key==POSTKEYS[-1]:
                form_data.append(content)
            else:
                return "Missing information"
        user = db.addUser(*form_data)
        if user:
            pq.addTask(user.getNextTaskTime())
            updateQueue()
            with open(PICKLEFILE,'wb') as f:
                db.dumpData(f)
            return "ok"
        return "Invalid information"

    else:
        user = db.getUser(request.args.get("email"))
        if user:
            return ", ".join(db.basicInfo(user))
        return getClients()

@app.route('/settings/<name>', methods=['GET'])
def settings(name):
    if name == "verbose":
         DebugSettings.VERBOSE = not DebugSettings.VERBOSE
         return f"verbose is now {DebugSettings.VERBOSE}"   
    

def getClients():
    data = db.getListofUsers()
    convertedStr = ""
    for index,infoList in enumerate(data):
        convertedStr += f'<p>{index}. {", ".join(infoList)}</p>'
    return convertedStr
    
if __name__=="__main__":
    serve(app,host='0.0.0.0',port=5123)
    #serve(app,host='0.0.0.0',port=5123)