#!/usr/bin/env python
# coding=utf-8
import sys
import os
import csv

ip=[]
def split(tsv_file):
    with open(tsv_file) as l:
        lines = csv.reader(l,delimiter='\t') 
        for line in lines: 
            ip.append(line[4])
    ip_set=set(ip)
    print(ip_set)



if __name__ == '__main__': 

    if len(sys.argv) < 2:
        print("Usage:"+ sys.argv[0] +" <infile.tsv>")
        exit(1)
    tsv_file = sys.argv[1]
    split(tsv_file)

