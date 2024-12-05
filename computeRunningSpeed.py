from ChgModbusLib import pyZerovaChgrModbus
import time
import matplotlib.pyplot as plt


modbus = pyZerovaChgrModbus()
modbus.connect('192.168.10.150', "")

total_time = 0
num_of_loop = 100
#time_elapsed_list = []

for i in range(num_of_loop):
    start = time.time()
    modbus.writeConfig([1, 0, 0, 0, 0])
    #modbus.readConfig()
    end = time.time()
    time_elapsed = end - start
    #time_elapsed_list.append(time_elapsed) 
    total_time += time_elapsed
    print(time_elapsed)


print("average running time:", total_time/num_of_loop)
# Plot the time_elapsed as a line chart
# plt.figure(figsize=(10, 6))
# plt.plot(range(num_of_loop), time_elapsed_list, marker='o', linestyle='-')
# plt.title('Execution Time for Each Loop Iteration')
# plt.xlabel('Iteration')
# plt.ylabel('Time Elapsed (seconds)')
# plt.grid()
# plt.show()