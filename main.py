import tty, sys

class Game:

    def __init__(self):
        self.X = []
        self.O = []
        self.cursor = [0, 0]
        self.row = 0
        self.column = 0
        self.player = 'X'

    CURSOR_BACKGROUND = '\u001b[42m'
    BACKGROUND_RESET = '\u001b[0m'

    def get_space_value(self):
        if (self.row, self.column) in self.X:
            space = 'X'
        elif (self.row, self.column) in self.O:
            space = 'O'
        else:
            space = ' '
        if [self.row, self.column] == self.cursor:
            space = f'{self.CURSOR_BACKGROUND}{space}{self.BACKGROUND_RESET}'
        return space

    def draw_board(self):
        print(chr(27) + '[2J' + chr(27) + '[0;0H') # clears terminal
        game_board = f'\n\rPlayer {self.player} Goes:\n\n\r'

        while self.row < 3:
            while self.column < 3:
                space = self.get_space_value()
                if self.column is 1:
                    game_board += f'|{space}|'
                else:
                    game_board += space
                self.column += 1
            if self.row < 2:
                game_board += '\r\n_____\n'
            game_board += '\r'
            self.row += 1
            self.column = 0
        
        print(game_board)
        self.row = 0
        self.column = 0

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
        elif char == 32:
            return 'space'
        elif char == 10 or char == 13:
            return 'enter'
        elif char == 3: # CTRL-C
            return 'exit'

    def move_cursor_up(self):
        if self.cursor[0] > 0:
            self.cursor[0] -= 1

    def move_cursor_down(self):
        if self.cursor[0] < 2:
            self.cursor[0] += 1

    def move_cursor_right(self):
        if self.cursor[1] < 2:
            self.cursor[1] += 1

    def move_cursor_left(self):
        if self.cursor[1] > 0:
            self.cursor[1] -= 1

    def handle_keypress(self, keypress, mode):
        if keypress is 'up':
            self.move_cursor_up()
        elif keypress is 'down':
            self.move_cursor_down()
        elif keypress is 'right':
            self.move_cursor_right()
        elif keypress is 'left':
            self.move_cursor_left()
        elif keypress is 'enter':
            tty.tcsetattr(sys.stdin, tty.TCSAFLUSH, mode)
            raise KeyboardInterrupt
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
