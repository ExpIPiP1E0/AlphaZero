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
#class HumanPlayer(object):
#Not implemented yet.
