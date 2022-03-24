import os

if __name__ == '__main__':
	threads = [1,2,4,8]
	partitions = [1,2,4,6,8,10,12,14,16,18]
	for t in threads:
		for p in partitions:
			print("Startig on {} threads and {} partitions".format(t,p))
			os.system("perf stat -o ./logs/23Mar2022Log"+str(t)+"-"+str(p)+".txt -e cycles,instructions,L1-icache-load-misses,L1-dcache-load-misses,LLC-load-misses,cache-misses,stalled-cycles-frontend,stalled-cycles-backend,branch-misses,iTLB-load-misses,dTLB-load-misses ./data_process_v2 {} {}".format(t,p))
