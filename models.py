import othello
import tkinter


# GUI constants
BACKGROUND_COLOR = '#8EAF83'
GAME_COLOR = '#1a8014'
FONT = ('Comic Sans MS', 30)
PLAYERS = {othello.BLACK: 'Black', othello.WHITE: 'White'}


class GameBoard:
    def __init__(self, game: othello.OthelloGame, game_width: float, game_height: float, window) -> None:
        # Initialize the game board's settings here
        self.game = game
        self.rows = self.game.rows
        self.cols = self.game.cols
        self.board = tkinter.Canvas(master=window, width=game_width, height=game_height,  background=GAME_COLOR, cursor="hand2")

    def new_game_settings(self, game) -> None:
        ''' The game board's new game settings is now changed accordingly to
            the specified game state '''
        self.game = game
        self.rows = self.game.rows
        self.cols = self.game.cols

    def redraw_board(self) -> None:
        ''' Redraws the board '''
        self.board.delete(tkinter.ALL)
        row_multiplier = float(self.board.winfo_height()) / self.rows
        col_multiplier = float(self.board.winfo_width()) / self.cols

        # Draw the horizontal lines
        for row in range(1, self.rows):
            self.board.create_line(0, row * row_multiplier, float(self.board.winfo_width()), row * row_multiplier)

        # Draw the column lines
        for col in range(1, self.cols):
            self.board.create_line(col * col_multiplier, 0, col * col_multiplier, float(self.board.winfo_height()))

        for row in range(self.rows):
            for col in range(self.cols):
                if self.game.current_board[row][col] != othello.NONE:
                    self.draw_cell(row, col)

    def draw_cell(self, row: int, col: int) -> None:
        ''' Draws the specified cell '''
        self.board.create_oval(col * self.get_cell_width() + 5,
                               row * self.get_cell_height() + 5,
                               (col + 1) * self.get_cell_width() - 5,
                               (row + 1) * self.get_cell_height() - 5,
                               fill=PLAYERS[self.game.current_board[row][col]])

    def update_game_state(self, game: othello.OthelloGame) -> None:
        ''' Updates our current _game_state to the specified one in the argument '''
        self.game = game

    def get_cell_width(self) -> float:
        ''' Returns a game cell's width '''
        return float(self.board.winfo_width()) / self.cols

    def get_cell_height(self) -> float:
        ''' Returns a game cell's height '''
        return float(self.board.winfo_height()) / self.rows

class Score:
    def __init__(self, color: str, game: othello.OthelloGame, window) -> None:
        ''' Initializes the score label '''
        self.player = color
        self.score = game.get_total_cells(self.player)
        self.score_label = tkinter.Label(master=window,
                                          text=self.score_text(),
                                          background=BACKGROUND_COLOR,
                                          fg=PLAYERS[color],    #text color
                                          font=FONT)

    def update_score(self, game: othello.OthelloGame) -> None:
        ''' Updates the score with the specified game state '''
        self.score = game.get_total_cells(self.player)
        self.score_label['text'] = self.score_text()          #change score text

    def score_text(self) -> str:
        ''' Returns the score in text string format '''
        return PLAYERS[self.player] + ' : ' + str(self.score)


class Turn:
    def __init__(self, game: othello.OthelloGame, window) -> None:
        ''' Initializes the player's turn Label '''
        self.player = game.turn
        self.turn_label = tkinter.Label(master=window,
                                         text=self.turn_text(),
                                         background=BACKGROUND_COLOR,
                                         fg=PLAYERS[self.player],
                                         font=FONT)

    def display_winner(self, winner: str) -> None:
        ''' Only called when the game is over. Displays the game winner '''
        if winner == None:
            victory_text = 'Nobody wins :)'
            text_color = 'BLACK'
        else:
            victory_text = PLAYERS[winner] + ' player wins!'
            text_color = PLAYERS[winner]
        self.turn_label['text'] = victory_text
        self.turn_label['fg'] = text_color

    def switch_turn(self, game: othello.OthelloGame) -> None:
        ''' Switch's the turn between the players '''
        self.player = game.turn
        self.change_turn_text()

    def change_turn_text(self) -> None:
        ''' Changes the turn label's text '''
        self.turn_label['text'] = self.turn_text()
        self.turn_label['fg'] = PLAYERS[self.player]


    def update_turn(self, turn: str) -> None:
        ''' Updates the turn to whatever the current game state's turn is '''
        self.player = turn
        self.change_turn_text()

    def turn_text(self) -> str:
        ''' Returns the turn in text/string form '''
        return PLAYERS[self.player] + " player's turn"

    def opposite_turn(self) -> None:
        ''' Returns the opposite turn of current turn '''
        return {othello.BLACK: othello.WHITE, othello.WHITE: othello.BLACK}[self.player]

