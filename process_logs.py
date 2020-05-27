#!/usr/bin/python

import sys
from os import listdir, rename, remove
from time import sleep
from mpi4py import MPI
from csv import writer

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

seconds_to_process = 1
max_no_of_cycles = 3

if len(sys.argv) > 1: seconds_to_process = int(sys.argv[1])
if len(sys.argv) > 2: max_no_of_cycles = int(sys.argv[2])
print('seconds_to_process is ',seconds_to_process,'max_no_of_cycles is ',max_no_of_cycles)

if (rankid == 0):
    start = MPI.Wtime()
    all_times_temps = []

for icycles in range(max_no_of_cycles):
    
# prepare log files, as many as there are, up to one per rank
    if (rankid == 0):
        # check the logs directory every second until it's not empty
        while not listdir('./logs'):
            sleep(1)
        filenames=listdir('./logs')[:nranks]
        filecontents = []
        cleanup = []

# move log files to old_logs folder and delete non-log files
        for filename in filenames:
            if filename.endswith('.log'):
                f = open(filename, "r")
                filecontents.append(f.read())
                f.close()
                rename('./logs/'+filename, './old_logs/'+filename)
            else:
                print('clean up', filename)
                remove('./logs/'+filename)
                cleanup.append(filename)

# tidy up the list of file names to process
        for filename in cleanup:
            filenames.remove(filename)
        nfiles = len(filenames)
        if nfiles != len(filecontents): print('Something went wrong with read')

# fill up ranks with empty filenames and contents to avoid scatter error
        while (nfiles < nranks):
            filenames.append("")
            filecontents.append("")
            nfiles = len(filenames)
    else:
        filenames = None
        filecontents = None

    if (rankid == 0):
        print('no. filenames is',nfiles)
        print('Input filenames are', filenames)

# distribute the files over the ranks
    filenames = comm.scatter(filenames, root = 0)
    filecontents = comm.scatter(filecontents, root = 0)

# 'process' the log files - time delay simulates the processing time
    sleep(seconds_to_process)
    times_temps = [filenames[11:19].replace("_",":"), filecontents[5:7]]

# gather the results from the ranks
    times_temps = comm.gather(times_temps, root = 0)

# tidy up the empty filenames which were added to avoid scatter error
    if (rankid == 0):
        for time_temp in times_temps:
            if time_temp != ['', '']:
                all_times_temps.append(time_temp)
# output the results
        print('Gathered times and temps are',all_times_temps)
        with open("output.csv", "w", newline="") as f:
            graph_writer = writer(f)
            graph_writer.writerows(all_times_temps)

# display the time required to process log files
if (rankid == 0):
    end = MPI.Wtime()
    runtime = end - start
    print('Runtime is ',runtime)
