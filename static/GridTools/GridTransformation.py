from GridTools.Grid import Grid

class GridTransformation:
    @staticmethod
    def rotate_90_clockwise(grid):
        """Rotate the grid 90 degrees clockwise."""
        rows, cols = grid.rows, grid.cols
        new_grid = Grid(cols, rows)
        for x in range(rows):
            for y in range(cols):
                new_grid.set_cell(y, rows - 1 - x, grid.get_cell(x, y).color)
        return new_grid

    @staticmethod
    def rotate_90_counterclockwise(grid):
        """Rotate the grid 90 degrees counterclockwise."""
        rows, cols = grid.rows, grid.cols
        new_grid = Grid(cols, rows)
        for x in range(rows):
            for y in range(cols):
                new_grid.set_cell(cols - 1 - y, x, grid.get_cell(x, y).color)
        return new_grid

    @staticmethod
    def flip_vertical(grid):
        """Flip the grid vertically."""
        new_grid = Grid(grid.rows, grid.cols)
        for x in range(grid.rows):
            for y in range(grid.cols):
                new_grid.set_cell(grid.rows - 1 - x, y, grid.get_cell(x, y).color)
        return new_grid

    @staticmethod
    def flip_horizontal(grid):
        """Flip the grid horizontally."""
        new_grid = Grid(grid.rows, grid.cols)
        for x in range(grid.rows):
            for y in range(grid.cols):
                new_grid.set_cell(x, grid.cols - 1 - y, grid.get_cell(x, y).color)
        return new_grid

    @staticmethod
    def transpose(grid):
        """Transpose the grid."""
        new_grid = Grid(grid.cols, grid.rows)
        for x in range(grid.rows):
            for y in range(grid.cols):
                new_grid.set_cell(y, x, grid.get_cell(x, y).color)
        return new_grid
