import csv, time, threading

class Partitions:
    # method has to be Independent Output or Concurrent Output
    def __init__(self, numPartitions, threads):
        self.numPartitions = numPartitions
        self.threads = threads
        self.total = 0
        with open('data_set.txt', newline='') as f:
                reader = csv.reader(f)
                self.data = list(reader)
    

    def findPartition(self, data):
        return hash(data[0])%self.numPartitions
    
    def printConcurrentPartitions(self):
        total = 0
        for i in range(self.numPartitions):
            total += len(self.partitionsArray[i])
        print(total)
        print(len(self.data))

    def printIndependentPartitions(self):
        print(self.total)
        print(len(self.data))

    def concurrentPartition(self,start,finish):
        for i in range(start,finish):
            self.partitionsArray[self.findPartition(self.data[i])].append(self.data[i])

    def independentPartition(self,start,finish):
        partitionsArray = [[] for x in range(self.numPartitions)]
        for i in range(start,finish):
            partitionsArray[self.findPartition(self.data[i])].append(self.data[i])
        total = 0
        for i in range(self.numPartitions):
            total += len(partitionsArray[i])
        self.total += total

    def makeConcurrentPartition(self):
        self.partitionsArray = [[] for x in range(self.numPartitions)]
        print("len",len(self.data))
        indexesSplit = round(len(self.data)/self.threads)
        threadsArray = []
        for i in range(self.threads):
            if i+1 == self.threads:
                threadsArray.append(threading.Thread(target=self.concurrentPartition, args=(indexesSplit*(i),len(self.data))))
                print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),len(self.data)))
            else:
                threadsArray.append(threading.Thread(target=self.concurrentPartition, args=(indexesSplit*(i),indexesSplit*i+indexesSplit)))
                print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),indexesSplit*i+indexesSplit))
        startTime = time.time_ns()
        for i in range(self.threads):
            threadsArray[i].start()
        for i in range(self.threads):
            threadsArray[i].join()
        runningTime = time.time_ns()-startTime
        print("Running time for concurrent: ",runningTime // 1_000_000,"ms")

    def makeIndependentPartition(self):
        print("len",len(self.data))
        indexesSplit = round(len(self.data)/self.threads)
        threadsArray = []
        for i in range(self.threads):
            if i+1 == self.threads:
                threadsArray.append(threading.Thread(target=self.independentPartition, args=(indexesSplit*(i),len(self.data))))
                print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),len(self.data)))
            else:
                threadsArray.append(threading.Thread(target=self.independentPartition, args=(indexesSplit*(i),indexesSplit*i+indexesSplit)))
                print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),indexesSplit*i+indexesSplit))
        startTime = time.time_ns()
        for i in range(self.threads):
            threadsArray[i].start()
        for i in range(self.threads):
            threadsArray[i].join()
        runningTime = time.time_ns()-startTime
        print("Running time for independent: ",runningTime // 1_000_000,"ms")

P = Partitions(10,20)
P.makeConcurrentPartition()
P.printConcurrentPartitions()
P.makeIndependentPartition()
P.printIndependentPartitions()