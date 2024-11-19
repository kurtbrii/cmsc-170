# Punzalan, Kurt Brian Daine B.
# 2020-00772
# CMSC 170 - X-4L
# Exercise 7: K Nearest Neighbors

import operator  # class sorter
import os

os.system("cls")

from prettytable import PrettyTable


#! FUNCTIONS
# read file
def input_file(file_name):
    with open(file_name) as f:
        data = [[float(x) for x in line.split(",")] for line in f]

    return data


# class declaration
class Data:
    def __init__(self, list, distance):
        self.list = list
        self.distance = distance


#! MAIN FILE
pretty_table = PrettyTable()
data = input_file("src/knn/data01/diabetes.csv")
inputs = input_file("src/knn/data01/input.in")

k = int(input("Enter k: "))

with open("src/knn/output.txt", "w") as f:
    for input in inputs:
        distance_list = []
        for item in data:
            sum = 0
            for i in range(len(item) - 1):
                sum += (item[i] - input[i]) ** 2  # euclidean distance
            distance_list.append(Data(item, sum))  # append a new instance of Data class

        distance_list.sort(key=operator.attrgetter("distance"))  # sorts the classes

        classification_list = []
        for i in range(k):
            print(distance_list[i].list)
            print(distance_list[i].distance)
            classification_list.append(distance_list[i].list[-1])
            print(classification_list)
            print("\n")
            print("END OF DATA\n\n")

            classification = max(
                set(classification_list), key=classification_list.count
            )
            print("COUNTER", classification)

        new_item = []
        new_item.extend(input)
        new_item.append(classification)

        pretty_table.add_row(new_item)
        print(pretty_table)

    f.write(f"{str(pretty_table)}\n")
