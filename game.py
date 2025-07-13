import tkinter as tk
from tkinter import Canvas
import random
import numpy as np

BLOCK_SIZE = 40
WIDTH = 1000
HEIGHT = 1000

class SnakeGameAI:
    def __init__(self, root=None):
        self.dx, self.dy = 0, 1
        self.score = 0
        self.snake = [(480, 480)]
        self.frame_iteration = 0

        self.root = root
        if self.root:
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

        self.spawner()

    ######## SNAKE SETUP START ########
    def draw_snake(self):
        if self.root:
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
        if self.root:
            self.score_counter.config(text=f'Score : {self.score}')
        self.snake = [(480, 480)]
        self.frame_iteration = 0
        self.draw_snake()
        self.spawner()

    def spawner(self):
        if self.root:
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

        if self.root:
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

    def play_step(self, action):
        self.frame_iteration += 1

        self._move(action)

        head_x, head_y = self.snake[0]
        new_head = (head_x + self.dx * BLOCK_SIZE, head_y + self.dy * BLOCK_SIZE)

        reward = 0
        done = False
        if new_head in self.snake[1:]:
            done = True
            reward += -20
            return reward, done, self.score
        elif(
            new_head[0] < 0 or new_head[0] >= WIDTH
            or new_head[1] < 0 or new_head[1] >= HEIGHT
            or self.frame_iteration > 100 * len(self.snake)
        ):
            done = True
            reward += -10
            return reward, done, self.score

        if new_head[0] == self.x0 and new_head[1] == self.y0:
            self.score += 1
            reward += 10
            if self.root:
                self.score_counter.config(text=f'Score : {self.score}')
            self.snake = [new_head] + self.snake
            self.spawner()
        else:
            self.snake = [new_head] + self.snake[:-1]
            reward += -1  # step penalty

            old_distance = abs(head_x - self.x0) + abs(head_y - self.y0)
            new_distance = abs(new_head[0] - self.x0) + abs(new_head[1] - self.y0)
            if new_distance < old_distance:
                reward += 0.2  # got closer
            else:
                reward -= 0.2  # went away

        self.draw_snake()
        return reward, done, self.score
    def state_fetcher(self):
        head_x, head_y = self.snake[0]

        direction_left = 1 if self.dx == -1 else 0
        direction_right = 1 if self.dx == 1 else 0
        direction_up = 1 if self.dy == -1 else 0
        direction_down = 1 if self.dy == 1 else 0
        direction = [direction_left, direction_right, direction_up, direction_down]

        directions = {
            'straight': (self.dx, self.dy),
            'right': (self.dy, -self.dx),
            'left': (-self.dy, self.dx)
        }

        danger = {}
        for rel_dir, (dir_x, dir_y) in directions.items():
            next_x = head_x + dir_x * BLOCK_SIZE
            next_y = head_y + dir_y * BLOCK_SIZE
            wall_hit = next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT
            body_hit = (next_x, next_y) in self.snake
            danger[f'danger_{rel_dir}'] = 1 if (wall_hit or body_hit) else 0

        food_left = 1 if self.x0 < head_x else 0
        food_right = 1 if self.x0 > head_x else 0
        food_up = 1 if self.y0 < head_y else 0
        food_down = 1 if self.y0 > head_y else 0

        state = list(danger.values()) + direction + [food_left, food_right, food_up, food_down]
        return np.array(state, dtype=int)