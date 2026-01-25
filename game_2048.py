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
        
        # 스코어 설정
        self.score = 0

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
    #TODO : 이부분도 리펙토링?
    def command_w(self):
        self.board = np.transpose(self.board)
        self.board, isChanged, turn_score = self.shift(self.board)
        self.board = np.transpose(self.board).copy()
        return isChanged, turn_score

    def command_a(self):
        self.board, isChanged, turn_score= self.shift(self.board)
        return isChanged, turn_score
    def command_s(self):
        self.board = np.flip(np.transpose(self.board), axis=1)
        self.board, isChanged, turn_score = self.shift(self.board)
        self.board = np.transpose(np.flip(self.board, axis=1)).copy()
        return isChanged, turn_score
    def command_d(self):
        self.board = np.flip(self.board, axis=1)
        self.board, isChanged, turn_score = self.shift(self.board)
        self.board = np.flip(self.board, axis=1).copy()
        return isChanged, turn_score

    #테스트용 임시 로직

    def command_input_test(self):
        dicision = input("w/a/s/d\n")
        self.command_input(dicision)
    def command_input(self, dicision):
        
        isNotChanged = True
        axis = ["w","a","s","d"].index(dicision)
        direction_funcions = [
            self.command_w,
            self.command_a,
            self.command_s,
            self.command_d
        ]
        isNotChanged, turn_score = direction_funcions[axis]()
        if isNotChanged:
            
            #-1 : 전방위 이동 불가(게임 오버)
            if self.isGameOver() : return -1, -20

            # 1 : 해당 방향 처리 불가(이동 불가)    
            return 1, -2
        
        # 0 : 정상
        return 0, turn_score
                
    #시프트 연산
    def shift(self, board):
        new_board = []
        turn_score = 0 #이번 턴에 획득한 점수
        for line in board:
            non_zeros = line[line!=0]
            new_line = []
            checked = False #이전 검사때 합쳐졌으면 스킵할지 정하는 플래그
            for i in range(len(non_zeros)):
                if(checked):
                    checked = False
                    continue
                elif i+1<len(non_zeros) and non_zeros[i]==non_zeros[i+1]:
                    merged_val = non_zeros[i] * 2
                    new_line.append(merged_val)
                    turn_score += merged_val # 합쳐진 값을 점수로 추가
                    checked = True
                else:
                    new_line.append(non_zeros[i])
            new_board.append(new_line + [0] *(4-len(new_line)) ) 
        
        self.score += turn_score
        #안바뀌었으면 True, 바뀌었으면 False
        return np.array(new_board), True if np.array_equal(new_board, board) else False, turn_score

    def isGameOver(self):
        # 빈칸 있는지 체크
        if np.any(self.board == 0):
            return False
        
        #길이 3인 배열 만들어서 비교(하나라도 같으면 참 반환)
        if np.any(self.board[:, :-1] == self.board[:, 1:]) or np.any(self.board[:-1, :] == self.board[1:, :]):
            return False   
            
        # 전부 참일시 게임오버
        return True
    #=================
    
    #=================
    #출력관련코드
    def clear_screen(self):
        os.system('cls')
    def print_board(self):
        print(self.board)
        print(f"현재 스코어 : {self.score}점")

    #=================
    
    #딥러닝용 값 로그화 함수
    def get_state(self):
        """보드 데이터를 log2로 변환하여 0~11 정도의 정수 범위로 압축합니다."""
        # 0인 값은 0으로 유지하고, 나머지 값만 log2 처리
        return np.where(self.board > 0, np.log2(self.board), 0).astype(int)
    #========================

    #===================
    def run(self):
        while True:
            #=====테스트 로직======
            # 1 : 처리 불가
            # 0 : 정상처리
            # -1 : 게임 오버
            state, reward = self.command_input(self.rng.choice(["w", "a", "s", "d"]))
            # state, reward = self.command_input()
            if state==1:
                print("can not move")
                continue
            elif state==-1:
                self.clear_screen()
                self.print_board()
                print("game over")
                break
            #=====================

            

            #값 생성
            if(state == 0):
                self.add_new_number()


            #=====학습시엔 가릴것==============
            #보드 초기화
            self.clear_screen()
            
            #보드 출력
            self.print_board()
            #=======================

            
    #====================
    

#===================================
#실행부
#===================================
if __name__ == "__main__":
    g1 = g2048()
    g1.run()


