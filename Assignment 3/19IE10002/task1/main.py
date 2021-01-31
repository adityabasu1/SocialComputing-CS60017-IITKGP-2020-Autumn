#Creator: Aditya Basu, 19IE10002


import os
import csv
import string
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import spacy
import fasttext

curr_dir_path = os.getcwd()  #returns current directory path
common = curr_dir_path[:-5] #since "task1" occupies 5 places. we slice it out to get out the common path where we'll add file names to enter that reqd dir

file_name = common + "data" + "/" + "train.tsv"
#print(file_name) to check that we got the correct filepath

train_df = pd.read_csv(file_name,delimiter = '\t', encoding='utf-8', quoting = csv.QUOTE_NONE, error_bad_lines= False) #train data-frame using pandas

#generating the required lists for train dataset
#note that we purposely use lists since they are mutable and can be changed by the pre-processing function which we shall later define

train_id = train_df['id'].tolist() #returns the list of values
train_text = train_df['text'].tolist() #returns the list of text
train_outcome = train_df['hateful'].tolist() #outcome as in 0 or 1. we get the list of values


file_name = common + "data" + "/" + "test.tsv"

test_df = pd.read_csv(file_name,delimiter = '\t', encoding='utf-8', quoting = csv.QUOTE_NONE, error_bad_lines= False) #test data-frame

#generating the required lists for test dataset

test_id = test_df['id'].tolist() #returns the list of values
test_text = test_df['text'].tolist() #returns the list of text

#print(len(train_id)) confirming this gives 16112
#print(len(test_id)) confirming this gives 5000

#defining the pre-processing function

def pre_processing(L):  #L is the list of inputs
    for w in range(len(L)):
        L[w] = L[w].lower()

    for w in range(len(L)):
        for ch in L[w]:
            if ch in string.punctuation: #string.punctuation contains all the lists
                L[w] = L[w].replace(ch,"")

#now pre-processing our lists
pre_processing(train_text)
pre_processing(test_text)

#Random Forest Classifier(first part of first task)

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

train_embeddings = vectorizer.fit_transform(train_text) #creating embeddings
rcf = RandomForestClassifier(n_estimators = 128)
rcf.fit(train_embeddings, train_outcome)    #fitting the training data to get our model


test_embeddings = vectorizer.transform(test_text)
test_outcome = rcf.predict(test_embeddings) #generating our prediction in a list

#will write it to our file
my_list = []
my_list.append(['id','hateful'])

for i in range(len(test_id)):
    my_list.append(list( (test_id[i],test_outcome[i]) ))

os.mkdir(common + "/" + "predictions")
os.chdir(common + "/" + "predictions")

with open('RF.csv', 'w', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(my_list)
    
f.close()

#second part of task1

os.chdir(common + "/" + "task1")

from sklearn.svm import SVC

op = spacy.load('en_core_web_md')
train_embeddings = []

for line in train_text:             #first we shall generate embeddings
    train_embeddings.append(op(line).vector)

cf = SVC()
cf.fit(train_embeddings,train_outcome)


test_embeddings = []
for line in test_text:
    test_embeddings.append(op(line).vector)

test_outcome = cf.predict(test_embeddings)

my_list = []
my_list.append(['id','hateful'])

for i in range(len(test_id)):
    my_list.append(list( (test_id[i],test_outcome[i]) ))

os.chdir(common + "/" + "predictions")

with open('SVM.csv', 'w', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(my_list)

f.close()

#third part of first task

os.chdir(common + "/" + "task1")

ft_list = []    #this is the fasttext list

for i in range(len(train_id)):  #generating data in fasttext format
    ft_list.append("__label__" + str(train_outcome[i]) + " " + train_text[i])

with open('temp.txt', 'w') as f:    #writing the list to a text file #temp.txt will be generated
    for item in ft_list:
        f.write("%s\n" % item)

model = fasttext.train_supervised('temp.txt')	#generating our model

test_outcome = []

for t in test_text:
    test_outcome.append( (model.predict(t))[0][0][-1] )	#getting the label from the prediction

my_list = []
my_list.append(['id','hateful'])

for i in range(len(test_id)):
    my_list.append(list( (test_id[i],test_outcome[i]) ))

os.chdir(common + "/" + "predictions")

with open('FT.csv', 'w', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(my_list)

f.close()

