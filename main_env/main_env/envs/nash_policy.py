from auction_env import AuctionEnv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
# np.random.seed(10)
def Nash_policy(state,agent,timestep,total_timestep):
    
    ask_price = state["ask_price"]
    ask_qty = state["ask_qty"]
    # print(ask_price,ask_qty,"Prices and quantity")
    requirements = state["reqs"]
    # print(" no asks", len(ask_price), "total_supply", sum(ask_qty))
    # print("requirements",requirements)
    num_agents = len(requirements)
    QDh = sum(requirements)
    QDh_Qbh = QDh - requirements
    # print("QDh-Qbh",QDh_Qbh)
    qty = 0
    pvh = np.zeros(num_agents)
    flags = np.zeros(num_agents)

    for index,ask in enumerate(zip(ask_price,ask_qty)):
        qty += ask[1]
        
        for agt in range(num_agents):
            if QDh_Qbh[agt] < qty and not flags[agt]:
                pvh[agt] = ask[0] 
                flags[agt] = 1
            
        
        if QDh <= qty:
            puh = ask[0]
            break
    # print("index",index)
    # print(puh,ask_price[index],sum(ask_qty[:index+1]))
    # print(total_timestep,timestep)
    v0h = max(0,index - (total_timestep - 1 - timestep))
    pv0h = ask_price[v0h]
    # print("pvh",pvh)
    # print("pv0h",pv0h)

    quant_inx = sorted(range(len(requirements)), key=lambda k:requirements[k], reverse=True)
    requirements_sorted = [requirements[i] for i in quant_inx]
    pvh_sorted = [pvh[i] for i in quant_inx]
    
    # print("requirements_sorted",requirements_sorted)
    # print("pvh_sorted",pvh_sorted)
    # for ind,reqs in enumerate(requirements_sorted):
    #     if pv0h < 

    if pv0h <= pvh_sorted[0]:
        pzh = pvh_sorted[0]
        if agent == quant_inx[0]:
            bid_price = pzh
        else:
            bid_price = "pmax"
    else:
        pzh = pv0h
        for s_ind in range(num_agents):
            if pv0h > pvh_sorted[s_ind]:
                break
        agt = quant_inx[s_ind-1]
        if agent == agt:
            bid_price = pzh
        else:
            bid_price = "pmax"
    
    # print("bid price",bid_price)
    return bid_price,requirements[agent]

def Nash_policy2(state,agent):
    ask_price = state["ask_price"]
    ask_qty = state["ask_qty"]
    requirements = state['reqs']
    QDh_Qbh = sum(requirements) - requirements[agent]
    flag = 0

    if agent == min(requirements):
        for index,ask in enumerate(zip(ask_price,ask_qty)):
            qty += ask[1]

            if QDh_Qbh < qty and not flag:
                pvh = ask[0] 
                flag = 1
                
            if QDh < qty:
                puh = ask[0]
                break
        


def ZI_policy(state,agent):
    requirements = state["reqs"]
    bid_price = np.random.uniform(1,50)
    # bid_qty = np.random.uniform(30,requirements[agent])
    bid_qty = requirements[agent]
    return bid_price,bid_qty

def ZIP_policy():
    pass


def simulation(deviation = 0,num_agents = 3,bid_price_in = 0, ZI = False):
    env = AuctionEnv() 
    episodes = 1
    scores = {i : [] for i in env.agents}
    score = {i : 0 for i in env.agents}
    non_deviating = list(range(0,num_agents)) 
    if deviation != None:
        non_deviating.remove(deviation)
        # print(non_deviating,"non deviating")

    for episode in range(episodes):
        # print("episode")
        states, _ = env.reset()
        env.timestep = 23
        # if episode % 11 == 0:
        #     env.timestep = 22
        
        # if episode % 13 == 0:
        #     env.timestep = 23
        
        state = states[0]
        requirements2 = state["reqs"].copy()
        # print("requirements2",requirements2,"episode",episode)
        while True:     
            actions = {}
            # print(env.agents)
            for agent in range(num_agents):
                # print(env.agents)
                if agent in env.agents:
                    if agent in non_deviating:
                        # print("timestep",env.timestep)
                        bid_price, bid_qty = Nash_policy(states[agent],agent,env.timestep,env.horizon)
                        if bid_price == "pmax":
                            bid_price = env.max_bid_price
                        print("Nash policy",bid_price,bid_qty,"agent",agent)
                        actions[agent] = np.array([[bid_price,bid_qty]])
                    else:
                        if ZI:
                            
                            bid_price, bid_qty = ZI_policy(states[agent],agent)
                            actions[agent] = np.array([[bid_price,bid_qty]])
                            # print("ZI policy",bid_price,bid_qty,"agent",agent)
                        else:
                            # print(agent)
                            _, bid_qty = ZI_policy(states[agent],agent)
                            actions[agent] = np.array([[bid_price_in,bid_qty]])
                            print("prescribed policy",bid_price_in,bid_qty,"agent",agent)
        
            next_states,rewards,terminations,_,_ = env.step(actions)
            states = next_states
            for i in env.possible_agents:
                if i in rewards.keys():
                    score[i] = score[i] + rewards[i] 
           
            # print("rewards",rewards)
            # print("terminations",terminations)    
            if all(value == True for value in terminations.values()):
                for i in env.possible_agents:
                    score[i] = score[i]/requirements2[i]
                # print("score",score)
                for i in env.possible_agents:
                    scores[i].append(score[i])
                score = {i : 0 for i in env.possible_agents}
                break

        # print("------------------------------------")

    for i in env.possible_agents:
        scores[i] = sum(scores[i])/episodes
    # print("scores", scores)
    return scores
    


if __name__=="__main__":
    scores_all_play_Nash = simulation(deviation=None)
    scores_deviation = simulation(deviation=2,bid_price_in= 14, ZI = False)
    width = 0.25

    # print(scores_all_play_Nash)
    # print(scores_deviation)
    plt.rcParams.update({'font.size': 22})
    x_labels = ["P0","P1","P2"]
    plt.bar(np.array(list(scores_all_play_Nash.keys())),scores_all_play_Nash.values(),width,color='black')
    plt.bar(np.array(list(scores_deviation.keys()))+width,scores_deviation.values(),width,color='grey')
    plt.legend(['All players play MPNE','Player P2 deviates'])
    # plt.xlabel("Players")
    plt.ylabel("Value function")
    plt.tick_params(left = False, labelleft=False) 
    plt.xticks(list(range(3)),x_labels)
    plt.ylim([0, 1100])
    plt.show()