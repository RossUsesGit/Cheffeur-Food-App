from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys, os, requests

API_KEY = "b30c48b00e76492eae8351c72971925d"  # Replace with your actual Spoonacular API key

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CHEFFEUR")
        self.setFixedSize(800, 700)
        self.current_calories = "N/A"
        self.setupMenu()
        self.setupUI()

    def setupUI(self):
        # ComboBox for Ingredients
        self.text_edit = QComboBox()
        self.text_edit.setEditable(True)
        self.text_edit.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.text_edit.setPlaceholderText("Ingredients")
        self.text_edit.setMinimumWidth(200)
        self.text_edit.setMaxVisibleItems(10)
        self.text_edit.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.text_edit.lineEdit().editingFinished.connect(self.fetch_calories)

        # Buttons
        self.add_ingredient = QPushButton("Add")
        self.edit_ingredient = QPushButton("Edit")
        self.delete_ingredient = QPushButton("Delete")

        self.add_ingredient.clicked.connect(self.add_ingredient_row)
        self.edit_ingredient.clicked.connect(self.edit_ingredient_row)
        self.delete_ingredient.clicked.connect(self.delete_ingredient_row)

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
        self.table.setHorizontalHeaderLabels(["Ingredients", "Calories"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.table, 2, 1, 1, 2)

        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

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
        self.msg_box.setText("CHEFFEUR - Ingredient Tracker with Calorie Lookup")
        self.msg_box.exec()

    def show_help_window(self):
        self.msg_box = QMessageBox(self)
        self.msg_box.setIcon(QMessageBox.Icon.Information)
        self.msg_box.setWindowTitle("Help")
        self.msg_box.setInformativeText("Type an ingredient, press Enter to fetch calories, then Add/Edit/Delete.")
        self.msg_box.exec()

    def fetch_calories(self):
        ingredient = self.text_edit.currentText()
        if not ingredient:
            return
        url = f"https://api.spoonacular.com/food/ingredients/search?query={ingredient}&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        if data["results"]:
            ingredient_id = data["results"][0]["id"]
            info_url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information?amount=100&unit=gram&apiKey={API_KEY}"
            info_response = requests.get(info_url)
            info_data = info_response.json()
            nutrients = info_data.get("nutrition", {}).get("nutrients", [])
            calories = next((n["amount"] for n in nutrients if n["name"] == "Calories"), "N/A")
            self.current_calories = calories
        else:
            self.current_calories = "N/A"

    def add_ingredient_row(self):
        ingredient = self.text_edit.currentText()
        if not ingredient:
            return
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(ingredient))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(self.current_calories)))
        self.text_edit.setCurrentText("")

    def edit_ingredient_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            ingredient = self.text_edit.currentText()
            self.table.setItem(selected, 0, QTableWidgetItem(ingredient))
            self.table.setItem(selected, 1, QTableWidgetItem(str(self.current_calories)))
            self.text_edit.setCurrentText("")

    def delete_ingredient_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
