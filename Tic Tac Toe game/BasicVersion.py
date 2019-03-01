
# coding: utf-8

# In[1]:

import time
import sys


# In[2]:

class BasicTTT:
    def __init__(self,initial=[' ' for i in range(1,10)]):
        self.board=initial
        self.dic={'X':3,'O':1}
        self.actions=[]
        for i in range(len(self.board)):
            if self.board[i]==' ':
                self.actions.append(i+1)

    def action(self,state):
        action=[]
        for i in range(9):
            if state[i]==' ':
                action.append(i+1)
        return action
    
    def move(self,state,loc,player):
        state[loc-1]=player
        return state
    
    def isBoardFull(self,state):
        for i in state:
            if i==' ':
                return False
        return 2
    
    def isWinner(self,state): # if X wins return 1, O return -1, else return False   
        for i in range(3):
            if len(set(state[i*3:i*3+3]))==1 and state[i*3]!=' ':
                return self.dic[state[i*3]]
            elif len(set(state[0+i:7+i:3]))==1 and state[0+i]!=' ':
                return self.dic[state[0+i]]         
        if state[0]==state[4] and state[4] ==state[8] and  state[0]!=' ':
            return self.dic[state[0]]        
        if (state[2]==state[4]) and (state[4] ==state[6]) and  state[2]!=' ':
            return self.dic[state[2]]
        return False  
    
    
    def terminal_test(self,state):# define terminal state
        if self.isWinner(state):
            return self.isWinner(state)
        elif self.isBoardFull(state):
            return self.isBoardFull(state)
        else:
            return False   


# In[3]:

def displayboard(board):#displayboard 
    for j in range(3):
        for i in range(2):
            sys.stderr.write('    %s    |'%(board[i+j*3])) 
        sys.stderr.write('    %s    '%(board[2+j*3]))
        sys.stderr.write('\n------------------------------------\n')
    sys.stderr.write('||||||||||||||||||||||||||||||||||||||||||||\n')


# In[4]:

def alphabeta(state, player):# X is Max, O is Min
    
    def max_value(state,alpha,beta):
        if game.terminal_test(state):
            return game.terminal_test(state)        
        v = float("-inf")
        for a in game.action(state):
            v=max(v,min_value(game.move(state[:], a,'X'),alpha,beta))
            if v>=beta:
                return v
            alpha=max(alpha,v)                            
        return v
    
    def min_value(state,alpha,beta):
        if game.terminal_test(state):
            return game.terminal_test(state)        
        v = float("inf") 
        for a in game.action(state):
            v=min(v,max_value(game.move(state[:], a,'O'),alpha,beta))
            if v<=alpha:
                return v
            beta=min(beta,v)                
        return v      
    
    alpha=float("-inf")
    beta=float("inf")
    game=BasicTTT(state[:])
    if player=='X':
        v = float("-inf")
        for a in game.actions:
            if v<min_value(game.move(state[:],a,'X'),alpha,beta):
                v=min_value(game.move(state[:],a,'X'),alpha,beta)
                best_action=a
                alpha=max(alpha,v)
        return best_action   
    else:
        v = float("inf")
        for a in game.actions:
            if v>max_value(game.move(state[:],a,'O'),alpha,beta):
                v=max_value(game.move(state[:],a,'O'),alpha,beta)
                best_action=a
                beta=min(beta,v)
        return best_action


# In[6]:

def Initialgame():
    sys.stdout.write('Welcome to TIC TAC TOE\n')
    sys.stdout.write('Do you want to be X or O?\n')
    user=None
    while True:
        user=sys.stdin.readline()[:-1]
        if user!='O' and user!='X':
            sys.stderr.write('Input erro: please input X or O\n')
        else:
            break
    player={}
    player['user']=user
    if player['user']=='O':
        player['AI']='X'
    else:
        player['AI']='O'
    n=[i for i in range(1,10)]
    sys.stdout.write('Please input the position where you want to put your chess\n')
    displayboard(n)
    sys.stdout.write('--------------------------------\n')
    time.sleep(2)
    sys.stdout.write('X first')
    sys.stdout.write('--------------------------------\n')
    return player 

def playgame(game,player):
    game=game
    while not game.terminal_test(game.board):
        if  player['user']=='X':
            loc=None
            while True:
                try:
                    loc= int(sys.stdin.readline()[:-1])
                except ValueError:
                    sys.stderr.write("That's not an int!\n")
                if loc not in game.action(game.board):
                    sys.stderr.write('Please input right number of empty space \n')
                else:
                    break
            game.move(game.board,loc,'X')
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
            loc=alphabeta(game.board, player['AI'])
            game.move(game.board,loc,'O')
            sys.stdout.write('AI:%d \n'%(loc))
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
        else:
            loc=alphabeta(game.board, player['AI'])
            game.move(game.board,loc,'X')
            sys.stdout.write('AI:%d\n'%(loc))
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
            loc=None
            while True:
                try:
                    loc= int(sys.stdin.readline()[:-1])
                except ValueError:
                    sys.stderr.write("That's not an int!\n")
                if loc not in game.action(game.board):
                    sys.stderr.write('Please input number of empty space\n')
                else:
                    break
            game.move(game.board, loc,'O')
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
                

    if game.terminal_test(game.board)==2:
        return 'Draw'
    elif game.terminal_test(game.board)==3:
        return 'X wins'
    else:
        return 'O wins'
    


over=False
while not over:
    player=Initialgame()
    game=BasicTTT([' ' for i in range(1,10)])
    result=playgame(game,player)
    sys.stdout.write(result)
    sys.stdout.write('Do you want to play again?  Y/N\n')
    while True:
        end=sys.stdin.readline()[:-1]
        if end!='Y' and end!='N':
            sys.stderr.write('Input erro: please input Y or N\n')
        else:
            break
    if end=='N':
        over=True

