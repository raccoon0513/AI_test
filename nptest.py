import numpy as np
import os
os.system("cls")

rng = np.random.default_rng(42)
board = np.array([[rng.choice([0,2,4], p=[0.2, 0.5, 0.3]) for _ in range(4)] for _ in range(4)])


print(board)

for line in board:
    non_zeros = line[line!=0]
    if len(non_zeros) > 1:
        

