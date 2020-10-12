import gym
import Agent_ai
import Agent_human

env = gym.make('gym_monopoly:monopoly-v0')
obs = env.reset()

for _ in range(1000):
    agents = [Agent_human(), Agent_human(), Agent_human(), Agent_human()]
    current_agent = agents[obs[1]]
    action = current_agent.get_action(obs)
    obs, done, reward, _ = env.step(action)
    if done:
        env.reset()
        break
    env.render()
env.close()
