import time
import random

board = [['_', '_', '_'], 
         ['_', '_', '_'], 
         ['_', '_', '_']]


board_coors = {'TL':[0,0], 'T':[0,1], 'TR':[0,2], # Lookup table to convert player input to board indices
               'L': [1,0], 'C':[1,1], 'R': [1,2],
               'BL':[2,0], 'B':[2,1], 'BR':[2,2]}

scores = {'tie': 0, 'X': 1, 'O': -1} # X is always the MAXIMIZING player, O is always MINIMIZING

def main():
    global board
    while True:
        global player
        player = input("Would you like to be X or O? X goes first. ").upper()
        if player == 'X':
            global ai
            ai = 'O'
            player_to_move = player
            break
        if player == 'O':
            ai = 'X'
            player_to_move = ai
            break

    next_turn = True
    while next_turn:
        if player_to_move == player:
            print_board()
            move = input("\nMake your move:\nTL T TR\nL  C R\nBL B BR\n\n").upper()
            if move in board_coors:
                row = board_coors[move][0]
                col = board_coors[move][1]
                if board[row][col] == '_': 
                    board[row][col] = player
                else: continue
            else: continue

            player_to_move = ai
            print_board()
            time.sleep(0.5)
            print('\nAI is moving...')

        else:
            best_move()
            player_to_move = player

        if check_winner() != None:
            print_board()
            declare_result(check_winner())
            board = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
            time.sleep(0.5)
            next_turn = False
                

def best_move():
    if ai == 'X':
        best_score = -1000 # Sets initial best score as worst case
        other_maximizing = False # If ai is X (maximizing player), checks each tile for worst case scenario with minimax (minimum score)
    else:
        best_score = 1000
        other_maximizing = True

    for row in range(3):
        for col in range(3):
            if board[row][col] == '_':
                board[row][col] = ai
                score = minimax(other_maximizing)
                board[row][col] = '_'
                if ai == 'X':
                    if score > best_score:
                        best_score = score
                        best_move_row = row
                        best_move_col = col
                else:
                    if score < best_score:
                        best_score = score
                        best_move_row = row
                        best_move_col = col
                        
    if empty_board():
        best_move_row = random.choice([0,2])
        best_move_col = random.choice([0,2])

    board[best_move_row][best_move_col] = ai

def minimax(is_maximizing):
    result = check_winner()
    if result:
        return scores[result] # If there is an end-game state, no need to look further!
    if is_maximizing == True: # AI is the maximizing player X
        best_score = -1000
        for row in range(3):
            for col in range(3):
                if board[row][col] == '_':
                    board[row][col] = ai
                    score = minimax(False)
                    board[row][col] = '_'
                    best_score = max(score, best_score)
                    
        return best_score

    else:
        best_score = 1000
        for row in range(3):
            for col in range(3):
                if board[row][col] == '_':
                    board[row][col] = ai
                    score = minimax(True)
                    board[row][col] = '_'
                    best_score = min(score, best_score)

        return best_score

def empty_board():
    for row in board:
        for ele in row:
            if ele != '_':
                return False
    return True

def winning_row(a, b, c): # Given 3 elements in a row, determines if they are a tic-tac-toe
    return a != '_' and a == b and b == c

def check_winner():
    winner = None
    for row in board:
        if winning_row(row[0], row[1], row[2]):
            winner = row[0]
    for col in range(3):
        if winning_row(board[0][col], board[1][col], board[2][col]):
            winner = board[0][col]
    if winning_row(board[0][0], board[1][1], board[2][2]) or winning_row(board[0][2], board[1][1], board[2][0]):
        winner = board[1][1]
    
    open_spots = 0
    for row in board:
        for ele in row:
            if ele == '_':
                open_spots += 1
    
    if winner == None and open_spots == 0:
        return 'tie'
    else:
        return winner

def declare_result(result):
    if result == 'tie':
        print("Tie!\n")
    elif result == player:
        print("Player win!\n")
    elif result == ai:
        print("AI win! The robot revolution is nigh 😈\n") 

def print_board():
    print(chr(27) + "[2J")
    for row in board:
        print(*row)

while True:
    main()