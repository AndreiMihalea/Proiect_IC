ciphertext = 'ULEHK GZLBY YQXFK BWBYN LURPU JYKGV WRVLS NYXPO GHABX'
key = 'CRYPTONOMICON'

plaintext = []

ct = []
k = []

for c in ciphertext:
	if c != ' ':
		ct.append(ord(c) - ord('A'))

for c in key:
	k.append(ord(c) -  ord('A'))

#initial deck
deck = [i + 1 for i in range(52)] + ['A'] + ['B']

print (deck)

for char in key:
	#pas1
	A = deck.index('A')
	if A < 53:
		deck[A], deck[A + 1] = deck[A + 1], deck[A]
	else:
		deck[1:] = deck[-1:] + deck[1:-1]

	print (deck)

	#pas2
	B = deck.index('B')
	if B < 53:
		deck[B], deck[B + 1] = deck[B + 1], deck[B]
	else:
		deck[1:] = deck[-1:] + deck[1:-1]

	B = deck.index('B')
	if B < 53:
		deck[B], deck[B + 1] = deck[B + 1], deck[B]
	else:
		deck[1:] = deck[-1:] + deck[1:-1]

	print (deck)

	#pas3
	above_first = []
	first_index = 0
	for i, c in enumerate(deck):
		if c == 'A' or c == 'B':
			first_index = i
			break
		else:
			above_first.append(c)

	below_second = []
	second_index = 53
	for i, c in enumerate(reversed(deck)):
		if c == 'A' or c == 'B':
			second_index = 53 - i
			break
		else:
			below_second.append(c)

	below_second = list(reversed(below_second))

	deck = below_second + deck[first_index:second_index + 1] + above_first

	print (deck)

	#pas4
	bottom = deck[53]
	if bottom == 'A' or bottom == 'B':
		bottom = 53
	deck = deck[bottom:53] + deck[0:bottom] + [deck[53]]

	print (deck)

	#pas5
	cut = ord(char) - ord('A') + 1
	bottom = cut
	deck = deck[bottom:53] + deck[0:bottom] + [deck[53]]

	print (deck)
	print ()

stream = []

while len(stream) < len(ciphertext):
	#pas1
	A = deck.index('A')
	if A < 53:
		deck[A], deck[A + 1] = deck[A + 1], deck[A]
	else:
		deck[1:] = deck[-1:] + deck[1:-1]

	print (deck)

	#pas2
	B = deck.index('B')
	if B < 53:
		deck[B], deck[B + 1] = deck[B + 1], deck[B]
	else:
		deck[1:] = deck[-1:] + deck[1:-1]

	B = deck.index('B')
	if B < 53:
		deck[B], deck[B + 1] = deck[B + 1], deck[B]
	else:
		deck[1:] = deck[-1:] + deck[1:-1]

	print (deck)

	#pas3
	above_first = []
	first_index = 0
	for i, c in enumerate(deck):
		if c == 'A' or c == 'B':
			first_index = i
			break
		else:
			above_first.append(c)

	below_second = []
	second_index = 53
	for i, c in enumerate(reversed(deck)):
		if c == 'A' or c == 'B':
			second_index = 53 - i
			break
		else:
			below_second.append(c)

	below_second = list(reversed(below_second))

	deck = below_second + deck[first_index:second_index + 1] + above_first

	print (deck)

	#pas4
	bottom = deck[53]
	if bottom == 'A' or bottom == 'B':
		bottom = 53
	deck = deck[bottom:53] + deck[0:bottom] + [deck[53]]

	print (deck)

	#pas5
	top = deck[0]
	if top == 'A' or top == 'B':
		top = 53
	add = deck[top]

	if add != 'A' and add != 'B':
		stream.append(add)

print (stream)

for i, c in enumerate(ct):
	plaintext.append((c - stream[i]) % 26)

plaintext = [chr(i + 65) for i in plaintext]

plaintext = ''.join(plaintext)

print (plaintext)