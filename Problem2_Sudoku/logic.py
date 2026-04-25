def is_valid_sudoku(grid, r, c, k):
    not_in_row = all(grid[r][i] != k for i in range(9))
    not_in_col = all(grid[i][c] != k for i in range(9))
    start_r, start_c = 3 * (r // 3), 3 * (c // 3)
    not_in_box = all(grid[i][j] != k for i in range(start_r, start_r+3) for j in range(start_c, start_c+3))
    return not_in_row and not_in_col and not_in_box

def solve_sudoku(grid, stats):
    stats['steps'] += 1
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for k in range(1, 10):
                    if is_valid_sudoku(grid, r, c, k):
                        grid[r][c] = k
                        if solve_sudoku(grid, stats): 
                            return True
                        grid[r][c] = 0
                return False
    return True
