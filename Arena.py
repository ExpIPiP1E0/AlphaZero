#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Arena(object):
    """
    2つのPlayerを闘わせる．
    学習には直接は用いられない．
    Modelをアップデートすべきかどうか，既存Modelとの性能比較のために用いる．
    """
    ###########################################################################
    def __init__(self, player1, player2, env, display=None):
        '''
        player1/2は，canonical_stateを引数sとして，行動aを返す関数．
        '''
        self.player1 = player1
        self.player2 = player2  # 内部的には-1でコードされているので注意．
        self.env = env
        self.display = env.display  # 表示実行用のメソッド
        
        
    ###########################################################################
    def play_game(self, verbose=False):
        '''
        ゲームを1エピソードプレイする．
        Return:
            player1の終了時スコアを返す．
            1ならplayer1の勝利・-1ならplayer2の勝利，
            現在の実装では，ドローはplayer2の勝利扱いとなっている（0かどうかで終了判定をしている都合上）．
        '''
        it = 0  # 経過カウンタ
        self.env.reset()
        while True: #環境が終了状態でない限り続ける．
            it += 1
            if verbose:
                assert(self.display)
                print('Turn ', str(it), ' Player ', str(self.env.player))
                self.display()
                
            # あくまでも行動のための状態入力は正準状態に対してのものである．
            if self.env.player==1:
                action = self.player1(self.env.get_canonical_state())
            else:
                action = self.player2(self.env.get_canonical_state())
            #print('\n')

            # state, player, reward, reward!=0, None が返ってくる．このうち必要なのはdone (=reward!=0）のみ．
            _, _, _, done, _ = self.env.step(action)
            
            if done:
                break
        
        # 終了時の処理
        if verbose:
            assert(self.display)
            print('Game over: Turn ', str(it), 'Result ', str(self.env.get_ended()))  # get_endedはplayer1の勝敗を返す．
            self.display()
            
        return self.env.get_ended(player=1)
        
        
    ###########################################################################
    def play_games(self, num_episodes=1, verbose=False):
        '''
        self.player1とself.player2を，num_episode回対戦させて性能を評価する．
        1回目はplayer1が先手，以降は順次先番入替となる．
        Return:
            one_win:player1の勝利回数．
            two_win:player2の勝利回数．
            draws  :ドローの数（現行の実装では発生しない）．
        '''
        one_win = 0
        two_win = 0
        draws = 0
        
        episode = 1
        while episode<=num_episodes:
            result = self.play_game(verbose=verbose)
            if result==1:
                one_win += 1
            elif result==-1:
                two_win += 1
            else:
                draws += 1
            
            episode += 1
            if num_episodes<episode:
                break
            
            self.player1, self.player2 = self.player2, self.player1  # 入替
            
            # プレイヤーを入れ替えての再戦
            result = self.play_game(verbose=verbose)
            if result==-1:
                one_win += 1
            elif result==1:
                two_win += 1
            else:
                draws += 1
            
            episode += 1
            if num_episodes<episode:
                break

            self.player1, self.player2 = self.player2, self.player1  # 入替
            
        return one_win, two_win, draws
            
            