from PyQt6.QtWidgets import QGroupBox,QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel,QHBoxLayout

class DeviceInfo(QGroupBox):
    def __init__(self):
        super().__init__("Device Info")
        self.init_ui()
    
    def init_ui(self):
        
        self.fields = self.items = [
            "Model Name", 
            "Serial Number", 
            "Input Voltage",
            "AC Input Voltage L1", 
            "AC Input Voltage L2", 
            "AC Input Voltage L3", 
            "DC Output Voltage", 
        ]

        # Store input widgets
        self.input_widgets = {}

        grid_layout = QGridLayout()
        for i, field_name in enumerate(self.fields):
            label = QLabel(field_name)
            line_edit = QLineEdit()
            line_edit.setReadOnly(True)
            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(line_edit, i, 1)
            self.input_widgets[field_name] = line_edit

        self.setLayout(grid_layout)
    def update_device_info(self,new_device_info:list):
        for i in range(len(new_device_info)):
            self.input_widgets[self.fields[i]].setText(str(new_device_info[i]))
            
        