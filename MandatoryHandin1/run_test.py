import os

if __name__ == '__main__':
	threads = [1,2,4,8,16,32]
	partitions = [1,2,4,6,8,10,12,14,16]
	for t in threads:
		for p in partitions:
			print("Startig on {} partitions and {} threads".format(p,t))
			os.system(f"python data_process_v2.py {t} {p}")