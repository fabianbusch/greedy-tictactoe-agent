from ttt import TicTacToeGame
from agent import Agent

agent1 = Agent('Agent1', 0.3, 1, 0.001, deepLearn=True, debug=False)
agent1.loadModel()

done = False

board = [
        'N','N','N',
        'N','N','N',
        'N','N','N'
        ]

while not done:

    while True:
        x = agent1.decide(board)
        if board[x] == 'N': 
            board[x] = 'X'
            break
    
    print(board)

    while True:
        o = int(input('your next step?'))
        if board[o] == 'N':
            board[o] = 'O'
            break
