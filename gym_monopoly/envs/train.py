import gym
from gym_monopoly.envs.Agent_human import Agent_human

env = gym.make('gym_monopoly:monopoly-v0')
obs = env.reset()
a1 = Agent_human(1)
a2 = Agent_human(2)
a3 = Agent_human(3)
a4 = Agent_human(4)
agents = [a1, a2, a3, a4]

for _ in range(10000):
    current_agent = agents[obs[1].player_number-1]
    action = current_agent.get_action(obs)
    obs, reward, done, _ = env.step(action)
    # print(obs, reward, done)
    if done:
        env.reset()
        break
    env.render()
env.close()
