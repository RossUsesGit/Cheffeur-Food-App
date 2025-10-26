from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QShortcut, QKeySequence
from themes import Themes
from splash import SplashScreen1
from recipe_window import RecipeSearch
import sys, requests


with open("API_KEY_SPOONACULAR.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        API_KEY = line
        break  
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.setWindowTitle("CHEFFEUR")                
        self.setFixedSize(850, 700)                                    
        self.setStyleSheet(Themes.default())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Initialize Components
        self.SetupMenu()                               # Create top menu bar
        self.SetupUI()                                 # Create UI aspects

        # Shortcuts
        self.fullscreen_trigger = False
        self.fullscreen_toggle = QShortcut(QKeySequence("F11"), self)
        self.fullscreen_toggle.activated.connect(self.FullScreen)

        self.title_bar_trigger = False
        self.title_bar_toggle = QShortcut(QKeySequence("Alt+F11"), self)
        self.title_bar_toggle.activated.connect(self.ShowTitleBar)

    def ShowTitleBar(self):
        if self.title_bar_trigger:
            self.setWindowFlags(Qt.WindowType.Window)
        else:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.title_bar_trigger = not self.title_bar_trigger
        self.show()
        self.CenterWindow()

    def FullScreen(self):
        if self.fullscreen_trigger:
            self.showNormal()
            self.setFixedSize(850, 700)
        else:
            self.showFullScreen()
        self.fullscreen_trigger = not self.fullscreen_trigger

    def CenterWindow(self):
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def SetupUI(self):
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

        # Table Action Buttons
        self.add_ingredient = QPushButton("Add")
        self.delete_ingredient = QPushButton("Delete")
        self.calorie_search = QPushButton("Nutrition Search")
        self.recipe_search = QPushButton("Recipe Search")

        # Connect button actions to functions
        self.add_ingredient.clicked.connect(self.AddIngredientRow)
        self.delete_ingredient.clicked.connect(self.DeleteIngredientRow)
        self.calorie_search.clicked.connect(self.FetchCalories)
        self.recipe_search.clicked.connect(self.FetchRecipes)

        # Inputs and Button Layout
        button_layout = QGridLayout()
        button_layout.addWidget(self.text_edit, 0, 0, 1, 1)
        button_layout.addWidget(self.amount_edit, 1, 0, 1, 1)
        button_layout.addWidget(self.unit_edit, 2, 0, 1, 1)
        button_layout.addWidget(self.add_ingredient, 0, 1, 1, 1)
        button_layout.addWidget(self.delete_ingredient, 0, 2, 1, 1)
        button_layout.addWidget(self.calorie_search, 1, 1, 1, 2)
        button_layout.addWidget(self.recipe_search, 2, 1, 2, 2)

        # Table
        self.table = QTableWidget(0, 11)
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

        # Main Grid Layout
        self.main_layout = QGridLayout()
        self.main_layout.addLayout(button_layout, 1, 1, 1, 2)
        self.main_layout.addWidget(self.table, 2, 1, 1, 1)

        # Setting the Central Widget
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

    def SetupMenu(self):
        self.menu_bar = self.menuBar()

        # Options Menu
        self.options_menu = self.menu_bar.addMenu("Options")

        # About Section
        self.about_section = self.options_menu.addAction("About")
        self.about_section.triggered.connect(self.ShowAboutWindow)

        # Help Section
        self.help_section = self.options_menu.addAction("Help")
        self.help_section.triggered.connect(self.ShowHelpWindow)

        # Exit Button
        self.exit_button = self.options_menu.addAction("Exit")
        self.exit_button.triggered.connect(lambda: self.close())

        # Themes Menu
        self.themes_menu = self.menu_bar.addMenu("Themes")

        self.default_theme = self.themes_menu.addAction("Default")
        self.dark_theme = self.themes_menu.addAction("Dark")
        self.strawberry_theme = self.themes_menu.addAction("Strawberry")
        self.bread_theme = self.themes_menu.addAction("Bread")
        self.salad_theme = self.themes_menu.addAction("Salad")
        self.melon_theme = self.themes_menu.addAction("Melon")
        self.peppermint_theme = self.themes_menu.addAction("Peppermint")
        self.cyberpunk_theme = self.themes_menu.addAction("Cyberpunk")
        self.matrix_theme = self.themes_menu.addAction("Matrix")
        self.carbon_rose_theme = self.themes_menu.addAction("Carbon Rose")
        self.ocean_breeze_theme = self.themes_menu.addAction("Ocean Breeze")
        self.midnight_mint_theme = self.themes_menu.addAction("Midnight Mint")
        self.blue_baby_theme = self.themes_menu.addAction("Blue Baby")
        self.ocean_glow_theme = self.themes_menu.addAction("Ocean Glow")

        # Theme Connections
        self.default_theme.triggered.connect(lambda: self.ChangeTheme("Default"))
        self.dark_theme.triggered.connect(lambda: self.ChangeTheme("Dark"))
        self.strawberry_theme.triggered.connect(lambda: self.ChangeTheme("Strawberry"))
        self.bread_theme.triggered.connect(lambda: self.ChangeTheme("Bread"))
        self.salad_theme.triggered.connect(lambda: self.ChangeTheme("Salad"))
        self.melon_theme.triggered.connect(lambda: self.ChangeTheme("Melon"))
        self.peppermint_theme.triggered.connect(lambda: self.ChangeTheme("Peppermint"))
        self.cyberpunk_theme.triggered.connect(lambda: self.ChangeTheme("Cyberpunk"))
        self.matrix_theme.triggered.connect(lambda: self.ChangeTheme("Matrix"))
        self.carbon_rose_theme.triggered.connect(lambda: self.ChangeTheme("Carbon Rose"))
        self.ocean_breeze_theme.triggered.connect(lambda: self.ChangeTheme("Ocean Breeze"))
        self.midnight_mint_theme.triggered.connect(lambda: self.ChangeTheme("Midnight Mint"))
        self.blue_baby_theme.triggered.connect(lambda: self.ChangeTheme("Blue Baby"))
        self.ocean_glow_theme.triggered.connect(lambda: self.ChangeTheme("Ocean Glow"))

    def ShowAboutWindow(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("About")
        msg_box.setText("CHEFFEUR - Ingredient Tracker with Calorie Lookup")
        msg_box.exec()

    def ShowHelpWindow(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Help")
        msg_box.setInformativeText(
            "Type an ingredient, press Enter to fetch calories, then Add.\n"
            "To edit: select a row, type new ingredient, press Edit.\n"
            "To delete: select a row, press Delete."
        )
        msg_box.exec()

    def FetchCalories(self):
        row = self.table.rowCount()
        if not row:
            QMessageBox.warning(self, "Error", "No ingredients are added.")
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

    def FetchRecipes(self):
        ingredients = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                ingredients.append(item.text())

        # Open RecipeSearch window, passing ingredients + current theme
        self.recipe_window = RecipeSearch(API_KEY, self.styleSheet(), ingredients)
        self.recipe_window.show()

    def AddIngredientRow(self):
        ingredient = self.text_edit.text()
        unit = self.unit_edit.text()
        amount = self.amount_edit.text()

        if not ingredient:
            QMessageBox.warning(self, "Error", "No ingredient Entered.")
            self.ClearInputs()
            return
        if not amount:
            QMessageBox.warning(self, "Error", "No Amount Entered.")
            self.ClearInputs()
            return
        if not unit:
            QMessageBox.warning(self, "Error", "No Unit Entered.")
            self.ClearInputs()
            return

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(ingredient))
        self.table.setItem(row_position, 1, QTableWidgetItem(amount))
        self.table.setItem(row_position, 2, QTableWidgetItem(unit))
        self.ClearInputs()

    def DeleteIngredientRow(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)
        else:
            QMessageBox.warning(self, "Error", "No items to delete.")

    def ChangeTheme(self, theme_name):
        if theme_name == "Default":
            self.setStyleSheet(Themes.default())
        elif theme_name == "Dark":
            self.setStyleSheet(Themes.dark())
        elif theme_name == "Strawberry":
            self.setStyleSheet(Themes.strawberry())
        elif theme_name == "Bread":
            self.setStyleSheet(Themes.bread())
        elif theme_name == "Salad":
            self.setStyleSheet(Themes.salad())
        elif theme_name == "Melon":
            self.setStyleSheet(Themes.melon())
        elif theme_name == "Peppermint":
            self.setStyleSheet(Themes.peppermint())
        elif theme_name == "Cyberpunk":
            self.setStyleSheet(Themes.cyberpunk())
        elif theme_name == "Matrix":
            self.setStyleSheet(Themes.matrix())
        elif theme_name == "Carbon Rose":
            self.setStyleSheet(Themes.carbon_rose())
        elif theme_name == "Ocean Breeze":
            self.setStyleSheet(Themes.ocean_breeze())
        elif theme_name == "Midnight Mint":
            self.setStyleSheet(Themes.midnight_mint())
        elif theme_name == "Blue Baby":
            self.setStyleSheet(Themes.blue_baby())
        elif theme_name == "Ocean Glow":
            self.setStyleSheet(Themes.ocean_glow())

    def ClearInputs(self):
        self.text_edit.clear()
        self.unit_edit.clear()
        self.amount_edit.clear()


# App Start 
app = QApplication(sys.argv)
window = MainWindow()
splash = SplashScreen1()
splash.show()
splash.finished.connect(lambda: window.show())
app.exec()
