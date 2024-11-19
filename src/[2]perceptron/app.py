# Punzalan, Kurt Brian Daine B.
# 2020-00772
# CMSC 170 - X-4L
# Exercise 6 - Perceptron

import os

from functions import *

os.system("cls")

from prettytable import PrettyTable

weight_converges = False
counter = 1
with open("output.txt", "w") as f:
    while not weight_converges:
        learning_rate, threshold, bias, training_data = input_file(
            "src/[2]perceptron/files/not_2.txt"
        )
        a_list = []
        y_list = []
        z_list = []

        # initialize weights
        weights = [[float(0)] * (len(training_data[0]))] if counter == 1 else weights

        outer_index = 0
        for item in training_data:
            # initialize the table (for output)
            pretty_table = PrettyTable()

            # separate items of y in the training data and append each to z_list
            # insert bias per row
            separate_data(item, z_list, bias)

            # computes for a and append it to the list
            a_sum = compute_perceptron(item, weights, outer_index, a_list)
            # print(f"A_SUM: {a_sum}")

            y_data = compute_y(y_list, a_sum, threshold)

            adjust_weights(weights, outer_index, item, learning_rate, z_list, y_data)

            item.extend(weights[outer_index])
            item.extend(
                [
                    round(a_list[outer_index], 2),
                    y_list[outer_index],
                    z_list[outer_index],
                ]
            )

            outer_index += 1

        # output file
        # print_data(training_data)

        # create names
        x_name = [
            "b" if x == len(weights[outer_index]) - 1 else f"x{str(x)}"
            for x in range(len(weights[outer_index]))
        ]
        w_name = [
            "wb" if x == len(weights[outer_index]) - 1 else f"w{str(x)}"
            for x in range(len(weights[outer_index]))
        ]

        x_name.extend(w_name)
        x_name.extend(["a", "y", "z"])

        # pretty table
        pretty_table.field_names = x_name
        pretty_table.add_rows(training_data)
        print(pretty_table)

        # output file using pretty table
        f.writelines(f"\n\nIteration {counter}\n\n")
        f.write(f"{str(pretty_table)}")

        # output_file(pretty_tablen, counter, x_name, f)
        counter += 1

        # weight converges?
        weight_converges = check_if_converges(weights)

        if not weight_converges:
            weights = did_not_converge(weights)
