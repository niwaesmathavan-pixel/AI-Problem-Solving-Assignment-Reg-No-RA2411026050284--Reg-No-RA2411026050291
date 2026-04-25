import streamlit as st
import copy

st.set_page_config(page_title="Sudoku Solver CSP", page_icon="🧩")

def is_valid_sudoku(grid, r, c, k):
    not_in_row = all(grid[r][i] != k for i in range(9))
    not_in_col = all(grid[i][c] != k for i in range(9))
    start_r, start_c = 3 * (r // 3), 3 * (c // 3)
    not_in_box = all(grid[i][j] != k for i in range(start_r, start_r+3) for j in range(start_c, start_c+3))
    return not_in_row and not_in_col and not_in_box

def solve_sudoku(grid, stats=None):
    if stats is not None:
        stats["steps"] += 1
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

st.title("Interactive Sudoku Solver 🧩")
st.markdown("Play and solve Sudoku based on a Constraint Satisfaction Problem (CSP) approach.")

# Easy level default puzzle
default_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

if 'grid' not in st.session_state:
    st.session_state.grid = copy.deepcopy(default_puzzle)

st.write("Edit the grid below. Use 0 for empty cells.")
edited_grid = st.data_editor(st.session_state.grid, key="sudoku_grid", height=350, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("Solve using CSP", use_container_width=True):
        grid_copy = copy.deepcopy(edited_grid)
        stats = {"steps": 0}
        with st.spinner("Solving..."):
            solved = solve_sudoku(grid_copy, stats)
        
        if solved:
            st.success(f"You won! Solved in {stats['steps']} backtracks.")
            st.session_state.grid = grid_copy
            st.rerun()
        else:
            st.error("Try again. No solution exists for this configuration.")

with col2:
    if st.button("Reset Puzzle", use_container_width=True):
        st.session_state.grid = copy.deepcopy(default_puzzle)
        st.rerun()

st.markdown("""
### How CSP Works here:
1. **Variables**: 81 cells in the grid.
2. **Domain**: Integers 1-9.
3. **Constraints**:
   - Each row contains digits 1–9 exactly once.
   - Each column contains digits 1–9 exactly once.
   - Each 3×3 subgrid contains digits 1–9 exactly once.
""")
