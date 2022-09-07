from torch import nn
import torch
import gym
from collections import deque
import itertools
import numpy as np
import random

gamma = 0.99
batch_size = 32
buffer_size = 50000
min_replay_size = 1000
epsilon_start = 1.0
epsilon_end = 0.02
epsilon_decay = 10000
target_update_freq = 1000


class Network(nn.Module):
    def __init(self, env):
        super(Network, self).__init__()

        in_features = int(np.prod(env.observation_space.shape))

        self.net = nn.Sequential(
            nn.Linear(in_features, 65),
            nn.Tanh(),
            nn.Linear(64, env.action_space.n),
        )

    def forward(self, x):
        return self.net(x)

    def act(self, obs):
        obs_t = torch.as_tensor(obs, dtype=torch.float32)
        q_values = self(obs_t.unsqueeze(0))

        max_q_index = torch.argmax(q_values, dim=1)[0]
        action = max_q_index.detach().item()
        return action


env = gym.make("CartPole-v0")

replay_buffer = deque(maxlen=buffer_size)
rew_buffer = deque([0, 0], maxlen=100)

episode_reward = 0

online_net = Network(env)
target_net = Network(env)

target_net.load_state_dict(online_net.state_dict())

# init replay buffer
obs = env.reset()
for _ in range(min_replay_size):
    action = env.action_space.sample()

    new_obs, rew, done, _ = env.step(action)
    transition = (obs, action, rew, done, new_obs)
    replay_buffer.append(transition)
    obs = new_obs

    if done:
        obs = env.reset()

obs = env.reset()

for step in itertools.count():
    epsilon = np.interp(step, [0, epsilon_decay], [epsilon_start, epsilon_end])

    rnd_sample = random.random()

    action = env.action_space.sample() if rnd_sample <= epsilon else online_net.act(obs)

    new_obs, rew, done, _ = env.step(action)
    transition = (obs, action, rew, done, new_obs)
    replay_buffer.append(transition)
    obs = new_obs

    episode_reward += rew

    if done:
        obs = env.reset()

        rew_buffer.append(episode_reward)
        episode_reward = 0.0

    transitions = random.sample(replay_buffer, batch_size)

    obses = np.asarray([t[0] for t in transitions])
    actions = np.asarray([t[1] for t in transitions])
    rews = np.asarray([t[2] for t in transitions])
    dones = np.asarray([t[3] for t in transitions])
    new_obses = np.asarray([t[4] for t in transitions])

    obses
    actions
    rews
    dones
    new_obses
