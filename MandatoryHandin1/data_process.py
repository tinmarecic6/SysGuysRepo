import csv

class Partitions:
    # method has to be Independent Output or Concurrent Output
    def __init__(self, numPartitions, threads, method):
        self.numPartitions = numPartitions
        with open('data_set.txt', newline='') as f:
                reader = csv.reader(f)
                self.data = list(reader)
        if (method == "Concurrent Output"):
            self.partitionsArray = [[] for x in range(numPartitions)]

    def findPartition(self, data):
        return hash(data[0])%self.numPartitions
    
    def printPartitions(self):
        print("Partitions: "+str(self.partitionsArray))

P = Partitions(10,2,"Concurrent Output")
P.printPartitions()