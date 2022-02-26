#input size == 2^24
#tuple(8byte key,8byte value)

import random
def chunks(lst, n):
	for i in range(0, len(lst), n):
		yield (lst[i:i + n])


def gen(start,finish,result,index):
	target = [(i,random.randint(1,finish)) for i in range(start,finish)]
	result[index] = target
	return target

def writeToFile(filename,mode,l):
	with open(filename+".txt",mode) as f:
		for item in l:
			f.write(str(item)+'\n')
