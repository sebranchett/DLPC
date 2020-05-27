import matplotlib.pyplot as plt
from csv import reader

with open('output.csv', newline='') as f:
    data_reader = reader(f)
    data = list(data_reader)

temps = [item[1] for item in data]
times = [item[0] for item in data]
plt.plot(times, temps)

# plt.ylim((20,80))
plt.show()
