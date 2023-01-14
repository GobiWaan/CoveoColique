from game_message import *
from actions import *
from random import shuffle, choice
def Basic_strategy(game_message: GameMessage):
    pass



        
        


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.actions = []
        self.corners = []
        self.extended_corners =[]
    
    def att_corner(self, game_message):

        if not self.corners:
            self.corners = self.get_path_corners(game_message) 
            for i in self.corners:
                self.extended_corners += i
            shuffle(self.extended_corners)
            

        try:
            coin = self.extended_corners.pop(0)
            if game_message.playAreas[game_message.teamId].get_tile_at(Position(*coin)) is None:
                self.actions.append(BuildAction(TowerType.SPIKE_SHOOTER, Position(*coin)))
        except:
            pass



    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        other_team_ids = [team for team in game_message.teams if team != game_message.teamId]

        

        self.att_corner(game_message)


        return self.actions
    
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
                    direction = new_direction
            
            corners.append(coins)
        
        return corners
    
        
    def random_attack(self, game_message: GameMessage, team_id):
        attack = choice(game_message.shop.reinforcements.keys())
        self.actions.append(SendReinforcementsAction(attack, team_id))
