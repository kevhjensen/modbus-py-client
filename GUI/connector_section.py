from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QGroupBox, QMessageBox

class Connectors(QGroupBox):
    def __init__(self,num_of_connector,callbacks):
        super().__init__("Connectors")
        self.callbacks = callbacks
    
        self.connector_checbox_list = [] #tuple(checkbox,button_start,button_stop)
        self.connectors_info_list = []
        self.connector_info_widgets_list = []  # List to store widgets for each connector
        self.num_of_connector = num_of_connector
        
        self.init_ui()
        self.signal_bind()
    def init_ui(self):
        layout_QV = QVBoxLayout()
        checkbox_section = self.init_connector_checkbox_section()
        info_section = self.init_connector_info_section()

        layout_QV.addLayout(checkbox_section)
        layout_QV.addLayout(info_section)

        self.setLayout(layout_QV)
    def init_connector_checkbox_section(self):
        connector_checkbox_section = QHBoxLayout()
        for i in range(self.num_of_connector):
            new_checkbox = QCheckBox("Connector "+ str(i), self)
            new_start_button = QPushButton("Start Charging", self)
            new_stop_button = QPushButton("Stop Charging", self)
            connector_checkbox_section.addWidget(new_checkbox)
            connector_checkbox_section.addWidget(new_start_button)
            connector_checkbox_section.addWidget(new_stop_button)
            self.connector_checbox_list.append((new_checkbox,new_start_button,new_stop_button))
        
        return connector_checkbox_section
    
    # Function to initialize the Connector Info section
    def init_connector_info_section(self):
        connector_info_section = QHBoxLayout()  # Create a HBox for all connectors' info sections
        for i in range(self.num_of_connector):
            connector_name = "Connector " + str(i)
            scroll_area, info_widgets = self.init_single_connector_info_component(connector_name)
            scroll_area.hide()
            connector_info_section.addWidget(scroll_area)
            self.connectors_info_list.append(scroll_area)
            self.connector_info_widgets_list.append(info_widgets)  # Store the widgets for this connector

        return connector_info_section

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

        # Create a scroll area and set the group box as its widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(group_box)

        return scroll_area, info_widgets

    def signal_bind(self):
        # Bind the checkboxes to toggle the visibility of connector-info sections
        for i in range(self.num_of_connector):
            checkbox, start_button, stop_button = self.connector_checbox_list[i]
            checkbox.stateChanged.connect(lambda state, idx=i: self.on_check_connector_checkbox(idx))
            start_button.clicked.connect(lambda checked, idx=i: self.start_charging(idx))
            stop_button.clicked.connect(lambda checked, idx=i: self.stop_charging(idx))
    
    def start_charging(self,idx):
        if self.callbacks["start"]:
            self.callbacks["start"](idx)

    def stop_charging(self,idx):
        if self.callbacks["stop"]:
            self.callbacks["stop"](idx)

    # Toggle visibility of connector info sections based on checkbox
    def on_check_connector_checkbox(self,connector_id):
        # set the relation between the visibility of each connector-info and their checkbox 
        checkbox = self.connector_checbox_list[connector_id][0]
        is_checked = checkbox.isChecked()
        self.connectors_info_list[connector_id].setVisible(is_checked)
    
    def get_connector_info_widgets_list(self):
        return self.connector_info_widgets_list

