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
    key = bin(345)[2:]#= generateUniformNumber(lk) #secret key shared between A and B in the setup-session. Omega(n)=O(n)=Theta(n)
    print('[+] Setup')
    print('key : '+key)
    print('key_base10 :',int(key,2))
    return key


def phase1(ida):
    # 1)
    ida = ida #identity of A. O(1)
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
    return (c,n)


def phase3(c,counter):
    #3) Performed by A
    n = counter
    c_10 = str(int(c,2)) # O(lc)
    sc = sumDigits(c_10) # O(lc)

    t = int(key,2)+n # O(max(lk + l(n))). if l(n) < lk ==> O(lk)
    st = sumDigits(str(t)) # O(lk + l(n)). if l(n) < lk ==> O(lk)

    s = sc*st  #l(sc) << l(c_10) (same for st), so: O((max(lc,lk + l(n))^2) for sure (veeery big O)
    r = bin(s)[2:]
    print('\n[+] Phase 3')
    print('t :',t)
    print('\nt :',t,'\nst :',st,'\ns :',s)
    print('A -----> B : u3 = r = '+r)
    return r


def phase4(c):
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
    print('r_hat : ',int(r_hat,2))

    return r_hat


def phase3_C(st_prime,n,c):
    sn = sumDigits(n)
    print('n :',n,'sn :',sn)
    sn_prime = sumDigits(str(int(n)-25))
    print('int(n)-25:',int(n)-25,'sn_prime :',sn_prime)
    #hoping there is no carry ....
    st = st_prime + (-sn_prime+sn)
    print('st_prime:',st_prime,'sn_prime:',sn_prime,'sn:',sn)
    print('st :',st)
    sc = sumDigits(c)
    r = bin(int(sc*st))[2:]
    return r


#######################################################

if __name__ == '__main__':

    lk = 8
    n = 0 # counter
    lc = 8
    key = setup(lk)

    #intercepted values by C
    ida_int = -1
    c_int = -1
    r_int = -1


    while n < 35:
        #>>>> TASK 1 <<<<
        print('\n\n ----- Round',n,'-----\n\n')
        ida = phase1('0b1')
        c,_ = phase2(lc,n) #c and I don't care other params
        r = phase3(c,n)
        r_hat = phase4(c)
        if (r == r_hat):
            print('\nOK : B accepted A')
        else:
            print('\nNOT OK: B did NOT accept A')

        if n == 9: #C (eavesdropper) intercepts the values
            ida_int = ida
            c_int = c
            r_int = r

        n+=1 # update counter

    #>>>> TASK 2 <<<<
    print('\n'+'*'*35+'\n')
    print('Values intercepted by C at round',n-26)
    print('idA :',ida_int,'c :',c_int,int(c_int,2),'r :',r_int,int(r_int,2))
    times_acc = 0 #times C was accepted by B
    times_rej = 0 #times C was rejected by B
    sc_int = sumDigits(c_int)
    s_int = int(r_int,2)
    st_int = s_int/sc_int
    print('st_int :',st_int)

    iter = 300#35
    while iter > 0:

        phase1(str(ida_int))
        c,_ = phase2(lc,n)

        r = phase3_C(st_int,str(n),c)
        r_hat = phase4(c)
        if (r == r_hat):
            print('\nOK : B accepted C')
            times_acc += 1
        else:
            print('\nNOT OK: B did NOT accept C')
            times_rej += 1
        n += 1
        iter-=1

    print(times_acc/(times_acc+times_rej))
    print('times_acc :',times_acc)
