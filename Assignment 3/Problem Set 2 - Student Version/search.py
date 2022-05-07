from json.encoder import INFINITY
from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

# TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state)

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.


def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # get the agent index
    agent = game.get_turn(state)

    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[agent], None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    # Get the best action (The one with the maximum heuristic value) and its value based on the heuristic function
    value, _, action = max((heuristic(game, state, agent), -index, action)
                           for index, (action, state) in enumerate(actions_states))
    return value, action

##############################################################################################################################

# choice values:
# 0 --> min_value_minimax
# 1 --> max_value_minimax
# 2 --> min_value_alphabeta
# 3 --> max_value_alphabeta
# 4 --> negamax


def value(game: Game[S, A], state: S, agent: int, heuristic: HeuristicFunction, max_depth: int, alpha: int, beta: int, choice: int) -> Tuple[float, A]:

    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[agent], None
      # if the max depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, agent), None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    # 0 --> min_value_minimax
    if choice == 0:
        v = (INFINITY, None)
        # Get the best action (The one with the minimum value) and its value based
        for (action, next_state) in actions_states:
            temp = value(game, next_state, agent,
                         heuristic, max_depth-1, 0, 0, 1)
            if temp[0] < v[0]:
                v = temp[0], action
        return v
    # 1 --> max_value_minimax
    elif choice == 1:
        v = (-INFINITY, None)
        # Get the best action (The one with the maximum value) and its value based
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, 0, 0, 0)
            if temp[0] > v[0]:
                v = temp[0], action
        return v
    # 2 --> min_value_alphabeta
    elif choice == 2:
        v = (INFINITY, None)
        # Get the best action (The one with the minimum value) and its value based
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, alpha, beta, 3)
            if temp[0] < v[0]:
                v = temp[0], action
            if v[0] <= alpha:
                return v
            beta = min(beta, v[0])
        return v
    # 3 --> max_value_alphabeta
    elif choice == 3:
        v = (-INFINITY, None)
        # Get the best action (The one with the maximum value) and its value based
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, alpha, beta, 2)
            if temp[0] > v[0]:
                v = temp[0], action
            if v[0] >= beta:
                return v
            alpha = min(alpha, v[0])
        return v
    # 4 --> negamax
    elif choice == 4:
        v = (-INFINITY, None)
        # Get the best action (The one with the maximum value) and its value based
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, 0, 0, 4)
            if temp[0] > v[0]:
                v = temp[0], action
        v[0] = -v[0]
        return v


##############################################################################################################################

# Apply Minimax search and return the tree value and the best action
maxPlayer_minimax = None


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # The max Node is the root node (the agent that calls the function for the first time)
    global maxPlayer_minimax
    # get the agent index
    agent = game.get_turn(state)
    if maxPlayer_minimax == None:
        maxPlayer_minimax = agent

    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[agent], None
    # if the max depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, agent), None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    # if it is the max Node, then maximize the value
    if agent == maxPlayer_minimax:
        v = (-INFINITY, None)
        # for each next state
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, 0, 0, 0)
            if temp[0] > v[0]:
                v = temp[0], action
        return v
    # if it is any other Node, then it is a min Node, then minimize the value
    else:
        v = (INFINITY, None)
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, 0, 0, 1)
            if temp[0] < v[0]:
                v = temp[0], action
        return v

##############################################################################################################################

    # Apply Alpha Beta pruning and return the tree value and the best action


maxPlayer_alphabeta = None


def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # The max Node is the root node (the agent that calls the function for the first time)
    global maxPlayer_alphabeta
    # get the agent index
    agent = game.get_turn(state)
    if maxPlayer_alphabeta == None:
        maxPlayer_alphabeta = agent
    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[agent], None
    # if the max depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, agent), None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    # if it is the max Node, then maximize the value
    if agent == maxPlayer_alphabeta:
        v = (-INFINITY, None)
        # for each next state
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, -INFINITY, INFINITY, 2)
            if temp[0] > v[0]:
                v = temp[0], action
        return v
    # if it is any other Node, then it is a min Node, then minimize the value
    else:
        v = (INFINITY, None)
        for (action, next_state) in actions_states:
            temp = value(
                game, next_state, agent, heuristic, max_depth-1, -INFINITY, INFINITY, 3)
            if temp[0] < v[0]:
                v = temp[0], action
        return v
    ##############################################################################################################################

    # Apply Alpha Beta pruning with move ordering and return the tree value and the best action


def negamax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # get the agent index
    agent = game.get_turn(state)

    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[agent], None
    # if the max depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, agent), None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    v = (-INFINITY, None)
    # for each next state
    for (action, next_state) in actions_states:
        temp = value(
            game, next_state, agent, heuristic, max_depth-1, 0, 0, 4)
        if temp[0] > v[0]:
            v = temp[0], action
    v[0] = - v[0]
    return v


##############################################################################################################################

# Apply Expectimax search and return the tree value and the best action


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # TODO: ADD YOUR CODE HERE
    NotImplemented()
