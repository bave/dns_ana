# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
[q1]___[q2]___[q3]____
<--------------------> : total connection time
                  <--> : conn_time
<-->                   : session create count count

- map
map['ip_1'] = [timeline,,,,,,,,,,]
map['ip_2'] = [timeline,,,,,,,,,,]
      :
map['ip_n'] = [timeline,,,,,,,,,,]

- timeline
 0: no connection
 1: create connection
 2: keep connection
"""

import os
import sys
import copy
import pickle

def write_file(path, p1, p2):
    f = open(path, 'w')
    if len(p1) == len(p2):
        for i in range(len(p1)):
            f.write(str(p1[i]) + " " + str(p2[i]) + "\n")
        print path, " write success"
    else:
        print path, " write failed"

    f.close()
    return

def proc_total_time(conn_times):
    total_time = []
    count = 0
    for i in conn_times:
        if (i > 0):
            count += 1
            total_time.append(count)
        else:
            count = 0
            total_time.append(count)

    return total_time

def proc_conn_time(f, conn_time):

    ONE_DAY = 86400
    timeline = []
    for i in range(ONE_DAY):
        timeline.append(0)

    for i in f:
        line = i.replace('\n', '').split(' ')[0].split('.')
        #if (timeline[int(line[0])] == 1):
        #    print "dup"
        timeline[int(line[0])] = 1

    keep_count = conn_time + 1
    for i in range(len(timeline)):
        if timeline[i] == 0:
            keep_count += 1
            if keep_count <= conn_time:
                timeline[i] = 2
        elif timeline[i] > 0:
            keep_count = 0

    return timeline


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
    path_each_ips = file_prefix+".each_ip"
    list = os.listdir(path_each_ips)
    for file in list:
        files.append(file)

    path_timelines = file_prefix + "_" + str(conn_time) + ".timeline"
    if not os.path.exists(path_timelines):
        os.mkdir(path_timelines)


    for i in files:
        print i
        f = open(path_each_ips+"/"+i, 'r')
        conn_times = proc_conn_time(f, conn_time)
        total_times = proc_total_time(conn_times)
        #print len(conn_times)
        #print len(total_times)
        write_file(path_timelines+"/"+i, conn_times, total_times)
        f.close()

    return

#end_def

if __name__ == '__main__':
    main()

