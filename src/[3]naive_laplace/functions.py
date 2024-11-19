import os
from decimal import *

# bag of words funct
def loopFiles(path):
  number_of_files = len([entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))])

  # from https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
  file = []
  for filename in os.listdir(path):
    f = os.path.join(path, filename)
    # checking if it is a file
    if os.path.isfile(f):
      file.extend(readFile(f))

  return file, number_of_files

# TOKENIZE by splitting them into a single list
def readFile(file_name):
  f = open(file_name, "r", encoding='latin-1')

  file = []
  lines = f.readlines()
  for line in lines:
    file.extend(line.split(" "))

  return file


# removes non-alphaneumeric
def removeNonAlpha(item):
  included_letters = "abcdefghijklmnopqrstuvwxyz0123456789"
  for character in item:
    if character not in included_letters:
      item = item.replace(character, "")

  return item

def bagOfWordsGenerator(file, is_bow_checked):
  words_counter = 0
  index = 0
  words_dict = []
  
  for item in file:
    # CLEAN by setting each item in lowercase
    item = item.lower()
    item = removeNonAlpha(item)

    if item != "":
      # COUNT
      duplicate_index = wordExists(words_dict, item, is_bow_checked)
      if is_bow_checked:
        if index == 0 or duplicate_index == -1:
          newDict = {}
          words_dict.append(newDict)

          newDict["index"] = index
          newDict["word"] = item
          newDict["frequency"] = 1
          
          index += 1
        else:
          words_dict[duplicate_index]["frequency"] += 1

        words_counter += 1
      else:
        if duplicate_index == -1:
          words_counter += 1
          words_dict.append(item)

  return words_counter, words_dict

def wordExists(words_dict, item, is_bow_checked):
  for i in range(len(words_dict)):
    if is_bow_checked:
      if words_dict[i]["word"] == item:
        return i # returns the index so that the frequency of the element with that index will be incremented
    else:
      if words_dict[i] == item:
        return i # returns the index so that the frequency of the element with that index will be incremented
  return -1

# Spam Filtering
def computeDSize(spam_list, ham_list):
  new_spam_list = [i.lower() for i in spam_list]
  new_ham_list = [i.lower() for i in ham_list]

  new_spam_list.extend(new_ham_list)
  combined_list = list(dict.fromkeys(new_spam_list)) # removes duplicates
  d_size = len(combined_list)

  return d_size, combined_list

def computeNewWords(text, combined_list):
  count_new_words = 0
  for element in text.split():
    if element not in combined_list:
      count_new_words += 1

  return count_new_words

def countInBag(bag, element):
  count = 0
  for item in bag:
    if element == item['word']:
      count = item['frequency']
      return count
  return count
  

def computeTotalSpamHam(text, spam_ham_bag, k, spam_ham_count, d_size, count_new_words, p_spam_ham):
  total = 1
  for element in text.split():
    count = countInBag(spam_ham_bag, element)
    subtotal = Decimal(count + k)/Decimal(spam_ham_count + (k * (d_size + count_new_words)))
    total *= subtotal

  new_total = total*Decimal(p_spam_ham)
  return new_total.ln()

# probability of spam given message
def pSpamGivenMessage(total_spam, total_ham):
  p_spam_msg = Decimal(total_spam.exp())/(Decimal(total_spam.exp())+Decimal(total_ham.exp()))

  return p_spam_msg
