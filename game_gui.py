import tkinter as tk
from tkinter import messagebox
import logic  # the same logic.py from the GeeksforGeeks tutorial (unchanged)

# ---------- Look & feel ----------
BG_COLOR = "#bbada0"
EMPTY_COLOR = "#cdc1b4"
TILE_COLORS = {
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}
FONT = ("Helvetica", 28, "bold")


class Game2048(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2048")
        self.resizable(False, False)

        # Top bar with title + New Game button
        top = tk.Frame(self, padx=10, pady=10)
        top.pack(fill="x")
        tk.Label(top, text="2048", font=("Helvetica", 24, "bold")).pack(side="left")
        tk.Button(top, text="New Game", command=self.new_game).pack(side="right")

        # Grid area
        self.board = tk.Frame(self, bg=BG_COLOR, padx=6, pady=6)
        self.board.pack(padx=10, pady=(0, 10))

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                lbl = tk.Label(
                    self.board, text="", width=4, height=2,
                    font=FONT, bg=EMPTY_COLOR,
                )
                lbl.grid(row=i, column=j, padx=4, pady=4)
                row.append(lbl)
            self.cells.append(row)

        # Keyboard controls: arrow keys + WASD
        self.bind("<Key>", self.on_key)

        self.new_game()

    def new_game(self):
        self.mat = logic.start_game()   # creates 4x4 grid and adds the first 2
        logic.add_new_2(self.mat)       # the tutorial starts with two tiles
        self.draw()

    def draw(self):
        for i in range(4):
            for j in range(4):
                value = self.mat[i][j]
                lbl = self.cells[i][j]
                if value == 0:
                    lbl.config(text="", bg=EMPTY_COLOR)
                else:
                    bg, fg = TILE_COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                    lbl.config(text=str(value), bg=bg, fg=fg)
        self.update_idletasks()

    def on_key(self, event):
        key = event.keysym.lower()
        moves = {
            "w": logic.move_up,    "up": logic.move_up,
            "s": logic.move_down,  "down": logic.move_down,
            "a": logic.move_left,  "left": logic.move_left,
            "d": logic.move_right, "right": logic.move_right,
        }
        if key not in moves:
            return

        self.mat, changed = moves[key](self.mat)
        if changed:                      # only spawn a new 2 if the board moved
            logic.add_new_2(self.mat)
        self.draw()

        status = logic.get_current_state(self.mat)
        if status == "WON":
            messagebox.showinfo("2048", "You won! 🎉")
        elif status == "LOST":
            messagebox.showinfo("2048", "Game over!")


if __name__ == "__main__":
    Game2048().mainloop()