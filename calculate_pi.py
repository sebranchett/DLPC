#!/usr/bin/python

import sys
from mpi4py import MPI
from csv import writer
import random
from numpy import shape, reshape, where
import matplotlib.pyplot as plt

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

min_no_of_points = 30

# optional argument provided is the minimum number of points
# if this number is not divisible by nranks, the no. or points will be larger
if len(sys.argv) > 1: min_no_of_points = int(sys.argv[1])

# calculate the number of points per rank
points_per_rank = int(min_no_of_points / nranks)
if min_no_of_points % nranks != 0: points_per_rank += 1

results = []

if (rankid == 0):
    start = MPI.Wtime()

for point in range(points_per_rank):

# generate a random point in 2D between 0 and 1
# this is a quater of a circle/square
    x = random.random()
    y = random.random()

# is this point inside (1) or outside (0) a circle of radius 1 with center (0,0)
    if (x*x + y*y) <= 1.:
        circle = 1
    else:
        circle = 0

    result = [point, rankid, x, y, circle]
    results.append(result)

# gather the results from the ranks
results = comm.gather(results, root = 0)

# calculate pi
if (rankid == 0):
    results = reshape(results, (-1,5))
    pi = 4. * results.sum(axis=0)[-1] / shape(results)[0]
    print('number of points is',shape(results)[0])
    print('estimate of pi is',pi)

# display the time required to process log files
if (rankid == 0):
    end = MPI.Wtime()
    runtime = end - start
    print('Runtime is ',runtime)

# output the results
if (rankid == 0):
    with open("pi.csv", "w", newline="") as f:
        graph_writer = writer(f)
        graph_writer.writerows(results)

    inside_circle = results[where(results[:,4] == 1)]
    outside_circle = results[where(results[:,4] != 1)]
    data = (inside_circle, outside_circle)
    colors = ("blue", "orange")
    groups = ("inside circle", "outside circle")

    fig = plt.figure(1, figsize=(6, 6))
    ax = fig.add_subplot(1, 1, 1)

    for data, color, group in zip(data, colors, groups):
        ax.scatter(data[:,2], data[:,3], c=color, label=group, marker="x")

    plt.title('Estimate of pi with '+str(shape(results)[0])+' points is '+\
              str(pi))
    plt.legend(loc=2)
    plt.show()
