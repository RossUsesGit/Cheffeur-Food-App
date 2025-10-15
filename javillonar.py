def ocean_breeze():
    return """
    QMainWindow {
        background: #B0CDE0;
    }

    QPushButton {
        background: #0D4C7D;
        color: #FFFFFF;
        border-radius: 6px;
        padding: 6px;
    }

    QPushButton:hover {
        background: #1565A8;
        color: #E0F2FF;
    }

    QPushButton:clicked {
        background: #0B3A60;
        color: #B0CDE0;
    }

    QLineEdit {
        background: #6C98B0;
        color: #F0F8FF;
        border-radius: 6px;
        padding: 6px;
    }

    QDateEdit {
        background: #6C98B0;
        color: #F0F8FF;
        border-radius: 6px;
        padding: 6px;
    }

    QComboBox {
        background: #6C98B0;
        color: #F0F8FF;
        border-radius: 6px;
        padding: 6px;
    }

    QMenuBar {
        background: #0D4C7D;
        color: #FFFFFF;
        padding: 6px;
    }

    QMenuBar::item:selected {
        background: #1565A8;
    }

    QTableWidget {
        background: #A1C2D6;
        color: #0B3A60;
        gridline-color: #0D4C7D;
        padding: 6px;
    }

    QHeaderView::section {
        background: #0D4C7D;
        color: #FFFFFF;
        padding: 6px;
    }
    """


def midnight_mint():
    return """
    QMainWindow {
        background: #CDEFEF;
    }

    QPushButton {
        background: #1E1F1C;
        color: #E0FFFF;
        border-radius: 6px;
        padding: 6px;
    }

    QPushButton:hover {
        background: #3B3C38;
        color: #A8E6E6;
    }

    QPushButton:clicked {
        background: #0E0E0E;
        color: #CDEFEF;
    }

    QLineEdit {
        background: #8C8D8A;
        color: #0E0E0E;
        border-radius: 6px;
        padding: 6px;
    }

    QDateEdit {
        background: #8C8D8A;
        color: #0E0E0E;
        border-radius: 6px;
        padding: 6px;
    }

    QComboBox {
        background: #8C8D8A;
        color: #0E0E0E;
        border-radius: 6px;
        padding: 6px;
    }

    QMenuBar {
        background: #1E1F1C;
        color: #E0FFFF;
        padding: 6px;
    }

    QMenuBar::item:selected {
        background: #3B3C38;
    }

    QTableWidget {
        background: #BEEBEA;
        color: #0E0E0E;
        gridline-color: #1E1F1C;
        padding: 6px;
    }

    QHeaderView::section {
        background: #1E1F1C;
        color: #E0FFFF;
        padding: 6px;
    }
    """

self.ocean_breeze_theme = self.themes_menu.addAction("Ocean Breeze")
self.midnight_mint_theme = self.themes_menu.addAction("Midnight Mint")

self.ocean_breeze_theme.triggered.connect(lambda: self.change_theme("Ocean Breeze"))
self.midnight_mint_theme.triggered.connect(lambda: self.change_theme("Midnight Mint"))

    elif theme_name == "Ocean Breeze":
        self.setStyleSheet(Themes.ocean_breeze())
    elif theme_name == "Midnight Mint":
        self.setStyleSheet(Themes.midnight_mint())
