import random
import time
from player import *
from human_player import *

# Type 0 : Property (0, name, color, cost, rent, rent1H, rent2H, rent3H, rent4H, RentHotel, costBuilding)
# Type 1 : Free Parking, GO, jail (1)
# Type 2 : Chance (2)
# Type 3 : Community Chest (3)
# Type 4 : Railroad (4, name, price=200)
# Type 5 : Go to Jail (5)
# Type 6 : Taxes (6, Amount)
# Type 7 : Water Works or Electric Company (7, Amount)

BOARD = [
    # [0 - 9]
    (1, "GO"),
    (0, "Mediteranean Avenue", "Brown", 60, 2, 10, 30, 90, 160, 250, 50),
    (3, "Community Chest"),
    (0, "Baltic Avenue", "Brown", 60, 4, 20, 60, 180, 320, 450, 50),
    (6, "Income Tax", 200),
    (4, "Reading Railroad", 200),
    (0, "Oriental Avenue", "Lt.Blue", 100, 6, 30, 90, 270, 400, 550, 50),
    (2, "Chance"),
    (0, "Vermont Avenue", "Lt.Blue", 100, 8, 40, 100, 300, 450, 600, 50),
    (0, "Conneticut Avenue", "Lt.Blue", 120, 6, 30, 90, 270, 400, 550, 50),

    # [10 - 19]
    (1, "Jail"),
    (0, "St. Charles Places", "Pink", 140, 10, 50, 150, 450, 625, 750, 100),
    (7, "Electric Company", 150),
    (0, "States Avenue", "Pink", 140, 10, 50, 150, 450, 625, 750, 100),
    (0, "Virginia Avenue", "Pink", 160, 12, 60, 180, 500, 700, 900, 100),
    (4, "Pennysylvania Railroad", 200),
    (0, "St. James Place", "Orange", 180, 14, 70, 200, 550, 700, 900, 100),
    (3, "Community Chest"),
    (0, "Tenessee Avenue", "Orange", 180, 14, 70, 200, 550, 700, 950, 100),
    (0, "New York Avenue", "Orange", 200, 16, 80, 220, 600, 800, 1000, 100),

    # [20 - 29]
    (1, "Free Parking"),
    (0, "Kentucky Avenue", "Red", 220, 18, 90, 250, 700, 875, 1050, 150),
    (2, "Chance"),
    (0, "Indiana Avenue", "Red", 220, 18, 90, 250, 700, 875, 1050, 150),
    (0, "Illinois Avenue", "Red", 240, 20, 100, 300, 750, 925, 1100, 150),
    (4, "B. & O. Railroad", 200),
    (0, "Atlantic Avenue", "Yellow", 260, 22, 110, 330, 800, 975, 1150, 150),
    (0, "Ventnor Avenue",  "Yellow", 260, 22, 110, 330, 800, 975, 1150, 150),
    (7, "Water Works", 150),
    (0, "Marvin Gardens", "Yellow", 280, 24, 120, 360, 850, 1025, 1200, 150),

    # [30 - 39]
    (5, "Go To Jail"),
    (0, "Pacific Avenue", "Green", 300, 26, 130, 390, 900, 1100, 1275, 200),
    (0, "North Carolina Avenue", "Green", 300, 26, 130, 390, 900, 1100, 1275, 200),
    (3, "Community Chest"),
    (0, "Pennsylvania Avenue", "Green", 320, 28, 150, 450, 1000, 1200, 1400, 200),
    (4, "Short Line", 200),
    (2, "Chance"),
    (0, "Park Place", "Blue", 350, 35, 175, 500, 1100, 1300, 1500, 200),
    (6, "Luxury Tax", 100),
    (0, "Boardwalk", "Blue", 400, 50, 200, 600, 1400, 1700, 2000, 200),
]


# Type 0: Movement
# Type 1: Movement + Collect Bank Monetary
# Type 2: Bank Monetary
# Type 3: G.O.O.J
# Type 4: G.to.Jls

# Type 5: Birthday
# Type 6: Movement 

CHANCE = [
    
]

COMMUNITY_CHEST = [
    
]


class Game:

    def __init__(self):
        self.p1 = Player("[p1]")
        self.p2 = Player("[p2]")
        self.gametime = 0
        self.players = [self.p1, self.p2]

    def rollDice(self):
        return random.randint(1,6) + random.randint(1,6)
    
    def move_player(self, board, player, sum_die):
        player.position += sum_die
        if (player.position >= 40):
            player.position = player.position % 40
            player.money += 200
    
    def run(self):
        while(self.gametime < 20):
            sum_die = self.rollDice()
            current_player = ""
            if (self.gametime % 2 == 0):
                current_player = self.p1
            else:
                current_player = self.p2
            self.move_player(BOARD, current_player, sum_die)
            print(current_player.get_symbol() + " rolls a ", sum_die)
            self.print_board(self.players)
            self.gametime += 1
    
    def print_board(self, players):
        tmp = [ ["F.P.", "-", "-", "-", "-", "-", "-", "-", "-", "-", "G.T.J"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["-", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "-"],
                ["Jail", "-", "-", "-", "-", "-", "-", "-", "-", "-", "GO"]
        ]

        # For pretty print
        for player in players:
            number = player.position
            if number <= 10:
                if tmp[10][10 - number] == '-'
                    tmp[10][10 - number] = (player.get_symbol())
                else:
                    tmp[10][10 - number] += (player.get_symbol())
            elif number <= 20:
                tmp[10-(number % 10)][0] += (player.get_symbol())
            elif number <= 30:
                tmp[0][number % 10] += (player.get_symbol())
            elif number < 40:
                tmp[number % 10][10] += (player.get_symbol())
            else:
                print("Something really really went wrong!")
            
        
        for i,e in enumerate(tmp):
            print(e)
            
        print("\n")


if __name__ == "__main__":
    game = Game()

    ending = True
    game.run()

    # print("Outcome of Game: ", status)