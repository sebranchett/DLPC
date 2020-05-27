import matplotlib.pyplot as plt
from csv import reader

with open('output.csv', newline='') as f:
    data_reader = reader(f)
    data = list(data_reader)

temps = [float(item[1]) for item in data]
times = [item[0] for item in data]
print(temps)
print(times)
plt.plot(times, temps, marker = 'o')

plt.xticks(times)
plt.yticks(temps)
plt.axis([None, None, 0, 40])
plt.show()
