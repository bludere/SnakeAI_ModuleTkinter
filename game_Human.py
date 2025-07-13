import tkinter as tk
from tkinter import Canvas
import random
import numpy as np

BLOCK_SIZE = 40
WIDTH = 1000
HEIGHT = 1000

class SnakeGameAI:
    def __init__(self, root):
        self.root = root
        self.dx, self.dy = 0, 1
        self.score = 0
        self.snake = [(480, 480)]
        self.frame_iteration = 0

        self.canvas = Canvas(root, width=WIDTH, height=HEIGHT)

        ######## BOARD SETUP START ########
        a = 0
        for i in range(0, WIDTH, BLOCK_SIZE):
            for f in range(0, HEIGHT, BLOCK_SIZE):
                if a % 2 == 0:
                    self.canvas.create_rectangle(i, f, i + BLOCK_SIZE, f + BLOCK_SIZE, fill='#A8D948', width=0)
                else:
                    self.canvas.create_rectangle(i, f, i + BLOCK_SIZE, f + BLOCK_SIZE, fill='#8FCD39', width=0)
                a += 1

        self.score_counter = tk.Label(root, text=f'Score : {self.score}',height=1)
        self.score_counter.pack(anchor='ne')

        self.canvas.pack(fill='both', expand=True)
        ######## BOARD SETUP END ########

        ######## KEY BINDINGS START ########
        root.bind('<Up>', self.up)
        root.bind('<Down>', self.down)
        root.bind('<Left>', self.left)
        root.bind('<Right>', self.right)
        ######## KEY BINDINGS END ########

        self.spawner()
        # self.move()  # Removed from here to call explicitly in manual mode

    ######## SNAKE SETUP START ########
    def draw_snake(self):
        self.canvas.delete('snake')
        for (x, y) in self.snake:
            self.canvas.create_rectangle(x, y, x + BLOCK_SIZE, y + BLOCK_SIZE, fill='#4470E5', width=0, tags='snake')

    """
    MOVEMENT LOGIC
    DY = 0 DX = 1 : RIGHT
    DY = 0 DX = -1 : LEFT
    DY = 1 DX = 0 : DOWN
    DY = -1 DX = 0 : UP
    """
    ######## SNAKE SETUP END ########

    ######## APPLE SPAWN START ########
    def reset(self):
        self.dx, self.dy = 0, 1
        self.score = 0
        self.score_counter.config(text=f'Score : {self.score}')
        self.snake = [(480, 480)]
        self.frame_iteration = 0
        self.draw_snake()
        self.spawner()
        if self.root:
            self.root.after_cancel(self.root.after_id) if hasattr(self.root, 'after_id') else None
            self.move()

    def spawner(self):
        self.canvas.delete('apple')
        radius = 20
        cols = WIDTH // BLOCK_SIZE
        rows = HEIGHT // BLOCK_SIZE

        while True:
            center_x = (random.randint(0, cols - 1) * BLOCK_SIZE) + BLOCK_SIZE // 2
            center_y = (random.randint(0, rows - 1) * BLOCK_SIZE) + BLOCK_SIZE // 2
            grid_x = center_x - BLOCK_SIZE // 2
            grid_y = center_y - BLOCK_SIZE // 2
            if (grid_x, grid_y) not in self.snake:
                break

        self.x0 = grid_x
        self.y0 = grid_y

        self.canvas.create_oval(
            self.x0, self.y0, self.x0 + BLOCK_SIZE, self.y0 + BLOCK_SIZE,
            width=0, fill='#E7471D', tags='apple'
        )
    ######## APPLE SPAWN END ########

    ######## MOVEMENT SETUP START ########
    def _move(self, action):
        """
        action: [straight, right, left]
        """
        dx, dy = self.dx, self.dy

        if np.array_equal(action, [1, 0, 0]):
            # Keep same direction
            pass

        elif np.array_equal(action, [0, 1, 0]):
            # Turn right relative to current
            if dx == 1:      # Right → Down
                self.dx, self.dy = 0, 1
            elif dx == -1:   # Left → Up
                self.dx, self.dy = 0, -1
            elif dy == 1:    # Down → Left
                self.dx, self.dy = -1, 0
            elif dy == -1:   # Up → Right
                self.dx, self.dy = 1, 0

        else:
            # Turn left relative to current
            if dx == 1:      # Right → Up
                self.dx, self.dy = 0, -1
            elif dx == -1:   # Left → Down
                self.dx, self.dy = 0, 1
            elif dy == 1:    # Down → Right
                self.dx, self.dy = 1, 0
            elif dy == -1:   # Up → Left
                self.dx, self.dy = -1, 0

    def move(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.dx * BLOCK_SIZE, head_y + self.dy * BLOCK_SIZE)

        if (
            new_head in self.snake[1:] or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        ):
            self.reset()
            return

        if new_head[0] == self.x0 and new_head[1] == self.y0:
            self.score += 1
            if self.root:
                self.score_counter.config(text=f'Score : {self.score}')
            self.snake = [new_head] + self.snake  # Grow
            self.spawner()
        else:
            self.snake = [new_head] + self.snake[:-1]  # Normal move

        self.draw_snake()
        self.root.after_id = self.root.after(80, self.move)

    def play_step(self, action):
        self.frame_iteration += 1

        self._move(action)

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.dx * BLOCK_SIZE, head_y + self.dy * BLOCK_SIZE)

        reward = 0
        done = False

        if (
            new_head in self.snake[1:]
            or new_head[0] < 0 or new_head[0] >= WIDTH
            or new_head[1] < 0 or new_head[1] >= HEIGHT
            or self.frame_iteration > 100 * len(self.snake)
        ):
            done = True
            reward = -10
            return reward, done, self.score

        if new_head[0] == self.x0 and new_head[1] == self.y0:
            self.score += 1
            reward = 10
            if self.root:
                self.score_counter.config(text=f'Score : {self.score}')
            self.snake = [new_head] + self.snake
            self.spawner()
        else:
            self.snake = [new_head] + self.snake[:-1]

        self.draw_snake()
        return reward, done, self.score

    ######## DIRECTION SETUP START ########
    def up(self, event):
        if self.dy == 0:
            self.dx, self.dy = 0, -1

    def down(self, event):
        if self.dy == 0:
            self.dx, self.dy = 0, 1

    def left(self, event):
        if self.dx == 0:
            self.dx, self.dy = -1, 0

    def right(self, event):
        if self.dx == 0:
            self.dx, self.dy = 1, 0
    
    ######## DIRECTION SETUP END ########

root = tk.Tk()
root.geometry(f"1000x1021")
game = SnakeGameAI(root)
game.move()
root.mainloop()