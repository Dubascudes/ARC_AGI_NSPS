from GridTools.GridCell import GridCell

class Grid:
    def __init__(self, rows, cols, default_color=0):
        self.rows = rows
        self.cols = cols
        self.grid = [[GridCell(default_color, x, y) for y in range(cols)] for x in range(rows)]

    def get_cell(self, x, y):
        """Get the GridCell at position (x, y)."""
        if 0 <= x < self.rows and 0 <= y < self.cols:
            return self.grid[x][y]
        else:
            raise IndexError("Cell position out of bounds")

    def set_cell(self, x, y, color):
        """Set the color of the cell at position (x, y)."""
        cell = self.get_cell(x, y)
        cell.color = color

    def to_list(self):
        """Convert the grid to a list of lists format for JSON compatibility."""
        return [[cell.color for cell in row] for row in self.grid]

    @classmethod
    def from_list(cls, data):
        """Initialize a grid from a list of lists."""
        rows, cols = len(data), len(data[0])
        grid = cls(rows, cols)
        for i in range(rows):
            for j in range(cols):
                grid.set_cell(i, j, data[i][j])
        return grid
    
    def __repr__(self):
        grid_repr = "\n".join([" ".join([str(cell.color) for cell in row]) for row in self.grid])
        return f"Grid({self.rows}x{self.cols}):\n{grid_repr}"
