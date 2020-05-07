from os import listdir, rename, remove
from time import sleep

for ifiles in range(3):
    while not listdir('./logs'):
        sleep(1)
    
    filename=listdir('./logs')[0]
    
    if filename.endswith('.log'):
        print('assign file to slave', filename)
        f = open(filename, "r")
        line = f.read()
        f.close()
    
        tempdeg = line[5:7]
        print("Temperature is ",tempdeg,"'C")
    
        timestamp = filename[11:19].replace("_",":")
        print("Time stamp is ",timestamp)
    
        print(timestamp,tempdeg)
    
        rename('./logs/'+filename, './old_logs/'+filename)
    else:
        print('clean up')
        remove('./logs/'+filename)
