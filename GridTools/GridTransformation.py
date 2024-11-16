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
    

    @staticmethod
    def layer_grids(grid1, grid2):
        """
        Combines two grids of the same dimensions by layering grid2 on top of grid1.
        Cells in grid2 take precedence over grid1 if they are non-black (color != 0).

        Parameters:
            grid1 (Grid): The base grid.
            grid2 (Grid): The top layer grid.

        Returns:
            Grid: A new grid with grid2 layered on top of grid1.

        Raises:
            ValueError: If the dimensions of the two grids do not match.
        """
        if grid1.rows != grid2.rows or grid1.cols != grid2.cols:
            raise ValueError("Grids must have the same dimensions to layer them.")

        # Create a new grid with the same dimensions
        layered_grid = Grid(grid1.rows, grid1.cols)

        for x in range(grid1.rows):
            for y in range(grid1.cols):
                # Take the color of grid2 if it's non-black, otherwise use grid1's color
                top_color = grid2.get_cell(x, y).color
                base_color = grid1.get_cell(x, y).color
                layered_color = top_color if top_color != 0 else base_color

                # Set the resulting color in the new grid
                layered_grid.set_cell(x, y, layered_color)

        return layered_grid