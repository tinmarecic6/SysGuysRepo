import csv, time, threading,sys,os
from datetime import datetime
import multiprocessing



class Partitions:
	# method has to be Independent Output or Concurrent Output
	log_header = f"method|timestamp|throughput|duration(ms)|noTuples|noPartitions|noThreads\n"
	"""
	Init method
	"""
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
		read_end_time = time.time()-read_start_time
		print(f"Reading the data took:{read_end_time} seconds")
		self.indexesSplit = round(len(self.data)/self.threads)
	"""
	Logging methods
	"""
	def log(self,starttime,duration,noTuples,method,partitions,threads):
		file = "log_"+starttime.strftime("%Y-%m-%d")+".csv"
		dttm = starttime.strftime("%Y-%m-%d %H:%M:%S")
		throughput = noTuples/duration
		with open(file,"a") as f:
			f.write(f"{method}|{dttm}|{throughput}|{duration}|{noTuples}|{partitions}|{threads}\n")

	"""
	Partition methods
	"""
	def findPartition(self, data):
		return hash(data[0])%self.numPartitions
	
	def concurrentPartition(self,start,finish):
		print(start,finish)
		for i in range(start,finish):
			self.partitionsArray[self.findPartition(self.data[i])].append(self.data[i])

	def independentPartition(self,start,finish):
		print(multiprocessing.current_process().name,start,finish)
		localPartitionsArray = [[] for x in range(self.numPartitions)]
		for i in range(start,finish):
			localPartitionsArray[self.findPartition(self.data[i])].append(self.data[i])
		""" total = 0
		for i in range(self.numPartitions):
			total += len(localPartitionsArray[i])
		self.total += total """
	
	def independentPartitionTest(self):
		print(multiprocessing.current_process().name)
		localPartitionsArray = [[] for x in range(self.numPartitions)]
		for i in range(len(self.data)):
			localPartitionsArray[self.findPartition(self.data[i])].append(self.data[i])


	"""
	Printing methods
	"""
	def printConcurrentPartitions(self):
		total = 0
		for i in range(self.numPartitions):
			total += len(self.partitionsArray[i])
		print(total)
		print(len(self.data))

	def printIndependentPartitions(self):
		print(self.total)
		print(len(self.data))

	
	"""
	Partition methods using Threads
	"""	
	def makeConcurrentPartition(self):
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

	"""
	Partitioning methods using Processes
	"""
	def makeConcurrentPartitionProc(self,pool):
		print("Starting concurrent partition with proceses")
		results = []							
		start = time.time_ns()
		for i in range(self.threads):
			start_ind = self.indexesSplit*i
			end_ind = self.indexesSplit*i+self.indexesSplit if self.indexesSplit*i+self.indexesSplit < len(self.data) else len(self.data)
			res = pool.apply_async(self.concurrentPartition,args=[start_ind,end_ind])
			results.append(res)
		for result in results:
			result.wait()
		print(f"Running time for concurrent process: {round((time.time_ns()-start)/1_000_000)} ms")

	
	def makeIndependentPartitionProc(self,pool):
		print("Starting independent partition with pool proceses")
		results = []							
		start = time.time_ns()
		for i in range(self.threads):
			start_ind = self.indexesSplit*i
			end_ind = self.indexesSplit*i+self.indexesSplit if self.indexesSplit*i+self.indexesSplit < len(self.data) else len(self.data)
			res = pool.map(self.independentPartition,(start_ind,end_ind))
			results.append(res)
		for result in results:
			result.wait()
		end_time = round((time.time_ns()-start)/1_000_000)
		print(f"Running time for independent pool process: {end_time} ms")
		#self.log(datetime.now(),end_time,len(self.data),"Independent",self.numPartitions,self.threads)

	def testProcess(self):
		processes = []
		print("Starting independent partition with just proceses")
		print(multiprocessing.current_process().name)
		results = []							
		start = time.time_ns()
		for i in range(self.threads):
			start_ind = self.indexesSplit*i
			end_ind = self.indexesSplit*i+self.indexesSplit if self.indexesSplit*i+self.indexesSplit < len(self.data) else len(self.data)
			p = multiprocessing.Process(target=self.independentPartition,args=[start_ind,end_ind])
			processes.append(p)
		for p in processes:
			p.start()
		for p in processes:
			p.join()
		""" for result in results:
			result.wait() """
		end_time = round((time.time_ns()-start)/1_000_000)
		print(f"Running time for independent process: {end_time} ms")


	def testProcess2(self):
		print("Starting independent partition with just proceses")
		print(multiprocessing.current_process().name)
		start = time.time_ns()
		with multiprocessing.Pool(self.threads) as pool:
			res = pool.map(self.independentPartitionTest)
		
		
		end_time = round((time.time_ns()-start)/1_000_000)
		print(f"Running time for independent process: {end_time} ms")

		

if __name__ == '__main__':
	multiprocessing.set_start_method("spawn")
	partitions = int(sys.argv[1])
	noThreads = int(sys.argv[2])
	print(f"Starting with {partitions} partitions and {noThreads} threads")
	P = Partitions(partitions,noThreads)
	pool = multiprocessing.Pool(processes=noThreads)
	filename = "log_"+datetime.now().strftime("%Y-%m-%d")+".csv"
	if not os.path.isfile(filename):
		with open(filename,"w") as f:
			f.write(P.log_header)
	"""P.makeIndependentPartition() """
	#P.testProcess2()
	#P.makeConcurrentPartition()
	P.makeConcurrentPartitionProc(pool)
	pool.close()
	pool.join()
