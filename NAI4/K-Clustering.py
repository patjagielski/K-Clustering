import copy
import math
import random as rand




def classifyPoints(list_of_k_points, data):
    class_dict = dict()
    max_distance = 1000000
    index_of_cluster = -1
    for row in range(len(list_of_k_points)):
        point_list = list_of_k_points[row][0:4]
        euclid_distance = euclidean_distance(point_list, data)

        if euclid_distance < max_distance:
            max_distance = euclid_distance
            index_of_cluster = row
    return index_of_cluster

def preprocess(point):
    templist= []
    templist = [(str(coordinate)) for coordinate in point]

    return [float(str(coordinate.replace(',', '.'))) for coordinate in templist]


def generate_K_Points(k, set_of_items):
    rand.shuffle(set_of_items)
    return copy.deepcopy(set_of_items[0:k])


def euclidean_distance(k_points, data):
    a, b, c, d = preprocess(k_points)
    w, x, y, z = preprocess(data)
    # createScatterPlot(w, x, name, a, b)
    return math.sqrt(((a - w) ** 2) + ((b - x) ** 2) + ((c - y) ** 2) + ((d - z) ** 2))


file = open("./iris_training.txt", "r")

training_list = file.read().splitlines()
k = int(input("Insert K:"))
for i in range(0, len(training_list)):
    training_list[i] = training_list[i].split('\t')


k_points = generate_K_Points(k, training_list)
oldDict = dict()

def pair_wise_addition(output, input):
    templist = copy.deepcopy(output)
    for i in range(len(output)):
        templist[i] += input[i]
    return templist

def pair_wise_devision(output, input):
    templist=[0 for j in range(len(output))]
    for i in range(len(output)):
        templist[i]=output[i]/input
    return templist



def computePoint(list_of_k_points, data, oldDict,  k):
    newDict = dict()
    templist = []
    for k in range(len(list_of_k_points)):
        newDict[k] = []
    for point in data:
        index_of_cluster = classifyPoints(list_of_k_points, point[0:4])
        newDict[index_of_cluster].append(point)
    for i in range(k+1):
        for j in list_of_k_points[i]:
            templist.append(str(j))
        sumOf = [0 for q in range(4)]
        counter = 0
        for val in newDict[i]:
            newval = preprocess(val[0:4])
            sumOf = pair_wise_addition(sumOf, newval)
            counter+=1
        templist = []
        sumOf = pair_wise_devision(sumOf, max(counter, 1))
        print(sumOf)
        list_of_k_points[i] = sumOf

    flag = (newDict == oldDict)
    if not flag:
        computePoint(list_of_k_points, data, newDict, k)
    else:
        print("The k-clustering algorithm is complete")
        for key in newDict:
            entropy = 0
            dict_of_keys = {"Iris-setosa":0, "Iris-virginica":0, "Iris-versicolor":0}
            for value in newDict[key]:
                dict_of_keys[value[4]]+=1
            for name in dict_of_keys:
                x = sum(dict_of_keys.values())
                probability = dict_of_keys[name]/x
                print(dict_of_keys)
                if probability == 0:
                    entropy += 0
                    continue
                else:
                    entropy += math.log2(probability)*probability

            print("Entropy",-entropy)

computePoint(k_points, training_list, oldDict, k)

