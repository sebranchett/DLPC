import matplotlib.pyplot as plt
from csv import reader
from datetime import datetime, timedelta

with open('output.csv', newline='') as f:
    data_reader = reader(f)
    data = list(data_reader)

temps = [float(item[1]) for item in data]
times = [item[0] for item in data]
plt.plot(times, temps, marker = 'o')

print(times)
lower_date = datetime.strptime(times[0],"%X").replace(second=0,microsecond=0)
date_list = [lower_date + timedelta(minutes=x) for x in range(3)]
time_list = [str(x.time()) for x in date_list]
print(time_list)
plt.xticks(time_list)
plt.yticks(range(0, 81, 10))
plt.show()
