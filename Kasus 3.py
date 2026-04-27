import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Data pasien: (nama, prioritas)
# 0 = kritis, 1 = darurat, 2 = menengah, 3 = ringan
patients = [
    ("Budi", 3),
    ("Ani", 0),
    ("Citra", 2),
    ("Dedi", 0),
    ("Eka", 1)
]

# Urutkan berdasarkan prioritas + urutan datang (FIFO untuk prioritas sama)
queue = sorted(enumerate(patients), key=lambda x: (x[1][1], x[0]))
queue = [p[1] for p in queue]

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.set_title("Simulasi Antrian Rumah Sakit (Priority Queue)")
ax.axis("off")

texts = []

def init():
    return texts

def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_title("Simulasi Antrian Rumah Sakit (Priority Queue)")
    ax.axis("off")

    # Tampilkan pasien yang sedang dilayani
    if frame < len(queue):
        name, prio = queue[frame]
        ax.text(4, 3, f"Sedang dilayani:\n{name} (P{prio})",
                fontsize=14, ha='center', bbox=dict(facecolor='red', alpha=0.3))

    # Tampilkan antrian tersisa
    for i in range(frame + 1, len(queue)):
        name, prio = queue[i]
        ax.text(1 + (i-frame-1)*2, 1, f"{name}\nP{prio}",
                fontsize=12, bbox=dict(facecolor='blue', alpha=0.2))

    return texts

ani = animation.FuncAnimation(fig, update, frames=len(queue),
                              init_func=init, interval=1500, repeat=False)

plt.show()