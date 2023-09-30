#!/usr/bin/env python

import json
import logging
import numpy as np
import src.nn as nn
from src.train import NNAgent
from flask import Flask, request, jsonify, render_template
#from ticTacToe import Player


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def load_data(path:str) -> tuple:
    '''
    Load a json encoded model.

    Args:
        path(str): the location of the model
    
    Returns:
        tuple: model definition and parameters
    '''
    with open(path, 'rb') as f:
        data = json.load(f)
        return data['model'], np.asarray(data['parameters'])


# Create the application.
APP = Flask(__name__)
#APP.logger.setLevel(logging.ERROR)

model_description, parameters = load_data('policies/model_mlp_1000.json')
model = nn.NN(model_description)
model.update(parameters)
player = NNAgent(model)
#player.loadPolicy('policies/100000.pickle')


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
    #board = board.reshape(3, 3)
    ps = int(request.args.get('player'))

    logger.info(f'board = {board}')
    logger.info(f'Player Symbol = {ps}')
    #r, c = st.play_it(row, column)

    r, c, nn = player.chooseAction(board, ps)

    logger.info(f'Play {r} {c}')
    return jsonify({'row':int(r), 'col':int(c), 'neural_network':nn})


if __name__ == '__main__':
    APP.debug=True
    APP.run()
