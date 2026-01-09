from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QWidget
from PyQt6.QtCore import Qt
from views.login_page import LoginPage

class MainWindow(QMainWindow):
    PAGE_LOGIN = 0
    PAGE_GAME = 1
    PAGE_COMBAT = 2

    def __init__(self):
        super().__init__()
        self.last_player_name = ""
        self.game_page = None
        self.setup_window()
        self.setup_pages()
        self.connect_signals()

    def setup_window(self):
        self.setWindowTitle("Dungeon Crawler")
        self.setFixedSize(690, 503)
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def setup_pages(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.login_page = LoginPage()
        self.stack.addWidget(self.login_page)       
        self.stack.addWidget(QWidget())
        self.show_login()

    def connect_signals(self):
        self.login_page.start_clicked.connect(self.on_play_clicked)

    def show_login(self):
        self.stack.setCurrentIndex(self.PAGE_LOGIN)
        if self.last_player_name:
            self.login_page.set_player_name(self.last_player_name)

    def show_game(self, player_name):
        self.last_player_name = player_name
        from views.game_page import GamePage
        if hasattr(self, 'game_page') and self.game_page is not None:
            self.stack.removeWidget(self.game_page)
            self.game_page.deleteLater()
        self.game_page = GamePage(player_name)
        self.game_page.back_clicked.connect(self.show_login)
        self.game_page.game_finished.connect(self.on_game_finished)
        self.stack.insertWidget(self.PAGE_GAME, self.game_page)
        self.stack.setCurrentIndex(self.PAGE_GAME)
        self.game_page.start_game(player_name)
        self.game_page.level1_clicked.connect(lambda player, lvl=1: self.show_combat(player, lvl))
        self.game_page.level2_clicked.connect(lambda player, lvl=2: self.show_combat(player, lvl))
        self.game_page.level3_clicked.connect(lambda player, lvl=3: self.show_combat(player, lvl))
        self.game_page.level4_clicked.connect(lambda player, lvl=4: self.show_combat(player, lvl))
        self.game_page.level5_clicked.connect(lambda player, lvl=5: self.show_combat(player, lvl))

    def show_combat(self, player_name, level):
        if hasattr(self, 'combat_page') and self.combat_page is not None:
            self.stack.removeWidget(self.combat_page)
            self.combat_page.deleteLater()
        from views.combat_page import CombatPage
        self.combat_page = CombatPage()
        self.combat_page.game_finished.connect(self.on_game_finished)
        self.stack.insertWidget(self.PAGE_COMBAT, self.combat_page)
        self.combat_page.start_game(player_name, level)
        self.stack.setCurrentIndex(self.PAGE_COMBAT)

    def on_play_clicked(self, player_name):
        self.show_game(player_name)

    def on_game_finished(self, player_name, xp, level, reset):
        from controllers.stats_controller import StatsController
        QMessageBox.information(self, "Game Finished", f"{player_name} finished with {xp} XP at level {level}")
        if reset:
            StatsController.reset_player(player_name)
            self.show_login()
        else:
            self.show_game(player_name)

    def closeEvent(self, event):
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            current = self.stack.currentIndex()
            if current != self.PAGE_LOGIN:
                if current == self.PAGE_GAME:
                    self.game_page.on_back_clicked()
                else:
                    self.show_login()
        else:
            super().keyPressEvent(event)