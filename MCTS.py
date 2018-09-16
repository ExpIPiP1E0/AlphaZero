#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import math
import time
EPS=1e-8 #UCT計算時において，状態sへの訪問数が2のときのため．
#import cupy as cp


class MCTS(object):
    '''
    Model(s,a)<-MCTS(Model,s,a)
    s:string representation of enviroment (including player information)
    state:not including which player side
    '''
    def __init__(self,env_utils,model_system,args):
        self.env_model_utils=env_utils
        self.model_system=model_system
        self.args=args
        
        self.Qsa={} #行動価値関数Q(s,a)の推定値：nnetによる推定値とシミュレーションによる平均値
        self.Nsa={} #状態行動対(s,a)が訪問された回数
        self.Ns ={} #状態sが訪問された回数．UCT計算で使用．
        self.Ps ={} #nnetによって推定される状態sにおける方策a
        self.Es ={} #状態sの終了判定：player1の勝利なら1・敗北なら-1・終了で無ければ0．
        self.Vs ={} #状態sの合法手．
        self.Ws ={} #Σ_a Q(s,a)


    ###########################################################################
    def get_action_prob(self,canonical_state,temp=1):
        '''
        Input:
            canonical_enviroment:正準形式環境
            temp:ボルツマン温度
            
        Return:
            i番目の行動の選択確率がNsa[(s,a)]**(1./temp)であるようなベクトルを返す
        '''
        for i in range(self.args.num_MCTS):
            self.search(canonical_state,depth=0)
            
        s=self.env_model_utils.get_string_representation(canonical_state)
        counts=np.array([self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.env_model_utils.get_action_size())])
        
        #counts=0
        
        #ボルツマン温度が0ならば，グリーディ方策．
        if temp==0:
            best_a=np.argmax(counts)
            probs=np.zeros(len(counts))
            probs[best_a]=1
            return probs
        
        probs=counts**(1./temp)
        probs=probs/probs.sum()
        return probs
        
    
    ###########################################################################
    def search(self,canonical_state,depth=1):
        '''
        基本方針は以下の通り：
        1.状態sが終端かどうかを確認．終端であれば結果を（-1倍して)返す．
        2.状態sに初訪問の場合，NNを起動して，Ps・Vs・Nsを登録の上，NNによる状態価値の推定値を返す．
        3.状態sに2回目以降の訪問の場合，UCTを計算して，最大となる行動を選択・実行して再帰呼出する．
        '''
        s=self.env_model_utils.get_string_representation(canonical_state)
        #1
        if s not in self.Es:
            self.Es[s]=self.env_model_utils.get_ended(canonical_state,1)
        
        if self.Es[s]!=0:
            return -self.Es[s]
        
        #2
        if s not in self.Ps:
            self.Ps[s],v=self.model_system.predict(canonical_state)
            valids=self.env_model_utils.get_valid_actions(canonical_state,1)
            self.Ps[s]=self.Ps[s]*valids #非合法手をマスク
            sum_Ps_s=np.sum(self.Ps[s])
            if sum_Ps_s>0:
                self.Ps[s]/=sum_Ps_s #正規化
            else:
                print('All valid moves are masked. do workaround')
                self.Ps[s]=valids/valids.sum()
            
            self.Vs[s]=valids
            self.Ns[s]=0
            
            return -v
        
        #3
        valids=self.Vs[s]
        cur_best=-float('inf')
        best_a=-1
        
        
        dirichlet=np.random.choice(range(self.env_model_utils.get_action_size()), \
                                   p=valids/valids.sum())
        if depth==0:
            Ps_adj=(1-self.args.dirichlet_eps)*self.Ps[s]
            Ps_adj[dirichlet]+=self.args.dirichlet_eps
        else:
            Ps_adj=self.Ps[s]
        
        for a in range(self.env_model_utils.get_action_size()): #n*n+1
            if valids[a]:
                if (s,a) in self.Qsa:
                    u=self.Qsa[(s,a)]+self.args.cpuct*Ps_adj[a] \
                                     *math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                else:
                    u=self.args.cpuct*Ps_adj[a] \
                     *math.sqrt(self.Ns[s]+EPS)
                
                if u>cur_best:
                    cur_best=u
                    best_a=a
                    
        a=best_a
        next_state,next_player=self.env_model_utils.get_next_state(canonical_state,1,a)
        v=self.search(self.env_model_utils.get_canonical_form(next_state,next_player),depth=depth+1)
        #この再帰呼出が発生しないケースは，終端状態あるいはs初訪問の場合のみ．

        if (s,a) in self.Qsa:
            self.Qsa[(s,a)]=(self.Nsa[(s,a)]*self.Qsa[(s,a)]+v)/(self.Nsa[(s,a)]+1)
            self.Nsa[(s,a)]+=1
        else:
            self.Qsa[(s,a)]=v
            self.Nsa[(s,a)]=1
                     
        self.Ns[s]+=1
        
        return -v
        
        
