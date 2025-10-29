from math import inf

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

def minimax(board, player, alpha, beta):

    empty_cells = get_empty_cells(board)

    if check_winner(board, 'O'):
        return 10
    if check_winner(board, 'X'):
        return -10
    if not empty_cells:
        return 0

    next_player = 'O' if player == 'X' else 'X'

    if player == 'O': 
        best_val = -inf
        for cell in empty_cells:
            new_board = board[:]
            new_board[cell] = player
            val = minimax(new_board, next_player, alpha, beta)
            if val > best_val:
                best_val = val
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best_val
    
    else: 
        best_val = inf
        for cell in empty_cells:
            new_board = board[:]
            new_board[cell] = player
            val = minimax(new_board, next_player, alpha, beta)
            if val < best_val:
                best_val = val
            beta = min(beta, val)
            if beta <= alpha:
                break
        return best_val

# Example usage
result = minimax(board, 'O', -inf, inf)
print("Game result:", result)