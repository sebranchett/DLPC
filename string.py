from os import listdir, rename, remove
from time import sleep
from mpi4py import MPI

comm = MPI.COMM_WORLD
nranks = comm.Get_size()
rankid = comm.Get_rank()

max_no_of_cylces = 3
all_times_temps = []

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

    times_temps = []

# This is where the work is done

    times_temps = [filenames[11:19].replace("_",":"), filecontents[5:7]]

    times_temps = comm.gather(times_temps, root = 0)

    if (rankid == 0):
        for i, time_temp in enumerate(times_temps):
            if time_temp != ['', '']:
                all_times_temps = all_times_temps + time_temp
        print('Gathered times and temps are',all_times_temps)

if (rankid == 0):
    end = MPI.Wtime()
    runtime = end - start
    print('Runtime is ',runtime)
