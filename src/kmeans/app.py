import math
import os
import random

import matplotlib.pyplot as plt
import numpy as np

os.system("clear")


def input_file(file_name):
    with open(file_name) as f:
        name = f.readline()  # do not include the first line
        data = [[float(x) for x in line.split(",")] for line in f]
    name = name.split(",")
    return name, data


def calc(n_clusters, attr1, attr2):
    #! get random x and y centroids
    centroids_list = []
    for i in range(n_clusters):
        x_centroid = data[random.randrange(0, len(data))][attr1]
        y_centroid = data[random.randrange(0, len(data))][attr2]

        centroids_list.append([x_centroid, y_centroid])

    # centroids_list = [[11.76, 2.68], [13.77, 1.9]]

    centroids_are_changing = True
    while centroids_are_changing:

        cluster_list = []
        for c in centroids_list:
            cluster_list.append([])

        data_points_list = []
        data_sum = []
        for feature_vector in data:
            feature_point = [feature_vector[attr1], feature_vector[attr2]]

            #! get the distance
            sum_list = []
            for centroid in centroids_list:
                distance = 0
                index = 0
                for item in centroid:  # calculate x and y
                    distance += (feature_point[index] - item) ** 2  # euclidean distance
                    index += 1
                sum_list.append(math.sqrt(distance))
            data_sum.append(sum_list)

            # get the index of the minimum in the list
            cluster = sum_list.index(min(sum_list))
            # data_points_list.append([feature_point, cluster, distance])

            # group into clusters
            cluster_list[cluster].append(feature_point)

        #! update centroid
        new_centroid = []
        for item in cluster_list:
            x_sum = 0
            y_sum = 0
            cluster_length = len(item)
            # print(cluster_length)
            for each in item:
                x_sum += each[0]
                y_sum += each[1]

            temp_centroid = [x_sum / cluster_length, y_sum / cluster_length]
            new_centroid.append(temp_centroid)

        print(new_centroid)

        # check if the centroids are the same as the previous
        if centroids_list == new_centroid:
            centroids_are_changing = False
        else:
            centroids_list = new_centroid

    #! output to a file
    with open("src/kmeans/output.csv", "w") as file:
        for output_index in range(len(new_centroid)):
            file.writelines(
                str(
                    f"Centroid: {output_index} ({new_centroid[output_index][0]}, {new_centroid[output_index][1]})\n"
                )
            )

            print()
            for item in cluster_list[output_index]:

                file.writelines("".join(str(item)))
                file.writelines("\n")

    #! scatter plot
    color_list = [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "violet",
        "black",
        "pink",
        "brown",
        "cyan",
    ]

    for scatter_index in range(len(new_centroid)):
        x_list = []
        y_list = []
        for item in cluster_list[scatter_index]:

            x_list.append(item[0])
            y_list.append(item[1])
        x = np.array(x_list)
        y = np.array(y_list)

        # plot on the graph depending on the color
        plt.scatter(x, y, c=color_list[scatter_index])

    # Display
    plt.savefig("src/kmeans/plot.png")
    plt.show()


#! MAIN FILE
name, data = input_file("src/kmeans/Wine.csv")

import os.path

import PySimpleGUI as sg

value = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
k = []
# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Attribute 1"),
        sg.OptionMenu(values=name, size=(4, 8), key="-ATTR1-", default_value=name[0]),
    ],
    [
        sg.Text("Attribute 2"),
        sg.OptionMenu(values=name, size=(4, 8), key="-ATTR2-", default_value=name[1]),
    ],
    [
        sg.Text("Enter n clusters"),
        sg.OptionMenu(
            values=value, size=(4, 8), key="-N-CLUSTER-", default_value=value[1]
        ),
    ],
    [sg.Text("Centroids and Clusters:")],
    [sg.Listbox(k, size=(30, 6))],
    [sg.Button("RUN"), sg.Button("RESET")],
]


# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
    ]
]
window = sg.Window("Image Viewer", layout)
while True:
    event, values = window.read()

    # Folder name was filled in, make a list of files in the folder
    if event == "RUN":
        if values["-ATTR1-"] != values["-ATTR2-"]:
            # get the index of the dropdown list
            attr1 = name.index(values["-ATTR1-"])
            attr2 = name.index(values["-ATTR2-"])
            n_clusters = values["-N-CLUSTER-"]

            print(attr1)
            print(attr2)
            print(n_clusters)
            calc(int(n_clusters), attr1, attr2)
            print(k)
    if event == "RESET":
        window.FindElement("-ATTR1-").Update(name[0])
        window.FindElement("-ATTR2-").Update(name[1])
        window.FindElement("-N-CLUSTER-").Update(value[1])

    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
        except:
            pass

    if event == "Exit" or event == sg.WIN_CLOSED:
        break
