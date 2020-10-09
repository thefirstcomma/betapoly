import gym


env = gym.make('gym_monopoly:monopoly-v0')
env.reset()

for _ in range(1000):
    env.render()
    players = env.get_players()
    for player in players:
        if player == 'ai':
            action = [0, 1, None, None]
            obs, reward, done, _ = env.step(env.action_space.sample()) # take a random action
        else:
            env.human_step() -> input()
env.close()