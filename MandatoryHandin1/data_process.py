import csv, time, threading

class Partitions:
    # method has to be Independent Output or Concurrent Output
    def __init__(self, numPartitions, threads, method):
        self.numPartitions = numPartitions
        with open('data_set.txt', newline='') as f:
                reader = csv.reader(f)
                self.data = list(reader)
        if (method == "Concurrent Output"):
            self.partitionsArray = [[] for x in range(numPartitions)]
            print("len",len(self.data))
            indexesSplit = round(len(self.data)/threads)
            threadsArray = []
            for i in range(threads):
                if i+1 == threads:
                    threadsArray.append(threading.Thread(target=self.concurrentPartition, args=(indexesSplit*(i),len(self.data))))
                    print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),len(self.data)))
                else:
                    threadsArray.append(threading.Thread(target=self.concurrentPartition, args=(indexesSplit*(i),indexesSplit*i+indexesSplit)))
                    print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),indexesSplit*i+indexesSplit))
            startTime = time.time_ns()
            for i in range(threads):
                threadsArray[i].start()
            for i in range(threads):
                threadsArray[i].join()
            runningTime = time.time_ns()-startTime
            print("Running time: ",runningTime // 1_000_000,"ms")

    

    def findPartition(self, data):
        return hash(data[0])%self.numPartitions
    
    def printPartitions(self):
        total = 0
        for i in range(self.numPartitions):
            total += len(self.partitionsArray[i])
        print(total)
        print(len(self.data))

    def concurrentPartition(self,start,finish):
        for i in range(start,finish):
            self.partitionsArray[self.findPartition(self.data[i])].append(self.data[i])

P = Partitions(10,20,"Concurrent Output")
P.printPartitions()