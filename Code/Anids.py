#Kearas RNN 
#source ./venv/bin/activate
import numpy as np
import keras
from keras.models import load_model
from keras.layers.normalization import BatchNormalization
from keras.layers import LSTM
import csv
import os, sys
import numpy as np
from numpy import array
from numpy import argmax

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=4, n_informative=2, n_redundant=0,random_state=0, shuffle=False)
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, y)

print(clf.feature_importances_)

print(clf.predict([[0, 0, 0, 0]]))




from sklearn import svm
from sklearn import datasets
clf = svm.SVC()
X, y= datasets.load_iris(return_X_y=True)
clf.fit(X, y)

import pickle
s = pickle.dumps(clf)
clf2 = pickle.loads(s)
clf2.predict(X[0:1])

from joblib import dump, load
dump(clf, 'autoRandomForest.joblib')
clf = load('autoEncoderRandomForest.joblib') 


inputfile1 = sys.argv[1]
inputfile2 = sys.argv[2]

X_train = []
Y_train = []
X_test  = []
Y_test  = []

with open(inputfile1) as csv_file1:
    csv_reader1 = csv.reader(csv_file1, delimiter=',')
    for row in csv_reader1:
        x = row[0:122]
        y = row[122]  
        X_train.append(array(x))
        Y_train.append(array(y))

with open(inputfile2) as csv_file2:
    csv_reader2 = csv.reader(csv_file2, delimiter=',')
    for row in csv_reader2:
        x = row[0:122]
        y = row[122]  
        X_test.append(array(x))
        Y_test.append(array(y))

X_train=np.array(X_train).reshape(len(X_train),1,122)
Y_train=np.array(Y_train).reshape(len(Y_train),1,1)

X_test=np.array(X_test).reshape(len(X_test),1,122)
Y_test=np.array(Y_test).reshape(len(Y_test),1,1)


#print x_train
#print y_train
#print x_train.shape
#print y_train.shape
model=keras.Sequential()
model.add(keras.layers.SimpleRNN( input_dim  =  122, output_dim = 200, return_sequences = True))
model.add(BatchNormalization())
model.add(keras.layers.SimpleRNN( output_dim = 300, return_sequences = True))
model.add(BatchNormalization())
model.add(keras.layers.SimpleRNN( output_dim = 30, return_sequences = True))
model.add(BatchNormalization())
#model.add(Dropout(0.5))
model.add(keras.layers.TimeDistributed(keras.layers.Dense(output_dim = 1, activation  =  "sigmoid")))

#Dense means fully connected
model.compile(loss = "mse", optimizer = "rmsprop",metrics=['accuracy'])
model.fit(X_train, Y_train, nb_epoch = 10, batch_size = 5000)
model.save('main.h5')

"""
model_yaml = model.to_yaml()
with open("model.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
"""

#print(model.predict(np.array([[[1,1],[2,2]]])))

del model
l_model = load_model('main.h5')
scores = l_model.evaluate(X_test,Y_test,verbose=0)
print("%s: %.2f%%" % (l_model.metrics_names[1], scores[1]*100))

