#!/usr/bin/python

import sys
from mpi4py import MPI
from csv import writer
import random
from numpy import shape, reshape, where
try:
    import matplotlib.pyplot as plt
except:
    pass

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

def export_results(results, npoints, pi):
    """Export results to a csv file and create and export a graph.
    
    The csv contains the result columns:
    point index, rank index, x-coordinate, y-coordinate, boolean inside circle?
    The graph plots points inside the circle in blue and points outside
    in orange. The calculation and the graph show only one quadrant.
    npoints is used here to label the graph and the output files.
    pi is used here to label the graph with the estimate of pi.
    """
    filename = 'pi_estimate_'+str(npoints)+'_points.csv'
    with open(filename, "w", newline="") as f:
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

    plt.title('Estimate of pi with '+str(npoints)+' points is '+\
              str(pi))
    plt.legend(loc=2)
    filename = 'pi_estimate_'+str(npoints)+'_points.png'
    plt.savefig(filename)
    return

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
    """
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
        npoints = shape(results)[0]
        pi = 4. * results.sum(axis=0)[-1] / npoints
        print('number of points is',npoints)
        print('estimate of pi is',pi)

        # display the time required to process log files
        end = MPI.Wtime()
        runtime = end - start
        print('Runtime is ',runtime)

        # output the results
        export_results(results, npoints, pi)

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
