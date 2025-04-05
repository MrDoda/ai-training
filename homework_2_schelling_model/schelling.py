import random
from config import GRID_ROWS, GRID_COLS, CELL_SIZE, GRID_ORIGIN_X, GRID_ORIGIN_Y, COLOR_EMPTY, COLOR_TYPE1, COLOR_TYPE2, COLOR_GRID_LINE

def initialize_representation(density=0.9):
    """
    Returns a 2D list (GRID_ROWS x GRID_COLS) where each cell is:
      0: empty
      1: agent type 1
      2: agent type 2
    Cells are occupied with probability 'density'. When occupied, the agent type is chosen at random.
    """
    rep = []
    for i in range(GRID_ROWS):
        row = []
        for j in range(GRID_COLS):
            if random.random() < density:
                row.append(random.choice([1, 2]))
            else:
                row.append(0)
        rep.append(row)
    return rep

def is_satisfied(rep, i, j, threshold=0.5):
    """
    Checks if the agent at position (i, j) is satisfied.
    An agent is satisfied if the fraction of like-type neighbors among non-empty neighbors is at least 'threshold'.
    Uses the Moore neighborhood (up to 8 neighbors).
    If an agent has no neighbors, it is considered satisfied.
    """
    agent_type = rep[i][j]
    if agent_type == 0:
        return True
    like = 0
    total = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = i + di
            nj = j + dj
            if 0 <= ni < GRID_ROWS and 0 <= nj < GRID_COLS:
                neighbor = rep[ni][nj]
                if neighbor != 0:
                    total += 1
                    if neighbor == agent_type:
                        like += 1
    if total == 0:
        return True
    return (like / total) >= threshold

def step(rep, threshold=0.5):
    """
    Executes one step of Schelling’s model:
      - Finds unsatisfied agents.
      - Moves each unsatisfied agent to a randomly chosen empty cell.
    Returns the updated representation.
    """
    unsatisfied = []
    empty_cells = []
    # Identify unsatisfied agents and empty cells.
    for i in range(GRID_ROWS):
        for j in range(GRID_COLS):
            if rep[i][j] == 0:
                empty_cells.append((i, j))
            else:
                if not is_satisfied(rep, i, j, threshold):
                    unsatisfied.append((i, j))
    random.shuffle(unsatisfied)
    # Move each unsatisfied agent if an empty cell is available.
    for (i, j) in unsatisfied:
        if empty_cells:
            new_pos = random.choice(empty_cells)
            empty_cells.remove(new_pos)
            rep[new_pos[0]][new_pos[1]] = rep[i][j]
            rep[i][j] = 0
            empty_cells.append((i, j))
    return rep

def plot(rep, surface):
    """
    Draws the current state of the Schelling model on the given Pygame surface.
    Each cell is drawn as a rectangle with its color determined by its state.
    Grid lines are also drawn.
    """
    import pygame
    for i in range(GRID_ROWS):
        for j in range(GRID_COLS):
            cell = rep[i][j]
            if cell == 0:
                color = COLOR_EMPTY
            elif cell == 1:
                color = COLOR_TYPE1
            elif cell == 2:
                color = COLOR_TYPE2
            else:
                color = COLOR_EMPTY
            x = GRID_ORIGIN_X + j * CELL_SIZE
            y = GRID_ORIGIN_Y + i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)
    # Draw grid lines
    for i in range(GRID_ROWS + 1):
        y = GRID_ORIGIN_Y + i * CELL_SIZE
        pygame.draw.line(surface, COLOR_GRID_LINE, (GRID_ORIGIN_X, y), (GRID_ORIGIN_X + GRID_COLS * CELL_SIZE, y))
    for j in range(GRID_COLS + 1):
        x = GRID_ORIGIN_X + j * CELL_SIZE
        pygame.draw.line(surface, COLOR_GRID_LINE, (x, GRID_ORIGIN_Y), (x, GRID_ORIGIN_Y + GRID_ROWS * CELL_SIZE))
