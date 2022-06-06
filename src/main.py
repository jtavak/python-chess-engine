import chess
from src.evaluation import evaluate


def minimax(board: chess.Board, depth, alpha, beta, color):
    if depth == 0 or board.is_checkmate():
        return evaluate(board), None

    if color == chess.WHITE:
        max_eval = -2000000
        best_move = None
        for move in board.legal_moves:
            board.push(move)

            eval, _ = minimax(board, depth-1, alpha, beta, chess.BLACK)

            if eval > max_eval:
                max_eval = eval
                best_move = move

            board.pop()

            if max_eval >= beta:
                break

            alpha = max(alpha, max_eval)

        return max_eval, best_move

    if color == chess.BLACK:
        min_eval = 2000000
        best_move = None
        for move in board.legal_moves:
            board.push(move)

            eval, _ = minimax(board, depth-1, alpha, beta, chess.WHITE)

            if eval < min_eval:
                min_eval = eval
                best_move = move

            board.pop()

            if min_eval <= alpha:
                break

            beta = min(beta, min_eval)

        return min_eval, best_move


def play(board: chess.Board, color):

    if color == chess.BLACK:
        _, move = minimax(board, 4, -2000000, 2000000, chess.WHITE)

        print(move)
        board.push(move)

    optimize_color = chess.BLACK if color == chess.WHITE else chess.WHITE

    while not board.is_checkmate():
        try:
            board.push_san(input('Input move: '))
        except (ValueError, AssertionError):
            print('Move not legal')
            continue

        _, move = minimax(board, 4, -2000000, 2000000, optimize_color)

        print(move)
        board.push(move)


board = chess.Board()
play(board, chess.WHITE)
