# if __name__ == "__main__":
#     print("Started Game")
#     game = Game()
#     game.run()

#     print("\nOutcome of Game: ")
#     for player in game.players:
#         print(player.symbol, "Equity: ", player.total_equity, "Value: ", player.money)

# def run(self):
#         number_doubles = 0
#         while not self.game_ended:
#             print("-----------------------")
#             print("\tTurn", self.turns, ":")
#             print("-----------------------")
#             current_player = self.get_current_player()
#             print(current_player.symbol, "turn!")

#             # TODO: Add actions phase here!
#             self.action_trade(current_player, sum_die=-1, rolled_double=-1)
            
#             sum_die, rolled_double = self.roll_dice()
#             number_doubles += rolled_double

#             if current_player.in_jail:
#                 action = current_player.get_out_jail_actions()
#                 if action == "ROLL_DOUBLE":
#                     if current_player.turns_in_jail == 2:
#                         if rolled_double:
#                             print(f"{current_player.symbol} ROLLED A DOUBLE IN JAIL, GET OUT FOR FREE!")
#                             number_doubles -= 1
#                             rolled_double = False
#                         else:
#                             current_player.update_money(-50)
#                             current_player.update_equity(-50)
#                             print(f"{current_player.symbol} paid $50 because 3 turns passed w/o doubles")
#                         current_player.turns_in_jail = 0
#                         current_player.in_jail = False
#                     elif current_player.turns_in_jail < 2:
#                         if rolled_double:
#                             print(f"{current_player.symbol} ROLLED A DOUBLE IN JAIL, GET OUT FOR FREE!")
#                             number_doubles -= 1
#                             current_player.turns_in_jail = 0
#                             current_player.in_jail = False
#                             rolled_double = False
#                         else:
#                             print(f"{current_player.symbol} did not roll a double in Jail\n")
#                             current_player.turns_in_jail += 1
#                             self.turns += 1
#                             self.player_turn_indicator += 1
#                             self.print_board()
#                             continue
#                 elif current_player.get_out_jail_card > 0 and action == "USE_JAIL_CARD":
#                     current_player.get_out_jail_card -= 1
#                     print(f"{current_player.symbol} used a Get out of Jail Card")
#                     current_player.in_jail = False
#                     current_player.turns_in_jail = 0
#                 elif current_player.money >= 50 and action == "PAY_50":
#                     current_player.update_money(-50)
#                     current_player.update_equity(-50)
#                     print(f"{current_player.symbol} paid $50 to get out of Jail early!")
#                     current_player.in_jail = False
#                     current_player.turns_in_jail = 0
#                 else:
#                     print("You cannot do that, resources unavailable or wrong command. Your turn will restart!\n")
#                     current_player.turns_in_jail -= 1
#                     if number_doubles > 0:
#                         number_doubles -= 1
#                     continue

#             if number_doubles >= 3:
#                 print(current_player.symbol, "ROLLED 3 DOUBLES consecutively, move to Jail for speeding!")
#                 self.land_on_type5(current_player)
#                 number_doubles = 0
#                 self.turns += 1
#                 self.print_board()
#                 self.player_turn_indicator += 1
#                 self.print_property_and_money()
#                 continue

#             # TODO: Add actions phase here
#             # self.action_trade(players, board, current_player, sum_die, rolled_double)
            
#             self.move_player(current_player, sum_die)
#             # print(f"\n---> {current_player.get_symbol()} rolled ({sum_die}) to {self.board[current_player.position][2]}\n")
#             # if rolled_double:
#             #     print(current_player.symbol, "ROLLED A DOUBLE!!! Gets to go again next turn!!!\n")

#             self.check_landed_on_type(current_player, sum_die)
#             # self.print_board()
        
#             # self.action_trade(players, board, current_player, sum_die, rolled_double)
            
#             # self.print_property_and_money()

#             # if not (rolled_double and current_player.in_jail == False):
#             #     self.player_turn_indicator += 1
#             #     number_doubles = 0

#             # self.turns += 1



# def auction_phase(self, prop_index):
#         print("\nEntered an auction!!!!\n")
#         auction_state = [True for x in self.players]
#         highest_price = 0
#         player_with_highest_bid = None
#         while sum(auction_state) > 1:
#             # Only iterates through the players who don't have the highest bid
#             for player in list(filter(lambda a: a != player_with_highest_bid, self.players)):
#                 raise_price = input("Does " + player.symbol + " want to buy " + self.board[prop_index][2] + " (Y/N) ")
#                 raise_price = raise_price.upper()
#                 if raise_price == "Y":
#                     action = -1
#                     while (action <= highest_price):
#                         print("Highest price: ", highest_price)
#                         action = input("What is the price that " + player.symbol + " bids for " + self.board[prop_index][2] + "?  $")
#                         try:
#                             action = int(action)
#                         except ValueError:
#                             print("User didn't input a valid number.")
#                     highest_price = action
#                     player_with_highest_bid = player
#                     auction_state = [True for x in self.players]
#                     break
#                 elif raise_price == "N":
#                     auction_state[int(player.symbol[2]) - 1] = False
#                 else:
#                     print("Did not understand what you wanted to do, (y/n) ONLY >>")
        
#         player_with_highest_bid.update_money(-highest_price)
#         player_with_highest_bid.update_equity(-highest_price + int(self.board[prop_index][1]/2))
#         player_with_highest_bid.property_in_use.append(prop_index)
#         print(f"\nCongratulations {player_with_highest_bid.symbol} bought {self.board[prop_index][2]}"
#                 f" for ${highest_price}!")



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

                    # FIXME Something is broken here!
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