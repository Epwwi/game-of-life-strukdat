import random
import time
import os

# Ukuran grid
ROWS = 20
COLS = 40

# Membuat grid awal secara acak
def create_grid():
    return [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

# Menampilkan grid
def print_grid(grid):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in grid:
        for cell in row:
            if cell == 1:
                print("■", end="")
            else:
                print(" ", end="")
        print()

# Menghitung jumlah tetangga hidup
def count_neighbors(grid, row, col):
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1),  (1, 0), (1, 1)
    ]
    
    count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            count += grid[r][c]
    return count

# Update ke generasi berikutnya
def update_grid(grid):
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    for r in range(ROWS):
        for c in range(COLS):
            neighbors = count_neighbors(grid, r, c)
            
            if grid[r][c] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r][c] = 0
                else:
                    new_grid[r][c] = 1
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1
    
    return new_grid

# Program utama
def main():
    grid = create_grid()
    
    while True:
        print_grid(grid)
        grid = update_grid(grid)
        time.sleep(0.3)

if __name__ == "__main__":
    main()