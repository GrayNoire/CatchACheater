from Game import game
from Player import player

from scipy.stats import binom, norm
import matplotlib.pyplot as plt
from math import sqrt, ceil

# Set global defaults
plt.rcParams['figure.facecolor'] = '#222831'  # Dark gray for figure
plt.rcParams['axes.facecolor'] = '#393e46'    # Lighter gray for axes
plt.rcParams['savefig.facecolor'] = '#222831' # Ensures saved images match   

class hypoTest:
    def __init__(self, p_cheater: float, p_fair: float):
        """
        Parameters:
            p_cheater (float): The proportion of cheaters that are caught
            p_fair (float): The proportion of fair players we allow to be misclassified
        """

        self.p = player.CHEATER_EDGE
        self.p_cheater = p_cheater
        self.p_fair = p_fair

        # Use standard normal distribution to find n
        # Then n = [(z_alpha + 2z_beta*sqrt(p(1-p))) / (2p - 1)]^2

        z_alpha = norm.ppf(1-p_fair)
        z_beta = norm.ppf(p_cheater)
        print(f"z_alpha: {z_alpha}, z_beta: {z_beta}")

        self.n = int(((z_alpha + 2 * z_beta * (self.p * (1-self.p))**0.5) / (2 * self.p - 1))**2 + 1)
        print(f"Calculated number of flips needed: {self.n}")

        g: game = game(10, self.n)

    def find_threshold(self):
        z_alpha = norm.ppf(1-self.p_fair)
        z_beta = norm.ppf(self.p_cheater)

        k1 = sqrt(self.n)/2 * z_alpha + self.n/2
        k2 = self.n * self.p - sqrt(self.n * self.p * (1-self.p)) * z_beta
        thresh = ceil(max(k1, k2))

        x = range(self.n+1)
        yf = binom.pmf(x, self.n, 0.5)
        yc = binom.pmf(x, self.n, self.p)

        false_positive_rate = sum(yf[thresh:])
        false_negative_rate = sum(yc[:thresh])

        while false_positive_rate > self.p_fair or false_negative_rate > self.p_cheater:
            thresh += 1
            false_positive_rate = sum(yf[thresh:])
            false_negative_rate = sum(yc[:thresh])
        
        print(f"Final threshold k: {thresh}")

    
    def visualize_test(self, p: float, thresh: int = None):
        # flips: int = self.n
        flips = 1000
        x = range(flips+1)
        yf = binom.pmf(x, flips, 0.5)
        yc = binom.pmf(x, flips, p)

        # thresh = self.find_threshold()

        plt.suptitle(f'Hypothesis Test (p_cheater={self.p_cheater}, p_fair={self.p_fair})', color='white', fontsize=16)

        # Fair player distribution
        plt.subplot(2, 1, 1)
        plt.bar(x, yf)
        plt.ylabel('Probability', color='white')
        plt.tick_params(axis='both', colors='white')

        # Cheater distribution
        plt.subplot(2, 1, 2)
        plt.bar(x, yc, color='red')
        plt.xlabel('Number of heads', color='white')
        plt.ylabel('Probability', color='white')
        plt.tick_params(axis='both', colors='white')

        # Add vertical line for threshold
        if thresh is not None and 0 <= thresh <= flips:
            plt.axvline(x=thresh-0.5, color='white', linestyle='--')
            plt.subplot(2, 1, 1)
            plt.axvline(x=thresh-0.5, color='white', linestyle='--')

        # Display false positive and false negative rates
        if thresh is not None:
            false_positive_rate = sum(yf[thresh:])  # Fair players misclassified as cheaters
            false_negative_rate = sum(yc[:thresh])  # Cheaters misclassified as fair

            plt.subplot(2, 1, 1)
            plt.text(0.95, 0.95, f'False Positive Rate: {false_positive_rate:.2%}', 
                     transform=plt.gca().transAxes, ha='right', va='top', color='white')
            
            plt.subplot(2, 1, 2)
            plt.text(0.95, 0.95, f'False Negative Rate: {false_negative_rate:.2%}', 
                     transform=plt.gca().transAxes, ha='right', va='top', color='white')

        plt.show()

    def test_player(self, player: player, thresh: int):
        return player.score > thresh
        

    def test(self, game):
        cheaters = [p for p in game.players if p.cheater]
        fair_players = [p for p in game.players if not p.cheater]


h = hypoTest(0.90, 0.05)
h.visualize_test(0.60, 550)