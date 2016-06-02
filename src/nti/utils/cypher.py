#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import copy
import math
import base64
import pickle
import random
from itertools import cycle
from itertools import combinations

def _XOR(text, key):
	"""
	A TOY "cipher" that symmetrically obscures
	the `text` based `key`. Do not use this when
	security matters.
	"""
	result = []
	key = cycle(key)
	for t in text:
		t = chr(ord(t) ^ ord(next(key)))
		result.append(t)

	return b''.join(result)

DEFAULT_PASSPHRASE = base64.b64decode('TjN4dFRoMHVnaHQhIUM=')

def make_ciphertext(plaintext, passphrase=DEFAULT_PASSPHRASE):
	"""
	A trivial function that uses a toy "cipher" (XOR) to obscure
	and then base64 encode a sequence of bytes.
	"""
	encoded = _XOR(plaintext, passphrase)
	result = base64.b64encode(encoded)
	return result

def get_plaintext(ciphertext, passphrase=DEFAULT_PASSPHRASE):
	"""
	A trivial function that uses a toy "cipher" (XOR) to obscure
	a base64 encoded sequence of bytes.
	"""
	result = base64.b64decode(ciphertext)
	result = _XOR(result, passphrase)
	return result

# A implementation of RSA public key encryption algorithms
# Adapted from https://gist.github.com/avalonalex/2122098

def euclid(a, b):
	"""
	returns the Greatest Common Divisor of a and b
	"""
	a = abs(a)
	b = abs(b)
	if a < b:
		a, b = b, a
	while b != 0:
		a, b = b, a % b
	return a

def co_prime(l):
	"""
	returns 'True' if the values in the list L are all co-prime
	otherwise, it returns 'False'.
	"""
	for i, j in combinations(l, 2):
		if euclid(i, j) != 1:
			return False
	return True

def extended_euclid(a, b):
	"""
	return a tuple of three values: x, y and z, such that x is
	the GCD of a and b, and x = y * a + z * b
	"""
	if a == 0:
		return b, 0, 1
	else:
		g, y, x = extended_euclid(b % a, a)
		return g, x - (b // a) * y, y

def mod_inv(a, m):
	"""
	returns the multiplicative inverse of a in modulo m as a
	positive value between zero and m-1
	"""
	# notice that a and m need to co-prime to each other.
	if co_prime([a, m]):
		linearCombination = extended_euclid(a, m)
		return linearCombination[1] % m
	else:
		return 0

def extract_twos(m):
	"""
	m is a positive integer. A tuple (s, d) of integers is returned
	such that m = (2 ** s) * d.
	"""
	# the problem can be break down to count how many '0's are there in
	# the end of bin(m). This can be done this way: m & a stretch of '1's
	# which can be represent as (2 ** n) - 1.
	assert m >= 0
	i = 0
	while m & (2 ** i) == 0:
		i += 1
	return i, m >> i

def int2base_two(x):
	"""
	x is a positive integer. Convert it to base two as a list of integers
	in reverse order as a list.
	"""
	# repeating x >>= 1 and x & 1 will do the trick
	assert x >= 0
	bitInverse = []
	while x != 0:
		bitInverse.append(x & 1)
		x >>= 1
	return bitInverse

def mod_exp(a, d, n):
	"""
	returns a ** d (mod n)
	"""
	assert d >= 0
	assert n >= 0
	base2D = int2base_two(d)
	base2DLength = len(base2D)
	modArray = []
	result = 1
	for i in range(1, base2DLength + 1):
		if i == 1:
			modArray.append(a % n)
		else:
			modArray.append((modArray[i - 2] ** 2) % n)
	for i in range(0, base2DLength):
		if base2D[i] == 1:
			result *= base2D[i] * modArray[i]
	return result % n

def miller_rabin(n, k):
	"""
	Miller Rabin pseudo-prime test
	return True means likely a prime, (how sure about that, depending on k)
	return False means definitely a composite.
	Raise assertion error when n, k are not positive integers
	and n is not 1
	"""
	assert n >= 1
	# ensure n is bigger than 1
	assert k > 0
	# ensure k is a positive integer so everything down here makes sense

	if n == 2:
		return True
	# make sure to return True if n == 2

	if n % 2 == 0:
		return False
	# immediately return False for all the even numbers bigger than 2

	extract2 = extract_twos(n - 1)
	s = extract2[0]
	d = extract2[1]
	assert 2 ** s * d == n - 1

	def try_composite(a):
		"""
		Inner function which will inspect whether a given witness
		will reveal the true identity of n. Will only be called within
		millerRabin
		"""
		x = mod_exp(a, d, n)
		if x == 1 or x == n - 1:
			return None
		else:
			for _ in range(1, s):
				x = mod_exp(x, 2, n)
				if x == 1:
					return False
				elif x == n - 1:
					return None
			return False

	for _ in range(0, k):
		a = random.randint(2, n - 2)
		if try_composite(a) == False:
			return False
	return True  # actually, we should return probably true.

def prime_sieve(k):
	"""
	return a list with length k + 1, showing if list[i] == 1, i is a prime
	else if list[i] == 0, i is a composite, if list[i] == -1, not defined
	"""

	def is_prime(n):
		"""
		return True is given number n is absolutely prime,
		return False is otherwise.
		"""
		for i in range(2, int(n ** 0.5) + 1):
			if n % i == 0:
				return False
		return True
	result = [-1] * (k + 1)
	for i in range(2, int(k + 1)):
		if is_prime(i):
			result[i] = 1
		else:
			result[i] = 0
	return result

def find_a_prime(a, b, k):
	"""
	Return a pseudo prime number roughly between a and b,
	(could be larger than b). Raise ValueError if cannot find a
	pseudo prime after 10 * ln(x) + 3 tries.
	"""
	x = random.randint(a, b)
	for _ in range(0, int(10 * math.log(x) + 3)):
		if miller_rabin(x, k):
			return x
		else:
			x += 1
	raise ValueError()

def new_key(a, b, k):
	"""
	Try to find two large pseudo primes roughly between a and b.
	Generate public and private keys for RSA encryption.
	Raises ValueError if it fails to find one
	"""
	try:
		p = find_a_prime(a, b, k)
		while True:
			q = find_a_prime(a, b, k)
			if q != p:
				break
	except Exception:
		raise ValueError("Cannot find a prime")

	n = p * q
	m = (p - 1) * (q - 1)

	while True:
		e = random.randint(1, m)
		if co_prime([e, m]):
			break

	d = mod_inv(e, m)
	return (n, e, d)

def string_2_numlist(strn):
	"""
	Converts a string to a list of integers based on ASCII values
	"""
	return [ ord(chars) for chars in pickle.dumps(strn) ]

def numlist_2_string(l):
	"""
	Converts a list of integers to a string based on ASCII values
	"""
	return pickle.loads(''.join(map(chr, l)))

def numlist_2_blocks(l, n):
	"""
	Take a list of integers(each between 0 and 127), and combines them
	into block size n using base 256. If len(L) % n != 0, use some random
	junk to fill L to make it."""
	# Note that ASCII printable characters range is 0x20 - 0x7E
	return_list = []
	to_process = copy.copy(l)
	if len(to_process) % n != 0:
		for i in range(0, n - len(to_process) % n):
			to_process.append(random.randint(32, 126))
	for i in range(0, len(to_process), n):
		block = 0
		for j in range(0, n):
			block += to_process[i + j] << (8 * (n - j - 1))
		return_list.append(block)
	return return_list

def blocks_2_numlist(blocks, n):
	"""
	inverse function of numlist_2_blocks.
	"""
	return_list = []
	to_process = copy.copy(blocks)
	for num_block in to_process:
		inner = []
		for _ in range(0, n):
			inner.append(num_block % 256)
			num_block >>= 8
		inner.reverse()
		return_list.extend(inner)
	return return_list

def encrypt(message, modN, e, block_size=15):
	"""
	given a string message, public keys and blockSize, encrypt using
	RSA algorithms.
	"""
	num_list = string_2_numlist(message)
	num_blocks = numlist_2_blocks(num_list, block_size)
	return [mod_exp(blocks, e, modN) for blocks in num_blocks]

def decrypt(secret, modN, d, block_size=15):
	"""
	reverse function of encrypt
	"""
	num_blocks = [mod_exp(blocks, d, modN) for blocks in secret]
	num_list = blocks_2_numlist(num_blocks, block_size)
	return numlist_2_string(num_list)

# n, e, d = new_key(10 ** 100, 10 ** 101, 50)
# cipher = encrypt(message, n, e)
# deciphered = decrypt(cipher, n, d)