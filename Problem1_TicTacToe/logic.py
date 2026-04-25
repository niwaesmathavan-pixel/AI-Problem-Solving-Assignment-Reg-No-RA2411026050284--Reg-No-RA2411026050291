import time

def check_winner(board):
    win_states = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for combo in win_states:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            return board[combo[0]]
    return "Draw" if "" not in board else None

def minimax(board, depth, is_maximizing, alpha, beta, use_pruning, stats):
    stats['nodes'] += 1
    res = check_winner(board)
    if res == "O": return 10 - depth
    if res == "X": return -10 + depth
    if res == "Draw": return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False, alpha, beta, use_pruning, stats)
                board[i] = ""
                best_score = max(score, best_score)
                if use_pruning:
                    alpha = max(alpha, score)
                    if beta <= alpha: break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True, alpha, beta, use_pruning, stats)
                board[i] = ""
                best_score = min(score, best_score)
                if use_pruning:
                    beta = min(beta, score)
                    if beta <= alpha: break
        return best_score

def get_best_move(board, use_pruning):
    stats = {'nodes': 0}
    start_time = time.time()
    best_score = -float('inf')
    move = -1
    
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False, -float('inf'), float('inf'), use_pruning, stats)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
                
    time_taken = time.time() - start_time
    return {'move': move, 'nodes': stats['nodes'], 'time': time_taken}
