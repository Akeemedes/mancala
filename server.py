# -*- coding: utf-8 -*-
"""
Flask Server for Mancala games
"""

import datetime
import os
from flask import Flask, jsonify
from flask import send_from_directory
from mancala.utility import split_string
from mancala.game import Game


FLASKAPP = Flask(__name__)
FLASKAPP.config.from_object(__name__)


@FLASKAPP.route('/')
def show():
    """Returns current time"""
    return jsonify({'current_time': datetime.datetime.utcnow().isoformat()})


@FLASKAPP.route('/play/<string:board>/<int:player_turn>/<int:move>')
def play_board(board, player_turn, move):
    """Make a move based on a player and a board"""
    board_arr = split_string(board, 2)

    if len(board_arr) != 14:
        return jsonify({"error": "Invalid Board"}), 400

    if player_turn != 1 and player_turn != 2:
        return jsonify({"error": "Invalid Player"}), 400

    if move < 0 or move > 13:
        return jsonify({"error": "Invalid move"}), 400

    game = Game(board_arr, player_turn)
    game.move(move)
    return jsonify({
        'board': game.board(),
        'player_turn': game.turn_player(),
        'score': game.score(),
        'game_over': game.over(),
        'current_time': datetime.datetime.utcnow().isoformat()
    })


@FLASKAPP.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    full_path = os.path.join(os.getcwd(), 'www')
    return send_from_directory(full_path, filename)

FLASKAPP.run()
