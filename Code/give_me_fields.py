#!/usr/bin/env python
# coding=utf-8

import netStat2 as ns
import csv
import numpy as np
import sys
#/usr/bin/tshark -r $1 -T fields -e [0]frame.time_epoch -e [1]frame.len -e [2]eth.src -e [3]eth.dst -e [4]ip.src -e [5]ip.dst -e [6]ip.hdr_len -e [7]ip.len -e [8]ip.flags.rb -e [9]ip.flags.df -e [10]ip.flags.mf -e [11]ip.ttl -e [12]tcp.srcport -e [13]tcp.dstport -e [14]tcp.seq -e [15]tcp.ack -e [16]tcp.flags.res -e [17]tcp.flags.ack -e [18]tcp.flags.cwr -e [19]tcp.flags.ecn -e [20]tcp.flags.fin -e [21]tcp.flags.ns -e [22]tcp.flags.push -e [23]tcp.flags.reset -e [24]tcp.flags.syn -e [25]tcp.flags.urg -e [26]tcp.window_size_value -e [27]tcp.urgent_pointer -e [28]udp.length -e [29]udp.srcport -e [30]udp.dstport -e [31]icmp.type -e [32]icmp.code -e [33]arp.opcode -e [34]arp.src.hw_mac -e [35]arp.src.proto_ipv4 -e [36]arp.dst.hw_mac -e [37]arp.dst.proto_ipv4 -e [38]http.request.method -e [39]http.request.uri -e [40]http.request.version -e [41]http.response.code -e [42]http.host -e [43]http.connection -e [44]ipv6.src -e [45]ipv6.dst -e i[46]pv6.dstopts.nxt -e [47]ipv6.flow -e [48]ipv6.tclass -e [49]ipv6.tclass.dscp -e [50]ipv6.tclass.ecn -e [51]ipv6.hlim -e [52]ipv6.version -e [53]ipv6.plen

HeadTable = {
    "time"      :       [0],
    "flen"      :       [1],
    "esrc"      :       [2],
    "edst"      :       [3],
    "ipsrc"     :       [4],
    "ipdst"     :       [5],
    "iplen"     :       [7],
    "tcpsport"  :       [12],
    "tcpdport"  :       [13],
    "udpsport"  :       [29],
    "udpdport"  :       [30],
    "ip6src"    :       [31],
    "ip6dst"    :       [45],
    "arpipsrc"  :       [35],
    "arpipdst"  :       [36],
    "srcport"   :       [12,29],
    "dstport"   :       [13,30]
}

maxInt = sys.maxsize
decrement = True
while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt / 10)
        decrement = True

# filters is a list as follows:
# filters = [
#   { 4 : "192.168.1.1" },          # only consider srcip
#   { 5 : "192.168.1.2" },          # only consider dstip
#   { 12: "62112", 13: "62112"},    # consider tcp.srcport=62112 or udp.srcport=62112
#    {... }
#  ]
#  
#  This functions matches the record in the infile with the filters. 
#
#
def createTSV(path, filters):
    with open(path, 'rt', encoding="utf8") as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        # For each row
        for row in tsvin:
            output = True 
            # Check each filter
            for filter in filters: 
                filter_key = ""
                filter_value = ""
                row_value = ""
                # for each filter, check each field. 
                for key, value in filter.items():
                    filter_value += value
                    row_value += row[key]
                if filter_value != row_value:
                    output = False
                    break 
            if output == True:
                r = row[0]
                for field in row[1:]:
                    r += '\t' + field
                print(r)
    
# filters is a list as follows:
# filters = [
#   { 4 : "192.168.1.1" },          # only consider srcip
#   { 5 : "192.168.1.2" },          # only consider dstip
#   { 12: "62112", 13: "62112"},    # consider tcp.srcport=62112 or udp.srcport=62112
#    {... }
#  ]
#
# This functions create a label file according to the filters. 
# If a record mathces the filter, the label file will output a '1',
# otherwise the label file will output a '0' for that record. 
#
def createLebel(path, filters):
    with open(path, 'rt', encoding="utf8") as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        # For each row
        for row in tsvin:
            output = True 
            # Check each filter
            for filter in filters: 
                filter_key = ""
                filter_value = ""
                row_value = ""
                # for each filter, check each field. 
                for key, value in filter.items():
                    filter_value += value
                    row_value += row[key]
                if filter_value != row_value:
                    output = False
                    break 
            if output == True:
                print("1")
            else:
                print("0")

def make_filters(path):
    filters = []
    with open(path, 'rt', encoding="utf8") as tsvin:
        tsvin = csv.reader(tsvin) 
        for row in tsvin:
            fields = HeadTable[row[0]]
            filter = {}
            count = len(fields)
            i = 0 
            while (i < count):
                filter[fields[i]] = row[i+1]
                i += 1
            filters.append(filter) 
    return filters 


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " <filter.ft> <infile.tsv>")
        exit(0)
    filters = make_filters(sys.argv[1])
    createTSV(sys.argv[2], filters) 
