# AlphaZero
Simple implementation of AlphaZero in game of Othello using Keras.  

## Reference
Most part is based on suraganair's code shown below.  
https://github.com/suragnair/alpha-zero-general

Othello enviroment code is based on beow book.  
https://www.amazon.co.jp/Pythonによる深層強化学習入門-ChainerとOpenAI-Gymではじめる強化学習-牧野-浩二/dp/4274222535/ref=sr_1_2?ie=UTF8&qid=1536471915&sr=8-2&keywords=深層強化学習

## Main Algorithm
**NeuralNet(state) <- \[MCTS (NeuralNet,state),actual game result\]**  
i.e. MCTS is policy improver of NeuralNet.

## Source files
 - main.py : start training
 - Pit.py : start pitting between 2 players.
 
 - ModelSystem.py : define Neural Net obeject.
 - MCTS.py : define MCTS (Monte-Carlo Tree Search). referes ModelSystem and EnviromentUtilities.
 - Trainer.py : does reinforcement learning.
 - EnviromentUtilities.py : define Othello logic.
 - Enviroment.py : Othello enviroment.
 - Arena.py : 
 
 Dirichlet noise in the original paper is approximated as adding random spike to prior distribution Ps\[s\]. Because Dir(0.03) is very spiky and number of valid actions in othello is very limited compared to Go, then I think it is not so material that correctly implemented.
