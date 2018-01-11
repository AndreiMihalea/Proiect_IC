import os
import math
import numpy as np
from binary_search_attack import *

w = int(len(K) / T)

partitions = [K[x:x + T] for x in range(0, len(K), T)]

def inject_files_hierarchical(path, K):
	for i in range(w):
		f = open(path + 'fmic' + str(i), "w")
		for k in partitions[i]:
			f.write(k + '\n')

	for i in range(int(w / 2)):
		if not os.path.exists(path + 'FF' + str(i)):
			os.makedirs(path + 'FF' + str(i))

		p1 = partitions[2 * i]
		p2 = partitions[2 * i + 1]

		u = p1 + p2

		inject_files(path + 'FF' + str(i) + '/', u)

def recover_hierarchical(path, K, *token):
	all_files = [f for f in os.listdir(path) if os.path.isfile(path + f) and 'fmic' in f]

	file_no = 0

	for f in all_files:
		if server(path, *token)[0] == f:
			file_no = int(f[4:])
			break

	partition_no = int (file_no / 2)

	p1 = partitions[2 * partition_no]
	p2 = partitions[2 * partition_no + 1]

	u = p1 + p2

	return recover(path + 'FF' + str(partition_no) + '/', u, *token)

#inject_files_hierarchical('files/', K)
#print(recover_hierarchical('files/', K, 7))