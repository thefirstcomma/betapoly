
class Agent_human:
    def __init__(self, player_number):
        self.player_number = player_number
        print("Created Player", self.player_number)
        
    def set_action_type(self):
        pass

    def get_action(self, obs):
        NUMBER_OF_ACTIONS = 14
        print("Current Player turn Player", self.player_number)
        print("Choose actions: \n")
        print("BUY_PROPERTY_LANDED (BP), \n IN_JAIL_ACTION (JA), \n CONTINUE_AUCTION (CA), \n ")
        print("ACCEPT_TRADE (AT), \n MORTGAGE (M), \n UNMORTGAGE (U), \n TRADE (T), \n BUY_HOUSE (B), \n")
        print("SELL_HOUSE (S), \n END (E), \n ROLL-DICE (R), \n")
        action_input = input("Enter Action: ")
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
    

        if action_input == 'BUY_PROPERTY_LANDED' or action_input == 'BP':
            action[0] = 0
        elif action_input == 'IN_JAIL_ACTION' or action_input == 'JA':
            action[0] = 1
            if output.upper() == 'ROLL_DOUBLE':
                action[1] = 1
            elif output.upper() == 'PAY_50':
                action[1] = 0
            elif output.upper() == 'USE_CARD':
                acton[1] = 2
        elif action_input == 'CONTINUE_AUCTION' or action_input == 'CA':
            pass
        elif action_input == 'ACCEPT_TRADE' or action_input == 'AT':
            pass
        elif action_input == 'MORTGAGE' or action_input == 'M':
            pass
        elif action_input == 'UNMORTGAGE' or action_input == 'U':
            pass
        elif action_input == 'TRADE' or action_input == 'T':
            pass
        elif action_input == 'BUY_HOUSE'or action_input == 'B':
            pass
        elif action_input == 'SELL_HOUSE' or action_input == 'S':
            pass
        elif action_input == 'END' or action_input == 'E':
        	action[0]= 9
        elif action_input == 'ROLL-DICE' or action_input == 'R':
            action[0] = 10
        else:
            print("YOU SUCK!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        return action

        
