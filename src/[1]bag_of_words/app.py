# Kurt Brian Daine B. Punzalan
# 2020-00772
# CMSC 170 - X4-L
# Exercise 04: Bag of Words

import os

from functions import *

os.system("cls")

# MAIN
file = readFile("./src/[1]bag_of_words/files/002.txt")

words_counter = 0
words_dict = []
for item in file:
    # CLEAN by setting each item in lowercase
    item = item.lower()
    item = removeNonAlpha(item)

    # COUNT
    if item:
        duplicate_index = wordExists(words_dict, item)
        if duplicate_index == -1:
            newDict = {}
            words_dict.append(newDict)

            newDict["word"] = item
            newDict["frequency"] = 1
        else:
            words_dict[duplicate_index]["frequency"] += 1

        words_counter += 1

print(len(words_dict))
print(words_counter)

words_dict = sorted(words_dict, key=lambda k: k["word"])

for item in words_dict:
    print(f'{item["word"]}\t{item["frequency"]}\t')

outputFile(words_dict, "output.txt", words_counter)
