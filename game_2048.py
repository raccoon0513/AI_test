# TODO : 시작할때 랜덤한 곳에 숫자 두개
# 4의 확률 10%, 2의 확률 90%
# 입력 : wasd, r(리셋)
import os
import numpy as np

class g2048():
    def __init__(self, seed=42):
        # 시드고정
        rng = np.random.default_rng(seed)

        self.board = np.array([
            [0,0,0,0] for i in range(4)
        ])
    
    #=================
    #게임실행관련
    def add_new_number(self):
        # self.board.flatten()
        pass

    #=================
    
    #출력관련코드
    def clear_screen(self):
        os.system('cls')
    def print_board(self):
        print(self.board)

    #=================

    def run(self):
        self.clear_screen()

        
        self.print_board()

    

#===================================
#실행부
#===================================
if __name__ == "__main__":
    g1 = g2048()
    


