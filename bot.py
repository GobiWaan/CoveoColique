from game_message import *
from actions import *
from random import shuffle, choice
import random
from functools import reduce
import operator

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.actions = []
        self.corners = []
        self.extended_corners =[]
        self.spawns = []
        self.gates = []
    
    def att_corner(self, game_message):

        if not self.corners:
            self.corners = self.get_path_corners(game_message) 
            for i in self.corners:
                self.extended_corners += i
            shuffle(self.extended_corners)

        coin = self.extended_corners.pop(0)
        if game_message.playAreas[game_message.teamId].get_tile_at(Position(*coin)) is None:
            self.actions.append(BuildAction(TowerType.SPIKE_SHOOTER, Position(*coin)))


    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        actions = []
        other_team_ids = [team for team in game_message.teams if team != game_message.teamId]

        if not self.corners:
            self.corners = self.get_path_corners(game_message)
            self.path_sides = self.get_path_sides(game_message)
            self.path_sides = reduce(operator.add, self.path_sides, [])
            random.shuffle(self.path_sides)
            for path in game_message.map.paths:
                self.spawns.append(path.tiles[0])
                self.gates.append(path.tiles[-1])


        rand = random.random()

        if not self.get_empty_tiles(game_message):
            rand = 0


        if rand < 0.1:
            if other_team_ids:
                if game_message.round < 10:
                    actions.append(SendReinforcementsAction(EnemyType.LVL1, random.choice(other_team_ids)))
                elif game_message.round > 20:
                    actions.append(SendReinforcementsAction(EnemyType.LVL8, random.choice(other_team_ids)))
                else:
                    actions.append(self.random_attack(game_message, random.choice(other_team_ids)))
        elif 0.1 < rand < 0.45:
            for coins_par_path in self.corners:
                for coin in coins_par_path:
                    if game_message.playAreas[game_message.teamId].get_tile_at(Position(*coin)) is None:
                        actions.append(BuildAction(TowerType.SPIKE_SHOOTER, Position(*coin)))
                        break
            if not actions:
                if self.get_empty_tiles(game_message):
                    actions.append(BuildAction(TowerType.SPEAR_SHOOTER, self.get_position_for_spear(game_message)))
        else:
            #actions.append(BuildAction(TowerType.SPEAR_SHOOTER, random.choice(self.get_empty_tiles(game_message))))
            if self.get_empty_tiles(game_message):
                actions.append(BuildAction(TowerType.SPEAR_SHOOTER, self.get_position_for_spear(game_message)))

        return actions

    def get_path_sides(self, game_message: GameMessage) -> List[List[Position]]:
        w, h = game_message.map.width, game_message.map.height

        sides_per_path = []

        for path in game_message.map.paths:
            sides = []
            for tile in path.tiles:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if game_message.playAreas[game_message.teamId].is_empty(Position(tile.x+i, tile.y+j)):
                            sides.append(Position(tile.x+i, tile.y+j))
            sides_per_path.append(sides)
        
        return sides_per_path

    def get_path_corners(self, game_message: GameMessage):
        corners = []
        chemins = []
        
        for path in game_message.map.paths:
            chemins.append(path.tiles)
        
        for chemin in chemins:
            coins = []
            direction = (chemin[1].x - chemin[0].x, chemin[1].y - chemin[0].y)
            
            for i in range(len(chemin)-1):
                new_direction = (chemin[i + 1].x - chemin[i].x, chemin[i + 1].y - chemin[i].y)
                if new_direction != direction:
                    coins.append((chemin[i - 1].x + new_direction[0], chemin[i - 1].y + new_direction[1]))
                    x, y = chemin[i - 1].x + new_direction[0], chemin[i - 1].y + new_direction[1]
                    if game_message.playAreas[game_message.teamId].is_empty(Position(x, y)):
                        coins.append((chemin[i - 1].x + new_direction[0], chemin[i - 1].y + new_direction[1]))
                    direction = new_direction
            
            corners.append(coins)
        
        return corners
    
    def random_attack(self, game_message: GameMessage, team_id):
        attack = choice(list(game_message.shop.reinforcements.keys()))
        return SendReinforcementsAction(attack, team_id)
    
    def get_empty_tiles(self, game_message: GameMessage) -> List[Position]:
        w, h = game_message.map.width, game_message.map.height

        empty_tiles = []

        for i in range(w):
            for j in range(h):
                if game_message.playAreas[game_message.teamId].get_tile_at(Position(i, j)) is None:
                    empty_tiles.append(Position(i, j))
        
        return empty_tiles

    def get_position_for_spear(self, game_message):
        
        empty_tiles = self.get_empty_tiles(game_message)

        def rank_tile(tile):
            c = 0
            for i in range(-2, 3):
                for j in range(-2, 3):
                    t = game_message.playAreas[game_message.teamId].get_tile_at(Position(tile.x+i, tile.y+j))
                    if Position(tile.x+i, tile.y+j) in self.spawns or Position(tile.x+i, tile.y+j) in self.gates:
                        c +=2
                    elif t is not None and t.paths:
                        c += 1
            return c

        empty_tiles.sort(key=rank_tile)

        return random.choice(empty_tiles[-int(len(empty_tiles)/3):])
