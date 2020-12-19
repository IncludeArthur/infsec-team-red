#Laboratory 3, team: RED

import random
import matplotlib.pyplot as plt

def generateUniformNumber(length_num):
    '''
    @return binary number, with length_num in length
    '''
    num = ''
    for i in range(length_num):
        tmp = random.random()
        if( tmp < 0.5 ):
            num += '0'
        else:
            num += '1'
    return num


def sumDigits(num):
    '''
    @num : string number with decimal digits
    @return the sum of the digits of num
    '''
    sumNum = 0
    for i in num:
        sumNum += int(i,10)

    return sumNum


def setup(lk):
    # SETUP
    lk = lk #key-length
    key = generateUniformNumber(lk) #secret key shared between A and B in the setup-session. Omega(n)=O(n)=Theta(n)
    print('[+] Setup')
    print('key : '+key)
    #print('key_base10 :',int(key,2))
    return key


def phase1():
    # 1)
    ida = '0b1' #identity of A. O(1)
    print('\n[+] Phase 1')
    #print('\nidA : '+str(int(ida,2)))
    print('A -----> B : u1 = idA = '+str(int(ida,2)))
    return int(ida,2)


def phase2(lc,n):
    # 2)
    lc = lc #challenge-length
    c = generateUniformNumber(lc) #challenge . O(lc)
    n = n
    print('\n[+] Phase 2')
    #print('c (challenge) : '+c+'\nn (counter) : '+str(n))
    print('B -----> A : u2 = (c,n) = (',c,',',n,')')
    return c


def phase3(c,counter):
    #3) Performed by A
    n = counter
    c_10 = str(int(c,2)) # O(lc)
    sc = sumDigits(c_10) # O(lc)

    t = int(key,2)+n # O(lk + l(n)). if l(n) < lk ==> O(lk)
    st = sumDigits(str(t)) # O(lk + l(n)). if l(n) < lk ==> O(lk)

    s = sc*st  #l(sc) << l(c_10) (same for st), so: O((max(lc,lk + l(n))^2) for sure (veeery big O)
    r = bin(s)[2:]
    print('\n[+] Phase 3')
    #print('c_base10 : '+c_10,'\nsc:',sc,'\nt :',t,'\nst :',st,'\ns :',s,'\nr (response) :',r)
    print('A -----> B : u3 = r = '+r)
    return r


def phase4(c,r):
    #4) Performed by B
    #B has got: key, idA, c, n, r
    #this method has the same complexity of  phase3()
    c_10 = str(int(c,2))
    sc = sumDigits(c_10)

    t = int(key,2)+n
    st = sumDigits(str(t))

    s = sc*st
    r_hat = bin(s)[2:]

    print('\n[+] Phase 4')
    print('r_hat : ',r_hat)

    return r_hat


#######################################################

if __name__ == '__main__':

    lk = 8
    n = 1 # counter
    lc = 8

    #intercepted values by C
    ida_int = -1
    c_int = -1
    r_int = -1


    while n <= 35:
        #>>>> TASK 1 <<<<
        print('\n\n ----- Round',n,'-----\n\n')
        key = setup(lk)
        ida = phase1()
        c = phase2(lc,n)
        r = phase3(c,n)
        r_hat = phase4(c,r)
        if (r == r_hat):
            print('\nOK : B accepted A')
        else:
            print('\nNOT OK: B did NOT accept A')

        if n == 10: #C (eavesdropper) intercepts the values
            ida_int = ida
            c_int = c
            r_int = r

        n+=1 # update counter

    #>>>> TASK 2 <<<<
    print('\n'+'*'*35+'\n')
    print('Values intercepted by C at round',n-26)
    print('idA :',ida_int,'c :',c_int,'r :',r_int)
    times_acc = 0 #times C was accepted by B
    times_rej = 0 #times C was rejected by B

    iter = 15
    while iter > 0:

        iter-=1
