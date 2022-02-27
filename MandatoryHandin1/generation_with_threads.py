import time,random, data_gen

import threading

def concat(results):
	l = []
	for list in results:
		l+=list
	random.shuffle(l)
	return l

if __name__=='__main__':
	max = pow(2,24)
	noThreads = 4
	indexes_start = [None]*noThreads
	indexes_end = [None]*noThreads
	indexesSplit = round(max/noThreads)
	threads = [None] * noThreads
	results = [None] * noThreads
	for i in range(noThreads):
		start_ind = indexesSplit*i
		end_ind = indexesSplit*i+indexesSplit if indexesSplit*i+indexesSplit < max else max
		indexes_start[i] = start_ind
		indexes_end[i] = end_ind
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

