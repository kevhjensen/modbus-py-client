# from ChgModbusLib import pyZerovaChgrModbus
# import time
# #import matplotlib.pyplot as plt


# modbus = pyZerovaChgrModbus()
# modbus.connect('192.168.100.1', "")

# total_time = 0
# num_of_loop = 100
# #time_elapsed_list = []
# setPoints = [60, 50, 60, 55, 50, 55, 60, 59, 58, 57, 56, 55, 56, 57, 58, 59, 60]

# for sP in setPoints:
#     start = time.time()
#     modbus.writeConfig([0, 0, 0, sP, 0])
#     #modbus.readConfig()
#     end = time.time()
#     time_elapsed = end - start
#     #time_elapsed_list.append(time_elapsed) 
#     valid, data = modbus.get_connector_info(5)
#     #print(data)
#     total_time += time_elapsed
#     print(time_elapsed)


# print("average running time:", total_time/num_of_loop)
# # Plot the time_elapsed as a line chart
# # plt.figure(figsize=(10, 6))
# # plt.plot(range(num_of_loop), time_elapsed_list, marker='o', linestyle='-')
# # plt.title('Execution Time for Each Loop Iteration')
# # plt.xlabel('Iteration')
# # plt.ylabel('Time Elapsed (seconds)')
# # plt.grid()
# # plt.show()