# src/reinforce.py

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class PolicyNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return torch.softmax(self.fc2(x), dim=-1)  # Softmax to get probabilities

class REINFORCEAgent:
    def __init__(self, state_size, action_size, lr=0.01):
        self.policy_net = PolicyNetwork(state_size, action_size)
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)

    def select_action(self, state):
        state_tensor = torch.FloatTensor(state)
        probabilities = self.policy_net(state_tensor)
        action = np.random.choice(len(probabilities), p=probabilities.detach().numpy())
        return action, probabilities[action]

    def update_policy(self, rewards, log_probs):
        # Calculate the discounted rewards
        discounted_rewards = []
        for t in range(len(rewards)):
            G = sum(rewards[t + i] * (0.99 ** i) for i in range(len(rewards) - t))
            discounted_rewards.append(G)
        
        discounted_rewards = torch.FloatTensor(discounted_rewards)
        log_probs = torch.cat(log_probs)

        # Calculate loss
        loss = -log_probs * discounted_rewards  # Policy Gradient Loss
        loss = loss.mean()

        # Update the policy network
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
