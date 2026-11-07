import math

class Entity():
    def __init__(self, x, y, speed, size, color):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed  # px/s
        self.size = size  # w=h
        self.color = color

        # going vectors
        self.dx = 0.0
        self.dy = 0.0

        # Canvas ID
        self.canvas_id = None

    def set_direction(self, dx, dy):
        if dx and dy:
            inv = 1 / math.sqrt(2)
            dx *= inv
            dy *= inv
        self.dx = dx
        self.dy = dy

    def update(self, dt, bounds):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

        max_x, max_y = bounds
        self.x = max(0, min(max_x - self.size, self.x))
        self.y = max(0, min(max_y - self.size, self.y))

    def spawn(self, canvas):
        self.canvas_id = canvas.create_rectangle(
            self.x, self.y,
            self.x + self.size, self.y + self.size,
            fill=self.color, outline="#2a5a10", width=2,
        )

    def render(self, canvas, camera):
        if self.canvas_id is None:
            return
        sx, sy = camera.to_screen(self.x, self.y)
        canvas.coords(
            self.canvas_id,
            sx, sy,
            sx + self.size, sy + self.size,
        )
