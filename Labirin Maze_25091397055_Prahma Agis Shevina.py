"""
Tugas Praktikum - Pemecahan Labirin dengan Tumpukan (Stack)
Algoritma: DFS (Depth-First Search) berbasis Stack
Mata Kuliah: Struktur Data - Bab 7 Tumpukan

Cara menjalankan:
    pip install pygame
    python maze_solver.py

Kontrol:
    SPACE  - Mulai / Jeda animasi
    R      - Reset
    +/-    - Tambah/kurangi kecepatan
    Q/ESC  - Keluar
"""

import pygame
import sys

# ─── Implementasi Stack ────────────────────────────────────────────────────────

class Stack:
    """Stack (Tumpukan) - implementasi LIFO menggunakan Python List."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Tambah item ke puncak tumpukan."""
        self._items.append(item)

    def pop(self):
        """Hapus dan kembalikan item puncak."""
        if self.is_empty():
            raise IndexError("pop dari stack kosong")
        return self._items.pop()

    def peek(self):
        """Lihat item puncak tanpa menghapus."""
        if self.is_empty():
            raise IndexError("peek dari stack kosong")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def to_list(self):
        return list(self._items)


# ─── Definisi Labirin ─────────────────────────────────────────────────────────

MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

ROWS  = len(MAZE)
COLS  = len(MAZE[0])
START = (1, 1)
END   = (18, 18)


# ─── Konstanta Tampilan ───────────────────────────────────────────────────────

CELL_SIZE  = 34
SIDEBAR_W  = 280
MARGIN     = 16
HEADER_H   = 70
FOOTER_H   = 50

MAZE_W     = COLS * CELL_SIZE
MAZE_H     = ROWS * CELL_SIZE
WIN_W      = MAZE_W + SIDEBAR_W + MARGIN * 3
WIN_H      = MAZE_H + HEADER_H + FOOTER_H + MARGIN * 2

# Warna
DARK_BG     = (15, 20, 40)
NAVY        = (30, 39, 97)
WALL        = (20, 30, 80)
WALL_BORDER = (40, 55, 130)
PATH_BG     = (230, 235, 248)
PATH_BORDER = (200, 208, 235)
COLOR_START = (29, 158, 117)
COLOR_END   = (249, 168, 37)
COLOR_VISIT = (159, 225, 203)
COLOR_STACK = (240, 153, 123)
COLOR_SOL   = (216, 90, 48)
COLOR_CUR   = (249, 97, 103)
TEXT_WHITE  = (240, 245, 255)
TEXT_MUTED  = (140, 155, 190)
TEXT_GREEN  = (29, 158, 117)
TEXT_ACCENT = (249, 168, 37)
PANEL_BG    = (22, 30, 65)
PANEL_BORD  = (45, 60, 120)
BTN_BG      = (40, 55, 110)
BTN_HOV     = (60, 80, 160)
BTN_ACT     = (29, 158, 117)


# ─── Solver Labirin ────────────────────────────────────────────────────────────

class MazeSolver:
    """Pemecah labirin menggunakan Stack (DFS iteratif)."""

    def __init__(self, maze, start, end):
        self.maze  = maze
        self.start = start
        self.end   = end
        self.rows  = len(maze)
        self.cols  = len(maze[0])
        self.reset()

    def reset(self):
        self.stack    = Stack()
        self.visited  = set()
        self.parent   = {}
        self.solution = set()
        self.steps    = 0
        self.solved   = False
        self.no_sol   = False
        self.finished = False
        self.current  = None

    def start_solve(self):
        self.reset()
        self.stack.push(self.start)
        self.visited.add(self.start)
        self.parent[self.start] = None

    def step(self):
        """
        Lakukan satu langkah DFS.
        Return True jika algoritma masih berjalan, False jika selesai.
        """
        # FIX 1: Cek stack kosong di awal; tandai no_sol dan selesai.
        if self.stack.is_empty():
            self.no_sol   = True
            self.finished = True
            return False

        self.current = self.stack.peek()
        self.steps  += 1

        if self.current == self.end:
            self.solved   = True
            self.finished = True
            self._build_solution()
            return False

        neighbors = self._get_neighbors(*self.current)
        unvisited = [n for n in neighbors if n not in self.visited]

        if unvisited:
            # FIX 2: Ambil tetangga terakhir (bukan pertama) karena stack
            # membalik urutan — dengan begitu eksplorasi berjalan atas→bawah,
            # kiri→kanan secara visual (lebih intuitif).
            nxt = unvisited[-1]
            self.visited.add(nxt)
            self.parent[nxt] = self.current
            self.stack.push(nxt)
        else:
            # Tidak ada tetangga yang belum dikunjungi: backtrack
            self.stack.pop()

        return True

    def _get_neighbors(self, r, c):
        # Urutan: atas, bawah, kiri, kanan
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (0 <= nr < self.rows and 0 <= nc < self.cols
                    and self.maze[nr][nc] == 0):
                result.append((nr, nc))
        return result

    def _build_solution(self):
        cur = self.end
        while cur is not None:
            self.solution.add(cur)
            cur = self.parent.get(cur)


# ─── Aplikasi Utama ───────────────────────────────────────────────────────────

class MazeApp:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(
            "Pemecahan Labirin dengan Tumpukan — Bab 7 Struktur Data"
        )
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        self.clock  = pygame.time.Clock()

        # Font
        self.font_title = pygame.font.SysFont("consolas",   18, bold=True)
        self.font_body  = pygame.font.SysFont("consolas",   13)
        self.font_small = pygame.font.SysFont("consolas",   11)
        self.font_mono  = pygame.font.SysFont("couriernew", 12)
        self.font_big   = pygame.font.SysFont("consolas",   22, bold=True)

        self.solver = MazeSolver(MAZE, START, END)
        self.speed  = 15   # langkah per detik
        self._accum = 0.0
        self.state  = "idle"   # idle | running | paused | done

        # Posisi area labirin & sidebar
        self.maze_x    = MARGIN
        self.maze_y    = HEADER_H + MARGIN
        self.sidebar_x = MAZE_W + MARGIN * 2
        self.sidebar_y = HEADER_H + MARGIN

    # ── Loop Utama ─────────────────────────────────────────────────────────────

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit(); sys.exit()

                elif event.key == pygame.K_SPACE:
                    if self.state == "idle":
                        self.solver.start_solve()
                        self.state = "running"
                    elif self.state == "running":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "running"
                    elif self.state == "done":
                        self._reset()

                elif event.key == pygame.K_r:
                    self._reset()

                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    self.speed = min(60, self.speed + 5)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    self.speed = max(1, self.speed - 5)

    def _reset(self):
        self.solver.reset()
        self.state  = "idle"
        self._accum = 0.0

    def _update(self, dt):
        if self.state != "running":
            return
        self._accum += dt
        interval = 1.0 / self.speed
        while self._accum >= interval:
            self._accum -= interval
            still_going = self.solver.step()
            if not still_going:
                self.state = "done"
                break

    # ── Gambar ─────────────────────────────────────────────────────────────────

    def _draw(self):
        self.screen.fill(DARK_BG)
        self._draw_header()
        self._draw_maze()
        self._draw_sidebar()
        self._draw_footer()
        pygame.display.flip()

    def _draw_header(self):
        title = self.font_big.render(
            "Pemecahan Labirin dengan Tumpukan (Stack)", True, TEXT_WHITE
        )
        sub = self.font_body.render(
            "Algoritma DFS — SPACE: Mulai/Jeda  |  R: Reset  |  +/-: Kecepatan  |  Q: Keluar",
            True, TEXT_MUTED
        )
        self.screen.blit(title, (MARGIN, 14))
        self.screen.blit(sub,   (MARGIN, 44))

    def _draw_maze(self):
        mx, my    = self.maze_x, self.maze_y
        stack_set = set(self.solver.stack.to_list())

        for r in range(ROWS):
            for c in range(COLS):
                x   = mx + c * CELL_SIZE
                y   = my + r * CELL_SIZE
                pos = (r, c)
                cell = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                if MAZE[r][c] == 1:
                    pygame.draw.rect(self.screen, WALL, cell)
                    pygame.draw.rect(self.screen, WALL_BORDER, cell, 1)
                elif pos == END:
                    pygame.draw.rect(self.screen, COLOR_END, cell)
                elif pos == START:
                    pygame.draw.rect(self.screen, COLOR_START, cell)
                elif self.solver.solution and pos in self.solver.solution:
                    pygame.draw.rect(self.screen, COLOR_SOL, cell)
                # FIX 3: Gambar posisi saat ini (current) sebelum stack/visited
                # supaya titik merah selalu terlihat di atas sel lain.
                elif pos == self.solver.current and not self.solver.finished:
                    pygame.draw.rect(self.screen, COLOR_CUR, cell)
                elif pos in stack_set:
                    pygame.draw.rect(self.screen, COLOR_STACK, cell)
                elif pos in self.solver.visited:
                    pygame.draw.rect(self.screen, COLOR_VISIT, cell)
                else:
                    pygame.draw.rect(self.screen, PATH_BG, cell)
                    pygame.draw.rect(self.screen, PATH_BORDER, cell, 1)

        # Label S dan E (selalu di atas)
        self._draw_cell_label(
            mx + START[1] * CELL_SIZE, my + START[0] * CELL_SIZE, "S", (255, 255, 255)
        )
        self._draw_cell_label(
            mx + END[1]   * CELL_SIZE, my + END[0]   * CELL_SIZE, "E", NAVY
        )

        # Border labirin
        maze_rect = pygame.Rect(mx, my, MAZE_W, MAZE_H)
        pygame.draw.rect(self.screen, PANEL_BORD, maze_rect, 2)

    def _draw_cell_label(self, x, y, text, color):
        lbl = self.font_small.render(text, True, color)
        lx  = x + (CELL_SIZE - lbl.get_width())  // 2
        ly  = y + (CELL_SIZE - lbl.get_height()) // 2
        self.screen.blit(lbl, (lx, ly))

    def _draw_sidebar(self):
        sx, sy  = self.sidebar_x, self.sidebar_y
        panel_h = MAZE_H

        # Panel background
        panel = pygame.Rect(sx, sy, SIDEBAR_W, panel_h)
        pygame.draw.rect(self.screen, PANEL_BG,   panel, border_radius=8)
        pygame.draw.rect(self.screen, PANEL_BORD, panel, 1, border_radius=8)

        y = sy + 12

        # ─ Status ─
        status_map = {
            "idle":    ("● Siap",         TEXT_MUTED),
            "running": ("▶ Berjalan...",   (100, 220, 150)),
            "paused":  ("⏸ Dijeda",        TEXT_ACCENT),
            "done":    (
                "✓ Selesai!" if self.solver.solved else "✗ Tidak ada solusi",
                TEXT_GREEN  if self.solver.solved else (220, 80, 80)
            ),
        }
        status_text, status_color = status_map[self.state]
        stat_lbl = self.font_title.render(status_text, True, status_color)
        self.screen.blit(stat_lbl, (sx + 12, y))
        y += 30

        # ─ Statistik ─
        self._sidebar_divider(sx, y, SIDEBAR_W); y += 10
        stats = [
            ("Langkah",      str(self.solver.steps)),
            ("Dikunjungi",   str(len(self.solver.visited))),
            ("Ukuran Stack", str(len(self.solver.stack))),
            ("Kecepatan",    f"{self.speed} step/s"),
        ]
        for label, val in stats:
            lbl_s = self.font_body.render(label, True, TEXT_MUTED)
            val_s = self.font_body.render(val,   True, TEXT_WHITE)
            self.screen.blit(lbl_s, (sx + 12, y))
            self.screen.blit(val_s, (sx + SIDEBAR_W - val_s.get_width() - 12, y))
            y += 20

        if self.solver.solved:
            sol_lbl = self.font_body.render("Panjang Solusi", True, TEXT_MUTED)
            sol_val = self.font_body.render(str(len(self.solver.solution)), True, TEXT_ACCENT)
            self.screen.blit(sol_lbl, (sx + 12, y))
            self.screen.blit(sol_val, (sx + SIDEBAR_W - sol_val.get_width() - 12, y))
            y += 20

        y += 8
        self._sidebar_divider(sx, y, SIDEBAR_W); y += 10

        # ─ Legenda ─
        legend_title = self.font_body.render("LEGENDA", True, TEXT_MUTED)
        self.screen.blit(legend_title, (sx + 12, y)); y += 20

        legends = [
            (COLOR_START, "Titik Awal (S)"),
            (COLOR_END,   "Titik Keluar (E)"),
            (COLOR_CUR,   "Posisi saat ini"),
            (COLOR_VISIT, "Sudah dikunjungi"),
            (COLOR_STACK, "Ada di Stack"),
            (COLOR_SOL,   "Jalur solusi"),
        ]
        for color, text in legends:
            box = pygame.Rect(sx + 12, y + 2, 14, 14)
            pygame.draw.rect(self.screen, color, box, border_radius=3)
            t = self.font_small.render(text, True, TEXT_MUTED)
            self.screen.blit(t, (sx + 32, y))
            y += 18

        y += 6
        self._sidebar_divider(sx, y, SIDEBAR_W); y += 10

        # ─ Isi Stack (dari puncak ke bawah) ─
        stack_title = self.font_body.render(
            f"ISI STACK  [{len(self.solver.stack)}]", True, TEXT_MUTED
        )
        self.screen.blit(stack_title, (sx + 12, y)); y += 20

        stack_list = self.solver.stack.to_list()
        max_show   = max(1, (sy + panel_h - 16 - y) // 16)
        items_show = stack_list[-max_show:] if len(stack_list) > max_show else stack_list

        # FIX 4: Gunakan is_empty() sebelum peek() untuk hindari IndexError
        top_item = self.solver.stack.peek() if not self.solver.stack.is_empty() else None

        for i, item in enumerate(reversed(items_show)):
            is_top    = (i == 0 and item == top_item)
            bg        = COLOR_START if is_top else (35, 50, 100)
            tc        = TEXT_WHITE  if is_top else (100, 200, 160)
            item_rect = pygame.Rect(sx + 12, y, SIDEBAR_W - 24, 14)
            pygame.draw.rect(self.screen, bg, item_rect, border_radius=3)
            arrow = "→ " if is_top else "  "
            txt = self.font_mono.render(f"{arrow}({item[0]}, {item[1]})", True, tc)
            self.screen.blit(txt, (sx + 16, y))
            y += 16
            if y > sy + panel_h - 16:
                break

    def _sidebar_divider(self, x, y, w):
        pygame.draw.line(self.screen, PANEL_BORD, (x + 8, y), (x + w - 8, y), 1)

    def _draw_footer(self):
        # FIX 5: Hitung fy dengan benar (header + margin atas + maze + margin bawah)
        fy = HEADER_H + MARGIN + MAZE_H + MARGIN

        hints = [
            ("[SPACE]", "Mulai / Jeda / Lanjut"),
            ("[R]",     "Reset"),
            ("[+/-]",   "Kecepatan"),
            ("[Q/ESC]", "Keluar"),
        ]
        x = MARGIN
        for key_lbl, desc in hints:
            k = self.font_body.render(key_lbl, True, TEXT_ACCENT)
            d = self.font_small.render(f" {desc}  ", True, TEXT_MUTED)
            self.screen.blit(k, (x, fy + 16))
            x += k.get_width()
            self.screen.blit(d, (x, fy + 18))
            x += d.get_width() + 8


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = MazeApp()
    app.run()