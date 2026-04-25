import streamlit as st
import time

def check_winner(board):
    win_states = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for combo in win_states:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != "":
            return board[combo[0]]
    if "" not in board:
        return "Draw"
    return None

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

def get_best_move(board, is_maximizing_player, use_pruning):
    best_score = -float('inf') if is_maximizing_player else float('inf')
    move = -1
    stats = {'nodes': 0}
    player_symbol = "O" if is_maximizing_player else "X"
    
    start_time = time.time()
    for i in range(9):
        if board[i] == "":
            board[i] = player_symbol
            score = minimax(board, 0, not is_maximizing_player, -float('inf'), float('inf'), use_pruning, stats)
            board[i] = ""
            
            if is_maximizing_player:
                if score > best_score:
                    best_score = score
                    move = i
            else:
                if score < best_score:
                    best_score = score
                    move = i
                    
    exec_time = time.time() - start_time
    return move, stats['nodes'], exec_time

st.set_page_config(page_title="Tic-Tac-Toe AI", page_icon="🎮")
st.title("Interactive Tic-Tac-Toe AI 🎮")
st.markdown("Play against an AI. The AI evaluates moves using either **Minimax** or **Alpha-Beta Pruning**. Compare their performance!")

if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'last_stats' not in st.session_state:
    st.session_state.last_stats = None

st.sidebar.header("Settings")
algo_choice = st.sidebar.radio("Select AI Algorithm", ("Minimax", "Alpha-Beta Pruning"))
user_symbol = st.sidebar.radio("Select your symbol", ("X", "O"))
use_pruning = True if algo_choice == "Alpha-Beta Pruning" else False
ai_symbol = "O" if user_symbol == "X" else "X"
ai_is_maximizing = True if ai_symbol == "O" else False

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.last_stats = None

st.sidebar.button("Restart Game", on_click=reset_game)

# Perform AI move if it's AI's turn
def ai_turn():
    if not st.session_state.game_over and st.session_state.board.count("") > 0:
        with st.spinner("AI is thinking..."):
            best_move, nodes, exec_time = get_best_move(st.session_state.board, ai_is_maximizing, use_pruning)
            if best_move != -1:
                st.session_state.board[best_move] = ai_symbol
                st.session_state.last_stats = {"nodes": nodes, "time": exec_time, "algo": algo_choice}
                
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner

# Function to handle button click
def play_move(idx):
    if not st.session_state.game_over and st.session_state.board[idx] == "":
        st.session_state.board[idx] = user_symbol
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        else:
            ai_turn()

st.write("---")

cols = st.columns([1,1,1, 3])
with cols[0]:
    for i in range(0, 3):
        st.button(st.session_state.board[i] if st.session_state.board[i] else " ", key=f"btn_{i}", on_click=play_move, args=(i,), disabled=st.session_state.game_over, use_container_width=True)
with cols[1]:
    for i in range(3, 6):
        st.button(st.session_state.board[i] if st.session_state.board[i] else " ", key=f"btn_{i}", on_click=play_move, args=(i,), disabled=st.session_state.game_over, use_container_width=True)
with cols[2]:
    for i in range(6, 9):
        st.button(st.session_state.board[i] if st.session_state.board[i] else " ", key=f"btn_{i}", on_click=play_move, args=(i,), disabled=st.session_state.game_over, use_container_width=True)

with cols[3]:
    st.subheader("Game Status")
    if st.session_state.game_over:
        if st.session_state.winner == "Draw":
            st.info("It's a Draw!")
        elif st.session_state.winner == user_symbol:
            st.success("You Win! (Wait, that's illegal!)")
        else:
            st.error("AI Wins! Better luck next time.")
    else:
        st.write("**Your Turn!**" if st.session_state.board.count("") % 2 == (1 if user_symbol=="X" else 0) else "**AI Turn!**")
        
    if st.session_state.last_stats:
        st.write("---")
        st.write(f"**Last AI Move Stats ({st.session_state.last_stats['algo']}):**")
        st.write(f"- Nodes Explored: **{st.session_state.last_stats['nodes']}**")
        st.write(f"- Execution Time: **{st.session_state.last_stats['time']:.5f} sec**")

# If AI goes first
if not st.session_state.game_over and st.session_state.board.count("") == 9 and user_symbol == "O":
    ai_turn()
    st.rerun()
