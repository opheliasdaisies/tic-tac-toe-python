from game import Game

def main():

    try:
        players = input('How many players? (1 or 2) ')

        Game(players).play_game()

        while True:
            play_again = input('Do you want to play again? (Y/N) ')
            if play_again.upper() == 'Y':
                Game().play_game()
            else:
                break
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
