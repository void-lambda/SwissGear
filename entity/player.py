from entity.entity import Entity

class Player(Entity):
    def __init__(self, x, y, speed):
        super().__init__(x=x, y=y, speed=speed, size=64, color="#7ec850")

        # keyboard
        self.keys = set()

    def handle_key_press(self, key):
        self.keys.add(key.lower())

    def handle_key_release(self, key):
        self.keys.discard(key.lower())

    def update(self, dt, bounds):

        dx = dy = 0
        if "w" in self.keys or "up" in self.keys: dy -= 1
        if "s" in self.keys or "down" in self.keys: dy += 1
        if "a" in self.keys or "left" in self.keys: dx -= 1
        if "d" in self.keys or "right" in self.keys: dx += 1
        self.set_direction(dx, dy)

        super().update(dt, bounds)
