from Player import player

class game:
    def __init__(self, num_players, num_flips):
        """Parameters:
        num_players (int): The number of players in the game
        num_flips (int): The number of coin flips each player will perform

        Members:
        num_players (int): The total number of players in the game
        num_flips (int): The number of flips each player will perform
        players (list): A list of player objects participating in the game
        cheaters (list): A list of player objects that are cheaters
        """
        self.num_players = num_players
        self.num_flips = num_flips

        self.players = [player(f'Player {i+1}') for i in range(num_players)]
        self.num_cheaters = len([p for p in self.players if p.cheater])
    

    def play(self):
        """Simulates the game by flipping coins for each player"""
        for _ in range(self.num_flips):
            for p in self.players:
                p.flip()

    