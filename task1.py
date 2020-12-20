#Laboratory 3, team: RED

import random
import time
import matplotlib.pyplot as plt
import numpy as np
from functions import *

def attack2(n,lc,lk):

	setup(lk)

	# cycle n
	phase1('0b1')
	c1 = phase2(lc, n)
	r1 = phase3(c1, n)
	s1 = int(r1, 2)
	sc1 = sumDigits(str(int(c1, 2)))

	if sc1 == 0: return 0
	st1 = int(s1 / sc1)

	#from cycle n, C knows (n,c1) and s1

	# cycle n + 25
	n = n + 25
	phase1('0b1')
	c2 = phase2(lc, n)
	sc2 = sumDigits(str(int(c2, 2)))

	s2_fake = (st1 - 2) * sc2
	r2_hat = phase4(c2, n)
	s2_hat = int(r2_hat, 2)

	# print('st: ',st1, int(s2_hat/sc2))
	#print('s: ', s2_fake, s2_hat)
	if s2_fake == s2_hat:
		return 1
	else: return 0


def main():

	n = 0  # starting counter
	it_max = 1000

	for lc in range(4,20,4):
		times = []
		for lk in range(8,512,4):
			t = 0
			for it in range(it_max):
				start_time = time.time()

				setup(lk)

				phase1('0b1')
				n = n + it
				c = phase2(lc, n)
				r = phase3(c, n)
				s = int(r, 2)
				sc = sumDigits(str(int(c, 2)))
				r_hat = phase4(c, n)
				s_hat = int(r_hat, 2)

				end_time = time.time()

				t += (end_time - start_time)

			times.append(t/it_max)
			print("elapsed time:", t/it_max)

		plt.plot(range(8, 512, 4), times, label=lc)

	#plt.ylim(0, 0.00003)
	plt.legend(title='lc value')
	plt.xlabel('lk')
	plt.ylabel('elapsed time')
	plt.show()


if __name__ == '__main__':
	main()