import os
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6 import uic
from controllers.stats_controller import StatsController
from PyQt6.QtGui import QPixmap


class LoginPage(QWidget):
    player_check_clicked = pyqtSignal(str)
    start_clicked = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Configure l'interface utilisateur en chargeant le fichier .ui"""
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "login_page.ui")
        uic.loadUi(ui_path, self)
        self.label_error.setStyleSheet("color: #e74c3c;")
        img_path = os.path.join(os.path.dirname(__file__), "..", "ressources", "wall_background.jpg")
        self.background_wall.setPixmap(QPixmap(img_path))
        self.background_wall.setScaledContents(True)
    
    def connect_signals(self):
        self.btn_start.clicked.connect(self.on_play_clicked)
        self.username_entry.returnPressed.connect(self.on_play_clicked)
    
    def on_play_clicked(self):
        player_name = self.username_entry.text().strip()
        if not player_name:
            self.label_error.setText("⚠️ Please enter a username to start playing.")
            self.username_entry.setFocus()
            return
        if len(player_name) < 2:
            self.label_error.setText("⚠️ Your username must be at least 2 characters long.")
            self.username_entry.setFocus()
            return
        self.label_error.clear()
        if not StatsController.player_exists(player_name):
                if self.warrior_radio.isChecked():
                    character_class = "Warrior"
                elif self.mage_radio.isChecked():
                    character_class = "Mage"
                else:
                    self.label_error.setText("Please choose a character class if you are a new player.")
                    return
                StatsController.save_new_player(player_name, character_class)
        self.label_error.clear()
        self.start_clicked.emit(player_name)
    
    def reset(self):
        self.username_entry.clear()
        self.label_error.clear()
        self.username_entry.setFocus()
    
    def set_player_name(self, name):
        self.username_entry.setText(name)
