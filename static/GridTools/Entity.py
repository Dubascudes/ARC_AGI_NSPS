class Entity:
    def __init__(self, cells):
        """Initialize an Entity with a list of GridCell objects."""
        self.cells = cells  # List of GridCell objects making up the entity

    def get_bounds(self):
        """Calculate the bounding box of the entity."""
        xs = [cell.position[0] for cell in self.cells]
        ys = [cell.position[1] for cell in self.cells]
        return min(xs), min(ys), max(xs), max(ys)

    def move(self, dx, dy):
        """Move the entity by (dx, dy)."""
        for cell in self.cells:
            new_x = cell.position[0] + dx
            new_y = cell.position[1] + dy
            cell.position = (new_x, new_y)

    def __repr__(self):
        return f"Entity(cells={self.cells})"
