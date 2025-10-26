from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import requests, webbrowser

class RecipeSearch(QMainWindow):
    def __init__(self, api_key, theme_stylesheet, ingredients=None):
        super().__init__()

        self.api_key = api_key
        self.ingredients = ingredients or []
        self.setWindowTitle("Recipe Search")
        self.setFixedSize(700, 600)
        self.setStyleSheet(theme_stylesheet)

        # UI Elements
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter ingredient or recipe name...")
        self.query_input.setStyleSheet("QLineEdit { font-style: italic; }")

        self.search_button = QPushButton("Search Recipes")
        self.search_button.clicked.connect(self.SearchRecipes)

        # URL Redirects for each recipe (Foodista Link)
        self.results_table = QTableWidget(0, 4)
        self.results_table.setHorizontalHeaderLabels(["Title", "Ready In (min)", "Servings", "Link"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.results_table.cellClicked.connect(self.OpenRecipeLink)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.query_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.results_table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Automatically search if ingredients in table exist
        if self.ingredients:
            self.query_input.setText(", ".join(self.ingredients))
            QTimer.singleShot(300, self.SearchRecipes)  # run after UI fully loads

    def SearchRecipes(self):
        query = self.query_input.text().strip()
        if not query:
            QMessageBox.warning(self,"Error", "No ingredients entered.")  # If there are no ingredients in the table, return a warning and do nothing
            return 

        # Use addRecipeInformation=true to include readyInMinutes, servings, and sourceUrl
        url = (
            f"https://api.spoonacular.com/recipes/complexSearch"
            f"?includeIngredients={query}&number=10&addRecipeInformation=true&apiKey={self.api_key}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            QMessageBox.critical(self, "API Error", f"Error {response.status_code}: Unable to fetch recipes.")
            return

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            QMessageBox.critical(self, "API Error", "Invalid response received from API.")
            return

        results = data.get("results", [])
        self.results_table.setRowCount(0)

        if not results:
            QMessageBox.information(self, "No Results", "No recipes found for the given ingredients.")
            return

        for recipe in results:
            row = self.results_table.rowCount()
            self.results_table.insertRow(row)

            title = recipe.get("title", "N/A")
            ready_in = recipe.get("readyInMinutes", "N/A")
            servings = recipe.get("servings", "N/A")
            source_url = recipe.get("sourceUrl", "https://spoonacular.com")  # fallback if there are no other recipe links returned

            # Fill table with info from Spoonacular
            self.results_table.setItem(row, 0, QTableWidgetItem(title))
            self.results_table.setItem(row, 1, QTableWidgetItem(str(ready_in)))
            self.results_table.setItem(row, 2, QTableWidgetItem(str(servings)))

            # Clickable Recipe Redirects
            link_item = QTableWidgetItem(title)
            link_item.setForeground(QBrush(QColor(0, 102, 204)))  # blue text like a hyperlink for universal understanding
            link_item.setData(Qt.ItemDataRole.UserRole, source_url)
            link_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)  # Make the link non-editable
            self.results_table.setItem(row, 3, link_item)

    def OpenRecipeLink(self, row, column):
        if column == 3:  # Only open when clicking "Link" column
            item = self.results_table.item(row, column)
            if item:
                url = item.data(Qt.ItemDataRole.UserRole)
                if url:
                    webbrowser.open(url)
