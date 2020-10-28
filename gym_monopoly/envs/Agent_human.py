
class Agent_human:
    def __init__(self, player_number):
        self.player_number = player_number
        print("Created Player", self.player_number)
        
    def set_action_type(self):
        pass

    def print_properties(self):
        print(f"\n{player.symbol} Properties: ")
        tmp = sorted(player.property_in_use + player.property_in_mort)
        for i in tmp:
            if player.check_property_index_for_houses(i):

                if i in player.property_in_mort:
                    print(f'{self.board[i][3]} - {self.board[i][2]} [{i}] - In Mortgage' + Style.RESET_ALL)
                else:
                    print(f'{self.board[i][3]} - {self.board[i][2]} [{i}]' + Style.RESET_ALL)
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

    def get_action(self, obs):
        NUMBER_OF_ACTIONS = 14
        print("-------------------------------")
        print(f"-------------- P{self.player_number} -------------")
        print("-------------------------------")
        print("BUY_PROP (BP), IN_JAIL_ACT (JA), Bid Auction(CA), TRADE (T),")
        print("ACCEPT_TRADE (AT), MORTGAGE (M), UNMORTGAGE (U), BUY_HOUSE (B),")
        print("SELL_HOUSE (S), END (E), ROLL-DICE (R)")
        action_input = input("Enter Action: ")
        action_input = action_input.upper()
        action = [None]* NUMBER_OF_ACTIONS

        # indexes of the list of action {
    #     0 : Type For ACTION_LOOKUP
    #     1 : PAY 50 FOR JAIL (0)/ ROLL DOUBLE (1)/ USE G.O.O.J CARD (2)
    #     2 : DONT BUY / BUY INDEX PROPERTY LANDED ON   [0,1]
    #     3 : BUY HOUSE ON THIS INDEX
    #     4 : SELL HOUSE ON THIS INDEX
    #     5 : MORTGAGE ON THIS INDEX
    #     6 : UN-MORTGAGE ON THIS INDEX
    #     7 : TRADE WITH PLAYER NUMBER
    #     8 : MONEY YOU GIVE
    #     9 : MONEY YOU TAKE
    #     10 : PROPERTY YOU GIVE
    #     11 : PROPERTY YOU GET
    #     12 : AUCTION AMOUNT # if == None or 0, quit auction
    #     13 : ACCEPT_TRADE
    # }

    # obs = [self.players, self.current_player, self.board, self.total_houses, self.total_hotels, self.rolled_double]
        current_player = obs[1]
    
        if action_input == 'BUY_PROPERTY_LANDED' or action_input == 'BP':
            action[0] = 0
            board = obs[2]
            buy_action_choice = input(f"Do you buy or auction {board[current_player.position]} (B/A)?")
            buy_action_choice = buy_action_choice.upper()
            if buy_action_choice == 'B':
                action[2] = 1
            elif buy_action_choice == 'A':
                action[2] = 0
            else:
                print("Buy or Auction command is invalid")
        elif action_input == 'IN_JAIL_ACTION' or action_input == 'JA':
            action[0] = 1
            output = input('Agent_human.py: What do you do ROLL_DOUBLE, PAY_50, or USE_CARD (R, P, U)? ')
            output = output.upper()
            if output.upper() == 'ROLL_DOUBLE' or output.upper() == 'R':
                action[1] = 0
            elif output.upper() == 'PAY_50' or output.upper() == 'P':
                action[1] = 1
            elif output.upper() == 'USE_CARD' or output.upper() == 'U':
                acton[1] = 2
        elif action_input == 'CONTINUE_AUCTION' or action_input == 'CA':
            action[0] = 2
            output = input(f"The highest bid is ${obs[7]}. Input an integer for how much you want to bid: ")
            action[10] = int(output)
        elif action_input == 'ACCEPT_TRADE' or action_input == 'AT':
            action[0] = 3
            pass
        elif action_input == 'MORTGAGE' or action_input == 'M':
            action[0] = 4
            output = input("Put in the integer of the property you want to Mortgage: ")
            action[5] = output
        elif action_input == 'UNMORTGAGE' or action_input == 'U':
            action[0] = 5
            output = input("Put in the integer of the property you want to Unmortgage: ")
            action[6] = output
        elif action_input == 'TRADE' or action_input == 'T':
            action[0] = 6
            output = input("What player do you want to trade with (1, 2, 3 , 4): ")
            action[7] = int(output)
            output = input("How much money are you going to pay the trade_partner for this trade: ")
            action[8] = int(output)
        elif action_input == 'BUY_HOUSE'or action_input == 'B':
            action[0] = 7
            house_number = input("What House do you want to buy? (House Number)")
        elif action_input == 'SELL_HOUSE' or action_input == 'S':
            action[0] = 8
            house_number = input("What House do you want to sell? (House Number)")
        elif action_input == 'END' or action_input == 'E':
        	action[0]= 9
        elif action_input == 'ROLL-DICE' or action_input == 'R':
            action[0] = 10
        else:
            print("Incorrect prompt at Agent_human!!!!")
        
        return action

        