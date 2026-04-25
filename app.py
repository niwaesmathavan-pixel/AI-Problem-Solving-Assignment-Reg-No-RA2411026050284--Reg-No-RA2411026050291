# Project: AI Problem Solving Assignment
# Name: Niwaes M | Reg No: RA2411026050284 | Class: AIML-E
from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# --- TIC-TAC-TOE LOGIC (Minimax & Alpha-Beta) ---
def check_winner(board):
    win_states = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for combo in win_states:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            return board[combo[0]]
    return "Draw" if "" not in board else None

def minimax(board, depth, is_maximizing, alpha, beta, use_pruning, stats):
    stats['nodes'] += 1
    res = check_winner(board)
    if res == "O": return 1
    if res == "X": return -1
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

# --- SUDOKU LOGIC (CSP) ---
def is_valid_sudoku(grid, r, c, k):
    not_in_row = all(grid[r][i] != k for i in range(9))
    not_in_col = all(grid[i][c] != k for i in range(9))
    start_r, start_c = 3 * (r // 3), 3 * (c // 3)
    not_in_box = all(grid[i][j] != k for i in range(start_r, start_r+3) for j in range(start_c, start_c+3))
    return not_in_row and not_in_col and not_in_box

def solve_sudoku(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for k in range(1, 10):
                    if is_valid_sudoku(grid, r, c, k):
                        grid[r][c] = k
                        if solve_sudoku(grid): return True
                        grid[r][c] = 0
                return False
    return True

@app.route('/')
def index():
    return render_template('index.html', name="Niwaes M", reg_no="RA2411026050284")

@app.route('/ttt_move', methods=['POST'])
def ttt_move():
    board = request.json['board']
    # Compare Minimax vs Alpha-Beta Pruning [cite: 13]
    stats_mm = {'nodes': 0}
    start_mm = time.time()
    minimax(board, 0, True, -float('inf'), float('inf'), False, stats_mm)
    time_mm = time.time() - start_mm

    stats_ab = {'nodes': 0}
    start_ab = time.time()
    # Actual AI move logic
    best_score = -float('inf')
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False, -float('inf'), float('inf'), True, stats_ab)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    time_ab = time.time() - start_ab
    
    return jsonify({'move': move, 'nodes_mm': stats_mm['nodes'], 'time_mm': time_mm, 'nodes_ab': stats_ab['nodes'], 'time_ab': time_ab})

if __name__ == '__main__':
    app.run(debug=True)