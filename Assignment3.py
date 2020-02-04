#!/usr/bin/env python
# coding: utf-8

# In[4]:


'''
1.  (5 points) Exercise 4, p. 104

    a. Use the Euclidean algorithm to compute gcd(30030, 257)
       
       Using the Euclidean algorithm in a small function below, we see that the gcd of the 
       two numbers 30030 and 257 is 1. They are coprime.
       
    b. Using the result of part (a) and the fact that 30030 2*3*5*7*11*13, show that 257 is prime.
    
       If 257 is composite, then there exists a prime number under 17 (17 ** 2 = 289) that divides 257. 
       But we know from 2a that the prime factoriation of 30030 is the product of all primes under 17,
       and since we've already shown that 257 and 30030 are coprime, it is not possible for them to share
       any factors greater than 1. Thus, 257 cannot be composite, and therefore must be prime.
    
'''

import math

def eGCD(a, b):
    if a == 0: return b
    if b == 0: return a
    return eGCD(b, a % b)

print("GCD of 30030 and 257 = {0}".format(eGCD(30030, 257)))


# In[5]:


'''
2.  (5 points) Exercise 5, p. 104
    
    a. Compute gcd(4883, 4369).
    
       Using the eGCD function from above, we calculate the gcd of 4883 and 4369 to be 257.
    
    
    b. Factor 4883 and 4369 into products of primes.
    
       Utilizing the prime factorization method below, your get:
       
       Prime factorization of 4883: [19, 257]
       Prime factorization of 4369: [17, 257]
    
'''

print("GCD of 4883 and 4369 = {0}".format(eGCD(4883, 4369)))


# In[21]:


def getPrimes(n):
    
    factors = list()
    
    while n % 2 == 0:
        factors.append(2)
        n /= 2
        
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n /= i
    
    if n > 2:
        factors.append(int(n))

    return factors


# In[22]:


print("Prime factorization of 4883: {0}".format(getPrimes(4883)))
print("Prime factorization of 4369: {0}".format(getPrimes(4369)))


# In[ ]:


'''
3.  (5 points) Exercise 11, p. 105

    Let p be prime. Show that a ** p === a mod p for all a.
    
    There are two possibilities two consider: the first is that p divides a, and the second
    is that p does not divide a. 
    
    If the first is true, and p does divide a, then both sides are equivalent to 0 mod p.
    For example, if a = 10 and p = 2, then 10 ** 2 = 100, which is equivalent to 0 mod 2. 
    The other side of the equation, a mod p, is also equivalent to 0 mod 2. Hence, both sides
    are equal to 0 mod p, which holds true for all numbers a and p such that p divides a.
    
    In the second scenario, p does not divide a, and this covers the rest of the numbers
    not included in scenario number one. Fermat's little theorem tells us that if p does not divide a, 
    then a ** (p-1) === 1 mod p, and if we multiply both sides by a, we end up with a(a ** (p-1)) === a(1) mod p.
    This is in turn equivalent to a ** p === a mod p, which is in fact what we are aiming to show.
    
    Thus, for any two numbers p and a, a ** p === a mod p.
'''


# In[ ]:


'''
4.  (5 points) Exercise 12, p. 105

    Divide 2 ** 10203 by 101. What is the remainder.
    
    101 is a prime number. Thus, we know from Fermat's little theorem that 2 ** 100 === 1 mod 101. 
    Since we know that 2 ** 100 === 1 mod 101, we can say that 2 ** (100 * n) === 1 ** n mod 101 also,
    because we are just raising each side to the power n. So, we know that 2 ** 100n === 1 mod 101, and
    therefore 2 ** 10200 === 1 mod 101 because 100 divides 10200. We are then left with a remainder of 
    2 ** 3, or: 
    
    8 mod 101.
'''


# In[ ]:


'''
5.  (5 points) Exercise 13, p. 105

    Find the last two digits of 123 ** 562.
    
    Euler's theorem states that a ** phi(n) === 1 mod n. If we are looking for a two-digit number,
    then we are looking for what number between 0 and 99 our value is congruent to (mod 100). 
    We know that phi(100) = 40, and also that phi(123) is equal to 40 because 100 and 123
    are coprime. So, we end up with 123 ** 40 === 1 mod 100, or 23 ** 40 === 1 mod 100 because we are mod 100.
    
    Since 560 / 40 = 14, we can also say that (23 ** 40) ** 14 = 23 ** 560 = 1 mod 100. 
    Since 23 ** 562 is equivalent to (23 ** 560) * (23 ** 2), we can simply take the last 
    two digits of 529 (23 ** 2).
    
    We are therefore left with the digits 29 as our answer.  
'''


# In[63]:


'''
6. (10 points) Stream cipher with the Blum-Blum-Shub CSPRNG Write a program that:

    Takes as input a plaintext that is a sequence of bits represented as a string of zeroes and ones
    
    Using the Blum-Blum-Shub CSPRNG written in the last assignment and initialized as shown in the textbook, 
    generate a sequence of key bits represented as a string of zeroes and ones with the same 
    length as the input string
    
    Create a ciphertext string of ones and zeroes where each bit is the exclusive-or of the 
    corresponding bits in the plaintext and key strings
    
    Print the ciphertext string as a sequence of bits in groups of 4
    
    You can test your program with this plaintext string, which is the word SECURE in ASCII:
    0101 0011 0100 0101 0100 0011 0101 0101 0101 0010 0100 0101
    
    My bbsprng is inserted below. Using the initial p and q values from the book, 
    and the above string of bits as plaintext, we get the following:
    
    plaintext:  0101 0011 0100 0101 0100 0011 0101 0101 0101 0010 0100 0101
    key:        0011 1000 0000 0110 1111 1100 0111 0000 0011 1111 1100 0000 
    ciphertext: 0110 1011 0100 0011 1011 1111 0010 0101 0110 1101 1000 0101 

'''

def bbsprng(i):
    result = [0] * i

    # Start with the two primes from the text
    p = 24672462467892469787
    q = 396736894567834589803
    
    # Calculate n
    n = p * q
    x = 873245647888478349013

    # For each bit in the plaintext, generate a pseudo-random x
    for j in range(i):
        x = (x**2) % n
        result[j] = x
        
    # For each x in the key, get the last bit
    result = [j%2 for j in result]
    
    return result

plaintext = "0101 0011 0100 0101 0100 0011 0101 0101 0101 0010 0100 0101"
print("plaintext:  " + plaintext)
plaintext = plaintext.replace(" ","")
plaintext = [int(x) for x in plaintext]

key = bbsprng(len(plaintext))
key_str = ""
for i in range(len(key)):
    key_str += str(key[i])
    if (i + 1) % 4 == 0:
        key_str += " " 
print("key:        "+ key_str)

ciphertext = [a^b for a,b in zip(plaintext, key)]

result_str = ""
for i in range(len(ciphertext)):
    result_str += str(ciphertext[i])
    if (i + 1) % 4 == 0:
        result_str += " "      
        
print("ciphertext: "+ result_str)


# In[117]:


'''
7.  (15 points) Generating prime numbers 
    Write a program that uses the primality test derived from Fermat's Little Theorem 
    to generate a sequence of prime numbers. The program will repeat the following 16 times 
    (and so generate 16 prime numbers):

    In a loop:
        Randomly generate an integer between 2**24 and 2**25
        
        Check whether it's prime using the FLT test
    
        Terminate the loop if a prime is found

        Print the prime and the number of times the loop repeated before finding a prime

    
    You will have to implement the FLT test. If you use Java as your language, 
    only use primitive variables and values.
    
    My implementation is below and returned the following tuple: (27220013, 1). The first item in the tuple is
    the prime candidate, and the second number is the iteration (between 1 and 16). If no prime is found, the
    function returns a prime candidate equal to -1.
'''

import random
def findPrime(n):
    
    # In a loop:
    for i in range(n):
        isPrime = True
        
        #Randomly generate an integer between 2**24 and 2**25
        p = random.randrange(2**24,2**25,2)-1
        
        # Check whether it's prime using the FLT test
        for j in range(20):
            a = random.randint(0,p)
            if eGCD(a,p) != 1 or fastMod(a,p) != 1: 
                isPrime = False
                break
                
        # Terminate the loop if a prime is found
        if isPrime:
            return (p,i+1)
        
    # Print the prime and the number of times the loop repeated before finding a prime (no prime found = -1)        
    return (-1,n)
     
def fastMod(a,p):
    res = 1
    power = p-1;
    while power > 0:
        if power%2 == 1:
            res = (a*res) % p
            power -= 1
        power /= 2
        a = (a*a) % p;
    return res
    
findPrime(16)


# In[ ]:




