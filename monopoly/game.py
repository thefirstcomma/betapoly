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
        self.gametime = 0
        p1 = player.Player("(P1)")
        p2 = player.Player("(P2)")
        self.players = [p1, p2]
        # -1 == not buyable, 0 == buyable
        self.owner_list = [-1, 0, -1, 0, -1, 0, 0, -1, 0, 0, 
                            -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, 
                            -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 
                            -1, 0, 0, -1, 0, 0, -1, 0, -1, 0]

    def roll_dice(self):
        return random.randint(1,6) + random.randint(1,6)
    
    def move_player(self, player, sum_die):
        player.position += sum_die
        if player.position >= 40:
            player.position = player.position % 40
            player.money += 200

    # FIXME: Auctions, Houses/Hotels
    def land_on_type0(self, current_player, board):
        # curr_property_owner = self.property_owner(self.board, self.players, current_player.position)
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == 0:
            print(current_player.symbol, "Current money:", current_player.money)
            action = input(f"Does {current_player.symbol} buy the {board[current_player.position][3]} property named: " 
                            f"{board[current_player.position][2]} for ${board[current_player.position][1]} (Y/N)\n")
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-board[current_player.position][1])
                self.owner_list[current_player.position] = current_player
                print(f"{current_player.symbol} bought the {board[current_player.position][3]} property named: "
                        f"{board[current_player.position][2]}\n")
            elif action == "n" or action == "N":
                # TODO: Auction phase
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
            current_player.update_money(-board[current_player.position][4])
            curr_property_owner.update_money(board[current_player.position][4])
            print(f"{current_player.symbol} paid ${board[current_player.position][4]} rent to {curr_property_owner.symbol}")
    
    def land_on_type1(self, current_player, board):
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == 0:
            action = input(f"Does {current_player.symbol} buy property named: "
                            f"{board[current_player.position][2]} for ${board[current_player.position][1]} (Y/N)\n")
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-board[current_player.position][1])
                self.owner_list[current_player.position] = current_player
                print(f"{current_player.symbol} MONEY NOW: ${current_player.money}")
                print(f"{current_player.symbol} bought RailRoad property: {board[current_player.position][2]}\n")
            elif action == "N" or action == "n":
                # TODO WORK ON THIS
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
            total_amount = 0
            if 5 in curr_property_owner.property_in_use:
                total_amount += 1
            if 15 in curr_property_owner.property_in_use:
                total_amount += 1
            if 25 in curr_property_owner.property_in_use:
                total_amount += 1
            if 35 in curr_property_owner.property_in_use:
                total_amount += 1
            
            if total_amount == 3:
                total_amount = 4
            elif total_amount == 4:
                total_amount = 8
            current_player.update_money(-25*total_amount)
            curr_property_owner.update_money(-25*total_amount)
            print(f"{current_player.symbol} paid rent of  ${-25*total_amount} to {curr_property_owner.symbol}")

    # TODO Need this auction phase done
    def auction_phase(self):
        pass

    # Only works for 2 players right now
    def get_current_player(self, players):
        return players[0] if self.gametime % 2 == 0 else players[1]
            
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
            elif number <= 20:
                if mini_board[10-(number % 10)][0] == '-':
                    mini_board[10-(number % 10)][0] = ''
                mini_board[10-(number % 10)][0] += (player.get_symbol())
            elif number <= 30:
                if mini_board[0][number % 10] == '-':
                    mini_board[0][number % 10] = ''
                mini_board[0][number % 10] += (player.get_symbol())
            elif number < 40:
                if mini_board[number % 10][10] == '-':
                    mini_board[number % 10][10] = ''
                mini_board[number % 10][10] += (player.get_symbol())
            else:
                print("Landed on Type not yet programmed!\n")
        
        for i, e in enumerate(mini_board):
            print(e)
        print("\n")
    
    # Alternative styling.
    # def property_owner(self, board, players, property_index):
    #     for player in players:
    #         if player.owns_property(board, property_index):
    #             return player
    #     return "UNOWNED PROPERTY"

    def run(self, players, board):
        while(not players[0].is_bankrupt() and not players[1].is_bankrupt()):
            print("-----------------------")
            print("\tTurn", self.gametime, ":")
            print("-----------------------")
            # TODO: Add trade / mortgage phase here!
            # current_player.get_actions()

            sum_die = self.roll_dice()
            current_player = self.get_current_player(players)
            # TODO: check for mortgage and trades
            # current_player.get_actions()

            self.move_player(current_player, sum_die)
            print(f"\n{current_player.get_symbol()} rolled ({sum_die}) to {board[current_player.position][2]}\n")
            self.print_board(players)

            if board[current_player.position][0] == 0:
                self.land_on_type0(current_player, board)
            elif board[current_player.position][0] == 1:
                self.land_on_type1(current_player, board)
            # elif board[current_player.position][0] == 2:
            #     self.land_on_type1(current_player, board)
            else:
                print("Something went went wrong with our types\n")
        
            # TODO: Add trade / mortgage phase here as well!
            # current_player.get_actions()
            for player in players:
                print(player.symbol, "money:", player.get_money())
            print("\n")

            for i,e in enumerate(self.owner_list):
                if e is not 0 and e is not -1:
                    print(f"{board[i][2]} [{i}] - owned by {e.symbol}")
            print("\n")
        
            self.gametime += 1


if __name__ == "__main__":
    game = Game()
    game.run(game.players, game.board)

    # print("Outcome of Game: ", status)