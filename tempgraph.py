from os import listdir, rename, remove
from time import sleep
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

max_no_of_cylces = 3

if (rankid == 0):
    start = MPI.Wtime()

for icycles in range(max_no_of_cylces):
    
    if (rankid == 0):
        while not listdir('./logs'):
            sleep(1)
        all_filenames = np.array(listdir('./logs'), dtype=object)
        filecontents = np.array([], dtype=object)
        filenames = np.array([], dtype=object)
        for filename in all_filenames:
            print(filename)
            if filename.endswith('.log'):
                f = open(filename, "r")
                filecontents = np.append(filecontents, f.read())
                f.close()
                filenames = np.append(filenames, filename)
                rename('./logs/'+filename, './old_logs/'+filename)
                print(filecontents)
            else:
                print('clean up', filename)
                remove('./logs/'+filename)
        nfiles = len(filenames)
        if nfiles != len(filecontents): print('Something went wrong with read')
        comm.bcast(nfiles)
    else:
        filenames = np.array([], dtype=object)
        filecontents = np.array([], dtype=object)
        nfiles = comm.bcast(None)

    if (rankid == 0):
        print('no. filenames is',nfiles)
        print('Input filenames are', filenames)

    m = int(nfiles / nranks)
    print('m is ',m)

    recvnames = np.empty(m, dtype=object)
    recvcontents = np.empty(m, dtype=object)
    filenames = comm.Scatter(filenames, recvnames, root = 0)
    filecontents = comm.Scatter(filecontents, recvcontents, root = 0)

    times = []
    temps = []

# This is where the work is done

    print('rank, filenames, filecontents', rank, filenames, filecontents)
    times = filenames[11:19].replace("_",":")
    temps = filecontents[5:7]

    recvbuf = None
    if rank == 0:
        recvbuf = np.empty([size, 100], dtype=object)
        comm.Gather(sendbuf, recvbuf, root=0)
    times = comm.Gather(times, recvbuf, root = 0)
    temps = comm.Gather(temps, recvbuf, root = 0)

    if (rankid == 0):
        print('Gathered times and temps are',times,temps)

if (rankid == 0):
    end = MPI.Wtime()
    runtime = end - start
    print('Runtime is ',runtime)
