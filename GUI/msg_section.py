from PyQt6.QtWidgets import QGroupBox,QTextEdit,QVBoxLayout
class Message(QGroupBox):
    def __init__(self):
        super().__init__("Message")

        # Create a vertical layout for the QGroupBox
        layout = QVBoxLayout()

        # Create a scroll area and set the group box as its widget
        self.info_area = QTextEdit(self)
        self.info_area.setReadOnly(True)
        self.info_area.setPlaceholderText("Messages will appear here...")
        
        # Add the QTextEdit to the layout
        layout.addWidget(self.info_area)

        # Set the layout for the QGroupBox
        self.setLayout(layout)
    
    def append_message(self,message):
        """Append a new message to the info area."""
        self.info_area.append(message + '\n')