#!/usr/bin/env python


__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import json
import math
import random
import joblib
import logging
import argparse
import numpy as np
import src.nn as nn
import pyBlindOpt.pso as pso
import pyBlindOpt.init as init
import src.tictactoe as tictactoe
import src.minMaxAgent as minMaxAgent


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


NN_ARCHITECTURE = [
    {'input_dim': 9, 'output_dim': 16, 'activation': 'relu'},
    {'input_dim': 16, 'output_dim': 9, 'activation': 'sigmoid'}
]


memory = joblib.Memory('/dev/shm/joblib', verbose=0)


class NNAgent:
    def __init__(self, model, train=True):
        self.model = model
        self.train = train
        self.cols = 3
    
    def _available_positions(self, current_state):
        positions = []
        for i in range(len(current_state)):
            if current_state[i] == 0:
                r = int(i / self.cols)
                c = i % self.cols
                positions.append((r, c))
        return positions

    def chooseAction(self, current_state, symbol):
        available_positions = self._available_positions(current_state)
        if symbol == 1:
            #logger.info(f'Symbol {symbol} -> {current_state}')
            actions, activations = self.model.predict_activations(current_state)
        else:
            fixed_current_state = current_state * -1.0
            #logger.info(f'Symbol {symbol} -> {current_state} -> {fixed_current_state}')
            actions, activations = self.model.predict_activations(fixed_current_state)
        
        # Select only valid actions within valid positions
        if self.model.nn_architecture[-1]['activation'] == 'sigmoid':
            mask = [i for i in range(9) if actions[i] > 0.5]
        else:
            mask = [i for i in range(9) if actions[i] > 0.0]
        
        #logger.info(f'Mask: {mask}')
        positions = [(int(idx / self.cols), idx % self.cols) for idx in mask]
        positions = [p for p in positions if p in available_positions]
        mask = [(row * self.cols) + col for row, col in positions]
        weights = actions[mask]
        
        if len(mask) > 0:
            if self.train:
                r,c = random.choices(positions, weights=weights, k=1)[0]
            else:
                idx = np.argmax(weights)
                r, c = positions[idx]
        else:
            # select random action
            if self.train:
                r,c = random.choice(available_positions)
            else:
                r,c = available_positions[0]

        nn = {'activations': activations, 'networkLayer': self.model.layers()}
        
        return r, c, nn


def objective(p: np.ndarray) -> float:
    '''
    Objective function used to evaluate the candidate solution.

    Args:
        p (np.ndarray): the parameters of the candidate solution
    
    Returns:
        float: the cost value
    '''
    model = nn.NN(NN_ARCHITECTURE)
    model.update(p)
    current_agent = NNAgent(model)
    
    reward = 0.0

    adversary_agent = minMaxAgent.MinMaxAgent(memory)
    
    game = tictactoe.TicTacToe(current_agent, adversary_agent)
    win_p1, draws, win_p2 = game.play(10)
    
    reward += (1.0 * win_p1 + 0.25 * draws + -1.0 * win_p2)
    #logger.info(f'Agent 1 {win_p1}, {draws}, {win_p2} -> {reward}')

    game = tictactoe.TicTacToe(adversary_agent, current_agent)
    win_p1, draws, win_p2 = game.play(10)
    
    reward += (-1.0 * win_p1 + 0.5 * draws + 1.0 * win_p2)
    #logger.info(f'Agent 2 {win_p1}, {draws}, {win_p2} -> {reward}')
    
    return -reward


def store_data(model:dict, parameters:np.ndarray, path:str) -> None:
    '''
    Store the model into a json file.

    Args:
        model (dict): the model definition
        parameters (np.ndarray): the model parameters
        path (str): the location of the file
    '''
    with open(path, 'w') as f:
        json.dump({'model':model, 'parameters':parameters.tolist()}, f)


def main(args: argparse.Namespace) -> None:
    # Define the bounds for the optimization
    bounds = np.asarray([[-1.0, 1.0]]*nn.network_size(NN_ARCHITECTURE))

    # Generate the initial population
    population = [nn.NN(NN_ARCHITECTURE, seed=args.s).ravel() for _ in range(args.n)]

    #reward = objective(population[0])
    #logger.info(f'{reward}')

    # Apply Opposition Learning to the inital population
    population = init.opposition_based(objective, bounds, population=population, n_jobs=args.n)

    # Run the optimization algorithm
    best, obj = pso.particle_swarm_optimization(objective, bounds, n_iter=args.e,
    population=population, n_jobs=args.n, cached=False, verbose=True, seed=args.s)

    logger.info(f'OBJ {obj}')

    # store the best model
    store_data(NN_ARCHITECTURE, best, args.o)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train the agents', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-s', type=int, help='Random generator seed', default=42)
    parser.add_argument('-e', type=int, help='optimization epochs', default=10000)
    parser.add_argument('-n', type=int, help='population size', default=50)
    parser.add_argument('-o', type=str, help='store the best model', default='policies/model_mlp_50_10000.json')
    args = parser.parse_args()
    main(args)