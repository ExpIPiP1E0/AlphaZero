#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 20:50:35 2018

@author: RyoMiyazaki
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Arena import Arena

from EnviromentUtilities import EnviromentUtilities
from Enviroment import Enviroment

from MCTS import MCTS

from Model import ModelSystem

from Players import *


import numpy as np
from utils import *


###############################################################################
env_utils=EnviromentUtilities(6)
env=Enviroment(env_utils)


###############################################################################
rp=RandomPlayer(env).play
gp=GreedyPlayer(env,env_utils).play
agp=AntiGreedyPlayer(env,env_utils).play
cgp=CompositeGreedyPlayer(env,env_utils).play

ms1=ModelSystem(env)
ms1.load_checkpoint('temp','best.pth.tar')
args1=dotdict({'num_MCTS':25,'cpuct':1.0,'dirichlet_eps':0.0})
mcts1=MCTS(env_utils,ms1,args1) #MCTSはnum_MCTS,dirichlet_epsしか参照しない．
azp1=lambda x:np.argmax(mcts1.get_action_prob(x,temp=0)) #AlphaZero

#Name,Player Instance, Is Stochastic
players=[('RandomPlayer',rp,1),
         ('GreedyPlayer',gp,0),
         ('AntiGreedyPlayer',agp,0),
         ('CompositeGreedyPlayer',cgp,0),
         ('mini-AlphaZero',azp1,1)]


###############################################################################
num_trial=100

results=np.zeros(shape=(len(players),len(players)))

for i in range(len(players)):
    for j in range(len(players))[0:i+1]:
        arena=Arena(player1=players[i][1],player2=players[j][1],env=env,display=None)
        
        actual_num_trial=2 if (players[i][2]==0 and players[j][2]==0) else num_trial #playerが両方とも決定論的な場合は2回で済ます．
        
        one_win,two_win,draw=arena.play_games(actual_num_trial,verbose=False)
        print(players[i][0],' vs ',players[j][0],' : ',one_win/float(actual_num_trial),' wins.')
        results[i,j]=one_win/float(actual_num_trial)
        

###############################################################################
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.DataFrame(results,index=[x[0] for x in players],columns=[x[0] for x in players])

plt.figure(figsize=(10,10))
sns.heatmap(df,annot=True)
plt.show()

df.to_csv('cross_performance.csv')

###############################################################################
#MCTS Power test
mcts_trials=np.array([2,5,10,20,40,80,128],dtype='int')
mcts_results=np.zeros(len(mcts_trials))

for i in range(len(mcts_trials)):
    ms1=ModelSystem(env)
    ms1.load_checkpoint('temp','best.pth.tar')
    args1=dotdict({'num_MCTS':mcts_trials[i],'cpuct':1.0,'dirichlet_eps':0.0})
    mcts1=MCTS(env_utils,ms1,args1) 
    azp1=lambda x:np.argmax(mcts1.get_action_prob(x,temp=0))
    
    arena=Arena(player1=azp1,player2=rp,env=env,display=None)
        
    actual_num_trial=100
        
    one_win,two_win,draw=arena.play_games(actual_num_trial,verbose=False)
    print('AlphaZero at MCTS ',mcts_trials[i],' vs RandomPlayer : ',one_win/float(actual_num_trial),' wins.')
    mcts_results[i]=one_win/float(actual_num_trial)

    
plt.plot(mcts_trials,mcts_results)
plt.show()

df_mcts_num=pd.DataFrame(np.array([mcts_trials,mcts_results]).T,
                         columns=['num_MCTS','winning ratio'])
df_mcts_num.to_csv('mcts_num_performance.csv')












