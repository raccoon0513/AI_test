import game_2048
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random
from collections import deque

# 1. 신경망 구조 (기존 코드 유지)
class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(16, 128) # 성능을 위해 노드 수를 조금 늘렸습니다
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 4)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

# 2. 경험 재생 메모리 (경험을 저장하고 무작위로 추출)
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        # 무작위로 묶음(batch) 추출
        state, action, reward, next_state, done = zip(*random.sample(self.buffer, batch_size))
        return (np.array(state), np.array(action), np.array(reward), 
                np.array(next_state), np.array(done))
    
    def __len__(self):
        return len(self.buffer)

# 3. DQN 에이전트 (학습과 판단의 주체)
class DQNAgent:
    def __init__(self):
        self.model = DQN()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.memory = ReplayBuffer()
        self.gamma = 0.99   # 미래 보상 할인율
        self.epsilon = 1.0  # 탐험 확률 (처음엔 무작위)
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995 # 갈수록 모델의 예측을 신뢰
        self.batch_size = 64

    def select_action(self, state):
        # 엡실론-그리디 전략
        if random.random() <= self.epsilon:
            return random.randint(0, 3) # 무작위
        
        state_tensor = torch.FloatTensor(state.flatten()).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        return torch.argmax(q_values).item() # 모델의 최선책

    def train(self):
        if len(self.memory) < self.batch_size:
            return

        # 메모리에서 데이터 추출
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        # 텐서 변환
        states = torch.FloatTensor(states.reshape(self.batch_size, 16))
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states.reshape(self.batch_size, 16))
        dones = torch.FloatTensor(dones)

        # 현재 Q값 계산
        current_q = self.model(states).gather(1, actions).squeeze()
        
        # 목표 Q값 계산 (Bellman Equation)
        next_q = self.model(next_states).max(1)[0].detach()
        target_q = rewards + (1 - dones) * self.gamma * next_q

        # 오차(Loss) 계산 및 최적화
        loss = F.mse_loss(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # 탐험 확률 감소
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay