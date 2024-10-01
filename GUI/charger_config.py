from PyQt6.QtWidgets import QGroupBox,QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel
class Configuration(QGroupBox):
    def __init__(self):
        super().__init__("Configuration")
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
            # Set the default value from the backend
            line_edit.setText("")
            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(line_edit, i, 1)
            self.input_widgets[field_name] = line_edit

        layout_QV.addLayout(grid_layout)

        # Save button
        self.save_button = QPushButton("Save Config")
        layout_QV.addWidget(self.save_button)

        self.setLayout(layout_QV)