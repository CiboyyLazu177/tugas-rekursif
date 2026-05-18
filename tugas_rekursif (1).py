"""
Tugas Rekursif - Visualisasi dengan Python (Tkinter)
====================================================
1. N-Queens Problem
2. Knight's Tour Problem
3. Knapsack Problem
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading


# ─────────────────────────────────────────────
# WARNA & STYLE
# ─────────────────────────────────────────────
BG_DARK    = "#0f0f1a"
BG_PANEL   = "#1a1a2e"
BG_CARD    = "#16213e"
ACCENT1    = "#e94560"   # merah-pink
ACCENT2    = "#0f3460"   # biru gelap
ACCENT3    = "#533483"   # ungu
GOLD       = "#f5a623"
TEXT_MAIN  = "#eaeaea"
TEXT_SUB   = "#8888aa"
BOARD_LIGHT = "#f0d9b5"
BOARD_DARK  = "#b58863"
QUEEN_CLR  = "#e94560"
KNIGHT_CLR = "#f5a623"
VISITED_CLR = "#1e88e5"


# ═══════════════════════════════════════════════════════════
# SOAL 1 — N-QUEENS
# ═══════════════════════════════════════════════════════════
class NQueensApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.solutions = []
        self.current_sol = 0
        self.n = 8
        self._build_ui()

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill="x", padx=20, pady=(18, 6))
        tk.Label(hdr, text="♛  N-Queens Problem", font=("Georgia", 22, "bold"),
                 fg=ACCENT1, bg=BG_DARK).pack(side="left")

        # Desc
        desc = ("Tempatkan N ratu di papan N×N sehingga tidak ada dua ratu\n"
                "yang saling menyerang (baris, kolom, atau diagonal).")
        tk.Label(self, text=desc, font=("Consolas", 10),
                 fg=TEXT_SUB, bg=BG_DARK, justify="left").pack(anchor="w", padx=24)

        # Control
        ctrl = tk.Frame(self, bg=BG_PANEL, pady=10)
        ctrl.pack(fill="x", padx=20, pady=10)

        tk.Label(ctrl, text="Ukuran Papan (N):", font=("Consolas", 11),
                 fg=TEXT_MAIN, bg=BG_PANEL).pack(side="left", padx=(14, 6))

        self.n_var = tk.IntVar(value=8)
        spin = tk.Spinbox(ctrl, from_=4, to=12, textvariable=self.n_var,
                          width=4, font=("Consolas", 13), bg=BG_CARD, fg=GOLD,
                          buttonbackground=BG_CARD, relief="flat")
        spin.pack(side="left", padx=4)

        self.btn_solve = tk.Button(ctrl, text="▶  Selesaikan", font=("Consolas", 11, "bold"),
                                   bg=ACCENT1, fg="white", relief="flat", cursor="hand2",
                                   padx=14, pady=6, command=self._solve)
        self.btn_solve.pack(side="left", padx=10)

        self.btn_prev = tk.Button(ctrl, text="◀ Prev", font=("Consolas", 10),
                                  bg=ACCENT3, fg="white", relief="flat", cursor="hand2",
                                  padx=10, pady=6, command=self._prev_sol, state="disabled")
        self.btn_prev.pack(side="left", padx=2)

        self.btn_next = tk.Button(ctrl, text="Next ▶", font=("Consolas", 10),
                                  bg=ACCENT3, fg="white", relief="flat", cursor="hand2",
                                  padx=10, pady=6, command=self._next_sol, state="disabled")
        self.btn_next.pack(side="left", padx=2)

        self.lbl_info = tk.Label(ctrl, text="", font=("Consolas", 10),
                                 fg=GOLD, bg=BG_PANEL)
        self.lbl_info.pack(side="left", padx=10)

        # Board canvas
        self.canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0, height=420)
        self.canvas.pack(expand=True, fill="both", padx=20, pady=10)

    # ── Algoritma ──────────────────────────────
    def _is_safe(self, board, row, col):
        for i in range(row):
            c = board[i]
            if c == col or abs(c - col) == abs(i - row):
                return False
        return True

    def _solve_nqueens(self, board, row, n, results):
        if row == n:
            results.append(board[:])
            return
        for col in range(n):
            if self._is_safe(board, row, col):
                board[row] = col
                self._solve_nqueens(board, row + 1, n, results)
                board[row] = -1

    # ── UI helpers ─────────────────────────────
    def _solve(self):
        self.n = self.n_var.get()
        self.solutions = []
        self._solve_nqueens([-1] * self.n, 0, self.n, self.solutions)
        self.current_sol = 0
        if self.solutions:
            self.lbl_info.config(text=f"Solusi: 1/{len(self.solutions)}")
            self.btn_next.config(state="normal")
            self.btn_prev.config(state="normal")
            self._draw_board(self.solutions[0])
        else:
            messagebox.showinfo("N-Queens", "Tidak ada solusi.")

    def _next_sol(self):
        if self.solutions:
            self.current_sol = (self.current_sol + 1) % len(self.solutions)
            self.lbl_info.config(text=f"Solusi: {self.current_sol+1}/{len(self.solutions)}")
            self._draw_board(self.solutions[self.current_sol])

    def _prev_sol(self):
        if self.solutions:
            self.current_sol = (self.current_sol - 1) % len(self.solutions)
            self.lbl_info.config(text=f"Solusi: {self.current_sol+1}/{len(self.solutions)}")
            self._draw_board(self.solutions[self.current_sol])

    def _draw_board(self, queens):
        self.canvas.delete("all")
        self.update_idletasks()
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        n = self.n
        size = min(W, H) - 40
        cell = size // n
        ox = (W - cell * n) // 2
        oy = (H - cell * n) // 2

        for r in range(n):
            for c in range(n):
                clr = BOARD_LIGHT if (r + c) % 2 == 0 else BOARD_DARK
                x0, y0 = ox + c * cell, oy + r * cell
                self.canvas.create_rectangle(x0, y0, x0 + cell, y0 + cell,
                                             fill=clr, outline="")
                if queens[r] == c:
                    # Highlight
                    self.canvas.create_rectangle(x0+2, y0+2, x0+cell-2, y0+cell-2,
                                                 fill="#ff6b8a", outline="")
                    # Queen symbol
                    self.canvas.create_text(x0 + cell // 2, y0 + cell // 2,
                                            text="♛", font=("Arial", max(10, cell - 10), "bold"),
                                            fill="white")
        # Border
        self.canvas.create_rectangle(ox, oy, ox + cell * n, oy + cell * n,
                                     outline=ACCENT1, width=2)


# ═══════════════════════════════════════════════════════════
# SOAL 2 — KNIGHT'S TOUR
# ═══════════════════════════════════════════════════════════
class KnightsTourApp(tk.Frame):
    MOVES = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.board_size = 6
        self.board = []
        self.solving = False
        self._build_ui()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill="x", padx=20, pady=(18, 6))
        tk.Label(hdr, text="♞  Knight's Tour", font=("Georgia", 22, "bold"),
                 fg=GOLD, bg=BG_DARK).pack(side="left")

        desc = ("Kuda catur harus mengunjungi setiap petak tepat satu kali\n"
                "menggunakan gerakan-L yang legal.")
        tk.Label(self, text=desc, font=("Consolas", 10),
                 fg=TEXT_SUB, bg=BG_DARK, justify="left").pack(anchor="w", padx=24)

        ctrl = tk.Frame(self, bg=BG_PANEL, pady=10)
        ctrl.pack(fill="x", padx=20, pady=10)

        tk.Label(ctrl, text="Ukuran:", font=("Consolas", 11), fg=TEXT_MAIN, bg=BG_PANEL).pack(side="left", padx=(14,4))
        self.size_var = tk.IntVar(value=6)
        tk.Spinbox(ctrl, from_=5, to=8, textvariable=self.size_var,
                   width=3, font=("Consolas", 13), bg=BG_CARD, fg=GOLD,
                   buttonbackground=BG_CARD, relief="flat").pack(side="left", padx=4)

        tk.Label(ctrl, text="  Start (baris,kol):", font=("Consolas", 11), fg=TEXT_MAIN, bg=BG_PANEL).pack(side="left", padx=(10,4))
        self.row_var = tk.IntVar(value=0)
        self.col_var = tk.IntVar(value=0)
        tk.Spinbox(ctrl, from_=0, to=7, textvariable=self.row_var,
                   width=2, font=("Consolas", 12), bg=BG_CARD, fg=KNIGHT_CLR,
                   buttonbackground=BG_CARD, relief="flat").pack(side="left", padx=2)
        tk.Label(ctrl, text=",", fg=TEXT_MAIN, bg=BG_PANEL, font=("Consolas",12)).pack(side="left")
        tk.Spinbox(ctrl, from_=0, to=7, textvariable=self.col_var,
                   width=2, font=("Consolas", 12), bg=BG_CARD, fg=KNIGHT_CLR,
                   buttonbackground=BG_CARD, relief="flat").pack(side="left", padx=2)

        self.btn_solve = tk.Button(ctrl, text="▶  Selesaikan", font=("Consolas", 11, "bold"),
                                   bg=GOLD, fg=BG_DARK, relief="flat", cursor="hand2",
                                   padx=14, pady=6, command=self._start_solve)
        self.btn_solve.pack(side="left", padx=10)

        self.lbl_status = tk.Label(ctrl, text="", font=("Consolas", 10), fg=GOLD, bg=BG_PANEL)
        self.lbl_status.pack(side="left", padx=8)

        self.canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0, height=420)
        self.canvas.pack(expand=True, fill="both", padx=20, pady=10)

    # ── Algoritma Warnsdorff ────────────────────
    def _degree(self, board, r, c, n):
        count = 0
        for dr, dc in self.MOVES:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == -1:
                count += 1
        return count

    def _solve_kt(self, board, r, c, move_num, n, path):
        if move_num == n * n:
            return True
        neighbors = []
        for dr, dc in self.MOVES:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == -1:
                deg = self._degree(board, nr, nc, n)
                neighbors.append((deg, nr, nc))
        neighbors.sort()
        for _, nr, nc in neighbors:
            board[nr][nc] = move_num
            path.append((nr, nc))
            if self._solve_kt(board, nr, nc, move_num + 1, n, path):
                return True
            board[nr][nc] = -1
            path.pop()
        return False

    def _start_solve(self):
        n = self.size_var.get()
        sr, sc = self.row_var.get(), self.col_var.get()
        if sr >= n or sc >= n:
            messagebox.showwarning("Input Error", f"Posisi awal harus < {n}")
            return
        self.lbl_status.config(text="Mencari solusi...")
        self.btn_solve.config(state="disabled")
        self.update()

        board = [[-1]*n for _ in range(n)]
        board[sr][sc] = 0
        path = [(sr, sc)]
        found = self._solve_kt(board, sr, sc, 1, n, path)

        if found:
            self.lbl_status.config(text=f"✓ Solusi ditemukan! ({n*n} langkah)")
            self._animate_tour(board, path, n)
        else:
            self.lbl_status.config(text="✗ Tidak ada solusi.")
        self.btn_solve.config(state="normal")

    def _animate_tour(self, board, path, n):
        self.canvas.delete("all")
        self.update_idletasks()
        W = self.canvas.winfo_width()
        H = self.canvas.winfo_height()
        size = min(W, H) - 40
        cell = size // n
        ox = (W - cell * n) // 2
        oy = (H - cell * n) // 2

        def cx(c): return ox + c * cell + cell // 2
        def cy(r): return oy + r * cell + cell // 2

        # Draw base board
        for r in range(n):
            for c in range(n):
                clr = BOARD_LIGHT if (r+c)%2==0 else BOARD_DARK
                self.canvas.create_rectangle(ox+c*cell, oy+r*cell,
                                             ox+(c+1)*cell, oy+(r+1)*cell,
                                             fill=clr, outline="")

        # Draw path animated
        for i in range(1, len(path)):
            pr, pc = path[i-1]
            cr2, cc2 = path[i]
            # line
            self.canvas.create_line(cx(pc), cy(pr), cx(cc2), cy(cr2),
                                    fill=KNIGHT_CLR, width=2, arrow=tk.LAST)
            # number on cell
            r2, c2 = path[i-1]
            self.canvas.create_text(cx(c2), cy(r2),
                                    text=str(board[r2][c2]),
                                    font=("Consolas", max(7, cell//3), "bold"),
                                    fill=BG_DARK)

        # Last cell number
        lr, lc = path[-1]
        self.canvas.create_text(cx(lc), cy(lr),
                                text=str(board[lr][lc]),
                                font=("Consolas", max(7, cell//3), "bold"),
                                fill=BG_DARK)

        # Start & End markers
        sr2, sc2 = path[0]
        er, ec = path[-1]
        self.canvas.create_oval(cx(sc2)-10, cy(sr2)-10, cx(sc2)+10, cy(sr2)+10,
                                fill=ACCENT1, outline="white", width=2)
        self.canvas.create_text(cx(sc2), cy(sr2), text="S", fill="white",
                                font=("Consolas", 9, "bold"))
        self.canvas.create_oval(cx(ec)-10, cy(er)-10, cx(ec)+10, cy(er)+10,
                                fill=ACCENT3, outline="white", width=2)
        self.canvas.create_text(cx(ec), cy(er), text="E", fill="white",
                                font=("Consolas", 9, "bold"))
        self.canvas.create_rectangle(ox, oy, ox+cell*n, oy+cell*n,
                                     outline=GOLD, width=2)


# ═══════════════════════════════════════════════════════════
# SOAL 3 — KNAPSACK
# ═══════════════════════════════════════════════════════════
class KnapsackApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.items = [2, 5, 6, 9, 12, 14, 20]
        self.target = 30
        self._build_ui()

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG_DARK)
        hdr.pack(fill="x", padx=20, pady=(18, 6))
        tk.Label(hdr, text="🎒  Knapsack Problem", font=("Georgia", 22, "bold"),
                 fg=ACCENT3, bg=BG_DARK).pack(side="left")

        desc = ("Pilih kombinasi barang yang totalnya tepat sama dengan berat target\n"
                "menggunakan algoritma rekursif backtracking.")
        tk.Label(self, text=desc, font=("Consolas", 10),
                 fg=TEXT_SUB, bg=BG_DARK, justify="left").pack(anchor="w", padx=24)

        # Input area
        inp = tk.Frame(self, bg=BG_PANEL, pady=12)
        inp.pack(fill="x", padx=20, pady=(8,0))

        tk.Label(inp, text="Berat Barang (pisahkan koma):", font=("Consolas", 10),
                 fg=TEXT_MAIN, bg=BG_PANEL).grid(row=0, column=0, sticky="w", padx=(14,6), pady=4)
        self.items_entry = tk.Entry(inp, font=("Consolas", 11), bg=BG_CARD, fg=GOLD,
                                    relief="flat", insertbackground=GOLD, width=36)
        self.items_entry.insert(0, "2, 5, 6, 9, 12, 14, 20")
        self.items_entry.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(inp, text="Berat Target:", font=("Consolas", 10),
                 fg=TEXT_MAIN, bg=BG_PANEL).grid(row=1, column=0, sticky="w", padx=(14,6), pady=4)
        self.target_entry = tk.Entry(inp, font=("Consolas", 11), bg=BG_CARD, fg=ACCENT1,
                                     relief="flat", insertbackground=ACCENT1, width=10)
        self.target_entry.insert(0, "30")
        self.target_entry.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        self.btn_solve = tk.Button(inp, text="▶  Cari Solusi", font=("Consolas", 11, "bold"),
                                   bg=ACCENT3, fg="white", relief="flat", cursor="hand2",
                                   padx=14, pady=6, command=self._solve)
        self.btn_solve.grid(row=0, column=2, rowspan=2, padx=16)

        self.lbl_status = tk.Label(inp, text="", font=("Consolas", 10),
                                   fg=GOLD, bg=BG_PANEL)
        self.lbl_status.grid(row=0, column=3, rowspan=2, padx=6)

        # Result canvas
        self.canvas = tk.Canvas(self, bg=BG_DARK, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=20, pady=10)

    # ── Algoritma rekursif ──────────────────────
    def _knapsack(self, weights, target, idx, chosen, all_solutions):
        if target == 0:
            all_solutions.append(chosen[:])
            return
        if idx >= len(weights) or target < 0:
            return
        # Ambil item ini
        chosen.append(weights[idx])
        self._knapsack(weights, target - weights[idx], idx + 1, chosen, all_solutions)
        chosen.pop()
        # Lewati item ini
        self._knapsack(weights, target, idx + 1, chosen, all_solutions)

    def _solve(self):
        try:
            raw = self.items_entry.get()
            weights = [int(x.strip()) for x in raw.split(",") if x.strip()]
            target = int(self.target_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Input tidak valid.")
            return

        all_solutions = []
        self._knapsack(weights, target, 0, [], all_solutions)

        self.canvas.delete("all")
        self.update_idletasks()

        if not all_solutions:
            self.lbl_status.config(text="✗ Tidak ada solusi.")
            self._draw_no_solution(weights, target)
            return

        self.lbl_status.config(text=f"✓ {len(all_solutions)} solusi ditemukan!")
        self._draw_solutions(weights, target, all_solutions)

    def _draw_solutions(self, weights, target, solutions):
        self.canvas.delete("all")
        W = self.canvas.winfo_width() or 700
        H = self.canvas.winfo_height() or 380

        # Title
        self.canvas.create_text(W//2, 22, text=f"Target: {target} — {len(solutions)} Solusi",
                                font=("Georgia", 13, "bold"), fill=GOLD)

        # Draw all items at top
        item_w = max(40, min(70, (W - 40) // len(weights)))
        total_w = item_w * len(weights)
        sx = (W - total_w) // 2

        # Label baris items
        self.canvas.create_text(sx - 10, 55, text="Semua\nBarang:", font=("Consolas", 8),
                                fill=TEXT_SUB, anchor="e")
        for i, w in enumerate(weights):
            x0 = sx + i * item_w + 3
            x1 = sx + (i+1) * item_w - 3
            self.canvas.create_rectangle(x0, 42, x1, 72, fill=BG_CARD, outline=TEXT_SUB, width=1)
            self.canvas.create_text((x0+x1)//2, 57, text=str(w), font=("Consolas", 11, "bold"),
                                    fill=TEXT_MAIN)

        # Tampilkan hingga 8 solusi
        max_show = min(8, len(solutions))
        row_h = min(46, (H - 90) // max_show)

        for si, sol in enumerate(solutions[:max_show]):
            sol_set = set(sol)  # simple: match by index (use enumerate trick)
            y_top = 88 + si * row_h
            y_bot = y_top + row_h - 4

            # Label solusi
            self.canvas.create_text(sx - 10, (y_top+y_bot)//2,
                                    text=f"#{si+1}", font=("Consolas", 8, "bold"),
                                    fill=ACCENT3, anchor="e")

            used_items = self._match_solution(weights, sol)
            total = 0
            for i, w in enumerate(weights):
                x0 = sx + i * item_w + 3
                x1 = sx + (i+1) * item_w - 3
                used = used_items[i]
                fill = ACCENT3 if used else BG_CARD
                out = ACCENT1 if used else TEXT_SUB
                self.canvas.create_rectangle(x0, y_top, x1, y_bot,
                                             fill=fill, outline=out, width=1 if not used else 2)
                self.canvas.create_text((x0+x1)//2, (y_top+y_bot)//2,
                                        text=str(w), font=("Consolas", max(7,row_h//4), "bold"),
                                        fill="white" if used else TEXT_SUB)
                if used:
                    total += w

            # Total bar
            tx = sx + total_w + 10
            self.canvas.create_text(tx, (y_top+y_bot)//2,
                                    text=f"= {total}", font=("Consolas", 9, "bold"),
                                    fill=GOLD, anchor="w")
            bar_w = int((total / target) * 120)
            self.canvas.create_rectangle(tx + 40, y_top+4, tx + 40 + 120, y_bot-4,
                                         fill=BG_CARD, outline=TEXT_SUB)
            self.canvas.create_rectangle(tx + 40, y_top+4, tx + 40 + bar_w, y_bot-4,
                                         fill=ACCENT3, outline="")

        if len(solutions) > max_show:
            self.canvas.create_text(W//2, H - 14,
                                    text=f"... dan {len(solutions)-max_show} solusi lainnya",
                                    font=("Consolas", 9), fill=TEXT_SUB)

    def _match_solution(self, weights, sol):
        """Return boolean list: which weight indices are used in sol."""
        used = [False] * len(weights)
        remaining = list(sol)
        for i, w in enumerate(weights):
            if w in remaining:
                used[i] = True
                remaining.remove(w)
        return used

    def _draw_no_solution(self, weights, target):
        W = self.canvas.winfo_width() or 700
        H = self.canvas.winfo_height() or 380
        self.canvas.create_text(W//2, H//2, text="Tidak ada kombinasi\nyang memenuhi target.",
                                font=("Georgia", 16), fill=ACCENT1, justify="center")


# ═══════════════════════════════════════════════════════════
# MAIN APP WINDOW
# ═══════════════════════════════════════════════════════════
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tugas Rekursif — Visualisasi Python")
        self.geometry("900x640")
        self.minsize(780, 560)
        self.configure(bg=BG_DARK)
        self._build()

    def _build(self):
        # Top bar
        topbar = tk.Frame(self, bg="#090915", height=52)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="  TUGAS REKURSIF", font=("Consolas", 13, "bold"),
                 fg=ACCENT1, bg="#090915").pack(side="left", pady=12)
        tk.Label(topbar, text="Algoritma Rekursif & Backtracking",
                 font=("Consolas", 9), fg=TEXT_SUB, bg="#090915").pack(side="left", padx=10, pady=12)

        # Notebook
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=BG_PANEL, foreground=TEXT_SUB,
                        font=("Consolas", 10, "bold"),
                        padding=[18, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", BG_CARD)],
                  foreground=[("selected", TEXT_MAIN)])

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=0, pady=0)

        tab1 = NQueensApp(self.nb)
        tab2 = KnightsTourApp(self.nb)
        tab3 = KnapsackApp(self.nb)

        self.nb.add(tab1, text="  ♛  N-Queens  ")
        self.nb.add(tab2, text="  ♞  Knight's Tour  ")
        self.nb.add(tab3, text="  🎒  Knapsack  ")

        # Footer
        foot = tk.Frame(self, bg="#090915", height=26)
        foot.pack(fill="x")
        foot.pack_propagate(False)
        tk.Label(foot, text="  Rekursif · Backtracking · Python + Tkinter",
                 font=("Consolas", 8), fg=TEXT_SUB, bg="#090915").pack(side="left")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
