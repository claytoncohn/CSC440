#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Clayton Cohn
CSC440 - 810
Prof. John Rogers
16 March 2020
'''

'''
Breaking Vigenére with a crib (5 points). 

You are given the ciphertext below that you know to be the result of 
applying the Vigenére cipher with a key of no more than 12 letters. 

You suspect that the crib word "think" occurs in the first 25 letters. Use that to break it.
'''

ciphertext = "XHUXMKSAMMERSQYSVHDALZCRBSOLRTJMGWLZTBYWHHRRUMITFGTIPQVXUOPBMWIFEESWIEWWBRLEESA" +              "PLHNSGFJVLJQAVWFHHVVLVZEVLVTAVFJITPCXICYEMTSTTBYHWLQFCLWQHZSBVWKHPVRIDOGJLRGHKE" +              "SJWHAMTHVNEVWOGASWSLKTDZSGPRXXZBSSKHGVRXRVVGWUHXVRGDZAPGKSSICVKLZJDWFHVRVKLVXCV" +              "SGHXVAFINEMOXUXVSDQEVAHIOEKWLQDOTZTASTDUAEFMQIHGZEOMCKZWRORFQVLJSDGTJEESLKTDZSG" +              "PLRKLIWGGCQZIIKLLEVSHIOITALDPFWFIOIGTYAZBLVTTSITPVEWEOILMJWPANCFJXJXZDUQYAQSPYP" +              "ZTZBDHMRNVJKWLAFPBSRAMJWHZPRABIOMJQLTTSXOCKQRXUBLWFSSPXWDYULBQMTHVJ"

# Create function based on above pseudocode to determine (likely) length of Vigenère key.
def getKeyLength(ciphertext):
    for i in range(1,15):
        shifted = ciphertext[-i:] + ciphertext[:-i]
        counter = 0
        for j in range(0, len(ciphertext)):
            if shifted[j] == ciphertext[j]:
                counter += 1
        
        print("Shift: {0}, Coinc: {1}\n".format(i, counter))
        
getKeyLength(ciphertext)

'''
Based on the above code (derived from provided pseudocode), the shift with the most
coincidences is 11, which has 42 coincidences. That means that the likely length of the
Vigenère key from the provided ciphertext is 11.
''' 


# In[2]:


# Now that we know the key length is 11, let's implement our getKey method from Assignment2:

def getKey(ciphertext, n):
    
    # Create placeholder for the key of length n
    key = ""
    
    # English language letter distribution
    A = [.082, .015, .028, .043, .127, .022, .020, .061, .070, .002,
        .008, .040, .024, .067, .075, .019, .001, .060, .063, .091,
        .028, .010, .023, .001, .020, .001]
    
    # For each part of the key
    for i in range(n):
        
        # First create array of every n character
        chars = []
        for j in range(len(ciphertext)):
            if j % n == i:
                chars.append(ciphertext[j])
                
        # For each i, get the character distributions
        V = [0] * 26
        for j in range(len(chars)):
            V[ord(chars[j]) - ord('A')] += 1
        
        # Convert each distribution to a percentage
        W = [0] * 26
        for j in range(len(V)):
            W[j] = round(V[j] / len(chars), 4)
        
        # Find largest value j for W * Aj
        sums = [0] * 26
        for j in range(26):
            Aj = A[-j:] + A[:-j]
            total = 0
            for k in range(len(W)):
                total += W[k] * Aj[k]
            sums[j] = round(total, 3)
            
        # Find max of sums and convert index to char    
        index = sums.index(max(sums))
        letter = chr(ord('A') + index)
        key += letter
        
    return key
                        
key = getKey(ciphertext, 11)
key


# In[3]:


# And then to decrypt with the key
def vigenere_decrypt(ciphertext, key):
    n = len(key)
    key_int = [ord(i) - ord('A') for i in key]
    ciphertext_int = [ord(i) - ord('A') for i in ciphertext]
    plaintext = ""
    
    for i in range(len(ciphertext)):
        val = (ciphertext_int[i] - key_int[i % n]) % 26
        char = chr(val + ord('A'))
        plaintext += char
    
    return plaintext

plaintext = vigenere_decrypt(ciphertext, key)
print(plaintext)


# In[4]:


'''
RSA encryption and signature (15 points) 

In this problem, you are going to send me a digitally signed message using RSA with a 128-bit modulus 
for both the signature and the encryption. 

Generate your own RSA keys. 

To generate the signature, consult the procedure on page 245. 
'''

'''
1.  Create a plaintext m that is your student id number multiplied by the height of the highest point in Wisconsin. 
    Finding that height was supposed to be a little diversion from the work of the final. 
    That apparently failed so here's the value: 1951.

'''
height = 1951
dpu_id = 1198780
m = 1951 * 1198780
m


# In[5]:


'''
2.  Create your own RSA keys nA and eA with the modulus containing no more than 127 bits. 
    This will guarantee that values encrypted with these keys are no more than 127 bits in length. 
    Note that this is a slight change from the 128 bits stated in the exam.
'''

# p and q generated randomly from website: https://asecuritysite.com/encryption/random3?val=8

p = 496870560775040327                         # 59 bits
q = 16477733467337812643                       # 64 bits
n = 8187300668217788611846832210295454261      # 123 bits
    
phi_n = 8187300668217788594872228182182601292  # (p-1) * (q-1)
        
# e must be in between 1 and phi(n), and also must be coprime with phi(n)
e = 3


# In[6]:


# Check that phi_n % e != 0
phi_n % e


# In[7]:


# Calculate our d value to create the signature
d = (2*phi_n + 1) // e
d 


# In[8]:


'''
3.  Create a digital signature from m called s.

    s = m^d mod n
'''

s = pow(m,d,n)
s


# In[9]:


'''
Using the variable names from that procedure, your message m is your seven-digit DePaul id number 
multiplied by the height in feet of the highest point in Wisconsin. 

Let cm denote the encrypted message and cs the encrypted signature, both encrypted using my public keys.

My public keys are the following:

n = 433101827453818529674861602460176423853
e = 34258983635230832483
'''
n_bob = 433101827453818529674861602460176423853
e_bob = 34258983635230832483


# In[10]:


'''
4.  Encrypt m for transmission to me (Bob). This is the value cm.
'''
cm = pow(m,e_bob,n_bob)
cm


# In[11]:


'''
5.  Encrypt s for transmission to me (Bob). This is the value cs.
'''
cs = pow(s,e_bob,n_bob)
cs


# In[12]:


'''
6.  Send me the block described in the exam, which contains nA, eA, cm, and cs.

=RSA=
Cohn, Clayton
n 8187300668217788611846832210295454261
e 3
cm 250321993341100643804362776828247673629
cs 141993753745530359302700541300342466938
'''


# In[13]:


'''
Meet in the middle attack (10 points) 

You have a known 12-bit plaintext 1660 (011001111100) and a 12-bit ciphertext 2509 (100111001101). 

You know that the system used was a double encipherment where the first stage used the simple DES 
from the book and the second stage used a right bit-rotation shift. 

There are 512 possible DES keys and 12 possible rotation shifts. Using a meet-in-the-middle attack, 
determine the 9-bit DES key and the shift that were used, stated in a block as follows:
'''
pt = 1660
ct = 2509


# In[14]:


# Using my encrypt method from Assignment 4

import binascii
from textwrap import wrap

def encrypt(plaintext, key):
    
    plaintext = bin(plaintext)[2:]
    while (len(plaintext) < 12): plaintext = "0" + plaintext

    key = bin(key)[2:]
    while (len(key) < 9): key = "0" + key

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

    # Create ciphertext
    ciphertext = ""
    
    # For each block...
    for i in range(0,len(blocks)):
        block = blocks[i]
        
        # Split block into left and right
        l, r = block[:len(block)//2], block[len(block)//2:]
        
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
            
            s1row = int(r1[0])
            s1col = int(r1[1:],2)
    
            s2row = int(r2[0])
            s2col = int(r2[1:],2)
            
            sbox1_choice = s1[s1row][s1col]
            sbox2_choice = s2[s2row][s2col]
            
            #Output of function f is those 6 bits
            f = sbox1_choice + sbox2_choice
            
            # To get the new r, we need to xor f with the previous l
            r = xor(l_old,f,6)
                        
        # Add blocks to ciphertext
        ciphertext += l + r
    
    if len(ciphertext) == 0: return 0
    else: ciphertext = int(ciphertext, 2)
        
    # Return int ciphertext
    # print("\nCiphertext: {0}".format(ciphertext))
    return ciphertext
        
# Helper function to use as E for expansion from 6 bits to 8
def expand(s):
    result = s[0] + s[1] + s[3] + s[2] + s[3] + s[2] + s[4] + s[5]
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
    
    return result


# In[15]:


# We will start by encrypting the plaintext with all possible keys:

des_key_pairs = {}
for i in range(512):
    des_key_pairs.update({ encrypt(pt,i) : i })


# In[16]:


from itertools import islice
print({k:v for (k,v) in [d for d in des_key_pairs.items()][:50]})


# In[17]:


# We will employ a shift_left function to "decrypt" the shift right used to encipher it
def shift_left(text,n):
    text = bin(text)[2:]
    while len(text) < 12:
        text = "0" + text
    return int(text[n:] + text[:n],2)


# In[18]:


# Now we will decrypt the ciphertext with all possible keys
shift_right_key_pairs = {}
for i in range(12):
    shift_right_key_pairs.update({ shift_left(ct,i) : i })


# In[19]:


print({k:v for (k,v) in [d for d in shift_right_key_pairs.items()]})


# In[20]:


# Cross reference lists to find candidates
candidates = []

for key in shift_right_key_pairs.keys():
    if key in des_key_pairs:
        candidates.append((des_key_pairs[key], shift_right_key_pairs[key]))


# In[21]:


for t in candidates:
    a, b = t
    print(str(a) + ", " + str(b))


# In[22]:


# Add the right shift and des decrypt for testing
def shift_right(text,n):
    text = int(text)
    text_b = bin(text)[2:]
    while len(text_b) < 12:
        text_b = "0" + text_b
    rotated_text = text_b[-n:] + text_b[:-n]
    return int(rotated_text,2)


# In[23]:


# We have 4 candidates, now we will test them via the encryption
plaintext = input("Please enter plaintext: ")
k = input("Please enter des key: ")
if (plaintext.isdigit() and k.isdigit()): 
    middle = encrypt(int(plaintext), int(k))
    print("middle: ",middle)
    k = int(input("Please enter shift right key: "))
    n = shift_right(middle,k)
    print("Return value: " + str(n))
else: 
    print("Either your plaintext or key was not a deimal number. Please try again .")


# In[24]:


# Using decrypt from assignment 5 to make sure everything works
def decrypt(ciphertext,key):
    
    ciphertext = bin(ciphertext)[2:]
    while (len(ciphertext) < 12): ciphertext = "0" + ciphertext

    key = bin(key)[2:]
    while (len(key) < 9): key = "0" + key
    
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
    
    # Create plaintext
    plaintext = ""
    
    # For each block...
    for i in range(len(blocks) - 1, -1, -1):
        block = blocks[i]
        
        # Split block into left and right
        l, r = block[:len(block)//2], block[len(block)//2:]
        
        # 4 rounds for simplified version
        for j in range(3,-1,-1):
            
            # 1. Next r = current l
            next_r = l
            
            # 2. v = expand(next_r) ^ subkeys[i]
            next_r_expanded = expand(next_r)
            v = xor(next_r_expanded,subkeys[j],8)
    
            # Split bits and prepare for s-boxes
            r1, r2 = v[:len(v)//2], v[len(v)//2:] 
            
            s1row = int(r1[0])
            s1col = int(r1[1:],2)
    
            s2row = int(r2[0])
            s2col = int(r2[1:],2)
            
            sbox1_choice = s1[s1row][s1col]
            sbox2_choice = s2[s2row][s2col]
            
            #Output of function f is those 6 bits
            f = sbox1_choice + sbox2_choice
            
            # To get the new l, we need to xor f with the previous r
            l = xor(r,f,6)
            
            # Set r = next_r
            r = next_r
                        
        # Prepend blocks to plaintext
        plaintext = l + r + plaintext
    
    if len(plaintext) == 0: return 0
    else: plaintext = int(plaintext, 2)
        
    # Return int plaintext
    return plaintext


# In[25]:


# Run the decryption
ciphertext = input("Please enter ciphertext: ")
k = input("Please enter shift right key: ")
if (ciphertext.isdigit() and k.isdigit()): 
    middle = int(shift_left(int(ciphertext),int(k)))
    print("middle: ",middle)
    k = int(input("Please enter des key: "))
    n = int(decrypt(int(middle),int(k)))
    print("Return value: " + str(n))
else: 
    print("Either your plaintext or key was not a deimal number. Please try again .")


# In[26]:


'''
=MITM=
Cohn, Clayton
DESkey [152,49,315,271]g
Shift [0,1,5,11]
'''


# In[27]:


'''
The ElGamal ciphersystem (10 points) 

Using the ElGamal keys I supply below, encrypt your 7-digit student id number and provide the ciphertext. 

Recall that the ElGamal system works as follows, where Alice (you) wish to send a message (your id) to Bob (me):

    Bob chooses a large prime p and an integer α less than p (which should be a primitive element), 
    a secret integer a and then he computes β=αa mod p.
    
    Alice chooses a random integer k and computes y1=αk mod p, y2=xβk mod p, where x is her message.
    
    She sends these y values to Bob.

    Bob then uses his secret information to decrypt.

My public keys are:

p = 1416545561
α = 512170907
β = 331036412
'''

p = 1416545561
alpha = 512170907
beta = 331036412

m = 1198780


# In[28]:


# Alice chooses a random integer k
k = 31


# In[29]:


# Alice computes y1 = α^k mod p
y1 = pow(alpha,k,p)
y1


# In[30]:


# Alice computes y2 = (x^β)*k mod p, where x is her message
y2 = (pow(beta,k)*m) % p
y2


# In[31]:


'''
Provide your answers in a block of text with the format:
=ElGamal=
Cohn, Clayton
y1 106137901
y2 1297605993
'''

