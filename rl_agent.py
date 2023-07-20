from main_env.envs.auction_env import AuctionEnv
from pettingzoo.test import parallel_api_test

if __name__ == "__main__":
    env = AuctionEnv()
    # env.reset()
    # a=set(env.agents[:])
    # print('l', a)
    parallel_api_test(env, num_cycles=1000000)
    