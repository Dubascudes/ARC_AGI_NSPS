from GridTools.GridCell import GridCell
class Entity:
    def __init__(self, cells):
        """Initialize an Entity with a list of GridCell objects."""
        self.cells = cells  # List of GridCell objects making up the entity

    def get_bounds(self):
        """Calculate the bounding box of the entity."""
        xs = [cell.position[0] for cell in self.cells]
        ys = [cell.position[1] for cell in self.cells]
        return min(xs), min(ys), max(xs), max(ys)

    def scale(self, old_size, new_size):
        """
        Scales the entity from the original bounds to a new specified size.
        
        Parameters:
            old_size (tuple): The original dimensions (width, height) of the entity.
            new_size (tuple): The desired dimensions (new_width, new_height) for the scaled entity.
        
        Returns:
            Entity: A new, scaled-down or scaled-up Entity object.
        """
        min_x, min_y, max_x, max_y = self.get_bounds()
        original_width, original_height = old_size
        new_width, new_height = new_size

        # Determine the scaling factors for width and height
        scale_x = original_width / new_width
        scale_y = original_height / new_height

        # Prepare cells for the new scaled entity
        scaled_cells = []

        # Iterate through the new grid dimensions and fill each cell
        for new_x in range(new_width):
            for new_y in range(new_height):
                # Calculate the region in the original entity that maps to this scaled cell
                start_x = int(min_x + new_x * scale_x)
                end_x = int(min_x + (new_x + 1) * scale_x)
                start_y = int(min_y + new_y * scale_y)
                end_y = int(min_y + (new_y + 1) * scale_y)

                # Collect colors of cells in this block
                block_colors = [
                    cell.color
                    for cell in self.cells
                    if start_x <= cell.position[0] < end_x and start_y <= cell.position[1] < end_y
                ]

                # Check if all cells in the block have the same color
                if len(block_colors) > 0 and all(color == block_colors[0] for color in block_colors):
                    # Use the uniform color for the scaled cell
                    scaled_color = block_colors[0]
                else:
                    # If not uniform, default to a color (e.g., background or mixed color indicator)
                    scaled_color = 0  # Set to a default color if blocks have mixed colors

                # Add the scaled cell to the list
                scaled_cell = GridCell(scaled_color, new_x, new_y)
                scaled_cells.append(scaled_cell)

        # Return the new scaled entity
        return Entity(scaled_cells)

    def get_dim(self):
        minx, miny, maxx, maxy = self.get_bounds()
        return maxx - minx, maxy - miny

    def get_cells_ordinal(self, orientation):
        """
        Returns a new Entity object representing a "slice" of the original entity along one of its sides.
        Orientation:
        0 = top, 1 = bottom, 2 = left, 3 = right
        """
        min_x, min_y, max_x, max_y = self.get_bounds()
        slice_cells = []


        if orientation == 0:  # Top
            slice_cells = [cell for cell in self.cells if cell.position[0] == min_x]

        elif orientation == 1:  # Bottom
            slice_cells = [cell for cell in self.cells if cell.position[0] == max_x]

        elif orientation == 2:  # Left
            slice_cells = [cell for cell in self.cells if cell.position[1] == min_y]

        elif orientation == 3:  # Right
            slice_cells = [cell for cell in self.cells if cell.position[1] == max_y]

        else:
            raise ValueError("Invalid orientation. Use 0 for top, 1 for bottom, 2 for left, or 3 for right.")

        return Entity(slice_cells)

    def move(self, dx, dy):
        """Move the entity by (dx, dy)."""
        for cell in self.cells:
            new_x = cell.position[0] + dx
            new_y = cell.position[1] + dy
            cell.position = (new_x, new_y)

    def fill_by_color(self, new_color, old_color=0):
        """
        Replace all cells of the specified old_color in the entity with new_color.
        
        Parameters:
        - new_color (int): The color to apply to cells.
        - old_color (int): The color to replace. Defaults to 0.
        """
        for cell in self.cells:
            if cell.color == old_color:
                cell.color = new_color
                
        return self
    

    def set_color(self, new_color):
        """
        Replace all cells of the specified old_color in the entity with new_color.
        
        Parameters:
        - new_color (int): The color to apply to cells.
        - old_color (int): The color to replace. Defaults to 0.
        """
        for cell in self.cells:
            cell.color = new_color
                
        return self

    def is_rectangle_with_hole(self):
        """
        Returns True if the entity is a rectangle with a hole on one of its sides.
        """
        min_x, min_y, max_x, max_y = self.get_bounds()
        
        # Check that the entity fills the entire rectangle, except for a hole in one side
        grid = [[0] * (max_y - min_y + 1) for _ in range(max_x - min_x + 1)]

        # Mark the cells in the grid
        for cell in self.cells:
            x, y = cell.position
            grid[x - min_x][y - min_y] = 1

        # Check each side for a hole
        for side, (dx, dy) in enumerate([(0, 1), (0, -1), (1, 0), (-1, 0)]):  # right, left, bottom, top
            has_hole = False
            filled_cells = 0
            for i in range(min_x, max_x + 1) if dy == 0 else range(min_y, max_y + 1):
                if dy == 0:  # horizontal (top or bottom)
                    x, y = i, min_y if dx == 0 else max_y
                else:  # vertical (left or right)
                    x, y = min_x if dy == -1 else max_x, i
                if grid[x - min_x][y - min_y] == 0:
                    has_hole = True
                else:
                    filled_cells += 1
            if has_hole and filled_cells > 0:
                return True
        return False

    def get_color(self):
        """
        Returns the color of the entity if all non-zero cells share the same color.
        If there are no non-zero cells or if they don't match, returns None.
        """
        non_zero_colors = {cell.color for cell in self.cells if cell.color != 0}

        # Check if there's only one unique non-zero color
        if len(non_zero_colors) == 1:
            return non_zero_colors.pop()
        else:
            return None
    def get_hole(self):
        """
        Identifies and returns an Entity object representing the hole in the current entity.
        The hole is defined as a group of unfilled cells within the entity's bounding box.
        """
        min_x, min_y, max_x, max_y = self.get_bounds()
        hole_cells = []

        # Create a grid representation of the entity’s area
        entity_grid = [[False] * (max_y - min_y + 1) for _ in range(max_x - min_x + 1)]
        for cell in self.cells:
            x, y = cell.position
            entity_grid[x - min_x][y - min_y] = True

        # Check for empty spaces (holes) within the entity’s bounding box
        for i in range(max_x - min_x + 1):
            for j in range(max_y - min_y + 1):
                if not entity_grid[i][j]:  # Cell is empty in the entity grid
                    hole_cells.append(GridCell(0, min_x + i, min_y + j))  # Fill the hole cells with color 0
        self.hole = Entity(hole_cells)
        return Entity(hole_cells)

    def get_orientation(self, quality):
        """
        Returns the orientation of the specified quality (e.g., 'hole') as an integer.
        0 = up, 1 = down, 2 = left, 3 = right
        """
        if quality == "hole":
            min_x, min_y, max_x, max_y = self.get_bounds()
            grid_width = max_y - min_y + 1
            grid_height = max_x - min_x + 1

            # Create a grid representation of the entity's cells
            grid = [[0] * grid_width for _ in range(grid_height)]
            for cell in self.cells:
                x, y = cell.position
                grid[x - min_x][y - min_y] = 1

            # Check each side for a hole (any cell with a 0 along a filled side)
            # Top side
            if any(grid[0][j] == 0 for j in range(grid_width)):
                return 0  # Up

            # Bottom side
            if any(grid[grid_height - 1][j] == 0 for j in range(grid_width)):
                return 1  # Down

            # Left side
            if any(grid[i][0] == 0 for i in range(grid_height)):
                return 2  # Left

            # Right side
            if any(grid[i][grid_width - 1] == 0 for i in range(grid_height)):
                return 3  # Right

            return -1  # No hole found on any side
        else:
            raise ValueError(f"Unknown quality '{quality}' for orientation check")
        

    def __repr__(self):
        return f"Entity(cells={self.cells})"
