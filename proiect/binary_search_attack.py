import os
import math
import numpy as np
from copy import copy

server_path = 'files/simulated_files/'
leaked_path = 'files/leaked_files/'

n_keys = 1024

T = 64

bits = int(math.log(n_keys, 2))
K = [i for i in range(n_keys)]
K = list(map(lambda x: np.binary_repr(x, width = bits), K))

token_dict = {}
for i in range(len(K)):
	token_dict[i] = K[i]

def server(path, *token):
	files = [f for f in os.listdir(path) if os.path.isfile(path + f)]

	file_names = []
	for f in files:
		fo = open(path + f, "r")
		content = fo.read()
		fo.close()
		if all([token_dict[t] in content for t in token]):
			file_names.append(f)

	return file_names

def inject_files(path, K):
	l = int(math.log(len(K), 2))
	mask = [i for i in range(len(K))]
	mask = list(map(lambda x: np.binary_repr(x, width = l), mask))

	for i in range(l):
		f = open(path + "F" + str(i), "w")
		for j in range(len(mask)):
			if mask[j][i] == '1':
				f.write(K[j] + '\n')

def recover(path, K, *token):
	all_files = [f for f in os.listdir(path) if os.path.isfile(path + f)]

	files = server(path, *token)

	if len(files) == 0:
		return K[0]

	contents = {}

	for f in all_files:
		fo = open(path + f, "r")
		content = fo.read()
		content_list = content.split('\n')[:-1]
		contents[f] = content_list
		fo.close()

	result = list(set(contents[files[0]]))
	for f in all_files:
		if f in files:
			result = list(set(result).intersection(set(contents[f])))
		else:
			result = list(set(result).difference(set(contents[f])))

	return result

'''
inject_files('files/', K)
print (recover('files/', K, 4))
'''