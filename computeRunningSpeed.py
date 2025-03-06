from ChgModbusLib import pyZerovaChgrModbus
import time


modbus = pyZerovaChgrModbus()

print(modbus.connect('192.168.10.111'))

total_time = 0
num_of_loop = 100
setpoints = [i for i in range(5)] # + [i for i in range(30, 50, 5)] + [0, 50, 5, 10]
print(setpoints)

time_elapsed_list = []
commands = [    #writeconf, readconf, getconn(1-> num), readvolt
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 1, 2, 0],
    [1, 1, 2, 1],
    [1, 1, 5, 0],
    [1, 1, 5, 1],

    ] 
setpoints = [0, 1]
for command in commands:
    for i in range(len(setpoints)):
        start = time.time()
        if command[0]:
            print(modbus.writeConfig([0, 0, 0, setpoints[i], 0, 0, 0, 0, 0]))
        if command[1]:
            print(modbus.readConfig())
        for id in range(1, command[2]):
            res = modbus.get_connector_info(id)
            print(f"GetConn({id}). Res: {res[0]}")
            if not res[0]:
                print(res[1])
        if command[3]:
            print(modbus.read_input_voltage())
        end = time.time()
        time_elapsed = end - start
        time_elapsed_list.append(time_elapsed)
        print(time_elapsed)
        print("---") 
        total_time += time_elapsed
        # time.sleep(3)
    print("----------------------")


print("average running time:", total_time/num_of_loop)
print(time_elapsed_list)
