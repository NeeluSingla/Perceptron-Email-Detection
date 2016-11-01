import os
import sys
import math
import re
import string
import random
import json

def learn(rootdir):
    dictionary = {}
    new_dict = {}
    L = list()
    weights = {}
    max_iterations = 30
    for dirName, subdirList, fileList in os.walk(rootdir):
        for fname in fileList:
            if fname.endswith('.txt'):
                filename = (os.path.join(dirName, fname))
                L.append(filename)
                with open(filename, "r", encoding="latin1") as file:
                    dict_words = {}
                    for line in file:
                        words = line.split()
                        for word in words:
                            if word not in dict_words:
                                dict_words[word] = 1
                            else:
                                dict_words[word] += 1
                            if word not in weights:
                                weights[word] = [0,0]
                dictionary[filename] = dict_words
    #print(L)
    #print(len(L))
    #print(dictionary
    #print(weights)

    bias = 0
    gamma = 0
    little_bias = 0
    counter = 1
    for iter in range(0,max_iterations):

        random.shuffle(L)
        for path in L:
            alpha=0
            if path.split('/')[-2] == 'spam':
                gamma = 1
            else:
                gamma = -1
            for word in dictionary.get(path):
                #print(word)
                alpha += (weights.get(word)[0]*dictionary.get(path)[word])
            alpha += bias
            #print(alpha)
            y = alpha*gamma
            #print(y)
            if(y <= 0):
                for word in dictionary.get(path):
                    weights[word][0] += gamma*dictionary.get(path)[word]
                    weights[word][1] += gamma*dictionary.get(path)[word]*counter
                bias += gamma
                little_bias += gamma*counter
            counter += 1
    #print(weights)
    #print(len(weights))
    #print(bias)
    for word in weights:
         weights[word][1] = weights[word][0]-((1/counter)*weights[word][1])
    little_bias = bias-((1/counter)*little_bias)
    print(little_bias)
    #print(weights)

    for key, val in weights.items():
        new_dict[key] = val[1]
    new_dict["per_model_bias"] = little_bias
    with open("per_model.txt", 'w') as fp:
        json.dump(new_dict, fp)

if __name__ == "__main__":
    learn(sys.argv[1])





