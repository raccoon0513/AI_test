import numpy as np
import os
os.system("cls")

rng = np.random.default_rng(42)
#board = np.array([[rng.choice([0,2,4], p=[0.2, 0.5, 0.3]) for _ in range(4)] for _ in range(4)])
board = np.array([
    [4,2,4,2],
    [0,4,4,4],
    [0,2,2,4],
    [2,4,2,2]
    ])

print(board)

def shift():
    new_board = []
    for line in board:

        non_zeros = line[line!=0]
        new_line = []
        checked = False
        for i in range(len(non_zeros)):
            if(checked):
                checked = False
                continue
            elif i+1<len(non_zeros) and non_zeros[i]==non_zeros[i+1]:
                new_line.append(non_zeros[i]*2)
                checked = True
            else:
                new_line.append(non_zeros[i])

        new_board.append(new_line + [0] *(4-len(new_line)) )


    return np.array(new_board)


        

