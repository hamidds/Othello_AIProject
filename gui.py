import othello
import models
import tkinter
import time
import time
from PIL import ImageTk, Image, ImageOps

# Game Settings
ROWS = 8
COLUMNS = 8
FIRST_PLAYER = othello.BLACK

# GUI Constants
BACKGROUND_COLOR = models.BACKGROUND_COLOR
BOARD_HEIGHT = 400
BOARD_WIDTH = 600


class HomeGUI:
    def __init__(self):
        # Home page
        self.window = tkinter.Tk()
        self.window.geometry('{}x{}'.format(BOARD_WIDTH, BOARD_HEIGHT))
        self.window.title('OTHELLO')
        self.window.configure(background=BACKGROUND_COLOR, width=BOARD_WIDTH, height=BOARD_HEIGHT)

        self.name = tkinter.Label(master=self.window,
                                  text='OTHELLO',
                                  font=('Comic Sans MS', 50),
                                  background=BACKGROUND_COLOR,
                                  fg='white')
        self.wallpaper_img = Image.open("assets/wallpaper.png")
        self.wallpaper_img = self.wallpaper_img.resize((BOARD_WIDTH, int(BOARD_HEIGHT / 2 + 10)), Image.ANTIALIAS)
        self.wallpaper_img = ImageTk.PhotoImage(self.wallpaper_img)
        self.wallpaper = tkinter.Label(master=self.window,
                                       image=self.wallpaper_img,
                                       width=BOARD_WIDTH,
                                       height=BOARD_HEIGHT / 2,
                                       border=20,
                                       background=BACKGROUND_COLOR)
        self.new_game_label = tkinter.Label(master=self.window,
                                            text='New Game',
                                            font=models.FONT,
                                            background=BACKGROUND_COLOR,
                                            fg='white',
                                            cursor="hand2")
        self.exit_label = tkinter.Label(master=self.window,
                                        text='Exit',
                                        font=models.FONT,
                                        background=BACKGROUND_COLOR,
                                        fg='black',
                                        cursor="hand2")

        # Bind my home page with these two events.
        self.new_game_label.bind('<Button-1>', self.new_game_button_clicked)
        self.exit_label.bind('<Button-1>', self.exit_button_clicked)

        # Layout all the widgets here using grid layout
        self.name.grid(row=0, column=0, sticky=tkinter.E + tkinter.S + tkinter.W, pady=0)
        self.wallpaper.grid(row=1, column=0, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W, pady=0)
        self.new_game_label.grid(row=2, column=0, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W, pady=0)
        self.exit_label.grid(row=3, column=0, sticky=tkinter.N + tkinter.E + tkinter.W, pady=10)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)

    def start(self) -> None:
        ''' Runs the mainloop of the window '''
        self.window.mainloop()

    def exit_button_clicked(self, event: tkinter.Event) -> None:
        ''' Exit the game'''
        self.window.destroy()

    def new_game_button_clicked(self, event: tkinter.Event) -> None:
        ''' Restart the game'''
        self.window.destroy()
        GameGUI().start()

    def on_window_resized(self, event: tkinter.Event) -> None:
        ''' Resize the window'''
        self.window.destroy()


class GameGUI:

    def __init__(self):
        # Game settings
        self.rows = ROWS
        self.columns = COLUMNS
        self.first_player = FIRST_PLAYER

        self.game = othello.OthelloGame(self.rows, self.columns, self.first_player)

        # Board game setting
        self.window = tkinter.Tk()
        self.window.title('OTHELLO')
        self.window.configure(background=BACKGROUND_COLOR)
        self.board = models.GameBoard(self.game, BOARD_WIDTH, BOARD_HEIGHT, self.window)
        self.black_score = models.Score(othello.BLACK, self.game, self.window)
        self.white_score = models.Score(othello.WHITE, self.game, self.window)
        self.player_turn = models.Turn(self.game, self.window)

        # Bind my game board with these two events.
        self.board.board.bind('<Configure>', self.on_board_resized)
        self.board.board.bind('<Button-1>', self.on_board_clicked)

        # restart button
        self.restart_icon = Image.open("assets/restart.jpg")
        self.restart_icon = ImageOps.fit(self.restart_icon, (40, 40))
        self.restart_icon = ImageTk.PhotoImage(self.restart_icon)
        self.restart_button = tkinter.Label(master=self.window,
                                            image=self.restart_icon,
                                            cursor="hand2",
                                            bg=BACKGROUND_COLOR)
        self.restart_button.bind('<Button-1>', self.restart_button_clicked)

        # exit button
        self.exit_icon = Image.open("assets/home.jpg")
        self.exit_icon = ImageOps.fit(self.exit_icon, (40, 40))
        self.exit_icon = ImageTk.PhotoImage(self.exit_icon)
        self.exit_button = tkinter.Label(master=self.window,
                                         image=self.exit_icon,
                                         cursor="hand2",
                                         bg=BACKGROUND_COLOR)
        self.exit_button.bind('<Button-1>', self.exit_button_clicked)

        # Layout all the widgets here using grid layout
        self.board.board.grid(row=0, column=0, columnspan=2, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)
        self.black_score.score_label.grid(row=1, column=0, pady=20, sticky=tkinter.N)
        self.white_score.score_label.grid(row=1, column=1, pady=20, sticky=tkinter.N)
        self.player_turn.turn_label.grid(row=2, column=0, columnspan=2, padx=10, pady=20)
        self.restart_button.grid(row=3, column=0, pady=10, sticky=tkinter.E, padx=10)
        self.exit_button.grid(row=3, column=1, pady=10, sticky=tkinter.W, padx=10)

        # Configure the root window's row/column weight (from the grid layout)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

    def start(self) -> None:
        ''' Runs the mainloop of the window '''
        self.window.mainloop()

    def new_game(self) -> None:
        ''' Creates a new game'''
        self.game = othello.OthelloGame(self.rows, self.columns, self.first_player)
        self.board.new_game_settings(self.game)
        self.board.redraw_board()
        self.black_score.update_score(self.game)
        self.white_score.update_score(self.game)
        self.player_turn.update_turn(self.game.turn)

    def exit_button_clicked(self, event: tkinter.Event) -> None:
        ''' Exit the game'''
        self.window.destroy()
        HomeGUI().start()

    def restart_button_clicked(self, event: tkinter.Event) -> None:
        ''' Restart the game'''
        self.new_game()


    def on_board_clicked(self, event: tkinter.Event) -> None:
        ''' Attempt to play a move on the board if it's valid '''

        pointx = event.x
        pointy = event.y
        row = int(pointy // self.board.get_cell_height())
        if row == self.board.rows:
            row -= 1
        col = int(pointx // self.board.get_cell_width())
        if col == self.board.cols:
            col -= 1

        try:
            self.game.move(row, col)
            self.update_board()

            if self.game.is_game_over():
                self.player_turn.display_winner(self.game.winner())
            else:
                self.player_turn.switch_turn(self.game)
        except:
            pass

    def update_board(self):
        self.board.update_game_state(self.game)
        self.board.redraw_board()
        self.black_score.update_score(self.game)
        self.white_score.update_score(self.game)

    def next_move(self):
        start_time = time.time()
        row, col = self.game.get_minimax_move_alpha(self.game.turn, start_time)
        self.game.move(row, col)

    def on_board_resized(self, event: tkinter.Event) -> None:
        ''' Called whenever the window is resized '''
        self.board.redraw_board()

    def on_restart_button_clicked(self, event: tkinter.Event) -> None:
        ''' Called whenever the restart button is clicked '''


if __name__ == '__main__':
    HomeGUI().start()
