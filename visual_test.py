import tkinter as tk
from agent import Agent
import torch
from game import SnakeGameAI

root = tk.Tk()
root.geometry(f"1000x1021")
game = SnakeGameAI(root)

agent = Agent()
agent.model.load_state_dict(torch.load('model/model.pth'))
agent.model.eval()

def run_ai():
    state = agent.get_state(game)
    final_move = agent.get_action(state)
    reward, done, score = game.play_step(final_move)
    if not done:
        root.after(80, run_ai)
    else:
        print("Game over! Score:", score)
        game.reset()
        run_ai()

run_ai()


root.mainloop()