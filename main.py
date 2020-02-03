import tty, sys

class Game:

    def __init__(self):
        self.X = []
        self.O = []
        self.cursor_row = 0
        self.cursor_column = 0
        self.player = 'X'
        self.has_winner = False

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

    def check_if_winner(self, last_move):
        checked_set = self.X if self.player is 'X' else self.O
        if len(checked_set) > 2:
            for winning_set in self.WINNING_SETS:
                if all(item in checked_set for item in winning_set):
                    self.has_winner = True

    def make_move(self):
        cursor_coordinates = (self.cursor_row, self.cursor_column)
        if cursor_coordinates not in self.X and cursor_coordinates not in self.O:
            if self.player is 'X':
                self.X.append(cursor_coordinates)
            elif self.player is 'O':
                self.O.append(cursor_coordinates)

        self.check_if_winner(cursor_coordinates)

        if self.has_winner or len(self.X) + len(self.O) is 9:
            return True

        return False

    def change_player(self):
        self.player = 'O' if self.player is 'X' else 'X'

    def process_keyboard_input(self):
        char = ord(sys.stdin.read(1)) # listen for arrow keys and get char code
        if char == 27: # Arrow keys process as a sequence of three characters
            next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
            if next1 == 91: # The second character in the arrow key sequence
                if next2 == 65:
                    return 'up'
                elif next2 == 66:
                    return 'down'
                elif next2 == 67:
                    return 'right'
                elif next2 == 68:
                    return 'left'
        elif char == 10 or char == 13 or char == 32:
            return 'select'
        elif char == 3: # CTRL-C
            return 'exit'

    def move_cursor_up(self):
        if self.cursor_row > 0:
            self.cursor_row -= 1

    def move_cursor_down(self):
        if self.cursor_row < 2:
            self.cursor_row += 1

    def move_cursor_right(self):
        if self.cursor_column < 2:
            self.cursor_column += 1

    def move_cursor_left(self):
        if self.cursor_column > 0:
            self.cursor_column -= 1

    def handle_keypress(self, keypress, mode):
        if keypress is 'up':
            self.move_cursor_up()
        elif keypress is 'down':
            self.move_cursor_down()
        elif keypress is 'right':
            self.move_cursor_right()
        elif keypress is 'left':
            self.move_cursor_left()
        elif keypress is 'select':
            game_is_over = self.make_move()
            if game_is_over:
                tty.tcsetattr(sys.stdin, tty.TCSAFLUSH, mode)
                return False
            else:
                self.change_player()
        elif keypress is 'exit':
            tty.tcsetattr(sys.stdin, tty.TCSAFLUSH, mode)
            raise KeyboardInterrupt
        return True

    def play(self):
        mode = tty.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        accepting_input = True
        self.draw_board()

        while accepting_input:
            keypress = self.process_keyboard_input()
            accepting_input = self.handle_keypress(keypress, mode)            
            self.draw_board()

        if self.has_winner:
            print(f'\n{self.BLINK}PLAYER {self.player} WINS!{self.STOP_BLINK}\n\r')
        else:
            print('\nGAME ENDED IN A TIE.\n\r')

def main():
    game = Game()

    try:
        game.play()

        while True:
            play_again = input('Do you want to play again? (Y/N)')
            if play_again.upper() == 'Y':
                game = Game()
                game.play()
            else:
                break
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
