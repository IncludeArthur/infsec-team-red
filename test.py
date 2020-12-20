import matplotlib.pyplot as plt
import numpy as np

def sum_digits(n):
   r = 0
   while n:
       r, n = r + n % 10, n // 10
   return r

# t = k + n
# n' = n - 25
# t' = k' + n' = k + n - 25 = t - 25

def main():

    ranget = 1000000
    dif = []
    su = []
    for n in range(25,ranget):
        t = n + 0
        d = sum_digits(t) - sum_digits(t-25)
        #if (n>26 and d!=dif[-1]): print(t,d)
        dif.append(d)
        su.append(sum_digits(t))

    plt.plot(range(25,ranget),dif)
    plt.show()
    #plt.hist(dif)
    #plt.show()

    plt.plot(range(25, ranget), su)
    plt.show()
    plt.hist(su)
    plt.show()

    unique, counts = np.unique(dif, return_counts=True)
    perc = counts*100/ranget
    print('frequencies of St diff:')
    print(np.asarray((unique, counts)).T)
    print(perc)

    unique, counts = np.unique(su, return_counts=True)
    perc = counts * 100 / ranget
    print('frequencies of Sum of digits:')
    print(np.asarray((unique, counts)).T)
    print(perc)


if __name__ == '__main__':
    main()