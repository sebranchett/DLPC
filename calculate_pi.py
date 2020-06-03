#!/usr/bin/python

import sys
from mpi4py import MPI
from csv import writer
import random
from numpy import shape, reshape

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

max_no_of_iterations = 30

# optional argument provided is the maximum number of iterations
# note that in each iteration cycle, nranks points will be used to calculate pi
if len(sys.argv) > 1: max_no_of_iterations = int(sys.argv[1])
print('number of iterations will be', max_no_of_iterations)

results = []

if (rankid == 0):
    start = MPI.Wtime()

for iteration in range(max_no_of_iterations):

# generate a random point in 2D between 0 and 1
# this is a quater of a circle/square
    x = random.random()
    y = random.random()

# is this point inside (1) or outside (0) a circle of radius 1 with center (0,0)
    if (x*x + y*y) <= 1.:
        circle = 1
    else:
        circle = 0

    result = [iteration, rankid, x, y, circle]
    results.append(result)

# gather the results from the ranks
results = comm.gather(results, root = 0)

# output the results
if (rankid == 0):
    results = reshape(results, (-1,5))
    print('results are',results)
    print('sum of columns is',results.sum(axis=0))
    print('number inside circle is',results.sum(axis=0)[-1])
    print('number of points is',shape(results)[0])
    pi = 4. * results.sum(axis=0)[-1] / shape(results)[0]
    print('estimate of pi is',pi)
    with open("pi.csv", "w", newline="") as f:
        graph_writer = writer(f)
        graph_writer.writerows(results)

# display the time required to process log files
if (rankid == 0):
    end = MPI.Wtime()
    runtime = end - start
    print('Runtime is ',runtime)
