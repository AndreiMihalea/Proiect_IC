from binary_search_attack import *
import random

files = [f for f in os.listdir('files')]
for f in files:
	if f != 'leaked_files' and f != 'simulated_files':
		if os.path.isfile('files/' + f):
			os.remove('files/' + f)
		else:
			shutil.rmtree('files/' + f)

def inject_files_single(path, token, K):
	all_files = [f for f in os.listdir(path + 'simulated_files/') if os.path.isfile(path + 'simulated_files/' + f)]
	token_freq = len(server(server_path, token)) / len(all_files)

	all_keyword_freq = {}

	for k in K:
		all_keyword_freq[k] = 0

	leaked_files = [f for f in os.listdir(path + 'leaked_files/') if os.path.isfile(path + 'leaked_files/' + f)]

	for k in K:
		for l in leaked_files:
			f = open(path + 'leaked_files/' + l)
			content = f.read()
			if k in content:
				if k in all_keyword_freq:
					all_keyword_freq[k] += 1

	for k in all_keyword_freq:
		all_keyword_freq[k] = all_keyword_freq[k] / len(leaked_files)

	sorted_freq = sorted(all_keyword_freq.items(), key=lambda x: abs(x[1] - token_freq))

	Kprim = [x[0] for x in sorted_freq][0:2 * T]

	inject_files(path, Kprim)

	return Kprim

def recover_single(path, token, K):
	files = server(path, token)
	if len(files) == 0:
		return None
	else:
		return recover(path, K, token)

def main():
	Kprim = inject_files_single('files/', 3, K)
	print(recover_single('files/', 3, Kprim))

if __name__ == "__main__":
	main()