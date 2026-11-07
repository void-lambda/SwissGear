import tkinter as tk
import time

from entity.entity import Entity
from entity.player import Player
from camera import Camera

# CONSTANTS
TILE = 16  # pixels
SCALE = 4  # 4 times
TILE_PXL = TILE * SCALE  # 64px
GRID = 12
WINDOW = TILE_PXL * GRID  # 768

WORLD_GRID = 24
WORLD_PXL = TILE_PXL * WORLD_GRID  # 1536

FPS = 60
SPEED = 300  # px/s
CAMERA_SPEED = 5.0

class Game():
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW, height=WINDOW, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()

        self.bounds = (WORLD_PXL, WORLD_PXL)

        self.camera = Camera(
            width=WINDOW, height=WINDOW,
            world_width=WORLD_PXL, world_height=WORLD_PXL,
            follow_speed=CAMERA_SPEED,
        )

        self._build_grid()

        self.player = Player(
            x=WORLD_PXL // 2 - TILE_PXL // 2,
            y=WORLD_PXL // 2 - TILE_PXL // 2,
            speed=SPEED,
        )
        self.player.spawn(self.canvas)

        self.camera.snap_to(
            self.player.x + self.player.size / 2,
            self.player.y + self.player.size / 2,
        )

        # Spawn Entities
        self.entities: list[Entity] = [self.player]

        # Keyboard
        root.bind("<KeyPress>",   lambda e: self.player.handle_key_press(e.keysym))
        root.bind("<KeyRelease>", lambda e: self.player.handle_key_release(e.keysym))

        self._last = time.perf_counter()
        self._loop()

    def _build_grid(self):
        self.grid_lines = []
        for i in range(WORLD_GRID + 1):
            wx = i * TILE_PXL
            line = self.canvas.create_line(0, 0, 0, 0, fill="#2a2a2a")
            self.grid_lines.append(("v", wx, line))
        for i in range(WORLD_GRID + 1):
            wy = i * TILE_PXL
            line = self.canvas.create_line(0, 0, 0, 0, fill="#2a2a2a")
            self.grid_lines.append(("h", wy, line))

    def _render_grid(self):
        for kind, wp, line in self.grid_lines:
            if kind == "v":
                sx, _ = self.camera.to_screen(wp, 0)
                self.canvas.coords(line, sx, 0, sx, WINDOW)
            else:
                _, sy = self.camera.to_screen(0, wp)
                self.canvas.coords(line, 0, sy, WINDOW, sy)

    def _loop(self):
        now = time.perf_counter()
        dt = min(now - self._last, 0.05)
        self._last = now

        # 1. Мир обновляется
        for entity in self.entities:
            entity.update(dt, self.bounds)

        # 2. Камера догоняет НОВУЮ позицию игрока
        pcx = self.player.x + self.player.size / 2
        pcy = self.player.y + self.player.size / 2
        self.camera.follow(pcx, pcy, dt)

        # 3. Рисуем всё через камеру
        self._render_grid()
        for entity in self.entities:
            entity.render(self.canvas, self.camera)

        self.root.after(max(1, int(1000 / FPS)), self._loop)



def main():
    root = tk.Tk()
    root.title("Swiss Gear Calculator")
    root.geometry("768x768")
    root.resizable(False, False)
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
