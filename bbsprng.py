#!/usr/bin/env python
# coding: utf-8

# In[14]:


'''
5. (20 points) Implement the Blum-Blum-Shub PRNG 

Section 2.10 (pp. 41-43) describes the Blum-Blum-Shub algorithm for 
generating cryptographically secure pseudo-random bits. Implement the 
algorithm as a program to reproduce the results on page 43. 

That is, your program should:

    a.  Hardcode the values for p and q;
    b.  Compute n from those;
    c.  Using the value given for x, compute and print the values x0, x1, 
        ..., x8. For the moment, don't worry about producing the values 
        b0, b1, ..., b8.

Your answer will be a source file in Python or Java. 
Please call it bbsprng.{java,py}.


'''

def bbsprng():
    result = [0] * 9

    # a.
    p = 24672462467892469787
    q = 396736894567834589803
    
    # b.
    n = p * q
    x = 873245647888478349013

    # c.
    for i in range(9):
        x = (x**2) % n
        result[i] = x
    
    return result

result = bbsprng()
for i in range(len(result)):
    print(str(result[i]) + "\n")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




