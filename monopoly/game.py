import random
import time
from player import *
from human_player import *

# Type 0 : Property (0, name, color, cost, rent, rent1H, rent2H, rent3H, rent4H, RentHotel, costBuilding)
# Type 1 : Railroad
# Type 2 : Water Works or Electric Company
# Type 3 : Taxes
# Type 4  : Free Parking, GO, jail
# Type 5 : Go to Jail
# Type 6 : Community Chest
# Type 7 : Chance

BOARD = [
    # [0 - 9]
    (4, "GO"),
    (0, 60, "Mediteranean Avenue", "Brown", 2, 10, 30, 90, 160, 250, 50),
    (6, "Community Chest"),
    (0, 60, "Baltic Avenue", "Brown", 4, 20, 60, 180, 320, 450, 50),
    (3, 200, "Income Tax"),
    (1, 200, "Reading Railroad"),
    (0, 100, "Oriental Avenue", "Lt.Blue", 6, 30, 90, 270, 400, 550, 50),
    (7, "Chance"),
    (0, 100, "Vermont Avenue", "Lt.Blue", 8, 40, 100, 300, 450, 600, 50),
    (0, 120, "Conneticut Avenue", "Lt.Blue", 6, 30, 90, 270, 400, 550, 50),

    # [10 - 19]
    (4, "Jail"),
    (0, 140, "St. Charles Places", "Pink", 10, 50, 150, 450, 625, 750, 100),
    (2, 150, "Electric Company"),
    (0, 140, "States Avenue", "Pink", 10, 50, 150, 450, 625, 750, 100),
    (0, 160, "Virginia Avenue", "Pink", 12, 60, 180, 500, 700, 900, 100),
    (1, 200, "Pennysylvania Railroad"),
    (0, 180, "St. James Place", "Orange", 14, 70, 200, 550, 700, 900, 100),
    (6, "Community Chest"),
    (0, 180, "Tenessee Avenue", "Orange", 14, 70, 200, 550, 700, 950, 100),
    (0, 200, "New York Avenue", "Orange", 16, 80, 220, 600, 800, 1000, 100),
    
    # [20 - 29]
    (4, "Free Parking"),
    (0, 220, "Kentucky Avenue", "Red", 18, 90, 250, 700, 875, 1050, 150),
    (7, "Chance"),
    (0, 220, "Indiana Avenue", "Red", 18, 90, 250, 700, 875, 1050, 150),
    (0, 240, "Illinois Avenue", "Red", 20, 100, 300, 750, 925, 1100, 150),
    (1, 200, "B. & O. Railroad"),
    (0, 260, "Atlantic Avenue", "Yellow", 22, 110, 330, 800, 975, 1150, 150),
    (0, 260, "Ventnor Avenue",  "Yellow", 22, 110, 330, 800, 975, 1150, 150),
    (2, 150, "Water Works"),
    (0, 280, "Marvin Gardens", "Yellow", 24, 120, 360, 850, 1025, 1200, 150),

    # [30 - 39]
    (5, "Go To Jail"),
    (0, 300, "Pacific Avenue", "Green", 26, 130, 390, 900, 1100, 1275, 200),
    (0, 300, "North Carolina Avenue", "Green", 26, 130, 390, 900, 1100, 1275, 200),
    (6, "Community Chest"),
    (0, 320, "Pennsylvania Avenue", "Green", 28, 150, 450, 1000, 1200, 1400, 200),
    (1, 200, "Short Line"),
    (7, "Chance"),
    (0, 350, "Park Place", "Blue", 35, 175, 500, 1100, 1300, 1500, 200),
    (3, 100, "Luxury Tax"),
    (0, 400, "Boardwalk", "Blue", 50, 200, 600, 1400, 1700, 2000, 200),
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
        self.p1 = Player("[P1]")
        self.p2 = Player("[P2]")
        self.gametime = 0
        self.players = [self.p1, self.p2]
        # -1 == not buyable, 0 == buyable
        self.owner_list = [-1, 0, -1, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, -1, 0]

    def roll_dice(self):
        return random.randint(1,6) + random.randint(1,6)
    
    def move_player(self, player, sum_die):
        player.position += sum_die
        if (player.position >= 40):
            player.position = player.position % 40
            player.money += 200
    
    def run(self):
        while(not self.players[0].is_bankrupt() and not self.players[1].is_bankrupt()):
            sum_die = self.roll_dice()
            current_player = self.get_current_player()
            # check for mortgage and trades

            self.move_player(current_player, sum_die)
            print("\n\n", current_player.get_symbol() + " rolled: ", sum_die)
            self.print_board(self.players)

            # if player moved to board of type 0
            if BOARD[current_player.position][0] == 0:
                self.land_on_type0(current_player)
            # elif BOARD[current_player.position][0] == 1:
            #     self.land_on_type1(current_player)
            # elif BOARD[current_player.position][0] == 2:
            #     self.land_on_type2(current_player)
            # elif BOARD[current_player.position][0] == 3:
            #     self.land_on_type3(current_player)
            # elif BOARD[current_player.position][0] == 4:
            #     self.land_on_type4(current_player)
            # elif BOARD[current_player.position][0] == 5:
            #     self.land_on_type5(current_player)
            # elif BOARD[current_player.position][0] == 6:
            #     self.land_on_type6(current_player)
            # elif BOARD[current_player.position][0] == 7:
            #     self.land_on_type7(current_player)
            else:
                print("Something went went wrong with our types\n")
                
            for player in self.players:
                print(player.symbol,  " money: ", player.get_money())
            print("\n")

            for i,e in enumerate(self.owner_list):
                if e is not 0 and e is not -1:
                    print("Location ", i, " owned by", e.symbol)
        
            self.gametime += 1
    

    # Auctions, Houses/Hotels
    #FIX ME!!!!!!! LOTS OF CHANGES NEEDED
    def land_on_type0(self, current_player):
        # curr_property_owner = self.property_owner(self.players, current_player.position)
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == 0:
            action = input("Does " + current_player.symbol + " buy the " + BOARD[current_player.position][3] + " property named: " + BOARD[current_player.position][2] + " (Y/N)\n")
            assert(action == "Y" or action == "N")
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-BOARD[current_player.position][1])
                self.owner_list[current_player.position] = current_player
                print(current_player.symbol, " s MONEY NOW: ", current_player.money)
                print(current_player.symbol, " bought the ", BOARD[current_player.position][3] , " property named: ", BOARD[current_player.position][2])
            else:
                # auctions
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
            current_player.update_money(-BOARD[current_player.position][4])
            curr_property_owner.update_money(BOARD[current_player.position][4])
            print(current_player.symbol, " paid rent of ", BOARD[current_player.position][4], " to ", curr_property_owner.symbol)
    
    def land_on_type1(self, current_player):
        curr_property_owner = self.property_owner(self.players, current_player.position)
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == "UNOWNED PROPERTY":
            action = input("Does " + current_player.symbol + " buy the " + BOARD[current_player.position][3] + " property named: " + BOARD[current_player.position][2] + " (Y/N)\n")
            assert(action == "Y" or action == "N")
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-BOARD[current_player.position][1])
                print(current_player.symbol, " s MONEY NOW: ", current_player.money)
                print(current_player.symbol, " bought the ", BOARD[current_player.position][3] , " property named: ", BOARD[current_player.position][2])
            else:
                # auctions
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
            current_player.update_money(-BOARD[current_player.position][4])
            curr_property_owner.update_money(BOARD[current_player.position][4])
            print(current_player.symbol, " paid rent of ", BOARD[current_player.position][4], " to ", curr_property_owner.symbol)

    def land_on_type2(self, current_player):
        pass

    def land_on_type3(self, current_player):
        pass

    def land_on_type4(self, current_player):
        pass

    def land_on_type5(self, current_player):
        pass
    
    def land_on_type6(self, current_player):
        pass

    def land_on_type7(self, current_player):
        pass

    def auction_phase(self):
        pass

    # Only works for 2 players right now
    def get_current_player(self):
        return self.p1 if self.gametime % 2 == 0 else self.p2

    def property_owner(self, players, property_index):
        for player in players:
            if player.owns_property(BOARD, property_index):
                return player
        return "UNOWNED PROPERTY"
            
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
                if tmp[10][10 - number] == '-':
                    tmp[10][10 - number] = ''
                tmp[10][10 - number] += (player.get_symbol())
            elif number <= 20:
                if tmp[10-(number % 10)][0] == '-':
                    tmp[10-(number % 10)][0] = ''
                tmp[10-(number % 10)][0] += (player.get_symbol())
            elif number <= 30:
                if tmp[0][number % 10] == '-':
                    tmp[0][number % 10] = ''
                tmp[0][number % 10] += (player.get_symbol())
            elif number < 40:
                if tmp[number % 10][10] == '-':
                    tmp[number % 10][10] = ''
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