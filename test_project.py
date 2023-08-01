import numpy as np
from project import initialize, blocks, score, game_over, move_or_rotate


def mock_get_direction_d():
    return "d"


def mock_get_direction_a():
    return "a"


def mock_get_direction_w():
    return "w"


def mock_get_direction_s():
    return "s"


def mock_false_direction():
    return ""


def test_initialize_size():
    grid = initialize()
    assert grid.shape == (10, 6)


def test_initialize_type():
    grid = initialize()
    assert np.all(grid == " ")


def test_blocks():
    block = blocks()
    assert len(block) == 7


def test_score():
    grid = initialize()
    grid_copy_2 = np.copy(grid)
    grid[grid.shape[0] - 3 :] = "#"
    high_score = score(grid, 1000, grid_copy_2)
    assert high_score == 4000


def test_game_over_false():
    grid = initialize()
    block = np.array([["#", "#", " "], [" ", "#", "#"]])
    grid[grid.shape[0] - 8 :, 4] = "#"
    over = game_over(grid, block)
    assert over is False


def test_game_over_true():
    grid = initialize()
    block = np.array([["#", "#", "#", "#"]])
    grid[grid.shape[0] - 10 :, 2] = "#"
    over = game_over(grid, block)
    assert over is True


def test_false_direction(monkeypatch):
    grid = initialize()
    block = np.array([["#", "#", "#", "#"]])
    col_num = 1
    row_num = 3
    monkeypatch.setattr("project.get_direction", mock_false_direction)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res == (col_num, block)


def test_move_or_rotate_right(monkeypatch):
    grid = initialize()
    block = np.array([["#", "#", "#", "#"]])
    col_num = 1
    row_num = 3
    monkeypatch.setattr("project.get_direction", mock_get_direction_d)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res == (col_num + 1, block)


def test_move_or_rotate_beyond(monkeypatch):
    grid = initialize()
    block = np.array([["#", "#", "#", "#"]])
    col_num = grid.shape[1] - len(block[0])
    row_num = 3
    monkeypatch.setattr("project.get_direction", mock_get_direction_d)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res == (col_num, block)


def test_move_or_rotate_left(monkeypatch):
    grid = initialize()
    block = np.array([["#", "#", "#", "#"]])
    col_num = 1
    row_num = 3
    monkeypatch.setattr("project.get_direction", mock_get_direction_a)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res == (col_num - 1, block)


def test_move_or_rotate_neg(monkeypatch):
    grid = initialize()
    block = np.array([["#", "#", "#", "#"]])
    col_num = 0
    row_num = 3
    monkeypatch.setattr("project.get_direction", mock_get_direction_a)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res == (0, block)


def test_move_or_rotate_clockwise(monkeypatch):
    grid = initialize()
    block = np.array([[" ", "#", " "], ["#", "#", "#"]])
    block_rot = np.array([["#", " "], ["#", "#"], ["#", " "]])
    col_num = 1
    row_num = 0
    monkeypatch.setattr("project.get_direction", mock_get_direction_w)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res[0] == col_num
    assert np.array_equal(res[1], block_rot)


def test_move_or_rotate_clockwise_beneath(monkeypatch):
    grid = initialize()
    block = np.array([[" ", "#", " "], ["#", "#", "#"]])
    block_rot = np.array([["#", " "], ["#", "#"], ["#", " "]])
    col_num = 3
    row_num = (grid.shape[0] - len(block_rot)) + 1
    monkeypatch.setattr("project.get_direction", mock_get_direction_w)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res[0] == col_num
    assert np.array_equal(res[1], block)


def test_move_or_rotate_counterc(monkeypatch):
    grid = initialize()
    block = np.array([[" ", "#", " "], ["#", "#", "#"]])
    block_rot = np.array([[" ", "#"], ["#", "#"], [" ", "#"]])
    col_num = 1
    row_num = 0
    monkeypatch.setattr("project.get_direction", mock_get_direction_s)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res[0] == col_num
    assert np.array_equal(res[1], block_rot)


def test_move_or_rotate_counterc_beneath(monkeypatch):
    grid = initialize()
    block = np.array([[" ", "#", " "], ["#", "#", "#"]])
    block_rot = np.array([[" ", "#"], ["#", "#"], [" ", "#"]])
    col_num = 3
    row_num = (grid.shape[0] - len(block_rot)) + 1
    monkeypatch.setattr("project.get_direction", mock_get_direction_s)
    res = move_or_rotate(col_num, row_num, block, grid)
    assert res[0] == col_num
    assert np.array_equal(res[1], block)
