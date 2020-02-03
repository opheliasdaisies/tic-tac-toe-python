import tty, sys

class Game:

    def __init__(self):
        self.X = []
        self.O = []
        self.cursor = (0, 0)
        self.row = 0
        self.column = 0
        self.player = 'X'


    def get_space_value(self):
        if (self.row, self.column) in self.X:
            space = 'X'
        elif (self.row, self.column) in self.O:
            space = 'O'
        else:
            space = ' '
        # if row is self.cursor(0)
        return space

    def draw_board(self):
        # print(chr(27) + '[2J' + chr(27) + '[0;0H') # clears terminal
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

    def play(self):
        mode = tty.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        accepting_input = True

        self.draw_board()


def main():
    game = Game()
    game.play()

    # try:
    #     board.populate_board()
    #     while True:
    #         tick(board)
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     return

if __name__ == "__main__":
    main()
