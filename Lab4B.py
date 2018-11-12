"""
CS 2302
Mark Williams
Lab 4 - Option B
Diego Aguirre/Manoj Saha
11-11-18
Purpose: Compare the binary tree implementation of Lab 3B with a hash
         table implementation.
"""

import math
import random
from HashTableNode import HashTableNode
import time

# This is the mapping used for converting a word to a base 10 number
MAPPING = {
            "a" : 0,
            "b" : 1,
            "c" : 2,
            "d" : 3,
            "e" : 4,
            "f" : 5,
            "g" : 6,
            "h" : 7,
            "i" : 8,
            "j" : 9,
            "k" : 10,
            "l" : 11,
            "m" : 12,
            "n" : 13,
            "o" : 14,
            "p" : 15,
            "q" : 16,
            "r" : 17,
            "s" : 18,
            "t" : 19,
            "u" : 20,
            "v" : 21,
            "w" : 22,
            "x" : 23,
            "y" : 24,
            "z" : 25,
          }


def modulo_hash(word, hashtable):
  """
  Finds the modulo hash for a given word.
  
  Args:
    word: A word in English
    hashtable: The hashtable being used
  
  Returns:
    conversion % len(hashtable): The hash for word

  """
  conversion = word_to_number(word)
  if conversion == -1:
    return -1
  return conversion % len(hashtable)


def multiplicative_hash(word, hashtable):
  """
  Finds the multiplicative hash for a given word.
  
  Args:
    word: A word in English
    hashtable: The hashtable being used
  
  Returns:
    int(string_hash) % len(hashtable): The multiplicative hash for word

  """
  string_hash = modulo_hash(word, hashtable)

  for character in word.lower():
    # In this segment, the modulo hash for a word is multiplied by
    # an arbitrary number and an arbitrary number is added to the hash
    if character in MAPPING:
      string_hash = (string_hash * 199) + MAPPING[character]
    else:
      return -1

  return int(string_hash) % len(hashtable)


def random_hash(word, hashtable):
  """
  Finds a random hash for a given word based on the length of the table.
  
  Args:
    word: A word in English
    hashtable: The hashtable being used
  
  Returns:
    random.randint(0, len(hashtable)): The random hash for word

  """
  conversion = word_to_number(word)
  if conversion == -1:
    return -1
  return random.randint(0, len(hashtable))


def load_factor(hash_table):
  """
  Finds a the load factor of a hashtable.
  
  Args:
    hash_table: The hashtable being used
  
  Returns:
    num_elements / len(hash_table): The load factor of the table

  """
  num_elements = 0
  for i in range(len(hash_table)):
    temp = hash_table[i]

    while temp is not None:
      num_elements += 1
      temp = temp.next

  return num_elements / len(hash_table)


def num_comparisons(hash_table, word, index):
  """
  Finds the number of comparisons needed to find a word in 
  the hashtable.
  
  Args:
    hash_table: The hashtable being used
    word: The searchee word
    index: The hash of the word
  
  Returns:
    count: The number of comparisons needed to find a word in 
    the hashtable.

  """
  temp = hash_table[index]
  count = 0
  while temp is not None:
    count += 1
    if temp.item == word:
      break
    temp = temp.next

  return count


def average_comparisons(hash_table, filename, function):
  """
  Finds the average number of comparisons needed to retrive a word
  in the table.
  
  Args:
    hash_table: The hashtable being used
    filename: The file containing all the words in the hashtable
    function: The hash function the user specifies
  
  Returns:
    sum_searches/count: The average number of comparisons needed to 
    retrive a word in the table

  """
  reader = open(filename, "r")
  lines = reader.readlines()
  index = 0
  searches = dict()
  for line in lines:
    if "\n" in line:
      line = line.replace("\n", "")
    if function == 1:
      index = modulo_hash(line, hash_table)
    elif function == 2: 
      index = multiplicative_hash(line, hash_table)
    else:
      index = random_hash(line, hash_table)
    if index == -1:
      continue
    searches[line] = num_comparisons(hash_table, line, index)
  sum_searches = 0
  count = 0
  # Counts the total comparisons and divides it by 
  # the number of searches
  for key in searches:
    sum_searches += searches[key]
    count += 1
  return sum_searches / count


def word_to_number(word):
  """
  Converts a base 26 number to a base 10 number.
  
  Args:
    word: The word (base 26 number) to be converted
  
  Returns:
    number: The base 10 converted number

  """
  word = word.lower()
  i = len(word)-1
  number = 0
  counter = 0
  # This is a basic algorithm for conversion to base 10
  while i != 0 :
    if word[i] in MAPPING:
      number += MAPPING[word[i]] * math.pow(26, counter)
      counter += 1
      i -= 1
    else:
      number = -1
      break
  return int(number)

def create_hashtable(function, filename):
  """
  Creates a hashtable of size 400000 based on the file provided.
  
  Args:
    function: The hash function the user specifies
    filename: The file containing all the words in the hashtable
  
  Returns:
    hash_table: A complete hashtable of all valid english words

  """
  reader = open(filename, "r")
  lines = reader.readlines()
  hash_table = [None] * 400000
  for line in lines:
    if "\n" in line:
      line = line.replace("\n", "")
    if function == 1:
      if modulo_hash(line, hash_table) != -1:
        hash_table[modulo_hash(line, hash_table)] = \
          HashTableNode(line, hash_table[modulo_hash(line, hash_table)])
    elif function == 2: 
      if multiplicative_hash(line, hash_table) != -1:
        hash_table[modulo_hash(line, hash_table)] = \
          HashTableNode(line, hash_table[modulo_hash(line, hash_table)])
    else:
      if random_hash(line, hash_table) != -1:
        hash_table[modulo_hash(line, hash_table)] = \
          HashTableNode(line, hash_table[modulo_hash(line, hash_table)])
  return hash_table


def main():
  user_input = 0
  while user_input <= 0 or user_input >= 4:
    print("What type of hash function do you want to use?")
    print("Enter 1 for modulo, 2 for multiplicative, 3 for random.")
    user_input = int(input())
    if user_input == 1 or user_input == 2 or user_input == 3:
      break
    print("Not valid input. Please try again.")
  filename = "words.txt"
  hash_table = create_hashtable(user_input, filename)
  print("The load factor of this hash_table is " + 
        str(load_factor(hash_table)))
  print("The average number of comparisons required to perform a " +
        "successful retrieve operation are: " + 
        str(average_comparisons(hash_table, filename, user_input)))
  

main()
