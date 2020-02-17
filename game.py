import tty, sys
import random
from interface import Interface

class Game:

    def __init__(self, players):
        self.X = []
        self.O = []
        self.possible_moves = [(0, 0), (0,1), (0,2), (1, 0), (1,1), (1,2), (2, 0), (2,1), (2,2)]
        self.cursor_row = 0
        self.cursor_column = 0
        self.player = 'X'
        self.has_winner = False
        self.ai = int(players) is 1

    CURSOR_BACKGROUND = '\u001b[42m'
    BACKGROUND_RESET = '\u001b[0m'
    BLINK = '\u001b[5m'
    STOP_BLINK = '\u001b[25m'

    WINNING_SETS = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def get_space_value(self, row, column):
        coordiantes = (row, column)
        if coordiantes in self.X:
            space = 'X'
        elif coordiantes in self.O:
            space = 'O'
        else:
            space = ' '
        if coordiantes == (self.cursor_row, self.cursor_column):
            space = f'{self.CURSOR_BACKGROUND}{space}{self.BACKGROUND_RESET}'
        return space

    def draw_board(self):
        row = 0
        column = 0
        print(chr(27) + '[2J' + chr(27) + '[0;0H') # clears terminal
        game_board = f'\n\rPlayer {self.player} Goes:\n\n\r'

        while row < 3:
            while column < 3:
                space = self.get_space_value(row, column)
                if column is 1:
                    game_board += f'|{space}|'
                else:
                    game_board += space
                column += 1
            if row < 2:
                game_board += '\r\n_____\n'
            game_board += '\r'
            row += 1
            column = 0
        
        print(game_board)
        row = 0
        column = 0

    def check_if_winner(self):
        moves_made_by_player = getattr(self, self.player)
        if len(moves_made_by_player) > 2:
            for winning_set in self.WINNING_SETS:
                if all(move in moves_made_by_player for move in winning_set):
                    self.has_winner = True
                    break

    def make_move(self):
        cursor_coordinates = (self.cursor_row, self.cursor_column)
        if cursor_coordinates in self.X or cursor_coordinates in self.O:
            return False # does not take move if spot has already been taken

        getattr(self, self.player).append(cursor_coordinates)
        self.possible_moves.remove(cursor_coordinates)

        self.check_if_winner()
        if self.has_winner or len(self.X) + len(self.O) is 9:
            return True

        if self.ai:
            self.change_player()
            self.ai_moves()
            self.check_if_winner()
            if self.has_winner or len(self.X) + len(self.O) is 9:
                return True

        self.change_player()
        return False

    def change_player(self):
        self.player = 'O' if self.player is 'X' else 'X'

    def ai_moves(self):
        move_index = random.randint(0, len(self.possible_moves) - 1)
        move = self.possible_moves[move_index]
        self.possible_moves.remove(move)
        self.O.append(move)

    def play_game(self):
        mode = tty.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        accepting_input = True
        self.draw_board()
        interface = Interface(self)

        while accepting_input:
            keypress = interface.read_keyboard_input()
            accepting_input = interface.handle_keypress(keypress, mode)            
            self.draw_board()

        if self.has_winner:
            print(f'\n{self.BLINK}PLAYER {self.player} WINS!{self.STOP_BLINK}\n\r')
        else:
            print('\nGAME ENDED IN A TIE.\n\r')
