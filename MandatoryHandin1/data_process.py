import csv

class Partitions:
    # method has to be Independent Output or Concurrent Output
    def __init__(self, numPartitions, threads, method):
        self.numPartitions = numPartitions
        if (method == "Independent Output")
        self.arrays = [[] for x in range(numPartitions)]
        with open('data_set.txt', newline='') as f:
            reader = csv.reader(f)
            self.data = list(reader)

    def findPartition(self, data):
        return hash(data[0])%self.numPartitions

P = Partitions(4)
print(P.data)