board = [
    0, 1, 2,
    3, 4, 5,
    6, 7, 8
]

winning_combinations = [
    [0, 1, 2],[3, 4, 5],
    [6, 7, 8],[0, 3, 6],
    [1, 4, 7],[2, 5, 8],
    [0, 4, 8],[2, 4, 6]
]

def get_empty_cells(board):
    return [i for i, cell in enumerate(board) if cell not in ['X', 'O']]

def check_winner(board , player):
    for pos in winning_combinations:
        if all(board[i] == player for i in pos):
            return True 
        
    return False

def minimax(board , start_player):
    empty_cells = get_empty_cells(board)
    if check_winner(board , 'O'):
        return 10
    elif check_winner(board , 'X'):
        return -10
    elif not empty_cells:
        return 0
    
    moves = []
    for cell in empty_cells:
        new_board = board[:]
        new_board[cell] = start_player
        next_player = 'O' if start_player == 'X' else 'X'
        result = minimax(new_board , next_player)
        moves.append((cell, result))

    if start_player == 'O':
        best_move = max(moves, key=lambda x: x[1]) if moves else (None, 'Draw')
    else:
        best_move = min(moves, key=lambda x: x[1]) if moves else (None, 'Draw')

    return best_move[1]
# Example usage
result = minimax(board , 'X')
print("Game result:", result)