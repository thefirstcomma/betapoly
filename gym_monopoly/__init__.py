from gym.envs.registration import register

register(
    id='monopoly-v0',
    entry_point='gym_monopoly.envs:MonopolyEnv',
)
register(
    id='monopoly-extrahard-v0',
    entry_point='gym_monopoly.envs:MonopolyExtraHardEnv',
)