#!/bin/python

import chess
from chess import Board, Move
from random import random, choice
import os

def uci():
    board = Board()
    while True:
        command = input()
        if command.startswith('uci'):
            print('id name Dumb')
            print('id author William')
            print('uciok')
        elif command.startswith('setoption'):
            pass
        elif command.startswith('isready'):
            print('readyok')
        elif command.startswith('ucinewgame'):
            pass
        elif command.startswith('quit'):
            break
        elif command.startswith('position'):
            for word in command.split(' '):
                if word == 'position':
                    pass
                elif word == 'startpos':
                    board = Board()
                elif word == 'moves':
                    pass
                else:
                    board.push_uci(word)
        elif command.startswith('go'):
            move = generate_move(board)
            print('bestmove {}'.format(move.uci()))


# transposition_table = {}
positions_checked = 0
def generate_move(board: Board) -> chess.Move:
    global positions_checked
    # global transposition_table

    positions_checked = 0
    # transposition_table = {}
    score, move = minimax_fast(board, 5, -99, 99, board.turn == chess.WHITE)
    print('info nodes {}'.format(positions_checked))
    print('info score {}'.format(score))
    print('=========== DEBUG ===========')
    print('positions checked:\t{}'.format(positions_checked))
    print('current evaluation:\t{}'.format(evaluation(board)))
    print('move made:\t\t{}'.format(move))
    print('score of move:\t{}'.format(score))
    print('=========== DEBUG ===========')
    return move

def minimax_fast(board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> (int, chess.Move):
    global positions_checked

    if depth == 0:
        return (evaluation(board), None)
    if maximizing:
        value = -99
        best_move = None
        for move in board.legal_moves:
            positions_checked += 1
            board.push(move)
            new_value, _ = minimax_fast(board, depth - 1, alpha, beta, False)
            board.pop()
            if new_value > value:
                best_move = move
                value = new_value
            alpha = max(alpha, value)
            if beta <= alpha:
                return (alpha, None)
        return (value, best_move)
    else:
        value = 99
        best_move = None
        for move in board.legal_moves:
            positions_checked += 1
            board.push(move)
            new_value, _ = minimax_fast(board, depth - 1, alpha, beta, True)
            board.pop()
            if new_value < value:
                best_move = move
                value = new_value
            beta = min(beta, value)
            if beta <= alpha:
                return (beta, None)
        return (value, best_move)

def minimax_random(board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> (int, chess.Move):
    global positions_checked

    fen = board.fen()
    # if fen in transposition_table:
        # return transposition_table[fen]

    if depth == 0:
        return (evaluation(board), None)
    if maximizing:
        value = -99
        best_moves = []
        for move in board.legal_moves:
            positions_checked += 1
            board.push(move)
            new_value, _ = minimax_random(board, depth - 1, alpha, beta, False)
            board.pop()
            if new_value == value:
                best_moves.append(move)
            elif new_value > value:
                best_moves.clear()
                best_moves.append(move)
                value = new_value
            alpha = max(alpha, value)
            if beta < alpha:
                return (alpha, None)
        if len(best_moves) == 0:
            return (value, None)
        move = choice(best_moves)
        # transposition_table[fen] = (value, move)
        return (value, move)
    else:
        value = 99
        best_moves = []
        for move in board.legal_moves:
            positions_checked += 1
            board.push(move)
            new_value, _ = minimax_random(board, depth - 1, alpha, beta, True)
            board.pop()
            if new_value == value:
                best_moves.append(move)
            elif new_value < value:
                best_moves.clear()
                best_moves.append(move)
                value = new_value
            beta = min(beta, value)
            if beta < alpha:
                return (beta, None)
        if len(best_moves) == 0:
            return (value, None)
        move = choice(best_moves)
        # transposition_table[fen] = (value, move)
        return (value, move)

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 99,
}
def evaluation(board: Board) -> int:
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99
        else:
            return 99
    total = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.BLACK:
                val *= -1
            total += val
    return total

def main():
    uci()

if __name__ == '__main__':
    main()
