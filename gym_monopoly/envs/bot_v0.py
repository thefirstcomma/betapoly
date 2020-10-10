import gym


env = gym.make('gym_monopoly:monopoly-v0')
env.reset()

for _ in range(1000):
    players = env.get_players()
    if player == 'ai':
        # action - [0, 1, None, None]
        action = create_action()
        obs, reward, done, _ = env.step(env.action_space.sample()) # take a random action
    else:
        env.human_step()
    env.render()
env.close()

def create_action(obs):
    pass


for _ in range(1000):
    obs = None
    ply = [ai1, ai2, per1, per2]
    current_player = obs[next_player]
    action = current_player.get_action(prev_obs)
    obs, done, reward, etc = step(action)
    env.render()
env.close()
