# Kurt Brian Daine B. Punzalan
# 2020-00772
# CMSC 170 - X4-L
# Exercise 05: Spam Filtering

import os

from functions import *

os.system("clear")

# MAIN

# ==== BOW ====
# from https://pynative.com/python-count-number-of-files-in-a-directory/
spam_path = r"./src/[3]naive_laplace/spam"
spam_list, spam_file_length = loopFiles(spam_path)
spam_count, spam_bag = bagOfWordsGenerator(spam_list, True)

ham_path = r"./src/[3]naive_laplace/ham"
ham_list, ham_file_length = loopFiles(ham_path)
ham_count, ham_bag = bagOfWordsGenerator(ham_list, True)

print("HAM")
print(f"Dictionary Size: {len(ham_bag)}")
print(f"Total Number of Words: {ham_count}")
print()
print("SPAM")
print(f"Dictionary Size: {len(spam_bag)}")
print(f"Total Number of Words: {spam_count}")

# ==== SPAM OR HAM ====
k = int(input("Enter a smoothing factor: "))

# probabilities of ham and spam
p_spam = (spam_file_length + k) / ((spam_file_length + ham_file_length) + 2 * k)
p_ham = 1 - p_spam

d_size, combined_list = computeDSize(spam_list, ham_list)

classify_path = r"./src/[3]naive_laplace/classify"
index = 0
spam_ham_list = []
for filename in os.listdir(classify_path):
    f = os.path.join(classify_path, filename)
    # checking if it is a file
    if os.path.isfile(f):
        text = readFile(f)
        text_count, text = bagOfWordsGenerator(text, False)
        text = " ".join(text)

        count_new_words = computeNewWords(text, combined_list)

        total_spam = computeTotalSpamHam(
            text, spam_bag, k, spam_count, d_size, count_new_words, p_spam
        )
        total_ham = computeTotalSpamHam(
            text, ham_bag, k, ham_count, d_size, count_new_words, p_ham
        )

        p_spam_msg = pSpamGivenMessage(total_spam, total_ham)

        spam_ham_list.append(p_spam_msg)


with open("src/[3]naive_laplace/classify.out", "w+") as f:
    for item in spam_ham_list:
        is_spam = "HAM"
        if item > 0.5:
            is_spam = "SPAM"
        f.writelines(f"{index}\t{is_spam}\t{str(item)}\n")
        index += 1
print("Output file successful")


# for item in sorted(spam_bag, key=lambda k: k['word']):
#   print(f'{item["index"]}\t\t{item["word"]}\t\t{item["frequency"]}\t')

# print()

# for item in sorted(ham_bag, key=lambda k: k['word']):
#   print(f'{item["index"]}\t\t{item["word"]}\t\t{item["frequency"]}\t')
