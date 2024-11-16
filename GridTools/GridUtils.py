# GridUtils.py

from GridTools.Grid import Grid
from GridTools.GridCell import GridCell
from GridTools import GridTransformation  # If needed
from GridTools.Entity import Entity
from collections import Counter
from itertools import combinations


def get_silhouette(grid):
    x = grid.rows
    y = grid.cols
    return Grid(x, y)
def get_color_counts(grid):
    """
    Returns a list of counts of each color in the grid.
    The list has 9 elements, corresponding to colors 0 through 8.
    """
    color_counts = [0] * 9  # Initialize counts for colors 0-8

    for row in grid.grid:
        for cell in row:
            color = cell.color
            if 0 <= color <= 8:
                color_counts[color] += 1
            else:
                # Handle unexpected color values
                print(f"Warning: Found unexpected color value {color}")
    return color_counts

def get_surrounded(grid, color):
    """
    Returns a list of Entity objects where each entity is a grid cell
    (or connected group of cells) not of the specified color but surrounded
    by cells of the specified color.
    """
    entities = []
    visited = set()
    rows = grid.rows
    cols = grid.cols

    for x in range(rows):
        for y in range(cols):
            cell = grid.get_cell(x, y)
            if (x, y) not in visited and cell.color != color:
                if is_surrounded(grid, x, y, color):
                    entity_cells = explore_entity(grid, x, y, color, visited)
                    entity = Entity(entity_cells)
                    entities.append(entity)
    print(len(entities))
    return entities

def is_surrounded(grid, x, y, surround_color):
    """
    Checks if the cell at (x, y) is surrounded by cells of surround_color.
    """
    rows = grid.rows
    cols = grid.cols

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbor_color = grid.get_cell(nx, ny).color
            if neighbor_color != surround_color:
                return False
        else:
            # Edge cells cannot be fully surrounded
            return False
    return True

def explore_entity(grid, x, y, surround_color, visited):
    """
    Performs a flood fill to find all connected cells starting from (x, y)
    that are surrounded by surround_color.
    """
    stack = [(x, y)]
    entity_cells = []
    rows = grid.rows
    cols = grid.cols

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        cell = grid.get_cell(cx, cy)
        if cell.color == surround_color:
            continue  # Skip cells of the surround color
        if not is_surrounded(grid, cx, cy, surround_color):
            continue  # Ensure each cell is surrounded

        entity_cells.append(cell)

        # Explore neighboring cells (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbor = grid.get_cell(nx, ny)
                if neighbor.color != surround_color and (nx, ny) not in visited:
                    stack.append((nx, ny))
    return entity_cells


def get_all_entities_by_color(grid):
    colors = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    all_entities = [0] * len(colors)
    for c in range (0, len(colors)):
        all_entities[c] = get_entities_by_color(grid, colors[c])
    return all_entities



def combine_entities(entities):
    """
    Combines a list of entities into a single entity.
    
    Parameters:
        entities (list of Entity): A list of entities to combine.
        
    Returns:
        Entity: A new entity containing all unique cells from the input entities.
    """
    # Use a set to store all unique cells across entities
    combined_cells = set()
    
    # Add cells from each entity in the list to the set
    for entity in entities:
        combined_cells.update(entity.cells)
    
    # Convert the set back to a list and create a new Entity with the combined cells
    combined_entity = Entity(list(combined_cells))
    
    return combined_entity


def get_entities_by_color(grid, color):
    """
    Finds all groups of connected cells with the specified color in the grid.
    Each group is represented as an Entity object.
    """
    entities = []
    visited = set()  # To keep track of already visited cells
    rows = grid.rows
    cols = grid.cols

    for x in range(rows):
        for y in range(cols):
            cell = grid.get_cell(x, y)
            if (x, y) not in visited and cell.color == color:
                # Explore this new entity of connected cells of the specified color
                entity_cells = explore_connected_cells(grid, x, y, color, visited)
                entities.append(Entity(entity_cells))

    return entities

def get_isolated_entities(grid):
    """
    Finds all groups of connected colored cells that are isolated from other groups.
    Isolation means no neighboring group is horizontally, vertically, or diagonally adjacent.

    Parameters:
        grid (Grid): The grid to search within.

    Returns:
        List[Entity]: A list of Entity objects, where each Entity represents
                      a group of isolated colored cells.
    """
    isolated_groups = []
    visited = set()  # Keep track of visited cells
    rows, cols = grid.rows, grid.cols

    # Directions for 8-connected neighbors
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-left, top, top-right
        (0, -1),          (0, 1),   # Left,       right
        (1, -1), (1, 0), (1, 1)     # Bottom-left, bottom, bottom-right
    ]

    def explore_group(x, y, color):
        """
        Perform a flood fill to gather all connected cells of the same color.
        """
        stack = [(x, y)]
        group_cells = []

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            cell = grid.get_cell(cx, cy)
            if cell.color == 0:
                continue
            group_cells.append(cell)

            # Add all valid neighbors to the stack
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                    stack.append((nx, ny))

        return group_cells

    for x in range(rows):
        for y in range(cols):
            if (x, y) in visited or grid.get_cell(x, y).color == 0:
                continue

            # Start exploring a new group
            color = grid.get_cell(x, y).color
            group_cells = explore_group(x, y, color)

            if group_cells:
                isolated_groups.append(Entity(group_cells))

    return isolated_groups



def get_isolated_cells(grid):
    """
    Finds all isolated cells in the grid. An isolated cell has no horizontal,
    vertical, or diagonal neighbors that are non-black (color != 0).
    
    Parameters:
        grid (Grid): The grid to search within.
        
    Returns:
        List[Entity]: A list of Entity objects where each Entity represents
                      a single isolated cell.
    """
    isolated_entities = []
    rows, cols = grid.rows, grid.cols

    # Directions for 8-connected neighbors
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-left, top, top-right
        (0, -1),          (0, 1),   # Left,       right
        (1, -1), (1, 0), (1, 1)     # Bottom-left, bottom, bottom-right
    ]

    for x in range(rows):
        for y in range(cols):
            cell = grid.get_cell(x, y)
            if cell.color == 0:  # Skip black cells
                continue
            
            # Check all neighbors
            is_isolated = True
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:  # Valid neighbor position
                    neighbor = grid.get_cell(nx, ny)
                    if neighbor.color != 0:  # Neighbor is non-black
                        is_isolated = False
                        break

            if is_isolated:
                # Create an entity for the isolated cell
                isolated_entities.append(Entity([cell]))

    return isolated_entities

def get_common_color(grid, no_black = False):
    """
    Returns the color integer that is most commonly seen among all entities on the grid.
    """
    color_counts = Counter()
    start = 1 if no_black else 0
    # Assuming color range is 0-8 (adjust if other colors are possible)
    for color in range(start, 9):  
        entities = get_entities_by_color(grid, color)
        color_counts[color] += len(entities)

    # Find the color with the highest entity count
    most_common_color, _ = color_counts.most_common(1)[0]
    
    return most_common_color







def get_all_entities_by_shape(grid):
    """
    Groups all entities on the grid by their shape, excluding single-cell entities.

    Parameters:
        grid (Grid): The grid to analyze.

    Returns:
        List[List[Entity]]: A list of lists of entities, where each list contains entities of the same shape.
    """
    def normalize_entity_shape(entity):
        """
        Normalize the positions of an entity's cells relative to (0, 0) for shape comparison.
        """
        min_x, min_y, _, _ = entity.get_bounds()
        normalized_positions = {(cell.position[0] - min_x, cell.position[1] - min_y) for cell in entity.cells}
        return frozenset(normalized_positions)  # Use frozenset for hashable type

    def explore_entity_with_diagonals(grid, x, y, visited):
        """
        Explore an entity's cells including diagonally connected cells.
        """
        stack = [(x, y)]
        entity_cells = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            cell = grid.get_cell(cx, cy)
            if cell.color == 0:  # Ignore background color
                continue
            entity_cells.append(cell)
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < grid.rows and 0 <= ny < grid.cols and (nx, ny) not in visited:
                    neighbor = grid.get_cell(nx, ny)
                    if neighbor.color == cell.color:  # Add diagonally connected cells
                        stack.append((nx, ny))
        return entity_cells

    # Get all entities from the grid
    all_entities = []
    visited = set()
    
    for x in range(grid.rows):
        for y in range(grid.cols):
            if (x, y) not in visited and grid.get_cell(x, y).color != 0:  # Assuming 0 is the background
                entity_cells = explore_entity_with_diagonals(grid, x, y, visited)
                if entity_cells and len(entity_cells) > 1:  # Exclude single-cell entities
                    all_entities.append(Entity(entity_cells))
    
    # Group entities by their normalized shapes
    shape_groups = {}
    
    for entity in all_entities:
        shape = normalize_entity_shape(entity)
        if shape not in shape_groups:
            shape_groups[shape] = []
        shape_groups[shape].append(entity)
    
    # Convert the shape_groups dictionary to a list of lists
    grouped_entities = list(shape_groups.values())
    
    return grouped_entities



def get_entities_by_shape(grid, target_entity):
    """
    Finds all entities in the grid that have the same shape as the input target entity.
    
    Parameters:
        grid (Grid): The grid to search within.
        target_entity (Entity): The target entity whose shape we want to match.
    
    Returns:
        List[Entity]: A list of Entity objects in the grid that match the shape of target_entity.
    """
    
    def normalize_entity_shape(entity):
        """
        Normalize the positions of an entity's cells relative to (0, 0) for shape comparison.
        """
        min_x, min_y, _, _ = entity.get_bounds()
        normalized_positions = {(cell.position[0] - min_x, cell.position[1] - min_y) for cell in entity.cells}
        return normalized_positions

    # Get the normalized shape of the target entity
    target_shape = normalize_entity_shape(target_entity)
    if not target_shape:  # Skip if the target entity is empty
        print("Target entity is empty, skipping shape matching.")
        return []

   # print(f"Target shape (normalized): {target_shape}")

    # List to store matching entities
    matching_entities = []

    # Visited cells to avoid recounting entities
    visited = set()

    # Loop through the grid to find entities
    for x in range(grid.rows):
        for y in range(grid.cols):
            if (x, y) not in visited and grid.get_cell(x, y).color != 0:  # Assuming color 0 is the background
                # Explore and create an entity from the current position
                entity_cells = explore_entity_cells(grid, x, y, visited)

                if entity_cells:  # Only consider non-empty entities
                    entity = Entity(entity_cells)
                    entity_shape = normalize_entity_shape(entity)
                    #print(f"Entity shape (normalized): {entity_shape}")

                    # Check if the shapes match
                    if entity_shape == target_shape:
                        matching_entities.append(entity)

    return matching_entities

def explore_entity_cells(grid, x, y, visited):
    """
    Finds all connected cells starting from (x, y) that form an entity.
    Marks cells as visited and only includes cells that are not background color (assumed to be color 0).
    """
    stack = [(x, y)]
    entity_cells = []
    color = grid.get_cell(x, y).color

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue
        visited.add((cx, cy))
        cell = grid.get_cell(cx, cy)

        if cell.color == color:
            entity_cells.append(cell)
            # Check neighbors for connection
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Only cardinal directions
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < grid.rows and 0 <= ny < grid.cols and (nx, ny) not in visited:
                    neighbor = grid.get_cell(nx, ny)
                    if neighbor.color == color:
                        stack.append((nx, ny))

    return entity_cells


def explore_connected_cells(grid, x, y, color, visited):
    """
    Helper function to perform a flood fill and find all connected cells
    starting from (x, y) that are of the specified color.
    """
    stack = [(x, y)]
    connected_cells = []

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))
        cell = grid.get_cell(cx, cy)
        if cell.color == color:
            connected_cells.append(cell)

            # Check neighbors (up, down, left, right)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < grid.rows and 0 <= ny < grid.cols and (nx, ny) not in visited:
                    neighbor = grid.get_cell(nx, ny)
                    if neighbor.color == color:
                        stack.append((nx, ny))

    return connected_cells


def plus_sign(color, position=(0, 0)):
    """
    Returns an Entity representing a plus sign with the specified color, 
    positioned on a larger grid based on the given position offset.
    """
    pos_x, pos_y = position
    cells = []
    
    # Center row and center column
    for i in range(3):
        cells.append(GridCell(color, pos_x + 1, pos_y + i))  # Center row
        cells.append(GridCell(color, pos_x + i, pos_y + 1))  # Center column
    
    return Entity(cells)



def corners(color, position=(0, 0)):
    """
    Returns an Entity representing only the corners with the specified color, 
    positioned on a larger grid based on the given position offset.
    """
    pos_x, pos_y = position
    cells = [
        GridCell(color, pos_x + 0, pos_y + 0),  # Top-left
        GridCell(color, pos_x + 0, pos_y + 2),  # Top-right
        GridCell(color, pos_x + 2, pos_y + 0),  # Bottom-left
        GridCell(color, pos_x + 2, pos_y + 2)   # Bottom-right
    ]
    
    return Entity(cells)

def diagonals(color, direction=0, position=(0, 0)):
    """
    Returns an Entity representing a diagonal with the specified color, 
    positioned on a larger grid based on the given position offset.
    
    direction=0 draws from top-left to bottom-right,
    direction=1 draws from bottom-left to top-right.
    """
    pos_x, pos_y = position
    cells = []
    
    if direction == 0:
        # Top-left to bottom-right
        for i in range(3):
            cells.append(GridCell(color, pos_x + i, pos_y + i))
    elif direction == 1:
        # Bottom-left to top-right
        for i in range(3):
            cells.append(GridCell(color, pos_x + (2 - i), pos_y + i))
    
    return Entity(cells)


def get_midpoint(entity1: Entity, entity2: Entity):
    """
    Returns the midpoint (x, y) between the centers of two entities.
    The midpoint is calculated as the average of the center positions of each entity.
    """
    # Calculate the center of entity1
    min_x1, min_y1, max_x1, max_y1 = entity1.get_bounds()
    center_x1 = (min_x1 + max_x1) / 2
    center_y1 = (min_y1 + max_y1) / 2

    # Calculate the center of entity2
    min_x2, min_y2, max_x2, max_y2 = entity2.get_bounds()
    center_x2 = (min_x2 + max_x2) / 2
    center_y2 = (min_y2 + max_y2) / 2

    # Calculate the midpoint between the two centers
    midpoint_x = (center_x1 + center_x2) / 2
    midpoint_y = (center_y1 + center_y2) / 2

    return (int(midpoint_x), int(midpoint_y))

def square(color, position=(0, 0)):
    """
    Returns an Entity representing a 3x3 square with a hole in the middle 
    with the specified color, positioned on a larger grid based on the given position offset.

    Parameters:
    - color (int): The color of the square's border.
    - position (tuple): The top-left position of the square in the grid (default is (0, 0)).

    Returns:
    - Entity: An Entity object representing the square with a hole in the middle.
    """
    pos_x, pos_y = position
    cells = [
        GridCell(color, pos_x + 0, pos_y + 0),  # Top-left
        GridCell(color, pos_x + 0, pos_y + 1),  # Top-center
        GridCell(color, pos_x + 0, pos_y + 2),  # Top-right
        GridCell(color, pos_x + 1, pos_y + 0),  # Middle-left
        # Middle-center is the hole, no cell added here
        GridCell(color, pos_x + 1, pos_y + 2),  # Middle-right
        GridCell(color, pos_x + 2, pos_y + 0),  # Bottom-left
        GridCell(color, pos_x + 2, pos_y + 1),  # Bottom-center
        GridCell(color, pos_x + 2, pos_y + 2),  # Bottom-right
    ]

    return Entity(cells)
def box(color, position=(0, 0)):
    """
    Returns an Entity representing a 3x3 square with a hole in the middle 
    with the specified color, positioned on a larger grid based on the given position offset.

    Parameters:
    - color (int): The color of the square's border.
    - position (tuple): The top-left position of the square in the grid (default is (0, 0)).

    Returns:
    - Entity: An Entity object representing the square with a hole in the middle.
    """
    pos_x, pos_y = position
    cells = [
        GridCell(color, pos_x + 0, pos_y + 0),  # Top-left
        GridCell(color, pos_x + 0, pos_y + 1),  # Top-center
        GridCell(color, pos_x + 0, pos_y + 2),  # Top-right
        GridCell(color, pos_x + 1, pos_y + 0),  # Middle-left
        GridCell(color, pos_x + 1, pos_y + 1),  # Middle-left
        GridCell(color, pos_x + 1, pos_y + 2),  # Middle-right
        GridCell(color, pos_x + 2, pos_y + 0),  # Bottom-left
        GridCell(color, pos_x + 2, pos_y + 1),  # Bottom-center
        GridCell(color, pos_x + 2, pos_y + 2),  # Bottom-right
    ]

    return Entity(cells)

def get_entity_distance(entity1, entity2):
    """
    Calculates the shortest Manhattan distance between any cell in entity1
    to any cell in entity2.

    Parameters:
    - entity1 (Entity): The first entity.
    - entity2 (Entity): The second entity.

    Returns:
    - int: The shortest Manhattan distance between any cell in the two entities.
    """
    min_distance = float('inf')

    for cell1 in entity1.cells:
        for cell2 in entity2.cells:
            distance = abs(cell1.position[0] - cell2.position[0]) + abs(cell1.position[1] - cell2.position[1])
            if distance < min_distance:
                min_distance = distance

    return min_distance

def find_corner_rectangles(grid):
    """
    Identifies all instances on the grid where there are 4 colored cells that form the corners of a rectangle.
    
    Parameters:
    - grid (Grid): The grid to search for corner rectangles.
    
    Returns:
    - List[Entity]: A list of entities, each representing a 'corner rectangle'.
    """
    rectangles = []
    cells_by_color = {}

    # Organize cells by color
    for x in range(grid.rows):
        for y in range(grid.cols):
            cell = grid.get_cell(x, y)
            if cell.color != 0:  # Ignore empty cells (color 0)
                if cell.color not in cells_by_color:
                    cells_by_color[cell.color] = []
                cells_by_color[cell.color].append(cell)

    # Check all combinations of four cells of the same color
    for color, cells in cells_by_color.items():
        for c1, c2, c3, c4 in combinations(cells, 4):
            # Extract positions of the four cells
            positions = {tuple(c1.position), tuple(c2.position), tuple(c3.position), tuple(c4.position)}

            # Check if these positions form a rectangle
            if forms_rectangle(positions):
                rectangles.append(Entity([c1, c2, c3, c4]))

    return rectangles

def forms_rectangle(positions):
    """
    Checks if the given set of four positions forms the corners of a rectangle.
    
    Parameters:
    - positions (set of tuples): A set of four (x, y) positions.
    
    Returns:
    - bool: True if the positions form a rectangle, False otherwise.
    """
    if len(positions) != 4:
        return False

    # Extract unique x and y coordinates
    xs = {x for x, y in positions}
    ys = {y for x, y in positions}

    # A rectangle must have exactly 2 unique x and y coordinates
    return len(xs) == 2 and len(ys) == 2



def is_aligned(e1, e2):
    """
    Returns True if there is any horizontal or vertical overlap between two entities,
    allowing for a straight line connection.

    Parameters:
        e1 (Entity): The first entity.
        e2 (Entity): The second entity.

    Returns:
        bool: True if the entities are aligned, False otherwise.
    """
    # Get bounds of both entities
    min_x1, min_y1, max_x1, max_y1 = e1.get_bounds()
    min_x2, min_y2, max_x2, max_y2 = e2.get_bounds()

    print(e1.get_bounds())
    print(e2.get_bounds())

    # Check for horizontal alignment
    if max_y1 >= min_y2 and min_y1 <= max_y2:
        # Horizontal overlap exists, check vertical gap
        #if min_x1 > max_x2 or min_x2 > max_x1:
            #return False  # No vertical connection possible
        return True

    # Check for vertical alignment
    if max_x1 >= min_x2 and min_x1 <= max_x2:
        # Vertical overlap exists, check horizontal gap
        #if min_y1 > max_y2 or min_y2 > max_y1:
            #return False  # No horizontal connection possible
        return True

    # No alignment found
    return False


from GridTools.Entity import Entity

def find_squares(grid, color=None):
    """
    Finds all squares of any dimension greater than a single grid cell in the grid.
    If a color is specified, only returns squares of that color.

    Parameters:
        grid (Grid): The grid to search within.
        color (int, optional): The color of squares to search for. If None, all colors are considered.

    Returns:
        List[Entity]: A list of Entity objects representing the squares.
    """
    rows, cols = grid.rows, grid.cols
    squares = []

    # Helper function to check if a square exists at (x, y) with side length `side`
    def is_square(x, y, side):
        for i in range(x, x + side):
            for j in range(y, y + side):
                if i >= rows or j >= cols:  # Out of bounds
                    return False
                cell = grid.get_cell(i, j)
                if cell.color != square_color:
                    return False
        return True

    visited = set()  # Track visited cells to avoid duplicate squares

    # Iterate over all possible starting points for squares
    for x in range(rows):
        for y in range(cols):
            cell = grid.get_cell(x, y)

            # Skip black cells or cells not matching the specified color
            if cell.color == 0 or (color is not None and cell.color != color):
                continue

            square_color = cell.color

            # Expand the square dimensionally as long as it's valid
            side = 2
            while is_square(x, y, side):
                # Create a list of cells for this square
                square_cells = [
                    grid.get_cell(i, j)
                    for i in range(x, x + side)
                    for j in range(y, y + side)
                ]

                # Ensure the square hasn't already been visited
                square_positions = {(cell.position[0], cell.position[1]) for cell in square_cells}
                if not visited.intersection(square_positions):
                    squares.append(Entity(square_cells))
                    visited.update(square_positions)

                side += 1  # Increase side length for the next iteration

    return squares


def is_split(grid):
    """
    Determines if the grid is divided by a horizontal or vertical nonblack (color != 0) line.
    
    Returns:
        int: 
            -1 if the grid is divided by a horizontal nonblack line,
             1 if the grid is divided by a vertical nonblack line,
             0 if the grid is not divided by a nonblack line.
    """
    rows, cols = grid.rows, grid.cols

    # Check for horizontal division
    for x in range(rows):
        if all(grid.get_cell(x, y).color != 0 for y in range(cols)):
            return -1  # Found a horizontal nonblack line

    # Check for vertical division
    for y in range(cols):
        if all(grid.get_cell(x, y).color != 0 for x in range(rows)):
            return 1  # Found a vertical nonblack line

    # No dividing line found
    return 0


def get_halves(grid):
    """
    Splits the grid into two halves if it is divided by a horizontal or vertical nonblack line.

    Returns:
        Tuple[Grid, Grid]:
            - The two halves of the grid (top/bottom or left/right).
        Raises:
            ValueError: If the grid is not divided by a valid nonblack line.
    """
    split_type = is_split(grid)  # Determine the type of split
    rows, cols = grid.rows, grid.cols

    if split_type == -1:  # Horizontal split
        for x in range(rows):
            if all(grid.get_cell(x, y).color != 0 for y in range(cols)):
                # Create top and bottom grids
                top_grid = Grid.from_list([row[:] for row in grid.to_list()[:x]])
                bottom_grid = Grid.from_list([row[:] for row in grid.to_list()[x+1:]])
                return top_grid, bottom_grid

    elif split_type == 1:  # Vertical split
        for y in range(cols):
            if all(grid.get_cell(x, y).color != 0 for x in range(rows)):
                # Create left and right grids
                left_grid = Grid.from_list([row[:y] for row in grid.to_list()])
                right_grid = Grid.from_list([row[y+1:] for row in grid.to_list()])
                return left_grid, right_grid

    # If no valid split, raise an error
    raise ValueError("The grid cannot be split into halves because it does not have a dividing nonblack line.")


def get_non_empty_half(grid):
    """
    Retrieves the non-empty half of a grid where one half (top/bottom or left/right) is completely empty.

    Parameters:
        grid (Grid): The input grid to check.

    Returns:
        Grid: A new grid containing the non-empty half.

    Raises:
        ValueError: If the grid does not have an empty half.
    """
    mid_row = grid.rows // 2
    mid_col = grid.cols // 2

    # Check top and bottom halves
    top_empty = all(grid.get_cell(x, y).color == 0 for x in range(mid_row) for y in range(grid.cols))
    bottom_empty = all(grid.get_cell(x, y).color == 0 for x in range(mid_row, grid.rows) for y in range(grid.cols))

    if top_empty:
        # Return the bottom half as a new grid
        return Grid.from_list([row[:] for row in grid.grid[mid_row:]])
    elif bottom_empty:
        # Return the top half as a new grid
        return Grid.from_list([row[:] for row in grid.grid[:mid_row]])

    # Check left and right halves
    left_empty = all(grid.get_cell(x, y).color == 0 for x in range(grid.rows) for y in range(mid_col))
    right_empty = all(grid.get_cell(x, y).color == 0 for x in range(grid.rows) for y in range(mid_col, grid.cols))

    if left_empty:
        # Return the right half as a new grid
        return Grid.from_list([row[mid_col:] for row in grid.grid])
    elif right_empty:
        # Return the left half as a new grid
        return Grid.from_list([row[:mid_col] for row in grid.grid])

    # Raise an error if no half is empty
    raise ValueError("Grid does not have an empty half.")
