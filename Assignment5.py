#!/usr/bin/env python
# coding: utf-8

# In[63]:


'''
Clayton Cohn
20200228
CSC440
Assignment 5

75 points

'''

'''
1. (50 points) Meet in the middle attack on 2DES Implement the meet-in-the-middle attack on 2DES, 
where you use the simplified DES from the textbook. Follow the instructions on pp. 143-144. 
Because you're using the simplifed DES, which has a key containing 9 bits, you will need to generate two lists, 
each of length 512.

You should have the DES encryption function implemented in assignment 4 and you will now need to implement the 
decryption function. Write the program so that it outputs a list of possible key pairs. Here are two sets of inputs 
on which to test your program:

Plaintext: 101, ciphertext: 199
Plaintext: 110, ciphertext: 2816

Each of those inputs will produce a list of about 50 possible key pairs Write your program so that constructs lists 
of key pairs for each input and then finds and prints the key pair(s) that appear on both lists.
'''

# Using my encrypt method from Assignment 4

import binascii
from textwrap import wrap

def encrypt(plaintext, key):
    
    plaintext = bin(plaintext)[2:]
    while (len(plaintext) < 12): plaintext = "0" + plaintext

    key = bin(key)[2:]
    while (len(key) < 9): key = "0" + key

#     print("\nPlaintext: {0} ({1})".format(plaintext, int(plaintext,2)))
#     print("\nKey: {0} ({1})".format(key,int(key,2)))
    
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
#     print("\nSubkeys: {}".format(subkeys))
    
#     print("\nBlocks: {0}".format(blocks))
    
    # Create ciphertext
    ciphertext = ""
    
    # For each block...
    for i in range(0,len(blocks)):
        block = blocks[i]
        
        # Split block into left and right
        l, r = block[:len(block)//2], block[len(block)//2:]
#         print("\nBlock {0}\nLeft: {1} ({2})\nRight: {3} ({4})".format(i,l,int(l,2),r,int(r,2)))
        
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
#             print("r1: " + r1)
#             print("r2: " + r2)
            
            s1row = int(r1[0])
            s1col = int(r1[1:],2)
#             print("S1 row: {0}, S1 col: {1}".format(s1row,s1col))
    
            s2row = int(r2[0])
            s2col = int(r2[1:],2)
#             print("S2 row: {0}, S2 col: {1}".format(s2row,s2col))
            
            sbox1_choice = s1[s1row][s1col]
            sbox2_choice = s2[s2row][s2col]
#             print("S1 choice: {0}, S2 choice: {1}".format(sbox1_choice,sbox2_choice))
            
            #Output of function f is those 6 bits
            f = sbox1_choice + sbox2_choice
            
            # To get the new r, we need to xor f with the previous l
            r = xor(l_old,f,6)
#             print("L: {0}, R: {1}, ".format(l,r,int(subkeys[j],2)))
#             print("END Block {0} - Round {1}: L = {2} ({3}), R = {4} ({5}), Subkey = {6} ({7})" \
#                   .format(i,j,l,int(l,2),r,int(r,2),subkeys[j],int(subkeys[j],2)))
            
#             print("\n")
            
        # Add blocks to ciphertext
        ciphertext += l + r
    
#     print("Final ciphertext: " + ciphertext)
    if len(ciphertext) == 0: return 0
    else: ciphertext = int(ciphertext, 2)
        
    # Return int ciphertext
    # print("\nCiphertext: {0}".format(ciphertext))
    return ciphertext
        
# Helper function to use as E for expansion from 6 bits to 8
def expand(s):
    result = s[0] + s[1] + s[3] + s[2] + s[3] + s[2] + s[4] + s[5]
#     print(s + " expanded to " + result)
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
    
#     print(s1 + " XOR " +  s2 + " = " + result)
    return result


# In[64]:


def decrypt(ciphertext,key):
    
    ciphertext = bin(ciphertext)[2:]
    while (len(ciphertext) < 12): ciphertext = "0" + ciphertext

    key = bin(key)[2:]
    while (len(key) < 9): key = "0" + key

#     print("\nCiphertext: {0} ({1})".format(ciphertext, int(ciphertext,2)))
#     print("\nKey: {0} ({1})".format(key,int(key,2)))
    
    # First make sure arguments are without bounds
    if len(ciphertext) not in range(0, 4096) or len(key) not in range(0, 512):
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
    
    # Separate ciphertext into 12-bit blocks
    blocks = wrap(ciphertext,12)
    
    # Pad last block with 0s
    blocks[-1] = blocks[-1].ljust(12,"0")[:12]
    
    # Generate subkeys from key
    long_key = key * 2
    subkeys = [long_key[0:8], long_key[1:9], long_key[2:10], long_key[3:11]]
#     print("\nSubkeys: {}".format(subkeys))
    
#     print("\nBlocks: {0}".format(blocks))
    
    # Create plaintext
    plaintext = ""
    
    # For each block...
    for i in range(len(blocks) - 1, -1, -1):
        block = blocks[i]
        
        # Split block into left and right
        l, r = block[:len(block)//2], block[len(block)//2:]
#         print("\nBlock {0}\nLeft: {1} ({2})\nRight: {3} ({4})".format(i,l,int(l,2),r,int(r,2)))
        
        # 4 rounds for simplified version
        for j in range(3,-1,-1):
#             print("subkeys[{0}]: {1}".format(j,subkeys[j]))
            
            # 1. Next r = current l
            next_r = l
            
            # 2. v = expand(next_r) ^ subkeys[i]
            next_r_expanded = expand(next_r)
            v = xor(next_r_expanded,subkeys[j],8)
#             print("v = " + next_r_expanded + " ^ " + subkeys[j] + " = " + v)
    
            # Split bits and prepare for s-boxes
            r1, r2 = v[:len(v)//2], v[len(v)//2:] 
#             print("r1: " + r1)
#             print("r2: " + r2)
            
            s1row = int(r1[0])
            s1col = int(r1[1:],2)
#             print("S1 row: {0}, S1 col: {1}".format(s1row,s1col))
    
            s2row = int(r2[0])
            s2col = int(r2[1:],2)
#             print("S2 row: {0}, S2 col: {1}".format(s2row,s2col))
            
            sbox1_choice = s1[s1row][s1col]
            sbox2_choice = s2[s2row][s2col]
#             print("S1 choice: {0}, S2 choice: {1}".format(sbox1_choice,sbox2_choice))
            
            #Output of function f is those 6 bits
            f = sbox1_choice + sbox2_choice
            
            # To get the new l, we need to xor f with the previous r
            l = xor(r,f,6)
            
            # Set r = next_r
            r = next_r
            
#             print("L: {0}, R: {1}, ".format(l,r,int(subkeys[j],2)))
#             print("END Block {0} - Round {1}: L = {2} ({3}), R = {4} ({5}), Subkey = {6} ({7})" \
#                   .format(i,j,l,int(l,2),r,int(r,2),subkeys[j],int(subkeys[j],2)))
            
#             print("\n")
            
        # Prepend blocks to plaintext
        plaintext = l + r + plaintext
    
#     print("Final plaintext: " + plaintext)
    if len(plaintext) == 0: return 0
    else: plaintext = int(plaintext, 2)
        
    # Return int plaintext
    # print("\nPlaintext: {0}".format(plaintext))
    return plaintext


# In[65]:


# Run the encryption
pt = input("Please enter plaintext: ")
k = input("Please enter key: ")
if (pt.isdigit() and k.isdigit()): 
    n = encrypt(int(pt), int(k))
    print("\nReturn value: " + str(n))
else: 
    print("Either your plaintext or key was not a deimal number. Please try again .")


# In[66]:


# Run the decryption

ct = input("Please enter ciphertext: ")
k = input("Please enter key: ")
if (ct.isdigit() and k.isdigit()): 
    n = decrypt(int(ct), int(k))
    print("\nReturn value: " + str(n))
else: 
    print("Either your ciphertext or key was not a deimal number. Please try again .")


# In[77]:


# Meet-in-the-middle attack:

def getKeys(plaintext,ciphertext):

    # The index will serve as the key
    encrypted = []
    decrypted = []
    
    candidates = []
    
    for i in range(0,512):
        
        # Get all possible ciphertexts from plaintexts and store them in an array. 
        encrypted.append(encrypt(plaintext,i))
        
        # Get all possible plaintexts from ciphertexts and store them in an array. 
        decrypted.append(decrypt(ciphertext,i))
        
    for i in range(len(encrypted)):
        for j in range(len(decrypted)):
            
            # Gather the candidate keys:
            if encrypted[i] == decrypted[j]:
                candidates.append((i,j))
                
    print("Total candidates: {0}".format(len(candidates)))
          
#     for i in range(len(candidates)):
#         print("k1: {0}, k2: {1}".format(candidates[i][0], candidates[i][1]))
        
    return candidates


# In[78]:


# Get the list of candidate keys
candidates = getKeys(101,199)


# In[92]:


# Now that we have our candidate keys, we are going to test each pair on another plaintext/ciphertext pair
def verifyKeys(key_pairs, plaintext, ciphertext):
    
    key1s, key2s = [ i for i, j in key_pairs ], [ j for i, j in key_pairs ]
    
    # Track which key pairs encrypt our plaintext to ciphertext
    candidates = []
    
    # Check all candidate pairs against new plaintext/ciphertext pair
    for i in range(len(key1s)):
        
        # perform the encrytion and compare the ciphertexts
        e1 = encrypt(plaintext,key1s[i])
        e2 = encrypt(e1,key2s[i])
        if e2 == ciphertext:
            candidates.append((key1s[i],key2s[i]))
            
    print("Verified candidates: {0}".format(len(candidates)))
    
    return candidates


# In[98]:


# Check out list of candidates against the other plaintext/ciphertext pair
verified_candidates = verifyKeys(candidates,110,2816)

# Print all possible verified candidates
for i in range(len(verified_candidates)):
    print("(K1: {0}, K2: {1})".format(verified_candidates[i][0], verified_candidates[i][1]))


# In[102]:


'''
Our meet-in-the-middle attack has landed us the keys 42 and 151 for K1 and K2, respectively.
Now let's test these on the two plaintext/ciphertext pairs that we have to make sure we have a match.

We have two pairs to test: 101/199 and 110/2816
'''
a1 = encrypt(101,42)
a2 = encrypt(a1,151) # Should be equal to 199

b1 = encrypt(110,42)
b2 = encrypt(b1,151) # Should be equal to 2816

print("encrypt_test1: {0}\nencrypt_test2: {1}".format(a2,b2))


# In[104]:


'''
Both of our tests yielded the results we were expecting.
Now let's verify with decrypt...just for fun!
'''

c1 = decrypt(199,151)
c2 = decrypt(c1,42) # Should be 101

d1 = decrypt(2816,151)
d2 = decrypt(d1,42) # Should be 110
print("decrypt_test1: {0}\ndecrypt_test2: {1}".format(c2,d2))


# In[164]:


'''
2. (25 points) Baby step, giant step attack on discrete log Implement the attack described in section 7.2.2 of 
the textbook. You will need these values:

p = 595117
alpha = 1002
alpha^x = 437083

Your program will output x, which will be an integer where each pair of digits repressents a letter in the encoding 
scheme A = 01, B = 02, ..., Z = 26. Please translate the integer to an acronym.
'''

import math
from decimal import Decimal

# We are looking for an x such that A^x === B (mod p)
def bsgs(p,A,B):
    
    # First calculate N
    N = int(math.ceil(math.sqrt(p-1)))
    
    # Compute all A ^ j for 0 <= j < N to create set of "baby steps"
    lst = [pow(A,j,p) for j in range(0,N)]
    
    # Using FML for A ^ -N = e:
    e = pow(A,N*(p-2),p)
    
    # Now we will create and check for matches in second list simultaneously (giant steps)
    for k in range(N):
        
        # Calculate B*A^(-N*K)
        val = (B*pow(e,k,p)) % p
        
        # Go until we find a match, otherwise the function will terminate with None
        if val in lst:
            return k*N + lst.index(val)
        
    return None
                
print(bsgs(595117,1002,437083))

'''
We get an x value of 141901, which separates into 14 19 01, which is the acronym: OTA
'''


# In[ ]:




