from PyQt6.QtWidgets import QSplitter,QScrollArea,QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QGroupBox, QMessageBox
from PyQt6.QtCore import QTimer,Qt
from GUI.login_section import LoginSection
from GUI.charger_config import Configuration
from GUI.msg_section import Message
from GUI.connector_section import Connectors
class ModbusUI(QWidget):

    def __init__(self,modbus):
        super().__init__()
        self.modbus = modbus

        #init variables
        self.num_of_connector = 4
        
        #login- condition
        #self.is_logged_in  = False

        # Initialize connector timers
        self.connector_timer = QTimer()
        self.connector_timer.timeout.connect(self.update_all_connectors_info) #Connect the timer's timeout signal to the update method

        self.init_ui()  # Initialize the UI components
        
    # initialize all UI    
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        '''
        ------------------Initialize each section----------------------------
        '''
        login_section_callbacks = {"reboot":self.on_reboot,"login":self.on_login,"disconnect":self.on_disconnect}
        connectors_callbacks = {"start":self.on_start_charging,"stop":self.on_stop_charging}
        config_callbacks = {"save":self.on_save_config}

        self.login_section = LoginSection(login_section_callbacks)
        self.message_section = Message()
        self.config_section = Configuration(config_callbacks)
        self.connectors_section = Connectors(self.num_of_connector,connectors_callbacks)


        '''
        ----------------------Manage the layout----------------------------
        '''
        # # Create a splitter
        # splitter = QSplitter(Qt.Orientation.Vertical)
        # splitter.addWidget(message_section)
        # splitter.addWidget(connectors_section)

        # Add sections to the main layout
        layout_A = QVBoxLayout()
        layout_A.addWidget(self.login_section)
        layout_A.addWidget(self.message_section)
        
        layout_B = QHBoxLayout()
        layout_B.addLayout(layout_A)
        layout_B.addWidget(self.config_section)

        # main_layout.addWidget(splitter)
        main_layout.addLayout(layout_B)
        main_layout.addWidget(self.connectors_section)
    
        # Set layout for the main window
        self.setLayout(main_layout)

        # Window settings
        self.setWindowTitle('Modbus TCP Client V1.2')
        self.setGeometry(300, 300, 600, 600)
        self.show()
        
    
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
        pass
    def string_to_16bit(self,data):
        try:
            value = int(data) # Convert the string to an integer             
            if not (0 <= value <= 65535): # Ensure the value fits within the uint16 range (0 to 65535)
                raise ValueError("Value must be between 0 and 65535.")
            
            return value
        except ValueError:
            raise ValueError("Invalid input")
    def on_save_config(self,input_widgets):
        '''
        each val of config is Big endian, MaxEnergy MaxPower MaxCurrent MaxDuration are uint16, other fields are boolean
        '''
        new_configs= []
        # Retrieve values from input fields and convert them to the appropriate types
        try:
            new_configs.append(self.string_to_16bit(input_widgets["Auth (0: Disable, 1: Enable)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["EvccidAuth (0: Disable, 1: Enable)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["MaxEnergy (kWh,0 is unlimited)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["MaxPower (kW,0 is unlimited)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["MaxCurrent (A,0 is unlimited)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["MaxDuration (minutes,0 is unlimited)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["RfidEndian (0: little endian, 1: big endian)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["ISO-15118 enable (0: Disable, 1: Enable)"].text()))
            new_configs.append(self.string_to_16bit(input_widgets["ISO-15118 PnC enable (0: Disable, 1: Enable)"].text()))

            # Call the Modbus function to write the configuration
            write_success, response = self.modbus.writeConfig(new_configs)
            if write_success:
                self.message_section.append_message(f"{response}\n")
            else:
                QMessageBox.warning(self, 'Error', f"Failed to save configuration: {response}")
                self.message_section.append_message(f"Error:{response}")

        except ValueError as e:
            QMessageBox.warning(self, 'Error', f"Invalid input: {e}")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f"An error occurred: {e}")
    def on_login(self,ipaddr, pwd):
        isSuccess,msg = self.modbus.connect(ipaddr,pwd)
        if isSuccess:
            #self.is_logged_in = True #????
            self.message_section.append_message(msg + '\n')
            modelName,serialNumber = self.modbus.readInfo()
            self.message_section.append_message(f"Model Number: {modelName}\nSerial Number: {serialNumber}")
            print("success connection")
            
            # Start the single timer to update connector info
            self.connector_timer.start(1000)  # Update every second
            
            # Read default configuration values
            read_config_success, config_values  = self.modbus.readConfig()
            if read_config_success:
                self.config_section.populate_configuration_fields(config_values)
            else:
                QMessageBox.warning(self, 'Error', f"Failed to retrieve configuration: {config_values}")
                
        else:
            QMessageBox.warning(self, 'Error', msg)
            self.message_section.append_message(f"Error: {msg}")
    
    def on_disconnect(self):
        '''
        button on click disconnect 
        '''
        success,response = self.modbus.disconnect()
        if success:
            self.message_section.append_message(response + '\n')

            if self.connector_timer.isActive():
                self.connector_timer.stop()
            print("success disconnection")
        else:
            QMessageBox.warning(self, 'Error', response)
            self.message_section.append_message(f"Error: {response}")   
    def on_reboot(self):
        isSuccess,msg = self.modbus.BTN_reboot()
        if isSuccess:
            self.message_section.append_message(msg + '\n')
        else:
            QMessageBox.warning(self, 'Error', 'reboot failed.')
            self.message_section.append_message(f"Error: {msg}")


    def on_start_charging(self,connector_id):
        backend_connector_id = connector_id+1
        success, message = self.modbus.BTN_start_charging(backend_connector_id)
        if success:
            self.message_section.append_message(f"Started charging on Connector {connector_id}")
            
        else:
            QMessageBox.warning(self, 'Error', f"Failed to start charging on Connector {connector_id}: {message}")
            self.message_section.append_message(f"Error: {message}")
    def on_stop_charging(self,connector_id):
        backend_connector_id = connector_id+1
        success, message = self.modbus.BTN_stop_charging(backend_connector_id)
        if success:
            self.message_section.append_message(f"Stopped charging on Connector {connector_id}")
        else:
            QMessageBox.warning(self, 'Error', f"Failed to stop charging on Connector {connector_id}: {message}")  
            self.message_section.append_message(f"Error: {message}")

    # def start_charging_timer(self,connector_id):
    #     timer = self.connector_timers[connector_id]
    #     if not timer.isActive():
    #         timer.start(1000)  # Update every 1 second
    # def stop_charging_timer(self, connector_id):
    #     timer = self.connector_timers[connector_id]
    #     if timer.isActive():
    #         timer.stop()

    def update_all_connectors_info(self):
        """Update information for all connectors."""
        info_widgets_list = self.connectors_section.get_connector_info_widgets_list()
        for connector_id in range(self.num_of_connector):
            self.update_connector_info(connector_id,info_widgets_list[connector_id])

    
    def update_connector_info(self, connector_id,info_widgets):
        """
        Update the UI elements for a specific connector with the provided data.

        :param connector_id: The index of the connector (0-based)
        :param connector_info: A dictionary containing the connector info
        """
        backend_connector_id = connector_id+1
        success, result = self.modbus.get_connector_info(backend_connector_id)
        if success:
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
                    info_widgets[ui_field].setText(str(value)) # Convert value to string if necessary
        else:
            self.message_section.append_message(f"Error updating connector {connector_id}: {result}")
    
    
