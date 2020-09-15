import time
import game

class Player:
    position = 0
    property_in_use = []
    property_in_mort = []
    money = 1500
    total_equity = 1500
    in_jail = False
    get_out_jail_card = 0

    def __init__(self, string_symbol):
        self.symbol = string_symbol

    def get_symbol(self):
        return self.symbol

    def is_bankrupt(self):
        return self.total_equity <= 0

    #  returns a List of actions
    def actions(self):
        all_actions = []
        return all_actions

    def mortgage_property(self, board, pos):
        self.property_in_use.remove(pos)
        self.property_in_mort.append(pos)
        # This is questionable below ->
        update_money(self, board[pos][3] // 2)

    def get_money(self):
        return self.money

    def update_money(self, value):
        if self.money + value < 0:
            print("Bankruptcy")
        self.money += value
        self.total_equity += value

    def owns_property(self, board, property_index):
        assert(board[property_index][0] < 3)
        return property_index in self.property_in_use or property_index in self.property_in_mort