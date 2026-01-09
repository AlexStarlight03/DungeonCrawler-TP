from database import save_stats, get_player_stats, save_player, reset_player, player_exists


class StatsController:
    @staticmethod
    def get_player_statistics(player_name):
        return get_player_stats(player_name)
    
    @staticmethod
    def get_curr_level(player_name):
        stats = get_player_stats(player_name)
        if not stats:
            return 1  
        return stats['xp'] // 100 + 1

    @staticmethod
    def get_attack(player_name):
        stats = get_player_stats(player_name)
        if not stats:
            return 1  
        return stats['attack']
    
    @staticmethod
    def get_hp(player_name):
        stats = get_player_stats(player_name)
        if not stats:
            return 1  
        return stats['hp_current']
    
    @staticmethod
    def get_max_hp(player_name):
        stats = get_player_stats(player_name)
        if not stats:
            return 1  
        return stats['hp_max']
    
    @staticmethod
    def save_stats(player_name, level, xp, gold, hp_current, hp_max, attack):
        return save_stats(player_name, level, xp, gold, hp_current, hp_max, attack)
    
    @staticmethod
    def player_exists(player_name):
        return player_exists(player_name)

    @staticmethod
    def save_new_player(player_name, player_class):
        return save_player(player_name, player_class)
    
    @staticmethod
    def reset_player(player_name):
        return reset_player(player_name)
    
    @staticmethod
    def level_up(player_name):
        player = get_player_stats(player_name)
        if player["xp"] >= player["level"] * 100:
            new_level = player["level"] + 1
            save_stats(
                player_name,
                new_level,
                player["xp"],
                player["gold"] + 10,
                player["hp_current"],
                player["hp_max"] + 50,
                player["attack"] + (10 * new_level)
            )
            return True
    
    @staticmethod
    def update_lifebar(bar_widget, current_hp, max_hp, full_width=100):
        percent = max(0, min(1, current_hp / max_hp))
        bar_widget.setFixedWidth(int(full_width * percent))

