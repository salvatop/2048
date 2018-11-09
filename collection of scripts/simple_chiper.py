#!/usr/bin/env python3

"""
Created on Thu Nov  8 11:53:33 2016

@author: Salvatore Palazzo
"""

"""
Example how to create a simple cipher, this example 
take the first letter of each word (unless it's a vowel), 
and put it at the end adding "ay".
"""

def pygLatin(original_word):

 pyg = 'ay'
 original_word = input("Enter a word:")

 if len(original_word) > 0 and original_word.isalpha():
    word = original_word.lower()
    first = word[0]
    new_word = word + first + pyg
    new_word = new_word[1:len(new_word)]
    print (new_word)

 else:
    print ("empty")
    

