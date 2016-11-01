import os
import sys
import math
import re
import string
import random
import json

def learn(rootdir):
    dictionary = {}
    L = list()
    weights = {}
    max_iterations = 20
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
                                weights[word] = 0
                dictionary[filename] = dict_words
    #print(L)
    #print(len(L))
    #print(dictionary)
    #print(weights)

    bias = 0
    gamma = 0
    for iter in range(0,max_iterations):

        random.shuffle(L)
        for path in L:
            alpha = 0
            #print(path)
            if path.split('/')[-2] == 'spam':
                gamma = 1
            else:
                gamma = -1
            for word in dictionary.get(path):

                alpha += (weights.get(word)*dictionary.get(path)[word])

            alpha += bias
            #print(alpha)
            y = alpha*gamma
            #print(y)
            if(y <= 0):
                for word in dictionary.get(path):
                    #print(word)
                    #print(gamma)
                    weights[word] += gamma*dictionary.get(path)[word]
                    #print(weights[word])
                bias += gamma
                #print(bias)
    #print(weights)
    #print(len(weights))
    print(bias)
    weights["per_model_bias"] = bias
    with open("per_model.txt",'w') as f:
        json.dump(weights,f)

if __name__ == "__main__":
    learn(sys.argv[1])





