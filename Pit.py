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

rp=RandomPlayer(env).play
#gp=GreedyPlayer(env).play
hp=HumanPlayer(env).play

ms1=ModelSystem(env)
ms1.load_checkpoint('temp','checkpoint_88.pth.tar')
args1=dotdict({'num_MCTS':128,'cpuct':1.0,'dirichlet_eps':0.0})
mcts1=MCTS(env_utils,ms1,args1) #MCTSはnum_MCTS,dirichlet_epsしか参照しない．

azp1=lambda x:np.argmax(mcts1.get_action_prob(x,temp=0)) #AlphaZero

arena=Arena(player1=rp,player2=azp1,env=env,display=None)

print(arena.play_games(10,verbose=True))





