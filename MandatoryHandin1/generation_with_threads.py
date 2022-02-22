import time,random, data_gen

import threading

def concat(results):
	l = []
	for list in results:
		l+=list
	random.shuffle(l)
	return l

if __name__=='__main__':
	indexes_start = [0, 16, 20, 23]
	#indexes_start = [0]
	indexes_end = [15, 19, 22, 24]
	#indexes_end = [15]
	noThreads = len(indexes_start)
	threads = [None] * noThreads
	results = [None] * noThreads
	start_time = time.time()
	for i in range(len(threads)):
		threads[i] = threading.Thread(target=data_gen.gen, args=(indexes_start[i],indexes_end[i],results,i))
		threads[i].start()
		print("thread {} working on interval {} - {} ".format(threads[i].name,indexes_start[i],indexes_end[i]))

	for i in range(noThreads):
		print(i)
		threads[i].join()
	
	end_time = time.time() - start_time
	print("Execution lasted for {} seconds\nWriting to file now...".format(end_time))
	data_gen.writeToFile("data_set","w",concat(results))
	print("Finished writing to file.")

