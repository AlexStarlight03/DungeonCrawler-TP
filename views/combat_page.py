import os
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic
from controllers.game_controller import GameController
from controllers.stats_controller import StatsController
import random
from PyQt6.QtGui import QPixmap


class CombatPage(QWidget):
    """
    Page de combat du jeu
    """
    game_finished = pyqtSignal(str, int, int, bool)

    def __init__(self):
        super().__init__()
        self.player_name = ""
        self.game_controller = None
        self.setup_ui()

    def setup_ui(self):
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "combat_page.ui")
        uic.loadUi(ui_path, self)
        img_path = os.path.join(os.path.dirname(__file__), "..", "ressources", "wall_background.jpg")
        self.background_wall.setPixmap(QPixmap(img_path))
        self.background_wall.setScaledContents(True)
        self.label_help.hide()


    def start_game(self, player_name, level):
        self.player_name = player_name
        self.level = level
        self.stats = StatsController.get_player_statistics(player_name)
        self.game_controller = GameController(self)
        self.monster = self.game_controller.get_monster(level)
        self.monster_hp = getattr(self.monster, 'hp_base', 100)
        img_path = os.path.join(os.path.dirname(__file__), "..", self.monster.img_url)
        self.monster_entry.setPixmap(QPixmap(img_path))
        self.monster_entry.setScaledContents(True)
        hero_path = os.path.join(os.path.dirname(__file__), "..", "ressources", f"{self.stats['character_class'].lower()}.png")
        self.hero_entry.setPixmap(QPixmap(hero_path))
        self.hero_entry.setScaledContents(True)
        self.game_controller.start_game(level)
        self.btn_attack.clicked.connect(self.on_attack_clicked)
        self.monsterhp.setText(f"Ennemy HP: {self.monster_hp}/{getattr(self.monster, 'hp_base', 100)}")
        self.herohp.setText(f"Your HP: {self.stats['hp_current']}/{self.stats['hp_max']}")
        self.full_width = self.deathbar_hero.width()
        StatsController.update_lifebar(self.lifebar_hero, self.stats['hp_current'], self.stats['hp_max'], self.full_width)


    def on_attack_clicked(self):
        self.player_attack(self.stats, self.monster)

    def player_attack(self, player_stats, monster):
        dmg = player_stats['attack'] + random.randint(-5, 5)
        self.label_combat.setText(f"You deal {dmg} damage to the {monster.name}!")
        self.monster_hp -= dmg
        self.monsterhp.setText(f"Ennemy HP: {self.monster_hp}/{getattr(monster, 'hp_base', 100)}")
        StatsController.update_lifebar(self.lifebar_monster, self.monster_hp, getattr(self.monster, 'hp_base', self.deathbar_monster.width()))
        if self.monster_hp <= 0:
            self.on_game_over()
        else:
            self.monster_attack(player_stats, monster)

    def monster_attack(self, player_stats, monster):
        dmg = monster.attack + random.randint(-5, 5)
        self.label_combat2.setText(f"The {monster.name} deals {dmg} damage to you!")
        player_stats['hp_current'] -= dmg
        self.herohp.setText(f"Your HP: {player_stats['hp_current']}/{player_stats['hp_max']}")
        StatsController.update_lifebar(self.lifebar_hero, player_stats['hp_current'], player_stats['hp_max'], self.full_width)
        if player_stats['hp_current'] <= 0:
            self.on_game_over()


    def on_game_over(self):
        if self.monster_hp <= 0:
            score = self.level * random.randint(25, 50)
            gold = random.randint(1, 10) * self.level
            self.label_help.show()
            self.label_help.setText(f"🏆 Victory ! You gain {score} xp and {gold} gold!")
            self.stats['xp'] += score
            self.stats['gold'] += gold
            if self.stats['xp'] >= 100 * self.level:
                self.stats['level'] += 1
                self.stats['attack'] += 10
                self.stats['hp_max'] += 20
                QMessageBox.information(self, "LEVEL UP!", "You leveled up and gained +10 Attack and +20 Max HP!")
            StatsController.save_stats(
                self.player_name,
                self.stats['level'],
                self.stats['xp'],
                self.stats['gold'],
                self.stats['hp_current'],
                self.stats['hp_max'],
                self.stats['attack']
            )
            self.game_finished.emit(self.player_name, score, self.level, False)
        elif self.stats['hp_current'] <= 0:
            self.label_help.show()
            self.label_help.setText(f"💀 Game Over ! Level : {self.level}  XP : {self.stats['xp']}")
            self.game_finished.emit(self.player_name, self.stats['xp'], self.level, True)

    def update_combat_label(self, hero_dmg, monster_hp, monster_dmg, hero_hp):
        self.combat_label.setText(
            f"Hero deals {hero_dmg} damage! Monster HP: {monster_hp}\n"
            f"Monster deals {monster_dmg} damage! Hero HP: {hero_hp}"
        )
