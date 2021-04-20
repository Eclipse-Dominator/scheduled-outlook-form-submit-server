# Min heap
import heapq

class PriorityQueue:
    '''
    minimum queue to store tasks
    tasks are stored as their time to do task and their unique identifier (email)
    ( timestamp:int, email:str, options )
    '''
    def __init__(self,queue:list):
        self.queue = queue
        heapq.heapify(self.queue)

    def addTask(self, newTask:tuple):
        if next( (task for task in self.queue if task[1] == newTask[1]), False ):
            # Ensure uniqueness of new Task
            return False
        heapq.heappush(self.queue, newTask)

    def updateCompletedTask(self,newTask):
        if newTask[1] != self.queue[0][1]:
            print("new task unmatch")
            return False
        heapq.heapreplace(self.queue,newTask)

    def removeCompletedTask(self):
        return heapq.heappop(self.queue) if len(self.queue) else False

    def removeTaskFromUser(self,email):
        for index,item in enumerate(self.queue):
            if item[1] == email:
                return self.removeTask(index)
        
    def removeTask(self,index):
        if index == 0:
            return self.removeCompletedTask()
        parentIndex = (index-1)//2
        self.queue[index], self.queue[parentIndex] = self.queue[parentIndex],self.queue[index]
        return self.removeTask(parentIndex)

    @property
    def nextTask(self)->tuple:
        if len(self.queue):
            return self.queue[0]
        else:
            return None