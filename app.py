import sys
from PyQt6.QtWidgets import QApplication
from ChgModbusLib import pyZerovaChgrModbus
from modbus_UI import ModbusUI

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initialize UI and Modbus Backend
    
    modbus = pyZerovaChgrModbus()
    ui = ModbusUI(modbus)
    ui.show()

    sys.exit(app.exec())
