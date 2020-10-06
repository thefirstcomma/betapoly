import time
import math
from operator import add
from itertools import zip_longest
from gym_monopoly.game.board_info import board_info

class Player:
    def __init__(self, string_symbol):
        self.board = board_info.BOARD
        self.position = 0
        self.property_in_use = [] 
        self.property_in_mort = []
        self.money = 1500
        self.total_equity = 1500
        self.in_jail = False
        self.turns_in_jail = 0
        self.get_out_jail_card = 0
        self.symbol = string_symbol
        self.houses = [0]*40 # 1-5, 5 == hotel
        self.rolled_dice_this_turn = False

    def get_symbol(self):
        return self.symbol

    def is_bankrupt(self):
        return self.total_equity < 0

    # Can return only 1 of 4 strings
    def get_out_jail_actions(self):
        print(f'Get out of Jail Cards: {self.get_out_jail_card}\n')
        return input(f"{self.symbol} must 1.PAY_50, 2.ROLL_DOUBLE, or 3.USE_JAIL_CARD >>")

    def player_buys_property(self):
        action = ''
        while action != "y" and action != "n":
            action = input(f"Does {self.symbol} buy the {self.board[self.position][3]} property named: " 
            f"{self.board[self.position][2]} for ${self.board[self.position][1]} (Y/N) \n")
            action = action.lower().strip()
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

    def player_buys_railroad_utility(self):
        action = ''
        while action != "y" and action != "n":
            action = input(f"Does {self.symbol} buy the railroad/util named: " 
                        f"{self.board[self.position][2]} for ${self.board[self.position][1]} (Y/N) \n")
            action = action.lower().strip()
        return action
    
    def remove_non_housing_property(self, properties):
        if 5 in properties:
            properties.remove(5)
        if 15 in properties:
            properties.remove(15)
        if 25 in properties:
            properties.remove(25)
        if 35 in properties:
            properties.remove(35)
        if 12 in properties:
            properties.remove(12)
        if 28 in properties:
            properties.remove(28)
        return properties

    def check_property_index_for_houses(self, index):
        if index == 5 or index == 15 or index == 25 or index == 35:
            return False
        if index == 12 or index == 28:
            return False
        return True
    
    def is_monopoly(self, index):
        assert(self.board[index][0] == 0)
        prop = self.property_in_use + self.property_in_mort
        if self.board[index][3] == "Brown":
            if 1 in prop and 3 in prop:
                return True
        elif self.board[index][3] == "Lt.Blue":
            if 6 in prop and 8 in prop and 9 in prop:
                return True
        elif self.board[index][3] == "Pink":
            if 11 in prop and 13 in prop and 14 in prop:
                return True
        elif self.board[index][3] == "Orange":
            if 16 in prop and 18 in prop and 19 in prop:
                return True
        elif self.board[index][3] == "Red":
            if 21 in prop and 23 in prop and 24 in prop:
                return True
        elif self.board[index][3] == "Yellow":
            if 26 in prop and 27 in prop and 29 in prop:
                return True 
        elif self.board[index][3] == "Green":
            if 31 in prop and 32 in prop and 34 in prop:
                return True
        elif self.board[index][3] == "Blue":
            if 37 in prop and 39 in prop:
                return True
        return False

    def buy_numb_houses_is_good(self, index):
        assert(self.board[index][0] == 0)
        if self.board[index][3] == "Brown":
            if min(self.houses[1], self.houses[3]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Lt.Blue":
            if min(self.houses[6], self.houses[9], self.houses[8]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Pink":
            if min(self.houses[11], self.houses[13], self.houses[14]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Orange":
            if min(self.houses[16], self.houses[19], self.houses[18]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Red":
            if min(self.houses[21], self.houses[23], self.houses[24]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Yellow":
            if min(self.houses[26], self.houses[27], self.houses[29]) == self.houses[index]:
                return True 
        elif self.board[index][3] == "Green":
            if min(self.houses[31], self.houses[32], self.houses[34]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Blue":
            if min(self.houses[37], self.houses[39]) == self.houses[index]:
                return True
        return False

    def sell_numb_houses_is_good(self, index):
        assert(self.board[index][0] == 0)
        if self.board[index][3] == "Brown":
            if max(self.houses[1], self.houses[3]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Lt.Blue":
            if max(self.houses[6], self.houses[9], self.houses[8]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Pink":
            if max(self.houses[11], self.houses[13], self.houses[14]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Orange":
            if max(self.houses[16], self.houses[19], self.houses[18]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Red":
            if max(self.houses[21], self.houses[23], self.houses[24]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Yellow":
            if max(self.houses[26], self.houses[27], self.houses[29]) == self.houses[index]:
                return True 
        elif self.board[index][3] == "Green":
            if max(self.houses[31], self.houses[32], self.houses[34]) == self.houses[index]:
                return True
        elif self.board[index][3] == "Blue":
            if max(self.houses[37], self.houses[39]) == self.houses[index]:
                return True
        return False
    
    def has_no_property(self):
        return not (self.property_in_mort + self.property_in_use)
    
    def get_actions(self, players, sum_die, rolled_double):
        action = []
        response = input("6 commands: (M)ortgage, (U)nmortgage, (T)rade, (B)uy Houses, (S)ell Houses: ")
        action.append(response.upper().strip())
        if response == 'M' and not self.has_no_property():
            for i in self.property_in_use:
                print(f"{self.board[i][2]} [{i}]")
            get_index = input("What index property do you want to mortgage : ")
            action.append(get_index)
        elif response == 'U' and not self.has_no_property():
            for i in self.property_in_mort:
                print(f"{self.board[i][2]} [{i}]")
            get_index = input("What index property do you want to unmortgage : ")
            action.append(get_index)
        elif response == 'T':
            get_player = input("What player are you trading with (P#) ")
            other_player = '(P' + get_player + ')'
            trade_player = ":)"
            for player in players:
                if player.symbol == other_player.upper():
                    trade_player = player
                    action.append(trade_player)
                    break
            print("Opponent: ", trade_player.symbol, " regular properties:")
            for prop in trade_player.property_in_use:
                print(f'  -{self.board[prop][2]} [{prop}]')
            print("Opponent: ", trade_player.symbol, " mortgaged properties:")
            for prop in trade_player.property_in_mort:
                print(f'  -{self.board[prop][2]} [{prop}]')
            property_offer = input("\nWhat property(s) do you want from " + trade_player.symbol +  
                                    " - type ENTER for none: ")
            property_offer = property_offer.split(' ')
            # property_offer = list(map(int, property_offer)) 
            print(self.symbol, " regular properties: ")
            for prop in self.property_in_use:
                print(f'  -{self.board[prop][2]} [{prop}]')
            print(self.symbol, " mortgaged properties: ")
            for prop in self.property_in_mort:
                print(f'  -{self.board[prop][2]} [{prop}]')
            property_desire = input("\nWhat property(s) are you offering?: type ENTER for none: ")
            property_desire = property_desire.split(' ')
            # property_desire = list(map(int, property_desire)) 
            print(f'\nYour money: {self.money}')
            print(f'Their money: {trade_player.money}\n')
            my_money = input("How much money are you offering " + trade_player.symbol +  
                                " - type ENTER or 0 for none: $")
            your_money = input("How much money is " + trade_player.symbol +  
                                "offering you? - type ENTER or 0 for none: $")
            action.append(property_offer)
            action.append(property_desire)
            action.append(my_money) 
            action.append(your_money)
        elif response == 'B' and not self.has_no_property():
            total_prop = self.property_in_mort + self.property_in_use
            total_prop = self.remove_non_housing_property(total_prop)
            for i in total_prop:
                print(f"{self.board[i][2]} [{i}] \t\t# houses: {self.houses[i]}")
            get_index = input("What property do you want to buy a house on? ")
            action.append(get_index)
        elif response == 'S' and not self.has_no_property():
            total_prop = self.property_in_mort + self.property_in_use
            total_prop = self.remove_non_housing_property(total_prop)
            for i in total_prop:
                print(f"{self.board[i][2]} [{i}] \t\t# houses: {self.houses[i]}")
            get_index = input("What property do you want to sell a house on? ")
            action.append(get_index)
        else:
            print(f"No action was prompted or {self.symbol} has no property, can only (T)rade")
            return ["no_action"]
        return action

    #FIXME print values, should look cleaner
    def agree_disagree_trade(self, other_player, their_property, my_property, their_money, my_money):
        print("\nPlayer is Offering: ")
        for i in their_property:
            print(f'  -{self.board[i][2]} [{i}]')
        print("For your property of: ")
        for i in my_property:
            print(f'  -{self.board[i][2]} [{i}]')
        print("\nAND\n")
        print(f'{other_player.symbol} Offers: ${their_money} for your ${my_money}')
        action = input(f"Do you agree to the trade offered by {other_player.symbol}?"
                        f" Type 'agree' or 'disagree' ")
        return action.lower().strip()
    
    def print_houses(self):
        for i, e in enumerate(self.houses):
            if e > 0:
                print(f'{self.board[i][2]} [{i}] {e} houses')

    def buy_house(self, location_property, players):
        location_property = int(location_property)
        if self.houses[location_property] >= 5:
            print("Cannot buy more than a hotel!")
        elif not self.check_property_index_for_houses(location_property):
            print(f"Can't buy/sell houses on Railroad or Utility")
        elif not self.buy_numb_houses_is_good(location_property):
            print(f"Can't build multiple houses in a non-row fashion.")
        elif self.is_monopoly(location_property):
            print("This property is a monopoly! Buying!")
            self.houses[location_property] += 1
            self.update_money(-self.board[location_property][10], players)
            self.update_equity(-self.board[location_property][10] // 2)
        else:
            print("Not a monopoly property!")
        
    def sell_house(self, location_property, players):
        location_property = int(location_property)
        if self.houses[location_property] <= 0:
            print("Cannot sell 0 houses!")
        elif not self.check_property_index_for_houses(location_property):
            print(f"Can't buy/sell houses on Railroad or Utility")
        elif not self.sell_numb_houses_is_good(location_property):
            print(f"Can't sell multiple houses in a non-row fashion.")
        elif self.is_monopoly(location_property):
            self.houses[location_property] -= 1
            self.update_money(self.board[location_property][10]//2, players)
        else:
            print("YOU SHOULD NEVER EVER SEE THIS PRINT MESSAGE @(PLAYERS.SELL_HOUSE)")

    # FIXME - Cannot mortgage a property with houses on it.
    def mortgage_property(self, location_property, players):
        location_property = int(location_property)
        self.property_in_use.remove(location_property)
        self.property_in_mort.append(location_property)
        print(f"Mortgaged this property {self.board[location_property][2]} received: ${self.board[location_property][1] // 2} money")
        self.update_money(self.board[location_property][1]//2, players)

    # FIXME MUST DEAL WITH NEW_PLAYER_UNMORTGAGE == TRUE
    def unmortgage_property(self, location_property, players):
        location_property = int(location_property)
        self.property_in_use.append(location_property)
        self.property_in_mort.remove(location_property)
        ten_percent_interest = math.ceil((self.board[location_property][1] // 2) * .1)
        cost_plus_ten_percent_interest = (self.board[location_property][1] // 2) + ten_percent_interest
        self.update_money(-cost_plus_ten_percent_interest, players)
        self.update_equity(-ten_percent_interest)
    
    def might_pay_10_percent_extra_mortgaged_property(self, loc_property):
        print("Received a new mortgaged property from a player!")
        print("Unmortgage now (10%) or pay an xtra (10%) later!")
        print("Property named:", self.board[loc_property][2])
        prompt = input("Do you want to unmortgage this property right away. (y, n)")
        return prompt 
        
    def get_money(self):
        return self.money
    
    def update_money(self, value, players):
        while (self.money + value <= 0):
            print("\nYou don't have enough money!\n Must sell homes, mortgage, or trade property!")
            action = input()
            self.forced_get_money(players)
        self.money += value
    
    # This method is the ONLY METHOD that cheats by not calling update_money() and instead self.money*
    def forced_get_money(self, players):
        action = []
        response = input("3 commands: (M)ortgage, (T)rade, (S)ell Houses: ")
        action.append(response.upper().strip())
        if response == 'M' and not self.has_no_property():
            for i in self.property_in_use:
                print(f"{self.board[i][2]} [{i}]")
            get_index = input("What index property do you want to mortgage : ")
            action.append(get_index)
        elif response == 'T':
            get_player = input("What player are you trading with (P#) ")
            other_player = '(P' + get_player + ')'
            trade_player = ":)"
            for player in players:
                if player.symbol == other_player.upper():
                    trade_player = player
                    action.append(trade_player)
                    break
            print("Opponent: ", trade_player.symbol, " regular properties:")
            for prop in trade_player.property_in_use:
                print(f'  -{self.board[prop][2]} [{prop}]')
            print("Opponent: ", trade_player.symbol, " mortgaged properties:")
            for prop in trade_player.property_in_mort:
                print(f'  -{self.board[prop][2]} [{prop}]')
            property_offer = input("\nWhat property(s) do you want from " + trade_player.symbol +  
                                    " - type ENTER for none: ")
            property_offer = property_offer.split(' ')
            # property_offer = list(map(int, property_offer)) 
            print(self.symbol, " regular properties: ")
            for prop in self.property_in_use:
                print(f'  -{self.board[prop][2]} [{prop}]')
            print(self.symbol, " mortgaged properties: ")
            for prop in self.property_in_mort:
                print(f'  -{self.board[prop][2]} [{prop}]')
            property_desire = input("\nWhat property(s) are you offering?: type ENTER for none: ")
            property_desire = property_desire.split(' ')
            # property_desire = list(map(int, property_desire)) 
            print(f'\nYour money: {self.money}')
            print(f'Their money: {trade_player.money}\n')
            my_money = input("How much money are you offering " + trade_player.symbol +  
                                " - type ENTER or 0 for none: $")
            your_money = input("How much money is " + trade_player.symbol +  
                                "offering you? - type ENTER or 0 for none: $")
            action.append(property_offer)
            action.append(property_desire)
            action.append(my_money)
            action.append(your_money)
        elif response == 'S' and not self.has_no_property():
            total_prop = self.property_in_mort + self.property_in_use
            total_prop = self.remove_non_housing_property(total_prop)
            for i in total_prop:
                print(f"{self.board[i][2]} [{i}] \t\t# houses: {self.houses[i]}")
            get_index = input("What property do you want to sell a house on? ")
            action.append(get_index)
        else:
            print(f"No action was prompted or {self.symbol} has no property, can only (T)rade")
            return ["no_action"]
        return action
    
    def update_equity(self, value):
        self.total_equity += value