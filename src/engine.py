import chess
import concurrent.futures

from src.evaluation import evaluate


# Recursive implementation of minimax algorithm with alpha-beta pruning. prev_move used only for multiprocess execution
def minimax(board: chess.Board, depth, alpha, beta, color, prev_move=None):

    if depth == 0 or board.outcome():
        return evaluate(board), None, prev_move

    if color == chess.WHITE:
        max_eval = -2000000
        best_move = None
        for move in board.legal_moves:
            board.push(move)

            evaluation, _, _ = minimax(board, depth-1, alpha, beta, chess.BLACK, prev_move)

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

            board.pop()

            if max_eval >= beta:
                break

            alpha = max(alpha, max_eval)

        return max_eval, best_move, prev_move

    if color == chess.BLACK:
        min_eval = 2000000
        best_move = None
        for move in board.legal_moves:
            board.push(move)

            evaluation, _, _ = minimax(board, depth-1, alpha, beta, chess.WHITE, prev_move)

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move

            board.pop()

            if min_eval <= alpha:
                break

            beta = min(beta, min_eval)

        return min_eval, best_move, prev_move


def run_engine(board: chess.Board, depth, color, processes=1):

    # Use standard minimax if process == 1
    if processes == 1:
        evaluation, move, _ = minimax(board, depth, -1000000, 1000000, color)
        return evaluation, move

    if color == chess.WHITE:
        with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
            results = []
            for move in board.legal_moves:
                board.push(move)
                results.append(executor.submit(minimax, board.copy(), depth-1, -1000000, 1000000, chess.BLACK, move))
                board.pop()

            max_eval = -2000000
            best_move = None

            for r in concurrent.futures.as_completed(results):
                evaluation, _, move = r.result()

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

            return max_eval, best_move

    if color == chess.BLACK:
        with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
            results = []
            for move in board.legal_moves:
                board.push(move)
                results.append(executor.submit(minimax, board.copy(), depth-1, -1000000, 1000000, chess.WHITE, move))
                board.pop()

            min_eval = 2000000
            best_move = None

            for r in concurrent.futures.as_completed(results):
                evaluation, _, move = r.result()

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

            return min_eval, best_move
