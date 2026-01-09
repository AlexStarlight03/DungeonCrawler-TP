import os
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget
from controllers.stats_controller import StatsController
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPixmap

class GamePage(QWidget):
    back_clicked = pyqtSignal()
    game_finished = pyqtSignal(str, int, int)
    game_started = pyqtSignal(str)
    level1_clicked = pyqtSignal(str, int)
    level2_clicked = pyqtSignal(str, int)
    level3_clicked = pyqtSignal(str, int)
    level4_clicked = pyqtSignal(str, int)
    level5_clicked = pyqtSignal(str, int)

    def __init__(self, player_name):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "game_page.ui")
        uic.loadUi(ui_path, self)
        self.player_name = player_name
        self.stats = StatsController.get_player_statistics(player_name)
        self.init_ui()

    def init_ui(self):
        for i in range(1, 6):
            btn = getattr(self, f"btn_level{i}")
            required_xp = (i - 1) * 100
            btn.setEnabled(self.stats['xp'] >= required_xp)
            btn.clicked.connect(lambda checked, idx=i: self.on_action_clicked(idx))
        
        self.xp_entry.setText(str(self.stats['xp']))
        self.gold_entry.setText(str(self.stats['gold']))
        self.att_entry.setText(str(self.stats['attack']))
        self.class_entry.setText(str(self.stats['character_class']))
        self.name_entry.setText(str(self.stats['name']))
        img_path = os.path.join(os.path.dirname(__file__), "..", "ressources", "wall_background.jpg")
        self.background_wall.setPixmap(QPixmap(img_path))
        self.background_wall.setScaledContents(True)
        self.full_width = self.deathbar.width()
        self.hp_entry.setText(f"HP: {self.stats['hp_current']}/{self.stats['hp_max']}")
        StatsController.update_lifebar(self.lifebar, self.stats['hp_current'], self.stats['hp_max'], self.full_width)
        self.sleep_btn.clicked.connect(self.on_sleep_clicked)

    def on_sleep_clicked(self):
        if self.stats['gold'] >= 5:
            hp_max = StatsController.get_max_hp(self.player_name)
            StatsController.save_stats(
                self.player_name,
                self.stats['level'],
                self.stats['xp'],
                self.stats['gold'] - 5,
                hp_max,
                hp_max,
                self.stats['attack']
            )
            self.stats['gold'] -= 5
            self.gold_entry.setText(str(self.stats['gold']))
            self.hp_entry.setText(f"HP: {str(hp_max)}/{str(hp_max)}")
            self.stats['hp_current'] = hp_max
            StatsController.update_lifebar(self.lifebar, self.stats['hp_current'], self.stats['hp_max'], self.full_width)
        else:
            self.inn_error.show()
            self.inn_error.setText("⚠️ Not enough gold to rest!")

    def on_action_clicked(self, idx):
        if idx == 1:
            self.level1_clicked.emit(self.player_name, 1)
        elif idx == 2:
            self.level2_clicked.emit(self.player_name, 2)
        elif idx == 3:
            self.level3_clicked.emit(self.player_name, 3)
        elif idx == 4:
            self.level4_clicked.emit(self.player_name, 4)
        elif idx == 5:
            self.level5_clicked.emit(self.player_name, 5)

    def start_game(self, player_name):
        self.game_started.emit(player_name)
        
