from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QGroupBox, QMessageBox
from PyQt6.QtCore import QTimer
class ModbusUI(QWidget):

    def __init__(self,modbus):
        super().__init__()
        self.modbus = modbus

        #init variables
        self.num_of_connector = 4
        self.connector_checbox_list = [] #tuple(checkbox,button_start,button_stop)
        self.connectors_info_list = []
        self.connector_info_widgets_list = []  # List to store widgets for each connector

        self.input_ipaddr = None
        self.input_pwd = None
        self.connect_button = None
        self.disconnect_button = None
        self.info_area = None 
        self.connector_checkbox_section = None
        self.connector_info_section = None

        ##init_timer
        # Initialize connector timers
        self.connector_timers = [QTimer() for _ in range(self.num_of_connector)]
        for i, timer in enumerate(self.connector_timers):
            timer.timeout.connect(lambda x=i: self.update_connector_info(x))


        self.init_ui()  # Initialize the UI components
        self.bind_signals() #link UI component with interaction function 
    # initialize all UI    
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Initialize each section
        connect_section = self.init_charger_connect_section()
        message_section = self.init_message_display_section()
        connector_checkbox = self.init_connector_checkbox_section()
        connector_section = self.init_connector_info_section()
        
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
    def init_charger_connect_section(self):
        connect_section = QGridLayout()

        self.input_ipaddr = QLineEdit(self)
        self.input_ipaddr.setPlaceholderText("Enter IP address")
        
        self.input_pwd = QLineEdit(self)
        self.input_pwd.setPlaceholderText("Enter password")
        self.input_pwd.setEchoMode(QLineEdit.EchoMode.Password)

        self.connect_button = QPushButton('Connect', self)
        self.disconnect_button = QPushButton('Disconnect', self)
        #reboot button
        self.reboot_button = QPushButton('Reboot', self)

        # Add connect section elements to grid layout
        connect_section.addWidget(QLabel("IP Address"), 0, 0)
        connect_section.addWidget(self.input_ipaddr, 0, 1)
        connect_section.addWidget(QLabel("Password"), 1, 0)
        connect_section.addWidget(self.input_pwd, 1, 1)
        connect_section.addWidget(self.connect_button, 2, 0)
        connect_section.addWidget(self.disconnect_button, 2, 1)
        connect_section.addWidget(self.reboot_button)
        return connect_section
        
    # Function to initialize the Message Display section
    def init_message_display_section(self):
        self.info_area = QTextEdit(self)
        self.info_area.setReadOnly(True)
        self.info_area.setPlaceholderText("Messages will appear here...")
        return self.info_area
    # Function to initialize the Connector chekcboxes
    def init_connector_checkbox_section(self):
        self.connector_checkbox_section = QHBoxLayout()
        
        for i in range(self.num_of_connector):
            new_checkbox = QCheckBox("Connector "+ str(i), self)
            new_start_button = QPushButton("Start Charging", self)
            new_stop_button = QPushButton("Stop Charging", self)
            self.connector_checkbox_section.addWidget(new_checkbox)
            self.connector_checkbox_section.addWidget(new_start_button)
            self.connector_checkbox_section.addWidget(new_stop_button)
            self.connector_checbox_list.append((new_checkbox,new_start_button,new_stop_button))
        
        return self.connector_checkbox_section
    # Function to initialize the Connector Info section
    def init_connector_info_section(self):
        self.connector_info_section = QHBoxLayout()  # Create a HBox for all connectors' info sections
        
        for i in range(self.num_of_connector):
            connector_name = "Connector " + str(i)
            group_box, info_widgets = self.init_single_connector_info_component(connector_name)
            group_box.hide()
            self.connector_info_section.addWidget(group_box)
            self.connectors_info_list.append(group_box)
            self.connector_info_widgets_list.append(info_widgets)  # Store the widgets for this connector

        return self.connector_info_section


    def init_single_connector_info_component(self, connector_name):
        group_box = QGroupBox(connector_name)  # Group each section for better UI organization
        layout = QGridLayout()

        # Dictionary to store labels and corresponding QLineEdit widgets
        info_widgets = {}

        # List of all fields to display
        fields = [
            "System State",
            "Plug Status",
            "SOC",
            "Present Power",
            "Present Voltage DC",
            "Present Voltage AC L1",
            "Present Voltage AC L2",
            "Present Voltage AC L3",
            "Present Current DC",
            "Present Current AC L1",
            "Present Current AC L2",
            "Present Current AC L3",
            "Charged Energy",
            "Charged Duration",
            "Remaining Time",
            "Session ID Tag",
            "Status Code"
        ]

        # Create UI elements for each field
        for i, field_name in enumerate(fields):
            label = QLabel(field_name)
            line_edit = QLineEdit()
            line_edit.setReadOnly(True)
            layout.addWidget(label, i, 0)
            layout.addWidget(line_edit, i, 1)
            # Store the line_edit widget for later updates
            info_widgets[field_name] = line_edit

        group_box.setLayout(layout)
        return group_box, info_widgets

    '''
    --------------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------
    -----------------------------------------------------------------------------
    ---------------------------------interaction part--------------------------
    ----------------------------------------------------------------------------------
    --------------------------------------------------------------------------
    ----------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    
    '''
    #Signal binds to all UI
    def bind_signals(self):
        # Connect buttons to methods
        self.connect_button.clicked.connect(self.on_connect)
        #self.disconnect_button.clicked.connect(self.manage_disconnect)

        #reboot signal bind
        self.reboot_button.clicked.connect(self.on_reboot)
        # Bind the checkboxes to toggle the visibility of connector-info sections
        for i in range(self.num_of_connector):
            checkbox, start_button, stop_button = self.connector_checbox_list[i]
            checkbox.stateChanged.connect(lambda state, idx=i: self.on_check_connector_checkbox(idx))
            start_button.clicked.connect(lambda checked, idx=i: self.on_start_charging(idx))
            stop_button.clicked.connect(lambda checked, idx=i: self.on_stop_charging(idx))
    def on_connect(self):
        self.info_area.setText("")
        # Get values from input fields
        ipaddr = self.input_ipaddr.text()
        pwd = self.input_pwd.text()

        isSuccess,msg = self.modbus.connect(ipaddr,pwd)
        if isSuccess:
            self.info_area.append(msg + '\n')
            modelName,serialNumber = self.modbus.readInfo()
            self.info_area.append(f"Model Number: {modelName}\nSerial Number: {serialNumber}")
            print("success connection")
        else:
            QMessageBox.warning(self, 'Error', 'Connection failed. Please check ip address and pwd.')
            self.info_area.append(f"Error: {msg}")
    
    def on_disconnect(self):
        '''
        button on click disconnect 
        '''
        pass
    def on_reboot(self):
        isSuccess,msg = self.modbus.BTN_reboot()
        if isSuccess:
            self.info_area.append(msg + '\n')
        else:
            QMessageBox.warning(self, 'Error', 'reboot failed.')
            self.info_area.append(f"Error: {msg}")

    # Toggle visibility of connector info sections based on checkbox
    def on_check_connector_checkbox(self,connector_id):
        # set the relation between the visibility of each connector-info and their checkbox 
        checkbox = self.connector_checbox_list[connector_id][0]
        is_checked = checkbox.isChecked()
        self.connectors_info_list[connector_id].setVisible(is_checked)

    def on_start_charging(self,connector_id):
        backend_connector_id = connector_id+1
        success, message = self.modbus.BTN_start_charging(backend_connector_id)
        if success:
            self.info_area.append(f"Started charging on Connector {connector_id}")
            # Start the timer for this connector
            self.start_charging_timer(connector_id)
        else:
            QMessageBox.warning(self, 'Error', f"Failed to start charging on Connector {connector_id}: {message}")
    def on_stop_charging(self,connector_id):
        backend_connector_id = connector_id+1
        success, message = self.modbus.BTN_stop_charging(backend_connector_id)
        if success:
            self.info_area.append(f"Stopped charging on Connector {connector_id}")
            # Stop the timer for this connector
            self.stop_charging_timer(connector_id)
        else:
            QMessageBox.warning(self, 'Error', f"Failed to stop charging on Connector {connector_id}: {message}")  
    def start_charging_timer(self,connector_id):
        timer = self.connector_timers[connector_id]
        if not timer.isActive():
            timer.start(1000)  # Update every 1 second
    def stop_charging_timer(self, connector_id):
        timer = self.connector_timers[connector_id]
        if timer.isActive():
            timer.stop()
    def update_connector_info(self, connector_id):
        """
        Update the UI elements for a specific connector with the provided data.

        :param connector_id: The index of the connector (0-based)
        :param connector_info: A dictionary containing the connector info
        """
        backend_connector_id = connector_id+1
        success, result = self.modbus.get_connector_info(backend_connector_id)
        if success:

            info_widgets = self.connector_info_widgets_list[connector_id]

            # Map backend field names to UI field names
            field_mapping = {
                'system state': 'System State',
                'plug_status': 'Plug Status',
                'soc': 'SOC',
                'present_power': 'Present Power',
                'present_voltage_dc': 'Present Voltage DC',
                'present_voltage_ac_l1': 'Present Voltage AC L1',
                'present_voltage_ac_l2': 'Present Voltage AC L2',
                'present_voltage_ac_l3': 'Present Voltage AC L3',
                'present_current_dc': 'Present Current DC',
                'present_current_ac_l1': 'Present Current AC L1',
                'present_current_ac_l2': 'Present Current AC L2',
                'present_current_ac_l3': 'Present Current AC L3',
                'charged_energy': 'Charged Energy',
                'charged_duration': 'Charged Duration',
                'present_remain_time': 'Remaining Time',
                'session_idtag': 'Session ID Tag',
                'status_code': 'Status Code'
            }

            for backend_field, ui_field in field_mapping.items():
                if backend_field in result and ui_field in info_widgets:
                    value = result[backend_field]
                    # Convert value to string if necessary
                    info_widgets[ui_field].setText(str(value))
        else:
            # Handle error
            self.info_area.append(f"Error updating connector {connector_id}: {result}")
