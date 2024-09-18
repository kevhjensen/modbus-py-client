import sys
from ChgModbusLib import pyZerovaChgrModbus 
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QTextEdit, QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QMessageBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.modbus = pyZerovaChgrModbus()
    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create input fields for A and B
        self.input_ipaddr = QLineEdit(self)
        self.input_ipaddr.setPlaceholderText("Enter IP address")

        self.input_pwd = QLineEdit(self)
        self.input_pwd.setPlaceholderText("Enter password")

        # Create a button for submitting IP address and password
        self.button = QPushButton('Connect', self)
        self.button.clicked.connect(self.manage_connect)

        # Create a text area to show info 
        self.info_area = QTextEdit(self)
        self.info_area.setReadOnly(True)  # Make it read-only
        self.info_area.setPlaceholderText("Information will appear here...")

        # Add inputs and button to layout
        layout.addWidget(QLabel("ip address:"))
        layout.addWidget(self.input_ipaddr)

        layout.addWidget(QLabel("password:"))
        layout.addWidget(self.input_pwd)

        layout.addWidget(self.button)
        layout.addWidget(QLabel("Info:"))
        layout.addWidget(self.info_area)
        # Set layout
        self.setLayout(layout)

        # Window settings
        self.setWindowTitle('modbus')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def manage_connect(self):
        self.info_area.setText("")
        # Get values from input fields
        ipaddr = self.input_ipaddr.text()
        pwd = self.input_pwd.text()

        # Example validation logic
        # if a == "validA" and b == "validB":
        #     QMessageBox.information(self, 'Success', 'Information A and B are valid!')
        # else:
        #     QMessageBox.warning(self, 'Error', 'Invalid information A or B.')

        #print(ipaddr,pwd)
        isSuccess,msg = self.modbus.connect(ipaddr,pwd)
        if isSuccess == 1:
            self.info_area.append(msg + '\n')
            modelName,serialNumber = self.modbus.readInfo()
            self.info_area.append(f"{modelName}\n{serialNumber}")
            print("success connection")
        else:
            QMessageBox.warning(self, 'Error', 'Connection failed. Please check ip address and pwd.')
            self.info_area.append(f"Error: {msg}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()


