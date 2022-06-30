import chess
from engine import run_engine

ENGINE_DEPTH = 5
MAX_PROCESSES = 4

START_FEN = ''
HUMAN_COLOR = chess.WHITE


def play(board: chess.Board, color, depth):

    if color == chess.BLACK:
        _, move = run_engine(board, depth, chess.WHITE, MAX_PROCESSES)

        print(move)
        board.push(move)

    optimize_color = chess.BLACK if color == chess.WHITE else chess.WHITE

    while not board.outcome():
        try:
            board.push_san(input('Input move: '))
        except (ValueError, AssertionError):
            print('Move not legal')
            continue

        if board.outcome():
            break

        _, move = run_engine(board, depth, optimize_color, MAX_PROCESSES)

        print(move)
        board.push(move)


if __name__ == '__main__':
    if START_FEN:
        board = chess.Board(START_FEN)
    else:
        board = chess.Board()

    play(board, HUMAN_COLOR, ENGINE_DEPTH)
