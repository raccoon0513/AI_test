import deep_learning


if __name__ == "__main__":
    env = game_2048.g2048(seed=None) # 랜덤 게임 생성
    agent = DQNAgent()
    episodes = 1000 # 총 1000판 학습

    for ep in range(episodes):
        env.__init__() # 게임 리셋
        state = env.get_state()
        total_reward = 0
        
        while True:
            # 1. 방향 결정 (0:w, 1:a, 2:s, 3:d)
            action_idx = agent.select_action(state)
            actions = ["w", "a", "s", "d"]
            
            # 2. 게임에 적용
            res_state, reward = env.command_input(actions[action_idx])
            
            # 3. 다음 상태 및 종료 확인
            done = (res_state == -1)
            if res_state == 0:
                env.add_new_number()
            
            next_state = env.get_state()
            
            # 4. 메모리에 저장
            agent.memory.push(state, action_idx, reward, next_state, done)
            
            # 5. 학습 수행
            agent.train()
            
            state = next_state
            total_reward += reward
            
            if done:
                print(f"Episode: {ep}, Score: {env.score}, Epsilon: {agent.epsilon:.2f}")
                break