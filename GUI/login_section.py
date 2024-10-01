from PyQt6.QtWidgets import QGroupBox,QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel,QHBoxLayout

class LoginSection(QGroupBox):
    def __init__(self,callbacks):
        super().__init__("Target Device")
        self.callbacks = callbacks
        self.init_ui()
        self.signal_bind()
    def init_ui(self):
        login_section_QV = QVBoxLayout()
        input_section_QG = QGridLayout()
        button_section_QH = QHBoxLayout()
        
        #input
        self.input_ipaddr = QLineEdit(self)
        self.input_ipaddr.setPlaceholderText("Enter IP address")
        self.input_pwd = QLineEdit(self)
        self.input_pwd.setPlaceholderText("Enter password")
        self.input_pwd.setEchoMode(QLineEdit.EchoMode.Password)


        #login,reboot button
        self.login_button = QPushButton('Login', self)
        self.disconnect_button = QPushButton('Disconnect', self)
        self.reboot_button = QPushButton('Reboot', self)
        
        # Add connect section elements to grid layout
        input_section_QG.addWidget(QLabel("IP Address"), 0, 0)
        input_section_QG.addWidget(self.input_ipaddr, 0, 1)
        input_section_QG.addWidget(QLabel("Password"), 1, 0)
        input_section_QG.addWidget(self.input_pwd, 1, 1)
        button_section_QH.addWidget(self.login_button)
        button_section_QH.addWidget(self.disconnect_button)
        button_section_QH.addWidget(self.reboot_button)

        self.login_button.setVisible(True)
        self.disconnect_button.setVisible(False)

        login_section_QV.addLayout(input_section_QG)
        login_section_QV.addLayout(button_section_QH)

        self.setLayout(login_section_QV)
    
    def signal_bind(self):
        self.login_button.clicked.connect(self.login)
        self.reboot_button.clicked.connect(self.reboot)
        self.disconnect_button.clicked.connect(self.disconnect)
    def login(self):
        ipaddr = self.input_ipaddr.text()
        pwd = self.input_pwd.text()
        if self.callbacks["login"]:
            self.callbacks["login"](ipaddr, pwd)
            self.login_button.setVisible(False)
            self.disconnect_button.setVisible(True)
    def reboot(self):
        if self.callbacks["reboot"]:
            self.callbacks["reboot"]()
    
    def disconnect(self):
        if self.callbacks["disconnect"]:
            self.callbacks["disconnect"]()  # Call the disconnect callback
            self.login_button.setVisible(True)
            self.disconnect_button.setVisible(False)

        