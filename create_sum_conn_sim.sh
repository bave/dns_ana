#!/bin/sh

for i in `seq 1 1 30`
do
    echo "python sum_conn_sim.py nsjaist.pcap ${i}"
    eval "/usr/bin/python ./sum_conn_sim.py ./nsjaist.pcap ${i}"
done
