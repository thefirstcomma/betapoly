
class Agent_human:
    def __init__(self, player_number):
        self.player_number = player_number
        print("Created Player", self.player_number)
        
    def set_action_type(self):
        pass

    def get_action(self, obs):
        NUMBER_OF_ACTIONS = 66
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
    #     8 : TRADE MONEY YOU GIVE
    #     9 : TRADE MONEY YOU TAKE
    #     10 : AUCTION AMOUNT
    #     11 : ACCEPT_TRADE
    #     12-37: YOUR PROPERTY OFFERS
    #     38-63: ENEMY PROPERTY WANTS
    #     64: TRADER INITIATOR UNMORTGAGE PROPERTY RIGHT AWAY [0,1]
    #     65: TRADER DECISION UNMORTGAGE PROPERTY RIGHT AWAY [0,1]
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
                action[1] = 2
        elif action_input == 'CONTINUE_AUCTION' or action_input == 'CA':
            action[0] = 2
            output = input(f"The highest bid is ${obs[7]}. Input an integer for how much you want to bid: ")
            action[10] = int(output)
        elif action_input == 'ACCEPT_TRADE' or action_input == 'AT':
            action[0] = 3
            output = input("Do you accept the trade YES or NO (Y/N)")
            output = output.upper()
            if output == 'YES' or output == 'Y':
                action[11] = 1
            elif output == 'NO' or output == 'N':
                action[11] = 0
            else:
                print(f"{output} is an Invalid Input")
            output = input("Do you unmortgage properties you recieve right away YES or NO (Y/N)?")
            output = output.upper()
            if output == 'YES' or output == 'Y':
                action[65] = 1
            elif output == 'NO' or output == 'N':
                action[65] = 0
            else:
                print(f"{output} is an Invalid Input")
        elif action_input == 'MORTGAGE' or action_input == 'M':
            action[0] = 4
            output = input("Put in the integer of the property you want to Mortgage: ")
            action[5] = int(output)
        elif action_input == 'UNMORTGAGE' or action_input == 'U':
            action[0] = 5
            output = input("Put in the integer of the property you want to Unmortgage: ")
            action[6] = int(output)
        elif action_input == 'TRADE' or action_input == 'T':
            action[0] = 6
            output = input("What player do you want to trade with (1, 2, 3, 4): ")
            action[7] = int(output)
            output = input("How much money are you offering: ")
            action[8] = int(output)
            output = input("How much money are you recieving: ")
            action[9] = int(output)
            output = input("What properties are you offering: ")
            tmp = output.split(' ')
            if not tmp == ['']:
                tmp = list(map(int, tmp))
            prop = [1, 3, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 18, 19, 21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 34, 35, 37, 39]
            for i in range(0, 26):
                action[i+12] = 0
                if prop[i] in tmp:
                    action[i+12] += 1
            output = input("What properties do you want to recieve: ")
            tmp = output.split(' ')
            if not tmp == ['']:
                tmp = list(map(int, tmp))
            for i in range(0, 26):
                action[i+38] = 0
                if prop[i] in tmp:
                    action[i+38] += 1
            output = input("Do you unmortgage properties you recieve right away YES or NO (Y/N)?")
            output = output.upper()
            if output == 'YES' or output == 'Y':
                action[64] = 1
            elif output == 'NO' or output == 'N':
                action[64] = 0
            else:
                print(f"{output} is an INVALID input")
        elif action_input == 'BUY_HOUSE'or action_input == 'B':
            action[0] = 7
            house_number = input("What House do you want to buy? (House Number)")
            action[3] = int(house_number)
        elif action_input == 'SELL_HOUSE' or action_input == 'S':
            action[0] = 8
            house_number = input("What House do you want to sell? (House Number)")
            action[4] = int(house_number)
        elif action_input == 'END' or action_input == 'E':
        	action[0]= 9
        elif action_input == 'ROLL-DICE' or action_input == 'R':
            action[0] = 10
        else:
            print("Incorrect prompt at Agent_human!!!!")
        
        return action

        