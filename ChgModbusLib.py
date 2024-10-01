import pandas as pd
from hashlib import sha256
from pymodbus.client import ModbusTcpClient
import struct
from constants import *

#isConnected = False
isTLS = False
isCert = False
isKey = False
isCa = False
TLS_Cert = ""
TLS_Key = ""
TLS_Ca = ""





class pyZerovaChgrModbus:
    def __init__(self) -> None:
        self.curConfig = []
        pass
    
    def connect(self, ipAddr, password) -> tuple:
        """
        Connects to charger with given IP over port 502. Unlocks charger with password (hashed and encoded)
        """
        try:
            self.client = ModbusTcpClient(ipAddr)
            self.client.connect()
            response = self.client.write_registers(address=EVSE_REG_ADDR_LOGIN_PASSWORD, values=self.passwordHashAndModbusEncode(password))
            if response.isError():
                return 0, f"Error: {response}"
            return 1, "connection success"
        except Exception as e:
            return 0,str(e)

    def disconnect(self):
        """
        disconnect the device
        """
        try:
            self.client.close()
            return 1, "Disconnection success"
        except Exception as e:
            return 0,str(e)
    def readInfo(self) -> dict:
        """
        Read charger's model name and serial number. LSB, MSW, ASCII encoding
        """
        data = self.client.read_holding_registers(address=EVSE_REG_ADDR_MODEL_NAME, count=32)
        if data.isError():
            return 0, f"Error: {data}"
        modelName = self.byte_swap_u16(data.registers).decode('ascii').rstrip('\x00')
        
        data = self.client.read_holding_registers(address=EVSE_REG_ADDR_SN, count=32)
        serialNumber = self.byte_swap_u16(data.registers).decode('ascii').rstrip('\x00')

        return modelName, serialNumber
    

    def readConfig(self) -> list:
        """
        Read configuration. Returns a list with 7 integers
        {"Auth": 0, # 1 = Enable
         "EvccidAuth" : 1, # 1 = Enable
         "MaxEnergy" : 2, # 0 is unlimited
         "MaxPower" : 3,
         "MaxCurrent" : 4,
         "MaxDuration" : 5,
         "RfidEndian" : 6} # 0 = little, 1 = big
         "15118 enable": 7, boolean
         "15118 pnc": 8, boolean
        """
        data = self.client.read_holding_registers(address=EVSE_REG_ADDR_AUTH_MODE, count=9)
        if data.isError():
            return 0, f"Error: {data}"
        
        self.curConfig = data.registers
        
        return 1,data.registers
    
    def writeConfig(self, newConfig) -> list:
        """
        Sends new configuration to charger, then blips Save_Config coil high, writing the new config to NAND flash
        :param new_configuration: List of 7 booleans and numbers, that correspond to Auth, EvccidAuth...
        """
        write_response = self.client.write_registers(address=EVSE_REG_ADDR_AUTH_MODE, values = newConfig)
        if write_response.isError():
            return 0, f"error: {write_response}"
        save_response = self.client.write_coil(address=EVSE_COIL_ADDR_SAVE_CONFIG, value=1) #write config on holding register to NAND flash
        if save_response.isError():
            return 0, f"error:{save_response}"
        
        return 1,self.readConfig()

    def byte_swap_u16(self, data: list) -> bytearray:
        """
        Uses little endianness to convert a list of Modbus register values (16 bit / word (1 register)) to a bytearray
        :param data: raw list of u16 values
        """ 
        result = bytearray()
        for word in data:
            result.append(word & 0xff) # LSB, masks out MSB
            result.append((word >> 8) & 0xff) # get MSB by shifting out LSB, & 0xff for extra safety
        return result

    def passwordHashAndModbusEncode(self, password) -> list:
        """
        This function takes in a password and returns an output that fills modbus registers 64 to 95 of a Zerova, granting read / write privileges
        """
        
        pass_SHA256Hashed_HexString = sha256(password.encode('utf-8')).hexdigest() 
        # utf-8 encode into sequence of bytes, SHA256 hash, then convert each of the 32 bytes to a 2 char hexadecimal string

        hashed_HexStringed_ASCII = [ord(ch) for ch in pass_SHA256Hashed_HexString] 
        # ASCII encode hexdecimal chars into bytes (64 byte array)

        modbusRegisters = []
        for i in range(32):
            MSB, LSB = hashed_HexStringed_ASCII[i], hashed_HexStringed_ASCII[i + 1]
            register = (LSB << 8) | MSB 
            modbusRegisters.append(register)
            # 2 bytes in each register using little endianness

        return modbusRegisters

    def BTN_reboot(self):
        try:
            response = self.client.write_coil(address=EVSE_COIL_ADDR_REBOOT, value=1)
            if response.isError():
                return 0, f"error:{response}"
            return 1, "Reboot request sent successfully"
        except Exception as e:
            return 0, str(e)
        
    def BTN_start_charging(self,connectorID):
        """
        Send command to start charging for the given connector.
        :param connector_index: The index of the connector (e.g., 1 for Connector 1)
        """
        try:
            # Calculate the start charging coil address based on connector index
            coil_address = (connectorID * 1000) + CONNECTOR_COIL_ADDR_START
            response = self.client.write_coil(coil_address, True)  # Write '1' to start charging
            if response.isError():
                return 0, f"error:{response}"
            return 1, f"Start charging request sent to connector {connectorID}"
        except Exception as e:
            return 0, str(e)
    
    def BTN_stop_charging(self,connectorID):
        """
        Send command to stop charging for the given connector.
        :param connector_index: The index of the connector (e.g., 1 for Connector 1)
        """
        try:
            # Calculate the stop charging coil address based on connector index
            coil_address = (connectorID * 1000) + CONNECTOR_COIL_ADDR_STOP
            response = self.client.write_coil(coil_address, True)  # Write '1' to stop charging
            if response.isError():
                return 0, f"error:{response}"
            return 1, f"Stop charging request sent to connector {connectorID}"
        except Exception as e:
            return 0, str(e)
        
    def get_connector_info(self,connectorID):
        """
        Fetches the present connector info including:
        - System state
        - Plug status
        - State of charge (SOC)
        - Present power
        - Present voltages (DC, AC L1, AC L2, AC L3)
        - Present currents (DC, AC L1, AC L2, AC L3)
        - Charged energy
        - Charged duration
        - Remaining time
        - Session ID tag
        - Connector status code
        """
        try:
            # Calculate the base address for this connector
            base_address = connectorID * 1000

            # Read 50 registers starting from base address
            result = self.client.read_holding_registers(base_address + CONNECTOR_REG_ADDR_SYSTEM_STATE, 60)

            if result.isError():
                return 0, f"error:{result}"

            connector_info = result.registers
            connector_info_json = {}

            # Extract values from the read data
            raw_system_state = connector_info[CONNECTOR_REG_ADDR_SYSTEM_STATE]
            system_state = CONNECTOR_SYSTEM_STATE_MAP[raw_system_state]
            connector_info_json['system state'] = system_state
            connector_info_json['plug_status'] = connector_info[CONNECTOR_REG_ADDR_PLUG_STATUS] # 0 : Disconnected, 1 : Connected
            connector_info_json['soc'] = connector_info[CONNECTOR_REG_ADDR_PRESENT_SOC]

            connector_output_electrical_data = []
            for register in range(CONNECTOR_REG_ADDR_PRESENT_POWER, CONNECTOR_REG_ADDR_PRESENT_REMAIN_TIME + 1, 2):
                if register == 23: # account for empty register
                    continue
                raw = connector_info[register : register + 2]
                four_bytes_in_order = self.byte_swap_u16(raw)
                output_float = struct.unpack('f', bytes(four_bytes_in_order))[0]
                connector_output_electrical_data.append(output_float)

            electrical_data_names = [
                "present_power",
                "present_voltage_dc",
                "present_voltage_ac_l1",
                "present_voltage_ac_l2",
                "present_voltage_ac_l3",
                "present_current_dc",
                "present_current_ac_l1",
                "present_current_ac_l2",
                "present_current_ac_l3",
                "charged_energy",
                "charged_duration",
                "present_remain_time"
            ]
            
            for i, data in enumerate(connector_output_electrical_data):
                connector_info_json[electrical_data_names[i]] = data

            session_idtag = ""
            for i in range(CONNECTOR_REG_ADDR_PRESENT_IDTAG, CONNECTOR_REG_ADDR_STATUS_CODE-CONNECTOR_REG_ADDR_PRESENT_IDTAG+1,2):
                four_bytes_in_order = self.byte_swap_u16(connector_info[i:i+2])
                output_float = struct.unpack('f', bytes(four_bytes_in_order))[0]
                session_idtag+=str(output_float)
            
            status_code = ""
            for i in range(CONNECTOR_REG_ADDR_STATUS_CODE, 11,2):
                four_bytes_in_order = self.byte_swap_u16(connector_info[i:i+2])
                output_float = struct.unpack('f', bytes(four_bytes_in_order))[0]
                status_code+=str(output_float)
            
            connector_info_json["session_idtag"] = session_idtag
            connector_info_json["status_code"] = status_code
            return 1,connector_info_json

        except Exception as e:
            return 0, str(e)

    def read_input_voltage(self):
        data = self.client.read_holding_registers(address=EVSE_REG_ADDR_AC_INPUT_VOLTAGE_L1, count=8)
        if data.isError():
            return 0, f"error:{data}"
        input_voltage_list=[]
        for i in range(0,7,2): #combine 2 little endian
            four_bytes_in_order = self.byte_swap_u16(data.registers[i:i+2])
            output_float = struct.unpack('f', bytes(four_bytes_in_order))[0]
            input_voltage_list.append(output_float)

        return 1,input_voltage_list  
    
# test = pyZerovaChgrModbus()
# test.connect('192.168.10.155', 'hi')
# print(test.readInfo())
# test.readConfig()
# test.writeConfig([1, 0, 0, 0, 0])
# print(test.curConfig)

# msg = test.BTN_start_charging()
# print(msg)
# msg = test.BTN_stop_charging()
# print(msg)
# msg = test.get_connector_info(1)
# print(msg)
# msg = test.BTN_reboot()
# print(msg)

# print(test.read_input_voltage())