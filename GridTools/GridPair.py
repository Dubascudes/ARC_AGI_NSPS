class GridPair:
    def __init__(self, input_grid, output_grid):
        assert input_grid.rows == output_grid.rows and input_grid.cols == output_grid.cols, \
            "Input and output grids must have the same dimensions"
        self.input_grid = input_grid
        self.output_grid = output_grid

    def __repr__(self):
        return f"GridPair:\nInput:\n{self.input_grid}\nOutput:\n{self.output_grid}"
