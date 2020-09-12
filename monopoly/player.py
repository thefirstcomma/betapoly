import time
import game

# Turn 1:
#     actions() -> [List]
#     rolldie()
#         -buy_property_landed_on()
#             -possible_auction()
#             -actions() -> [List]
#         -possible_pay_rent()
        
#         actions() -> [List]


class Player:
    position = 0
    property_in_use = []
    property_in_mort = []
    money = 1500
    possible_money = 0
    in_jail = False
    get_out_jail = 0

    def __init__(self, string_symbol):
        self.symbol = string_symbol

    def get_symbol(self):
        return self.symbol

    #  returns a List of actions
    def actions(self):
        all_actions = []
        return all_actions
    
    def trade_property(self, board, players):
        None
    
    def agree_to_trade(self, proposal):
        None
    
    def buy_property(self, pos):
        None

    def mortgage_property(self, board, pos):
        self.property_in_use.remove(pos)
        self.property_in_mort.append(pos)
        # This is questionable below ->
        updateMoney(self, board[pos][3] // 2)
    
    def unmortgage_proprty(self):
        None
    
    def buy_houses(self):
        None
    
    def sell_houses(self):
        None

    def getMoney(self):
        return self.money

    def updateMoney(self, value):
        self.money += value

    def chance_card(self):
        None
    
    def community_card(self):
        None