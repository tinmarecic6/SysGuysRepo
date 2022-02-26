import csv, time, threading,os
import multiprocessing
from multiprocessing import Pool

from numpy import partition


class Partitions:
	# method has to be Independent Output or Concurrent Output
	partitionsArray = []
	def __init__(self, numPartitions, threads):
		self.numPartitions = numPartitions
		self.threads = threads
		self.total = 0
		self.partitionsArray = [[] for x in range(self.numPartitions)]
		read_start_time = time.time()
		with open('data_set.txt', newline='') as f:
			reader = csv.reader(f)
			self.data = list(reader)
		for x in range(len(self.data)):
			row = [int(self.data[x][0].replace('(','')),int(self.data[x][1].replace(')',''))]
			self.data[x] = row
		print(f"Reading the data took:{time.time()-read_start_time} seconds")


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
		print(start,finish)
		for i in range(start,finish):
			self.partitionsArray[self.findPartition(self.data[i])].append(self.data[i])

	def independentPartition(self,start,finish):
		print(f"{multiprocessing.current_process().name} started on range {start} - {finish}")
		partitionsArray = [[] for x in range(self.numPartitions)]
		for i in range(start,finish):
			partitionsArray[self.findPartition(self.data[i])].append(self.data[i])
		total = 0
		for i in range(self.numPartitions):
			total += len(partitionsArray[i])
		self.total += total
	
	
	def independentPartitionProc(self,start,finish):
		p = Pool(self.threads)
		results = []
		for i in range(start,finish):
			r = p.apply_async(self.findAndAddPartition,args=[self.data[i]])
			results.append(r)
		for res in results:
			res.wait()
		p.close()
		p.join()
		total = 0
		for i in range(self.numPartitions):
			total += len(self.partitionsArray[i])
		self.total += total

	def findAndAddPartition(self,data):
		return self.partitionsArray[hash(data[0])%self.numPartitions].append(self.data)

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
		startTime = time.time_ns()
		for i in range(self.threads):
			if i+1 == self.threads:
				threadsArray.append(threading.Thread(target=self.independentPartition, args=(indexesSplit*(i),len(self.data))))
				print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),len(self.data)))
			else:
				threadsArray.append(threading.Thread(target=self.independentPartition, args=(indexesSplit*(i),indexesSplit*i+indexesSplit)))
				print("thread {} working on interval {} - {} ".format(threadsArray[i].name,indexesSplit*(i),indexesSplit*i+indexesSplit))
		for i in range(self.threads):
			threadsArray[i].start()
		for i in range(self.threads):
			threadsArray[i].join()
		runningTime = time.time_ns()-startTime
		print("Running time for independent: ",runningTime // 1_000_000,"ms")

	def makeIndependentPartitionProc(self):
		print("len",len(self.data))
		indexesSplit = round(len(self.data)/self.threads)
		results = []
		start = time.time_ns()
		
		
		"""
		This one takes cca 70s
		"""
		p = multiprocessing.Pool(processes=self.threads)								
		for i in range(self.threads):
			start_ind = indexesSplit*i
			end_ind = indexesSplit*i+indexesSplit if indexesSplit*i+indexesSplit < len(self.data) else len(self.data)
			res = p.apply_async(self.independentPartition,args=[start_ind,end_ind])
			results.append(res)
		for r in results:
			r.wait()

		p.close()
		p.join()
		print(f"Process version took {round((time.time_ns()-start)/1_000_000)} ms")



if __name__ == '__main__':
	P = Partitions(10,8)
	"""	P.makeConcurrentPartition()
	P.printConcurrentPartitions()
	P.makeIndependentPartition()"""
	#P.makeConcurrentPartition()
	P.makeIndependentPartitionProc()
	
