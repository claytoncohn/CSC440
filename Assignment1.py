#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Clayton Cohn
# CSC 440
# 1/8/2020

# Assignment 1

# This assignment is saved in a multiple formats, and is meant to be read either in a text editor,
# or read and run as a python3 file. The file was created originally as a Jupyter Notebook.
# I will provide all three formats (.py, .txt, .ipynb) to facilitate ease of grading.

'''
1. Assume encryption is done with the affine function 19x+12 mod 26.
  a. Encrypt the word vortex.
  
     vortex encrypts to VSXJKH
     
      19x+12  mod26    =
      
     v    411      21      V
     o    278      18      S
     r    335      23      X
     t    373      9       J
     e    88       10      K
     x    449      7       H
   
  b. What is the decryption function?
  
     = modular multiplicative inverse of 19 * (y - 12) mod26
     = 11(y-12)mod26
     
      11(y-12)  mod26    =
      
     V      99        21    v
     S      66        14    o
     X      121       17    r
     J      -33       19    t
     K      -22       4     e
     H      -55       23    x
'''


# In[ ]:


'''
2. The ciphertext HCNKR was encrypted using the affine function 5x+10 mod 26. Find the plaintext.

The equation 5x+10mod26 decrypts as follows:

= modular multiplicative inverse of 5 * (y - 10) mod26
= 21(y - 10)mod26

  =    21(y - 10)    mod26    =

H   7            -63      15    p
C   2            -168     14    o
N   13           63       11    l
K   10           0        0     a
R   17           147      17    r
'''


# In[ ]:


'''
3. The Georgian alphabet has 33 letters and we can represent them with the integer values 0 to 32. 
If we are going to encrypt a Georgian plaintext using the affine cipher, 
how many possible keys are there, that is, what is the size of the key space?

Our 'a' must have a modular multiplicative inverse, meaning that the greatest common denominator for
'a' and the length of the alphabet must be 1. So, for a 33-letter alphabet, 'a' cannot be a multiple
of any of the multiples of 33, i.e. 'a' cannot be a multiple of 11 or 3. We are left with the following:

1,2,4,5,7,8,10,13,14,16,17,19,20,23,25,26,28,29,31,32

Thus, 'a' has 20 possible values.

'b' can be any value in the range of the length of the alphabet, so in this case 'b' has 33 possible values.

The total key space is represented by the total possible 'a' values multiplied by the total possible 'b' values,
which in this case is:

    20 * 33 = 660

There are 660 possible keys using a Georgian (33-letter) alphabet.

'''


# In[ ]:


'''
4. If an alphabet has 31 letters, what is the size of the key space using the affine cipher?

Our 'a' must have a modular multiplicative inverse, meaning that the greatest common denominator for
'a' and the length of the alphabet must be 1. So, for a 31-letter alphabet, 'a' cannot be a multiple
of any of the multiples of 31. But since 31 is prime, there are no numbers excluded. As a result, we 
are left with all numbers 1 through 30, for a total of 30 possible 'a' values.

'b' can be any value in the range of the length of the alphabet, so in this case 'b' has 31 possible values.

The total key space is represented by the total possible 'a' values multiplied by the total possible 'b' values,
which in this case is:

    30 * 31 = 930

There are 930 possible keys using a 31-letter alphabet.
'''


# In[23]:


# 5. Solve Computer Problem 1 on p. 59. I recommend writing a program but that's not necessary.

'''
5. The following ciphertext was encrypted by a shift cipher:

ycvejqwvhqtdtwvwu

Decrypt.

The answer (using the code I provided below) is "watchoutforbrutus".
This was decrypted with a shift equal to 24.
'''

# Brute force better than frequency count for shift ciphers (Trappe 14)
word = 'ycvejqwvhqtdtwvwu'
vector = [ord(x) - ord('a') for x in list(word)]
res = '';
for k in range(26):
    for c in vector:
        res += chr(((c + k) % 26) + ord('a'))
    print("Shift {0}: {1}".format(k, res))
    res = ''    


# In[51]:


'''
6. Solve Computer Problem 6 on p. 60. You may write a program for part (a) 
but you must write a program for part (b). The program may be in the "usual" languages, 
that is, C++, Java, or Python. Other languages may be used with permission.
'''

'''
6. In this problem you are to get your hands dirty doing some programming. 
Write some code that creates a new alphabet {A, C, G, T}. For example,
this alphabet could correspond to the four nucleotides adenine, cytosine,
guanine, and thymine, which are the basic building blocks of DNA and RNA codes.
Associate the letters A, C, G, T with the numbers 0, 1, 2, 3, respectively. 

    (a) Using the shift cipher with a shift of 1, encrypt the following sequence 
    of nucleotides, which is taken from the beginning of the thirteenth human
    chromosome:
    
    GAATTCGCGGCCGCAATTAACCCTCACTAAAGGGATCTCTAGAACT
    
    (b) Write a program that performs affine ciphers on the nucleotide alphabet.
    What restrictions are there on the affine cipher?
'''

# Create the new alphabet in the form of a dictionary
alphabet = {
            "A": 0, 
            "C": 1, 
            "G": 2, 
            "T": 3 
           }

# Create a dictionary of inverted key-value pairs from our alphabet
# We do this to access the letter via number value later on
inv_alphabet = dict(zip(alphabet.values(),alphabet.keys()))


# 6a.
letters = 'GAATTCGCGGCCGCAATTAACCCTCACTAAAGGGATCTCTAGAACT'
shift = 1
    
def encrypt_letters(letters, shift):
    '''
    Function takes each letter in letters parameter and obtains its numerical value,
    applies the shift, obtains the encrypted letter (mod26), and appends the ciphertext
    to the result string. After all letters are encrypted, function returns result string.
    '''
    result = ''
    for letter in letters:
        result += inv_alphabet[(alphabet[letter] + shift) % len(alphabet)]
    return result
    
def decrypt_letters(letters, shift):
    '''
    Function takes each letter in letters parameter and obtains its numerical value,
    applies the shift (subtracts), obtains the decrypted letter (mod26), and appends 
    plaintext to the result string. After all letters decrypted, function returns result string.
    '''
    result = ''
    for letter in letters:
        result += inv_alphabet[(alphabet[letter] - shift) % len(alphabet)]
    return result

result = encrypt_letters(letters, shift)

print("Encrypted: {0}".format(result))
print("Decrypted: {0}".format(decrypt_letters(result, shift)))

# 6b.

# Function to calculate GCD between 2 numbers
def gcd(x, y):
    if x > y:
        lt = y
    else:
        lt = x
    for i in range(1, lt + 1):
        if((x % i == 0) and (y % i == 0)):
            gcd = i 
    return gcd

# Function to get modular multiplicative inverse
def inverse(a) : 
    a = a % len(alphabet); 
    for x in range(1, len(alphabet)): 
        if ((a * x) % len(alphabet) == 1) : 
            return x 
    return 1

def encrypt_affine(letters, a, b):
    '''
    Function first checks that affine cipher is possible by making sure that 
    the greatest common denominator between the length of the alphabet and the
    chosen 'a' value is equal to 1.
    
    Then, function takes each letter in letters parameter and obtains its numerical value,
    applies the affine function (ax + b), obtains the encrypted letter (mod26), and appends the
    ciphertext to the result string. After all letters encrypted, function returns result string.
    '''
    if (gcd(a, len(alphabet)) != 1):
        print('Cannot get inverse of {0}'.format(a))
        return
    result = ''
    for letter in letters:
        result += inv_alphabet[(a*alphabet[letter] + b) % len(alphabet)]
    return result

def decrypt_affine(letters, a, b):
    '''
    Function first checks that affine cipher (decryption) is possible by making sure that 
    the greatest common denominator between the length of the alphabet and the
    chosen 'a' value is equal to 1.
    
    Then, function takes each letter in letters parameter and obtains its numerical value,
    applies the affine decryption function (inv*(y-b)), obtains the decrypted letter (mod26), 
    and appends the plaintext to the result string. After all letters decrypted, function 
    returns result string.
    '''
    if (gcd(a, len(alphabet)) != 1):
        print('Cannot get inverse of {0}'.format(a))
        return
    result = ''
    for letter in letters:
        i = inverse(a)
        y = alphabet[letter]
        x = (i*(y-b)) % len(alphabet)
        result += inv_alphabet[x]
    return result

result = encrypt_affine(letters, 3, 2)

print("Encrypted (affine): {0}".format(result))
print("Decrypted (affine): {0}".format(decrypt_affine(result, 3, 2)))

'''
The restrictions on the affine cypher means that there must be a modular 
multiplicative inverse of a. So, the greatest common denominator between a
and the length of the alphabet (4, in this case) must be 1. That means that 
for this problem, a can only equal 1 or 3. 
'''


# In[64]:


'''
The next two problems are based on this Vigenère ciphertext.

QHDLXNQLYNGAIGWBCERJFEARNIBKXUSVGZXKYNPXXTKGAATZRQCRFYIDCCLYXHUQXEIXFAFGEAMMAL
YRGAYXQMTGACDJSYRTLEXUVRVIYFFEGXFKOYSPHGBBYTRESOXUNTXXAKLUAWYDINAAWCZWIFVMCROI
UCEIFJYDJAYZJBEOTMUSGAGAYYQNIPTFPYMCBOYDYYSVGWDOJTBZLMFBYJXLQCUDRRIGMIUYWMQUUF
RPCZQHTVJOUJSMNRVQQZEJYLACNHRFCPTFENZYEJCLYMBQUCGUMYQDBUAWLQTMOAXCZJBEABHQJYEA
MQQDNIRLNTUINRMCYUJAQTZQMGOEXUDEONQPIDBXWNKNIEUNQMBQDUFGXLFXYBVKNTEZCBFJGJUTVH
HMBWOZIFQNCTLMBQELYVGNTUHIAXNQUHSROYZJCEFUIACVOBFVAEGBBHGNEIMOHIYRIOZQ

7. Write a program based on the following pseudocode to determine the likely length 
of the key used to create the above ciphertext. This is the technique described in section 2.3.1.

for shift = 1 to 14 do
  coincidenceCount = 0
  for index = 0 to ciphertext length - 1 do
    shiftedIndex = (index + shift) % ciphertext length
    if ciphertext[index] == ciphertext[shiftedIndex] then
      coincidenceCount++;
  print shift, coincidenceCount
  
8. Please break the above ciphertext using an online resource to help. 
There are some sites that, given the ciphertext, determine the key word 
and provide the plaintext. Format the plaintext by adding word spaces and punctuation.
'''

# 7. 

ciphertext = "QHDLXNQLYNGAIGWBCERJFEARNIBKXUSVGZXKYNPXXTKGAATZRQCRFYIDCCLYXHUQXEIXFAFGEAMMAL" +              "YRGAYXQMTGACDJSYRTLEXUVRVIYFFEGXFKOYSPHGBBYTRESOXUNTXXAKLUAWYDINAAWCZWIFVMCROI" +              "UCEIFJYDJAYZJBEOTMUSGAGAYYQNIPTFPYMCBOYDYYSVGWDOJTBZLMFBYJXLQCUDRRIGMIUYWMQUUF" +              "RPCZQHTVJOUJSMNRVQQZEJYLACNHRFCPTFENZYEJCLYMBQUCGUMYQDBUAWLQTMOAXCZJBEABHQJYEA" +              "MQQDNIRLNTUINRMCYUJAQTZQMGOEXUDEONQPIDBXWNKNIEUNQMBQDUFGXLFXYBVKNTEZCBFJGJUTVH" +              "HMBWOZIFQNCTLMBQELYVGNTUHIAXNQUHSROYZJCEFUIACVOBFVAEGBBHGNEIMOHIYRIOZQ"

# Create function based on above pseudocode to determine (likely) length of Vigenère key.
def getKeyLength(ciphertext):
    max_shift = -1
    max_coinc = -1
    
    for shift in range(1,15):
        coinc_count = 0
        for i in range(len(ciphertext)):
            shifted_index = (i + shift) % len(ciphertext)
            if ciphertext[i] == ciphertext[shifted_index]:
                coinc_count += 1
        print("Shift: {0}, Coincidences: {1}".format(shift, coinc_count))
        if coinc_count > max_coinc:
            max_shift = shift;
            max_coinc = coinc_count
         
    return (max_shift, max_coinc)

v_shift, v_coinc_count = getKeyLength(ciphertext)
print("v_shift: {0}, v_coinc_count: {1}".format(v_shift, v_coinc_count))

'''
Based on the above code (derived from provided pseudocode), the shift with the most
coincidences is 7, which has 41 coincidences. That means that the likely length of the
Vigenère key from the provided ciphertext is 7.
'''

#8.

'''
For this problem I used the website: https://www.dcode.fr/vigenere-cipher.
Inputing the ciphertext (along with the likely key length of 7 derived from #7), 
yielded the following plaintext (via the key word "QUANTUM"):

ANDYETEVENTHOUGHCRYPTOGRAPHYHASINFLUENCEDHUMANAFFAIRSFORMILLENIADEVELOPMENTSOVERTHELAST
THIRTYYEARSHAVECOMPLETELYYESCOMPLETELYCHANGEDOURUNDERSTANDINGOFITIFYOUPLOTTEDWHENTHEBASIC
MATHEMATICALDISCOVERIESINCRYPTOGRAPHYWEREMADEYOUWOULDSEEAFEWINANTIQUITYMAYBEAFEWFROMTHE
MIDDLEAGESTILLTHEEIGHTEENHUNDREDSONEINTHENINETEENTWENTIESTHEONETIMEPADAFEWMOREAROUNDWORLD
WARTWOANDTHENAFTERTHEBIRTHOFCOMPUTATIONALCOMPLEXITYTHEORYINTHENINETEENSEVENTIESBOOMBOOMBOOM
BOOMBOOMBOOMBOOMX

Which, when formatted with spaces and punctuation, yielded:

And yet even though cryptography has influenced human affairs for millenia, developments over
the last thirty years have completely (yes, completely) changed our understanding of it. If
you plotted when the basic mathematical discoveries in cryptography were made, you would see
a few in antiquity, maybe a few from the Middle Ages 'till the eighteen hundreds, one in the 
nineteen twenties (the one-time pad), a few more around World War Two, and then after the birth
of compuational complexity theory in the nineteen seventies: BOOM BOOM BOOM BOOM BOOM BOOM BOOM X.
'''



