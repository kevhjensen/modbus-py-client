import sys
from ChgModbusLib import pyZerovaChgrModbus 
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QTextEdit, QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QMessageBox,QGroupBox,QGridLayout,QCheckBox,QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.modbus = pyZerovaChgrModbus()
        self.init_ui()       # Initialize the UI components
        self.bind_signals()  # Bind signals to functions
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Initialize each section
        connect_section = self.init_section_connect()
        message_section = self.init_section_message_display()
        connector_checkbox = self.init_section_connector_checkbox()
        connector_section = self.init_section_connector_info()
        
        # Add sections to the main layout
        main_layout.addLayout(connect_section)
        main_layout.addWidget(QLabel("Messages"))
        main_layout.addWidget(message_section)
        main_layout.addLayout(connector_checkbox)
        main_layout.addLayout(connector_section)
    
        # Set layout for the main window
        self.setLayout(main_layout)

        # Window settings
        self.setWindowTitle('Modbus TCP Client V1.2')
        self.setGeometry(300, 300, 600, 800)
        self.show()

    # Function to initialize the Connect section
    def init_section_connect(self):
        connect_section = QGridLayout()

        self.input_ipaddr = QLineEdit(self)
        self.input_ipaddr.setPlaceholderText("Enter IP address")
        
        self.input_pwd = QLineEdit(self)
        self.input_pwd.setPlaceholderText("Enter password")
        self.input_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.connect_button = QPushButton('Connect', self)
        self.disconnect_button = QPushButton('Disconnect', self)

        # Add connect section elements to grid layout
        connect_section.addWidget(QLabel("IP Address"), 0, 0)
        connect_section.addWidget(self.input_ipaddr, 0, 1)
        connect_section.addWidget(QLabel("Password"), 1, 0)
        connect_section.addWidget(self.input_pwd, 1, 1)
        connect_section.addWidget(self.connect_button, 2, 0)
        connect_section.addWidget(self.disconnect_button, 2, 1)

        return connect_section

    # Function to initialize the Message Display section
    def init_section_message_display(self):
        self.info_area = QTextEdit(self)
        self.info_area.setReadOnly(True)
        self.info_area.setPlaceholderText("Messages will appear here...")
        return self.info_area
    # Function to initialize the Connector chekcboxes
    def init_section_connector_checkbox(self):
        connector_checkbox_section = QHBoxLayout()
        # Checkboxes for connector selection
        self.connector_1_check = QCheckBox("Connector 1", self)
        self.connector_2_check = QCheckBox("Connector 2", self)
        self.connector_3_check = QCheckBox("Connector 3", self)
        self.connector_4_check = QCheckBox("Connector 4", self)

        # Buttons for start/stop charging for each connector
        self.start_button_1 = QPushButton("Start Charging", self)
        self.stop_button_1 = QPushButton("Stop Charging", self)
        self.start_button_2 = QPushButton("Start Charging", self)
        self.stop_button_2 = QPushButton("Stop Charging", self)
        self.start_button_3 = QPushButton("Start Charging", self)
        self.stop_button_3 = QPushButton("Stop Charging", self)
        self.start_button_4 = QPushButton("Start Charging", self)
        self.stop_button_4 = QPushButton("Stop Charging", self)

        # Add checkboxes and buttons to the horizontal layout
        connector_checkbox_section.addWidget(self.connector_1_check)
        connector_checkbox_section.addWidget(self.start_button_1)
        connector_checkbox_section.addWidget(self.stop_button_1)

        connector_checkbox_section.addWidget(self.connector_2_check)
        connector_checkbox_section.addWidget(self.start_button_2)
        connector_checkbox_section.addWidget(self.stop_button_2)

        connector_checkbox_section.addWidget(self.connector_3_check)
        connector_checkbox_section.addWidget(self.start_button_3)
        connector_checkbox_section.addWidget(self.stop_button_3)

        connector_checkbox_section.addWidget(self.connector_4_check)
        connector_checkbox_section.addWidget(self.start_button_4)
        connector_checkbox_section.addWidget(self.stop_button_4)
        return connector_checkbox_section
    # Function to initialize the Connector Info section
    def init_section_connector_info(self):
        self.connector_section = QHBoxLayout()  # Create a VBox for all connectors' info sections
        
        self.connector_1_info = self.create_connector_info_section("Connector 1")
        self.connector_2_info = self.create_connector_info_section("Connector 2")
        self.connector_3_info = self.create_connector_info_section("Connector 3")
        self.connector_4_info = self.create_connector_info_section("Connector 4")

        # Initially hide all but the first connector info section
        self.connector_1_info.hide()
        self.connector_2_info.hide()
        self.connector_3_info.hide()
        self.connector_4_info.hide()

        # Add all connector sections to the main layout
        self.connector_section.addWidget(self.connector_1_info)
        self.connector_section.addWidget(self.connector_2_info)
        self.connector_section.addWidget(self.connector_3_info)
        self.connector_section.addWidget(self.connector_4_info)

        return self.connector_section

    def create_connector_info_section(self,connector_name):
        group_box = QGroupBox(connector_name)  # Group each section for better UI organization
        layout = QGridLayout()

        system_state = QLineEdit()
        system_state.setReadOnly(True)
        plug_status = QLineEdit()
        plug_status.setReadOnly(True)
        soc = QLineEdit()
        soc.setReadOnly(True)
        present_power = QLineEdit()
        present_power.setReadOnly(True)

        # Add labels and fields
        layout.addWidget(QLabel("System State"), 0, 0)
        layout.addWidget(system_state, 0, 1)
        layout.addWidget(QLabel("Plug Status"), 1, 0)
        layout.addWidget(plug_status, 1, 1)
        layout.addWidget(QLabel("SOC"), 2, 0)
        layout.addWidget(soc, 2, 1)
        layout.addWidget(QLabel("Present Power"), 3, 0)
        layout.addWidget(present_power, 3, 1)

        group_box.setLayout(layout)
        return group_box

    # Function to toggle visibility of connector info sections
    def toggle_connector_info(self):
        # Check the state of each checkbox and toggle visibility of respective connector-info sections
        self.connector_1_info.setVisible(self.connector_1_check.isChecked())
        self.connector_2_info.setVisible(self.connector_2_check.isChecked())
        self.connector_3_info.setVisible(self.connector_3_check.isChecked())
        self.connector_4_info.setVisible(self.connector_4_check.isChecked())
    
    def bind_signals(self):
        # Connect buttons to methods
        self.connect_button.clicked.connect(self.manage_connect)
        #self.disconnect_button.clicked.connect(self.manage_disconnect)

        # Bind the checkboxes to toggle the visibility of connector-info sections
        self.connector_1_check.stateChanged.connect(self.toggle_connector_info)
        self.connector_2_check.stateChanged.connect(self.toggle_connector_info)
        self.connector_3_check.stateChanged.connect(self.toggle_connector_info)
        self.connector_4_check.stateChanged.connect(self.toggle_connector_info)
    
    
    

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


