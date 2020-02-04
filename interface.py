import tty, sys

class Interface:

    def __init__(self, game):
        self.game = game

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
        if self.game.cursor_row > 0:
            self.game.cursor_row -= 1

    def move_cursor_down(self, ):
        if self.game.cursor_row < 2:
            self.game.cursor_row += 1

    def move_cursor_right(self, ):
        if self.game.cursor_column < 2:
            self.game.cursor_column += 1

    def move_cursor_left(self, ):
        if self.game.cursor_column > 0:
            self.game.cursor_column -= 1

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
            game_is_over = self.game.make_move()
            if game_is_over:
                tty.tcsetattr(sys.stdin, tty.TCSAFLUSH, mode)
                return False
            else:
                self.game.change_player()
        elif keypress is 'exit':
            tty.tcsetattr(sys.stdin, tty.TCSAFLUSH, mode)
            raise KeyboardInterrupt
        return True
