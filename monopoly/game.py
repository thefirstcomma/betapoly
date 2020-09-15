import random
import time
import player
import human_player
import board_info
import chance
import comm_chest


# Turn 1:
#     actions() -> [List]
#     rolldie()
#         -buy_property_landed_on()
#             -possible_auction()
#             -actions() -> [List]
#         -possible_pay_rent()
        
#         actions() -> [List]


class Game:

    def __init__(self):
        self.board = board_info.BOARD
        self.p1 = Player("[P1]")
        self.p2 = Player("[P2]")
        self.gametime = 0
        self.players = [self.p1, self.p2]
        # -1 == not buyable, 0 == buyable
        self.owner_list = [-1, 0, -1, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, -1, 0]

    def roll_dice(self):
        return random.randint(1,6) + random.randint(1,6)
    
    def move_player(self, player, sum_die):
        player.position += sum_die
        if (player.position >= 40):
            player.position = player.position % 40
            player.money += 200
    
    def run(self):
        while(not self.players[0].is_bankrupt() and not self.players[1].is_bankrupt()):
            sum_die = self.roll_dice()
            current_player = self.get_current_player()
            # check for mortgage and trades

            self.move_player(current_player, sum_die)
            print("\n\n", current_player.get_symbol() + " rolled: ", sum_die)
            self.print_board(self.players)

            # if player moved to board of type 0
            if self.board[current_player.position][0] == 0:
                self.land_on_type0(current_player, self.board)
            # elif self.board[current_player.position][0] == 1:
            #     self.land_on_type1(current_player)
            # elif self.board[current_player.position][0] == 2:
            #     self.land_on_type2(current_player)
            # elif self.board[current_player.position][0] == 3:
            #     self.land_on_type3(current_player)
            # elif self.board[current_player.position][0] == 4:
            #     self.land_on_type4(current_player)
            # elif self.board[current_player.position][0] == 5:
            #     self.land_on_type5(current_player)
            # elif self.board[current_player.position][0] == 6:
            #     self.land_on_type6(current_player)
            # elif self.board[current_player.position][0] == 7:
            #     self.land_on_type7(current_player)
            else:
                print("Something went went wrong with our types\n")
                
            for player in self.players:
                print(player.symbol,  " money: ", player.get_money())
            print("\n")

            for i,e in enumerate(self.owner_list):
                if e is not 0 and e is not -1:
                    print("Location ", i, " owned by", e.symbol)
        
            self.gametime += 1
    

    # Auctions, Houses/Hotels
    # FIX ME!!!!!!! LOTS OF CHANGES NEEDED
    def land_on_type0(self, current_player, board):
        # curr_property_owner = self.property_owner(self.board, self.players, current_player.position)
        curr_property_owner = self.owner_list[current_player.position]
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == 0:
            action = input("Does " + current_player.symbol + " buy the " + board[current_player.position][3] + " property named: " + board[current_player.position][2] + " (Y/N)\n")
            assert(action == "Y" or action == "N")
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-board[current_player.position][1])
                self.owner_list[current_player.position] = current_player
                print(current_player.symbol, " s MONEY NOW: ", current_player.money)
                print(current_player.symbol, " bought the ", board[current_player.position][3] , " property named: ", board[current_player.position][2])
            else:
                # auctions
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
            current_player.update_money(-board[current_player.position][4])
            curr_property_owner.update_money(board[current_player.position][4])
            print(current_player.symbol, " paid rent of ", board[current_player.position][4], " to ", curr_property_owner.symbol)
    
    def land_on_type1(self, current_player, board):
        curr_property_owner = self.property_owner(self.players, current_player.position)
        if curr_property_owner == current_player:
            pass
        elif curr_property_owner == "UNOWNED PROPERTY":
            action = input("Does " + current_player.symbol + " buy the " + board[current_player.position][3] + " property named: " + board[current_player.position][2] + " (Y/N)\n")
            assert(action == "Y" or action == "N")
            if action == "y" or action == "Y":
                current_player.property_in_use.append(current_player.position)
                current_player.update_money(-board[current_player.position][1])
                print(current_player.symbol, " s MONEY NOW: ", current_player.money)
                print(current_player.symbol, " bought the ", board[current_player.position][3] , " property named: ", board[current_player.position][2])
            else:
                # auctions
                self.auction_phase()
        else:
            # Assuming no houses/hotel is bought
            current_player.update_money(-board[current_player.position][4])
            curr_property_owner.update_money(board[current_player.position][4])
            print(current_player.symbol, " paid rent of ", board[current_player.position][4], " to ", curr_property_owner.symbol)

    def land_on_type2(self, current_player):
        pass

    def land_on_type3(self, current_player):
        pass

    def land_on_type4(self, current_player):
        pass

    def land_on_type5(self, current_player):
        pass
    
    def land_on_type6(self, current_player):
        pass

    def land_on_type7(self, current_player):
        pass

    def auction_phase(self):
        pass

    # Only works for 2 players right now
    def get_current_player(self):
        return self.p1 if self.gametime % 2 == 0 else self.p2

    def property_owner(self, board, players, property_index):
        for player in players:
            if player.owns_property(board, property_index):
                return player
        return "UNOWNED PROPERTY"
            
    def print_board(self, players):
        tmp = [ ["F.P.", "-", "-", "-", "-", "-", "-", "-", "-", "-", "G.T.J"],
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

        # For pretty print
        for player in players:
            number = player.position
            if number <= 10:
                if tmp[10][10 - number] == '-':
                    tmp[10][10 - number] = ''
                tmp[10][10 - number] += (player.get_symbol())
            elif number <= 20:
                if tmp[10-(number % 10)][0] == '-':
                    tmp[10-(number % 10)][0] = ''
                tmp[10-(number % 10)][0] += (player.get_symbol())
            elif number <= 30:
                if tmp[0][number % 10] == '-':
                    tmp[0][number % 10] = ''
                tmp[0][number % 10] += (player.get_symbol())
            elif number < 40:
                if tmp[number % 10][10] == '-':
                    tmp[number % 10][10] = ''
                tmp[number % 10][10] += (player.get_symbol())
            else:
                print("Something really really went wrong!")
            
        
        for i,e in enumerate(tmp):
            print(e)
            
        print("\n")



if __name__ == "__main__":
    game = Game()

    ending = True
    game.run()

    # print("Outcome of Game: ", status)