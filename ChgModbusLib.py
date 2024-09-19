import pandas as pd
from hashlib import sha256
from pymodbus.client import ModbusTcpClient

isConnected = False
isTLS = False
isCert = False
isKey = False
isCa = False
TLS_Cert = ""
TLS_Key = ""
TLS_Ca = ""


EVSE_COIL_ADDR_SAVE_CONFIG = 0
EVSE_COIL_ADDR_REBOOT = 1

CONNECTOR_COIL_ADDR_START = 0
CONNECTOR_COIL_ADDR_STOP = 1

EVSE_REG_ADDR_MODEL_NAME = 0
EVSE_REG_ADDR_SN = 32
EVSE_REG_ADDR_LOGIN_PASSWORD = 64
EVSE_REG_ADDR_AC_INPUT_VOLTAGE_L1 = 96
EVSE_REG_ADDR_AC_INPUT_VOLTAGE_L2 = 98
EVSE_REG_ADDR_AC_INPUT_VOLTAGE_L3 = 100
EVSE_REG_ADDR_DC_PUT_VOLTAGE = 102
EVSE_REG_ADDR_AUTH_MODE = 564
EVSE_REG_ADDR_AUTH_EVCCID = 565
EVSE_REG_ADDR_MAX_ENERGY = 566
EVSE_REG_ADDR_MAX_POWER = 567
EVSE_REG_ADDR_MAX_CURRENT = 568
EVSE_REG_ADDR_MAX_DURATION = 569
EVSE_REG_ADDR_RFID_ENDIAN = 570
EVSE_REG_ADDR_15118_ENABLE = 571
EVSE_REG_ADDR_15118_PNC = 572

CONNECTOR_REG_ADDR_SYSTEM_STATE = 0
CONNECTOR_REG_ADDR_PLUG_STATUS = 1
CONNECTOR_REG_ADDR_PRESENT_SOC = 2
CONNECTOR_REG_ADDR_PRESENT_POWER = 3
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_DC = 5
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L1 = 7
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L2 = 9
CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L3 = 11
CONNECTOR_REG_ADDR_PRESENT_CURRENT_DC = 13
CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L1 = 15
CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L2 = 17
CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L3 = 19
CONNECTOR_REG_ADDR_CHARGED_ENERGY = 21
CONNECTOR_REG_ADDR_CHARGED_DURATION = 25
CONNECTOR_REG_ADDR_PRESENT_REMAIN_TIME = 27
CONNECTOR_REG_ADDR_PRESENT_IDTAG = 28
CONNECTOR_REG_ADDR_STATUS_CODE = 50


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
            self.client.write_registers(address=EVSE_REG_ADDR_LOGIN_PASSWORD, values=self.passwordHashAndModbusEncode(password))
            #self.curConfig = self.readConfig()
            return 1, "connection success"
        except Exception as e:
            return 0,str(e)

    def readInfo(self) -> dict:
        """
        Read charger's model name and serial number. LSB, MSW, ASCII encoding
        """
        data = self.client.read_holding_registers(address=EVSE_REG_ADDR_MODEL_NAME, count=32)
        modelName = self.u16ToByte(data.registers).decode('ascii').rstrip('\x00')

        data = self.client.read_holding_registers(address=EVSE_REG_ADDR_SN, count=32)
        serialNumber = self.u16ToByte(data.registers).decode('ascii').rstrip('\x00')

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
        """
        data = self.client.read_holding_registers(address=EVSE_REG_ADDR_AUTH_MODE, count=9)
        self.curConfig = data.registers

        return data.registers
    
    def writeConfig(self, newConfig) -> list:
        """
        Takes in a list of 7 numbers, refer to readConfig for interpretation; reads values after writing
        """
        self.client.write_registers(address=EVSE_REG_ADDR_AUTH_MODE, values = newConfig)
        self.client.write_coil(address=EVSE_COIL_ADDR_SAVE_CONFIG, value=1) #write config on holding register to NAND flash

        return self.readConfig()

    def readConnectorStatus(self, conId) -> list:
        """
        """
        # {"sysStatus" : 0,
        #  ""}

    def u16ToByte(self, data: list) -> list:
        """
        Uses little endianness to convert a list of Modbus register values (16 bit / word (1 register)) to a bytearray
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
                return 0, "Error sending reboot request"
            return 1, "Reboot request sent successfully"
        except Exception as e:
            return 0, str(e)
    def BTN_start_charging(self,connectorID = 1):
        """
        Send command to start charging for the given connector.
        :param connector_index: The index of the connector (e.g., 1 for Connector 1)
        """
        try:
            # Calculate the start charging coil address based on connector index
            coil_address = (connectorID * 1000) + CONNECTOR_COIL_ADDR_START
            response = self.client.write_coil(coil_address, True)  # Write '1' to start charging
            if response.isError():
                return 0, "Error sending start charging request"
            return 1, f"Start charging request sent to connector {connectorID}"
        except Exception as e:
            return 0, str(e)
    
    def BTN_stop_charging(self,connectorID = 1):
        """
        Send command to stop charging for the given connector.
        :param connector_index: The index of the connector (e.g., 1 for Connector 1)
        """
        try:
            # Calculate the stop charging coil address based on connector index
            coil_address = (connectorID * 1000) + CONNECTOR_COIL_ADDR_STOP
            response = self.client.write_coil(coil_address, True)  # Write '1' to stop charging
            if response.isError():
                return 0, "Error sending stop charging request"
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
            result = self.client.read_holding_registers(base_address + CONNECTOR_REG_ADDR_SYSTEM_STATE, 51)

            if result.isError():
                return 0, "Error reading connector-info registers"

            connector_info = result.registers

            # Extract values from the read data
            # Extract values from the read data
            system_state = connector_info[CONNECTOR_REG_ADDR_SYSTEM_STATE]
            plug_status = connector_info[CONNECTOR_REG_ADDR_PLUG_STATUS]
            soc = connector_info[CONNECTOR_REG_ADDR_PRESENT_SOC]
            present_power = connector_info[CONNECTOR_REG_ADDR_PRESENT_POWER]
            present_voltage_dc = connector_info[CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_DC]
            present_voltage_ac_l1 = connector_info[CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L1]
            present_voltage_ac_l2 = connector_info[CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L2]
            present_voltage_ac_l3 = connector_info[CONNECTOR_REG_ADDR_PRESENT_VOLTAGE_AC_L3]
            present_current_dc = connector_info[CONNECTOR_REG_ADDR_PRESENT_CURRENT_DC]
            present_current_ac_l1 = connector_info[CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L1]
            present_current_ac_l2 = connector_info[CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L2]
            present_current_ac_l3 = connector_info[CONNECTOR_REG_ADDR_PRESENT_CURRENT_AC_L3]
            charged_energy = connector_info[CONNECTOR_REG_ADDR_CHARGED_ENERGY]
            charged_duration = (connector_info[CONNECTOR_REG_ADDR_CHARGED_DURATION + 1] << 16) | connector_info[CONNECTOR_REG_ADDR_CHARGED_DURATION]
            remaining_time = (connector_info[CONNECTOR_REG_ADDR_PRESENT_REMAIN_TIME + 1] << 16) | connector_info[CONNECTOR_REG_ADDR_PRESENT_REMAIN_TIME]
            session_idtag = connector_info[CONNECTOR_REG_ADDR_PRESENT_IDTAG]
            status_code = connector_info[CONNECTOR_REG_ADDR_STATUS_CODE]

            # Return a list with all the values
            return [
                {"System State": system_state},
                {"Plug Status": plug_status},
                {"SOC": soc},
                {"Present Power": present_power},
                {"Present Voltage DC": present_voltage_dc},
                {"Present Voltage AC L1": present_voltage_ac_l1},
                {"Present Voltage AC L2": present_voltage_ac_l2},
                {"Present Voltage AC L3": present_voltage_ac_l3},
                {"Present Current DC": present_current_dc},
                {"Present Current AC L1": present_current_ac_l1},
                {"Present Current AC L2": present_current_ac_l2},
                {"Present Current AC L3": present_current_ac_l3},
                {"Charged Energy": charged_energy},
                {"Charged Duration": charged_duration},
                {"Remaining Time": remaining_time},
                {"Session ID Tag": session_idtag},
                {"Connector Status Code": status_code}
            ]

        except Exception as e:
            return 0, str(e)
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