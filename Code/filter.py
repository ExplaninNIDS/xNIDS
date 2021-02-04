#!/usr/bin/env python
# coding=utf-8
import sys
import os
import csv
#==============================================================================
# This script filters out the samples in a given file according to a label file. 
# Input: infile, labels, <0|1>
# Output: to stdout the filtered samples 
#
# The lables indicate which smaples should be filtered out. 
# 0: output samples with 0 as label; 1: output samples with 1 as label. 
#
#==============================================================================
def filter(tsv_file, label_file, benign=True):
    with open(tsv_file) as f:
        content = f.readlines()
        with open(label_file) as l:
            labels = csv.reader(l,delimiter=',') 
            i = 0
            for label in labels: 
                if label[1].strip() == '0':
                    if benign == True:
                        sys.stdout.write(content[i])  
                else:
                    if benign == False:
                        sys.stdout.write(content[i])  
                i += 1



if __name__ == '__main__': 

    if len(sys.argv) < 4:
        print("Usage:"+ sys.argv[0] +" <infile.tsv> <label.lb> <0|1> \n 0: pick 0 samples, 1: pick 1 samples")
        exit(1)
    tsv_file = sys.argv[1]
    label_file = sys.argv[2]
    if sys.argv[3] == "0":
        benign = True
    elif sys.argv[3] == "1":
        benign = False
    else:
        print("Usage: sys.argv[0] <infile.tsv> <label.lb> <0|1> \n 0: negative sample, 1: positive sample")
        exit(1)
        
    filter(tsv_file, label_file, benign)

