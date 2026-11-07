import math

class Camera():
    def __init__(self, width, height, world, follow_speed=5.0):
        self.x = 0.0
        self.y = 0.0
        self.width = width
        self.height = height
        self.world = world
        self.follow_speed = follow_speed

    def snap_to(self, target_x, target_y):
        self.x = target_x - self.width / 2
        self.x = target_y - self.height / 2
        self._clamp()

    def follow(self, target_x, target_y, dt):
        want_x = target_x - self.width / 2
        want_y = target_y - self.height / 2

        k = 1 - math.exp(-self.follow_speed * dt)

        self.x += (want_x - self.x) * k
        self.y += (want_y - self.y) * k
        self._clamp()

    def _clamp(self):
        max_x = self.world.width - self.width
        max_y = self.world.height - self.height
        self.x = max(0, min(max_x, self.x))
        self.y = max(0, min(max_y, self.y))

    def to_screen(self, world_x, world_y):
        return world_x - self.x, world_y - self.y
