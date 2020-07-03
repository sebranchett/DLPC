#!/usr/bin/python

import sys
from os import listdir, rename, remove
from time import sleep
from mpi4py import MPI
from csv import writer

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

def collect_files(nranks):
    """Prepare log files, as many as there are, up to one per rank

    Only the manager node performs this file manipulation
    """
    # check the logs directory every second until it's not empty
    while not listdir('./logs'):
        sleep(1)
    filenames=listdir('./logs')[:nranks]
    filecontents = []
    cleanup = []
    
    # move log files to old_logs folder and delete non-log files
    for filename in filenames:
        if filename.endswith('.log'):
            f = open('./logs/'+filename, "r")
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
    if nfiles != len(filecontents):
        print('Something went wrong with read')
    
    # fill up ranks with empty filenames and contents to avoid
    # scatter error
    while (nfiles < nranks):
        filenames.append("")
        filecontents.append("")
        nfiles = len(filenames)

    print('no. filenames is',nfiles)
    print('Input filenames are', filenames)

    return(filenames, filecontents)


def process_files(seconds_to_process, max_no_of_cycles):
    """Process 'real time' log files
    
    Extracting temperature from log files and write the time and
    temperature to a csv file
    seconds_to_process represents the time to process data
    max_no_of_cycles is the number of times to search for unprocessed log files
    """

    if (rankid == 0): all_times_temps = []
    for icycles in range(max_no_of_cycles):
        
        if (rankid == 0):
            filenames, filecontents = collect_files(nranks)
        else:
            filenames = None
            filecontents = None
    
        # distribute the files over the ranks
        filenames = comm.scatter(filenames, root = 0)
        filecontents = comm.scatter(filecontents, root = 0)
    
        # 'process' the log files - time delay simulates the processing time
        sleep(seconds_to_process)
        times_temps = [filenames[11:19].replace("_",":"), filecontents[5:9]]
    
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

if __name__ == '__main__':

    seconds_to_process = 1
    max_no_of_cycles = 3

    # first optional argument is the number of seconds that represents
    # the processing of data
    if len(sys.argv) > 1: seconds_to_process = int(sys.argv[1])

    # the second optional argument is the number of processing cycles
    # before ending the job
    if len(sys.argv) > 2: max_no_of_cycles = int(sys.argv[2])

    print('seconds_to_process is ',seconds_to_process,'max_no_of_cycles is ',
          max_no_of_cycles)

    # intialise the manager node
    if (rankid == 0):
        start = MPI.Wtime()

    # process the 'real time' log files
    process_files(seconds_to_process, max_no_of_cycles)

    # display the time required to process log files
    if (rankid == 0):
        end = MPI.Wtime()
        runtime = end - start
        print('Runtime is ',runtime)
