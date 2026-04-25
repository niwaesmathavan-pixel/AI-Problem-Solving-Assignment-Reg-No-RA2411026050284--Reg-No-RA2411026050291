# AI Problem Solving Assignment

**Name:** Niwaes M  / Tamilarsan A
**Register Number:** RA2411026050284 / RA2411026050291 
**Class:** AIML-E  

This repository contains the interactive solutions to two AI Problem Statements implemented using a Python Flask backend and a modern HTML/CSS/JS frontend.

---

## 1. Problem 1: Interactive Game AI (Tic-Tac-Toe System)

### Problem Description
A web-based Tic-Tac-Toe game where the user can intuitively click and play against an AI opponent. The AI evaluates possible futures and guarantees the best move every single time, making it an unbeatable opponent.

### Algorithms Used
The AI plays using two algorithms running in parallel for direct demonstration:
- **Minimax Algorithm**: Evaluates every possible move assuming the user also plays perfectly.
- **Alpha-Beta Pruning**: An optimized version of Minimax that significantly reduces the number of game states evaluated without losing accuracy.

### Sample Output Comparison
When playing against the AI:
- **Minimax**: Might explore ~40,000 to ~250,000 nodes for the first few moves. Execution time can vary between 0.1s to 0.4s.
- **Alpha-Beta Pruning**: Explores fewer than ~10,000 to ~20,000 nodes. Execution time is virtually instant, clearly demonstrating algorithmic optimization.

---

## 2. Problem 6: Sudoku Solver using CSP

### Problem Description
Sudoku is a logic-based placement puzzle on a 9x9 grid. The objective is to fill remaining cells so that each row, column, and 3x3 block contains the digits 1 through 9 exactly once.

### Algorithms Used
- **Constraint Satisfaction Problem (CSP) / Backtracking Algorithms**: Formulates Sudoku cells as variables and rules as constraints. It explores digits sequentially and prunes the path whenever conditions are violated, automatically backtracking if it ends up in an unsolvable grid state.

### Sample Output
The UI will process the user's grid state and provide realtime feedback:
> *You won! Solved in 142 backtracks.*
> (Or alternatively if you put impossible digits manually) -> *Try again. No solution exists.*

---

## Execution Steps

To run the interactive applications locally, ensure you have Python installed, and follow these instructions:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/niwaesmathavan-pixel/AI-Problem-Solving-Assignment-Reg-No-RA2411026050284--Reg-No-RA2411026050291.git
   cd AI-Problem-Solving-Assignment
   ```

2. **Install the requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```bash
   python app.py
   ```
   *And open your browser to `http://localhost:5000` to view the unified application menu!*
