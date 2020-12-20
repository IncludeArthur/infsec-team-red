import time
import matplotlib.pyplot as plt
import numpy as np
from functions import *


def sum_digits(n):
	r = 0
	while n:
		r, n = r + n % 10, n // 10
	return r

#monte carlo method
#IT DOESN'T WORK FOR BIG LK!!
def most_likely_st(n, lk):
	su = []
	#seq = np.linspace(0,2**lk,100)
	seq = np.random.randint(0,2**lk,1000, dtype=np.int64)
	for k in seq:
		t = n + k
		su.append(sum_digits(t))
	unique, counts = np.unique(su, return_counts=True)
	return np.argmax(counts)


def most_likely_st2(n, lk):
	#digits = 3*lk/10
	digits = lk/np.log2(10)
	return round(4.5 * digits)


def attack3(n, lc, lk):
	setup(lk)
	phase1('0b1')
	c2 = phase2(lc, n)
	sc2 = sum_digits(int(c2, 2))

	st_fake = most_likely_st2(n, lk)
	#print('most likely st: ', st_fake)
	s2_fake = st_fake * sc2
	r2_hat = phase4(c2, n)
	s2_hat = int(r2_hat, 2)

	#print(st_fake,st_hat)
	if s2_fake == s2_hat:
		return 1
	else:
		return 0


def main():
	n = 0  # starting counter
	it_max = 1000

	for lc in range(4, 20, 4):
		success = []
		times = []
		for lk in range(8, 512, 4):
			succ = 0
			t = 0
			for it in range(it_max):
				start_time = time.time()

				acc = attack3(n + it, lc, lk)

				end_time = time.time()

				t += (end_time - start_time)
				succ += acc

			success.append(succ / it_max)
			times.append(t / it_max)
			print("success rate:", succ / it_max)
			print("elapsed time:", t / it_max)

		plt.figure(1)
		plt.plot(range(8, 512, 4), success, label=lc)
		plt.figure(2)
		plt.plot(range(8, 512, 4), times, label=lc)

	plt.figure(1)
	plt.ylim(0.0, 0.2)
	plt.legend(title='lc value')
	plt.xlabel('lk')
	plt.ylabel('success probability')

	plt.figure(2)
	# plt.ylim(0, 0.00003)
	plt.legend(title='lc value')
	plt.xlabel('lk')
	plt.ylabel('elapsed time')
	plt.show()


if __name__ == '__main__':
	main()
