class World():
    def __init__(self, grid_width, grid_height, tile_size):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_size = tile_size  # pixels per tile

        self.width = grid_width * tile_size
        self.height = grid_height * tile_size

        self._grid_lines = []

    # GEOMETRY
    @property
    def bounds(self):
        return (self.width, self.height)

    def center(self):
        return self.width / 2, self.height / 2

    # VISUALIZATION
    def spawn(self, canvas):

        for i in range(self.grid_width + 1):
            wx = i * self.tile_size
            line = canvas.create_line(0,0,0,0, fill="#2a2a2a")
            self._grid_lines.append(("v", wx, line))

        for j in range(self.grid_height + 1):
            wy = j * self.tile_size
            line = canvas.create_line(0,0,0,0, fill="#2a2a2a")
            self._grid_lines.append(("h", wy, line))

    def render(self, canvas, camera):
        for kind, wp, line in self._grid_lines:
            if kind == "v":
                sx, _ = camera.to_screen(wp, 0)
                canvas.coords(line, sx, 0, sx, camera.height)
            else:
                _, sy = camera.to_screen(0, wp)
                canvas.coords(line, 0, sy, camera.width, sy)
