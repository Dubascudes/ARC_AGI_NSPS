class GridCell:
    def __init__(self, color, x, y):
        self.color = color
        self.position = (x, y)

    def __repr__(self):
        return f"GridCell(color={self.color}, position={self.position})"
