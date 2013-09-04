# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
"""

import os
import sys
import copy
import pickle

def write_file(path, p1):
    f = open(path, 'w')
    for i in range(len(p1)):
        f.write(str(p1[i]) + "\n")
    f.close()
    return

def array_sum(a, b):
    if (len(a)==len(b)):
        return [a[i]+b[i] for i in range(len(a))]
    else:
        return "error"
#end_def

def array_sub(a, b):
    if (len(a)==len(b)):
        return [a[i]-b[i] for i in range(len(a))]
    else:
        return "error"
#end_def


def usage():
    print u"python %s [file_prefix] [conn_time]" % sys.argv[0]
    # file_prefix
    # hoge_file.each_ip -> hoge_file
    # nsjaist.pcap_ecah_ip -> nsjaist.pacp 
    return
#end_def

def main():

    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    file_prefix = sys.argv[1]
    if file_prefix == None:
        sys.exit(1)

    conn_time = int(sys.argv[2])
    if conn_time == None:
        sys.exit(1)

    files = []
    path_timelines = file_prefix + "_" + str(conn_time) + ".timeline"
    list = os.listdir(path_timelines)
    for file in list:
        files.append(file)

    ONE_DAY = 86400
    total_connection = []
    for i in range(ONE_DAY):
        total_connection.append(0)

    for i in files:
        print i
        f = open(path_timelines+"/"+i, 'r')
        tmp = []
        for j in f:
            line = j.replace('\n', '').split(' ')[0]
            if (int(line) > 0):
                tmp.append(1)
            else:
                tmp.append(0)
        total_connection = array_sum(total_connection, tmp)
        f.close()
        #print total_connection
        #print len(total_connection)
        write_file(file_prefix + ".sum/" +file_prefix + "_" + str(conn_time) + ".sum", total_connection)
    return

#end_def

if __name__ == '__main__':
    main()

