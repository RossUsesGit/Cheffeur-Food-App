from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
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
        self.setFixedSize(800, 700)                    # Fixed window size
        self.current_calories = "N/A"                  # Default calorie value

        # --- Initialize components ---
        self.setupMenu()                               # Create top menu bar
        self.setupUI()                                 # Create main interface


    # -----------------------------
    # 🧩 MAIN INTERFACE SETUP
    # -----------------------------
    def setupUI(self):
        # --- Input field for ingredient ---
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("insert ingredient here...")

        # Make placeholder text italic
        self.text_edit.setStyleSheet("QLineEdit { font-style: italic; }")

        self.text_edit.setMinimumWidth(200)

        # Connect Enter key to calorie fetching
        self.text_edit.returnPressed.connect(self.fetch_calories)

        # --- Buttons for table actions ---
        self.add_ingredient = QPushButton("Add")
        self.edit_ingredient = QPushButton("Edit")
        self.delete_ingredient = QPushButton("Delete")

        # Connect button actions to functions
        self.add_ingredient.clicked.connect(self.add_ingredient_row)
        self.edit_ingredient.clicked.connect(self.edit_ingredient_row)
        self.delete_ingredient.clicked.connect(self.delete_ingredient_row)

        # --- Layout for input and buttons ---
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.text_edit)
        button_layout.addWidget(self.add_ingredient)
        button_layout.addWidget(self.edit_ingredient)
        button_layout.addWidget(self.delete_ingredient)

        # --- Table setup ---
        self.table = QTableWidget(0, 3)                # Start with 0 rows, 2 columns
        self.table.setHorizontalHeaderLabels(["Ingredients", "Unit", "Calories"])
        self.table.horizontalHeader().setStretchLastSection(False)

        # --- Main grid layout ---
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(button_layout, 1, 1, 1, 2)   # Add input+buttons
        self.main_layout.addWidget(self.table, 2, 1, 1, 2)      # Add ingredient table

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


    # -----------------------------
    # 🍽️ FETCH CALORIES FROM API
    # -----------------------------
    def fetch_calories(self):
        ingredient = self.text_edit.text()  # ✅ Get text from QLineEdit
        if not ingredient:
            return

        # Step 1: Search for ingredient ID
        url = f"https://api.spoonacular.com/food/ingredients/search?query={ingredient}&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if data["results"]:
            ingredient_id = data["results"][0]["id"]

            # Step 2: Fetch ingredient info (nutrition)
            info_url = f"https://api.spoonacular.com/food/ingredients/{ingredient_id}/information?amount=100&unit=gram&apiKey={API_KEY}"
            info_response = requests.get(info_url)
            info_data = info_response.json()

            # Step 3: Extract calories
            nutrients = info_data.get("nutrition", {}).get("nutrients", [])
            calories = next((n["amount"] for n in nutrients if n["name"] == "Calories"), "N/A")
            self.current_calories = calories
        else:
            self.current_calories = "N/A"


    # -----------------------------
    # ➕ ADD INGREDIENT ROW
    # -----------------------------
    def add_ingredient_row(self):
        ingredient = self.text_edit.text()
        if not ingredient:
            return

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(ingredient))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(self.current_calories)))

        self.text_edit.clear()  # ✅ Clear input box after adding


    # -----------------------------
    # ✏️ EDIT SELECTED ROW
    # -----------------------------
    def edit_ingredient_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            ingredient = self.text_edit.text()
            self.table.setItem(selected, 0, QTableWidgetItem(ingredient))
            self.table.setItem(selected, 1, QTableWidgetItem(str(self.current_calories)))
            self.text_edit.clear()


    # -----------------------------
    # ❌ DELETE SELECTED ROW
    # -----------------------------
    def delete_ingredient_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)


# -----------------------------
# 🚀 RUN APPLICATION
# -----------------------------
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
