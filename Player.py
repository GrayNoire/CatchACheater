import random

class player:
    CHEATER_PROPORTION = 0.5
    CHEATER_EDGE = 0.75

    def __init__(self, name):
        """Parameters:
        name (str): The name of the player
        
        Members:
        name (str): Take a wild guess
        score (int): The player's current score, initialized to 0
        cheater (bool): Whether the player is a cheater, determined by a global variable CHEATER_PROPORTION
        """
        self.name = name
        self.score = 0
        self.cheater = random.random() < self.CHEATER_PROPORTION

    def new_player(name, is_cheater=False) -> player:
        p = player(name)
        p.cheater = is_cheater
        return p

    def __str__(self):
        return f"Player(name={self.name}, score={self.score}, cheater={self.cheater})"
    
    def __repr__(self):
        return self.__str__()
    
    def flip(self):
        r = random.random()

        if self.cheater and r < self.CHEATER_EDGE:
            self.score += 1

        else:
            self.score += 1 if r < 0.5 else 0