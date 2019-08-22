#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

###############################################################################
class RandomPlayer(object):
    '''
    ランダムプレイヤー
    '''
    def __init__(self, env):
        self.env = env
        
    def play(self, canonical_state):
        valids=self.env.get_valid_actions()
        a=np.random.choice(range(self.env.get_action_size()), p=valids/valids.sum())
        return a
    
    
###############################################################################
class HumanPlayer(object):
    '''
    人間プレイヤー
    '''
    def __init__(self, env):
        self.env = env
    
    
    def play(self, canonical_state):
        valids=self.env.get_valid_actions()
        #全ての合法手を表示する
        print('all valid moves')
        for i in range(len(valids)):
            if valids[i]==1:
                print(int(i/self.env.get_state_size()[1]),
                      int(i%self.env.get_state_size()[1]))
        
        #入力受付
        while True:
            a=input()
            try:
                x, y = [int(x) for x in a.split(' ')] #x y形式で入力
            except:
                print('Invalid input')
                continue
            a = self.env.get_state_size()[1]*x+y if x!=-1 else self.env.get_action_size()-1

            try:
                if valids[a]:
                    break
                else:
                    print('Invalid action')
            except:
                print('Invalid action')
                
                
        return a
            

###############################################################################
class GreedyPlayer(object):
    '''
    グリーディプレイヤー
    '''
    def __init__(self,env,env_utils):
        self.env=env
        self.env_utils=env_utils
        
        
    def play(self,canonical_state):
        valids=self.env.get_valid_actions()
        
        max_a=-1
        max_score=-float('inf')
        
        for a in range(len(valids)):
            if valids[a]==0:
                continue
            next_state,next_player=self.env_utils.get_next_state(self.env.state,self.env.player,a)
            score=self.env_utils.get_score(next_state,self.env.player)
            
            if max_score<score:
                max_score=score
                max_a=a
            
        return max_a
    

###############################################################################
class AntiGreedyPlayer(object):
    '''
    逆グリーディプレイヤー
    '''
    def __init__(self, env, env_utils):
        self.env=env
        self.env_utils=env_utils
        
        
    def play(self, canonical_state):
        valids=self.env.get_valid_actions()
        
        min_a=-1
        min_score=float('inf')
        
        for a in range(len(valids)):
            if valids[a]==0:
                continue
            next_state,next_player=self.env_utils.get_next_state(self.env.state,self.env.player,a)
            score=self.env_utils.get_score(next_state,self.env.player)
            
            if min_score>score:
                min_score=score
                min_a=a
            
        return min_a
    
    
###############################################################################
class CompositeGreedyPlayer(object):
    '''
    前半逆グリーディで後半グリーディ
    '''
    def __init__(self,env,env_utils):
        self.env=env
        self.env_utils=env_utils
        
        
    def play(self, canonical_state):
        valids=self.env.get_valid_actions()
        
        if np.sum(self.env.state!=0)<=self.env.get_action_size()//2:
            min_a=-1
            min_score=float('inf')
            
            for a in range(len(valids)):
                if valids[a]==0:
                    continue
                next_state,next_player=self.env_utils.get_next_state(self.env.state,self.env.player,a)
                score=self.env_utils.get_score(next_state,self.env.player)
                
                if min_score>score:
                    min_score=score
                    min_a=a
                
            return min_a
        
        else:
            max_a=-1
            max_score=-float('inf')
            
            for a in range(len(valids)):
                if valids[a]==0:
                    continue
                next_state,next_player=self.env_utils.get_next_state(self.env.state,self.env.player,a)
                score=self.env_utils.get_score(next_state,self.env.player)
                
                if max_score<score:
                    max_score=score
                    max_a=a
                
            return max_a    
