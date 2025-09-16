from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys,os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cheffeur")
        self.setFixedSize(800,700)
        self.setupMenu()
        self.setupUI()

    

    def setupUI(self):
        
        # Line Edit
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("Add")

        # Buttons
        self.add_ingredient = QPushButton("Add")
        self.edit_ingredient = QPushButton("Edit")
        self.delete_ingredient = QPushButton("Delete")
        
        # Layout
        self.main_layout = QGridLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.text_edit)
        button_layout.addWidget(self.add_ingredient)
        button_layout.addWidget(self.edit_ingredient)
        button_layout.addWidget(self.delete_ingredient)
        self.main_layout.addLayout(button_layout, 1, 1, 1, 2)
        
        # Table
        self.table = QTableWidget(0, 2)  
        self.table.setHorizontalHeaderLabels(["Ingredients" , "Calories"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.table, 2, 1, 1, 2)  
        
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

        




    # Setup Menu

    def setupMenu(self):

        self.menu_bar = self.menuBar()
    
        self.options_menu = self.menu_bar.addMenu("Options")

        self.about_section = self.options_menu.addAction("About")
        self.about_section.triggered.connect(self.show_about_window)

        self.help_section = self.options_menu.addAction("Help")
        self.help_section.triggered.connect(self.show_help_window)

        self.exit_button = self.options_menu.addAction("Exit")
        self.exit_button.triggered.connect(lambda: self.close())

        self.themes_menu = self.menu_bar.addMenu("Themes")
        self.default_theme = self.themes_menu.addAction("Default")

    def show_about_window(self):
        self.msg_box = QMessageBox(self)
        self.msg_box.setIcon(QMessageBox.Icon.Information)
        self.msg_box.setWindowTitle("About")
        self.msg_box.setText("test")
        self.msg_box.exec()

    def show_help_window(self):
        self.msg_box = QMessageBox(self)
        self.msg_box.setIcon(QMessageBox.Icon.Information)
        self.msg_box.setWindowTitle("Help")
        self.msg_box.setInformativeText("test")
        self.msg_box.exec()





app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()