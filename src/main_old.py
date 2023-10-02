#!/usr/bin/env python

import numpy as np
from flask import Flask, request, jsonify, render_template
from src.ticTacToe_old import Player

# Create the application.
APP = Flask(__name__)

player = Player('computer', exp_rate=0)
player.loadPolicy('policies/1000000.pickle')


@APP.route('/')
def index():
    return render_template('index.html')


@APP.route('/play')
def play():
    #row = int(request.args.get('row'))
    #column = int(request.args.get('col'))
    board = request.args.getlist('board')
    board = [float(x) for x in board]
    board = np.array(board)
    board = board.reshape(3, 3)
    ps = int(request.args.get('player'))

    print(f'board = {board}')
    print(f'Player Symbol = {ps}')
    #r, c = st.play_it(row, column)

    r, c = player.chooseAction(board, ps)
    return jsonify({'row':r, 'col':c})


if __name__ == '__main__':
    APP.debug=True
    APP.run()