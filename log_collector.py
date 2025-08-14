from ChgModbusLib import pyZerovaChgrModbus
import csv
from datetime import datetime
import time


READ_INTERVAL = 0.1 # in seconds
IP_ADDR = "192.168.10.155"
ACCURATE_TO = 3 # Number of decimal places for timestamp (e.g., 3 = milliseconds)
#preapre modbus 
modbus = pyZerovaChgrModbus()
modbus.connect(IP_ADDR,"")
first_config = modbus.writeConfig([0,0,0,0,0,0,0,0,0])
print("success set all 0s" if first_config[0] else "fail set all 0s", first_config[1])
charger_info = modbus.info
print(charger_info[1] if charger_info[0] else "fail read charger info")

# Generate filename with current time (formatted for safe filenames)
start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"modbus_log_{start_time}.csv"
# Create and open the CSV file for writing
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["current config"] + first_config[1])
    writer.writerow(["charger_info"]+charger_info[1])
    print("please plug in...")
    try:
        start_tick = time.perf_counter()
        first_tick = start_tick
        while True:
            current_tick = time.perf_counter()
            elapsed_ms = current_tick - start_tick
            if elapsed_ms >= READ_INTERVAL:
                timestamp = current_tick - first_tick 
                formatted_timestamp = f"{timestamp:.{ACCURATE_TO}f}"
                result = modbus.get_connector_info(1)
                
                if result[0]:
                    writer.writerow([formatted_timestamp] + result[1])
                else:
                    writer.writerow([formatted_timestamp, "Failed to read connector info"])
                
                file.flush()
                start_tick = current_tick # Reset the timer
    except KeyboardInterrupt:
        print("\nLogging stopped by user.")