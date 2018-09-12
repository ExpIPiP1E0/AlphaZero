#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class EnviromentUtilities(object):
    
    DIR=((-1,0),(-1,+1),(0,+1),(+1,+1), \
         (+1,0),(+1,-1),(0,-1),(-1,-1))
    
    ###########################################################################
    def __init__(self,n):
        self.n=n
        self.n_x=n
        self.n_y=n
    
    
    ###########################################################################
    def get_initial_state(self):
        state=np.zeros(shape=(self.n,self.n),dtype=np.int)
        
        mid_x=self.n_x//2 #切り捨て．但し，Pythonの添え字の関係上，これで遠い方になる．奇数でも同じ.
        mid_y=self.n_y//2
        
        state[mid_x,mid_y]=1
        state[mid_x-1,mid_y-1]=1
        state[mid_x-1,mid_y]=-1
        state[mid_x,mid_y-1]=-1
        
        return state
    
    
    ###########################################################################
    def get_state_size(self):
        return (self.n,self.n)
    
    
    ###########################################################################
    def get_action_size(self):
        return self.n*self.n+1 #+1はスキップ用
    
    
    ###########################################################################
    def get_valid_actions(self,state,player):
        valids=np.zeros(self.get_action_size(),dtype=np.int)
        emp=np.where(state==0)
        flag=False
        for i in range(len(emp[0])):
            pos=(emp[0][i],emp[1][i]) #(x,y)形式に変換
            if self.is_available(state,player,pos):
                valids[self.n_y*pos[0]+pos[1]]=1
                flag=True
                
        valids[-1]= 0 if flag==True else 1
        
        return valids
    
    
    ###########################################################################
    def get_next_state(self,state,player,action):
        #スキップの場合
        if action==self.n*self.n:
            return(state,-player)
        
        pos=[action//self.n_y,action%self.n_y]
        return self.get_next_state_pos(state,player,pos)
    
    
    ###########################################################################
    def get_ended(self,state,player):
        if self.has_valid_actions(state,player):
            return 0
        
        if self.has_valid_actions(state,-player):
            return 0
        
        if self.get_score(state,player)>0:
            return 1
        else:
            return -1
    
    
    ###########################################################################
    def get_canonical_form(self,state,player):
        return state*player
    
    
    ###########################################################################
    def get_symmetries(self,state,pi):
        '''
        generate augumented experience on state and action symmetry
        '''
        pi_square=np.reshape(pi[:-1],(self.n,self.n))
        sym=[]
        for i in range(1,5):
            for j in [True,False]:
                new_state=np.rot90(state,i)
                new_pi_square=np.rot90(pi_square,i)
                if j:
                    new_state=np.fliplr(new_state)
                    new_pi_square=np.fliplr(new_pi_square)
                sym.append([new_state,list(new_pi_square.ravel())+([pi[-1]])])
        
        return sym
    
    
    ###########################################################################
    def get_string_representation(self,state):
        #print(state)
        return state.tostring() #このメソッドはNDArrayに最初から入っているメソッド．
    
    
    ###########################################################################
    def get_score(self,state,player):
        return np.sum(state==player)-np.sum(state==player*-1)
    
    
    ###########################################################################
    def has_valid_actions(self,state,player):
            return self.get_valid_actions(state,player)[-1]==0
        
        
    ###########################################################################
    def is_available(self,state,player,pos):
        if state[pos[0],pos[1]]!=0:
            return False
        
        for dx,dy in EnviromentUtilities.DIR:
            x=pos[0] ; y=pos[1]
            flag=False
            while 0<=x<self.n_x and 0<=y<self.n_y:
                x+=dx ; y+=dy
                if 0<=x<self.n_x and 0<=y<self.n_y and state[x,y]==-player:
                    flag=True
                elif not(0<=x<self.n_x and 0<=y<self.n_y) \
                     or (flag==False and state[x,y]!=-player) \
                     or state[x,y]==0:
                    break
                elif state[x,y]==player and flag==True:
                    return True
        return False
    
    
    ###########################################################################
    def get_next_state_pos(self,state,player,pos):
        if self.is_available(state,player,pos)==False:
            return False,-player
        
        next_state=np.copy(state)
        next_state[pos[0],pos[1]]=player
        for dx,dy in EnviromentUtilities.DIR:
            tmp_next_state=np.copy(next_state)
            x=pos[0] ; y=pos[1]
            flag=False
            while 0<=x<self.n_x and 0<=y<self.n_y:
                x+=dx ; y+=dy
                if 0<=x<self.n_x and 0<=y<self.n_y and next_state[x,y]==-player:
                    flag=True
                    tmp_next_state[x,y]=player
                elif not(0<=x<self.n_x and 0<=y<self.n_y) \
                     or (flag==False and next_state[x,y]!=-player) \
                     or state[x,y]==0:
                    break
                elif next_state[x,y]==player and flag==True:
                    next_state=tmp_next_state
                    break

        return next_state,-player


    ###########################################################################
    def display(self,state):
        n=state.shape[0]
        
        #フィールド部分を表示
        f='  |0|'
        for y in range(1,n):
            f+=str(y)+'|'
        print(f)    
        print('-----------------')
        
        #行部分およびボード本体を表示．
        for y in range(n):
            print(y,'|',end='')
            for x in range(n):
                piece=state[y][x]
                if piece==1: print('b ',end='')
                elif piece==-1: print('w ',end='')
                else:
                    print('- ',end='')
            print('|')
        print('-----------------')
        print('\n\n\n')
        

###############################################################################

#以下，デバッグ用
if __name__=='__main__':
    env_utils=EnviromentUtilities(6)
    state=env_utils.get_initial_state()
    print(state)
    
    print(env_utils.get_valid_actions(state,1)[:-1].reshape((6,6)))
    
    next_state,next_player=env_utils.get_next_state_pos(state,1,(1,3))
    #print(next_state)
    
    #print(env_utils.is_available(state,1,(0,0)))
