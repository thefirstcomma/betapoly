import time

class Player:
    def __init__(self, string_symbol):
        self.position = 0
        self.property_in_use = []
        self.property_in_mort = []
        self.money = 1500
        self.total_equity = 1500
        self.in_jail = False
        self.rolled_double = False
        self.turns_in_jail = 0
        self.get_out_jail_card = 0
        self.symbol = string_symbol

    def get_symbol(self):
        return self.symbol

    def is_bankrupt(self):
        return self.total_equity < 0

    # Can return only 1 of 4 strings
    def get_out_jail_actions(self):
        s = input(f"Choose an Action for {self.symbol} between 1. PAY_50, 2. ROLL_DOUBLE, and 3. USE_JAIL_CARD\n>> ")
        return s

    def player_buys_property(self, board):
        return input(f"Does {self.symbol} buy the {board[self.position][3]} property named: " 
                            f"{board[self.position][2]} for ${board[self.position][1]} (Y/N)\n")

    def player_buys_railroad_utility(self, board):
        return input(f"Does {self.symbol} buy the property named: " 
                            f"{board[self.position][2]} for ${board[self.position][1]} (Y/N)\n")
    
    #  returns a List of actions
    def get_actions(self):
        all_actions = []
        return all_actions

    def mortgage_property(self, board, position):
        self.property_in_use.remove(position)
        self.property_in_mort.append(position)
        # FIXME This is questionable below ->
        self.update_money(self, board[position][3] // 2)

    def get_money(self):
        return self.money

    def update_money(self, value):
        if self.money + value < 0:
            print(self.symbol, " total money went negative! Shouldn't be able to buy!")
        self.money += value
        self.total_equity += value

    # def owns_property(self, board, property_index):
    #     assert(board[property_index][0] < 3)
    #     return property_index in self.property_in_use or property_index in self.property_in_mort