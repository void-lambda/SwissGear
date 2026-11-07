import tkinter as tk
from entity.entity import Entity

class Player(Entity):
    DIRECTIONS = ("down", "left", "right", "up")
    FRAMES = 2
    
    def __init__(self, x, y, speed, sprite_dir, sprite_scale=4, anim_fps=8):
        super().__init__(x=x, y=y, speed=speed, size=64, color="#7ec850")

        # Keyboard Inputs
        self.keys = set()

        # Animation
        self.facing = "down"
        self.frame = 0
        self.anim_fps = anim_fps
        self.anim_timer = 0.0
        self._last_anim = None

        self._load_sprites(sprite_dir, sprite_scale)

    # Loading
    def _load_sprites(self, sprite_dir, scale):
            self.sprites = {}
            for direction in self.DIRECTIONS:
                frames = []
                for i in range(1, self.FRAMES + 1):
                    path = f"{sprite_dir}/{direction}-{i}.png"
                    img = tk.PhotoImage(file=path).zoom(scale)
                    frames.append(img)
                self.sprites[direction] = frames

    # Keys
    def handle_key_press(self, key):
        self.keys.add(key.lower())

    def handle_key_release(self, key):
        self.keys.discard(key.lower())

    # Logic
    def update(self, dt, bounds):

        dx = dy = 0
        if "w" in self.keys or "up" in self.keys: dy -= 1
        if "s" in self.keys or "down" in self.keys: dy += 1
        if "a" in self.keys or "left" in self.keys: dx -= 1
        if "d" in self.keys or "right" in self.keys: dx += 1
        self.set_direction(dx, dy)

        if dx or dy:
            self.facing = self._pick_facing(dx, dy)
            self.anim_timer += dt
            frame_time = 1.0 / self.anim_fps
            while self.anim_timer >= frame_time:
                self.anim_timer -= frame_time
                self.frame = (self.frame + 1) % self.FRAMES
        else:
            self.frame = 0
            self.anim_timer = 0.0

        super().update(dt, bounds)

    def _pick_facing(self, dx, dy):
        if dy < 0: return "up"
        if dy > 0: return "down"
        if dx < 0: return "left"
        if dx > 0: return "right"
        return self.facing

    # Visual
    def spawn(self, canvas):
        self.canvas_id = canvas.create_image(
            self.x, self.y,
            image=self.sprites[self.facing][self.frame],
            anchor="nw"
        )
        self._last_anim = (self.facing, self.frame)

    def render(self, canvas, camera):
        if self.canvas_id is None:
            return
        sx, sy = camera.to_screen(self.x, self.y)
        canvas.coords(self.canvas_id, sx, sy)

        key = (self.facing, self.frame)
        if key != self._last_anim:
            canvas.itemconfig(self.canvas_id, image=self.sprites[self.facing][self.frame])
            self._last_anim = key
    