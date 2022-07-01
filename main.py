#!/usr/bin/env python

from flask import Flask, request, jsonify, render_template
from ticTacToe import Player, State

# Create the application.
APP = Flask(__name__)

p1 = Player('computer', exp_rate=0)
p1.loadPolicy('policies/5000.pickle')
st = State(p1)


@APP.route('/')
def index():
    return render_template('index.html')


@APP.route('/play')
def play():
    row = int(request.args.get('row'))
    column = int(request.args.get('col'))
    r, c = st.play_it(row, column)
    return jsonify({'row':r, 'col':c})


if __name__ == '__main__':
    APP.debug=True
    APP.run()