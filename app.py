from flask import Flask, render_template, request, jsonify
from Problem1_TicTacToe.logic import get_best_move
from Problem2_Sudoku.logic import solve_sudoku
import copy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ttt_move', methods=['POST'])
def ttt_move():
    data = request.json
    board = data.get('board', [""] * 9)
    # Get stats for both to compare
    stats_mm = get_best_move(list(board), use_pruning=False)
    stats_ab = get_best_move(list(board), use_pruning=True)
    
    return jsonify({
        'move': stats_ab['move'], 
        'nodes_mm': stats_mm['nodes'], 
        'time_mm': stats_mm['time'], 
        'nodes_ab': stats_ab['nodes'], 
        'time_ab': stats_ab['time']
    })

@app.route('/sudoku_solve', methods=['POST'])
def sudoku_api():
    grid = request.json.get('grid')
    if not grid or len(grid) != 9:
        return jsonify({'success': False, 'message': 'Invalid grid'})
    
    # Process inputs (convert empty string to 0)
    for r in range(9):
        for c in range(9):
            if grid[r][c] == "" or grid[r][c] is None:
                grid[r][c] = 0
            else:
                grid[r][c] = int(grid[r][c])
                
    stats = {'steps': 0}
    solved_grid = copy.deepcopy(grid)
    success = solve_sudoku(solved_grid, stats)
    
    return jsonify({
        'success': success,
        'grid': solved_grid,
        'steps': stats['steps']
    })

if __name__ == '__main__':
    app.run(debug=True)
