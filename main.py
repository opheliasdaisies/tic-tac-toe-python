import tty, sys

class Game:

    def __init__(self):
        self.X = []
        self.O = []
        self.cursor_row = 0
        self.cursor_column = 0
        self.player = 'X'

    CURSOR_BACKGROUND = '\u001b[42m'
    BACKGROUND_RESET = '\u001b[0m'

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

    def make_move(self):
        cursor_coordinates = (self.cursor_row, self.cursor_column)
        if cursor_coordinates not in self.X and cursor_coordinates not in self.O:
            if self.player is 'X':
                self.X.append(cursor_coordinates)
                self.player = 'O'
            elif self.player is 'O':
                self.O.append(cursor_coordinates)
                self.player = 'X'

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
            self.make_move()
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


def main():
    game = Game()

    try:
        game.play()
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
