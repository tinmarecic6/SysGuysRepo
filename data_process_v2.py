import csv, time
import threading

class Partitions:
    # method has to be Independent Output or Concurrent Output
    def __init__(self, numPartitions, method):
        self.threads = [None] * numPartitions
        self.chunks = [None] * numPartitions
        self.numPartitions = numPartitions
        with open('data_set.txt', newline='') as f:
                reader = csv.reader(f)
                self.data = list(reader)
        
        if (method == "Concurrent Output"):
            self.partitionsArray = [[] for x in range(numPartitions)]
            startTime = time.time_ns()
            """ with ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(self.Partition, self.data) """
            for i in range(len(numPartitions)):
                self.threads[i] = threading.Thread(target = self.Partition, args=())
            runningTime = time.time_ns()-startTime
            print("Running time: ",runningTime // 1_000_000,"ms")
                    

    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    def findPartition(self, data):
        return hash(data[0])%self.numPartitions
    
    def printPartitions(self):
        print("Partitions: "+str(self.partitionsArray))

    def Partition(self, data):
        self.partitionsArray[self.findPartition(data)].append(data)

P = Partitions(8,16,"Concurrent Output")
P.printPartitions()