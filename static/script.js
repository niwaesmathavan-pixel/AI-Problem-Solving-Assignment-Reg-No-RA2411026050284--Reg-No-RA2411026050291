let tttBoard = ["", "", "", "", "", "", "", "", ""];
let tttGameOver = false;

function initTTT() {
    const boardDiv = document.getElementById('ttt-board');
    boardDiv.innerHTML = '';
    for (let i = 0; i < 9; i++) {
        const cell = document.createElement('div');
        cell.className = 'ttt-cell';
        cell.onclick = () => makeMove(i);
        boardDiv.appendChild(cell);
    }
    updateTTTUI();
}

function updateTTTUI() {
    const cells = document.querySelectorAll('.ttt-cell');
    for (let i = 0; i < 9; i++) {
        cells[i].innerText = tttBoard[i];
        if (tttBoard[i] !== "") cells[i].classList.add('taken');
        else cells[i].classList.remove('taken');
    }
}

async function makeMove(i) {
    if (tttGameOver || tttBoard[i] !== "") return;
    
    // User move
    tttBoard[i] = "X";
    updateTTTUI();
    document.getElementById('ttt-status').innerText = "AI is thinking...";

    try {
        const response = await fetch('/ttt_move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({board: tttBoard})
        });
        const data = await response.json();
        
        document.getElementById('mm-nodes').innerText = data.nodes_mm;
        document.getElementById('mm-time').innerText = data.time_mm.toFixed(4);
        document.getElementById('ab-nodes').innerText = data.nodes_ab;
        document.getElementById('ab-time').innerText = data.time_ab.toFixed(4);

        if (data.move !== -1) {
            tttBoard[data.move] = "O";
        }
        updateTTTUI();
        checkWinner();
    } catch(err) {
        console.error(err);
    }
}

function checkWinner() {
    const wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
    let won = false;
    for (let combo of wins) {
        if (tttBoard[combo[0]] && tttBoard[combo[0]] === tttBoard[combo[1]] && tttBoard[combo[0]] === tttBoard[combo[2]]) {
            document.getElementById('ttt-status').innerText = `${tttBoard[combo[0]]} Wins!`;
            tttGameOver = true;
            won = true;
        }
    }
    if (!won && !tttBoard.includes("")) {
        document.getElementById('ttt-status').innerText = "Draw!";
        tttGameOver = true;
    } else if (!won) {
        document.getElementById('ttt-status').innerText = "Your turn! You are X.";
    }
}

function resetTTT() {
    tttBoard = ["", "", "", "", "", "", "", "", ""];
    tttGameOver = false;
    document.getElementById('ttt-status').innerText = "Your turn! You are X.";
    updateTTTUI();
}

// Sudoku
const defaultSudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
];

function initSudoku() {
    const gridDiv = document.getElementById('sudoku-grid');
    gridDiv.innerHTML = '';
    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.min = 1; input.max = 9;
            input.className = 'sudoku-cell';
            input.id = `cell-${r}-${c}`;
            if (defaultSudoku[r][c] !== 0) input.value = defaultSudoku[r][c];
            gridDiv.appendChild(input);
        }
    }
}

async function solveSudoku() {
    let grid = [];
    for (let r = 0; r < 9; r++) {
        let row = [];
        for (let c = 0; c < 9; c++) {
            let val = document.getElementById(`cell-${r}-${c}`).value;
            row.push(val ? parseInt(val) : 0);
        }
        grid.push(row);
    }
    document.getElementById('sudoku-status').innerText = "Solving...";
    
    try {
        const response = await fetch('/sudoku_solve', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({grid: grid})
        });
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('sudoku-status').innerText = `Solved in ${data.steps} backtracks!`;
            for (let r = 0; r < 9; r++) {
                for (let c = 0; c < 9; c++) {
                    document.getElementById(`cell-${r}-${c}`).value = data.grid[r][c];
                }
            }
        } else {
            document.getElementById('sudoku-status').innerText = "No solution exists for this configuration.";
        }
    } catch(err) {
        console.error(err);
    }
}

function resetSudoku() {
    initSudoku();
    document.getElementById('sudoku-status').innerText = "Fill in the grid or try the default!";
}

window.onload = () => {
    initTTT();
    initSudoku();
}
