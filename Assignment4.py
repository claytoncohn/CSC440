#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
Clayton Cohn
20200217
CSC440
Assignment 4
'''

'''
1. (10 points) Exercise 4, page 147

    For a string of bits S, let Sbar denote the complementary string obtained by changing all the 1s to 0s
    and all the 0s to 1s (equivalently, Sbar = S ^ 11111....). Show that if DES key K encrypts P to C, then
    Kbar encrypts Pbar to Cbar. (Hint: This has nothing to do with the structure of the S-boxes. To do the
    problem, just work through the encryption algorithm):
    
    I am going to start by pointing out that the xor function is self-inverting, associative, and commutative.
    We won't be needing all of that, but I feel that it is still interesting to point out. What we are going to
    use from the above is the fact that if S' is S ^ 1111111... and K' is K ^ 11111111, then S' ^ K' must equal 
    S ^ K (we will use this later). 
    
    I am now going to step through the algorithm and explain why, at each step, why DES of S' with key K' will
    always equal C'--that is, at every step of the algorithm, the left side will always be equal to the 
    corresponding right side of C ^ 1111111...
    
    The first step of DES is the initial permutation. This does not affect the relationship, as we are selecting 
    the same bits from both S and S'. For instance, reardless of where the 8th bit of S ends up, it will always be 
    at the same position as the 8th bit of S', and those two (by definition) will always xor to 1. It is by this 
    definition that we know that the same will also hold true for our key transformation, expansion permutation,
    and final permutation: all bits xoring their complementary counterpart will always be 1. In fact, this holds
    true for every part of this algorithm except one: s-box selection.
    
    During s-box selection, one might worry that our current equality might be in jeapordy because different input
    values on the left and right could result in different choices within the s-boxes, and therefore result in
    drastically different outcomes for each side (i.e. we could lose our corresponding bit congruency); 
    however, this is not the case. Let's remember how the input values for the s-boxes are chosen: by xor. 
    Because the input values are determined by xoring the key and plaintext, the above equality holds true. 
    That is, we are guaranteed to select the same s-box values on both sides, and will thus continue to be 
    referring to the same bits, and each of those bits (now, as always) will xor with its corresponding bit on 
    the other side of the equation to make 1. 
    
    So, throughout the algorithm in its entirety, there is never a point where DES(S') with key K' does not
    equal the compliment of the same step for DES(S) with key K. And since we know that XOR is commutative,
    and that DES(S) with key K = C, it follows that DES(S') with key K' must also equal C'.
'''


# In[ ]:


'''
2. (10 points) Exercise 6 on page 147

    Suppose Triple DES is performed by choosing two keys K1, K2 and computing Ek1(Ek2(Ek2(m))) (note that the order
    of the keys has been modified from the usual two-key version of Triple DES). Show how to attack this modified 
    version with a meet-in-the-middle attack.
    
    The meet-in-the-middle attack is designed for double DES, i.e. Ek1(Ek2(m)). Since we are trying to decrypt
    Ek1(Ek2(Ek2(m))), we can just do two separate meet-in-the-middle attacks. That being said, I am operating under
    two assumptions: the first is that there is no issue regarding memory storage capabilitity. The second is that 
    I have access to enough plaintext/ciphertext pairs to carry out the attack (it is given that we are to do a 
    meet-in-the-middle attack, so I assume this is not a problem). 
    
    Our encryption structure looks like this:
    
    m -> Ek2 -> x
    x -> Ek2 -> y
    y -> Ek1 -> c
    
    First, we are going to brute-force encrypt the plaintext m using all possible 2^56 keys, and store each
    encryption's corresponding ciphertext x...one of these keys will be our k2. Then we are going to decrypt the 
    corresponding ciphertext c with all possible 2^56 key values and store each decryption's corresponding 
    plaintext y...one of these keys will be our k1.
    
    Our xs were yieled by DES(m,k2). We also know that DES(x,k2) = y. Therefore, to find k2, we perform another
    encryption on each of our xs, each with its corresponding k2 from DES(m,k2), and we will have a set of ys
    to compare to the set of ys found from decrypting DES(c,k1). For every pair that matches, we obtain one set
    of candidate keys. Then it's simply a matter of using each pair of candidate keys with our other known plaintext 
    and ciphertext pairs, and finding out which set of keys transforms our plaintext into its corresponding ciphertext.
    
    It is important to note that this would be significantly faster than doing a meet-in-the-middle attack on 3DES
    where all three keys were different. If there were three different keys, we wouldn't be able to simply do DES(x,k2)
    (for all xs and one key per x) to get our ys. We only had that luxury because we knew that the first two 
    encryptions were done with the same key. If all three keys were different, we would have to do DES(x,k2) for ALL xs
    and ALL keys (hence the approximate 2^112 operations required to crack 3DES). Having the first two keys be equal to
    each other requires something more in the range of of 2^57 or 2^58 operations: 2^56 for m->x, 2^56 for x->y, 
    2^56 for c->y, and some additional operations for finding and verifying candidate keys. This isn't exact, of course,
    but you get the idea.  
'''


# In[242]:


'''
3. (50 points) Implement encryption in the textbook's simplified DES scheme. 

    Write the program so that it contains a method called encrypt(plaintext, key) 
    where the plaintext and the key are both integers. The first must be in the range 0 to 4095 
    and the second in the range 0 to 511. 
    
    My suggestion is to write this method with the first part 
    generating a list or array of the four sub-keys and the second part a loop that iterates four times, 
    once for each round. In that loop, call methods for carrying out an exclusive-or, for expanding, 
    and for applying each of the two S-boxes. I am leaving a number of details unspecified but those will 
    be filled in as you begin to work on this and ask me questions. I will provide test data in the form 
    of plaintexts, keys, and their resulting ciphertexts.

    Please also add to the program a driver method for testing your encryption. This method should prompt 
    for the plaintext and the key as integers, call the encryption method, and then output the ciphertext.
'''

import binascii
from textwrap import wrap

def encrypt(plaintext, key):
    
    plaintext = bin(plaintext)[2:]
    while (len(plaintext) < 12): plaintext = "0" + plaintext

    key = bin(key)[2:]
    while (len(key) < 9): key = "0" + key

    print("\nPlaintext: {0} ({1})".format(plaintext, int(plaintext,2)))
    print("\nKey: {0} ({1})".format(key,int(key,2)))
    
    # First make sure arguments are without bounds
    if len(plaintext) not in range(0, 4096) or len(key) not in range(0, 512):
        print("Invalid lengths.")
        return
    
    # Identify the s-boxes
    s1 =    [
                ["101", "010", "001", "110", "011", "100", "111", "000"],
                ["001", "100", "110", "010", "000", "111", "101", "011"] 
            ]
    s2 =    [
                ["100", "000", "110", "101", "111", "001", "011", "010"],
                ["101", "011", "000", "111", "110", "010", "001", "100"]
            ]
    
    # Separate plaintext into 12-bit blocks
    blocks = wrap(plaintext,12)
    
    # Pad last block with 0s
    blocks[-1] = blocks[-1].ljust(12,"0")[:12]
    
    # Generate subkeys from key
    long_key = key * 2
    subkeys = [long_key[0:8], long_key[1:9], long_key[2:10], long_key[3:11]]
    print("\nSubkeys: {}".format(subkeys))
    
    print("\nBlocks: {0}".format(blocks))
    
    # Create ciphertext
    ciphertext = ""
    
    # For each block...
    for i in range(0,len(blocks)):
        block = blocks[i]
        
        # Split block into left and right
        l, r = block[:len(block)//2], block[len(block)//2:]
        print("\nBlock {0}\nLeft: {1} ({2})\nRight: {3} ({4})".format(i,l,int(l,2),r,int(r,2)))
        
        # 4 rounds for simplified version
        for j in range (0,4):
            
            # Copy previous left and right
            l_old = l
            
            # Get appropriate key
            k = subkeys[j]
            
            # Assign next l to current r
            l = r
            
            # Perform f on r
        
            # First expand the r
            r = expand(r)
            
            # XOR k (keys[i]) with r
            r = xor(r,k,8)
            
            # Split bits and prepare for s-boxes
            r1, r2 = r[:len(r)//2], r[len(r)//2:] 
            print("r1: " + r1)
            print("r2: " + r2)
            
            s1row = int(r1[0])
            s1col = int(r1[1:],2)
            print("S1 row: {0}, S1 col: {1}".format(s1row,s1col))
    
            s2row = int(r2[0])
            s2col = int(r2[1:],2)
            print("S2 row: {0}, S2 col: {1}".format(s2row,s2col))
            
            sbox1_choice = s1[s1row][s1col]
            sbox2_choice = s2[s2row][s2col]
            print("S1 choice: {0}, S2 choice: {1}".format(sbox1_choice,sbox2_choice))
            
            #Output of function f is those 6 bits
            f = sbox1_choice + sbox2_choice
            
            # To get the new r, we need to xor f with the previous l
            r = xor(l_old,f,6)
            print("L: {0}, R: {1}, ".format(l,r,int(subkeys[j],2)))
            print("END Block {0} - Round {1}: L = {2} ({3}), R = {4} ({5}), Subkey = {6} ({7})"                   .format(i,j,l,int(l,2),r,int(r,2),subkeys[j],int(subkeys[j],2)))
            
            print("\n")
            
        # Add blocks to ciphertext
        ciphertext += l + r
    
    print("Final ciphertext: " + ciphertext)
    if len(ciphertext) == 0: return 0
    else: ciphertext = int(ciphertext, 2)
        
    # Return int ciphertext
    # print("\nCiphertext: {0}".format(ciphertext))
    return ciphertext
        
# Helper function to use as E for expansion from 6 bits to 8
def expand(s):
    result = s[0] + s[1] + s[3] + s[2] + s[3] + s[2] + s[4] + s[5]
    print(s + " expanded to " + result)
    return result

# Helper function to xor two bit strings
def xor(s1, s2, n):
    n1 = int(s1,2)
    n2 = int(s2,2)
    result = bin(n1^n2)[2:]
    
    # If result is not n bits, we must 0 append to beginning of result
    nZeros = n-len(result)
    zs = "0" * nZeros
    result = zs + result
    
    print(s1 + " XOR " +  s2 + " = " + result)
    return result
    


# In[253]:


pt = input("Please enter plaintext: ")
k = input("Please enter key: ")
if (pt.isdigit() and k.isdigit()): 
    n = encrypt(int(pt), int(k))
    print("\nReturn value: " + str(n))
else: 
    print("Either your plaintext or key was not a deimal number. Please try again .")


# In[ ]:





# In[ ]:




