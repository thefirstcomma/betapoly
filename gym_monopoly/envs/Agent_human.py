
class Agent_human:
    def __init__(self):
        pass


    def valid_action(action_type):
    	if action_type == 'BUY_PROPERTY_LANDED':
    		return True
        elif action_type == 'IN_JAIL_ACTION':
            return True
        elif action_type == 'CONTINUE_AUCTION':
            return True
        elif action_type == 'ACCEPT_TRADE':
            return True
        elif action_type == 'MORTGAGE':
            return True
        elif action_type == 'UNMORTGAGE':
            return True
        elif action_type == 'TRADE':
            return True
        elif action_type == 'BUY_HOUSE':
            return True
        elif action_type == 'SELL_HOUSE':
            return True
        elif action_type == 'END':
        	return True
        elif action_type == 'ROLL-DICE':
            return True
        else:
            print('Unrecognized action %d' % action_type)

    def set_action_type()


    def get_action(prevobs):
    	is_valid = False
    	print("Choose actions: \n")
    	print("BUY_PROPERTY_LANDED (BP), \n IN_JAIL_ACTION (JA), \n CONTINUE_AUCTION (CA), \n ")
    	print("ACCEPT_TRADE (AT), \n MORTGAGE (M), \n UNMORTGAGE (U), \n TRADE (T), \n BUY_HOUSE (B), \n")
    	print("SELL_HOUSE (S), \n END (E), \n ROLL-DICE (R), \n")
    	while is_valid:
    		action_input = input("Enter Action: ")
    		is_valid = valid_action(action_input)
    	action = [None]*14
    	action[0] = action_input

    	if action == 

        
