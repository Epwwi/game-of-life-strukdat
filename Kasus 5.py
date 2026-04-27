import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Parameter simulasi
NUM_AGENTS = 2
SIM_TIME = 30
ARRIVAL_PROB = 0.5
SERVICE_TIME = 3

queue = []
agents = [None] * NUM_AGENTS
service_timer = [0] * NUM_AGENTS

passenger_id = 1
history = []

for t in range(SIM_TIME):
    events = {"time": t, "queue": list(queue), "agents": list(agents)}

    # R1: kedatangan
    if random.random() < ARRIVAL_PROB:
        queue.append(f"P{passenger_id}")
        passenger_id += 1

    # R3: selesai layanan
    for i in range(NUM_AGENTS):
        if agents[i] is not None:
            service_timer[i] -= 1
            if service_timer[i] <= 0:
                agents[i] = None

    # R2: mulai layanan
    for i in range(NUM_AGENTS):
        if agents[i] is None and queue:
            agents[i] = queue.pop(0)
            service_timer[i] = SERVICE_TIME

    history.append({
        "queue": list(queue),
        "agents": list(agents)
    })

# ================= VISUALISASI =================
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")

def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    state = history[frame]

    # Judul waktu
    ax.text(4, 5.5, f"Waktu: {frame}", fontsize=14)

    # Gambar antrian
    ax.text(1, 4.5, "Antrian", fontsize=12)
    for i, p in enumerate(state["queue"][:5]):
        ax.text(1 + i*1.2, 3.5, p,
                bbox=dict(facecolor='blue', alpha=0.3),
                ha='center')

    # Gambar agen
    ax.text(1, 2.5, "Loket", fontsize=12)
    for i, agent in enumerate(state["agents"]):
        label = agent if agent else "Kosong"
        color = 'red' if agent else 'green'
        ax.text(1 + i*3, 1.5, f"Agen {i+1}\n{label}",
                bbox=dict(facecolor=color, alpha=0.3),
                ha='center')

ani = animation.FuncAnimation(
    fig, update, frames=len(history), interval=800, repeat=False
)

plt.show()