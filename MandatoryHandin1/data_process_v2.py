from datetime import datetime
import multiprocessing,time,random,sys
import os

# https://stackoverflow.com/a/55775916
import ctypes

CLOCK_REALTIME = 0

class timespec(ctypes.Structure):
        _fields_ = [
                        ('tv_sec', ctypes.c_int64), # seconds, https://stackoverflow.com/q/471248/1672565
                                ('tv_nsec', ctypes.c_int64), # nanoseconds
                                        ]

        clock_gettime = ctypes.cdll.LoadLibrary('libc.so.6').clock_gettime
        clock_gettime.argtypes = [ctypes.c_int64, ctypes.POINTER(timespec)]
        clock_gettime.restype = ctypes.c_int64    

        def time_ns():
                tmp = timespec()
                    ret = clock_gettime(CLOCK_REALTIME, ctypes.pointer(tmp))
                        if bool(ret):
                                    raise OSError()
                                    return tmp.tv_sec * 10 ** 9 + tmp.tv_nsec




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

if __name__ == '__main__':
	numPartitions = int(sys.argv[1])
	threads = int(sys.argv[2])
	print(f"Starting run with {numPartitions} partitions and {threads} threads")
	P = Partitions(numPartitions,threads)
	filename = "log_"+datetime.now().strftime("%Y-%m-%d")+".csv"
	if not os.path.isfile(filename):
		with open(filename,"w") as f:
			f.write(P.log_header)
	#start = time.time_ns()
        start = time_ns()

	with multiprocessing.Pool(threads) as pool:
		data = pool.map(P.gen,[x for x in range(0,pow(2,24))])
	print(f"Generated in {(time.time_ns()-start)// 1_000_000} s")
	with multiprocessing.Pool(threads) as pool:
		#start = time.time_ns()
		start = time_ns()
                independent_result = pool.map(P.independentPartition,[data])
		#end_time = (time.time_ns()-start)//1_000_000
                end_time = (time_ns()-start)//1_000_000
		print(f"Partitioned independently in {end_time} ms")
		P.log(datetime.now(),end_time,len(data),"Independent",numPartitions,threads)
		#start = time.time_ns()
		start = time_ns()
                concurrent_result = pool.map(P.concurrentPartition,[data])
		#end_time = (time.time_ns()-start)//1_000_000
		end_time = (time_ns()-start)//1_000_000
                print(f"Partitioned concurrently in {end_time} ms")
		P.log(datetime.now(),end_time,len(data),"Concurrent",numPartitions,threads)
