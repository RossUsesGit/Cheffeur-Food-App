  def dark():
        return """
        QMainWindow {background: #121212;}

        QPushButton {
            background: #1F1F1F;
            color: #E0E0E0;
            border-radius: 6px;
            padding: 6px;
            font-weight: bold;
        }

        QPushButton:hover {
            background: #2A2A2A;
            color: #FFFFFF;
        }

        QPushButton:pressed {
            background: #0D7377;
            color: #FFFFFF;
        }

        QLineEdit, QComboBox, QDateEdit {
            background: #2C2C2C;
            color: #E0E0E0;
            border: 2px solid #0D7377;
            border-radius: 6px;
            padding: 6px;
        }

        QMenuBar {
            background: #1E1E1E;
            color: #E0E0E0;
            padding: 6px;
        }

        QMenuBar::item:selected {
            background: #0D7377;
            color: #FFFFFF;
        }

        QTableWidget {
            background: #1E1E1E;
            color: #E0E0E0;
            gridline-color: #333333;
            selection-background-color: #0D7377;
            selection-color: #FFFFFF;
            padding: 6px;
        }

        QHeaderView::section {
            background: #0D7377;
            color: #FFFFFF;
            font-weight: bold;
            padding: 6px;
        }
        """
