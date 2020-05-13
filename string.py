from os import listdir, rename, remove
from time import sleep
from mpi4py import MPI

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
        filenames=listdir('./logs')[:nranks]
        filecontents = []
        cleanup = []
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

    filenames = comm.scatter(filenames, root = 0)
    filecontents = comm.scatter(filecontents, root = 0)

    times = []
    temps = []

# This is where the work is done

    temps = filecontents[5:7]
    times = filenames[11:19].replace("_",":")

    temps = comm.gather(temps, root = 0)
    times = comm.gather(times, root = 0)

    if (rankid == 0):
        print('Gathered times and temps are',times,temps)

if (rankid == 0):
    end = MPI.Wtime()
    runtime = end - start
    print('Runtime is ',runtime)
