import base64
from Crypto.PublicKey import RSA
from math import *
import ast
import gmpy

ciphertext = open('for_alice.enc').read()

key = RSA.importKey(open('alice.pubkey').read())

key.decrypt(ciphertext)
