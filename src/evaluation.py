import chess
import values


def _evaluate(board: chess.Board, color):

    # Get number of each piece
    pawns = board.pieces(chess.PAWN, color)
    knights = board.pieces(chess.KNIGHT, color)
    bishops = board.pieces(chess.BISHOP, color)
    rooks = board.pieces(chess.ROOK, color)
    queens = board.pieces(chess.QUEEN, color)
    kings = board.pieces(chess.KING, color)

    centipawn_material = 0

    pawn_count = len(pawns)
    knight_count = len(knights)
    bishop_count = len(bishops)
    rook_count = len(rooks)
    queen_count = len(queens)
    king_count = len(kings)

    # Add up material value
    centipawn_material += pawn_count * 100
    centipawn_material += knight_count * 320
    centipawn_material += bishop_count * 330
    centipawn_material += rook_count * 500
    centipawn_material += queen_count * 900
    centipawn_material += king_count * 20000

    centipawns = centipawn_material

    # Apply piece-position modifiers
    if color == chess.WHITE:
        for pawn in pawns:
            centipawns += values.knight_table[63 - pawn]

        for knight in knights:
            centipawns += values.knight_table[63 - knight]

        for bishop in bishops:
            centipawns += values.bishop_table[63 - bishop]

        for rook in rooks:
            centipawns += values.rook_table[63 - rook]

        for queen in queens:
            centipawns += values.queen_table[63 - queen]

        for king in kings:
            centipawns += values.king_table[63 - king]

    if color == chess.BLACK:
        for pawn in pawns:
            centipawns += values.knight_table[pawn]

        for knight in knights:
            centipawns += values.knight_table[knight]

        for bishop in bishops:
            centipawns += values.bishop_table[bishop]

        for rook in rooks:
            centipawns += values.rook_table[rook]

        for queen in queens:
            centipawns += values.queen_table[queen]

        for king in kings:
            centipawns += values.king_table[king]

    return centipawns


def evaluate(board: chess.Board):

    # Check for win, loss, and draw. Return evaluation accordingly
    if board.outcome():
        if not board.outcome().winner:
            return 0
        elif board.outcome().winner == chess.WHITE:
            return 1000000
        else:
            return -1000000

    return _evaluate(board, chess.WHITE) - _evaluate(board, chess.BLACK)
