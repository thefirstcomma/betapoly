import time
import math
from operator import add

class Player:
    def __init__(self, string_symbol):
        self.position = 0
        self.property_in_use = [] 
        self.property_in_mort = []
        self.money = 1500
        self.total_equity = 1500
        self.in_jail = False
        self.turns_in_jail = 0
        self.get_out_jail_card = 0
        self.symbol = string_symbol
        self.houses = [0] * 40 # 1-5, 5 == hotel

    def get_symbol(self):
        return self.symbol

    def is_bankrupt(self):
        return self.total_equity < 0

    # Can return only 1 of 4 strings
    def get_out_jail_actions(self):
        s = input(f"Choose an Action for {self.symbol} between 1. PAY_50, 2. ROLL_DOUBLE, and 3. USE_JAIL_CARD\n>> ")
        return s

    def player_buys_property(self, board):
        action = input(f"Does {self.symbol} buy the {board[self.position][3]} property named: " 
                    f"{board[self.position][2]} for ${board[self.position][1]} (Y/N)\n")
        
        if action == 'y' or action == 'Y':
            self.property_in_use.append(self.position)
        return action
    
    def get_houses_and_hotels(self):
        hotel = 0
        housing = 0
        for i in self.houses:
            if i == 5:
                hotel += 1
            else:
                housing += i
        return (housing, hotel)


    def player_buys_railroad_utility(self, board):
        action = input(f"Does {self.symbol} buy the railroad/util named: " 
                    f"{board[self.position][2]} for ${board[self.position][1]} (Y/N)\n")
        if action == 'y' or action == 'Y':
            self.property_in_use.append(self.position)
        return action

    #  returns a List of actions
    def get_actions(self, players, board, sum_die, rolled_double):
        action = []

        response = input("6 commands: Mortgage, UnMortgage, Trade, Buy Houses, Sell House, or (M, U, T, B, S, no_action)")
        action.append(response)
        if response == 'M':
            for i in self.property_in_use:
                print(f"{board[i][2], {i}}")
            get_index = input("What index property do you want to mortgage")
            action.append(get_index)
        elif response == 'U':
            for i in self.property_in_mort:
                print(f"{board[i][2], {i}}")
            get_index = input("What index property do you want to unmortgage")
            action.append(get_index)
        elif response == 'T':
            get_player = input("What player are you trading with <P#>")
            other_player = '(' + get_player + ')'
            trade_player = ":)"
            
            for player in players:
                if player.symbol == other_player.upper():
                    trade_player = player
                    action.append(trade_player)

            print(self.symbol, " unmortgaged properties:")
            for prop in trade_player.property_in_use:
                print(board[prop][2], "index: ", prop)
            print(self.symbol, "index: ", prop)
            for prop in trade_player.property_in_mort:
                print(board[prop][2], "(", prop, ")")
            property_offer = input("What properties do you want from" + trade_player.symbol + ": ")
            property_offer = property_offer.split(' ')
            # action = ["T", other_player, ["MY PROPERTY OFFER"], ["YOUR PROPERTY OFFER"], my_money, your_money]

            print("Opponent: ", trade_player.symbol, " unmortgaged properties:")
            for prop in self.property_in_use:
                print(board[prop][2])
            print("Opponent: ", trade_player.symbol, " mortgaged properties:")
            for prop in self.property_in_mort:
                print(board[prop][2])
            property_desire = input("What properties are you going to offer?: ")
            property_desire = property_desire.split(' ')

            my_money = input("How much money are you giving " + trade_player.symbol + " ?")
            your_money = input("How much money is " + trade_player.symbol + " giving you?")
            action.append(property_offer, property_desire, my_money, your_money)

        elif response == 'B':
            total_prop = self.property_in_mort + self.property_in_use
            for i in total_prop:
                print(board[i][2], "houses: ", self.houses[i])
            get_index = input("What property do you want to buy a house on?")
            action.append(get_index)
        elif response == 'S':
            for i in self.houses:
                if i > 0:
                    print(board[i][2], " has houses: ", self.houses[i])
            
            get_index = input("What property do you want to sell a house on?")
            action.append(get_index)
        else:
            print(f"No action was prompted by {self.symbol}!")
            action = []
            action.append("no_action")
            
        return action
    
    def agree_disagree_trade(self, trade_offer):
        return "agree"

    # FIXME - Cannot mortgage a property with houses on it.
    def mortgage_property(self, board, location_property):
        self.property_in_use.remove(location_property)
        self.property_in_mort.append(location_property)
        self.money += board[location_property][1] // 2

    def unmortgage_property(self, board, location_property, new_player_unmortgage):
        self.property_in_use.append(location_property)
        self.property_in_mort.remove(location_property)
        ten_percent_interest = math.ceil((board[location_property][1] // 2) * .1)
        cost_plus_ten_percent_interest = (board[location_property][1] // 2) + ten_percent_interest
        self.money -= cost_plus_ten_percent_interest
        self.total_equity -= ten_percent_interest
    
    def is_monopoly(self, board, index):
        assert(board[index][0] == 0)
        prop = self.property_in_use + self.property_in_mort
        if board[index][3] == "Brown":
            if 1 in prop and 3 in prop:
                return True
        elif board[index][3] == "Lt.Blue":
            if 6 in prop and 8 in prop and 9 in prop:
                return True
        elif board[index][3] == "Pink":
            if 11 in prop and 13 in prop and 14 in prop:
                return True
        elif board[index][3] == "Orange":
            if 16 in prop and 18 in prop and 19 in prop:
                return True
        elif board[index][3] == "Red":
            if 21 in prop and 23 in prop and 24 in prop:
                return True
        elif board[index][3] == "Yellow":
            if 26 in prop and 27 in prop and 29 in prop:
                return True 
        elif board[index][3] == "Green":
            if 31 in prop and 32 in prop and 34 in prop:
                return True
        elif board[index][3] == "Blue":
            if 37 in prop and 39 in prop:
                return True
        return False
        
    
    def get_money(self):
        return self.money

    def update_money(self, value):
        if self.money + value < 0:
            print(self.symbol, " total money went negative! Shouldn't be able to buy!")
        self.money += value
        self.total_equity += value