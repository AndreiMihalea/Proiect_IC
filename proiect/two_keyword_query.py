from binary_search_attack import *

files = [f for f in os.listdir('files')]
for f in files:
	if f != 'leaked_files' and f != 'simulated_files':
		if os.path.isfile('files/' + f):
			os.remove('files/' + f)
		else:
			shutil.rmtree('files/' + f)

def inject_files_disjoint(path, K1, K2):
	inject_files(path, K1)

	files = [f for f in os.listdir(path) if os.path.isfile(path + f)]

	for f in files:
		fo = open(path + f, 'r+')
		content = fo.read()

		for k in K2:
			if k not in content:
				fo.write(k + '\n')

def inject_files_conjunctive(path, K):
	K1s = {}
	K2s = {}
	for i in range(bits):
		K1i = []
		k2i = []

		for k in K:
			if k[i] == '0':
				K1i.append(k)

		K2i = list(set(K).difference(set(K1i)))

		F1i = open(path + 'F1' + str(i), 'w')
		F2i = open(path + 'F2' + str(i), 'w')

		for k in K1i:
			F1i.write(k + '\n')

		for k in K2i:
			F2i.write(k + '\n')

		if not os.path.exists(path + 'Fbold1' + str(i)):
			os.makedirs(path + 'Fbold1' + str(i))

		if not os.path.exists(path + 'Fbold2' + str(i)):
			os.makedirs(path + 'Fbold2' + str(i))

		inject_files_disjoint(path + 'Fbold1' + str(i) + '/', K1i, K2i)
		inject_files_disjoint(path + 'Fbold2' + str(i) + '/', K2i, K1i)

		K1s[i] = K1i
		K2s[i] = K2i

	return K1s, K2s

def recover_conjunctive(path, t1, t2, K, K1s, K2s):
	for i in range(bits):
		files = server(path, t1, t2)
		
		if 'F1' + str(i) not in files and 'F2' + str(i) not in files:
			k1 = recover(path + 'Fbold1' + str(i) + '/', K1s[i], t1, t2)
			k2 = recover(path + 'Fbold2' + str(i) + '/', K2s[i], t1, t2)

	return (k1, k2)

def main():
	K1s, K2s = inject_files_conjunctive('files/', K)
	print(recover_conjunctive('files/', 6, 5, K, K1s, K2s))

if __name__ == "__main__":
	main()