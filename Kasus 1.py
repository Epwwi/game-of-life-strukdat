import tkinter as tk
from tkinter import ttk
from collections import deque
import time
import threading

# ── Data ──────────────────────────────────────────────────────────────────────
DOCUMENTS = [
    ("laporan.pdf",      "📄"),
    ("tugas.docx",       "📝"),
    ("foto.jpg",         "🖼"),
    ("presentasi.pptx",  "📊"),
    ("data.xlsx",        "📋"),
    ("memo.txt",         "📃"),
]

# ── Warna ─────────────────────────────────────────────────────────────────────
BG         = "#F5F5F0"
WHITE      = "#FFFFFF"
BLUE_LIGHT = "#E6F1FB"
BLUE_MID   = "#378ADD"
BLUE_DARK  = "#0C447C"
GREEN      = "#3B6D11"
GREEN_LIGHT= "#EAF3DE"
ORANGE     = "#EF9F27"
GRAY_BORDER= "#CCCCCC"
GRAY_BG    = "#FAFAFA"
TEXT_MAIN  = "#1A1A1A"
TEXT_MUTED = "#888888"

# ── Aplikasi Utama ─────────────────────────────────────────────────────────────
class PrinterQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Antrian Printer Bersama — Queue FIFO")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.queue    = deque()
        self.output   = []
        self.doc_idx  = 0
        self.printing = False
        self.auto_running = False

        self._build_ui()

    # ── Build UI ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        pad = {"padx": 16, "pady": 8}

        # Judul
        tk.Label(self.root, text="Antrian Printer Bersama",
                 font=("Helvetica", 16, "bold"), bg=BG, fg=TEXT_MAIN
                 ).grid(row=0, column=0, columnspan=3, sticky="w", padx=16, pady=(16, 0))
        tk.Label(self.root, text="Struktur data Queue · FIFO — dokumen pertama masuk, pertama dicetak",
                 font=("Helvetica", 11), bg=BG, fg=TEXT_MUTED
                 ).grid(row=1, column=0, columnspan=3, sticky="w", padx=16, pady=(0, 12))

        # ── Kolom kiri: Antrian ────────────────────────────────────────────────
        tk.Label(self.root, text="ANTRIAN", font=("Helvetica", 10, "bold"),
                 bg=BG, fg=TEXT_MUTED).grid(row=2, column=0, sticky="w", padx=16)

        self.queue_frame = tk.Frame(self.root, bg=GRAY_BG,
                                    highlightbackground=GRAY_BORDER,
                                    highlightthickness=1, width=280, height=260)
        self.queue_frame.grid(row=3, column=0, padx=16, pady=4, sticky="nsew")
        self.queue_frame.grid_propagate(False)

        self.queue_canvas = tk.Canvas(self.queue_frame, bg=GRAY_BG,
                                      highlightthickness=0, width=276, height=256)
        self.queue_canvas.pack(fill="both", expand=True)
        self.queue_canvas.bind("<Configure>", lambda e: self._render_queue_canvas())

        # ── Kolom tengah: Printer ──────────────────────────────────────────────
        tk.Label(self.root, text="PRINTER", font=("Helvetica", 10, "bold"),
                 bg=BG, fg=TEXT_MUTED).grid(row=2, column=1, sticky="w", padx=8)

        self.printer_canvas = tk.Canvas(self.root, width=180, height=160,
                                         bg=BG, highlightthickness=0)
        self.printer_canvas.grid(row=3, column=1, padx=8, pady=4)
        self._draw_printer()

        self.status_var = tk.StringVar(value="Siap")
        tk.Label(self.root, textvariable=self.status_var,
                 font=("Helvetica", 11), bg=BG, fg=TEXT_MUTED
                 ).grid(row=4, column=1)

        # ── Kolom kanan: Output ────────────────────────────────────────────────
        tk.Label(self.root, text="OUTPUT", font=("Helvetica", 10, "bold"),
                 bg=BG, fg=TEXT_MUTED).grid(row=2, column=2, sticky="w", padx=16)

        self.output_frame = tk.Frame(self.root, bg=WHITE,
                                     highlightbackground=GRAY_BORDER,
                                     highlightthickness=1, width=220, height=260)
        self.output_frame.grid(row=3, column=2, padx=16, pady=4, sticky="nsew")
        self.output_frame.grid_propagate(False)

        self.output_canvas = tk.Canvas(self.output_frame, bg=WHITE,
                                       highlightthickness=0, width=216, height=256)
        self.output_canvas.pack(fill="both", expand=True)

        # ── Tombol ────────────────────────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.grid(row=5, column=0, columnspan=3, padx=16, pady=8, sticky="w")

        style = {"font": ("Helvetica", 12), "relief": "flat",
                 "cursor": "hand2", "padx": 14, "pady": 6, "bd": 1}

        self.btn_enq = tk.Button(btn_frame, text="+ Kirim Dokumen",
                                  bg=BLUE_LIGHT, fg=BLUE_DARK,
                                  command=self.enqueue_doc,
                                  highlightbackground=BLUE_MID, **style)
        self.btn_enq.pack(side="left", padx=(0, 6))

        self.btn_print = tk.Button(btn_frame, text="▶  Cetak Berikutnya",
                                    bg=WHITE, fg=TEXT_MAIN,
                                    command=self.print_next,
                                    highlightbackground=GRAY_BORDER, **style)
        self.btn_print.pack(side="left", padx=(0, 6))

        self.btn_auto = tk.Button(btn_frame, text="⚡ Auto Print",
                                   bg=WHITE, fg=TEXT_MAIN,
                                   command=self.toggle_auto,
                                   highlightbackground=GRAY_BORDER, **style)
        self.btn_auto.pack(side="left", padx=(0, 6))

        tk.Button(btn_frame, text="↺  Reset",
                  bg="#FCEBEB", fg="#A32D2D",
                  command=self.reset_all,
                  highlightbackground="#E24B4A", **style
                  ).pack(side="left")

        # ── Log ───────────────────────────────────────────────────────────────
        self.log_var = tk.StringVar(value='Tekan "+ Kirim Dokumen" untuk mulai…')
        tk.Label(self.root, textvariable=self.log_var,
                 font=("Courier", 11), bg="#F0F0F0", fg="#555555",
                 anchor="w", relief="flat", padx=10, pady=6,
                 wraplength=680
                 ).grid(row=6, column=0, columnspan=3,
                        padx=16, pady=(0, 16), sticky="ew")

        self._render_queue_canvas()
        self._render_output_canvas()

    # ── Gambar Printer (Canvas SVG-style) ──────────────────────────────────────
    def _draw_printer(self, led_color="#9FE1CB", paper_x=None):
        c = self.printer_canvas
        c.delete("all")
        # Badan printer
        c.create_rectangle(20, 55, 160, 130, fill="#ECECEC",
                            outline=GRAY_BORDER, width=1)
        # Slot atas (paper tray)
        c.create_rectangle(35, 40, 145, 60, fill=WHITE,
                            outline=GRAY_BORDER, width=1)
        c.create_rectangle(45, 45, 135, 57, fill="#E8E8E8", outline="")
        # LED
        c.create_oval(133, 78, 143, 88, fill=led_color, outline="")
        # Slot keluar (bawah)
        c.create_rectangle(50, 105, 130, 120, fill="#E8E8E8", outline="")
        c.create_line(50, 113, 130, 113, fill=GRAY_BORDER)
        # Kertas animasi
        if paper_x is not None:
            c.create_rectangle(paper_x, 43, paper_x + 80, 53,
                                fill=WHITE, outline=GRAY_BORDER, width=1)

    def _animate_paper(self, doc_name, on_done):
        """Animasi kertas masuk ke printer (thread terpisah)."""
        steps = 12
        for i in range(steps + 1):
            x = 160 - int((160 / steps) * i)   # kanan → kiri
            self.root.after(0, lambda px=x: self._draw_printer(
                led_color=ORANGE, paper_x=px))
            time.sleep(0.07)
        time.sleep(0.4)
        self.root.after(0, lambda: self._draw_printer(led_color="#9FE1CB"))
        self.root.after(0, on_done)

    # ── Render Antrian ─────────────────────────────────────────────────────────
    def _render_queue_canvas(self):
        c = self.queue_canvas
        c.delete("all")
        if not self.queue:
            c.create_text(138, 120, text="Antrian kosong",
                          fill=GRAY_BORDER, font=("Helvetica", 12))
            return
        for i, (name, icon) in enumerate(self.queue):
            y = 12 + i * 52
            is_first = (i == 0)
            fill   = BLUE_LIGHT if is_first else WHITE
            border = BLUE_MID   if is_first else GRAY_BORDER
            fg     = BLUE_DARK  if is_first else TEXT_MAIN

            c.create_rectangle(10, y, 266, y + 42,
                                fill=fill, outline=border, width=1)
            c.create_text(28, y + 21, text=icon,
                          font=("Helvetica", 16), anchor="w")
            c.create_text(54, y + 21, text=name,
                          font=("Helvetica", 12, "bold"),
                          fill=fg, anchor="w")
            badge = "NEXT" if is_first else f"#{i+1}"
            badge_bg = "#B5D4F4" if is_first else "#F0F0F0"
            badge_fg = "#042C53" if is_first else TEXT_MUTED
            c.create_rectangle(200, y + 11, 258, y + 31,
                                fill=badge_bg, outline="")
            c.create_text(229, y + 21, text=badge,
                          font=("Helvetica", 10, "bold"),
                          fill=badge_fg, anchor="center")

    # ── Render Output ──────────────────────────────────────────────────────────
    def _render_output_canvas(self):
        c = self.output_canvas
        c.delete("all")
        if not self.output:
            c.create_text(108, 30, text="—", fill=GRAY_BORDER,
                          font=("Helvetica", 14))
            return
        for i, (name, icon) in enumerate(self.output):
            y = 8 + i * 42
            c.create_rectangle(6, y, 210, y + 34,
                                fill=GREEN_LIGHT, outline=GRAY_BORDER, width=1)
            c.create_text(20, y + 17, text=icon,
                          font=("Helvetica", 14), anchor="w")
            c.create_text(44, y + 17, text=name,
                          font=("Helvetica", 11), fill=GREEN, anchor="w")
            c.create_text(200, y + 17, text="✓",
                          font=("Helvetica", 12, "bold"),
                          fill=GREEN, anchor="e")

    # ── Logika Queue ───────────────────────────────────────────────────────────
    def enqueue_doc(self):
        doc = DOCUMENTS[self.doc_idx % len(DOCUMENTS)]
        self.doc_idx += 1
        self.queue.append(doc)
        self._render_queue_canvas()
        self.log_var.set(
            f'enqueue("{doc[0]}") → ditambahkan ke antrian [pos #{len(self.queue)}]')

    def print_next(self):
        if self.printing or not self.queue:
            return
        self.printing = True
        self.btn_print.config(state="disabled")
        self.btn_enq.config(state="disabled")

        doc = self.queue[0]
        self.status_var.set(f"Mencetak: {doc[0]}")
        self.log_var.set(f'dequeue() → "{doc[0]}" mulai dicetak…')

        def on_done():
            self.queue.popleft()
            self.output.append(doc)
            self._render_queue_canvas()
            self._render_output_canvas()
            sisa = len(self.queue)
            self.status_var.set("Selesai · siap" if sisa == 0 else "Siap")
            self.log_var.set(
                f'✓ "{doc[0]}" selesai dicetak · sisa antrian: {sisa}')
            self.printing = False
            self.btn_print.config(state="normal")
            self.btn_enq.config(state="normal")

        t = threading.Thread(target=self._animate_paper,
                             args=(doc[0], on_done), daemon=True)
        t.start()

    def toggle_auto(self):
        if self.auto_running:
            self.auto_running = False
            self.btn_auto.config(text="⚡ Auto Print")
            return
        if not self.queue:
            for _ in range(3):
                self.enqueue_doc()
        self.auto_running = True
        self.btn_auto.config(text="⏹  Stop Auto")
        self._auto_step()

    def _auto_step(self):
        if not self.auto_running:
            return
        if self.queue and not self.printing:
            self.print_next()
            self.root.after(1800, self._auto_step)
        elif not self.queue and not self.printing:
            self.auto_running = False
            self.btn_auto.config(text="⚡ Auto Print")
        else:
            self.root.after(300, self._auto_step)

    def reset_all(self):
        self.auto_running = False
        self.btn_auto.config(text="⚡ Auto Print")
        self.printing = False
        self.queue.clear()
        self.output.clear()
        self.doc_idx = 0
        self.btn_enq.config(state="normal")
        self.btn_print.config(state="normal")
        self._draw_printer()
        self._render_queue_canvas()
        self._render_output_canvas()
        self.status_var.set("Siap")
        self.log_var.set("Reset — antrian dikosongkan.")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = PrinterQueueApp(root)
    root.mainloop()