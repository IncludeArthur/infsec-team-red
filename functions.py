import random

def generateUniformNumber(length_num):
    '''
    @return binary number (string), with length_num in length
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
    global key
    key = generateUniformNumber(lk)
    #key = bin(1900)[2:]#= generateUniformNumber(lk) #secret key shared between A and B in the setup-session. Omega(n)=O(n)=Theta(n)
    #print('[+] Setup')
    #print('key : '+key)
    #print('key_base10 :',int(key,2))
    return key


def phase1(ida):
    # 1)
    ida = ida #identity of A. O(1)
    #print('\n[+] Phase 1')
    #print('\nidA : '+str(int(ida,2)))
    #rint('A -----> B : u1 = idA = '+str(int(ida,2)))
    return int(ida,2)


def phase2(lc,n):
    # 2)
    lc = lc #challenge-length
    c = generateUniformNumber(lc) #challenge . O(lc)
    n = n
    #print('\n[+] Phase 2')
    #print('c (challenge) : '+c+'\nn (counter) : '+str(n))
    #print('B -----> A : u2 = (c,n) = (',c,',',n,')')
    return c


def phase3(c,counter):
    #3) Performed by A
    n = counter
    c_10 = str(int(c,2)) # O(lc)
    sc = sumDigits(c_10) # O(lc)

    t = int(key,2)+n # O(max(lk + l(n))). if l(n) < lk ==> O(lk)
    st = sumDigits(str(t)) # O(lk + l(n)). if l(n) < lk ==> O(lk)
    #print("c10: ",c_10, "sc: ", sc)

    s = sc*st  #l(sc) << l(c_10) (same for st), so: O((max(lc,lk + l(n))^2) for sure (veeery big O)
    r = bin(s)[2:]
    #print('\n[+] Phase 3')
    #print('t :',t)
    #print('\nt :',t,'\nst :',st,'\ns :',s)
    #print('st: ', st, 's: ',s, 'st div: ',int(s/sc))
    #print('s: ',s, 'st :', st)
    #print('A -----> B : u3 = r = '+r)
    return r


def phase4(c,n):
    #4) Performed by B
    #B has got: key, idA, c, n, r
    #this method has the same complexity of  phase3()
    c_10 = str(int(c,2))
    sc = sumDigits(c_10)

    t = int(key,2)+n
    st = sumDigits(str(t))

    s = sc*st
    r_hat = bin(s)[2:]

    #print('\n[+] Phase 4')
    #print('r_hat : ',int(r_hat,2))

    return r_hat


def phase3_C(st_prime,n,c):
    sn = sumDigits(n)
    #print('n :',n,'sn :',sn)
    sn_prime = sumDigits(str(int(n)-25))
    #print('int(n)-25:',int(n)-25,'sn_prime :',sn_prime)
    #hoping there is no carry ....
    st = st_prime + (-sn_prime+sn)
    #print('st_prime:',st_prime,'sn_prime:',sn_prime,'sn:',sn)
    print('st :',st)
    sc = sumDigits(c)
    r = bin(int(sc*st))[2:]
    return r

#we need to know key!!!!!
def get_st_difference(n):
    #n = n + int(key[-2:], 10)
    n = n + int(key, 10)
    if n<25:
        if 0 <= n%10 < 5: return -11
        else: return -2
    elif 0 <= n%10 < 5: return -2
    else: return 7