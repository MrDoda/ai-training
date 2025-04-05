import random

# Module-level variable to store the chosen rule function.
_selected_rule = None

def step(row):
    global _selected_rule
    if _selected_rule is None:
        rules = [
            two_neighbors,
            three_neighbors,
            exactly_two_neighbors,
            exactly_three_neighbors,
            at_least_one_neighbor,
            at_most_one_neighbor,
            even_neighbors,
            odd_neighbors,
            divisible_by_three,
            majority_rule,
            minority_rule,
            always_dead_rule,
            always_alive_rule,
            copy_rule,
            sum_plus_self_rule,
            double_threshold_rule,
            alternating_rule,
            weighted_rule,
            random_flip_rule,
            zero_rule,
            inverted_rule,
            parity_rule,
            mirror_rule
        ]
        _selected_rule = random.choice(rules)
        print(f"Using rule: {_selected_rule.__name__}")
    new_row = []
    for i in range(len(row)):
        new_row = _selected_rule(new_row, i, row)
    return new_row


def printrow(row):
    """
    Prints the row to the console using a block for alive cells.
    """
    print("".join("█" if cell == 1 else " " for cell in row))


# RULE FUNCTIONS – each takes (new_row, i, row) and appends the new state for cell i.

def two_neighbors(new_row, i, row):
    if i == 0:
        print("Applying two_neighbors: Cell becomes alive if at least 2 neighbors (positions -2, -1, +1, +2) are alive.")
    alive_neighbors = 0
    length = len(row)
    for offset in (-2, -1, 1, 2):
        idx = i + offset
        if 0 <= idx < length:
            alive_neighbors += row[idx]
    new_row.append(1 if alive_neighbors >= 2 else 0)
    return new_row

def three_neighbors(new_row, i, row):
    if i == 0:
        print("Applying three_neighbors: Cell becomes alive if at least 3 neighbors are alive.")
    alive_neighbors = sum(row[idx] for offset in (-2, -1, 1, 2)
                          for idx in [i + offset] if 0 <= idx < len(row))
    new_row.append(1 if alive_neighbors >= 3 else 0)
    return new_row

def exactly_two_neighbors(new_row, i, row):
    if i == 0:
        print("Applying exactly_two_neighbors: Cell becomes alive if exactly 2 neighbors are alive.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors == 2 else 0)
    return new_row

def exactly_three_neighbors(new_row, i, row):
    if i == 0:
        print("Applying exactly_three_neighbors: Cell becomes alive if exactly 3 neighbors are alive.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors == 3 else 0)
    return new_row

def at_least_one_neighbor(new_row, i, row):
    if i == 0:
        print("Applying at_least_one_neighbor: Cell becomes alive if at least 1 neighbor is alive.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors >= 1 else 0)
    return new_row

def at_most_one_neighbor(new_row, i, row):
    if i == 0:
        print("Applying at_most_one_neighbor: Cell becomes alive if at most 1 neighbor is alive.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors <= 1 else 0)
    return new_row

def even_neighbors(new_row, i, row):
    if i == 0:
        print("Applying even_neighbors: Cell becomes alive if the number of alive neighbors is even.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors % 2 == 0 else 0)
    return new_row

def odd_neighbors(new_row, i, row):
    if i == 0:
        print("Applying odd_neighbors: Cell becomes alive if the number of alive neighbors is odd.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors % 2 == 1 else 0)
    return new_row

def divisible_by_three(new_row, i, row):
    if i == 0:
        print("Applying divisible_by_three: Cell becomes alive if alive neighbors count is divisible by 3.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors % 3 == 0 else 0)
    return new_row

def majority_rule(new_row, i, row):
    if i == 0:
        print("Applying majority_rule: Cell becomes alive if more than 2 neighbors (out of 4) are alive.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors > 2 else 0)
    return new_row

def minority_rule(new_row, i, row):
    if i == 0:
        print("Applying minority_rule: Cell becomes alive if fewer than 2 neighbors are alive.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors < 2 else 0)
    return new_row

def always_dead_rule(new_row, i, row):
    if i == 0:
        print("Applying always_dead_rule: Cell is always dead.")
    new_row.append(0)
    return new_row

def always_alive_rule(new_row, i, row):
    if i == 0:
        print("Applying always_alive_rule: Cell is always alive.")
    new_row.append(1)
    return new_row

def copy_rule(new_row, i, row):
    if i == 0:
        print("Applying copy_rule: Cell copies its own state.")
    new_row.append(row[i])
    return new_row

def sum_plus_self_rule(new_row, i, row):
    if i == 0:
        print("Applying sum_plus_self_rule: Cell becomes alive if (neighbors sum + self) is at least 2.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    total = alive_neighbors + row[i]
    new_row.append(1 if total >= 2 else 0)
    return new_row

def double_threshold_rule(new_row, i, row):
    if i == 0:
        print("Applying double_threshold_rule: If cell is alive, needs >=2 neighbors; if dead, needs >=3 to become alive.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    if row[i] == 1:
        new_row.append(1 if alive_neighbors >= 2 else 0)
    else:
        new_row.append(1 if alive_neighbors >= 3 else 0)
    return new_row

def alternating_rule(new_row, i, row):
    if i == 0:
        print("Applying alternating_rule: Even indices require >=2 neighbors; odd indices require >=1 neighbor.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    if i % 2 == 0:
        new_row.append(1 if alive_neighbors >= 2 else 0)
    else:
        new_row.append(1 if alive_neighbors >= 1 else 0)
    return new_row

def weighted_rule(new_row, i, row):
    if i == 0:
        print("Applying weighted_rule: Outer neighbors count as 0.5, inner as 1; cell alive if weighted sum >=2.")
    weighted_sum = 0
    length = len(row)
    weights = { -2: 0.5, -1: 1, 1: 1, 2: 0.5 }
    for offset, weight in weights.items():
        idx = i + offset
        if 0 <= idx < length:
            weighted_sum += row[idx] * weight
    new_row.append(1 if weighted_sum >= 2 else 0)
    return new_row

def random_flip_rule(new_row, i, row):
    if i == 0:
        print("Applying random_flip_rule: Uses two_neighbors rule then flips result with 30% chance.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    state = 1 if alive_neighbors >= 2 else 0
    if random.random() < 0.3:
        state = 0 if state == 1 else 1
    new_row.append(state)
    return new_row

def zero_rule(new_row, i, row):
    if i == 0:
        print("Applying zero_rule: Cell becomes alive only if there are no alive neighbors.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if alive_neighbors == 0 else 0)
    return new_row

def inverted_rule(new_row, i, row):
    if i == 0:
        print("Applying inverted_rule: Inverts the result of two_neighbors rule.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    state = 1 if alive_neighbors >= 2 else 0
    new_row.append(0 if state == 1 else 1)
    return new_row

def parity_rule(new_row, i, row):
    if i == 0:
        print("Applying parity_rule: Cell becomes alive if parity of alive neighbors equals its own state.")
    alive_neighbors = sum(row[i + offset] for offset in (-2, -1, 1, 2)
                          if 0 <= i + offset < len(row))
    new_row.append(1 if (alive_neighbors % 2 == row[i]) else 0)
    return new_row

def mirror_rule(new_row, i, row):
    if i == 0:
        print("Applying mirror_rule: Cell copies the state of its immediate left neighbor (or itself if none).")
    if i - 1 >= 0:
        new_row.append(row[i - 1])
    else:
        new_row.append(row[i])
    return new_row
