#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
対戦用コード．
これを実行することで，


'''

from Arena import Arena

from EnviromentUtilities import EnviromentUtilities
from Enviroment import Enviroment

from MCTS import MCTS

from Model import ModelSystem

from Players import *

import numpy as np
from utils import *


###############################################################################
env_utils = EnviromentUtilities(6)
env = Enviroment(env_utils)

hp = HumanPlayer(env).play  # 人間プレイヤー

rp = RandomPlayer(env).play  # ランダム
gp = GreedyPlayer(env, env_utils).play  # グリーディ（常に直後に最も多くの石が取れる行動を選択）
agp = AntiGreedyPlayer(env, env_utils).play  # 逆グリーディ（グリーディの逆）
cgp = CompositeGreedyPlayer(env, env_utils).play  # 混合グリーディ（前半逆グリーディで後半グリーディ）

# AlphaZeroプレイヤー1の設定
ms1 = ModelSystem(env)
ms1.load_checkpoint('temp', 'best.pth.tar')  # DNNロード
args1 = dotdict({'num_MCTS':128, 'cpuct':1.0, 'dirichlet_eps':0.0})
mcts1 = MCTS(env_utils, ms1, args1)  # MCTSはnum_MCTS,dirichlet_epsしか参照しない．
azp1 = lambda x: np.argmax(mcts1.get_action_prob(x, temp=0))  # AlphaZeroプレイヤーオブジェクト

# AlphaZeroプレイヤー2の設定（AlphaZero同士で対戦させたいとき用）
ms2 = ModelSystem(env)
ms2.load_checkpoint('temp', 'best.pth.tar')  # DNNロード
args2 = dotdict({'num_MCTS':100, 'cpuct':1.0, 'dirichlet_eps':0.0})
mcts2 = MCTS(env_utils, ms2, args2)  # MCTSはnum_MCTS,dirichlet_epsしか参照しない．
azp2 = lambda x:np.argmax(mcts2.get_action_prob(x, temp=0))  # AlphaZeroプレイヤーオブジェクト


###############################################################################
# 試合設定
arena = Arena(player1=azp1, player2=hp, env=env, display=None)

# 対戦開始
print(arena.play_games(2, verbose=True))





