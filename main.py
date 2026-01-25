import game_2048
from deep_learning import DQNAgent

# deep_learning.py 하단 실행부 수정
if __name__ == "__main__":
    env = game_2048.g2048(seed=None)
    agent = DQNAgent()
    episodes = 1000
    scores = [] # 점수 기록용

    for ep in range(episodes):
        env.__init__()
        state = env.get_state()
        losses = [] # 이번 판의 오차 기록용
        
        while True:
            action_idx = agent.select_action(state)
            actions = ["w", "a", "s", "d"]
            res_state, reward = env.command_input(actions[action_idx])
            
            done = (res_state == -1)
            if res_state == 0:
                env.add_new_number()
            
            next_state = env.get_state()
            agent.memory.push(state, action_idx, reward, next_state, done)
            
            # 학습 후 발생한 오차 저장
            loss_val = agent.train()
            if loss_val > 0:
                losses.append(loss_val)
            
            state = next_state
            if done:
                scores.append(env.score)
                # 10판마다 평균 점수와 평균 오차 출력
                if (ep + 1) % 10 == 0:
                    avg_score = sum(scores[-10:]) / 10
                    avg_loss = sum(losses) / len(losses) if losses else 0
                    print(f"[{ep+1}] 평균점수: {avg_score:.1f}, 평균오차: {avg_loss:.4f}, 탐험율: {agent.epsilon:.2f}")
                break