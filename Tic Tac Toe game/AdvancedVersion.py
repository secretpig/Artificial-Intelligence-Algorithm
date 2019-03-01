
# coding: utf-8

# In[1]:

import random
import time
import sys


# In[2]:

class AdvancedTTT:
    def __init__(self,initial=[[' ' for x in range(9)] for y in range(9)]):
        self.board=initial
        self.dic={'X':22,'O':-18,'/':2}
     
                
    def actions(self,state,pos):
        actions=[]
        for i in range(9):
            if state[pos-1][i]==' ':
                actions.append(i+1)
        return actions
        
    def move(self,state,pos,loc,player):
        board=[i[:] for i in state[:]]
        board[pos-1][loc-1]=player
        return board
    
    def isBoardFull(self,state):
        for i in range(9):
            for j in state[i]:
                if j==' ':
                    return False
        return 2
    
    def isWinner(self,state): # if X wins return 3, O return 1, else return False   
        for j in range(9):
            for i in range(3):
                if state[j][i*3:i*3+3]==['X','X','X'] or state[j][0+i:7+i:3]==['X','X','X']:
                    return 22
                if state[j][i*3:i*3+3]==['O','O','O'] or state[j][0+i:7+i:3]==['O','O','O']:
                    return -18
            if [state[j][0],state[j][4],state[j][8]]==['X','X','X'] or [state[j][2],state[j][4],state[j][6]]==['X','X','X']:
                return 22
            if [state[j][0],state[j][4],state[j][8]]==['O','O','O'] or [state[j][2],state[j][4],state[j][6]]==['O','O','O']:
                return -18 
        return False      
   
    def terminal_test(self,state):# check board
        if self.isWinner(state):
            return self.isWinner(state)
        else:
            return self.isBoardFull(state) # is BIGboard is full return 2, else return False
    def quicktest(self,state,pos):
        for i in range(3):
            if state[pos-1][i*3:i*3+3]==['X','X','X'] or state[pos-1][0+i:7+i:3]==['X','X','X']:
                return 22
            if state[pos-1][i*3:i*3+3]==['O','O','O'] or state[pos-1][0+i:7+i:3]==['O','O','O']:
                return -18
        if [state[pos-1][0],state[pos-1][4],state[pos-1][8]]==['X','X','X'] or [state[pos-1][2],state[pos-1][4],state[pos-1][6]]==['X','X','X']:
                return 22
        if [state[pos-1][0],state[pos-1][4],state[pos-1][8]]==['O','O','O'] or [state[pos-1][2],state[pos-1][4],state[pos-1][6]]==['O','O','O']:
                return -18 
            
        for i in range(9):
            for j in state[i]:
                if j==' ':
                    return False
        return 2


# In[3]:

def displayboard(board):#displayboard 
    for brow in range(3):
        for srow in range(3):
            for row in range(brow*3,3+brow*3):
                sys.stdout.write('  %s  |'%(board[row][srow*3]))
                sys.stdout.write('  %s  |'%(board[row][1+srow*3]))
                sys.stdout.write('  %s  ||'%(board[row][2+srow*3]))
            sys.stdout.write('\n')
            sys.stdout.write('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
        sys.stdout.write('############################################################\n')


# In[4]:

def Supercool(state,pos,player):# X is Max, O is Min
#######################################  
    def max_value(state,pos,alpha,beta,depth,oldpos): 
        if game.quicktest(state,oldpos):
            return game.quicktest(state,oldpos)
        if depth<0:
            return cutoff(state) 
        pos=findpos(state,pos)
        actions=game.actions(state,pos)

        v = float("-inf")
        for a in actions:
            v=max(v,min_value(game.move(state,pos,a,'X'),a,alpha,beta,depth-1,pos))
            if v>=beta:
                return v
            alpha=max(alpha,v)
        return v
 #######################################  
    def min_value(state,pos,alpha,beta,depth,oldpos): 
        if game.quicktest(state,oldpos):
            return game.quicktest(state,oldpos)       
        if depth<0:
            return cutoff(state)        
        pos=findpos(state,pos)
        actions=game.actions(state,pos)
        v = float("inf")
        for a in actions:
            v=min(v,max_value(game.move(state,pos,a,'O'),a,alpha,beta,depth-1,pos))
            if v<=alpha:
                return v
            beta=min(beta,v)
        return v 
 #######################################          
    def findpos(state,pos):# find a pos where the board is not full and there is no winner yet
        if game.actions(state,pos):
            return pos
        poslist=[]
        for i in range(9):
            for j in range(9):
                if state[i][j]==' ':
                    poslist.append(i+1)
                    break        
        pos=poslist.pop()
        return pos
    
    def cutoff(state):
        totalX=0
        totalO=0        
        for i in range(9):
            if len(set(state[i]))>1:
                sumX=0
                sumO=0
                for j in range(3):
                    if [state[i][j*3],state[i][j*3+1],state[i][j*3+2]] in [['X','X',' '],['X',' ','X'],[' ','X','X']] or                     [state[i][j],state[i][j+3],state[i][j+6]] in [['X','X',' '],['X',' ','X'],[' ','X','X']]:
                        sumX+=1
                    if [state[i][j],state[i][j+3],state[i][j+6]] in [['O','O',' '],['O',' ','O'],[' ','O','O']] or                     [state[i][j],state[i][j+3],state[i][j+6]] in [['O','O',' '],['O',' ','O'],[' ','O','O']] :
                        sumO+=1
                    if [state[i][0],state[i][4],state[i][8]] in [['X','X',' '],['X',' ','X'],[' ','X','X']] or                     [state[i][2],state[i][4],state[i][6]] in [['X','X',' '],['X',' ','X'],[' ','X','X']]:
                        sumX+=1
                    if [state[i][0],state[i][4],state[i][8]] in [['O','O',' '],['O',' ','O'],[' ','O','O']] or                     [state[i][2],state[i][4],state[i][6]] in [['O','O',' '],['O',' ','O'],[' ','O','O']]:
                        sumO+=1
                if sumX>0 and sumO==0:
                    totalX+=1
                elif sumX==0 and sumO>0:
                    totalO+=1
                elif sumX>0 and sumO>0:
                    totalX+=1
                    totalO+=1
        if totalX==totalO:
            v=2
        else:
            v=2+(totalX-totalO)
        return v           

 ####################################### 
    game=AdvancedTTT()
    count=0
    for i in state:
        if i==[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']:
            count+=1
    if count>5:        
        depth=4
    elif count<2:
        depth=7
    else:
        depth=6 
        
######### ##############prepare          
    pos=findpos(state,pos)
    actions=game.actions(state,pos)
    alpha=float("-inf")
    beta=float("inf")
########################    
    if player=='X':
        v = float("-inf")
        for a in actions:
            if v<min_value(game.move(state,pos,a,'X'),a,alpha,beta,depth,pos):
                v=min_value(game.move(state,pos,a,'X'),a,alpha,beta,depth,pos)
                best_action=a
                alpha=max(alpha,v)
        return best_action,pos
    else:
        v=float("inf")
        for a in actions:
            if v>max_value(game.move(state,pos,a,'O'),a,alpha,beta,depth,pos):
                v=max_value(game.move(state,pos,a,'O'),a,alpha,beta,depth,pos)
                best_action=a
                beta=min(v,beta)
        return best_action,pos


# In[ ]:

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
    sys.stdout.write('X first')
    sys.stdout.write('--------------------------------\n')
    time.sleep(2)
    return player 

def checkinput(actions):
    loc=None
    while True:
        try:
            loc= int(sys.stdin.readline()[:-1])
        except ValueError:
            sys.stderr.write("That's not an int!\n")
        if loc not in actions:
            sys.stderr.write('Please input right number of empty space \n')
        else:
            break
    return loc

def playgame(game,player):
    game=game
    if player['user']=='X':## if user is X, user move first
        sys.stdout.write('Please choose square where you want to play\n')
        pos=checkinput([1,2,3,4,5,6,7,8,9])
        sys.stdout.write('Please input where you want to place\n')
        loc=checkinput([1,2,3,4,5,6,7,8,9])
        sys.stdout.write('X move-')
        game.board=game.move(game.board,pos,loc,'X')
        sys.stdout.write('pos:%d          loc:%d\n'%(pos,loc))
        displayboard(game.board)
        # take turns to move
        pos=loc
        while not game.terminal_test(game.board):
            loc,pos=Supercool(game.board,pos,'O')
            sys.stdout.write('O move-')
            game.board=game.move(game.board,pos,loc,'O')
            sys.stdout.write('pos:%d          loc:%d\n'%(pos,loc))
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
            pos=loc
             #user move
            if not game.actions(game.board,pos):
                sys.stdout.write('Please choose square\n')
                poslist=[]
                for i in range(9):
                    for j in range(9):
                        if game.board[i][j]==' ':
                            poslist.append(i+1)
                            break
                pos=checkinput(poslist)
                
            sys.stdout.write('Please input where you want to place in square%d\n'%(pos))
            loc=checkinput(game.actions(game.board,pos))
            sys.stdout.write('X move-')
            game.board=game.move(game.board,pos,loc,'X')
            sys.stdout.write('pos:%d          loc:%d\n'%(pos,loc))
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
            pos=loc
    else:# if user is O, AI move first, pos=5
        pos=5
        loc,pos=Supercool(game.board,pos,'X')
        sys.stdout.write('X move-')
        game.board=game.move(game.board,pos,loc,'X')
        sys.stdout.write('pos:%d          loc:%d\n'%(pos,loc))
        displayboard(game.board)
        # take turns to move
        pos=loc
        while not game.terminal_test(game.board):
            if not game.actions(game.board,pos):
                sys.stdout.write('Please choose square\n')
                poslist=[]
                for i in range(9):
                    for j in range(9):
                        if game.board[i][j]==' ':
                            poslist.append(i+1)
                            break
                pos=checkinput(poslist)
            sys.stdout.write('Please input where you want to place in square%d\n'%(pos))
            loc=checkinput(game.actions(game.board,pos))
            sys.stdout.write('O move-')
            game.board=game.move(game.board,pos,loc,'O')
            sys.stdout.write('pos:%d          loc:%d\n'%(pos,loc))
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
             #AI move   
            pos=loc
            loc,pos=Supercool(game.board,pos,'X')
            sys.stdout.write('X move-')
            game.board=game.move(game.board,pos,loc,'X')
            sys.stdout.write('pos:%d          loc:%d\n'%(pos,loc))
            displayboard(game.board)
            if game.terminal_test(game.board):
                displayboard(game.board)
                break
            pos=loc

    if game.terminal_test(game.board)==2:
        return 'Draw'
    elif game.terminal_test(game.board)==22:
        return 'X wins'
    else:
        return 'O wins'
    


# In[ ]:

over=False
while not over:
    player=Initialgame()
    game=AdvancedTTT([[' ' for x in range(9)] for y in range(9)])
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

