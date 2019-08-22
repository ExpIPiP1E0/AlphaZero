#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from EnviromentUtilities import EnviromentUtilities
from Enviroment import Enviroment
from Model import ModelSystem

from MCTS import MCTS

from Trainer import Trainer


from utils import dotdict


args = dotdict({
      'num_MCTS': 25,
      'dirichlet_eps': 0.25,
      
      'num_iters': 3,  # num_episodes回の自己対戦による学習・num_compares_arenaを行う回数．i.e.最外ループの回数．
      'num_episodes': 10,  # 1回のiterationに何episode使うか
      'mini_batch_size': 600,   # 1回のNNの学習に用いるexperience数．
      'max_experiences': 200000, # Experience Replay Buffer
      'num_compares_arena': 10,  # 現行モデルとの比較を何試合行うか．
      'update_threshold': 0.55,  # 現行モデルに対して勝率がどれだけあればアップデートするか．
      
      'temp_threshold': 15,  # 最初の何回ランダム気味にするか
      'cpuct': 1.0,  # UCT factor

      'checkpoint': './temp/',
      'load_model': False,
      })


if __name__ == '__main__':
    env_utils = EnviromentUtilities(n=6)
    env = Enviroment(env_utils)
    model_system = ModelSystem(env)
    
    if args.load_model:
        model_system.load_checkpoint('./temp/', 'best.pth.tar')
    
    trainer = Trainer(env, env_utils, model_system, args)
    trainer.train()
    
    