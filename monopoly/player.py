import time
import game

class Player:
    def __init__(self, string_symbol):
        self.position = 0
        self.property_in_use = []
        self.property_in_mort = []
        self.money = 1500
        self.total_equity = 1500
        self.in_jail = False
        self.get_out_jail_card = 0
        self.symbol = string_symbol

    def get_symbol(self):
        return self.symbol

    def is_bankrupt(self):
        return self.total_equity <= 0

    #  returns a List of actions
    def get_actions(self):
        all_actions = []
        return all_actions

    def mortgage_property(self, board, position):
        self.property_in_use.remove(position)
        self.property_in_mort.append(position)
        # This is questionable below ->
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