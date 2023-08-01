# CS50P-final-project
This was my CS50P final project. The premise was to create a simple implementation of the game of Tetris. The repository contains the source code, and tests 

# THE GAME OF TETRIS
    #### Video Demo:  https://youtu.be/LNm8VxaKcgo
## Description:
The program is a simple implementation of Tetris video game using third-party libraries ([numpy](https://numpy.org/), [inputimeout](https://pypi.org/project/inputimeout/) and [art](https://pypi.org/project/art/)) and built-in libraries (time, random, os and sys). The program contains score counter and allows users to move or rotate Tetronominos.
## Structure:
### main function:

Main function contains ASCII art imitating title screen and also short instructions explaining how to play the game. It also conatains infinite loop that allows user to choose whether to continue with the game or quit. If the response is ```y``` the grid (playing area) is generated with [initialize()](#grid-generation) function. The **tetris** variable is also generated here by calling a function [blocks()](#blocks-generation). After that there is another infinite loop created. New iteration of the loop starts when the current block stops to fall down. It contains function that cleans terminal (```os.system("clean")```) what erases the previous grid printed there each time the new block starts to fall down. Inside the loop there is also a [game()](#game-function) function.

Otherwise, if the response is ```n``` the program exists with "GAME OVER" message and if the user inputs something different then ```y``` or ```n``` the message about continuing the game is still printed.

A global variable **current_score** is initialized.

``` python
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
                os.system("cls")
                game(grid, tetris)
        elif resp == "n":
            sys.exit("GAME OVER")
        else:
            continue
```

### Grid generation

The grid or game area is generated with ```initialize()``` function. It declares a **10 x 6** empty [numpy.array](https://numpy.org/doc/stable/reference/generated/numpy.array.html) which is filled with whitespaces. The reason for choosing arrays insted of lists was because they offer a greater variety of possible functionalities that can be applied to them.
``` python
def initialize():
    grid = np.empty((10, 6), dtype=str)
    grid[:] = " "
    return grid
```

### Blocks generation

Just as in real Tetris there are seven different Tetronominos which are, in this case, arrays. Blocks are represented by the layout of hashes. There is also a list called **blocks** that contains all seven of Tetronominos and the function returns this list.

```python

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
```

### game function

The function takes two arguments **grid** and **tetris**. The block that will fall down is chosen at random. The return value of [game_over()](#game-over) is also checked within the function and if it is ```True``` it exits the program with the message the contains the final score of the user. Otherwise, the [fall()](#fall-function) function is executed.

```python
def game(grid, tetris):
    block = random.choice(tetris)
    if game_over(grid, block):
        sys.exit("***GAME OVER***\nYOUR SCORE IS {}".format(current_score))
    fall(grid, block)
```

### fall function

The block starts to fall down from column number ```0```. Then, two copies of the grid are made which are essential for the correct work of [update()](#updating-positions-of-the-grid) function and their premise is explained in the section where mentioned function is described. Then global variable **current_score** that contains the actual score of the player is updated with the return value of [score()](#calculating-score) function. Next, there is ```for``` loop that iterates through the indices of the grid's rows. Inside the loop, there is [move_or_rotate()](#moving-and-rotating) function that allows user to move block to the left or to the right or rotate clockwise or anti-clockwise. Since, each iteration of the loop results in grid being printed it was essential for readbility reasons to clean the terminal during each iteration with ```os.system("clean")```. There is also ```if``` statement and mentioned [update()](#updating-positions-of-the-grid) function. One of the copies declared outside the loop is updated. The block that falls changes its position after ```1``` second (```time.sleep(1)```). The function also assesses whether the block hits the bottom of the grid with the second ```if``` statement. If it does the loop is stopped. Function [clean()](#cleaning-the-grid) clears the current position of the block creating the illusion of falling down.

```python
def fall(grid, block):
    col_num = 0
    grid_copy_1 = np.copy(grid)
    grid_copy_2 = np.copy(grid)
    global current_score
    current_score = score(grid, current_score, grid_copy_2)
    for row_num in range(grid.shape[0]):
        col_num, block = move_or_rotate(col_num, row_num, block, grid)
        os.system("cls")
        if update(grid, block, row_num, col_num, grid_copy_1, grid_copy_2):
            break
        print(grid)
        print("CURRENT SCORE:", current_score)
        grid_copy_1 = np.copy(grid)
        time.sleep(1)
        if row_num == len(grid) - len(block):
            break
        clean(grid, block, row_num, col_num)
```
### Updating positions of the grid

The premise of the ```update()``` function is to update the empty positions of the grid with block. The function takes ```5``` arguments which are **grid**, **block**, **row_num**, **col_num**, **grid_copy_1** and **grid_copy_2**. First, a part of the grid is sliced and stored in the variable **grid_frag**. The necessity of using the **grid_copy_2** to cut the fragment of the grid is mainly caused by matching **l** and **j** with the ones that are already at the bottom of the grid. These two are the only ones that contain neighbouring whitespaces and beacuse of the nature of [clean()](#cleaning-the-grid) function using the original will result in overwriting one of the hashes that already is the part of the grid with whitespaces. Since the cleaning is only applied to the original grid, not the copy it will not affect the matching of **l** and **j** blocks. The size of the fragment corresponds to the actual size of the block and to the current position of it. The cells are updated one by one iterating through rows and columns.

```python
def update(grid, block, row_num, col_num, grid_copy_1, grid_copy_2):
    grid_frag = grid_copy_2[
        row_num : len(block) + row_num, col_num : len(block[0]) + col_num
    ]
    for row in range(block.shape[0]):
        for col in range(block.shape[1]):
```

There are multiple ```if``` statements within the function:

- the first ```if``` statement checks whether the block has a whitespace in cell and if the corresponding cell from grid also contains whitespace. If so, the grid is updated with whitespace (is basically left unchanged). As it comes to ```elif``` statement it checks whether the a part of the grid contains "#" and if it does it updates grid with "#". Utilizing this approach prevents overwriting already filled cell with whitespace.

```python
            if block[row][col] == " ":
                if grid_frag[row][col] == " ":
                    grid[row + row_num][col + col_num] = " "
                elif grid_frag[row][col] == "#":
                    grid[row + row_num][col + col_num] = "#"
```

- the ```elif``` statement check whether the block at current cell contains "#". If it does and if the cell from corresponding grid fragment does not it will update the cell with "#". If the cell in grid already contains the "#" orginal grid is replaced by copy of grid from previous iteration of ```for``` loop and returns ```True``` value what results in breaking from the loop as the block hit the new bottom which is in fact the stack of previously fallen blocks.

```python
            elif block[row][col] == "#":
                if grid_frag[row][col] == " ":
                    grid[row + row_num][col + col_num] = "#"
                elif grid_frag[row][col] == "#":
                    grid[:] = grid_copy_1
                    return True
```

To sum up, **update()** function updates cells in grid based on the contents of cells in blocks one by one using nested loops. It utilizes copies of grid: **grid_copy_1** being the copy of grid from previous iteration of the ```for``` loop and **grid_copy_2** which is a copy that is not modified within the mentioned ```for``` loop and is needed for matching blocks at the bottom of the grid (especially when it comes to **l** and **j** blocks) since it is not affected by [clean()](#cleaning-the-grid) function. It prevents filled cells that already are at the bottom of the grid to be uncontrollably overwritten.

### Cleaning the grid

Function ```clean()``` creates the illusion of blocks falling down. The function is called at the end of the [fall()](#fall-function) function and replaces cells in grid modified by block with whitespaces.

```python
def clean(grid, block, row_num, col_num):
    grid[row_num : len(block) + row_num, col_num : len(block[0]) + col_num] = " "
```

### Calculating score

Points are added to the score count when at least one, entire row is filled with hashes. The function calculates the number of fully filled rows and the number of such rows multiplied by ```1000``` is added to the current score. Next, filled rows are deleted from grid and new rows filled with whitespaces are added using [numpy.vstack](https://numpy.org/doc/stable/reference/generated/numpy.vstack.html) to trimmed grid to maintain the original number of rows. Both original grid and **grid_copy_2** are updated with the new grid. The score is returned and is printed in each iteration of ```for``` loop in [fall()](#fall-function) function.
```python
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
```

### Game over

The game is over when blocks stacked in grid hit the ceiling. The function calculates number of rows that contain at least one hash. The ```if``` statement assesses whether the number is sufficient to fit another block. If it is not, program exits with a message. Function ```game_over()``` is called inside [game()](#game-function) function.

```python
def game_over(grid, block):
    filled_rows = np.sum(np.any(grid == "#", axis=1))
    if filled_rows >= len(grid) - len(block) + 1:
        return True
    else:
        return False
```

### Interactivity
Function ```get_direction()``` allows user to move or rotate the falling block. It is done by using the functionality of [inputimeout](https://pypi.org/project/inputimeout/) module **inputimeout**. It gives the user a limited amount of time (1 second) to interact with the block. Even if the user fails to provide any input the program will continue to execute. When no direction is provided on time the exception ```TimeoutOccurred``` is raised.
```python
def get_direction():
    try:
        direction = inputimeout.inputimeout(prompt="", timeout=1)
        return direction
    except inputimeout.TimeoutOccurred:
        return ""
```
### Moving and rotating
A return value of ```get_direction()``` is assigned to **move** variable. Next the value is checked via a couple of ```if``` statements.
```python
def move_or_rotate(col_num, row_num, block, grid):
    try:
        move = get_direction()
```
#### move variable is empty
```if``` statement checks whether the **move** variable is empty. If it is **col_num** and **block** remain unchanged
```python
        if not move:
            return col_num, block
```
#### move variable is equal to ```a```
```elif``` statement checks whether the variable **move** is equal to ```a``` what should result in block moving left. Variable **col_num** is decremented and it is checked whether the mentioned variable is less then ```0```. If it does the custom exception ```NegativeIndexError``` is raised and the **col_num** is set to ```0```. Creating custom exception and handling it in mentioned way was necessary since it does not allow the block to move outside the grid to the left side. If **col_num** is greater or equal than ```0``` the function returns its modified version and not modified **block**.
```python
        elif move == "a":
            col_num -= 1
            if col_num < 0:
                raise NegativeIndexError
            return col_num, block
```
```python
class NegativeIndexError(Exception):
    pass
```
```python
    except NegativeIndexError:
        col_num = 0
        return col_num, block
```
#### move variable is equal to ```d```
```elif``` statement checks whether ```move``` variable is equal to ```d```, what should move the block to the right. The **col_num** variable is incremented. Then the sum of modified **col_num** and the number of columns of block is checked whether it is greater or equal than the number of columns of the game area. If it is ```True``` custom error ```BeyondGridIndexError``` is raised. The exception is handled what results in modifying the value of column **col_num** to the difference of the number of columns in grid and number of columns in block. Creating custom exception and handling way in mentioned way was necesseary to prevent blocks from going off the grid to the right. If the mentioned condition is ```False``` it returns modified **col_num** and unmodified **block**.
```python
        elif move == "d":
            col_num += 1
            if col_num + len(block[0]) >= grid.shape[1]:
                raise BeyondGridIndexError
            return col_num, block
```
```python
class BeyondGridIndexError(Exception):
    pass
```
```python
    except BeyondGridIndexError:
        col_num = grid.shape[1] - len(block[0])
        return col_num, block
```
#### move is equal to ```w``` or ```s```
```elif``` statement checks whether the **move** variable is equal to ```w```, what should result in rotating the block clockwise. ```if``` statement checks whether the sum of current **row_num** and length of rotated block is greater than the number of rows in grid. If it is ```True``` the custom error ```BeneathGridIndexError``` is raised. The exception handling results in returning unmodified **col_num** and **block**. This way, the program will not allow to rotate the block if there is a risk of getting out of the grid after rotating the block. There is also ```elif``` statement that checks whether the rotation will result in hitting stacked blocks at the bottom of the grid. If it is ```True``` it returns unmodified versions of **col_num** and **block**. If both conditions are ```False``` the function returns unmodified **col_num** and **block** which was rotated clockwise with [numpy.rot90](https://numpy.org/doc/stable/reference/generated/numpy.rot90.html). An identical methodology was applied to **move** is equal to ```s``` except, in this case, the block is rotated anti-clockwise.
```python
        elif move == "w":
            if row_num + len(np.rot90(block, -1)) > grid.shape[0]:
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
            if row_num + len(np.rot90(block, 1)) > grid.shape[0]:
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
```
```python
class BeneathGridIndexError(Exception):
    pass
```
```python
    except BeneathGridIndexError:
        return col_num, block
```
## Summary
Created was a simple version of Tetris video game with basic functionality. As for the research done, implementation of Tetris from scratch (without PyGame) is rare. The project has potential to be further developed e.g. adding score multiplier and removing the need of pressing ENTER each time the user interacts with program, which would make moving and rotating more responsive. Test file was created to check the correctness of couple of functions.





