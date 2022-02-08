#input size == 2^24
#tuple(8byte key,8byte value)

import random
size = pow(2,10)
l = [(i,random.randint(1,size)) for i in range(size)]
random.shuffle(l)
with open("data_set.txt","w") as f:
	for item in l:
		f.write(str(item[0])+","+str(item[1])+"\n")
