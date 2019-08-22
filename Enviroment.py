#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from EnviromentUtilities import EnviromentUtilities
'''
ゲームのルールそのものはこの環境クラスEnvironmentにはコードしない．
このオブジェクトにはあくまで現在の状態の情報のみを記憶し，
行動に対する対応・推移は全て別立てのEnviromrntUtilitiesを用いる．
これは，MCTSの性質上，元々，ゲームのルール部分を独立で持たせる必要があり，環境と同一化しない方が便利であるため．
あるいは，今後は，UtilitiesというよりはDynamicsとかMechanicsの方が合っているかも．
'''

class Enviroment(object):
    def __init__(self, env_utils):
        self.env_utils = env_utils
        self.state = self.env_utils.get_initial_state()  # ゲームの初期状態を獲得．
        self.player = 1  # 初期プレイヤーは1で固定．もう片方のプレイヤーは-1．
        
        
    def reset(self):
        self.state = self.env_utils.get_initial_state()
        self.player = 1
        return self.state
        
        
    def step(self, action):
        self.state, self.player = self.env_utils.get_next_state(self.state, self.player, action)
        reward = self.env_utils.get_ended(self.state, self.player)
        return self.state, self.player, reward, reward!=0, None


    def get_state_size(self):  # (n,n)
        return self.env_utils.get_state_size()
    
    
    def get_action_size(self):  # n*n+1
        return self.env_utils.get_action_size()
    
    
    def get_ended(self, player=1):  # ゲームが終了していればplayerのスコアを（±1）・していなければ0を返す．
        return self.env_utils.get_ended(self.state, player)
    
    
    def get_score(self, player):  # 恐らく直接は使われていない．グリーディプレイヤーなどの為にあると思われる．
        return self.env_utils.get_score(self.state, player)
    
    
    def get_canonical_state(self):  # 現在の状態を正準表示で取得．
        return self.env_utils.get_canonical_form(self.state, self.player)
    
    
    def get_valid_actions(self):  # 現在実行可能な行動を〜で取得．
        return self.env_utils.get_valid_actions(self.state, self.player)

    
    def display(self):  # 現在の状態を画面上に表示（コマンドプロンプト）．
        self.env_utils.display(self.state)
    

if __name__=='__main__':
    env = Enviroment(EnviromentUtilities(6))
    print(env.get_valid_actions())

