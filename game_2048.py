# TODO : 시작할때 랜덤한 곳에 숫자 두개
# 입력 : wasd, r(리셋)
import os
import numpy as np

class g2048():

    # TODO : 시드고정 코드. 후에 기존코드 주석 후 주석된거 풀기
    #=============================
    #이건 고정 시드
    def __init__(self, seed=42):
    #이건 랜덤 시드
    # def __init__(self, seed=None):
    #=============================
        # 시드 설정
        self.rng = np.random.default_rng(seed)

        # 빈 보드 생성
        self.board = np.zeros((4,4), dtype=int)
        
        #첫 실행 화면 초기화
        self.clear_screen()

        #TODO : 초기에 두개 생성하도록 조정할 것
        for _ in range(2): self.add_new_number() 
        
        self.print_board()
    #=================
    #게임실행관련
    def add_new_number(self):
        flatBoard = self.board.ravel()
        # ravel()함수
        # 결과값이 튜플인데, ex(1,2) 1차원데이터로 변경함
        # 그런데 튜플에서 값을 꺼내기 위해 [0]를 붙임
        isZeros = np.where(flatBoard==0)[0]
        if len(isZeros) > 0:
            flatBoard[self.rng.choice(isZeros)] = self.rng.choice([2,4], p=[0.9, 0.1])

    #커맨드 부분
    #TODO : 여기 추가하기

    #게임 오버 체크. 바뀌었는가?
    def game_over_check(self, w=True, a=True, s=True, d=True):
        pass
    #TODO : 이부분도 리펙토링?
    def command_w(self):
        self.board = np.transpose(self.board)
        self.board, isChanged = self.shift(self.board)
        self.board = np.transpose(self.board).copy()
        return isChanged

    def command_a(self):
        self.board, isChanged= self.shift(self.board)
        return isChanged
    def command_s(self):
        self.board = np.flip(np.transpose(self.board), axis=1)
        self.board, isChanged = self.shift(self.board)
        self.board = np.transpose(np.flip(self.board, axis=1)).copy()
        return isChanged
    def command_d(self):
        self.board = np.flip(self.board, axis=1)
        self.board, isChanged = self.shift(self.board)
        self.board = np.flip(self.board, axis=1).copy()
        return isChanged

    #테스트용 임시 로직
    def command_input(self):
        direction_checker = [
            False, False, False, False
        ]
        dicision = input("w/a/s/d\n")
        isNotChanged = True
        axis = ["w","a","s","d"].index(dicision)
        #TODO : 이부분 리펙토링 가능할듯
        direction_funcions = [
            self.command_w,
            self.command_a,
            self.command_s,
            self.command_d
        ]
        isNotChanged = direction_funcions[axis]()
        if isNotChanged:
            for axis, condition in enumerate(direction_checker):
                if(not condition) :
                    direction_checker[axis] = direction_funcions[axis]()
                    if not direction_checker[axis]:
                        break
        if all(direction_checker):
            pass
                
    #시프트 연산
    def shift(self, board):
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
        
        #안바뀌었으면 True, 바뀌었으면 False
        return np.array(new_board), True if np.array_equal(new_board, board) else False

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

            #=====테스트 로직======
            self.command_input()
            #=====================

            #보드 초기화
            #TODO : 클리어 스크린 재활성화
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


