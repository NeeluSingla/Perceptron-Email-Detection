import os
import sys
import math
import re
import string
import random
import json


def classifier(rootdir,filename):
    modified_weights = {}
    actual_spam = 0
    actual_ham = 0
    true_positive = 0
    bias = 0
    false_negative = 0
    count_ham = 0
    count_spam = 0
    with open('per_model.txt', "r+")as f:
        modified_weights = json.load(f)
        bias = modified_weights["per_model_bias"]

    fp = open(filename, 'w')
    for dirName, subdirList, fileList in os.walk(rootdir):
        for fname in fileList:
            alpha = 0
            if fname.endswith('.txt'):
                if dirName.endswith("spam"):
                    actual_spam += 1
                else:
                    actual_ham += 1
                with open(os.path.join(dirName, fname), "r", encoding='latin1') as file:
                    for line in file:
                        words = line.split()
                        for word in words:
                            if word in modified_weights:
                                alpha += modified_weights[word]
            alpha += bias
            if alpha > 0:
                count_spam += 1
                fp.write("spam "+dirName + '/' + fname + "\n")
                if dirName.endswith("spam"):
                    true_positive += 1
            else:
                count_ham += 1
                fp.write("ham " + dirName + '/' + fname + "\n")
                if dirName.endswith("ham"):
                    false_negative += 1



    #print(false_negative)
    #print(true_positive)
    #print(actual_spam)
    #print(actual_ham)
    recall_ham = false_negative / actual_ham
    print("recall_ham " + str(recall_ham) + "\n")
    recall_spam = true_positive / actual_spam
    print("recall_spam " + str(recall_spam) + "\n")
    precision_ham = false_negative / count_ham
    print("precision_ham " + str(precision_ham) + "\n")
    precision_spam = true_positive / count_spam
    print("precision_spam " + str(precision_spam) + "\n")
    f_score_spam = ((2 * precision_spam * recall_spam) / (precision_spam + recall_spam))
    print("f_score_spam " + str(f_score_spam) + "\n")
    f_score_ham = ((2 * precision_ham * recall_ham) / (precision_ham + recall_ham))
    print("f_score_ham " + str(f_score_ham) + "\n")
    accuracy = (false_negative + true_positive) / (actual_spam + actual_ham)
    print("accuracy " + str(accuracy))

if __name__ == "__main__":
    classifier(sys.argv[1],sys.argv[2]);