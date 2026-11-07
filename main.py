import tkinter as tk
import time

from entity.entity import Entity
from entity.player import Player
from camera import Camera
from world import World

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
        # WINDOW
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW, height=WINDOW, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()

        # WORLD
        self.world = World(grid_width=WORLD_GRID, grid_height=WORLD_GRID, tile_size=TILE_PXL)
        self.world.spawn(self.canvas)

        # CAMERA
        self.camera = Camera(
            width=WINDOW, height=WINDOW,
            world=self.world,
            follow_speed=CAMERA_SPEED,
        )

        # PLAYER
        cx, cy = self.world.center()
        self.player = Player(
            x=cx - TILE_PXL // 2,
            y=cy - TILE_PXL // 2,
            speed=SPEED,
            sprite_dir="src/tiles/player",
            sprite_scale=SCALE,
            anim_fps=8
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

        # Game Loop
        self._last = time.perf_counter()
        self._loop()

    def _loop(self):
        # Time Logic
        now = time.perf_counter()
        dt = min(now - self._last, 0.05)
        self._last = now

        # World Updates
        for entity in self.entities:
            entity.update(dt, self.world.bounds)

        # Camera Follows Player
        pcx = self.player.x + self.player.size / 2
        pcy = self.player.y + self.player.size / 2
        self.camera.follow(pcx, pcy, dt)

        # Rendering (Worlds -> Entities)
        self.world.render(self.canvas, self.camera)
        for entity in self.entities:
            entity.render(self.canvas, self.camera)

        self.root.after(max(1, int(1000 / FPS)), self._loop)



def main():
    root = tk.Tk()
    root.title("Swiss Gear Calculator")
    root.geometry(f"{WINDOW}x{WINDOW}")
    root.resizable(False, False)
    Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
