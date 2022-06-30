from multiprocessing import Pool
import chess

from evaluation import evaluate


# Recursive implementation of minimax algorithm with alpha-beta pruning.
def minimax(board: chess.Board, depth, alpha, beta, color):

    if depth == 0 or board.outcome():
        return evaluate(board), None

    if color == chess.WHITE:
        max_eval = -2000000
        best_move = None
        for move in board.legal_moves:
            board.push(move)

            evaluation, _ = minimax(board, depth-1, alpha, beta, chess.BLACK)

            if evaluation > max_eval:
                max_eval = evaluation
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

            evaluation, _ = minimax(board, depth-1, alpha, beta, chess.WHITE)

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move

            board.pop()

            if min_eval <= alpha:
                break

            beta = min(beta, min_eval)

        return min_eval, best_move


def run_engine(board: chess.Board, depth, color, processes=1):

    # Use standard minimax if process == 1
    if processes == 1:
        evaluation, move, _ = minimax(board, depth, -1000000, 1000000, color)
        return evaluation, move

    if color == chess.WHITE:
        args = []
        for move in board.legal_moves:
            board.push(move)
            args.append((board.copy(), depth-1, -1000000, 1000000, chess.BLACK))
            board.pop()

        max_eval = -2000000
        best_move = None

        with Pool(processes=processes) as pool:
            for (evaluation, _), move in zip(pool.starmap(minimax, args), board.legal_moves):
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

        return max_eval, best_move

    if color == chess.BLACK:
        args = []
        moves = []
        for move in board.legal_moves:
            moves.append(move)
            board.push(move)
            args.append((board.copy(), depth-1, -1000000, 1000000, chess.WHITE))
            board.pop()

        min_eval = 2000000
        best_move = None

        with Pool(processes=processes) as pool:
            for (evaluation, _), move in zip(pool.starmap(minimax, args), moves):
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

        return min_eval, best_move
