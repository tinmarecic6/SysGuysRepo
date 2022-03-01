from datetime import datetime
import multiprocessing,time,random,sys
import os

class Partitions:
	log_header = f"method|timestamp|throughput|duration(ms)|noTuples|noPartitions|noThreads\n"
	def __init__(self,numPartitions,threads):
		self.numPartitions = numPartitions
		self.threads = threads
		self.partitionsArray = [[] for x in range(self.numPartitions)]
	"""
	Generation method
	"""
	def gen(self,i):
		return (i,random.randint(0,pow(2,24)))
	"""
	Helper methods
	"""
	def findPartition(self,data):
		return hash(data[0])%self.numPartitions
	"""
	Partitioning methods
	"""
	def independentPartition(self,data):
		print(multiprocessing.current_process().name)
		localPartitionsArray = [[] for x in range(self.numPartitions)]
		for i in range(len(data)):
			localPartitionsArray[self.findPartition(data[i])].append(data[i])
		
		return localPartitionsArray
	
	def concurrentPartition(self,data):
		for i in range(len(data)):
			self.partitionsArray[self.findPartition(data[i])].append(data[i])
		return self.partitionsArray
	"""
	Logging methods
	"""
	def log(self,starttime,duration,noTuples,method,partitions,threads):
		file = "log_"+starttime.strftime("%Y-%m-%d")+".csv"
		dttm = starttime.strftime("%Y-%m-%d %H:%M:%S")
		throughput = noTuples/duration
		with open(file,"a") as f:
			f.write(f"{method}|{dttm}|{throughput}|{duration}|{noTuples}|{partitions}|{threads}\n")

def chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]

if __name__ == '__main__':
	temp = 2
	threads = int(sys.argv[1])
	P = Partitions(temp,threads)
	filename = "log_"+datetime.now().strftime("%Y-%m-%d")+".csv"
	if not os.path.isfile(filename):
		with open(filename,"w") as f:
			f.write(P.log_header)
	start = time.time()
	
	with multiprocessing.Pool(threads) as pool:
		data = pool.map(P.gen,[x for x in range(0,pow(2,24))])
	print(f"Generated in {(time.time()-start)} s")
	for numPartitions in [2,4,6,8,10,12,14,16,18]:
		print(f"Starting run with {numPartitions} partitions and {threads} threads")
		P = Partitions(numPartitions,threads)
		with multiprocessing.Pool(threads) as pool:
			chunksToWork = list(chunks(data,threads))
			start = time.time()
			independent_result = pool.map(P.independentPartition,chunksToWork)
			end_time = (time.time()-start)
			print(f"Partitioned independently in {end_time} ms")
			P.log(datetime.now(),end_time,len(data),"Independent",numPartitions,threads)
			start = time.time()
			concurrent_result = pool.map(P.concurrentPartition,chunksToWork)
			end_time = (time.time()-start)
			print(f"Partitioned concurrently in {end_time} ms")
			P.log(datetime.now(),end_time,len(data),"Concurrent",numPartitions,threads)
