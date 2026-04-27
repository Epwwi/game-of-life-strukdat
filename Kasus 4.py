import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
from collections import deque

# Definisi graph (adjacency list)
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# BFS untuk mendapatkan urutan kunjungan
def bfs(graph, start):
    visited = []
    queue = deque([start])
    seen = set([start])

    while queue:
        node = queue.popleft()
        visited.append(node)
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return visited

order = bfs(graph, 'A')

# Buat graph pakai networkx
G = nx.DiGraph()
for node in graph:
    for neighbor in graph[node]:
        G.add_edge(node, neighbor)

pos = nx.spring_layout(G, seed=42)

fig, ax = plt.subplots()

def update(frame):
    ax.clear()
    
    # Warna node
    colors = []
    for node in G.nodes():
        if node == order[frame]:
            colors.append("red")  # node aktif
        elif node in order[:frame]:
            colors.append("green")  # sudah dikunjungi
        else:
            colors.append("lightgray")  # belum
    
    nx.draw(G, pos, with_labels=True, node_color=colors,
            node_size=1500, font_size=12, ax=ax)
    
    ax.set_title(f"Langkah BFS ke-{frame+1}: {order[frame]}")

ani = animation.FuncAnimation(
    fig, update, frames=len(order), interval=1500, repeat=False
)

plt.show()