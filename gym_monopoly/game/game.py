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
            current_player.must_buy_or_auction = True
            return False
        else:
            loc = current_player.position
            if self.board[loc][0] == 0:
                self.rent_on_type0(curent_player, curr_property_owner)
            elif self.board[loc][0] == 1:
                self.rent_on_type1(curent_player, curr_property_owner)
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

    # TODO Need this auction parameters
    def auction_phase(self, prop_index):
        print("\nEntered an auction!!!!\n")
        auction_state = [True for x in self.players]
        highest_price = 0
        player_with_highest_bid = None
        while sum(auction_state) > 1:
            # Only iterates through the players who don't have the highest bid
            for player in list(filter(lambda a: a != player_with_highest_bid, self.players)):
                raise_price = input("Does " + player.symbol + " want to buy " + self.board[prop_index][2] + " (Y/N) ")
                raise_price = raise_price.upper()
                if raise_price == "Y":
                    action = -1
                    while (action <= highest_price):
                        print("Highest price: ", highest_price)
                        action = input("What is the price that " + player.symbol + " bids for " + self.board[prop_index][2] + "?  $")
                        try:
                            action = int(action)
                        except ValueError:
                            print("User didn't input a valid number.")
                    highest_price = action
                    player_with_highest_bid = player
                    auction_state = [True for x in self.players]
                    break
                elif raise_price == "N":
                    auction_state[int(player.symbol[2]) - 1] = False
                else:
                    print("Did not understand what you wanted to do, (y/n) ONLY >>")
        
        player_with_highest_bid.update_money(-highest_price)
        player_with_highest_bid.update_equity(-highest_price + int(self.board[prop_index][1]/2))
        player_with_highest_bid.property_in_use.append(prop_index)
        print(f"\nCongratulations {player_with_highest_bid.symbol} bought {self.board[prop_index][2]}"
                f" for ${highest_price}!")
            
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

    def action_trade(self, current_player, sum_die, rolled_double):
        prompt = ""
        while prompt != 'n':
            if prompt == 'y':
                action = current_player.get_actions(self.players, sum_die=-1, rolled_double=-1)
                if action[0] == 'M':
                    current_player.mortgage_property(action[1])
                elif action[0] == 'U':
                    current_player.unmortgage_property(action[1])
                elif action[0] == 'T':
                    _, trade_player, curr_property_offers, trader_property_offers, curr_money, trader_money = action
                    print(f"Trade request sent between {current_player.symbol} and {trade_player.symbol}")
                    try:
                        curr_property_offers.remove('')
                    except ValueError:
                        print("")
                    try:
                        trader_property_offers.remove('')
                    except ValueError:
                        print("")
                    if curr_property_offers:
                        curr_property_offers = list(map(int, curr_property_offers)) 
                    if trader_property_offers:
                        trader_property_offers = list(map(int, trader_property_offers)) 
                    trade_response = trade_player.agree_disagree_trade(current_player, curr_property_offers,
                                                        trader_property_offers, curr_money, trader_money)
                    if trade_response == 'agree':
                        print("Agreed to trade")
                        try:
                            curr_money = int(curr_money)
                        except ValueError:
                            curr_money = 0
                        try:
                            trader_money = int(trader_money)
                        except ValueError:
                            trader_money = 0
                        current_player.update_money(-curr_money)
                        current_player.update_equity(-curr_money)
                        trade_player.update_money(curr_money)
                        trade_player.update_equity(curr_money)
                        current_player.update_money(trader_money)
                        current_player.update_equity(trader_money)
                        trade_player.update_money(-trader_money)
                        trade_player.update_equity(-trader_money)
                        print(f"{current_player.symbol} ${current_player.money}, "
                                f"{current_player.symbol} ${trade_player.money}")

                        # FIXME :()
                        for i in trader_property_offers:
                            print(i, "WOWOWOWOWOWOWOW")
                            if i in trade_player.property_in_use:
                                trade_player.property_in_use.remove(i)
                                current_player.property_in_use.append(i)
                            elif i in trade_player.property_in_mort:
                                trade_player.property_in_mort.remove(i)
                                current_player.property_in_mort.append(i)
                                response = current_player.might_pay_10_percent_extra_mortgaged_property(i)
                                if response == 'y':
                                    current_player.unmortgage_property(i)
                                elif response == 'n':
                                    ten_percent_interest = math.ceil((self.board[i][1] // 2) * .1)
                                    current_player.update_money(-ten_percent_interest)
                                    current_player.update_equity(-ten_percent_interest)
                                else:
                                    print("Didn't understand prompt to unmortgage!")
                            else:
                                print("Player doesn't own this property to trade!")
                        
                        # FIXME, error in trades
                        for i in curr_property_offers:
                            print(i, "WOWOWOWOWOWOWOW")
                            if i in current_player.property_in_use:
                                current_player.property_in_use.remove(i)
                                trade_player.property_in_use.append(i)
                            elif i in current_player.property_in_mort:
                                current_player.property_in_mort.remove(i)
                                trade_player.property_in_mort.append(i)
                                response = trade_player.might_pay_10_percent_extra_mortgaged_property(i)
                                if response == 'y':
                                    trade_player.unmortgage_property(i)
                                elif response == 'n':
                                    ten_percent_interest = math.ceil((self.board[i][1] // 2) * .1)
                                    trade_player.update_money(-ten_percent_interest)
                                    trade_player.update_equity(-ten_percent_interest)
                                else:
                                    print("Didn't understand prompt to unmortgage!")
                            else:
                                print("Player doesn't own this property to trade!")
                    else:
                        print(trade_player.symbol, "has disagreed the trade offer!")
                        print("You can request another Trade offer... or not.")
                elif action[0] == 'B':
                    current_player.buy_house(action[1])
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
    
    def game_ended(self):
        if len(self.players) == 1:
            self.WON_MONOPOLY = self.players[0]
            return True
        else:
            return False

    def run(self):
        number_doubles = 0
        while not self.game_ended:
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
                            current_player.update_money(-50)
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
                    current_player.update_money(-50)
                    current_player.update_equity(-50)
                    print(f"{current_player.symbol} paid $50 to get out of Jail early!")
                    current_player.in_jail = False
                    current_player.turns_in_jail = 0
                else:
                    print("You cannot do that, resources unavailable or wrong command. Your turn will restart!\n")
                    current_player.turns_in_jail -= 1
                    if number_doubles > 0:
                        number_doubles -= 1
                    continue

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
            # print(f"\n---> {current_player.get_symbol()} rolled ({sum_die}) to {self.board[current_player.position][2]}\n")
            # if rolled_double:
            #     print(current_player.symbol, "ROLLED A DOUBLE!!! Gets to go again next turn!!!\n")

            self.check_landed_on_type(current_player, sum_die)
            # self.print_board()
        
            # self.action_trade(players, board, current_player, sum_die, rolled_double)
            
            # self.print_property_and_money()

            # if not (rolled_double and current_player.in_jail == False):
            #     self.player_turn_indicator += 1
            #     number_doubles = 0

            # self.turns += 1

    def validate_move(self, player, action):
        action_type = ACTION_LOOKUP[action[0]]
        if action_type == 'END':
            return player.rolled_dice_this_turn and not player.must_buy_or_auction
        elif action_type == 'ROLL-DICE':
            return (not player.rolled_dice_this_turn and not player.in_jail)
        elif action_type == 'BUY_PROPERTY_LANDED':

            #FIXME: Make sure that the property can be purchased
            #FIXME: Make sure that the property is correct. 
            curr_property_owner = None
            for real_player in self.players:
                player_full_property_list = real_player.property_in_use + real_player.property_in_mort
                if player.position in player_full_property_list:
                    curr_property_owner = real_player
            return player is not curr_property_owner

        elif action_type == 'BUY_HOUSE':
            return player.buyable(action[3])
        elif action_type == 'SELL_HOUSE':
            return player.sellable(action[4])

    # action = [0, None, None, None, 1, None]
    # obs -> self.players, go_again_next_turn, board_properties, player_turn
    def action_helper(self, action):
        player = self.get_current_player()
        action_type = ACTION_LOOKUP[action[0]]
        print(action_type)

        if not self.validate_move(player, action):
            print(f"Failed to do a Valid Move")
            return
        
        self.current_player = player

        # TODO
        if action_type == 'BUY_PROPERTY_LANDED':
            self.current_player.must_buy_or_auction = False
            pass
            # action = action[2]
            # if (action == 1) and (player.money > self.board[current_player.position][1]):
            #     current_player.update_money(-self.board[current_player.position][1])
            #     current_player.update_equity(-int(self.board[current_player.position][1]/2))

            #     current_player.property_in_use.append(current_player.position)
            #     print(f"{current_player.symbol} bought the {self.board[current_player.position][3]} property named: "
            #             f"{self.board[current_player.position][2]}\n")
            # elif action == 0:
            #     # TODO: Auction phase, more parameters
            #     self.next_player = self.players
        elif action_type == 'IN_JAIL_ACTION':
            self.act(action[1])
        elif action_type == 'CONTINUE_AUCTION':
            self.act(action[12])
        elif action_type == 'ACCEPT_TRADE':
            self.act(action[13])
        elif action_type == 'MORTGAGE':
            player.mortgage_property(action[5])
        elif action_type == 'UNMORTGAGE':
            player.unmortgage_property(action[6])
        elif action_type == 'TRADE':
            self.act(action[7], action[8], action[9], action[10], action[11])
            self.current_player = action[7]
        elif action_type == 'BUY_HOUSE':
            player.buy_house(action[3])
        elif action_type == 'SELL_HOUSE':
            player.sell_house(action[4])
        elif action_type == 'END':
            if player.is_bankrupt():
                print("player went bankrupt.")
                self.players.remove(player)

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
            if self.rolled_double:
                player.rolled_number_doubles += 1
            else:
                player.rolled_number_doubles = 0
            # Go to jail for 3 doubles in a roll
            if player.rolled_number_doubles >= 3:
                print(player.symbol, "ROLLED 3 DOUBLES consecutively, move to Jail for speeding!")
                self.land_on_type5(player)
                player.rolled_number_doubles = 0
            else:
                self.move_player(player, sum_die)
                self.check_landed_on_type(player, sum_die)
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
        self.current_player = self.players[0]
        return [self.players, self.current_player, self.board, self.total_houses, self.total_hotels, None]

    def get_state(self):
        return [self.players, self.current_player, self.board, self.total_houses, self.total_hotels, self.rolled_double]


# if __name__ == "__main__":
#     print("Started Game")
#     game = Game()
#     game.run()

#     print("\nOutcome of Game: ")
#     for player in game.players:
#         print(player.symbol, "Equity: ", player.total_equity, "Value: ", player.money)


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

