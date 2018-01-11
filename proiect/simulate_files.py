from binary_search_attack import *
import random
from shutil import copy

def simulate_files(path, no_files, K):
	if not os.path.exists(path):
		os.makedirs(path)

	all_keywords = []
	while len(all_keywords) != len(K):
		for i in range(no_files):
			no_keywords = random.randint(1, T)
			keywords = []
			f = open(path + 'file' + str(i), 'w+')
			for j in range(no_keywords):
				r = random.choice(K)
				while r in keywords:
					r = random.choice(K)
				keywords = keywords + [r]
				f.write(r + '\n')
			all_keywords = list(set(all_keywords).union(set(keywords)))

def leaked_files(path, percentage, K):
	files = [f for f in os.listdir(server_path) if os.path.isfile(server_path + f)]
	no_leaked = int(percentage * len(files))

	if not os.path.exists(path):
		os.makedirs(path)

	leaked_files = []
	for i in range(no_leaked):
		r = random.choice(files)
		while r in leaked_files:
			r = random.choice(files)
		leaked_files = leaked_files + [r]
		copy(server_path + r, path)


simulate_files('files/simulated_files/', 50, K)
leaked_files('files/leaked_files/', 0.2, K)