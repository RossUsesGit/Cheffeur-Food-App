from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from themes import Themes
from splash import SplashScreen
import sys, requests

# ✅ Spoonacular API key (replace with your own)
API_KEY = "b30c48b00e76492eae8351c72971925d"


# -----------------------------
# 🧠 MAIN WINDOW CLASS
# -----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Window setup ---
        self.setWindowTitle("CHEFFEUR")                # App title
        self.setFixedSize(850, 700)                    # Fixed window size
        self.current_calories = "N/A"                  # Default calorie value
        self.setStyleSheet(Themes.default())                  
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # --- Initialize components ---
        self.setupMenu()                               # Create top menu bar
        self.setupUI()                                 # Create main interface

    # -----------------------------
    # 🧩 MAIN INTERFACE SETUP
    # -----------------------------

    def setupUI(self):
        # Input field for ingredient name (egg, flour, butter, etc)
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("insert ingredient here...")

        # Input field for unit (grams, cups, etc)
        self.unit_edit = QLineEdit()
        self.unit_edit.setPlaceholderText("insert unit here...")

        # Input field for amount (how many units)
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("insert amount here...")

        # Make placeholder text italic
        self.text_edit.setStyleSheet("QLineEdit { font-style: italic; }")
        self.text_edit.setMinimumWidth(200) 
        self.unit_edit.setStyleSheet("QLineEdit { font-style: italic; }")
        self.unit_edit.setMinimumWidth(200)
        self.amount_edit.setStyleSheet("QLineEdit { font-style: italic; }")
        self.amount_edit.setMinimumWidth(200)  

        # --- Buttons for table actions ---
        self.add_ingredient = QPushButton("Add")
        self.delete_ingredient = QPushButton("Delete")
        self.calorie_search = QPushButton("Nutrition Search")
        self.recipe_search = QPushButton("Recipe Search")

        # Connect button actions to functions
        self.add_ingredient.clicked.connect(self.add_ingredient_row)
        self.delete_ingredient.clicked.connect(self.delete_ingredient_row)
        self.calorie_search.clicked.connect(self.fetch_calories)

        # --- Layout for input and buttons ---
        button_layout = QGridLayout()
        button_layout.addWidget(self.text_edit,0,0,1,1)
        button_layout.addWidget(self.amount_edit,1,0,1,1)
        button_layout.addWidget(self.unit_edit,2,0,1,1)
        button_layout.addWidget(self.add_ingredient,0,1,1,1)
        button_layout.addWidget(self.delete_ingredient,0,2,1,1)
        button_layout.addWidget(self.calorie_search,1,1,1,2)
        button_layout.addWidget(self.recipe_search,2,1,2,2)

        # --- Table setup ---
        self.table = QTableWidget(0, 11)  # 10 columns total
        self.table.setHorizontalHeaderLabels([
            "Ingredient",
            "Amount",
            "Unit",
            "Calories (kcal)",
            "Fat (g)",
            "Saturated Fat (g)",
            "Carbohydrates (g)",
            "Sugar (g)",
            "Protein (g)",
            "Cholesterol (mg)",
            "Sodium (mg)"
        ])

        # Adjust column stretch and resizing
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        # --- Main grid layout ---
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(button_layout, 1, 1, 1, 2)   # Add input+buttons
        self.main_layout.addWidget(self.table, 2, 1, 1, 1)      # Add ingredient table

        # --- Central widget ---
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)


    # -----------------------------
    # 🧾 MENU BAR SETUP
    # -----------------------------
    def setupMenu(self):
        self.menu_bar = self.menuBar()

        # --- Options Menu ---
        self.options_menu = self.menu_bar.addMenu("Options")

        # About Section
        self.about_section = self.options_menu.addAction("About")
        self.about_section.triggered.connect(self.show_about_window)

        # Help Section
        self.help_section = self.options_menu.addAction("Help")
        self.help_section.triggered.connect(self.show_help_window)

        # Exit Button
        self.exit_button = self.options_menu.addAction("Exit")
        self.exit_button.triggered.connect(lambda: self.close())

        # --- Themes Menu (for future expansion) ---
        self.themes_menu = self.menu_bar.addMenu("Themes")
        self.default_theme = self.themes_menu.addAction("Default")
        self.strawberry_theme = self.themes_menu.addAction("Strawberry")
        self.bread_theme = self.themes_menu.addAction("Bread")
        self.cyberpunk_theme= self.themes_menu.addAction("Cyberpunk")
        self.matrix_theme = self.themes_menu.addAction("Matrix")
        self.carbon_rose_theme = self.themes_menu.addAction("Carbon Rose")

        self.default_theme.triggered.connect(lambda: self.change_theme("Default"))
        self.strawberry_theme.triggered.connect(lambda: self.change_theme("Strawberry"))
        self.bread_theme.triggered.connect(lambda: self.change_theme("Bread"))
        self.cyberpunk_theme.triggered.connect(lambda:self.change_theme("Cyberpunk"))
        self.matrix_theme.triggered.connect(lambda:self.change_theme("Matrix"))
        self.carbon_rose_theme.triggered.connect(lambda:self.change_theme("Carbon Rose"))


    # -----------------------------
    # ℹ️ ABOUT WINDOW
    # -----------------------------
    def show_about_window(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("About")
        msg_box.setText("CHEFFEUR - Ingredient Tracker with Calorie Lookup")
        msg_box.exec()


    # -----------------------------
    # ❓ HELP WINDOW
    # -----------------------------
    def show_help_window(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Help")
        msg_box.setInformativeText(
            "Type an ingredient, press Enter to fetch calories, then Add.\n"
            "To edit: select a row, type new ingredient, press Edit.\n"
            "To delete: select a row, press Delete."
        )
        msg_box.exec()


    def fetch_calories(self):
        for row in range(self.table.rowCount()):
            ingredient = self.table.item(row, 0).text()
            amount = self.table.item(row, 1).text()
            unit = self.table.item(row, 2).text()

            url = f"https://api.spoonacular.com/food/ingredients/search?query={ingredient}&apiKey={API_KEY}"
            response = requests.get(url)
            data = response.json()

            if not data["results"]:
                continue

            ingredient_id = data["results"][0]["id"]
            info_url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information?amount={amount}&unit={unit}&apiKey={API_KEY}"
            info_response = requests.get(info_url)
            info_data = info_response.json()

            nutrients = info_data.get("nutrition", {}).get("nutrients", [])

            def get(name):
                return str(next((n["amount"] for n in nutrients if n["name"] == name), "N/A"))

            self.table.setItem(row, 3, QTableWidgetItem(get("Calories")))
            self.table.setItem(row, 4, QTableWidgetItem(get("Fat")))
            self.table.setItem(row, 5, QTableWidgetItem(get("Saturated Fat")))  
            self.table.setItem(row, 6, QTableWidgetItem(get("Carbohydrates")))
            self.table.setItem(row, 7, QTableWidgetItem(get("Sugar")))
            self.table.setItem(row, 8, QTableWidgetItem(get("Protein")))
            self.table.setItem(row, 9, QTableWidgetItem(get("Cholesterol")))
            self.table.setItem(row, 10, QTableWidgetItem(get("Sodium")))


    def add_ingredient_row(self):
        ingredient = self.text_edit.text()
        unit = self.unit_edit.text()
        amount = self.amount_edit.text()

        if not ingredient:
            QMessageBox.warning(self, "Error", "No ingredient Entered.")
            self.clear_inputs()
            return
        if not amount:
            QMessageBox.warning(self, "Error", "No Amount Entered.")
            self.clear_inputs()
            return
        if not unit:
            QMessageBox.warning(self, "Error", "No Unit Entered.")
            self.clear_inputs()
            return
       

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(ingredient))
        self.table.setItem(row_position,1, QTableWidgetItem(amount))
        self.table.setItem(row_position,2, QTableWidgetItem(unit))
        

        self.clear_inputs()

    # -----------------------------
    # ❌ DELETE SELECTED ROW
    # -----------------------------
    def delete_ingredient_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)
        else:
            QMessageBox.warning(self,"Error", "No items to delete.")

    def change_theme(self,theme_name):
        if theme_name == "Default":
            self.setStyleSheet(Themes.default())
        elif theme_name == "Strawberry":
             self.setStyleSheet(Themes.strawberry())
        elif theme_name == "Bread":
             self.setStyleSheet(Themes.bread())
        elif theme_name == "Cyberpunk":
             self.setStyleSheet(Themes.cyberpunk())
        elif theme_name == "Matrix":
             self.setStyleSheet(Themes.matrix())
        elif theme_name == "Carbon Rose":
             self.setStyleSheet(Themes.carbon_rose())


    def clear_inputs(self):
        self.text_edit.clear()
        self.unit_edit.clear()
        self.amount_edit.clear()


# -----------------------------
# 🚀 RUN APPLICATION
# -----------------------------
app = QApplication(sys.argv)
window = MainWindow()
splash = SplashScreen()
window.show()
app.exec()
