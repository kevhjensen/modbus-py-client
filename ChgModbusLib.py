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

# test = pyZerovaChgrModbus()
# test.connect('192.168.10.155', 'hi')
# print(test.readInfo())
# test.readConfig()
# test.writeConfig([1, 0, 0, 0, 0])
# print(test.curConfig)