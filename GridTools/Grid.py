from GridTools.GridCell import GridCell
from GridTools.Entity import Entity
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

    def insert_row(self, index, color=0):
        """
        Inserts a new row at the specified index. The new row will have the specified color.
        """
        if not (0 <= index <= self.rows):
            raise IndexError(f"Row index {index} out of range.")

        # Create a new row with the given color
        new_row = [GridCell(color, index, y) for y in range(self.cols)]
        
        # Adjust positions of existing rows after the insertion point
        for x in range(index, self.rows):
            for cell in self.grid[x]:
                cell.position = (cell.position[0] + 1, cell.position[1])

        # Insert the new row
        self.grid.insert(index, new_row)
        self.rows += 1

    def insert_col(self, index, color=0):
        """
        Inserts a new column at the specified index. The new column will have the specified color.
        """
        if not (0 <= index <= self.cols):
            raise IndexError(f"Column index {index} out of range.")

        # Adjust positions of existing cells after the insertion point
        for row in self.grid:
            for y in range(index, self.cols):
                cell = row[y]
                cell.position = (cell.position[0], cell.position[1] + 1)

        # Insert the new column
        for x in range(self.rows):
            new_cell = GridCell(color, x, index)
            self.grid[x].insert(index, new_cell)
        self.cols += 1

    def del_row(self, index):
        """
        Deletes the row at the specified index.
        """
        if not (0 <= index < self.rows):
            raise IndexError(f"Row index {index} out of range.")

        # Remove the row
        del self.grid[index]
        self.rows -= 1

        # Adjust positions of remaining rows
        for x in range(index, self.rows):
            for cell in self.grid[x]:
                cell.position = (cell.position[0] - 1, cell.position[1])

    def del_col(self, index):
        """
        Deletes the column at the specified index.
        """
        if not (0 <= index < self.cols):
            raise IndexError(f"Column index {index} out of range.")

        # Remove the column
        for row in self.grid:
            del row[index]

        # Adjust positions of remaining columns
        for x in range(self.rows):
            for y in range(index, self.cols - 1):
                cell = self.grid[x][y]
                cell.position = (cell.position[0], cell.position[1] - 1)

        self.cols -= 1
    def reset(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.grid[x][y].color = 0

    def to_list(self):
        """Convert the grid to a list of lists format for JSON compatibility."""
        return [[cell.color for cell in row] for row in self.grid]

    def select_cells_by_color(self, color):
        """
        Selects all cells of the given color and returns them as an Entity.

        Parameters:
        - color (int): The color to search for.

        Returns:
        - Entity: An Entity object containing all cells of the specified color.
        """
        selected_cells = []
        
        # Iterate through all cells in the grid
        for x in range(self.rows):
            for y in range(self.cols):
                cell = self.get_cell(x, y)
                if cell.color == color:
                    selected_cells.append(cell)
        
        # Create and return an Entity from the selected cells
        return Entity(selected_cells)
    @classmethod
    def from_list(cls, data):
        """Initialize a grid from a list of lists."""
        rows, cols = len(data), len(data[0])
        grid = cls(rows, cols)
        for i in range(rows):
            for j in range(cols):
                grid.set_cell(i, j, data[i][j])
        return grid

    def draw_entity(self, entity):
        """
        Draws the given entity on the grid by setting the color of cells in the grid
        to match the colors of the cells in the entity.
        
        Parameters:
        - entity (Entity): The entity to draw on the grid.
        """
        for cell in entity.cells:
            x, y = cell.position
            if 0 <= x < self.rows and 0 <= y < self.cols:
                self.set_cell(x, y, cell.color)
            else:
                print(f"Warning: Entity cell at ({x}, {y}) is out of grid bounds")

    def crop_to_occupied(self):
        """
        Creates a new grid that excludes any rows and columns consisting entirely of black cells (color 0).

        Returns:
        - Grid: A new cropped Grid object containing only the occupied (non-black) cells.
        """
        # Determine the bounding box of non-black cells
        min_x, min_y, max_x, max_y = self.rows, self.cols, 0, 0
        has_occupied_cells = False

        for x in range(self.rows):
            for y in range(self.cols):
                if self.get_cell(x, y).color != 0:  # Non-black cell
                    has_occupied_cells = True
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        # If no occupied cells, return an empty grid of the same size
        if not has_occupied_cells:
            return Grid(0, 0)

        # Create the new cropped grid
        cropped_rows = max_x - min_x + 1
        cropped_cols = max_y - min_y + 1
        cropped_grid = Grid(cropped_rows, cropped_cols)

        # Populate the new grid with the corresponding non-black cells
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cell = self.get_cell(x, y)
                if cell.color != 0:
                    cropped_grid.set_cell(x - min_x, y - min_y, cell.color)

        return cropped_grid
    def draw_entity_at_point(self, entity, center):
        """
        Draws the given entity on the grid, centered at the specified point (center_x, center_y).
        
        Parameters:
        - entity (Entity): The entity to draw on the grid.
        - center_x (int): The x-coordinate of the desired center position on the grid.
        - center_y (int): The y-coordinate of the desired center position on the grid.
        """
        # Calculate the bounding box of the entity
        min_x, min_y, max_x, max_y = entity.get_bounds()
        entity_width = max_x - min_x + 1
        entity_height = max_y - min_y + 1

        # Calculate the top-left starting position to center the entity
        center_x, center_y = center
        start_x = center_x - entity_width // 2
        start_y = center_y - entity_height // 2

        for cell in entity.cells:
            # Adjust each cell's position to center the entity
            x = start_x + (cell.position[0] - min_x)
            y = start_y + (cell.position[1] - min_y)
            
            # Check grid bounds before setting the cell
            if 0 <= x < self.rows and 0 <= y < self.cols:
                self.set_cell(x, y, cell.color)
            else:
                print(f"Warning: Centered entity cell at ({x}, {y}) is out of grid bounds")

    def get_entity_by_region(self, bounds):
        """
        Returns an Entity object made of the cells within the bounds defined by minx, miny, maxx, and maxy.

        Parameters:
        - minx, miny: The top-left corner of the region (inclusive).
        - maxx, maxy: The bottom-right corner of the region (inclusive).

        Returns:
        - Entity: An Entity object containing the cells within the specified region.
        """
        cells_in_region = []
        minx, miny, maxx, maxy = bounds
        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                if 0 <= x < self.rows and 0 <= y < self.cols:
                    cell = self.get_cell(x, y)
                    cells_in_region.append(cell)
                else:
                    print(f"Warning: Position ({x}, {y}) is out of grid bounds and will be skipped.")
        
        return Entity(cells_in_region)
    
    def draw_line(self, color_or_entity, start_x=None, start_y=None, direction=None, end_x=None, end_y=None):
        """
        Draws a line on the grid, with three possible modes:
        1. If `start_x`, `start_y`, and `direction` are provided, it draws a line starting at (start_x, start_y)
        in the specified direction (dir_x, dir_y) until it hits the grid's edge.
        2. If `start_x`, `start_y`, `end_x`, and `end_y` are provided, it draws a line from start to end.
        3. If an `Entity` object is provided as the first argument (`color_or_entity`), it draws the entity
        repeatedly in the given `direction` until the entity reaches the grid’s edge.
        """
        # Mode 1: Draw line with start point and direction
        if isinstance(color_or_entity, int) and start_x is not None and start_y is not None and direction is not None:
            color = color_or_entity
            dir_x, dir_y = direction
            x, y = start_x, start_y

            # Ensure direction values are valid
            if not (dir_x in (-1, 0, 1) and dir_y in (-1, 0, 1)):
                raise ValueError("Direction values must be -1, 0, or 1.")

            # Draw line until the edge of the grid is reached
            while 0 <= x < self.rows and 0 <= y < self.cols:
                self.set_cell(x, y, color)
                x += dir_x  # Move up/down
                y += dir_y  # Move left/right

        # Mode 2: Draw line from start to specified end point
        elif isinstance(color_or_entity, int) and start_x is not None and start_y is not None and end_x is not None and end_y is not None:
            color = color_or_entity
            dx = end_x - start_x
            dy = end_y - start_y

            # Determine the direction and increment
            if dx == 0:  # Vertical line
                step = 1 if dy > 0 else -1
                for y in range(start_y, end_y + step, step):
                    self.set_cell(start_x, y, color)

            elif dy == 0:  # Horizontal line
                step = 1 if dx > 0 else -1
                for x in range(start_x, end_x + step, step):
                    self.set_cell(x, start_y, color)

            elif abs(dx) == abs(dy):  # Diagonal line
                x_step = 1 if dx > 0 else -1
                y_step = 1 if dy > 0 else -1
                x, y = start_x, start_y
                for _ in range(abs(dx) + 1):
                    self.set_cell(x, y, color)
                    x += x_step
                    y += y_step

            else:
                raise ValueError("Only vertical, horizontal, or perfectly diagonal lines are supported.")

        # Mode 3: Draw an entity repeatedly in a direction
        elif isinstance(color_or_entity, Entity) and direction is not None:
            entity = color_or_entity
            dir_x, dir_y = direction

            # Ensure direction values are valid
            if not (dir_x in (-1, 0, 1) and dir_y in (-1, 0, 1)):
                raise ValueError("Direction values must be -1, 0, or 1.")

            while True:
                # Check if any part of the entity goes out of bounds
                if any(
                    not (0 <= cell.position[0] < self.rows and 0 <= cell.position[1] < self.cols)
                    for cell in entity.cells
                ):
                    break

                # Draw the entity in its current position
                for cell in entity.cells:
                    x, y = cell.position
                    self.set_cell(x, y, cell.color)

                # Move the entity
                entity.move(dir_x, dir_y)

    @classmethod
    def from_entity(cls, entity):
        """
        Creates a Grid object with dimensions matching the entity's bounding box,
        populates it with the entity's cells, and returns it.
        
        Args:
            entity (Entity): The entity to convert into a grid.

        Returns:
            Grid: A new grid populated with the entity's cells.
        """
        # Get bounds of the entity to determine grid dimensions
        min_x, min_y, max_x, max_y = entity.get_bounds()
        grid_width = max_y - min_y + 1
        grid_height = max_x - min_x + 1

        # Initialize a new grid with these dimensions
        grid = cls(grid_height, grid_width, default_color=0)

        # Populate the grid with the entity's cells
        for cell in entity.cells:
            # Calculate the local position within the grid based on bounds
            local_x = cell.position[0] - min_x
            local_y = cell.position[1] - min_y
            # Set the cell color in the grid
            grid.set_cell(local_x, local_y, cell.color)

        return grid
    

    def subdivide(self, div):
        """
        Subdivides each cell in the grid into a subgrid of size div x div, 
        effectively scaling up the grid by the factor of div.

        Parameters:
        - div (int): The subdivision factor. Each grid cell will become a div x div subgrid.
        """
        if div < 1:
            raise ValueError("Subdivision factor must be at least 1.")
        
        # Calculate new grid dimensions
        new_rows = self.rows * div
        new_cols = self.cols * div
        
        # Create a new grid to store the subdivided cells
        new_grid = [[None for _ in range(new_cols)] for _ in range(new_rows)]
        
        for x in range(self.rows):
            for y in range(self.cols):
                original_color = self.get_cell(x, y).color
                
                # Populate the subgrid for the current cell
                for i in range(div):
                    for j in range(div):
                        new_x = x * div + i
                        new_y = y * div + j
                        new_grid[new_x][new_y] = GridCell(original_color, new_x, new_y)
        
        # Update the grid's properties
        self.rows = new_rows
        self.cols = new_cols
        self.grid = new_grid

    def stitch(self, added_grid, direction):
        """
        Stitches the added_grid to one of the sides of the current grid.

        Parameters:
        - added_grid (Grid): The grid to be stitched onto the current grid.
        - direction (int): The side to stitch the grid to:
            0 - Top
            1 - Bottom
            2 - Left
            3 - Right

        Returns:
        - Grid: A new grid with the added grid stitched to the specified side.
        """
        if direction not in (0, 1, 2, 3):
            raise ValueError("Direction must be 0 (top), 1 (bottom), 2 (left), or 3 (right).")

        # Get the dimensions of the original and added grids
        self_rows, self_cols = self.rows, self.cols
        added_rows, added_cols = added_grid.rows, added_grid.cols

        # Determine the dimensions of the new grid
        if direction == 0:  # Top
            new_rows = self_rows + added_rows
            new_cols = max(self_cols, added_cols)
        elif direction == 1:  # Bottom
            new_rows = self_rows + added_rows
            new_cols = max(self_cols, added_cols)
        elif direction == 2:  # Left
            new_rows = max(self_rows, added_rows)
            new_cols = self_cols + added_cols
        elif direction == 3:  # Right
            new_rows = max(self_rows, added_rows)
            new_cols = self_cols + added_cols

        # Initialize the new grid
        new_grid = Grid(new_rows, new_cols, default_color=0)

        # Copy the cells from the original grid
        for x in range(self_rows):
            for y in range(self_cols):
                new_grid.set_cell(x, y, self.get_cell(x, y).color)

        # Copy the cells from the added grid to the specified side
        if direction == 0:  # Top
            for x in range(added_rows):
                for y in range(added_cols):
                    new_grid.set_cell(x, y, added_grid.get_cell(x, y).color)
            for x in range(self_rows):
                for y in range(self_cols):
                    new_grid.set_cell(x + added_rows, y, self.get_cell(x, y).color)

        elif direction == 1:  # Bottom
            for x in range(self_rows):
                for y in range(self_cols):
                    new_grid.set_cell(x, y, self.get_cell(x, y).color)
            for x in range(added_rows):
                for y in range(added_cols):
                    new_grid.set_cell(x + self_rows, y, added_grid.get_cell(x, y).color)

        elif direction == 2:  # Left
            for x in range(added_rows):
                for y in range(added_cols):
                    new_grid.set_cell(x, y, added_grid.get_cell(x, y).color)
            for x in range(self_rows):
                for y in range(self_cols):
                    new_grid.set_cell(x, y + added_cols, self.get_cell(x, y).color)

        elif direction == 3:  # Right
            for x in range(self_rows):
                for y in range(self_cols):
                    new_grid.set_cell(x, y, self.get_cell(x, y).color)
            for x in range(added_rows):
                for y in range(added_cols):
                    new_grid.set_cell(x, y + self_cols, added_grid.get_cell(x, y).color)

        return new_grid

    def connect_with_line(self, color, e1, e2):
        """
        Draws a line of the specified color connecting the closest point of e1 to e2.

        Parameters:
            color (int): The color of the line to be drawn.
            e1 (Entity): The first entity.
            e2 (Entity): The second entity.
        """
        def get_closest_points(e1, e2):
            """
            Finds the pair of points (one from each entity) that are closest to each other.
            
            Returns:
                (x1, y1), (x2, y2): Closest points from e1 and e2, respectively.
            """
            min_distance = float('inf')
            closest_pair = None
            
            for cell1 in e1.cells:
                for cell2 in e2.cells:
                    dist = abs(cell1.position[0] - cell2.position[0]) + abs(cell1.position[1] - cell2.position[1])
                    if dist < min_distance:
                        min_distance = dist
                        closest_pair = (cell1.position, cell2.position)
            
            return closest_pair

        # Get the closest points between the two entities
        (x1, y1), (x2, y2) = get_closest_points(e1, e2)

        # Determine the direction to move from (x1, y1) to (x2, y2)
        dx = 1 if x2 > x1 else -1 if x2 < x1 else 0
        dy = 1 if y2 > y1 else -1 if y2 < y1 else 0

        # Draw the line
        x, y = x1, y1
        while (x, y) != (x2, y2):
            self.set_cell(x, y, color)
            if x != x2:
                x += dx
            if y != y2:
                y += dy
        # Set the endpoint
        self.set_cell(x2, y2, color)

    def is_subdivision_valid(self):
        """
        Checks if the grid contains horizontal and vertical lines of any color that subdivide the grid.

        Returns:
            Tuple[bool, int, int, int]:
                - True, the color of the gridlines, the number of rows, and the number of columns in the original grid.
                - False, 0, 0, 0 if no valid subdivisions exist.
        """
        rows, cols = self.rows, self.cols

        # Find horizontal subdivision lines
        horizontal_lines = []
        horizontal_color = None
        for x in range(rows):
            line_colors = {self.get_cell(x, y).color for y in range(cols) if self.get_cell(x, y).color != 0}
            if len(line_colors) == 1:  # Ensure all cells in the line have the same color
                horizontal_lines.append(x)
                horizontal_color = line_colors.pop()  # Get the color of the horizontal line

        # Find vertical subdivision lines
        vertical_lines = []
        vertical_color = None
        for y in range(cols):
            line_colors = {self.get_cell(x, y).color for x in range(rows) if self.get_cell(x, y).color != 0}
            if len(line_colors) == 1:  # Ensure all cells in the line have the same color
                vertical_lines.append(y)
                vertical_color = line_colors.pop()  # Get the color of the vertical line

        # Check if there is at least one subdivision line in both directions
        if len(horizontal_lines) > 1 and len(vertical_lines) > 1:
            # Verify horizontal and vertical line colors are consistent
            if horizontal_color == vertical_color:
                # Calculate the dimensions of the original grid based on the subdivision lines
                original_rows = len(horizontal_lines) - 1
                original_cols = len(vertical_lines) - 1
                return True, horizontal_color, self.rows, self.cols
            else:
                raise ValueError("Inconsistent gridline colors for horizontal and vertical lines.")
        
        return False, 0, 0, 0



    def grid_to_subgrid(self):
        """
        Converts a subdivided grid into its representative smaller grid.

        Returns:
            Grid: The transformed grid, representing the subdivisions.
        """
        is_valid, gridline_color, original_rows, original_cols = self.is_subdivision_valid()
        if not is_valid:
            raise ValueError("The grid does not have valid subdivisions.")

        rows, cols = self.rows, self.cols

        # Find horizontal and vertical subdivision lines
        horizontal_lines = [
            x for x in range(rows) if all(self.get_cell(x, y).color == gridline_color for y in range(cols))
        ]
        vertical_lines = [
            y for y in range(cols) if all(self.get_cell(x, y).color == gridline_color for x in range(rows))
        ]

        # Handle cases where gridlines may or may not include borders
        if horizontal_lines[0] != 0:
            horizontal_lines.insert(0, 0)  # Include the top border
        if horizontal_lines[-1] != rows - 1:
            horizontal_lines.append(rows)  # Include the bottom border
        if vertical_lines[0] != 0:
            vertical_lines.insert(0, 0)  # Include the left border
        if vertical_lines[-1] != cols - 1:
            vertical_lines.append(cols)  # Include the right border

        # Create the new grid based on the number of cells
        subgrid_rows = len(horizontal_lines) - 1
        subgrid_cols = len(vertical_lines) - 1
        new_grid = Grid(subgrid_rows, subgrid_cols)

        # Iterate over each subgrid cell to determine its color
        for i in range(subgrid_rows):
            for j in range(subgrid_cols):
                # Define the bounds for each cell in the original grid
                top = horizontal_lines[i]
                bottom = horizontal_lines[i + 1]
                left = vertical_lines[j]
                right = vertical_lines[j + 1]

                # Collect all colors within the block
                block_colors = set(
                    self.get_cell(x, y).color
                    for x in range(top + 1 if top != 0 else top, bottom)
                    for y in range(left + 1 if left != 0 else left, right)
                )

                # If the block has more than one color, raise an error
                if len(block_colors) > 1:
                    raise ValueError(f"Block at ({i}, {j}) contains multiple colors: {block_colors}")

                # Assign the color to the new grid
                new_grid.set_cell(i, j, block_colors.pop())

        return new_grid


    def subgrid_to_grid(self, original_rows, original_cols, line_color):
        """
        Converts a subgrid back to the original grid representation by scaling up its cells
        and restoring gridlines between scaled cells.

        Parameters:
            original_rows (int): The number of rows in the original grid.
            original_cols (int): The number of columns in the original grid.

        Returns:
            Grid: The reconstructed grid with scaled-up cells and gridlines.
        """
        subgrid_rows, subgrid_cols = self.rows, self.cols

        # Calculate scaling factors for rows and columns
        row_scale = (original_rows + 1) // subgrid_rows
        col_scale = (original_cols + 1) // subgrid_cols

        # Validate that scaling factors produce valid dimensions
        if subgrid_rows * row_scale - 1 != original_rows or subgrid_cols * col_scale - 1 != original_cols:
            raise ValueError("Original dimensions do not match subgrid scaling.")

        # Create the reconstructed grid
        reconstructed_grid = Grid(original_rows, original_cols)

        # Fill the scaled-up cells and add gridlines
        for i in range(subgrid_rows):
            for j in range(subgrid_cols):
                cell_color = self.get_cell(i, j).color

                # Top-left corner of the scaled-up block
                top = i * row_scale
                left = j * col_scale

                # Bottom-right corner (excluding gridlines)
                bottom = top + row_scale - 1
                right = left + col_scale - 1

                # Fill the corresponding area in the reconstructed grid
                for x in range(top, bottom):
                    for y in range(left, right):
                        reconstructed_grid.set_cell(x, y, cell_color)

                # Add gridlines
                if i < subgrid_rows - 1:  # Horizontal gridline
                    for y in range(left, right):
                        reconstructed_grid.set_cell(bottom, y, line_color)

                if j < subgrid_cols - 1:  # Vertical gridline
                    for x in range(top, bottom):
                        reconstructed_grid.set_cell(x, right, line_color)
        # Explicitly handle gridline intersections
        for x in range(row_scale - 1, original_rows + 1, row_scale):
            for y in range(col_scale - 1, original_cols + 1, col_scale):
                if x < original_rows and y < original_cols:
                    reconstructed_grid.set_cell(x, y, line_color)
        return reconstructed_grid


    def is_split(self):
        """
        Determines if the grid is divided by a horizontal or vertical nonblack (color != 0) line.
        
        Returns:
            int: 
                -1 if the grid is divided by a horizontal nonblack line,
                1 if the grid is divided by a vertical nonblack line,
                0 if the grid is not divided by a nonblack line.
        """
        rows, cols = self.rows, self.cols

        # Check for horizontal division
        for x in range(rows):
            if all(self.get_cell(x, y).color != 0 for y in range(cols)):
                return -1  # Found a horizontal nonblack line

        # Check for vertical division
        for y in range(cols):
            if all(self.get_cell(x, y).color != 0 for x in range(rows)):
                return 1  # Found a vertical nonblack line

        # No dividing line found
        return 0
    
    def is_half_empty(self):
        """
        Checks if either half of the grid (top/bottom or left/right) is entirely empty (all black cells).

        Returns:
            bool: True if one half of the grid is empty, False otherwise.
        """
        mid_row = self.rows // 2
        mid_col = self.cols // 2

        # Check top and bottom halves
        top_empty = all(self.get_cell(x, y).color == 0 for x in range(mid_row) for y in range(self.cols))
        bottom_empty = all(self.get_cell(x, y).color == 0 for x in range(mid_row, self.rows) for y in range(self.cols))

        # Check left and right halves
        left_empty = all(self.get_cell(x, y).color == 0 for x in range(self.rows) for y in range(mid_col))
        right_empty = all(self.get_cell(x, y).color == 0 for x in range(self.rows) for y in range(mid_col, self.cols))

        return top_empty or bottom_empty or left_empty or right_empty


    def __repr__(self):
        grid_repr = "\n".join([" ".join([str(cell.color) for cell in row]) for row in self.grid])
        return f"Grid({self.rows}x{self.cols}):\n{grid_repr}"
