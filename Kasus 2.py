"""
Hot Potato Game - Visualisasi dengan Pygame
Simulasi permainan menggunakan Circular Queue

Instalasi:
    pip install pygame

Jalankan:
    python hot_potato.py
"""

import pygame
import math
import sys
import time
from collections import deque

# ── Konfigurasi ──────────────────────────────────────────────
WIDTH, HEIGHT = 800, 600
FPS = 60
CIRCLE_RADIUS = 180
CENTER = (WIDTH // 2, HEIGHT // 2 - 20)

# Warna
BG         = (15, 15, 25)
BG2        = (25, 25, 40)
WHITE      = (255, 255, 255)
GRAY       = (100, 100, 110)
GRAY_DIM   = (50, 50, 60)
AMBER      = (240, 160, 50)
AMBER_DIM  = (120, 80, 25)
RED        = (200, 60, 60)
GREEN      = (80, 200, 120)
PANEL_BG   = (30, 30, 48)
BORDER     = (60, 60, 80)

PLAYER_COLORS = [
    (79,  134, 216),
    (224, 112,  64),
    (92,  184, 122),
    (192, 111, 192),
    (212, 160,  32),
    (60,  188, 188),
    (160,  64,  64),
    (112, 112, 208),
    (80,  160,  96),
    (192,  80, 144),
]

# ── Queue (Circular) ─────────────────────────────────────────
class CircularQueue:
    def __init__(self, names):
        self.q = deque(names)

    def enqueue(self, item):
        self.q.append(item)

    def dequeue(self):
        return self.q.popleft()

    def front(self):
        return self.q[0]

    def next_front(self):
        return self.q[1] if len(self.q) > 1 else None

    def pass_potato(self):
        """Dequeue depan, enqueue ke belakang (oper melingkar)"""
        item = self.dequeue()
        self.enqueue(item)
        return item

    def eliminate(self):
        """Tersingkir: dequeue tanpa enqueue kembali"""
        return self.dequeue()

    def __len__(self):
        return len(self.q)

    def to_list(self):
        return list(self.q)


# ── State Permainan ──────────────────────────────────────────
class HotPotatoGame:
    def __init__(self, num_players=6, n_pass=4):
        self.num_players = num_players
        self.n_pass = n_pass
        self.reset()

    def reset(self):
        names = [chr(65 + i) for i in range(self.num_players)]
        self.all_players = {
            name: {
                "name": name,
                "color": PLAYER_COLORS[i % len(PLAYER_COLORS)],
                "alive": True,
                "angle": (2 * math.pi * i / self.num_players) - math.pi / 2,
                "scale": 1.0,
            }
            for i, name in enumerate(names)
        }
        self.queue = CircularQueue(names)
        self.pass_count = 0
        self.round = 0
        self.eliminated = []
        self.winner = None
        self.log = "Tekan SPACE untuk oper, E untuk eliminasi, A untuk auto, R untuk reset."
        self.phase = "idle"   # idle | playing | done
        self.auto_mode = False
        self.auto_timer = 0
        self.auto_interval = 0.45   # detik per langkah auto
        self.potato_pos = None      # (x, y) untuk animasi kentang
        self.anim_t = 1.0           # 0.0 → 1.0, selesai saat 1.0
        self.anim_from = None
        self.anim_to = None
        self.anim_speed = 2.5       # satuan per detik (fraksi)

    def player_pos(self, name):
        p = self.all_players[name]
        cx, cy = CENTER
        x = cx + CIRCLE_RADIUS * math.cos(p["angle"])
        y = cy + CIRCLE_RADIUS * math.sin(p["angle"])
        return (int(x), int(y))

    def start(self):
        self.phase = "playing"
        self.log = f"Permainan dimulai! N={self.n_pass} kali oper sebelum tersingkir."

    def do_pass(self):
        if self.phase != "playing" or len(self.queue) < 2 or self.anim_t < 1.0:
            return
        src = self.queue.front()
        self.queue.pass_potato()
        dst = self.queue.front()
        self.pass_count += 1
        self.log = f"Pemain {src} mengoper ke {dst}  (oper ke-{self.pass_count}/{self.n_pass})"
        # Mulai animasi
        self.anim_from = src
        self.anim_to   = dst
        self.anim_t    = 0.0

    def do_eliminate(self):
        if self.phase != "playing" or len(self.queue) < 2 or self.anim_t < 1.0:
            return
        if self.pass_count < self.n_pass:
            self.log = f"Belum cukup! Harus {self.n_pass} kali oper dulu."
            return
        elim = self.queue.eliminate()
        self.all_players[elim]["alive"] = False
        self.all_players[elim]["scale"] = 0.55
        self.eliminated.append(elim)
        self.pass_count = 0
        self.round += 1
        self.log = f"🔥 Pemain {elim} TERSINGKIR! (ronde {self.round})"
        if len(self.queue) == 1:
            self.winner = self.queue.front()
            self.phase = "done"
            self.auto_mode = False
            self.log = f"🏆 Pemenang: Pemain {self.winner}!"

    def do_step(self):
        """Satu langkah penuh: N kali oper lalu eliminasi (untuk auto)."""
        if self.pass_count < self.n_pass:
            self.do_pass()
        else:
            self.do_eliminate()

    def update(self, dt):
        if self.anim_t < 1.0:
            self.anim_t = min(1.0, self.anim_t + self.anim_speed * dt)
        if self.auto_mode and self.phase == "playing" and self.anim_t >= 1.0:
            self.auto_timer += dt
            if self.auto_timer >= self.auto_interval:
                self.auto_timer = 0
                self.do_step()


# ── Utilitas Gambar ──────────────────────────────────────────
def lerp(a, b, t):
    return a + (b - a) * t

def draw_circle_aa(surface, color, pos, radius, width=0):
    pygame.draw.circle(surface, color, pos, radius, width)

def draw_text(surface, text, font, color, pos, anchor="center"):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if anchor == "center":
        rect.center = pos
    elif anchor == "midleft":
        rect.midleft = pos
    elif anchor == "midright":
        rect.midright = pos
    elif anchor == "topleft":
        rect.topleft = pos
    surface.blit(surf, rect)

def ease_out(t):
    return 1 - (1 - t) ** 3

def ease_in_out(t):
    return t * t * (3 - 2 * t)


# ── Render Utama ─────────────────────────────────────────────
def draw_game(surface, game, fonts):
    font_lg  = fonts["lg"]
    font_md  = fonts["md"]
    font_sm  = fonts["sm"]
    font_xs  = fonts["xs"]

    surface.fill(BG)

    # Panel kiri: info
    panel_rect = pygame.Rect(0, 0, 210, HEIGHT)
    pygame.draw.rect(surface, PANEL_BG, panel_rect)
    pygame.draw.line(surface, BORDER, (210, 0), (210, HEIGHT), 1)

    draw_text(surface, "Hot Potato", font_lg, WHITE, (105, 28), "center")
    draw_text(surface, "Circular Queue", font_xs, GRAY, (105, 52), "center")

    # Divider
    pygame.draw.line(surface, BORDER, (16, 66), (194, 66), 1)

    # Statistik
    stats = [
        ("Pemain aktif", str(len(game.queue))),
        ("Ronde",        str(game.round)),
        ("Oper ke-",     f"{game.pass_count} / {game.n_pass}"),
        ("Tersingkir",   ", ".join(game.eliminated) if game.eliminated else "-"),
    ]
    y0 = 80
    for label, val in stats:
        draw_text(surface, label, font_xs, GRAY,  (18, y0),      "midleft")
        draw_text(surface, val,   font_sm, WHITE, (192, y0),     "midright")
        y0 += 28

    # Antrian
    pygame.draw.line(surface, BORDER, (16, y0 + 4), (194, y0 + 4), 1)
    y0 += 16
    draw_text(surface, "Antrian Queue", font_xs, GRAY, (18, y0), "midleft")
    y0 += 22
    q_list = game.queue.to_list()
    for i, name in enumerate(q_list[:8]):
        p = game.all_players[name]
        col = tuple(c // 2 for c in p["color"]) if i > 0 else p["color"]
        label = f"[{i}] {name}" + (" ← pemegang" if i == 0 else "")
        draw_text(surface, label, font_xs, col, (18, y0), "midleft")
        y0 += 18
    if len(q_list) > 8:
        draw_text(surface, f"... +{len(q_list)-8} lagi", font_xs, GRAY, (18, y0), "midleft")

    # Divider bawah
    pygame.draw.line(surface, BORDER, (16, HEIGHT - 100), (194, HEIGHT - 100), 1)

    # Kontrol
    ctrl = [
        ("SPACE", "Oper kentang"),
        ("E",     "Eliminasi"),
        ("A",     "Auto on/off"),
        ("R",     "Reset"),
        ("+/-",   "Ubah pemain"),
        ("N/M",   "Ubah N pass"),
    ]
    yc = HEIGHT - 94
    for key, desc in ctrl:
        draw_text(surface, f"{key}", font_xs, AMBER,  (18, yc),  "midleft")
        draw_text(surface, desc,     font_xs, GRAY,   (50, yc),  "midleft")
        yc += 16

    # ── Area permainan ──────────────────────────────────────
    # Lingkaran panduan
    pygame.draw.circle(surface, (40, 40, 60), CENTER, CIRCLE_RADIUS, 1)

    # Garis oper (saat animasi)
    if game.anim_t < 1.0 and game.anim_from and game.anim_to:
        p1 = game.player_pos(game.anim_from)
        p2 = game.player_pos(game.anim_to)
        t  = ease_out(game.anim_t)
        pygame.draw.line(surface, AMBER_DIM, p1, p2, 2)

    # Pemain
    for name, p in game.all_players.items():
        pos = game.player_pos(name)
        r   = int(28 * p["scale"])
        col = p["color"] if p["alive"] else GRAY_DIM

        # Highlight holder
        if game.phase == "playing" and len(game.queue) > 0 and game.queue.front() == name and game.anim_t >= 1.0:
            glow_col = tuple(min(255, c + 60) for c in col)
            pygame.draw.circle(surface, glow_col, pos, r + 10, 2)

        # Lingkaran pemain
        pygame.draw.circle(surface, col, pos, r)
        border_col = tuple(min(255, c + 60) for c in col) if p["alive"] else (60, 60, 70)
        pygame.draw.circle(surface, border_col, pos, r, 2)

        # Label nama
        draw_text(surface, name, font_md if p["alive"] else font_sm, WHITE if p["alive"] else GRAY, pos, "center")

        # Tanda eliminasi
        if not p["alive"]:
            ex, ey = pos[0], pos[1] + r + 12
            draw_text(surface, "✕", font_xs, RED, (ex, ey), "center")

    # ── Kentang ─────────────────────────────────────────────
    if game.phase != "idle" and game.winner is None:
        if game.anim_t < 1.0 and game.anim_from and game.anim_to:
            p1 = game.player_pos(game.anim_from)
            p2 = game.player_pos(game.anim_to)
            t  = ease_in_out(game.anim_t)
            # Parabola lompatan
            arc_h = -50 * math.sin(math.pi * t)
            px = int(lerp(p1[0], p2[0], t))
            py = int(lerp(p1[1], p2[1], t) + arc_h)
        else:
            if len(game.queue) > 0:
                hpos = game.player_pos(game.queue.front())
                px, py = hpos[0], hpos[1] - 36
            else:
                px, py = -999, -999

        if px > 0:
            # Badan kentang (oval)
            potato_rect = pygame.Rect(px - 14, py - 11, 28, 22)
            pygame.draw.ellipse(surface, (180, 110, 40), potato_rect)
            pygame.draw.ellipse(surface, (120, 70, 20), potato_rect, 2)
            # Bintik-bintik
            for dx, dy in [(-5, -3), (4, -2), (0, 4)]:
                pygame.draw.circle(surface, (100, 55, 15), (px + dx, py + dy), 2)
            # Uap (saat tidak terbang)
            if game.anim_t >= 1.0:
                t_now = pygame.time.get_ticks() / 1000
                for si, sx in enumerate([-4, 0, 4]):
                    off = math.sin(t_now * 3 + si) * 2
                    pygame.draw.line(surface, (180, 180, 180, 80),
                                     (px + sx, py - 12),
                                     (px + sx + int(off), py - 22), 1)

    # ── Pemenang banner ──────────────────────────────────────
    if game.winner:
        bw, bh = 320, 64
        bx = WIDTH // 2 - bw // 2 + 105
        by = HEIGHT - 80
        pygame.draw.rect(surface, (20, 80, 40), (bx, by, bw, bh), border_radius=12)
        pygame.draw.rect(surface, GREEN, (bx, by, bw, bh), 2, border_radius=12)
        draw_text(surface, f"🏆 Pemenang: Pemain {game.winner}!", font_md, GREEN, (bx + bw // 2, by + bh // 2), "center")

    # ── Log / Status ─────────────────────────────────────────
    log_y = HEIGHT - 32
    log_bg = pygame.Rect(220, log_y - 14, WIDTH - 230, 28)
    pygame.draw.rect(surface, PANEL_BG, log_bg, border_radius=6)
    pygame.draw.rect(surface, BORDER,   log_bg, 1, border_radius=6)
    draw_text(surface, game.log, font_xs, WHITE, (log_bg.centerx, log_bg.centery), "center")

    # Auto indicator
    if game.auto_mode:
        draw_text(surface, "● AUTO", font_xs, GREEN, (WIDTH - 20, 14), "midright")

    # Config atas kanan
    cfg = f"Pemain: {game.num_players}  |  N-pass: {game.n_pass}"
    draw_text(surface, cfg, font_xs, GRAY, (WIDTH - 20, HEIGHT - 14), "midright")


# ── Main ─────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hot Potato – Circular Queue Visualizer")
    clock = pygame.time.Clock()

    fonts = {
        "lg":  pygame.font.SysFont("Arial", 18, bold=True),
        "md":  pygame.font.SysFont("Arial", 14, bold=True),
        "sm":  pygame.font.SysFont("Arial", 13),
        "xs":  pygame.font.SysFont("Arial", 12),
    }

    num_players = 6
    n_pass      = 4
    game = HotPotatoGame(num_players, n_pass)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    if game.phase == "idle":
                        game.start()
                    elif game.phase == "playing":
                        game.do_pass()

                elif event.key == pygame.K_e:
                    if game.phase == "playing":
                        game.do_eliminate()

                elif event.key == pygame.K_a:
                    if game.phase == "idle":
                        game.start()
                    if game.phase == "playing":
                        game.auto_mode = not game.auto_mode
                        game.auto_timer = 0
                        status = "ON" if game.auto_mode else "OFF"
                        game.log = f"Mode auto: {status}"

                elif event.key == pygame.K_r:
                    game.auto_mode = False
                    game = HotPotatoGame(num_players, n_pass)

                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    num_players = min(10, num_players + 1)
                    game = HotPotatoGame(num_players, n_pass)

                elif event.key == pygame.K_MINUS:
                    num_players = max(3, num_players - 1)
                    game = HotPotatoGame(num_players, n_pass)

                elif event.key == pygame.K_n:
                    n_pass = max(1, n_pass - 1)
                    game = HotPotatoGame(num_players, n_pass)
                    game.log = f"N-pass diubah ke {n_pass}"

                elif event.key == pygame.K_m:
                    n_pass = min(15, n_pass + 1)
                    game = HotPotatoGame(num_players, n_pass)
                    game.log = f"N-pass diubah ke {n_pass}"

        game.update(dt)
        draw_game(screen, game, fonts)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()