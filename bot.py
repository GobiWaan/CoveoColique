from game_message import *
from actions import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        other_team_ids = [team for team in game_message.teams if team != game_message.teamId]
        actions = list()

        actions.append(SellAction(Position(0, 0)))
        actions.append(BuildAction(TowerType.SPEAR_SHOOTER, Position(0, 0)))

        if other_team_ids:
            actions.append(SendReinforcementsAction(EnemyType.LVL1, other_team_ids[0]))

        return actions
    
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