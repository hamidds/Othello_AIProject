# Some constants for the game
from copy import deepcopy
import time
import random

MIN_VALUE = -100000
MAX_VALUE = 100000

BLACK = 'B'  # indicates the black player bead
WHITE = 'W'  # indicates the white player bead
NONE = '-'  # empty

SQUARE_WEIGHTS = [

    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120]

    # 120 = 4
    # 20  = 8
    # 15  = 4
    # 5   = 8
    # 3   = 10
    # -5  = 16
    
    # -20 = 8
    # -40 = 4

]


class OthelloGame:

    def __init__(self, rows: int, cols: int, turn: str, winner_color=None, black_score=0, white_score=0,
                 black_weights=None, white_weights=None, first_player=BLACK):
        ''' Initialize all of the games settings and creates the board. '''
        if black_weights is None:
            black_weights = SQUARE_WEIGHTS
        if white_weights is None:
            white_weights = SQUARE_WEIGHTS
        self.black_weights = black_weights
        self.white_weights = white_weights
        self.winner_color = winner_color
        self.black_score = black_score
        self.white_score = white_score
        self.first_player = first_player
        # upper part is for phase 3
        self.rows = rows
        self.cols = cols
        self.turn = turn
        self.current_board = self.new_game_board(rows, cols)

    def new_game_board(self, rows: int, cols: int) -> [[str]]:
        ''' Creates the Othello Game board with specified dimensions. '''
        board = []

        # Create an empty board
        for row in range(rows):
            board.append([])
            for col in range(cols):
                board[-1].append(NONE)

        # Initialize the 4 game pieces in the center
        # W B
        # B W
        board[rows // 2 - 1][cols // 2 - 1] = WHITE
        board[rows // 2 - 1][cols // 2] = BLACK
        board[rows // 2][cols // 2 - 1] = BLACK
        board[rows // 2][cols // 2] = WHITE

        return board

    def set_game_board(self, new_board):
        self.current_board = new_board

    def set_winner(self, winner, score):
        self.winner = winner
        self.winner_score = score

    def opposite_turn(self, turn: str) -> str:
        ''' Returns the player of the opposite player '''
        return {BLACK: WHITE, WHITE: BLACK}[turn]

    def move(self, row: int, col: int, real=True, ai_vs_ai=False):
        self.require_valid_empty_space_to_move(row, col)
        # it throws exception when the user selects an invalid cell
        possible_directions = self.adjacent_opposite_color_directions(row, col, self.turn)

        next_turn = self.turn
        for direction in possible_directions:
            if self.is_valid_directional_move(row, col, direction[0], direction[1], self.turn):
                next_turn = self.opposite_turn(self.turn)
                self.convert_adjacent_cells_in_direction(row, col, direction[0], direction[1], self.turn)

        if next_turn != self.turn:
            self.current_board[row][col] = self.turn
            if self.can_move(next_turn):
                self.turn = self.opposite_turn(self.turn)  # switches the turn
                # if self.turn == WHITE and real:
                if self.turn == self.opposite_turn(self.first_player) and real:
                    start_time = time.time()
                    row, col = self.get_minimax_move_alpha(self.turn, start_time)
                    self.move(row, col)



        else:
            raise InvalidMoveException()

    def require_valid_empty_space_to_move(self, row: int, col: int) -> bool:
        ''' In order to move, the specified cell space must be within board boundaries
            AND the cell has to be empty '''

        if self.is_valid_cell(row, col) and self.cell_color(row, col) != NONE:
            raise InvalidMoveException()

    def cell_color(self, row: int, col: int) -> str:
        ''' Returns the color of the specified cell '''
        return self.current_board[row][col]

    def is_valid_cell(self, row: int, col: int) -> bool:
        ''' Returns True if the given cell move position is invalid due to
            position (out of bounds) '''
        return 0 <= row < self.rows and 0 <= col < self.cols

    def flip_cell(self, row: int, col: int) -> None:
        ''' Flips the specified cell over to the other color '''
        self.current_board[row][col] = self.opposite_turn(self.current_board[row][col])

    def adjacent_opposite_color_directions(self, row: int, col: int, turn: str) -> [tuple]:
        ''' Looks up to a possible of 8 directions surrounding the given move. If any of the
            move's surrounding cells is the opposite color of the move itself, then record
            the direction it is in and store it in a list of tuples [(row_dir, col_dir)].
            Return the list of the directions at the end. '''
        dir_list = []
        for row_dir in range(-1, 2):
            for col_dir in range(-1, 2):
                if self.is_valid_cell(row + row_dir, col + col_dir):
                    if self.current_board[row + row_dir][col + col_dir] == self.opposite_turn(turn):
                        dir_list.append((row_dir, col_dir))
        return dir_list

    def is_valid_directional_move(self, row: int, col: int, row_dir: int, col_dir: int, turn: str) -> bool:
        ''' Given a move at specified row/col, checks in the given direction to see if
            a valid move can be made. Returns True if it can; False otherwise.
            Only supposed to be used in conjunction with _adjacent_opposite_color_directions()'''
        current_row = row + row_dir
        current_col = col + col_dir

        last_cell_color = self.opposite_turn(turn)

        while True:

            if not self.is_valid_cell(current_row, current_col):  # if the current cell is not in the game board
                break
            if self.cell_color(current_row, current_col) == NONE:  # if the current cell's color is empty
                break
            if self.cell_color(current_row,
                               current_col) == turn:  # if the current cell's color is the same with turn color
                last_cell_color = turn
                break

            current_row += row_dir
            current_col += col_dir

        return last_cell_color == turn

    def convert_adjacent_cells_in_direction(self, row: int, col: int, row_dir: int, col_dir: int, turn: str) -> None:
        ''' If it can, converts all the adjacent/contiguous cells on a turn in
            a given direction until it finally reaches the specified cell's original color '''
        current_row = row + row_dir
        current_col = col + col_dir

        while self.cell_color(current_row, current_col) == self.opposite_turn(turn):
            self.flip_cell(current_row, current_col)
            current_row += row_dir
            current_col += col_dir

    def can_move(self, turn: str) -> bool:
        ''' Looks at all the empty cells in the board and checks to
            see if the specified player can move in any of the cells.
            Returns True if it can move; False otherwise. '''
        for row in range(self.rows):
            for col in range(self.cols):
                if self.current_board[row][col] == NONE:
                    possible_directions = self.adjacent_opposite_color_directions(row, col, turn)
                    for direction in possible_directions:
                        if self.is_valid_directional_move(row, col, direction[0], direction[1], turn):
                            return True
        return False

    def is_game_over(self) -> bool:
        ''' Looks through every empty cell and determines if there are
            any valid moves left. If not, returns True; otherwise returns False '''
        return not self.can_move(BLACK) and not self.can_move(WHITE)

    def winner(self) -> str:
        ''' Returns the winner. ONLY to be called once the game is over.
            Returns None if the game is a TIE game.'''
        black_cells = self.get_total_cells(BLACK)
        self.black_score = black_cells
        white_cells = self.get_total_cells(WHITE)
        self.white_score = white_cells
        if black_cells == white_cells:
            return None

        if black_cells > white_cells:
            return BLACK
        else:
            return WHITE

    def get_total_cells(self, turn: str) -> int:
        ''' Returns the total cell count of the specified colored player '''
        total = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.current_board[row][col] == turn:
                    total += 1
        return total

    # minimax section
    def get_cells_with_color(self, turn: str):
        ''' Returns a list that contains the total cells of the specified colored player '''
        cells = []
        for row in range(self.rows):
            for col in range(self.cols):
                # print(str((row, col)) + " color = " + str(self.cell_color(row, col)))
                if self.current_board[row][col] == turn:
                    # print((row, col))
                    cells.append((row, col))
        return cells

    def utility_function(self, turn):
        ''' Returns the current score based on the weight of a cell and its color '''
        our_cells = self.get_cells_with_color(turn)
        our_cells_value = 0
        opponent_cells = self.get_cells_with_color(self.opposite_turn(turn))
        opponent_cells_value = 0

        for cell in our_cells:
            if turn == BLACK:
                our_cells_value += self.black_weights[cell[0]][cell[1]]
            else:
                our_cells_value += self.white_weights[cell[0]][cell[1]]

        for cell in opponent_cells:
            if self.opposite_turn(turn) == BLACK:
                our_cells_value += self.black_weights[cell[0]][cell[1]]
            else:
                our_cells_value += self.white_weights[cell[0]][cell[1]]

        return our_cells_value - opponent_cells_value

    def is_valid_move(self, row: int, col: int, row_dir: int, col_dir: int, turn: str):
        ''' Returns a cell that is a correct move for a given color '''
        current_row = row + row_dir
        current_col = col + col_dir
        last_cell_color = self.opposite_turn(turn)

        number_of_opposite_beads = 0

        move = (-1, -1)
        while True:

            if not self.is_valid_cell(current_row, current_col):  # if the current cell is not in the game board
                break
            if self.cell_color(current_row, current_col) == NONE:  # if the current cell's color is empty
                last_cell_color = turn
                move = (current_row, current_col)
                break
            if self.cell_color(current_row,
                               current_col) == turn:  # if the current cell's color is the same with turn color
                break
            if self.cell_color(current_row,
                               current_col) == last_cell_color:
                number_of_opposite_beads += 1

            current_row += row_dir
            current_col += col_dir

        valid = last_cell_color == turn and number_of_opposite_beads > 0
        if valid:
            return move
        return None

    def get_priority(self, row, col, turn):
        ''' Returns the priority of the given cell '''
        if turn == BLACK:
            value = self.black_weights[row][col]
        else:
            value = self.white_weights[row][col]
        if 70 <= value <= 120:
            return 0
        if 20 <= value < 70:
            return 1
        if 15 <= value < 20:
            return 2
        if 5 <= value < 15:
            return 3
        if 0 <= value < 5:
            return 4
        # if -21 <= value <= -1:
        #     return 5
        # if -40 <= value < -21:
        #     return 6
        # if -150 <= value <= -40:
        #     return 7
        if -19 <= value <= -1:
            return 5
        if -39 <= value < -19:
            return 6
        if -100 <= value <= -40:
            return 7

        # switcher = {
        #     120: 0,
        #     20: 1,
        #     15: 2,
        #     5: 3,
        #     3: 4,
        #     - 5: 5,
        #     - 20: 6,
        #     - 40: 7
        # }
        # return switcher.get(value)
        # return (row, col) == (0, 0) or (row, col) == (0, 7) or (row, col) == (7, 0) or (row, col) == (7, 7)

    def get_possible_moves(self, turn):
        ''' Returns a set of all possible moves so that minimax can iterate over them and find the best '''
        possible_cells = self.get_cells_with_color(turn)
        possible_moves_1 = set()
        possible_moves_2 = set()
        possible_moves_3 = set()
        possible_moves_4 = set()
        possible_moves_5 = set()
        possible_moves_6 = set()
        possible_moves_7 = set()
        possible_moves_8 = set()
        all_possible_moves = set()
        possible_moves = [possible_moves_1, possible_moves_2, possible_moves_3, possible_moves_4,
                          possible_moves_5, possible_moves_6, possible_moves_7, possible_moves_8]

        for cell in possible_cells:
            # print(cell)
            possible_directions = self.adjacent_opposite_color_directions(cell[0], cell[1], turn)
            for direction in possible_directions:
                # print(str(cell) + "  " + str(direction))
                move = self.is_valid_move(cell[0], cell[1], direction[0], direction[1], turn)
                if move:
                    # print(move)
                    priority = self.get_priority(move[0], move[1], turn)
                    # print(priority)
                    possible_moves[priority].add(move)
                    all_possible_moves.add(move)

        result = set()
        for possible in possible_moves:
            if len(possible) > 0:
                result = possible
                break

        if 0 < len(all_possible_moves) and 0 < len(result) < 6:
            size1 = len(result)
            # print(size1)
            number_of_randoms = int((6 - size1) / 2)
            # print(number_of_randoms)
            # print(len(all_possible_moves))
            # print(result)
            # print(all_possible_moves)
            # all_possible_moves.difference(result)
            all_possible_moves.difference_update(result)
            # print(all_possible_moves)
            number_of_randoms = min(number_of_randoms, len(all_possible_moves))
            random_moves = random.sample(all_possible_moves, number_of_randoms)
            # print("Random Moves:")
            # print(random_moves)
            result.update(random_moves)
            # print(result)
        return list(result)

    def copy_game(self, turn):
        ''' Returns a copy of the current game for minimax '''
        new_board = deepcopy(self.current_board)
        new_game = OthelloGame(self.rows, self.cols, turn, black_weights=self.black_weights,
                               white_weights=self.white_weights)
        new_game.set_game_board(new_board)

        return new_game

    def minimax_alpha_beta(self, turn, depth, alpha, beta, start_time):
        # print("Turn = " + turn)

        time_expired = time.time() - start_time > 4.8
        if time_expired:
            # print("GAME OVER FOR TIME EXPIRED")
            return self.utility_function(turn), None

        if self.is_game_over():
            # print("GAME OVER FOR IS_GAME_OVER()")
            return self.utility_function(turn), None

        if depth <= 0:
            # print("GAME OVER FOR DEPTH")
            return self.utility_function(turn), None

        possible_moves = self.get_possible_moves(turn)
        # print("Depth = " + str(depth))

        if len(possible_moves) == 0:
            # print("GAME OVER FOR len(possible_moves) == 0")
            return self.utility_function(turn), None

        # print("POSSIBLE MOVES: ")
        if turn == BLACK:
            best_score = MIN_VALUE
            best_move = list(possible_moves)[0]
            for move in possible_moves:
                # print("possible move" + str(move))
                new_game = self.copy_game(turn)
                new_game.move(move[0], move[1], False)

                try_tuple = new_game.minimax_alpha_beta(self.opposite_turn(turn), depth - 1, alpha, beta, start_time)
                try_score = try_tuple[0]
                if try_score > best_score:
                    best_score = try_score
                    best_move = move
                alpha = max(best_score, alpha)
                if alpha >= beta:
                    # print("==============BETA CUTOFF==============")
                    # print("BETA = " + str(beta))
                    # print("ALPHA = " + str(alpha))
                    return best_score, best_move
        if turn == WHITE:
            best_score = MAX_VALUE
            best_move = list(possible_moves)[0]
            for move in possible_moves:
                # print("possible move" + str(move))
                new_game = self.copy_game(turn)
                new_game.move(move[0], move[1], False)

                try_tuple = new_game.minimax_alpha_beta(self.opposite_turn(turn), depth - 1, alpha, beta, start_time)
                try_score = try_tuple[0]
                if try_score < best_score:
                    best_score = try_score
                    best_move = move
                beta = min(best_score, beta)
                if alpha >= beta:
                    # print("==============ALPHA CUTOFF==============")
                    # print("BETA = " + str(beta))
                    # print("ALPHA = " + str(alpha))
                    return best_score, best_move

        return best_score, best_move

    def get_minimax_move_alpha(self, turn, start_time, test=False):
        ''' Returns the best move chosen by minimax function '''
        move = self.minimax_alpha_beta(turn, 5, MIN_VALUE, MAX_VALUE, start_time)[1]
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # print(self.turn)
        # print("CHOSEN MOVE = " + str(move))
        # end_time = time.time()
        # print("SEARCH TIME: " + str(end_time - start_time))
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        if move is None:
            return None, None
        return move

    def ai_vs_ai(self):
        while not self.is_game_over():
            start_time = time.time()
            row, col = self.get_minimax_move_alpha(self.first_player, start_time, test=True)
            if (row, col) == (None, None):
                break
            # print("===============================================================================")
            # print(row, col)
            # print("===============================================================================")
            self.move(row, col)
            # print("==================================MOVED========================================")
        self.winner_color = self.winner()
        # print(self.winner_color)
        # print(self.black_score)
        # print(self.white_score)
        if self.first_player == BLACK:
            return self.black_score, self.white_score
        return self.white_score, self.black_score

        # An Exception that is raised every time an invalid move occurs


class InvalidMoveException(Exception):
    ''' Raised whenever an exception arises from an invalid move '''
    pass
