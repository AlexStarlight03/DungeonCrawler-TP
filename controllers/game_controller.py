from PyQt6.QtCore import QObject, pyqtSignal
from database import create_monster


class GameController(QObject):
    game_over = pyqtSignal(int, int)
    stats_changed = pyqtSignal(dict)
    attack_made = pyqtSignal(int)
    
    
    def __init__(self, game_area):
        super().__init__()
        self.game_area = game_area

    
    def get_monster(self, level):
        self.level = level
        monster = create_monster(self.level)
        return monster

    def start_game(self, level):
        self.level = level
    
    def update_lifebar(self, bar_widget, current_hp, max_hp, full_width=330):
        percent = max(0, min(1, current_hp / max_hp))
        bar_widget.setFixedWidth(int(full_width * percent))