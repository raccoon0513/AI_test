import game_2048
from deep_learning import DQNAgent
import torch
import os
import json # JSON 처리를 위해 추가

if __name__ == "__main__":
    env = game_2048.g2048(seed=None)
    agent = DQNAgent()

    model_path = "model_2048.pth"
    config_path = "config.json" # 세대 정보를 저장할 경로
    
    start_ep = 0 # 시작 세대 번호 초기화

    # 1. 기존 모델 및 세대 정보 불러오기
    if os.path.exists(model_path):
        agent.model.load_state_dict(torch.load(model_path))
        agent.epsilon = 0.01 
        print(f"{model_path} 모델을 성공적으로 불러왔습니다.")
        
        # JSON 파일에서 마지막으로 저장된 세대 확인
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                start_ep = config.get("last_generation", 0)
                print(f"이전 학습 세대({start_ep}) 정보를 불러왔습니다.")
    else:
        print("저장된 모델이 없어 처음부터 학습을 시작합니다.")

    total_episodes = 1000 # 목표 총 세대 수
    scores = [] 
    current_ep = start_ep # 현재 진행 세대 추적용

    try:
        # 이전에 멈춘 세대부터 목표 세대까지 진행
        for ep in range(start_ep, total_episodes):
            current_ep = ep # 현재 세대 업데이트
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
        print(f"\n[중단 알림] 제 {current_ep + 1}세대 학습 중 중단되었습니다.")
    
    finally:
        # 2. 모델 가중치 저장
        torch.save(agent.model.state_dict(), model_path)
        
        # 3. 현재 세대 정보를 JSON에 저장
        with open(config_path, "w") as f:
            # 루프가 정상 종료되면 total_episodes를, 중단되면 current_ep+1을 저장
            save_data = {"last_generation": current_ep + 1}
            json.dump(save_data, f)
            
        print(f"현재 세대({current_ep + 1}) 정보와 모델이 저장되었습니다.")