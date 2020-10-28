import random
import time
import math
from colorama import Fore, Style
from gym_monopoly.game.player import Player
from gym_monopoly.game.board_info import BOARD, CHANCE, COMMUNITY_CHEST

# An Example Turn:
#     actions() -> [List]
#     rolldie()
#         -buy_property_landed_on()
#             -possible_auction()
#                -actions() -> [List]
#         -possible_pay_rent()
#     actions() -> [List]

# FIXME
# Have at max 2 G.o.o.J Cards
# Need to update Income tax to be possible 10% worth vs $200.00 (in type3)
# Auction for housing, limit housing=32, hotels=12, -- everytime someone buys/sells houses, iterate player actions.
# Auction bug, when everybody types 'n'
# Player number limit when trading, can't trade with yourself!
# Work on bankruptcy


class Game:
    def __init__(self):
        self.WON_MONOPOLY = None
        self.board = BOARD
        self.chance_cards = []
        self.comm_cards = []
        self.turns = 1
        p1 = Player(1)
        p2 = Player(2)
        p3 = Player(3)
        p4 = Player(4)
        self.players = [p1, p2, p3, p4]
        self.total_houses = 32
        self.total_hotels = 12
        self.current_player = self.players[0]
        self.in_auction = False
        self.player_before_auction_state = None
        self.highest_bid = 0
        self.player_with_highest_bid = None
        self.other_auction_players = self.players.copy()
        self.rolled_double = False
        self.trade_list = []

    def roll_dice(self):
        first_roll = random.randint(1,6)
        second_roll = random.randint(1,6)
        return (first_roll + second_roll, first_roll == second_roll)

    def get_current_player(self):
        return self.current_player
    
    def move_player(self, player, sum_die):
        player.position += sum_die
        if player.position >= 40:
            player.position = player.position % 40
            print(player.symbol, "passed GO, collect $200")
            player.update_money(200)
            player.update_equity(200)

    def move_cuz_card(self, player, future_location):
        if player.position > future_location:
            player.update_money(200)
            player.update_equity(200)
        player.position = future_location

    def pay_rent_if_owned(self, current_player, sum_die):
        curr_property_owner = None
        for player in self.players:
            player_full_property_list = player.property_in_use + player.property_in_mort
            if current_player.position in player_full_property_list:
                curr_property_owner = player

        if curr_property_owner == current_player:
            print(f"Landed on property you {current_player.symbol} already owns.")
            return True
        elif curr_property_owner == None:
            print(f"Landed on property nobody owns. Do you buy or auction the property?")
            print(f"\n{self.board[current_player.position][2]} [{current_player.position}]")
            current_player.must_buy_or_auction = True
            return False
        else:
            loc = current_player.position
            if self.board[loc][0] == 0:
                self.rent_on_type0(current_player, curr_property_owner)
            elif self.board[loc][0] == 1:
                self.rent_on_type1(current_player, curr_property_owner)
            elif self.board[current_player.position][0] == 2:
                self.rent_on_type2(current_player, curr_property_owner, sum_die)
            return True

    def rent_on_type0(self, current_player, curr_property_owner):
        loc = current_player.position
        if loc not in curr_property_owner.property_in_mort:
            if curr_property_owner.is_monopoly(loc): 
                numb_houses = curr_property_owner.houses[loc]
                if numb_houses > 0:
                    amount = self.board[current_player.position][4+numb_houses]
                    current_player.update_money(-amount)
                    current_player.update_equity(-amount)
                    curr_property_owner.update_money(amount)
                    curr_property_owner.update_equity(amount)
                    print(f"Paid extra because this property has {numb_houses} houses")
                    print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
                else:
                    amount = self.board[current_player.position][4]*2
                    current_player.update_money(-amount)
                    current_player.update_equity(-amount)
                    curr_property_owner.update_money(amount)
                    current_player.update_equity(amount)
                    print(f"Paid extra because this property is a monopoly w/o houses")
                    print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
            else:
                amount = self.board[current_player.position][4]
                current_player.update_money(-amount)
                current_player.update_equity(-amount)
                curr_property_owner.update_money(amount)
                curr_property_owner.update_equity(amount)
                print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
        else:
            print(f"{current_player.symbol} Landed on Mortgaged property, No payments YAY!!!")
    
    def rent_on_type1(self, current_player, curr_property_owner):
        loc = current_player.position
        if loc not in curr_property_owner.property_in_mort:
            total_amount = 0
            if 5 in curr_property_owner.property_in_use or 5 in curr_property_owner.property_in_mort:
                total_amount += 1
            if 15 in curr_property_owner.property_in_use or 15 in curr_property_owner.property_in_mort:
                total_amount += 1
            if 25 in curr_property_owner.property_in_use or 25 in curr_property_owner.property_in_mort:
                total_amount += 1
            if 35 in curr_property_owner.property_in_use or 35 in curr_property_owner.property_in_mort:
                total_amount += 1

            if total_amount == 4:
                total_amount = 8
            elif total_amount == 3:
                total_amount = 4
            current_player.update_money(-25*total_amount)
            current_player.update_equity(-25*total_amount)
            curr_property_owner.update_money(25*total_amount)
            curr_property_owner.update_equity(25*total_amount)
            print(f"{current_player.symbol} paid rent of ${25*total_amount} to {curr_property_owner.symbol}")
        else:
            print("Laned on mortgaged Railroad, No rent here!")
    
    def rent_on_type2(self, current_player, curr_property_owner, die_roll):
        loc = current_player.position
        if loc not in curr_property_owner.property_in_mort:
            total_amount, amount = 0, 0
            owner_list = curr_property_owner.property_in_mort + curr_property_owner.property_in_use
            if 12 in owner_list:
                total_amount += 1
            if 28 in owner_list:
                total_amount += 1
            if total_amount == 2:
                amount = die_roll*10
            elif total_amount == 1:
                amount = die_roll*4
            else:
                print(f"YOU SHOULD NOT SEE THIS ERROR MESSAGE (TYPE2)")
            
            print("1 or 2", total_amount)
            print("Amount owed for rent:", amount)
            current_player.update_money(-amount)
            current_player.update_equity(-amount)
            curr_property_owner.update_money(amount)
            curr_property_owner.update_equity(amount)
            print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
        else:
            print("Laned on mortgaged Utility, No rent here!")

    def land_on_type3(self, current_player):
        tax_amount = self.board[current_player.position][1]
        current_player.update_money(-tax_amount)
        current_player.update_equity(-tax_amount)
        print(f"{current_player.symbol} landed on TAXES. Has to pay ${tax_amount}")
        print(f"{current_player.symbol} Current Money Now: ${current_player.money}\n")

    def land_on_type5(self, current_player):
        # Go to Jail
        current_player.position = 10
        current_player.in_jail = True
        current_player.turns_in_jail = 0
    
    def land_on_type6(self, current_player, die_roll):
        if len(self.comm_cards) == 0:
            self.comm_cards = COMMUNITY_CHEST.copy()
            random.shuffle(self.comm_cards)

        card = (self.comm_cards.pop())
        print(f"\tLanded on Community Chest!! {card[1]}")

        if card[0] == 0:
            current_player.update_money(card[3])
            current_player.update_equity(card[3])
            if card[2] != -1:
                print(f"Moved to a new spot: {card[2]}")
                self.move_cuz_card(current_player, card[2])
                self.check_landed_on_type(current_player, die_roll)
        elif card[0] == 1:
            current_player.get_out_jail_card += 1
            print(f"{current_player.symbol} received a get out of Jail Card!")
        elif card[0] == 2:
            print(current_player.symbol, "goes to Jail")
            self.land_on_type5(current_player)
        elif card[0] == 3:
            print(f"{current_player.symbol} COLLECTS $$$ from every player.")
            for player in self.players:
                if current_player != player:
                    current_player.update_money(card[3])
                    current_player.update_equity(card[3])
                    player.update_money(-card[3])
                    player.update_equity(-card[3])
                    print(f"{current_player.symbol} collected ${card[3]} from {player.symbol}")
        elif card[0] == 4:
            houses, hotels = current_player.get_houses_and_hotels()
            print(f"Pay for each house: {houses} and hotel: {hotels}")
            current_player.update_money(houses * card[2])
            current_player.update_equity(houses * card[2])
            current_player.update_money(hotels * card[3])
            current_player.update_equity(hotels * card[3])
            print(f"{current_player.symbol} money updated {current_player.money}")
    
    def land_on_type7(self, current_player, die_roll):
        if len(self.chance_cards) == 0:
            self.chance_cards = CHANCE.copy()
            random.shuffle(self.chance_cards)

        card = (self.chance_cards.pop())
        print(f"Landed on Chance, {card[1]}")

        if card[0] == 0:
            current_player.update_money(card[3])
            current_player.update_equity(card[3])
            if card[2] != -1:
                print(f"Moved to new spot: {card[2]}")
                self.move_cuz_card(current_player, card[2])
                self.check_landed_on_type(current_player, die_roll)
        elif card[0] == 1:
            current_player.get_out_jail_card += 1
            print(f"{current_player.symbol} received a get out of Jail Card!")
        elif card[0] == 2:
            print(current_player.symbol, "goes to Jail")
            self.land_on_type5(current_player)
        elif card[0] == 3:
            print(f"{current_player.symbol} PAYS $$$ to every player.")
            for player in self.players:
                if current_player != player:
                    current_player.update_money(card[3])
                    current_player.update_equity(card[3])
                    player.update_money(-card[3])
                    player.update_equity(-card[3])
                    print(f"{current_player.symbol} paid {player.symbol} ${card[3]}")
        elif card[0] == 4:
            houses, hotels = current_player.get_houses_and_hotels()
            print(f"Pay for each house: {houses} and hotel: {hotels}")
            current_player.update_money(houses * card[2])
            current_player.update_equity(houses * card[2])
            current_player.update_money(hotels * card[3])
            current_player.update_equity(hotels * card[3])
            print(f"{current_player.symbol} money updated {current_player.money}")
        elif card[0] == 5:
            if card[2] == "util":
                if current_player.position > 28:
                    current_player.position = 12
                    print("Passed GO, collect 200")
                    current_player.update_money(200)
                    current_player.update_equity(200)
                elif current_player.position > 12:
                    current_player.position = 28
                elif current_player.position < 12:
                    current_player.position = 12
                self.land_on_type2(current_player, die_roll)
            elif card[2] == "railroad":
                if current_player.position > 35:
                    current_player.position = 5
                    current_player.update_money(200)
                    current_player.update_equity(200)
                elif current_player.position > 25:
                    current_player.position = 35
                elif current_player.position > 15:
                    current_player.position = 25
                elif current_player.position > 5:
                    current_player.position = 15
                self.land_on_type1(current_player)
            elif card[2] == "three":
                current_player.position -= 3
                self.check_landed_on_type(current_player, die_roll)

            
    def print_board(self):
        mini_board = [["F.P.", "-", "-", "-", "-", "-", "-", "-", "-", "-", "G.T.J"],
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
        for player in self.players:
            number = player.position
            if number <= 10:
                if mini_board[10][10 - number] == '-':
                    mini_board[10][10 - number] = ''
                mini_board[10][10 - number] += (player.get_symbol())
            elif number <= 19:
                if mini_board[10-(number % 10)][0] == '-':
                    mini_board[10-(number % 10)][0] = ''
                mini_board[10-(number % 10)][0] += (player.get_symbol())
            elif number <= 29:
                if mini_board[0][number % 10] == '-':
                    mini_board[0][number % 10] = ''
                mini_board[0][number % 10] += (player.get_symbol())
            elif number <= 39:
                if mini_board[number % 10][10] == '-':
                    mini_board[number % 10][10] = ''
                mini_board[number % 10][10] += (player.get_symbol())
            else:
                print("If you see this - Pretty Print is broken!\n")
        for i in mini_board:
            print(i)
        print("\n")

    def check_landed_on_type(self, current_player, sum_die):
        if self.board[current_player.position][0] == 0:
            self.pay_rent_if_owned(current_player, sum_die)
        elif self.board[current_player.position][0] == 1:
            self.pay_rent_if_owned(current_player, sum_die)
        elif self.board[current_player.position][0] == 2:
            self.pay_rent_if_owned(current_player, sum_die)
        elif self.board[current_player.position][0] == 3:
            self.land_on_type3(current_player)
        elif self.board[current_player.position][0] == 4:
            print(f"{current_player.symbol} Landed on | F.P.| GO | Jail-Visit |, Nothing happens!\n")
        elif self.board[current_player.position][0] == 5:
            self.land_on_type5(current_player)
        elif self.board[current_player.position][0] == 6:
            self.land_on_type6(current_player, sum_die)
        elif self.board[current_player.position][0] == 7:
            self.land_on_type7(current_player, sum_die)
        else:
            print("You should not see this print statement EVER!. @game/check_landed_on_type\n")
    
    def print_property_and_money(self):
        for player in self.players:
            print(f'{player.symbol} money: ${player.get_money()} - equity: ${player.total_equity}')

        for player in self.players:
            print(f"\n{player.symbol} Properties: ")
            tmp = sorted(player.property_in_use + player.property_in_mort)
            for i in tmp:
                if player.check_property_index_for_houses(i):
                    color = ''
                    if self.board[i][3] == 'Lt.Blue':
                        color = Fore.LIGHTCYAN_EX
                    elif self.board[i][3] == 'Brown':
                        pass
                    elif self.board[i][3] == 'Pink':
                        color = Fore.MAGENTA
                    elif self.board[i][3] == 'Orange':
                        pass
                    elif self.board[i][3] == 'Yellow':
                        color = Fore.YELLOW
                    elif self.board[i][3] == 'Red':
                        color = Fore.RED
                    elif self.board[i][3] == 'Green':
                        color = Fore.GREEN
                    elif self.board[i][3] == 'Blue':
                        color = Fore.BLUE

                    if i in player.property_in_mort:
                        print(color + f'{self.board[i][3]} - {self.board[i][2]} [{i}] - In Mortgage' + Style.RESET_ALL)
                    else:
                        print(color + f'{self.board[i][3]} - {self.board[i][2]} [{i}]' + Style.RESET_ALL)
                else:
                    if i in player.property_in_mort:
                        if i == 12 or i == 28:
                            print(f'Util: {self.board[i][2]} [{i}] - In Mortgage')
                        else:
                            print(f'Rail: {self.board[i][2]} [{i}] - In Mortgage')
                    else:
                        if i == 12 or i == 28:
                            print(f'Util: {self.board[i][2]} [{i}]')
                        else:
                            print(f'Rail: {self.board[i][2]} [{i}]')
            print()
        print("\n")
    
    def game_ended(self):
        if len(self.players) == 1:
            self.WON_MONOPOLY = self.players[0]
            return self.players
        else:
            return False





















     # indexes of the list of action {
    #     0 : Type For ACTION_LOOKUP
    #     1 : PAY 50 FOR JAIL (0)/ ROLL DOUBLE (1)/ USE G.O.O.J CARD (2)
    #     2 : DONT BUY / BUY INDEX PROPERTY LANDED ON   [0,1]
    #     3 : BUY HOUSE ON THIS INDEX
    #     4 : SELL HOUSE ON THIS INDEX
    #     5 : MORTGAGE ON THIS INDEX
    #     6 : UN-MORTGAGE ON THIS INDEX
    #     7 : TRADE WITH PLAYER NUMBER
    #     8 : TRADE MONEY YOU GIVE
    #     9 : TRADE MONEY YOU TAKE
    #     10 : AUCTION AMOUNT
    #     11 : ACCEPT_TRADE
    #     12-37: YOUR PROPERTY OFFERS
    #     38-63: ENEMY PROPERTY WANTS
    # }
                        

    def validate_action_list(self, action):
        # FIXME This shit is broken, david ur code keeps crashing holy shit holy shit fuck 
        # for act in action:
        #     if not isinstance(act, int):
        #         print("Is_instance error!")
        #         return False
        
        if action[0] < 0 or action[0] > 11:
            print(f"Error: action[0] = {action[0]}")
            return False
        if action[1] < 0 or action[1] > 2:
            print(f"Error: action[1] = {action[1]}")
            return False
        if action[2] < 0 or action[2] > 1:
            print(f"Error: action[2] = {action[2]}")
            return False
        if action[3] not in [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39]:
            print(f"Error: action[3] = {action[3]}")
            return False
        if action[4] not in [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39]:
            print(f"Error: action[4] = {action[4]}")
            return False
        if action[5] not in [1, 3, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 34, 35, 37, 39]:
            print(f"Error: action[5] = {action[5]}")
            return False
        if action[6] not in [1, 3, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 34, 35, 37, 39]:
            print(f"Error: action[6] = {action[6]}")
            return False
        if action[7] not in [1, 2, 3, 4]:
            print(f"Error: action[7] = {action[7]}")
            return False
        if action[8] < 0:
            print(f"Error: action[8] = {action[8]}")
            return False
        if action[9] < 0:
            print(f"Error: action[9] = {action[9]}")
            return False
        if action[10] < 0:
            print(f"Error: action[10] = {action[10]}")
            return False
        if action[11] not in [0, 1]:
            print(f"Error: action[11] = {action[11]}")
            return False
        for index_guy in range(12, 64):
            if action[index_guy] not in [0, 1]:
                print(f"Error: action[{index_guy}] = {action[index_guy]}")
                return False
        return True

    def validate_move(self, player, action):
        # FIXME bugged, can't roll the dice here
        if not self.validate_action_list(action):
            return False
        action_type = ACTION_LOOKUP[action[0]]
        
        if action_type == 'END' and not self.in_auction:
            if player.rolled_dice_this_turn and not player.must_buy_or_auction:
                return True
            else:
                print("Validation Failed!!!\nPlayer didn't roll the dice or is in a buy/auction state!\n")
                return False
        elif action_type == 'ROLL-DICE':
            if (not player.rolled_dice_this_turn and not player.in_jail and not self.in_auction):
                return True
            else:
                print("Already rolled this turn or In Jail or in an Auction!")
                return False
        elif action_type == 'BUY_PROPERTY_LANDED':
            if player.must_buy_or_auction == True and (action[2] == 1 or action[2] == 0) and not self.in_auction:
                return True
            else:
                print("Player cannot buy property or decide to auction in this moment!\n")
                return False
        elif action_type == 'IN_JAIL_ACTION':
            if action[1] == 2 and player.get_out_jail_card <= 0:
                print("Not enough get out of Jail Card")
                return False
            if player.in_jail and not player.rolled_dice_this_turn:
                return True
            else:
                print("Player not in Jail or player already rolled the dice!")
                return False
        elif action_type == 'BUY_HOUSE':
            return player.buyable(action[3])
        elif action_type == 'SELL_HOUSE':
            return player.sellable(action[4])
        elif action_type == 'CONTINUE_AUCTION':
            if action[10] <= player.money and self.in_auction:
                return True
            else:
                print("Player doesn't have enough money to auction OR the game is not in an auction phase!")
                return False
        elif action_type == 'MORTGAGE':
            curr_prop = action[5]
            return curr_prop in player.property_in_use
        elif action_type == "UNMORTGAGE":
            curr_prop = action[6]
            return curr_prop in player.property_in_mort
        elif action_type == "TRADE":
            trade_partner = action[7]
            if [p.player_number == trade_partner for p in self.players[0]] == player:
                 print("You cannot trade with yourself!")
                 return False
            
            
        elif action_type == 'ACCEPT_TRADE':
            pass
        else:
            print("Received Action that wasn't recognized!!!!")
            return False

    # action = [0, None, None, None, 1, None]
    # obs -> self.playerUs, go_again_next_turn, board_properties, player_turn
    def action_helper(self, action):
        player = self.get_current_player()
        action_type = ACTION_LOOKUP[action[0]]
        print(action_type)

        if not self.validate_move(player, action):
            print(f"Failed to do a Valid Move")
            # output punishable get_reward() here!
            return
        
        self.current_player = player

        if action_type == 'BUY_PROPERTY_LANDED':
            if action[2] == 1: # update money and equity
                player.update_money(-self.board[player.position][1])
                player.update_equity(-int(self.board[player.position][1]/2))
                player.property_in_use.append(player.position)
            elif action[2] == 0: # go to an auction
                print("Property goes to an auction!")
                self.in_auction = True
                self.player_before_auction_state = self.current_player
                copy_of_players = self.players.copy()
                random.shuffle(copy_of_players)
                self.current_player = copy_of_players.pop()
            player.must_buy_or_auction = False
        elif action_type == 'IN_JAIL_ACTION':
            if action[1] == 0: # roll-double
                sum_die, rolled_doubles = self.roll_dice()
                print("Chose to roll a double:")
                print("Dice Total:", sum_die, "Double status:", rolled_doubles)
                player.rolled_dice_this_turn = True
                if rolled_doubles:
                    self.move_player(player, sum_die)
                    self.check_landed_on_type(player, sum_die)
                    player.in_jail = False
                    player.turns_in_jail = 0
                else:
                    player.turns_in_jail += 1
                if player.turns_in_jail >= 3:
                    print("3 turns lasted in Jail without rolling a double!")
                    player.update_money(-50)
                    player.update_equity(-50)
                    self.move_player(player, sum_die)
                    self.check_landed_on_type(player, sum_die)
            elif action[1] == 1: # pay-50
                player.in_jail = False
                player.turns_in_jail = 0
                print("Player paid $50 to Get out of Jail early!")
                player.update_money(-50)
                player.update_equity(-50)
            elif action[1] == 2: # use g.o.o.j. card
                player.in_jail = False
                player.turns_in_jail = 0
                player.get_out_jail_card -= 1
                print("Player used a Get out of Jail Card!")
            else:
                print("Punish -1000 points. Wrong action type, out of range. Put in Wrong action.")
            
        elif action_type == 'CONTINUE_AUCTION':
            if action[10] > self.highest_bid:
                print("New highest Bidder!!")
                self.highest_bid = action[10]
                self.player_with_highest_bid = self.current_player
                self.other_auction_players = self.players.copy()
                self.other_auction_players.remove(self.player_with_highest_bid)
                random.shuffle(self.other_auction_players)
            else:
                print("Not enough money against the highest bid!")
                self.other_auction_players.remove(player)

            if not self.other_auction_players:
                prop_index = self.player_before_auction_state.position
                self.player_with_highest_bid.update_money(-self.highest_bid)
                self.player_with_highest_bid.update_equity(-self.highest_bid + int(self.board[prop_index][1]/2))
                self.player_with_highest_bid.property_in_use.append(prop_index)
                self.highest_bid = 0
                self.player_with_highest_bid = None
                self.other_auction_players = self.players.copy()
                self.current_player = self.player_before_auction_state
                self.player_before_auction_state = None
                self.in_auction = False
            else:
                next_bidder = self.other_auction_players[0]
                self.current_player = next_bidder

        elif action_type == 'ACCEPT_TRADE':
            # get back to the original player after accepting/declining the trade
            self.current_player = self.trade_list[0]
            self.act(action[11])
        elif action_type == 'MORTGAGE':
            player.mortgage_property(action[5])
        elif action_type == 'UNMORTGAGE':
            player.unmortgage_property(action[6])
        elif action_type == 'TRADE':
        #     7 : TRADE WITH PLAYER NUMBER
        #     8 : TRADE MONEY YOU GIVE
        #     9 : TRADE MONEY YOU TAKE
        #     12-37: YOUR PROPERTY OFFERS
        #     38-63: ENEMY PROPERTY WANTS
            my_offerings = action[12:38]
            property_desired = action[38:]
            self.trade_list = [player, action[7], action[8], action[9], my_offerings, property_desired]
            print("Trade Request Sent")
            self.current_player = action[7]
        elif action_type == 'BUY_HOUSE':
            player.buy_house(action[3])
        elif action_type == 'SELL_HOUSE':
            player.sell_house(action[4])
        elif action_type == 'END':
            if player.is_bankrupt():
                print("\nA player went bankrupt.\n")
                self.players.remove(player)
                if self.game_ended():
                    print("Game over!")
            if player.rolled_number_doubles > 0:
                self.current_player = player
            else:
                index_next_player = (self.players.index(player) + 1) % len(self.players)
                self.current_player = self.players[index_next_player]
            self.turns += 1
            self.print_property_and_money()
            player.rolled_dice_this_turn = False
        elif action_type == 'ROLL-DICE':
            player.rolled_dice_this_turn = True
            sum_die, self.rolled_double = self.roll_dice()
            if player.player_number == 1:
                sum_die = 12
                self.rolled_double = True
            if self.rolled_double:
                print("This player rolled doubles!!!!\n")
                player.rolled_number_doubles += 1
            else:
                self.rolled_double = False
                player.rolled_number_doubles = 0
            # Go to jail for 3 doubles in a roll
            if player.rolled_number_doubles >= 3:
                print(player.symbol, "ROLLED 3 DOUBLES consecutively, move to Jail for speeding!")
                self.land_on_type5(player)
                player.rolled_number_doubles = 0
            else:
                self.move_player(player, sum_die)
                self.check_landed_on_type(player, sum_die)
            self.print_board()
        else:
            print(f'Unrecognized action {action_type}')
    
    def print_info(self):
        self.print_board()
        self.print_property_and_money()
    
    def reset(self):
        self.WON_MONOPOLY = None
        self.board = BOARD
        self.chance_cards = []
        self.comm_cards = []
        self.turns = 1
        p1 = Player(1)
        p2 = Player(2)
        p3 = Player(3)
        p4 = Player(4)
        self.players = [p1, p2, p3, p4]
        self.total_houses = 32
        self.total_hotels = 12
        self.rolled_double = False
        self.current_player = self.players[0]
        self.player_before_auction_state = None
        self.highest_bid = 0
        self.player_with_highest_bid = None
        self.trade_list = []
        self.other_auction_players = self.players.copy()
        return self.get_state()

    def get_state(self):
        return [self.players, self.current_player, self.board, self.total_houses, self.total_hotels, self.rolled_double, self.in_auction, self.highest_bid, self.player_with_highest_bid, self.other_auction_players]



            
ACTION_LOOKUP = {
    0 : 'BUY_PROPERTY_LANDED',
    1 : 'IN_JAIL_ACTION',
    2 : 'CONTINUE_AUCTION',
    3 : 'ACCEPT_TRADE',
    4 : 'MORTGAGE',
    5 : 'UNMORTGAGE',
    6 : 'TRADE',
    7 : 'BUY_HOUSE',
    8 : 'SELL_HOUSE',
    9 : 'END',
    10 : 'ROLL-DICE'
}

