from game_message import *
from actions import *
import queue

def Basic_strategy(game_message: GameMessage):
    pass

def queu_filler(game_message ,list_of_corner: list) -> order:
    # list_of_corner : [[][]...[]]

    order = queue.Queue()
    lenght = [len(path) for path in list_of_corner]
    for i in range(0, max(lenght)):
        for path in list_of_corner:
            if game_message.playAreas[game_message.teamId].is_empty(path[i]):
                try:
                    order.put(path[i])
                except:
                    continue
            # else:
            #     try:
            #         order.put(path[i+1])
            #     except:
            #         continue
    return order

        
        

    #fill the queu with a corner from each path at a time
    pass

class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.corners = []

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        other_team_ids = [team for team in game_message.teams if team != game_message.teamId]
        actions = list()

        # if not self.corners:
        #     self.corners = self.get_path_corners(game_message)
        # actions.append()
        for path in game_message.map.paths:
            for tile in path.tiles:
                position_up = Position(tile.x, tile.y + 1)
                position_down = Position(tile.x, tile.y - 1)
                position_left = Position(tile.x - 1, tile.y) 
                position_right = Position(tile.x + 1, tile.y)
                if game_message.playAreas[game_message.teamId].is_empty(position_down):
                    actions.append(BuildAction(TowerType.SPIKE_SHOOTER, position_down))

                elif game_message.playAreas[game_message.teamId].is_empty(position_up):
                    actions.append(BuildAction(TowerType.SPIKE_SHOOTER, position_up))

                elif game_message.playAreas[game_message.teamId].is_empty(position_right):
                    actions.append(BuildAction(TowerType.SPIKE_SHOOTER, position_right))

                elif game_message.playAreas[game_message.teamId].is_empty(position_left):
                    actions.append(BuildAction(TowerType.SPIKE_SHOOTER, position_left))


        for coins_par_path in self.corners:
            for coin in coins_par_path:
                if game_message.playAreas[game_message.teamId].get_tile_at(Position(*coin)) is None:
                    actions.append(BuildAction(TowerType.SPIKE_SHOOTER, Position(*coin)))
                    break

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