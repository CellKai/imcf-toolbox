#!/usr/bin/env python

"""
Draws spots of a sine curve over time at a given sampling rate, plus
a straight calibration line marking the sampling time. Includes the
graph of the sine curve on request.
"""

from pylab import *
import sys
import argparse

argparser = argparse.ArgumentParser(description=__doc__)
argparser.add_argument('-d', '--delta', type=float, default='3',
    help='factor to multiply stepsize (default=3)')
argparser.add_argument('--orig', dest='draw_orig', action='store_const',
    const=True, default=False,
    help='draw original graph (default=False)')
argparser.add_argument('--aux', dest='draw_aux', action='store_const',
    const=True, default=False,
    help='draw auxiliary line (default=False)')
args = argparser.parse_args()

range_max = 6.0
stepsize = 0.01

t1 = np.arange(0.0, range_max, stepsize)
t2 = np.arange(0.0, range_max, stepsize * args.delta)

signal = sin(2*pi*t1)
sampled = sin(2*pi*t2)

# set the figure size
plt.figure(1, figsize=(14,7))

# we could draw both charts in one command, but by doing it with
# separate calls it is easy to disable parts of the graph:
if args.draw_orig:
    plt.plot(t1, signal, linewidth=2.0)
plt.plot(t2, sampled, 'ro', markersize=10)
if args.draw_aux:
    auxline1 = -1.1 * (t1 / t1)
    auxline2 = -1.1 * (t2 / t2)
    plt.plot(t1, auxline1, linewidth=2.0)
    plt.plot(t2, auxline2, 'bs', markersize=8)

# explicitly set an axis range so we can create comparable graphs:
ylim([-1.2,1.2])

xlabel('time (s)')
ylabel('signal ')
title('Continuous signal over time.')
grid(True)
show()
