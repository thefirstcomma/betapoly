import random
import time
from colorama import Fore, Style
import player
import board_info

# Turn Examples:
#     actions() -> [List]
#     rolldie()
#         -buy_property_landed_on()
#             -possible_auction()
#             -actions() -> [List]
#         -possible_pay_rent()
#     actions() -> [List]

# FIXME
# Deal with 4-8 players, get_current_player(self, players)
# Have at max 2 G.o.o.J Cards
# Colorama, for board presentation
# Auction Phase
# Finish (T)rading
# Check Mortgage for Type 2 (elec/Util)
# Need to update Income tax to be possible 10% worth vs $200.00 (in type3)
# Check printing overall throughout the Game
# Auction for housing, limit housing=32, hotels=12, and everytime someone buys/sells houses, iterate player actions.
# Fix Game__init__() for player# parameter/input
# Add a state for Player -> .open_for_trading()

class Game:
    def __init__(self):
        self.board = board_info.BOARD
        self.chance_cards = []
        self.comm_cards = []
        self.player_turn_indicator = 0
        self.turns = 1
        self.numb_players = 2
        p1 = player.Player("(P1)")
        p2 = player.Player("(P2)")
        self.players = [p1, p2]
        # -1 == not buyable, 0 == buyable, player.symbol == bought
        self.owner_list = [-1, 0, -1, 0, -1, 0, 0, -1, 0, 0, 
                            -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 
                            -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 
                            -1, 0, 0, -1, 0, 0, -1, 0, -1, 0]
        self.total_houses = 32
        self.total_hotels = 12

    def roll_dice(self):
        first_roll = random.randint(1,6)
        second_roll = random.randint(1,6)
        return (first_roll + second_roll, first_roll == second_roll)
    
    # TODO Only works for 2 players right now
    def get_current_player(self):
        return self.players[0] if self.player_turn_indicator % self.numb_players == 0 else self.players[1]
    
    def move_player(self, player, sum_die):
        player.position += sum_die
        if player.position >= 40:
            player.position = player.position % 40
            print(player.symbol, "passed GO, collect $200")
            player.update_money(200, self.players)
            player.update_equity(200)

    def move_cuz_card(self, player, future_location):
        if player.position > future_location:
            player.update_money(200, self.players)
            player.update_equity(200)
        player.position = future_location

    def land_on_type0(self, current_player):
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            print(f"Landed on property you {current_player.symbol} already owns.")
        elif curr_property_owner == 0:
            print(current_player.symbol, "Current money:", current_player.money)
            action = current_player.player_buys_property()
            if (action == "y" or action == "Y") and (current_player.money > self.board[current_player.position][1]):
                current_player.update_money(-self.board[current_player.position][1], self.players)
                current_player.update_equity(-int(self.board[current_player.position][1]/2))
                self.owner_list[current_player.position] = current_player
                current_player.property_in_use.append(current_player.position)
                print(f"{current_player.symbol} bought the {self.board[current_player.position][3]} property named: "
                        f"{self.board[current_player.position][2]}\n")
            elif action == "n" or action == "N":
                # TODO: Auction phase, more parameters
                self.auction_phase()
        else: #The case where we have a property owner
            loc = current_player.position
            if loc not in curr_property_owner.property_in_mort:
                if curr_property_owner.is_monopoly(loc): 
                    numb_houses = curr_property_owner.houses[loc]
                    if numb_houses > 0:
                        amount = self.board[current_player.position][4+numb_houses]
                        current_player.update_money(-amount, self.players)
                        current_player.update_equity(-amount)
                        curr_property_owner.update_money(amount, self.players)
                        curr_property_owner.update_equity(amount)
                        print(f"Paid extra because this property has {numb_houses} houses")
                        print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
                    else:
                        amount = self.board[current_player.position][4]*2
                        current_player.update_money(-amount, self.players)
                        current_player.update_equity(-amount)
                        curr_property_owner.update_money(amount, self.players)
                        current_player.update_equity(amount)
                        print(f"Paid extra because this property is a monopoly w/o houses")
                        print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
                else:
                    amount = self.board[current_player.position][4]
                    current_player.update_money(-amount, self.players)
                    current_player.update_equity(-amount)
                    curr_property_owner.update_money(amount, self.players)
                    curr_property_owner.update_equity(amount)
                    print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
            else:
                print(f"{current_player.symbol} Landed on Mortgaged property, No payments YAY!!!")
    
    def land_on_type1(self, current_player):
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            print(f"Landed on property you {current_player.symbol} already owns.")
        elif curr_property_owner == 0:
            print(f"{current_player.symbol} Current money: ${current_player.money}")
            action = current_player.player_buys_railroad_utility()
            if (action == "y" or action == "Y") and (current_player.money > self.board[current_player.position][1]):
                current_player.update_money(-self.board[current_player.position][1], self.players)
                current_player.update_equity(-int(self.board[current_player.position][1]/2))
                self.owner_list[current_player.position] = current_player
                current_player.property_in_use.append(current_player.position)
                print(f"{current_player.symbol} bought RailRoad property: {self.board[current_player.position][2]}\n")
            elif action == "N" or action == "n":
                # TODO needs more parameters
                self.auction_phase()
        else: # Assuming no houses/hotel is bought
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
                current_player.update_money(-25*total_amount, self.players)
                current_player.update_equity(-25*total_amount)
                curr_property_owner.update_money(25*total_amount, self.players)
                curr_property_owner.update_equity(25*total_amount)
                print(f"{current_player.symbol} paid rent of ${25*total_amount} to {curr_property_owner.symbol}")
            else:
                print("Laned on mortgaged Railroad, No rent here!")
    
    def land_on_type2(self, current_player, die_roll):
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            print(f"Landed on property you {current_player.symbol} already owns.")
        elif curr_property_owner == 0:
            print(f"{current_player.symbol} Current money: ${current_player.money}")
            action = current_player.player_buys_railroad_utility()
            if (action == "y" or action == "Y") and (current_player.money > self.board[current_player.position][1]):
                current_player.update_money(-self.board[current_player.position][1], self.players)
                current_player.update_equity(-int(self.board[current_player.position][1]/2))
                self.owner_list[current_player.position] = current_player
                current_player.property_in_use.append(current_player.position)
                print(f"{current_player.symbol} bought Water-Works / Electric property: {self.board[current_player.position][2]}\n")
            elif action == "N" or action == "n":
                # TODO WORK ON parameters for auction phase
                self.auction_phase()
        else:
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
                current_player.update_money(-amount, self.players)
                current_player.update_equity(-amount)
                curr_property_owner.update_money(amount, self.players)
                curr_property_owner.update_equity(amount)
                print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
            else:
                print("Laned on mortgaged Util, No rent here!")

    def land_on_type3(self, current_player):
        tax_amount = self.board[current_player.position][1]
        current_player.update_money(-tax_amount, self.players)
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
            self.comm_cards = board_info.COMMUNITY_CHEST.copy()
            random.shuffle(self.comm_cards)

        card = (self.comm_cards.pop())
        print(f"\tLanded on Community Chest!! {card[1]}")

        if card[0] == 0:
            current_player.update_money(card[3], self.players)
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
                    current_player.update_money(card[3], self.players)
                    current_player.update_equity(card[3])
                    player.update_money(-card[3], self.players)
                    player.update_equity(-card[3])
                    print(f"{current_player.symbol} collected ${card[3]} from {player.symbol}")
        elif card[0] == 4:
            houses, hotels = current_player.get_houses_and_hotels()
            print(f"Pay for each house: {houses} and hotel: {hotels}")
            current_player.update_money(houses * card[2], self.players)
            current_player.update_equity(houses * card[2])
            current_player.update_money(hotels * card[3], self.players)
            current_player.update_equity(hotels * card[3])
            print(f"{current_player.symbol} money updated {current_player.money}")
    
    def land_on_type7(self, current_player, die_roll):
        if len(self.chance_cards) == 0:
            self.chance_cards = board_info.CHANCE.copy()
            random.shuffle(self.chance_cards)

        card = (self.chance_cards.pop())
        print(f"Landed on Chance, {card[1]}")

        if card[0] == 0:
            current_player.update_money(card[3], self.players)
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
                    current_player.update_money(card[3], self.players)
                    current_player.update_equity(card[3])
                    player.update_money(-card[3], self.players)
                    player.update_equity(-card[3])
                    print(f"{current_player.symbol} paid {player.symbol} ${card[3]}")
        elif card[0] == 4:
            houses, hotels = current_player.get_houses_and_hotels()
            print(f"Pay for each house: {houses} and hotel: {hotels}")
            current_player.update_money(houses * card[2], self.players)
            current_player.update_equity(houses * card[2])
            current_player.update_money(hotels * card[3], self.players)
            current_player.update_equity(hotels * card[3])
            print(f"{current_player.symbol} money updated {current_player.money}")
        elif card[0] == 5:
            if card[2] == "util":
                if current_player.position > 28:
                    current_player.position = 12
                    print("Passed GO, collect 200")
                    current_player.update_money(200, self.players)
                    current_player.update_equity(200)
                elif current_player.position > 12:
                    current_player.position = 28
                elif current_player.position < 12:
                    current_player.position = 12
                self.land_on_type2(current_player, die_roll)
            elif card[2] == "railroad":
                if current_player.position > 35:
                    current_player.position = 5
                    current_player.update_money(200, self.players)
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

    # TODO Need this auction parameters
    def auction_phase(self):
        pass
            
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
            self.land_on_type0(current_player)
        elif self.board[current_player.position][0] == 1:
            self.land_on_type1(current_player)
        elif self.board[current_player.position][0] == 2:
            self.land_on_type2(current_player, sum_die)
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

    def action_trade(self, current_player, sum_die, rolled_double):
        prompt = ""
        while prompt != 'n':
            if prompt == 'y':
                action = current_player.get_actions(self.players, sum_die=-1, rolled_double=-1)
                if action[0] == 'M':
                    current_player.mortgage_property(action[1], self.players)
                elif action[0] == 'U':
                    current_player.unmortgage_property(action[1], False, self.players)
                elif action[0] == 'T':
                    _, trade_player, curr_property_offers, trader_property_offers, curr_money, trader_money = action
                    print(f"Trade request sent between {current_player.symbol} and {trade_player.symbol}")
                    curr_property_offers = list(map(int, curr_property_offers)) 
                    trader_property_offers = list(map(int, trader_property_offers)) 
                    trade_response = trade_player.agree_disagree_trade(current_player, curr_property_offers,
                                                        trader_property_offers, curr_money, trader_money)
                    if trade_response == 'agree':
                        print("Agreed to trade")
                        curr_money, trader_money = int(curr_money), int(trader_money)
                        current_player.update_money(-curr_money, self.players)
                        current_player.update_equity(-curr_money)
                        trade_player.update_money(curr_money, self.players)
                        trade_player.update_equity(curr_money)
                        current_player.update_money(trader_money, self.players)
                        current_player.update_equity(trader_money)
                        trade_player.update_money(-trader_money, self.players)
                        trade_player.update_equity(-trader_money)
                        print(f"{current_player.symbol} ${current_player.money}, "
                                f"{current_player.symbol} ${trade_player.money}")
                        print("----Work on property transferring here-----")
                        # TODO :(
                    else:
                        print(trade_player.symbol, "has disagreed the trade offer!")
                        print("You can request another Trade offer... or not.")
                elif action[0] == 'B':
                    current_player.buy_house(action[1], self.players)
                    print("Houses Now: ", current_player.print_houses())
                elif action[0] == 'S':
                    current_player.sell_house(action[1], self.players)
                    print("Houses Now: ", current_player.print_houses())
                    print("Money: ", current_player.money)
                elif action[0] == 'no_action':
                    prompt = "n"
                else:
                    print("Didn't understand input!")

            prompt = input("Do you want more actions? (y) or (n) ")
            prompt = prompt.lower().strip()

    def run(self):
        number_doubles = 0
        while not self.players[0].is_bankrupt() and not self.players[1].is_bankrupt():
            print("-----------------------")
            print("\tTurn", self.turns, ":")
            print("-----------------------")
            current_player = self.get_current_player()
            print(current_player.symbol, "turn!")

            # TODO: Add actions phase here!
            self.action_trade(current_player, sum_die=-1, rolled_double=-1)
            
            sum_die, rolled_double = self.roll_dice()
            number_doubles += rolled_double

            if current_player.in_jail:
                action = current_player.get_out_jail_actions()
                if action == "ROLL_DOUBLE":
                    if current_player.turns_in_jail == 2:
                        if rolled_double:
                            print(f"{current_player.symbol} ROLLED A DOUBLE IN JAIL, GET OUT FOR FREE!")
                            number_doubles -= 1
                            rolled_double = False
                        else:
                            current_player.update_money(-50, self.players)
                            current_player.update_equity(-50)
                            print(f"{current_player.symbol} paid $50 because 3 turns passed w/o doubles")
                        current_player.turns_in_jail = 0
                        current_player.in_jail = False
                    elif current_player.turns_in_jail < 2:
                        if rolled_double:
                            print(f"{current_player.symbol} ROLLED A DOUBLE IN JAIL, GET OUT FOR FREE!")
                            number_doubles -= 1
                            current_player.turns_in_jail = 0
                            current_player.in_jail = False
                            rolled_double = False
                        else:
                            print(f"{current_player.symbol} did not roll a double in Jail\n")
                            current_player.turns_in_jail += 1
                            self.turns += 1
                            self.player_turn_indicator += 1
                            self.print_board()
                            continue
                elif current_player.get_out_jail_card > 0 and action == "USE_JAIL_CARD":
                    current_player.get_out_jail_card -= 1
                    print(f"{current_player.symbol} used a Get out of Jail Card")
                    current_player.in_jail = False
                    current_player.turns_in_jail = 0
                elif current_player.money >= 50 and action == "PAY_50":
                    current_player.update_money(-50, self.players)
                    current_player.update_equity(-50)
                    print(f"{current_player.symbol} paid $50 to get out of Jail early!")
                    current_player.in_jail = False
                    current_player.turns_in_jail = 0
                else:
                    print("You cannot do that, resources unavailable or wrong command.")

            if number_doubles >= 3:
                print(current_player.symbol, "ROLLED 3 DOUBLES consecutively, move to Jail for speeding!")
                self.land_on_type5(current_player)
                number_doubles = 0
                self.turns += 1
                self.print_board()
                self.player_turn_indicator += 1
                self.print_property_and_money()
                continue

            # TODO: Add actions phase here
            # self.action_trade(players, board, current_player, sum_die, rolled_double)
            
            self.move_player(current_player, sum_die)
            print(f"\n---> {current_player.get_symbol()} rolled ({sum_die}) to {self.board[current_player.position][2]}\n")
            if rolled_double:
                print(current_player.symbol, "ROLLED A DOUBLE!!! Gets to go again next turn!!!\n")

            self.check_landed_on_type(current_player, sum_die)
            self.print_board()
        
            # TODO: Add actions phase here
            # self.action_trade(players, board, current_player, sum_die, rolled_double)
            
            self.print_property_and_money()

            if not (rolled_double and current_player.in_jail == False):
                self.player_turn_indicator += 1
                number_doubles = 0

            self.turns += 1



if __name__ == "__main__":
    game = Game()
    game.run()

    print("\nOutcome of Game: ")
    for player in game.players:
        print(player.symbol, "Equity: ", player.total_equity, "Value: ", player.money)