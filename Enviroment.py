#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from EnviromentUtilities import EnviromentUtilities


class Enviroment(object):
    def __init__(self,env_utils):
        self.env_utils=env_utils
        self.state=self.env_utils.get_initial_state()
        self.player=1
        
        
    def reset(self):
        self.state=self.env_utils.get_initial_state()
        self.player=1
        return self.state
        
        
    def step(self,action):
        self.state,self.player=self.env_utils.get_next_state(self.state,self.player,action)
        reward=self.env_utils.get_ended(self.state,self.player)
        return self.state,self.player,reward,reward!=0,None
    
    def get_state_size(self): #(n,n)
        return self.env_utils.get_state_size()
    
    
    def get_action_size(self): #n*n+1
        return self.env_utils.get_action_size()
    
    
    def get_ended(self,player=1):
        return self.env_utils.get_ended(self.state,player)
    
    
    def get_score(self,player):
        return self.env_utils.get_score(self.state,player)
    
    
    def get_canonical_state(self):
        return self.env_utils.get_canonical_form(self.state,self.player)
    
    
    def get_valid_actions(self):
        return self.env_utils.get_valid_actions(self.state,self.player)

    
    def display(self):
        self.env_utils.display(self.state)
    
    