
def is_empty(board):
    for row in board:
        for cell in row:
            if cell != " ":
                return False
    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    board_size = len(board)
    y_start = y_end - (length - 1) * d_y
    x_start = x_end - (length - 1) * d_x

    y_before = y_start - d_y
    x_before = x_start - d_x
    y_after = y_end + d_y
    x_after = x_end + d_x

    open_before = False
    open_after = False

    if 0 <= y_before < board_size and 0 <= x_before < board_size:
        if board[y_before][x_before] == " ":
            open_before = True
    else:
        open_before = False

    if 0 <= y_after < board_size and 0 <= x_after < board_size:
        if board[y_after][x_after] == " ":
            open_after = True
    else:
        open_after = False

    if open_before and open_after:
        return "OPEN"
    elif open_before or open_after:
        return "SEMIOPEN"
    else:
        return "CLOSED"


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    board_size = len(board)
    open_seq_count = 0
    semi_open_seq_count = 0

    row_cells = []
    y, x = y_start, x_start
    while 0 <= y < board_size and 0 <= x < board_size:
        row_cells.append(board[y][x])
        y += d_y
        x += d_x

    i = 0
    while i <= len(row_cells) - length:
        if row_cells[i] == col:
            match = True
            for offset in range(length):
                if row_cells[i + offset] != col:
                    match = False
                    break
            if match:
                before = i - 1
                after = i + length

                if ((before < 0 or row_cells[before] != col) and
                    (after >= len(row_cells) or row_cells[after] != col)):
                    seq_y_end = y_start + (i + length - 1) * d_y
                    seq_x_end = x_start + (i + length - 1) * d_x

                    seq_bound = is_bounded(board, seq_y_end, seq_x_end, length, d_y, d_x)

                    if seq_bound == "OPEN":
                        open_seq_count += 1
                    elif seq_bound == "SEMIOPEN":
                        semi_open_seq_count += 1

                    i += length
                    continue
        i += 1

    return open_seq_count, semi_open_seq_count


def detect_rows(board, col, length):
    board_size = len(board)
    total_open = 0
    total_semi_open = 0

    directions = [(0,1), (1,0), (1,1), (1,-1)]

    for d_y, d_x in directions:
        if d_y == 0 and d_x == 1:
            for y in range(board_size):
                open_seq, semi_open_seq = detect_row(board, col, y, 0, length, d_y, d_x)
                total_open += open_seq
                total_semi_open += semi_open_seq
        elif d_y == 1 and d_x == 0:
            for x in range(board_size):
                open_seq, semi_open_seq = detect_row(board, col, 0, x, length, d_y, d_x)
                total_open += open_seq
                total_semi_open += semi_open_seq
        elif d_y == 1 and d_x == 1:
            for x in range(board_size):
                open_seq, semi_open_seq = detect_row(board, col, 0, x, length, d_y, d_x)
                total_open += open_seq
                total_semi_open += semi_open_seq
            for y in range(1, board_size):
                open_seq, semi_open_seq = detect_row(board, col, y, 0, length, d_y, d_x)
                total_open += open_seq
                total_semi_open += semi_open_seq
        elif d_y == 1 and d_x == -1:
            for x in range(board_size):
                open_seq, semi_open_seq = detect_row(board, col, 0, x, length, d_y, d_x)
                total_open += open_seq
                total_semi_open += semi_open_seq
            for y in range(1, board_size):
                open_seq, semi_open_seq = detect_row(board, col, y, board_size - 1, length, d_y, d_x)
                total_open += open_seq
                total_semi_open += semi_open_seq

    return total_open, total_semi_open


def search_max(board):
    board_size = len(board)
    max_score_value = -float('inf')
    best_moves = []

    for y in range(board_size):
        for x in range(board_size):
            if board[y][x] == " ":
                board[y][x] = "b"
                current_score = score(board)
                board[y][x] = " "
                if current_score > max_score_value:
                    max_score_value = current_score
                    best_moves = [(y, x)]
                elif current_score == max_score_value:
                    best_moves.append((y, x))

    if not best_moves:
        return None, None

    return best_moves[0]


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b.get(5, 0) >= 1 or semi_open_b.get(5, 0) >=1:
        return MAX_SCORE

    elif open_w.get(5, 0) >=1 or semi_open_w.get(5,0) >=1:
        return -MAX_SCORE

    return (-10000 * (open_w.get(4,0) + semi_open_w.get(4,0)) + 
            500  * open_b.get(4,0)                     + 
            50   * semi_open_b.get(4,0)                + 
            -100  * open_w.get(3,0)                    + 
            -30   * semi_open_w.get(3,0)               + 
            50   * open_b.get(3,0)                     + 
            10   * semi_open_b.get(3,0)                +  
            open_b.get(2,0) + semi_open_b.get(2,0) - 
            open_w.get(2,0) - semi_open_w.get(2,0))


def is_win(board):
    board_size = len(board)

    def has_five(y, x, d_y, d_x, col):
        for i in range(5):
            ny = y + i * d_y
            nx = x + i * d_x
            if not (0 <= ny < board_size and 0 <= nx < board_size):
                return False
            if board[ny][nx] != col:
                return False
        before_y = y - d_y
        before_x = x - d_x
        after_y = y + 5 * d_y
        after_x = x + 5 * d_x
        if (0 <= before_y < board_size and 0 <= before_x < board_size and board[before_y][before_x] == col):
            return False
        if (0 <= after_y < board_size and 0 <= after_x < board_size and board[after_y][after_x] == col):
            return False
        return True

    for col, result in [("w", "White won"), ("b", "Black won")]:
        for y in range(board_size):
            for x in range(board_size):
                if board[y][x] == col:
                    directions = [(0,1), (1,0), (1,1), (1,-1)]
                    for d_y, d_x in directions:
                        if has_five(y, x, d_y, d_x, col):
                            return result

    for row in board:
        for cell in row:
            if cell == " ":
                return "Continue playing"

    return "Draw"


def print_board(board):
    board_size = len(board)
    header = "*" + "|".join(str(i % 10) for i in range(board_size)) + "*"
    print(header)
    for y in range(board_size):
        row = " " + str(y % 10) + " " + "|".join(board[y][x] for x in range(board_size)) + " *"
        print(row)
    footer = "*" * (board_size * 2 + 1)
    print(footer)


def make_empty_board(sz):
    return [[" " for _ in range(sz)] for _ in range(sz)]


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print(f"{full_name} stones:")
        for i in range(2, 6):
            open_count, semi_open_count = detect_rows(board, c, i)
            print(f"  Open rows of length {i}: {open_count}")
            print(f"  Semi-open rows of length {i}: {semi_open_count}")
        print()


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            if move_y is None or move_x is None:
                print("No possible moves. It's a draw!")
                return "Draw"

        print(f"Computer move: ({move_y}, {move_x})")
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res

        while True:
            try:
                print("Your move:")
                move_y = int(input(f"y coord (0-{board_size - 1}): "))
                move_x = int(input(f"x coord (0-{board_size - 1}): "))
                if not (0 <= move_y < board_size and 0 <= move_x < board_size):
                    print("Coordinates out of bounds. Please try again.")
                    continue
                if board[move_y][move_x] != " ":
                    print("Cell already occupied. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter integer coordinates.")

        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            print(game_res)
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        if 0 <= y < len(board) and 0 <= x < len(board[y]):
            board[y][x] = col
            y += d_y
            x += d_x
        else:
            break


def test_is_empty():
    board = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")


def test_is_bounded():
    board = make_empty_board(8)
    x = 5
    y = 1
    d_x = 0
    d_y = 1
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = y + (length - 1) * d_y
    x_end = x + (length - 1) * d_x

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5
    y = 1
    d_x = 0
    d_y = 1
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0, x, length, d_y, d_x) == (1, 0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")


def test_detect_rows():
    board = make_empty_board(8)
    x = 5
    y = 1
    d_x = 0
    d_y = 1
    length = 3
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col, length) == (1, 0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_boundary_sequences():
    board = make_empty_board(8)
    y = 4
    x = 7
    d_x = -1
    d_y = 1
    length = 4
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)

    if is_bounded(board, 7, 4, length, d_y, d_x) == "CLOSED":
        print("TEST CASE for boundary sequences PASSED")
    else:
        print("TEST CASE for boundary sequences FAILED")


def test_search_max():
    board = make_empty_board(8)
    x = 5
    y = 0
    d_x = 0
    d_y = 1
    length = 4
    col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)

    x = 6
    y = 0
    d_x = 0
    d_y = 1
    length = 4
    col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)

    print_board(board)

    expected_move = (4,6)
    optimal_move = search_max(board)
    if optimal_move == expected_move:
        print("TEST CASE for search_max PASSED")
    else:
        print(f"TEST CASE for search_max FAILED (Expected {expected_move}, Got {optimal_move})")


def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()


def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5
    x = 2
    d_x = 0
    d_y = 1
    length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)


    y = 3
    x = 5
    d_x = -1
    d_y = 1
    length = 2
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)


    y = 5
    x = 3
    d_x = -1
    d_y = 1
    length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)