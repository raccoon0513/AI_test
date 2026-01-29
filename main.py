import game_2048
from deep_learning import DQNAgent
import torch
import os

if __name__ == "__main__":
    env = game_2048.g2048(seed=None)
    agent = DQNAgent()

    model_path = "model_2048.pth"
    generation_path = "config.json"
    ep = 0 # 세대 번호를 예외 처리 구문에서도 접근할 수 있도록 루프 밖에서 초기화

    # 모델 불러오기 로직
    if os.path.exists(model_path):
        agent.model.load_state_dict(torch.load(model_path))
        agent.epsilon = 0.01 
        print(f"{model_path} 모델을 성공적으로 불러왔습니다.")
    else:
        print("저장된 모델이 없어 처음부터 학습을 시작합니다.")

    episodes = 1000
    scores = [] 

    try:
        for ep in range(episodes):
            env.__init__(seed=None)
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
        # Ctrl + C 중단 시 현재 진행 중이던 세대 번호 출력
        print(f"\n[중단 알림] 제 {ep + 1}세대 학습 중 사용자에 의해 중단되었습니다.")
    
    finally:
        # 중단되더라도 현재까지의 가중치를 파일로 저장
        torch.save(agent.model.state_dict(), model_path)
        print(f"현재 세대({ep + 1})까지의 모델이 {model_path}에 저장되었습니다.")
        