import os

if __name__ == '__main__':
	threads = 2 
	maxThreads = 32
	for t in range(2,maxThreads):
		for p in range(2,maxThreads):
			os.system(f"python data_process_v2.py {p} {t}")