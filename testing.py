from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        # Create two buttons
        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")

        # Add a spacer item
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout.addWidget(button1)
        layout.addItem(spacer)  # Adds expandable space
        layout.addWidget(button2)

        self.setLayout(layout)

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
