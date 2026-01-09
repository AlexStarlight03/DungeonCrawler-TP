from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import os
from datetime import datetime

DATABASE_URL = "postgresql://neondb_owner:npg_VKQ0tEAx6FNl@ep-billowing-shape-adseungn-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

db = PostgresqlExtDatabase(
    DATABASE_URL,
    autorollback=True
)

class BaseModel(Model):
    """Modèle de base pour tous les modèles"""
    class Meta:
        database = db

class Heroes(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=False, unique=True)
    character_class = CharField(max_length=20, null=False)
    level = IntegerField(default=1, null=False)
    xp = IntegerField(default=0, null=False)
    gold = IntegerField(default=0, null=False)
    hp_current = IntegerField(default=100, null=False)
    hp_max = IntegerField(default=100, null=False)
    attack = IntegerField(default=5, null=False)

class Monsters(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=False, unique=True)
    img_url = CharField(max_length=255, null=False)
    hp_base = IntegerField()
    attack = IntegerField()
    xp_reward = IntegerField()

class Dungeons(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False)
    boss_id = ForeignKeyField(Monsters, backref='dungeons', null=False)


def init_database():
    try: 
        db.connect(reuse_if_open=True)
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return False
    db.create_tables([Heroes, Monsters, Dungeons], safe=True)
    init_monsters()
    print("✅ Base de données initialisée")

def close_database():
    if db and not db.is_closed():
        db.close()
        print("🔌 Connexion fermée")

def init_monsters():
    monster_list = [
        {'name': 'Goblin', 'img_url': 'ressources/goblin.png', 'hp_base': 50, 'attack': 10, 'xp_reward': 20},
        {'name': 'Orc', 'img_url': 'ressources/orc.png', 'hp_base': 80, 'attack': 20, 'xp_reward': 40},
        {'name': 'Troll', 'img_url': 'ressources/troll.png', 'hp_base': 100, 'attack': 30, 'xp_reward': 60},
        {'name': 'Dragon', 'img_url': 'ressources/dragon.png', 'hp_base': 150, 'attack': 40, 'xp_reward': 80},
        {'name': 'Chimera', 'img_url': 'ressources/chimera.png', 'hp_base': 200, 'attack': 50, 'xp_reward': 100},
    ]
    for monster in monster_list:
        try:
            created = Monsters.get_or_create(
                name=monster['name'],
                defaults={
                    'img_url': monster['img_url'],
                    'hp_base': monster['hp_base'],
                    'attack': monster['attack'],
                    'xp_reward': monster['xp_reward'],
                }
            )
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout du monstre {monster['name']}: {e}")

def create_monster(level):
    monster_types = ['Goblin', 'Orc', 'Troll', 'Dragon', 'Chimera']
    name = monster_types[level % len(monster_types) - 1]
    try:
        monster = Monsters.get(Monsters.name == name)
        return monster
    except Exception as e:
        print(f"❌ Erreur lors de la création du monstre: {e}")
        return None

def save_player(player_name, character_class):
    try:
        if character_class == 'Warrior':
            hp_max = 150
            attack = 15
        else:
            hp_max = 100
            attack = 25

        new_player = Heroes.create(
            name=player_name.strip(),
            character_class=character_class,
            level=1,
            xp=0,
            gold=0,
            hp_max=hp_max,
            hp_current=hp_max,
            attack=attack
        )
        print(f"✅ Joueur sauvegardé: {player_name} - Class : {character_class}")
        return new_player
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return None
    
def get_player_stats(player_name):
    try:
        stats = (
            Heroes
            .select(
                (Heroes.name),
                (Heroes.character_class),
                (Heroes.level),
                (Heroes.xp),
                (Heroes.gold),
                (Heroes.hp_current),
                (Heroes.hp_max),
                (Heroes.attack),
            )
            .where(Heroes.name == player_name)
            .dicts()
            .first()
        )
        return stats
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return {'level': 1, 'xp': 0, 'gold': 0, 'hp_current': 100, 'hp_max': 100, 'attack': 5}
    
def reset_player(player_name):
    """Supprime les informations d'un joueur après une partie (victoire ou défaite)"""
    try:
        deleted = Heroes.delete().where(Heroes.name == player_name).execute()
        print(f"✅ Joueur réinitialisé: {player_name}")
        return deleted
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 0
    
def player_exists(player_name):
    """Vérifie si un joueur existe dans la base de données"""
    try:
        exists = Heroes.select().where(Heroes.name == player_name).exists()
        return exists
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
def save_stats(player_name, level, xp, gold, hp_current, hp_max, attack):
    try:
        new_stats = (
            Heroes
            .update(
                level=level,
                xp=xp,
                gold=gold,
                hp_current=hp_current,
                hp_max=hp_max,
                attack=attack
            )
            .where(Heroes.name == player_name)
            .execute()
        )
        print(f"✅ Statistiques mises à jour pour: {player_name}")
        return new_stats
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return 0