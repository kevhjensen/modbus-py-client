from PyQt6.QtWidgets import QGroupBox,QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QIntValidator,QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
class Configuration(QGroupBox):
    def __init__(self,callbacks):
        super().__init__("Configuration")
        self.callbacks = callbacks
        self.init_ui()
        self.signal_bind()
    def init_ui(self):
        layout_QV = QVBoxLayout()

        # Fields and labels
        self.fields = [
            "Auth (0: Disable, 1: Enable)",
            "EvccidAuth (0: Disable, 1: Enable)",
            "MaxEnergy (kWh,0 is unlimited)",
            "MaxPower (kW,0 is unlimited)",
            "MaxCurrent (A,0 is unlimited)",
            "MaxDuration (minutes,0 is unlimited)",
            "RfidEndian (0: little endian, 1: big endian)",
            "ISO-15118 enable (0: Disable, 1: Enable)",
            "ISO-15118 PnC enable (0: Disable, 1: Enable)"
        ]

        # Store input widgets
        self.input_widgets = {}

        grid_layout = QGridLayout()
        for i, field_name in enumerate(self.fields):
            label = QLabel(field_name)
            line_edit = QLineEdit()
            if i in {0,1,6,7,8}:
                validator = QRegularExpressionValidator(QRegularExpression("^[01]$"), self)  # Only allows '0' or '1'
                line_edit.setValidator(validator)
            else:
                validator = QIntValidator(0, 65535, self)
                line_edit.setValidator(validator)
            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(line_edit, i, 1)
            self.input_widgets[field_name] = line_edit

        layout_QV.addLayout(grid_layout)

        # Save button
        self.save_button = QPushButton("Save Config")
        layout_QV.addWidget(self.save_button)

        self.setLayout(layout_QV)
    
    def signal_bind(self):
        self.save_button.clicked.connect(self.save_config)
    def save_config(self):
        if self.callbacks["save"]:
            self.callbacks["save"](self.input_widgets)

    def populate_configuration_fields(self,config_values):
        """Populate the configuration fields with values from the Modbus device."""
        for i, field_name in enumerate(self.fields):
            if field_name in self.input_widgets:
                self.input_widgets[field_name].setText(str(config_values[i]))  # Update the field with the retrieved value