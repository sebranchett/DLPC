#!/usr/bin/python

import sys
from mpi4py import MPI
from csv import writer
import random
from numpy import shape, reshape

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
print('number of points per rank will be', points_per_rank)

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
    #SEB print('results are',results)
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
