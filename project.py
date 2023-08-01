import time
import numpy as np
import random
import os
import inputimeout
import sys
import art


current_score = 0


def main():
    print(art.text2art("TETRIS"))
    print(
        """
-> press d + ENTER to move block to the right\n
-> press a + ENTER to move block to the left\n
-> press w + ENTER to rotate block clockwise\n
-> press s + ENTER to rotate block anti-clockwise\n
            """
    )
    while True:
        resp = input("Continue (y/n)? ")
        if resp == "y":
            grid = initialize()
            tetris = blocks()
            while True:
                os.system("clear")
                game(grid, tetris)
        elif resp == "n":
            sys.exit("GAME OVER")
        else:
            continue


def game(grid, tetris):
    block = random.choice(tetris)
    if game_over(grid, block):
        sys.exit("***GAME OVER***\nYOUR SCORE IS {}".format(current_score))
    fall(grid, block)


def initialize():
    grid = np.empty((10, 6), dtype=str)
    grid[:] = " "
    return grid


def blocks():
    i = np.array([["#", "#", "#", "#"]])

    j = np.array([["#", " ", " "], ["#", "#", "#"]])

    l = np.array([[" ", " ", "#"], ["#", "#", "#"]])

    o = np.array([["#", "#"], ["#", "#"]])

    s = np.array([[" ", "#", "#"], ["#", "#", " "]])

    t = np.array([[" ", "#", " "], ["#", "#", "#"]])

    z = np.array([["#", "#", " "], [" ", "#", "#"]])

    blocks = [i, j, l, o, s, t, z]

    return blocks

def fall(grid, block):
    col_num = 0
    grid_copy_1 = np.copy(grid)
    grid_copy_2 = np.copy(grid)
    global current_score
    current_score = score(grid, current_score, grid_copy_2)
    for row_num in range(grid.shape[0]):
        col_num, block = move_or_rotate(col_num, row_num, block, grid)
        os.system("clear")
        if update(grid, block, row_num, col_num, grid_copy_1, grid_copy_2):
            break
        print(grid)
        print("CURRENT SCORE:", current_score)
        grid_copy_1 = np.copy(grid)
        time.sleep(1)
        if row_num == len(grid) - len(block):
            break
        clean(grid, block, row_num, col_num)


def update(grid, block, row_num, col_num, grid_copy_1, grid_copy_2):
    grid_frag = grid_copy_2[
        row_num : len(block) + row_num, col_num : len(block[0]) + col_num
    ]
    for row in range(block.shape[0]):
        for col in range(block.shape[1]):
            if block[row][col] == " ":
                if grid_frag[row][col] == " ":
                    grid[row + row_num][col + col_num] = " "
                elif grid_frag[row][col] == "#":
                    grid[row + row_num][col + col_num] = "#"
            elif block[row][col] == "#":
                if grid_frag[row][col] == " ":
                    grid[row + row_num][col + col_num] = "#"
                elif grid_frag[row][col] == "#":
                    grid[:] = grid_copy_1
                    return True
    return False


def clean(grid, block, row_num, col_num):
    grid[row_num : len(block) + row_num, col_num : len(block[0]) + col_num] = " "


def score(grid, score, grid_copy_2):
    full_rows = []
    for row in range(grid.shape[0]):
        if np.all(grid[row] == "#"):
            full_rows.append(row)
    score += 1000 * len(full_rows)
    trimmed = np.delete(grid, full_rows, 0)
    rows_to_add = np.empty((len(full_rows), grid.shape[1]), dtype=str)
    rows_to_add[:] = " "
    trimmed = np.vstack((rows_to_add, trimmed))
    grid[:] = trimmed
    grid_copy_2[:] = trimmed
    return score


def game_over(grid, block):
    filled_rows = np.sum(np.any(grid == "#", axis=1))
    if filled_rows >= len(grid) - len(block) + 1:
        return True
    else:
        return False


def get_direction():
    try:
        direction = inputimeout.inputimeout(prompt="", timeout=1)
        return direction
    except inputimeout.TimeoutOccurred:
        return ""


def move_or_rotate(col_num, row_num, block, grid):
    try:
        move = get_direction()
        if not move:
            return col_num, block
        elif move == "a":
            col_num -= 1
            if col_num < 0:
                raise NegativeIndexError
            return col_num, block
        elif move == "d":
            col_num += 1
            if col_num + len(block[0]) >= grid.shape[1]:
                raise BeyondGridIndexError
            return col_num, block
        elif move == "w":
            if row_num + len(np.rot90(block, -1)) > grid.shape[0]:  # clockwise
                raise BeneathGridIndexError
            elif np.any(
                grid[
                    row_num : row_num + len(np.rot90(block, -1)),
                    col_num : col_num + np.rot90(block, -1).shape[1],
                ]
                == "#"
            ):
                return col_num, block
            return col_num, np.rot90(block, -1)
        elif move == "s":
            if row_num + len(np.rot90(block, 1)) > grid.shape[0]:  # anti-clockwise
                raise BeneathGridIndexError
            elif np.any(
                grid[
                    row_num : row_num + len(np.rot90(block, 1)),
                    col_num : col_num + np.rot90(block, 1).shape[1],
                ]
                == "#"
            ):
                return col_num, block
            return col_num, np.rot90(block, 1)
        else:
            return col_num, block
    except NegativeIndexError:
        col_num = 0
        return col_num, block
    except BeyondGridIndexError:
        col_num = grid.shape[1] - len(block[0])
        return col_num, block
    except BeneathGridIndexError:
        return col_num, block


class NegativeIndexError(Exception):
    pass


class BeyondGridIndexError(Exception):
    pass


class BeneathGridIndexError(Exception):
    pass


if __name__ == "__main__":
    main()
