#!/usr/bin/env python
# coding=utf-8

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
labelfile=""
y = pd.read_csv(labelfile,header=None).as_matrix()
x = range(len(y))

j = 0
for i in y:
    if i[0] == 1:
        print("First positive label (i.e., label==1):" + str(j) + " (starting from 0)")
        break
    j += 1

fig = plt.scatter(x, y,s=0.2)
plt.title("Lables")
plt.ylabel("Label")
plt.xlabel("Sample Number")
plt.show()




