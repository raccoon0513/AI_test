import game_2048
import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        # 입력: 4x4 보드를 한 줄로 핀 16개 데이터
        self.fc1 = nn.Linear(16, 64)  
        self.fc2 = nn.Linear(64, 64)
        # 출력: 상, 하, 좌, 우 4개 방향에 대한 가치(Q-value)
        self.fc3 = nn.Linear(64, 4)

    def forward(self, x):
        # x: (batch_size, 16) 형태의 텐서
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)