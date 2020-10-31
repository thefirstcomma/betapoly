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

    def get_action(self, obs):
        pass