import threading
import time

class ThreadList:

    def __init__(self, threadNumber, processNumber, mode, callback):  # threadNumber kadar thread olusturur, listeye ekler
        self.THREAD_NUM = threadNumber
        self.PROCESS_NUM = processNumber
        self.MODE = mode
        self.threads = []
        self.minThread = None  # icinde sahip oldugu queue'da eleman sayısı en az olan thread
        self.order = 0  # sirayle ekleme modu icin var. siradaki emrin kacinci threade eklenecegini belirtir

        for i in range(self.THREAD_NUM):
            self.newThread = Thread(i, callback)
            self.threads.append(self.newThread)
        self.minThread = self.newThread

    def findMinThread(self):
        min = self.threads[0]
        for i in self.threads:
            print(i.id, "-", len(i.queue))
            if (len(i.queue)) < len(min.queue):
                min = i
        return min

    def addToMin(self, *args):
        self.minThread = self.findMinThread()
        self.minThread.addItemQueue(*args)

    def addInOrder(self, *args):
        if self.order > self.THREAD_NUM:
            self.order = 0
        self.threads[self.order].addItemQueue(*args)
        self.order = self.order + 1

    def add(self, *args):
        if self.MODE == 'order':
            self.addInOrder(*args)
        elif self.MODE == 'min':
            self.addToMin(*args)
        else:
            print("Error.")

class Thread:
    def __init__(self, ID, callback):
        self.id = ID
        self.callback = callback
        self.minThreadNum = None
        self.queue = []
        x = threading.Thread(target=self.run, args=(), daemon=True)
        x.start()

    def run(self):
        while True:
            try:
                time.sleep(0.1)
                if len(self.queue) > 0:
                    self.callback(*self.queue[0])
                    self.removeFirstItemQueue(self.queue)
            except:
                pass
    def addItemQueue(self, *args):
        self.queue.append([*args])

    def removeFirstItemQueue(self, queue):
        queue.pop(0)