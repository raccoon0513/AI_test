import game_2048
from deep_learning import DQNAgent
import torch
import os

if __name__ == "__main__":
    env = game_2048.g2048(seed=None)
    agent = DQNAgent()

    model_path = "best_model_2048.pth"

    # 파일이 존재하는지 확인 후 불러오기
    if os.path.exists(model_path):
        # 모델의 가중치 데이터를 불러와서 에이전트의 모델에 적용
        agent.model.load_state_dict(torch.load(model_path))
        
        # 불러온 후 바로 실전 모드로 돌리고 싶다면 탐험율을 낮춤
        agent.epsilon = 0.01 
        print(f"{model_path} 모델을 성공적으로 불러왔습니다.")
    else:
        

        episodes = 10
        scores = [] 

        for ep in range(episodes):
            env.__init__()
            state = env.get_state()
            losses = [] 
            
            while True:
                action_idx = agent.select_action(state)
                actions = ["w", "a", "s", "d"]
                res_state, reward = env.command_input(actions[action_idx])
                
                done = (res_state == -1)
                if res_state == 0:
                    env.add_new_number()
                
                next_state = env.get_state()
                agent.memory.push(state, action_idx, reward, next_state, done)
                
                loss_val = agent.train()
                if loss_val is not None and loss_val > 0:
                    losses.append(loss_val)
                
                state = next_state
                if done:
                    scores.append(env.score)
                    # 매 세대(에피소드)가 끝날 때마다 현재 세대 번호와 점수 출력
                    print(f"세대: {ep + 1} | 점수: {env.score} | 탐험율: {agent.epsilon:.2f}")
                    
                    # 10세대마다 평균 지표 추가 출력
                    if (ep + 1) % 10 == 0:
                        avg_score = sum(scores[-10:]) / 10
                        avg_loss = sum(losses) / len(losses) if losses else 0
                        print(f">>> [최근 10세대 평균] 점수: {avg_score:.1f}, 오차: {avg_loss:.4f}")
                    break
        # main.py 학습 종료 시점
        torch.save(agent.model.state_dict(), "model_2048.pth")
        print("모델 저장 완료!")