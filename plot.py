import matplotlib.pyplot as plt
from csv import reader
from datetime import datetime, timedelta
from operator import itemgetter

# read and sort time and temperature data from a csv file
with open('output.csv', newline='') as f:
    data_reader = reader(f)
    data = list(data_reader)
data = sorted(data, key= itemgetter(0))

# convert temperatures to real numbers
temps = [float(item[1]) for item in data]

# convert times to seconds from start of first minute
time_labels = [item[0] for item in data]
lower_date = datetime.strptime(time_labels[0],"%X").replace(second=0,microsecond=0)
time_vals = [(datetime.strptime(i,"%X") - lower_date).seconds for i in time_labels]

# create convenient tick marks and their labels
tick_at = []
tick_label = []
for step in range(3):
    tick_at.append(0 + step*60)
    tick_label.append(str((lower_date + timedelta(seconds=60*step)).time()))

# plot the data
plt.plot(time_vals, temps, marker = 'o')
plt.title('Temperature of master node DLPC')
plt.xlabel('Time')
plt.ylabel('Temperature (degrees Celcius)')
plt.xticks(tick_at,tick_label)
plt.yticks(range(0, 81, 10))
plt.show()
