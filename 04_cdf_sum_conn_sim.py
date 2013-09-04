#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pylab import *

def psum(x):
    x.sort()
    y = []
    step = float(100)/len(x)
    for i in range(1, len(x)+1):
        y.append(i*step)
    return y


def open_x(filename):
    ret = [] 
    for l in open(filename, 'r'):
        line = int(l.replace('\n', ''))
        if (line != 0):
            ret.append(line)
        #ret.append(line)
    ret.sort()
    return ret


if len(sys.argv) != 2:
    print "python cdf_sum_conn_sim.py [file_prefix]"
    sys.exit(1);


file_prefix = sys.argv[1]
files = []
label = []
x=[]
y=[]
for i in range(1, 31):
    label.append(str(i) + " [sec]")
    files.append(file_prefix + ".sum/" +file_prefix + "_" + str(i) + ".sum")

for i in files:
    x.append(open_x(i))

for i in x:
    y.append(psum(i))

rcParams['figure.facecolor'] = 'w'
rcParams['legend.numpoints'] = 2
rcParams['font.size'] = 20
rcParams['legend.fontsize'] = 14
rcParams['lines.linewidth'] = 2

for i in range(len(files)):
    print files[i]
    plot(x[i], y[i], label=label[i])


v = [None, None, 0, 100]
axis(v)

title("Cumulative Distribution Function", fontname='serif')
legend(loc='upper right')
xlabel("Number of Connections")
ylabel("percentage:%")

#savefig('png/' + savename + '.png')
#savefig('eps/' + savename + '.eps')
show()

