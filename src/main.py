import time

from monitor import MainBoard


if __name__ == '__main__':

    board = MainBoard()

    try:
        while True:
            board.update()

            time.sleep(10)

    except KeyboardInterrupt:
        board.cleanup()
        print('\ninterrupt caught, exiting')

    except:
        board.cleanup()
        raise
