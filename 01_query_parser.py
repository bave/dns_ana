# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
カレントディレクトリに"pcap_filename.each_ip"ディレクトリを作りその下に
送信元IPアドレス毎のファイルを作成しクエリネームを列挙する
"""

import sys
import dpkt
import os
import socket
from pylab import *
from datetime import *

def usage():
    print u"python %s [filename]" % sys.argv[0]
    return
#end_def


def main():

    write_on = 1
    global first_time

    if (len(sys.argv) != 2):
        usage()
        return 1
    #end_if

    filename = sys.argv[1]
    if filename == None:
        return -1

    try:
        pcr = dpkt.pcap.Reader(open(filename,'rb'))
    except:
        return -1

    packet_count = 0
    s = set()

    ret_dir = filename + ".each_ip"
    if not os.path.exists(ret_dir):
        os.mkdir(ret_dir)


    for (ts, buf) in pcr:

        if (packet_count == 0):
            first_time = ts
        elif ((packet_count%100000) == 0):
            current = str(ts-first_time) + '\n'
            sys.stderr.write(current)

        packet_count += 1

        try:
            eth = dpkt.ethernet.Ethernet(buf)
            if type(eth.data) != dpkt.ip.IP and type(eth.data) != dpkt.ip6.IP6:
                eth = dpkt.loopback.Loopback(buf)
        except:
            continue
        #end_try

        if type(eth.data) == dpkt.ip.IP:
            packet = eth.data
            src_ip = socket.inet_ntoa(packet.src)
            dst_ip = socket.inet_ntoa(packet.dst)
            segment = packet.data

            if type(packet.data) == dpkt.udp.UDP:
                src_port = segment.sport
                dst_port = segment.dport
                if dst_port == 53:
                    write_file(ret_dir, src_ip, ts, dnsparser(segment.data), write_on)
                continue

            elif type(packet.data) == dpkt.tcp.TCP:
                src_port = segment.sport
                dst_port = segment.dport
                flags = segment.flags
                continue
            #end_if

            #print 'src_port: ', src_port, ', ' 'dst_port: ', dst_port

        elif type(eth.data) == dpkt.ip6.IP6:
            packet = eth.data
            src_ip = socket.inet_ntop(socket.AF_INET6, packet.src)
            dst_ip = socket.inet_ntop(socket.AF_INET6, packet.dst)
            segment = packet.data

            if type(packet.data) == dpkt.udp.UDP:
                src_port = segment.sport
                dst_port = segment.dport
                if dst_port == 53:
                    write_file(ret_dir, src_ip, ts, dnsparser(segment.data), write_on)
                continue

            elif type(packet.data) == dpkt.tcp.TCP:
                src_port = segment.sport
                dst_port = segment.dport
                flags = segment.flags
                continue
            #end_if

        #end_if

    #end_for


#end_def

def write_file(ret_dir, src_ip, ts, parse_info, on):
    ts_string = str(ts - first_time)
    if on:
        f = open(ret_dir + '/' + src_ip, 'a')
        f.write(ts_string + " "  + parse_info + '\n')
        f.close()
    else:
        print ts_string + " "  + parse_info

def dnsparser(data):
    try:
        dns = dpkt.dns.DNS(data)
        if dns.opcode == dpkt.dns.DNS_QUERY:
            name = dns.qd
            return name[0].name
        else:
            raise
    except:
        return "error"
#end_def

if __name__ == '__main__':
    main()

