from binary_search_attack import *
from hierarchical_search_attack import *
import random

tokens = [i for i in range(n_keys)]

m = 128

n = 4

t = []

nr = 0

while nr < m:
	r = random.choice(tokens)
	if r not in t:
		t = t + [r]
		nr = nr + 1

def attack_multiple_tokens(path, t, K):
	t_freq = {}

	G = []

	keywords = []

	simulated_files = [f for f in os.listdir(path + 'simulated_files/') if os.path.isfile(path + 'simulated_files/' + f)]

	leaked_files = [f for f in os.listdir(path + 'leaked_files/') if os.path.isfile(path + 'leaked_files/' + f)]

	for to in t:
		t_freq[to] = len(server(path + 'simulated_files/', to)) / len(simulated_files)

	t1 = list(reversed(sorted(t_freq.items(), key=lambda x: x[1])))[0:n]

	t1 = [x[0] for x in t1]

	all_keyword_freq = {}

	for k in K:
		all_keyword_freq[k] = 0

	for k in K:
		for l in leaked_files:
			f = open(path + 'leaked_files/' + l)
			content = f.read()
			f.close
			if k in content:
				all_keyword_freq[k] += 1

	for k in all_keyword_freq:
		all_keyword_freq[k] /= len(leaked_files)

	Kprim = []

	for to in t1:
		sorted_freq = sorted(all_keyword_freq.items(), key=lambda x: abs(x[1] - t_freq[to]))
		Kt = [x[0] for x in sorted_freq][0:int(2 * T / n)]
		Kprim = list(set(Kprim).union(set(Kt)))

	inject_files(path, Kprim)

	for to in t1:
		rt = server(path, to)
		if len(rt) > 0:
			kt = recover(path, Kprim, to)
			G = G + [(to, kt)]
			keywords.append((to, kt[0]))

	t2 = list(set(t).difference(set(t1)))

	joint_freq_t = {}

	for to1 in t:
		for to2 in t:
			if to1 != to2:
				joint_freq_t[(to1, to2)] = len(server(path + 'simulated_files/', to1, to2)) / len(simulated_files)
				joint_freq_t[(to2, to1)] = joint_freq_t[(to1, to2)]

	Ksec = []

	for tp in t2:
		sorted_freq = sorted(all_keyword_freq.items(), key=lambda x: abs(x[1] - t_freq[tp]))
		Ktp = [x[0] for x in sorted_freq][0:int(2 * T / n)]

		joint = {}

		delta = 0

		for kp in Ktp:
			for (to, kt) in G:
				if to != tp and kt[0] != kp:
					for l in leaked_files:
						f = open(path + 'leaked_files/' + l)
						content = f.read()
						f.close()
						if kt[0] in content and kp in content:
							if (kt[0], kp) not in joint:
								joint[(kt[0], kp)] = 1 / len(leaked_files)
							else:
								joint[(kt[0], kp)] += 1 / len(leaked_files)

		for kp in Ktp:
			for (to, kt) in G:
				if to != tp and kt[0] != kp:
					if (kt[0], kp) in joint:
						if joint[(kt[0], kp)] != 0:
							if joint_freq_t[(to, tp)] / joint[(kt[0], kp)] > delta:
								delta = joint_freq_t[(to, tp)] / joint[(kt[0], kp)]

		for kp in Ktp:
			for (to, kt) in G:
				if to != tp and kt[0] != kp:
					if (kt[0], kp) in joint:
						if abs(joint_freq_t[(to, tp)] - joint[(kt[0], kp)]) > delta * joint[(kt[0], kp)]:
							if kp in Ktp:
								Ktp.remove(kp)

		Ksec = list(set(Ksec).union(set(Ktp)))

		if len(Ksec) > 2 * T:
			inject_files(path, Ksec)
			for tp in t2:
				ktp = recover(path, Ksec, tp)
				keywords.append((tp, ktp[0]))
		else:
			inject_files_hierarchical(path, Ksec)
			ktp = recover_hierarchical(path, Ksec, tp)
			keywords.append((tp, ktp[0]))

	print (keywords)

attack_multiple_tokens('files/', t, K)
