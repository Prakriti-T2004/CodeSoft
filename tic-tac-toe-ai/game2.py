import tkinter as tk
import math

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Tic-Tac-Toe: Human vs AI")
        self.root.configure(bg="#f0f8ff")
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        self.winning_combo = []

        # Score tracking
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0

        self.create_board()

        self.status = tk.Label(root, text="Your turn (X)", font=("Arial", 16, "bold"),
                               bg="#f0f8ff", fg="#333")
        self.status.grid(row=3, column=0, columnspan=3, pady=(10, 0))

        self.scoreboard = tk.Label(root, text=self.get_score_text(), font=("Arial", 12),
                                   bg="#f0f8ff", fg="#555")
        self.scoreboard.grid(row=4, column=0, columnspan=3)

        self.restart_btn = tk.Button(root, text="🔁 Restart", font=("Arial", 12),
                                     bg="#dcdcdc", command=self.restart_game)
        self.restart_btn.grid(row=5, column=0, columnspan=3, pady=10)

    def create_board(self):
        for i in range(9):
            btn = tk.Button(self.root, text=' ', font=("Arial", 24, "bold"),
                            width=5, height=2, bg="#e6f2ff",
                            command=lambda i=i: self.human_move(i))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

    def human_move(self, index):
        if self.board[index] == ' ' and not self.is_game_over():
            self.board[index] = 'X'
            self.update_gui()
            if self.check_winner('X'):
                self.player_score += 1
                self.status.config(text="🎉 You win!", fg="green")
                self.highlight_winner()
                self.update_scoreboard()
            elif self.is_draw():
                self.draws += 1
                self.status.config(text="🤝 It's a draw!", fg="gray")
                self.update_scoreboard()
            else:
                self.status.config(text="AI is thinking...", fg="#333")
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.is_game_over():
            return

        best_score = -math.inf
        best_move = None
        for move in self.get_available_moves():
            self.board[move] = 'O'
            score = self.minimax(0, False, -math.inf, math.inf)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move

        if best_move is not None:
            self.board[best_move] = 'O'
            self.update_gui()
            if self.check_winner('O'):
                self.ai_score += 1
                self.status.config(text="🤖 AI wins!", fg="red")
                self.highlight_winner()
                self.update_scoreboard()
            elif self.is_draw():
                self.draws += 1
                self.status.config(text="🤝 It's a draw!", fg="gray")
                self.update_scoreboard()
            else:
                self.status.config(text="Your turn (X)", fg="#333")

    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.check_winner('O'):
            return 10 - depth
        if self.check_winner('X'):
            return depth - 10
        if self.is_draw():
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for move in self.get_available_moves():
                self.board[move] = 'O'
                eval = self.minimax(depth + 1, False, alpha, beta)
                self.board[move] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.get_available_moves():
                self.board[move] = 'X'
                eval = self.minimax(depth + 1, True, alpha, beta)
                self.board[move] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def check_winner(self, player):
        win_conditions = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for cond in win_conditions:
            if all(self.board[i] == player for i in cond):
                self.winning_combo = cond
                return True
        return False

    def is_draw(self):
        return ' ' not in self.board and not self.check_winner('X') and not self.check_winner('O')

    def is_game_over(self):
        return self.check_winner('X') or self.check_winner('O') or self.is_draw()

    def update_gui(self):
        for i in range(9):
            self.buttons[i].config(text=self.board[i])

    def highlight_winner(self):
        for i in self.winning_combo:
            self.buttons[i].config(bg="#90ee90")  # Light green

    def restart_game(self):
        self.board = [' ' for _ in range(9)]
        self.winning_combo = []
        for btn in self.buttons:
            btn.config(text=' ', bg="#e6f2ff")
        self.status.config(text="Your turn (X)", fg="#333")

    def get_score_text(self):
        return f"Score — You: {self.player_score} | AI: {self.ai_score} | Draws: {self.draws}"

    def update_scoreboard(self):
        self.scoreboard.config(text=self.get_score_text())

# 🔥 Launch the GUI
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeAI(root)
    root.mainloop()

