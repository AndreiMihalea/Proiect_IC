from binary_search_attack import *
from collections import OrderedDict

files = [f for f in os.listdir('files')]
for f in files:
	if f != 'leaked_files' and f != 'simulated_files':
		if os.path.isfile('files/' + f):
			os.remove('files/' + f)
		else:
			shutil.rmtree('files/' + f)
			
def attack_conjunctive(path, q, K):
	k = []
	d = len(q)
	for i in range(d, 0, -1):
		Ki = [x for x in K]
		b = int(len(Ki) / 2)

		for j in range(2, int(math.log(len(Ki), 2) + 1)):
			fo = open(path + 'F', 'w')

			for l in range(b):
				fo.write(Ki[l] + '\n')

			for key in k:
				fo.write(key + '\n')

			fo.close()

			files = server(path, *q)

			if len(files) > 0:
				b = b - int(len(Ki) / (2**j))
			else:
				b = b + int(len(Ki) / (2**j))


		fo = open(path + 'F', 'w')

		for l in range(b):
			fo.write(Ki[l] + '\n')

		for key in k:
			fo.write(key + '\n')

		fo.close()

		files = server(path, *q)

		if len(files) > 0:
			ki = Ki[b - 1]
		else:
			ki = Ki[b]

		k.append(ki)

	return k

def main():
	print(attack_conjunctive('files/', [1, 15], K))

if __name__ == "__main__":
	main()