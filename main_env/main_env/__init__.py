from gymnasium.envs.registration import register

register(
     id="main_env/AuctionEnv-v0",
     entry_point="main_env.envs:AuctionEnv",
     max_episode_steps=24,
)