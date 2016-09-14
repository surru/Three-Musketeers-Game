# Saurabh Khoria
# 2013CSB1029

# Shubham Sharma
# 2013CSB1114

##Takes the input currentBoardState and
##return a list of two objects initial position and Final Position
##Board is in form of 2-D list where left top is [0,0] and right Bottom is [4,4]

##In Board
##0 -> Empty Location
##1 -> Musketeer
##2 -> soldier

import sys
from copy import copy, deepcopy
from random import randint

def musketeerMove(board):
    '''
    This function returns the best move for the musketeers given the board position
    I am considering further 6-ply moves in the 3 musketeers game.
    '''
    alpha=-sys.maxint
    beta=sys.maxint
    depth=6
    return alphabeta(board,depth,alpha,beta,"max",0)


##   This function returns the move in the format :  
##   [[initial Position Row, initial Position Column], [Final Position Row, Final Position Column]] 


def alphabeta(board,depth,alpha,beta,player,flag):
    '''
    This function implements the min-max algorithm with alpha-beta pruning
    '''
    mat=deepcopy(board)

    if player=="max":
        if depth==0:
            return utility(mat)
        moves=gen_max_moves(mat)
        if len(moves)==0:
            return utility(mat)
        best_move=[]
        best_score=-sys.maxint
        score=0
        for i in range(0,len(moves)):
            child=apply_max_move(mat,moves[i])
            score=alphabeta(child,depth-1,alpha,beta,"min",1)

            if score>best_score:
                best_move=moves[i]
                best_score=score
            alpha=max(alpha,best_score)

            if beta<=alpha:
                break

        if flag==0:
            return best_move
        else:
            return best_score

    if player=="min":
        if terminal(mat)==1:
            return utility(mat)

        moves=gen_min_moves(mat)
    
        if len(moves)==0:
            return utility(mat)

        best_move=[]
        best_score=sys.maxint
        score=0
        for i in range(0,len(moves)):
            child=[]
            chld=apply_min_move(mat,moves[i])
            child=chld[:][:]
            score=alphabeta(child,depth-1,alpha,beta,"max",1)

            if score<best_score:
                best_move=moves[i]
                best_score=score
            beta=min(beta,best_score)

            if beta<=alpha:
                break
        return best_score


def gen_max_moves(board):
    '''
    This function generates max moves i.e. moves of musketeers.
    '''
    mat=board
    moves=[]
    for i in range(0,5):
        for j in range(0,5):
            if mat[i][j]==1:
                if i-1>=0 and mat[i-1][j]==2:
                    moves.append([[i,j],[i-1,j]])
                if j-1>=0 and mat[i][j-1]==2:
                    moves.append([[i,j],[i,j-1]])
                if i+1<=4 and mat[i+1][j]==2:
                    moves.append([[i,j],[i+1,j]])
                if j+1<=4 and mat[i][j+1]==2:
                    moves.append([[i,j],[i,j+1]])

    return moves


def gen_min_moves(board):
    '''
    This function generates min moves i.e. moves of soldiers.
    '''
    mat=board
    moves=[]
    for i in range(0,5):
        for j in range(0,5):
            if mat[i][j]==2:
                if i-1>=0 and mat[i-1][j]==0:
                    moves.append([[i,j],[i-1,j]])
                if j-1>=0 and mat[i][j-1]==0:
                    moves.append([[i,j],[i,j-1]])
                if i+1<=4 and mat[i+1][j]==0:
                    moves.append([[i,j],[i+1,j]])
                if j+1<=4 and mat[i][j+1]==0:
                    moves.append([[i,j],[i,j+1]])

    return moves

def apply_max_move(board,move):
    '''
    This function applies the given max move on the given board and returns the new board
    '''
    mat=deepcopy(board)
    a=move[0]
    b=move[1]
    mat[a[0]][a[1]]=0
    mat[b[0]][b[1]]=1

    return mat

def apply_min_move(board,move):
    '''
    This function applies the given min move on the given board and returns the new board
    '''
    mat=deepcopy(board)
    a=move[0]
    b=move[1]
    mat[a[0]][a[1]]=0
    mat[b[0]][b[1]]=2

    return mat

def utility(board):
    '''
    This function returns the utility of the given board.
    I have used various factors like whether all musketeers are in same row or in same column,
    two of the musketeers are in same row or in same column, sum of manhettan distance between musketeers,
    count of max moves and min moves, count of number of soldiers remaining etc
    '''

    mat=board
    m1=gen_min_moves(mat)
    m2=gen_max_moves(mat)
    l1=len(m1)
    l2=len(m2)

    musk=[]
    for i in range(0,5):
        for j in range(0,5):
            if mat[i][j]==1:
                musk.append([i,j])
    flag=0
    f=0

    if musk[0][0]==musk[1][0] or musk[1][0]==musk[2][0]:
        flag-=1
    elif musk[0][1]==musk[1][1] or musk[1][1]==musk[2][1]:
        flag-=1

    if musk[0][0]==musk[1][0] and musk[1][0]==musk[2][0]:
        f=-1
    elif musk[0][1]==musk[1][1] and musk[1][1]==musk[2][1]:
        f=-1


    count=0

    x_dis=abs(musk[0][0]-musk[1][0])+abs(musk[1][0]-musk[2][0])
    y_dis=abs(musk[0][1]-musk[1][1])+abs(musk[1][1]-musk[2][1])

    for i in range(0,5):
        for j in range(0,5):
            if mat[i][j]==2:
                count+=1


    a=[100,200,50,150]
    b=[300,250,150,200]
    c=[600,700,650,500]
    d=[1000,1100,1200,1300]
    r1=randint(0,3)
    r2=randint(0,3)
    r3=randint(0,3)
    r4=randint(0,3)
    
    return f*30000+flag*d[r1]+(l2-l1)*b[r2]+a[r3]*(x_dis+y_dis)+c[r4]*count

def terminal(mat):
    '''
    This function checks whether the game is finished or not by checking whether all musketeers are in same row 
    or they are all in same column or not
    '''

    musk=[]
    flag=1
    for i in range(0,5):
        for j in range(0,5):
            if mat[i][j]==1:
                musk.append([i,j])

    if musk[0][0]==musk[1][0] and musk[1][0]==musk[2][0]:
        flag=0
    elif musk[0][1]==musk[1][1] and musk[1][1]==musk[2][1]:
        flag=0

    if flag==0:
        return 1
    else:
        return 0