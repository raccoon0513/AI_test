import game_2048
from deep_learning import DQNAgent
import torch
import os

if __name__ == "__main__":
    env = game_2048.g2048(seed=None)
    agent = DQNAgent()

    model_path = "model_2048.pth" # 불러올 파일명과 저장할 파일명을 통일하면 관리가 쉽습니다.

    # 1. 기존 학습 모델 불러오기
    if os.path.exists(model_path):
        agent.model.load_state_dict(torch.load(model_path))
        agent.epsilon = 0.01 # 이미 학습된 모델이면 낮은 탐험율로 시작
        print(f"{model_path} 모델을 성공적으로 불러왔습니다.")
    else:
        print("저장된 모델이 없어 처음부터 학습을 시작합니다.")

    episodes = 1000 # 목표 세대 수
    scores = [] 

    try:
        for ep in range(episodes):
            env.__init__(seed=None) # 매 판 새로운 시드로 시작
            state = env.get_state()
            
            while True:
                action_idx = agent.select_action(state)
                actions = ["w", "a", "s", "d"]
                res_state, reward = env.command_input(actions[action_idx])
                
                done = (res_state == -1)
                if res_state == 0:
                    env.add_new_number()
                
                next_state = env.get_state()
                agent.memory.push(state, action_idx, reward, next_state, done)
                
                agent.train()
                
                state = next_state
                if done:
                    scores.append(env.score)
                    print(f"세대: {ep + 1} | 점수: {env.score} | 탐험율: {agent.epsilon:.2f}")
                    break

    except KeyboardInterrupt:
        # 2. Ctrl + C 발생 시 실행되는 부분
        print("\n학습이 사용자에 의해 중단되었습니다. 현재까지의 모델을 저장합니다...")
    
    finally:
        # 3. 정상 종료되거나 중단되어도 항상 모델 저장
        torch.save(agent.model.state_dict(), model_path)
        print(f"모델 저장 완료: {model_path}")