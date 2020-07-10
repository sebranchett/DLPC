#!/usr/bin/python

import sys
from mpi4py import MPI
import random
from numpy import shape, reshape, where

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

def calculate_pi(points_per_rank):
    """ calculate pi from random points inside or outside a quarter circle

    Each rank generates points_per_rank random points on the surface of a
    unit square and determines if they lie in a circle of r=1 using Pythagoras.
    The ratio of points inside the circle and outside is used by the 0th rank
    to estimate the value of pi:
    points in quarter circle / all points in unit (quarter) square ~=
    points in circle / points in square of sides 2r ~=
    area of circle / area of square =
    pi * r^2 / (2r)^2 =
    pi / 4
    pi ~= 4 * points in quarter circle / all points

    This 'fastest' version only returns the number of points inside the circle
    to the manager node. The manager node does not know the coordinates and
    cannot output them to a csv or png file.
    """
    results = 0

    if (rankid == 0):
        start = MPI.Wtime()

    for point in range(points_per_rank):

    # generate a random point in 2D between 0 and 1
    # this is a quater of a circle/square
        x = random.random()
        y = random.random()

    # is this point inside (1) or outside (0) a circle of radius 1 with center (0,0)
        if (x*x + y*y) <= 1.:
            results += 1

    # gather the results from the ranks
    results = comm.gather(results, root = 0)

    # calculate pi
    if (rankid == 0):
        mysum = sum(i for i in results)
        npoints = points_per_rank * nranks
        pi = 4. * mysum / npoints
        print('number of points is',npoints)
        print('estimate of pi is',pi)

        # display the time required to process log files
        end = MPI.Wtime()
        runtime = end - start
        print('Runtime is ',runtime)

    return

if __name__ == '__main__':
    
    min_no_of_points = 30
    my_seed = None

    # optional argument provided is the minimum number of points
    # if this number is not divisible by nranks, the no. or points will be larger
    if len(sys.argv) > 1: min_no_of_points = int(sys.argv[1])

    # optional second argument provided is the seed to create random numbers
    if len(sys.argv) > 2: my_seed = int(sys.argv[2])+rankid
    random.seed(my_seed)

    # calculate the number of points per rank
    points_per_rank = int(min_no_of_points / nranks)
    if min_no_of_points % nranks != 0: points_per_rank += 1

    calculate_pi(points_per_rank)
