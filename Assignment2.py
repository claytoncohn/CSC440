#!/usr/bin/env python
# coding: utf-8

# In[61]:


'''
Clayton Cohn
CSC 440
Assignment 2
WQ 2020
'''

'''
1. (10 points) Breaking the affine cipher using a known plaintext attack: 
    
    You've intercepted the ciphertext 'DEJXDIJYZ'. 
    
    By bribing somebody you were able to find out that the first and second 
    letters of the corresponding plaintext are 'sn'.

    a.  Using the crib, find the encryption key, that is, determine a and b so 
        that ax+b=y (mod 26) encrypts 'sn' as 'DE', that is, when x=18 
        (the letter 's'), y=3 (D) and when x=13 (the letter 'n'), y=4 (E).
        
        Knowing that the encryption formula for an affine cipher is ax + b = y(mod26),
        and that 's' and 'n' encipher to 'D' and 'E', respectively, we get
        the following linear system of equations:
        
        18a + b = 3
        13a + b = 4
        
        Solving this system via subtraction yields 5 and 17 for 'a' and 'b',
        respectively, yielding an encryption function of:
        
        5x + 17 = y(mod26)
        a = 5, b = 17

    b.  Using the decryption formula a-1(y+(-b))=x (mod 26), determine the 
        corresponding decryption key for the encryption key you found in (a).

        The modular (26) multiplicative inverse of 5 is 21, so we get:
        
        21(y-17) = x(mod26)
        
        Refactoring to put b in between 0 and 25 as specified in the directions
        gives us:
        
        21(y+9) = x(mod26)
        a-1 = 21, -b = 9

    c.  Apply that decryption key to find the original plaintext for 'DEJXDIJYZ'.

        Applying the above decryption key to our ciphertext yields:
        
        SNOWSTORM
        
Your answer will consist of values for a, b, a-1, and -b, 
all expressed as values between 0 and 25 inclusive, and the plaintext 
word in letters.
'''


# In[62]:


'''
(5 points) 2. Exercise 6, page 55

Suppose you encrypt an affine cipher, then encrypt the encryption using 
another affine cipher (both are working mod 26). Is there any advantage?

The answer is no, there is no advantage to doing this. The affine cipher
is a monoalphabetic substitution cipher, meaning that every plaintext character
maps to one and only one ciphertext character, and vice versa. Most importantly,
every 'a' in plaintext will have the same representation in ciphertext, which
of course holds true for the entire alphabet. 

Therefore, regardless of how many times you encrypt the ciphertext, it will always be 
vulnerable to frequency analysis, and thus just as easily cracked as if
it had only been run through the cipher once. There is still only one 'a'
value, and one 'b' value in the encryption key.
'''


# In[63]:


'''
(10 points) 3. Hill cipher encryption Given the Hill encryption matrix

M = | 4  7 | 
    | 5 11 |

Please do the following:

    a.  Encrypt the plaintext "winter". Your answer is the ciphertext 
        containing six uppercase letters.
        
        Since 'n' = 2, we break down winter into 3 vectors of size 2.
        We then multiple each vector below by the key above to get the
        ciphertext (mod26): 
        
        'wi' =|4 7 | |22| = |144| = |14|
              |5 11|.|8 |   |198|   |16|


        'nt' =|4 7 | |13| = |185| = |3 |
              |5 11|.|19|   |274|   |14|


        'er' =|4 7 | |4 | = |135| = |5 |
              |5 11|.|17|   |207|   |25|
              
              14 16 3 14 5 25
              O  Q  D O  F Z
              
    b.  Calculate and write down the decryption matrix for the above 
        encryption matrix.
        
        The decryption matrix is calculated by getting the determinant
        of our key M such that:
        
        gcd(det(M), 26) = 1
        
        We need a decryption matrix N such that MN === I mod26, where 
        i == the n x n identity matrix. We solve for the determinant,
        and finally the inverse of M (N) mod26: 
        
        det(A) = 4 * 11 - 7 * 5 = 9
        
        N = 1/9 |11 -7| = 3 |11 -7| = |33 -21| = |7  5 |
                |-5  4|     |-5  4|   |-15 12|   |11 12|
                
        Decrypting our ciphertext 'OQDOFZ' we get:
              
        'OQ' =|7  5 | |14| = |178| = |22|
              |11 12|.|16|   |346|   |8|


        'DO' =|7  5 | |3 | = |91 | = |13|
              |11 12|.|14|   |201|   |19|


        'FZ' =|7  5 | |5 | = |160| = |4 |
              |11 12|.|25|   |355|   |17|
              
              22 8 13 19 4 17
              w  i n  t  e r

        So, our decryption worked using the below matrix:
        
        |7  5 |
        |11 12|
'''


# In[64]:


'''
(20 points) 4. Vigenère ciphertext break. The following ciphertext 
was created using the Vigenère cipher from an English plaintext.

    a.  First, determine the estimated key length using the technique from 
        assignment 1 and explained in the textbook on p 19.
        
        To determine the key length, I have created a simple function,
        getKeyLength, and outlined it below. Using this function, 
        the key length for this ciphertet is most likely:
        
        Shift 6 yielded 140 coincidences, and shift 12 yielded 178 
        coincidences. No other shifts (range 1 to 15) scored over 100
        coincidences. We must therefore investigate both shifts, 6 and 12.
        After completing the following step, we discover that the actual
        key length is 6.

    b.  Next, use the technique described in section 2.3.3 (pp. 23-24) to 
        find the key. You might want to write a program for this.
        
        Using the technique in 2.3.3, I have created a function, findKey,
        which is implemented below. Using this function, and after trying 
        both key lengths 6 and 12, we discover that the keys are, respectively:
        
        DARWIN, DARWINDARWIN
        
        So, it's safe to say that our key length is 6, and our key is DARWIN.

    c.  Finally, provide the plaintext.
    
        To obtain the plaintext, I have created a function, vigenere_decrypt,
        which is implemented below. Utilizing the function, we get the following
        plaintext:
        
        INTRODUCTIONWHENONBOARDHMSBEAGLEASNATURALISTIWASMUCHSTRUCKWITHCERTAINFACTSINTHEDISTRIBUTIONOFTHEINHABITANTSOFSOUTHAMERICAANDINTHEGEOLOGICALRELATIONSOFTHEPRESENTTOTHEPASTINHABITANTSOFTHATCONTINENTTHESEFACTSSEEMEDTOMETOTHROWSOMELIGHTONTHEORIGINOFSPECIESTHATMYSTERYOFMYSTERIESASITHASBEENCALLEDBYONEOFOURGREATESTPHILOSOPHERSONMYRETURNHOMEITOCCURREDTOMEINTHATSOMETHINGMIGHTPERHAPSBEMADEOUTONTHISQUESTIONBYPATIENTLYACCUMULATINGANDREFLECTINGONALLSORTSOFFACTSWHICHCOULDPOSSIBLYHAVEANYBEARINGONITAFTERFIVEYEARSWORKIALLOWEDMYSELFTOSPECULATEONTHESUBJECTANDDREWUPSOMESHORTNOTESTHESEIENLARGEDININTOASKETCHOFTHECONCLUSIONSWHICHTHENSEEMEDTOMEPROBABLEFROMTHATPERIODTOTHEPRESENTDAYIHAVESTEADILYPURSUEDTHESAMEOBJECTIHOPETHATIMAYBEEXCUSEDFORENTERINGONTHESEPERSONALDETAILSASIGIVETHEMTOSHOWTHATIHAVENOTBEENHASTYINCOMINGTOADECISIONMYWORKISNOWNEARLYFINISHEDBUTASITWILLTAKEMETWOORTHREEMOREYEARSTOCOMPLETEITANDASMYHEALTHISFARFROMSTRONGIHAVEBEENURGEDTOPUBLISHTHISABSTRACTIHAVEMOREESPECIALLYBEENINDUCEDTODOTHISASMRWALLACEWHOISNOWSTUDYINGTHENATURALHISTORYOFTHEMALAYARCHIPELAGOHASARRIVEDATALMOSTEXACTLYTHESAMEGENERALCONCLUSIONSTHATIHAVEONTHEORIGINOFSPECIESLASTYEARHESENTTOMEAMEMOIRONTHISSUBJECTWITHAREQUESTTHATIWOULDFORWARDITTOSIRCHARLESLYELLWHOSENTITTOTHELINNEANSOCIETYANDITISPUBLISHEDINTHETHIRDVOLUMEOFTHEJOURNALOFTHATSOCIETYSIRCLYELLANDDRHOOKERWHOBOTHKNEWOFMYWORKTHELATTERHAVINGREADMYSKETCHOFHONOUREDMEBYTHINKINGITADVISABLETOPUBLISHWITHMRWALLACESEXCELLENTMEMOIRSOMEBRIEFEXTRACTSFROMMYMANUSCRIPTSTHISABSTRACTWHICHINOWPUBLISHMUSTNECESSARILYBEIMPERFECTICANNOTHEREGIVEREFERENCESANDAUTHORITIESFORMYSEVERALSTATEMENTSANDIMUSTTRUSTTOTHEREADERREPOSINGSOMECONFIDENCEINMYACCURACYNODOUBTERRORSWILLHAVECREPTINTHOUGHIHOPEIHAVEALWAYSBEENCAUTIOUSINTRUSTINGTOGOODAUTHORITIESALONEICANHEREGIVEONLYTHEGENERALCONCLUSIONSATWHICHIHAVEARRIVEDWITHAFEWFACTSINILLUSTRATIONBUTWHICHIHOPEINMOSTCASESWILLSUFFICENOONECANFEELMORESENSIBLETHANIDOOFTHENECESSITYOFHEREAFTERPUBLISHINGINDETAILALLTHEFACTSWITHREFERENCESONWHICHMYCONCLUSIONSHAVEBEENGROUNDEDANDIHOPEINAFUTUREWORKTODOTHISFORIAMWELLAWARETHATSCARCELYASINGLEPOINTISDISCUSSEDINTHISVOLUMEONWHICHFACTSCANNOTBEADDUCEDOFTENAPPARENTLYLEADINGTOCONCLUSIONSDIRECTLYOPPOSITETOTHOSEATWHICHIHAVEARRIVEDAFAIRRESULTCANBEOBTAINEDONLYBYFULLYSTATINGANDBALANCINGTHEFACTSANDARGUMENTSONBOTHSIDESOFEACHQUESTIONANDTHISCANNOTPOSSIBLYBEHEREDONE
        
'''

ciphertext = "LNKNWQXCKEWAZHVJWAEORNLUPSSAITOEROVNWUIWTVVTZSIFPUTDAGUUTGEVWHTAZGDIEBIPWSZJBUHDZOBELBLPQBQOWPPRLNYWJVWAEPABISFQBUDMVNQPDAEZQAWHVCMBOOXEKNORVHIGLOEOWSWHVLZRVEEPBBWHVLIFWIEDIOLTRJBFRFKDIGFOEPQAHNKPPRVEWWKGVSVAURGTFIMGRTYNWJVODATVJHKKVGKEFNQTLNFBACHCZAAGKAKIGFWEIUWSPYJPMELEJWAVWHROJRHNTWTYHDSUWAHOWKCEJRVWBRVTGDQYRSFLPRUSFJULUEKQZAKODAQGRCTQZEHDKKURLNKDIGVODABULNXIQTKTGAZUDPJXMZDDVKCGRNKDQFTUVOBVRNSUXNWIVJBYBATYCZXLRPQAJAEZZRILVYBVQGFJIYOSFNBFRFWWKGVWYEKUFOLHLCRSJEJYBHRRMNQYSAIELNXKVVWAWPMEIIMAGRDRJSWENIRHTBZEUIGFHLWPWFSETQTNWEFJBUHSLXRRFTRJLQUENQXFRMVOPBUTEKBRVTYAARLEEHIEJEUEVVQTFWAXHTTDWSWHVYWAFLLOQBQSNDQPKTYAVFHEDALGRMVLZBEASHMSUODPPNWPVNQBGTFPPRSRVOMAWDRUQUDVVOBRDDZHGCXRJQMQWHVOIZHOSFMPWIYKXRWHRPQZDYSAMKFUJALSRRVJBRUIECWAWHVOMCHRJKVNODVPIVOSROQTLVVPPRPTFOPBZTYWBVKAMAVBWBVAVUDSKUQAFODEVTWORZMPLSZKVZBWFNSVVNFSVRDRCUNVQIJDMQEUKWAVWWZHTGDKVIMGZOFNBUUEVIWEHYVWZFWOTKUCOEKAQGDNUWAZBHVWTGKIJBIEIRFIAGUOECQUDVVXMRQUICMQWOGQJYLSYPPVVASOBEDCKEPNYEDKZRHSGAKVDLCUJRHNZJLHFEUPWQRTYEANVMISIYOATAEURIJJWJVTLZGVQGKDMADTLNIYKIJPWEBOWPPRPACWGNUCYEXROAXKPNVAINQIHDRPIYPOJPMKDCKHGGKEJWURJEEAZNOCFJKYXSZKVFWHRPQUDVVKVGKEFNQTLNFBACHCZAAYDSKUMNUHVOMAWTFIMNPEDKQERNKDQFVUSFMPWWZPPNUEHQMFWTYWBVZOLHLSRRNWZQLTKKAVUCYWZYHSCUMYOWYKARQTZPBBWHVHQAQERJABFIVPGNQDZPQFSUSHQFKEUEVGKEKDQEGVFHCZHOWPPRMOLNVNOOWPPNWSFYQRWYJEZPOYVHTNQDUNPBRKVNEURBFPPXQENKNZBWFNSGKECWBGHRYWDVQGIAIQPYJGMGFHFBPBQOLNMQPESUBULNBEVTLTRZDVVASHMGRPLXTVVHNEBUPRNWTYDCVOMKFECHMAWMVIWVUSFIMOUIVBMKWRRYBFIRFIULPAEQAPUIGPAGKIJWJFWRRYBJKITDQARWGQJYLSYICFWNVYMFVAIETLEEZIXRUFVYBVFAEJWGKEIAOVYEIANRUEEYMFDNUWCGKOIEBVHSWKZZBSVRMEDLJPIGHMVJBFDNUEUHVTKNCFWTFPPRUERZMEUEGKAVQGJKURFOEBQQHNTAQAPYRYKHUATUVBGOLXBRURFNAJLLCDIIHCIAXGLNKDWHJHZDWCHIYWDRDLNWGFEEVJKNXTZKCFLNKNCFWIECBBJOFZIHWHFNQGLEJWTBQEZYIAKEIAOVYEFJTLWHVCMAHRRHKBQCCQAVRNJWBJKITDQUDVVWZELVVZEVWHRBMJIATPAVQICHCFWRRPQBQBLPEULCYEPBSEZJUBVTTWARVWZHTFXFWEKRQOFJMPDNWAMYPOIAARQSZXTRWHRJQQROWPPRQETAAFLTPKNUHRVWNGHRGQJYLSYEVTLNUABNLLRHTGKEWWKGVWZPPEHFVNMAFEJKVJKITDULFOEYTHVIFJAUDVVXMRQGIKCAGEUWVQLHFLMVQAWQBHUENKZXWOUKBULSWKZVDMNATYDWRNMGKAKOKNUCVHGNVIECTRSOZJBVVDZOKHVSVZQAWHZODBOUDAWAZHZYPSDCKOKNQNFPJRDDUQKRGOWPMADPGWZRQTCUTRDDZJOGRCFJKYXSZKVFGIIAKGOYFLXBVIKABBWHFOMNWWYEKULHRRMNURZRMQDFREZEHSLHBPDNSAWOWAZJMQRNCUJLIUCHGFWAKEVTDNUXIYDNTEVTWHVBIPWSRJLNUGLIMAWSFJJBWHJELRVOWAIPKQLAAGLOEWVQWHZOKNQNFPXBVSZXTLEEYAZRGOEA"

def getKeyLength(ciphertext):
    for i in range(1,15):
        shifted = ciphertext[-i:] + ciphertext[:-i]
        counter = 0
        for j in range(0, len(ciphertext)):
            if shifted[j] == ciphertext[j]:
                counter += 1
        
        print("Shift: {0}, Coinc: {1}\n".format(i, counter))
        
getKeyLength(ciphertext)

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
                        
print(getKey(ciphertext, 6))
print(getKey(ciphertext, 12)) 

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

plaintext = vigenere_decrypt(ciphertext, "DARWIN")
print(plaintext)


# In[ ]:


'''
5. (20 points) Implement the Blum-Blum-Shub PRNG 

Section 2.10 (pp. 41-43) describes the Blum-Blum-Shub algorithm for 
generating cryptographically secure pseudo-random bits. Implement the 
algorithm as a program to reproduce the results on page 43. 

That is, your program should:

    a.  Hardcode the values for p and q;
    b.  Compute n from those;
    c.  Using the value given for x, compute and print the values x0, x1, ..., x8. For the moment, don't worry about producing the values b0, b1, ..., b8.

Your answer will be a source file in Python or Java. 
Please call it bbsprng.{java,py}.

PLEASE SEE bbsprng.py, ATTACHED
'''


# In[ ]:




