import random
import time
import player
import human_player
import board_info
import chance
import comm_chest

# Turn Examples:
#     actions() -> [List]
#     rolldie()
#         -buy_property_landed_on()
#             -possible_auction()
#             -actions() -> [List]
#         -possible_pay_rent()
#     actions() -> [List]

class Game:
    def __init__(self):
        self.board = board_info.BOARD
        self.player_turn_indicator = 0
        self.turns = 1
        p1 = player.Player("(P1)")
        p2 = player.Player("(P2)")
        self.players = [p1, p2]
        # -1 == not buyable, 0 == buyable, class_ref == bought
        self.owner_list = [-1, 0, -1, 0, -1, 0, 0, -1, 0, 0, 
                            -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 
                            -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 
                            -1, 0, 0, -1, 0, 0, -1, 0, -1, 0]

    def roll_dice(self):
        first_roll = random.randint(1,6)
        second_roll = random.randint(1,6)
        return (first_roll + second_roll, first_roll == second_roll)
    
    # Only works for 2 players right now
    def get_current_player(self, players):
        return players[0] if self.player_turn_indicator % 2 == 0 else players[1]
    
    def move_player(self, player, sum_die):
        player.position += sum_die
        if player.position >= 40:
            player.position = player.position % 40
            print(player.symbol, "passed GO, collect $200")
            player.money += 200

    # FIXME: Pricing with Houses/Hotels
    def land_on_type0(self, current_player, board):
        # curr_property_owner = self.property_owner(self.board, self.players, current_player.position)
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == 0:
            print(current_player.symbol, "Current money:", current_player.money)
            action = current_player.player_buys_property(board)
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-board[current_player.position][1])
                self.owner_list[current_player.position] = current_player
                print(f"{current_player.symbol} bought the {board[current_player.position][3]} property named: "
                        f"{board[current_player.position][2]}\n")
            elif action == "n" or action == "N":
                # TODO: Auction phase, more parameters
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
            amount = board[current_player.position][4]
            current_player.update_money(-amount)
            curr_property_owner.update_money(amount)
            print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")
    
    def land_on_type1(self, current_player, board):
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == 0:
            print(f"{current_player.symbol} Current money: ${current_player.money}")
            action = current_player.player_buys_railroad_utility(board)
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-board[current_player.position][1])
                self.owner_list[current_player.position] = current_player
                print(f"{current_player.symbol} bought RailRoad property: {board[current_player.position][2]}\n")
            elif action == "N" or action == "n":
                # TODO WORK ON THIS
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
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
            curr_property_owner.update_money(-25*total_amount)
            print(f"{current_player.symbol} paid rent of ${25*total_amount} to {curr_property_owner.symbol}")
    
    # TODO- Mortgage for this
    def land_on_type2(self, current_player, board, die_roll):
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == 0:
            print(f"{current_player.symbol} Current money: ${current_player.money}")
            action = current_player.player_buys_railroad_utility(board)
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-board[current_player.position][1])
                self.owner_list[current_player.position] = current_player
                print(f"{current_player.symbol} bought Water-Works / Electric property: {board[current_player.position][2]}\n")
            elif action == "N" or action == "n":
                # TODO WORK ON THIS
                self.auction_phase()
        else:
            total_amount, amount = 0, 0
            if 12 in curr_property_owner.property_in_use:
                total_amount += 1
            if 28 in curr_property_owner.property_in_use:
                total_amount += 1
            
            if total_amount == 2:
                amount = die_roll*10
            elif total_amount == 1:
                amount = die_roll*4

            current_player.update_money(-amount)
            curr_property_owner.update_money(amount)
            print(f"{current_player.symbol} paid ${amount} rent to {curr_property_owner.symbol}")

    # TODO- Need to update Income tax to be possible 10% worth vs $200.00
    def land_on_type3(self, current_player, board):
        tax_amount = board[current_player.position][1]
        current_player.update_money(-tax_amount)
        print(f"{current_player.symbol} landed on TAXES. Has to pay ${tax_amount}")
        print(f"{current_player.symbol} Current Money Now: ${current_player.money}\n")

    def land_on_type5(self, current_player, board):
        # Go to Jail
        current_player.position = 10
        current_player.in_jail = True
        current_player.turns_in_jail = 0

    # TODO Need this auction phase done
    def auction_phase(self):
        pass
            
    def print_board(self, players):
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
        # pretty print
        for player in players:
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
        
        for i, e in enumerate(mini_board):
            print(e)
        print("\n")
    
    # Alternative styling.
    # def property_owner(self, board, players, property_index):
    #     for player in players:
    #         if player.owns_property(board, property_index):
    #             return player
    #     return "UNOWNED PROPERTY"

    def check_landed_on_type(self, board, current_player, sum_die):
        if board[current_player.position][0] == 0:
            self.land_on_type0(current_player, board)
        elif board[current_player.position][0] == 1:
            self.land_on_type1(current_player, board)
        elif board[current_player.position][0] == 2:
            self.land_on_type2(current_player, board, sum_die)
        elif board[current_player.position][0] == 3:
            self.land_on_type3(current_player, board)
        elif board[current_player.position][0] == 4:
            print(f"{current_player.symbol} Landed on Free Parking or GO or Just Visiting, Nothing happens!")
        elif board[current_player.position][0] == 5:
            self.land_on_type5(current_player, board)
        # elif board[current_player.position][0] == 6:
        #     self.land_on_type6(current_player, board)
        # elif board[current_player.position][0] == 7:
        #     self.land_on_type7(current_player, board)
        else:
            print("Landed on Type Not Yet Programmed In.\n")

    def run(self, players, board):
        number_doubles = 0
        while not players[0].is_bankrupt() and not players[1].is_bankrupt():
            print("-----------------------")
            print("\tTurn", self.turns, ":")
            print("-----------------------")
            current_player = self.get_current_player(players)

            # TODO: Add trade / mortgage phase here!
            # actions = current_player.get_actions(board, players, sum_die=-1, rolled_double)

            sum_die, rolled_double = self.roll_dice()
            number_doubles += rolled_double
            
            # FIXME: Sent to jail for rolling two doubles, 
            # if current_player.in_jail:
            #     if current_player.turns_in_jail < 3:
            #         # 3 options, USE_JAIL_CARD, PAY_50, ROLL_DOUBLE, NO
            #         got_out = current_player.get_out_jail_actions()
            #         if got_out == "ROLL_DOUBLE":
            #             print(f"{current_player.symbol} rolled a {sum_die} in Jail. Which was a {rolled_double} double.\n")
            #             if rolled_double:
            #                 current_player.turns_in_jail = 0
            #                 current_player.in_jail = False
            #                 number_doubles = 0
            #             else:
            #                 current_player.turns_in_jail += 1
            #                 # Moving one turn out of Jail early cuz of here
            #                 self.player_turn_indicator += 1
            #                 self.turns += 1
            #                 self.print_board(players)
            #                 if current_player.turns_in_jail <= 2:
            #                     continue
            #         elif current_player.get_out_jail_card > 0 and got_out == "USE_JAIL_CARD":
            #             current_player.get_out_jail_card -= 1
            #         elif got_out == "PAY_50":
            #             current_player.update_money(-50)
            #             print(f"{current_player.symbol} paid $50 to get out of Jail early!")
            #         else:
            #             print("Wrong output type")
            #     else:
            #         if not rolled_double:
            #             print(f"{current_player.symbol} paid $50, did not roll a third double")
            #             current_player.update_money(-50)
            #         current_player.turns_in_jail = 0
            #         current_player.in_jail = False
                
            #     if rolled_double or got_out != "ROLL_DOUBLE":
            #         current_player.turns_in_jail = 0
            #         current_player.in_jail = False


            if current_player.in_jail:
                action = current_player.get_out_jail_actions()
                if action == "ROLL_DOUBLE":
                    if current_player.turns_in_jail == 3:
                        if rolled_double:
                            print(f"{current_player.symbol} ROLLED A DOUBLE IN JAIL, GET OUT FOR FREE!")
                            number_doubles -= 1
                            rolled_double = False
                        else:
                            current_player.update_money(-50)
                            print(f"{current_player.symbol} paid $50 because 3 turns passed w/o doubles")
                        current_player.turns_in_jail = 0
                        current_player.in_jail = False
                    elif current_player.turns_in_jail < 3:
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
                            self.print_board(players)
                            continue
                elif current_player.get_out_jail_card > 0 and action == "USE_JAIL_CARD":
                    current_player.get_out_jail_card -= 1
                    print(f"{current_player.symbol} used a Get out of Jail Card")
                    current_player.in_jail = False
                elif action == "PAY_50":
                    current_player.update_money(-50)
                    print(f"{current_player.symbol} paid $50 to get out of Jail early!")
                    current_player.in_jail = False
                else:
                    print("Wrong Output for Jail Action")

            if number_doubles >= 3:
                print(current_player.symbol, "ROLLED 3 DOUBLES consecutively, move to Jail for speeding!")
                self.land_on_type5(current_player, board)
                number_doubles = 0
                self.turns += 1
                self.print_board(players)
                continue

            if rolled_double:
                print(current_player.symbol, "ROLLED A DOUBLE!!! Goes again next turn!!!")

            # TODO: check for mortgage and trades
            # current_player.get_actions(board, players, sum_die, rolled_double)
 
            self.move_player(current_player, sum_die)
            print(f"\n{current_player.get_symbol()} rolled ({sum_die}) to {board[current_player.position][2]}\n")
            self.print_board(players)
            self.check_landed_on_type(board, current_player, sum_die)
        
            # TODO: Add trade / mortgage phase here as well!
            # current_player.get_actions(board, players, sum_die, rolled_double)
            for player in players:
                print(player.symbol, "money:", player.get_money())
            print("\n")

            for i,e in enumerate(self.owner_list):
                if e is not 0 and e is not -1:
                    print(f"{board[i][2]} [{i}] - owned by {e.symbol}")
            print("\n")

            if not (rolled_double and current_player.in_jail == False):
                self.player_turn_indicator += 1
                number_doubles = 0

            self.turns += 1





if __name__ == "__main__":
    game = Game()
    game.run(game.players, game.board)

    print("\nOutcome of Game: ")
    for player in game.players:
        print(player.symbol, player.total_equity)