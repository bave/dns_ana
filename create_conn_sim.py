#!/bin/sh

for i in `seq 1 1 30`
do
    echo "python conn_sim.py nsjaist.pcap ${i}"
    eval "/usr/bin/python ./conn_sim.py ./nsjaist.pcap ${i}"
done
