import time
import math

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
        self.total_houses = 0
        self.total_hotels = 0
        self.houses = [0] * 40

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

    def player_buys_railroad_utility(self, board):
        action = input(f"Does {self.symbol} buy the railroad/util named: " 
                    f"{board[self.position][2]} for ${board[self.position][1]} (Y/N)\n")
        if action == 'y' or action == 'Y':
            self.property_in_use.append(self.position)
        return action

    #  returns a List of actions
    def get_actions(self):
        all_actions = []
        return all_actions

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