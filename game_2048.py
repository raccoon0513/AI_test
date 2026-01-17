# TODO : 시작할때 랜덤한 곳에 숫자 두개
# 4의 확률 10%, 2의 확률 90%
# 입력 : wasd, r(리셋)
import os
import numpy as np

class g2048():

    # TODO : 시드고정 코드. 후에 기존코드 주석 후 주석된거 풀기
    #=============================
    #이건 고정 시드
    # def __init__(self, seed=42):
    #이건 랜덤 시드
    def __init__(self, seed=None):
    #=============================

        # 시드 설정
        self.rng = np.random.default_rng(seed)

        # ==================================
        # 빈 보드 생성
        self.board = np.zeros((4,4), dtype=int)
        # TODO : 테스트형 코드. 사용시 위 코드 주석
        # self.board = np.array([
        #     [0,0,1,0] for i in range(4)
        # ])
        # ==================================
        
        #처음에 두개 생성하지만, run()을 실행하면서 하나를 더 실행하므로 하나만
        self.add_new_number() 

    #=================
    #게임실행관련
    def add_new_number(self):
        flatBoard = self.board.ravel()

        # 결과값이 튜플인데, ex(1,2) 1차원데이터로 변경함
        # 그런데 튜플에서 값을 꺼내기 위해 [0]를 붙임
        isZeros = np.where(flatBoard==0)[0]
        if len(isZeros) > 0:
            flatBoard[self.rng.choice(isZeros)] = self.rng.choice([2,4], p=[0.9, 0.1])


    #커맨드 부분
    def command_w(self):
        pass
    def command_a(self):
        pass
    def command_s(self):
        pass
    def command_d(self):
        pass

    #시프트 연산
    def shift(self):
        pass

    #=================
    
    #=================
    #출력관련코드
    def clear_screen(self):
        os.system('cls')
    def print_board(self):
        print(self.board)

    #=================

    #===================
    def run(self):
        while(np.any(self.board==0)):
            #보드 초기화
            self.clear_screen()

            #값 생성
            self.add_new_number()
            
            #보드 출력
            self.print_board()
    #====================
    

#===================================
#실행부
#===================================
if __name__ == "__main__":
    g1 = g2048()
    g1.run()


