# 🐍 **Deep Q-Learning Snake AI**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-1.x-red)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)

---

## 🗒️ Overview

A practical Deep Q-Learning agent trained to play Snake on a custom Tkinter grid.  
Built to test the exact match between state representation, action logic, and reward shaping.  
Model architecture adapted from Patrick Loeber’s open-source Snake AI for clarity and reproducibility.

---

## ⚙️ Features

- **Tkinter Environment** — full game loop, grid rendering, and directional bindings in pure Tkinter.
- **Detailed State Vector** — 13 inputs: relative danger, absolute heading, absolute food position, normalized distances.
- **3-Layer Feedforward Model** — input → two hidden layers with ReLU → output: [straight, right, left].
- **Shaped Rewards** — heavier penalty for self-collisions, step penalty to avoid stalling, bonus for closing distance to the apple.
- **Replay Buffer** — deque with capacity up to 100,000 steps to stabilize learning.

---

## 📊 How It Works

Standard DQN loop:
- `state_fetcher()` aligns relative direction logic with the snake’s turn actions.
- `_move()` adjusts `dx` and `dy` precisely, matching relative danger checks.
- `QTrainer` updates Q-values using the Bellman equation.
- `epsilon` decays to maintain exploration in early games.

---

## 🚀 Quick Start

```bash
# Clone this repository
git clone https://github.com/yourusername/snake-dqn-tkinter.git
cd snake-dqn-tkinter

# Install requirements
pip install torch numpy

# Train the agent
python agent.py

# Run the AI in a visual Tkinter window
python test_visual.py
