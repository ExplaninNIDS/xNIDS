#!/usr/bin/env python
# coding=utf-8
import parser_script as ps
import sys
import numpy as np 

'''
Whether header fields exsit or not does not matter.
If header fields exist, 

'''

def tsv2csv(infile, outfile):
    X,Ts,srcIPs=ps.loadTSV(infile)
    print ("File size: " + str(X.shape))
    np.savetxt(outfile,X,delimiter=',',newline='\n') 
    print ("File saved to: " + outfile)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage:"+ sys.argv[0] +" <infile.tsv> <outfile.csv> ")
        exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
        
    tsv2csv(infile, outfile)



