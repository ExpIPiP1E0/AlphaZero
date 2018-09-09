#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

###############################################################################
class RandomPlayer(object):
    '''
    ランダムプレイヤー
    '''
    def __init__(self,env):
        self.env=env
        
    def play(self,canonical_state):
        valids=self.env.get_valid_actions()
        a=np.random.choice(range(self.env.get_action_size()),p=valids/valids.sum())
        return a
    
    
###############################################################################
class HumanPlayer(object):
    '''
    人間プレイヤー
    '''
    def __init__(self,env):
        self.inner_env=env
    
    
    def play(slef,state,player):
        valids=self.inner_env.action_space.valid(state,player)
        #全ての合法手を表示する
        
        #入力受付
        while Ture:
            a=input()
            x,y=[int(x) for x in a.split(' ')] #x y形式で入力
            

###############################################################################
class GreedyPlayer(object):
    '''
    グリーディプレイヤー
    '''
    











