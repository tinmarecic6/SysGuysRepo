import csv, time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class Partitions:
    # method has to be Independent Output or Concurrent Output
    def __init__(self, numPartitions, threads, method):
        self.numPartitions = numPartitions
        with open('data_set.txt', newline='') as f:
                reader = csv.reader(f)
                self.data = list(reader)
        if (method == "Concurrent Output"):
            self.partitionsArray = [[] for x in range(numPartitions)]
            startTime = time.time_ns()
            with ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(self.Partition, self.data)
            runningTime = time.time_ns()-startTime
            print("Running time: ",runningTime // 1_000_000,"ms")
                    

    def findPartition(self, data):
        return hash(data[0])%self.numPartitions
    
    def printPartitions(self):
        print("Partitions: "+str(self.partitionsArray))

    def Partition(self, data):
        self.partitionsArray[self.findPartition(data)].append(data)

P = Partitions(10,20,"Concurrent Output")