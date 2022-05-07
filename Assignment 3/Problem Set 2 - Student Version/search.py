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

# Apply Minimax search and return the tree value and the best action


def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def value_minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int, maxPlayer: int) -> Tuple[float, A]:
        # get the agent index
        agent = game.get_turn(state)

        # Check if this state is a terminal state
        # if it is a terminal state, the second return value will be a list of terminal values for all agents
        # if it is not a terminal state, the second return value will be None
        terminal, values = game.is_terminal(state)

        # if it is a terminal state, return the terminal value and None for actions
        # it is values[maxPlayer] and not values[agent] because all the agents want to maximize/minimize the utility of maxPlayer and not their own
        if terminal:
            return values[maxPlayer], None

          # if the max depth is reached, return the heuristic value
          # it is heuristic(game, state, maxPlayer) and not heuristic(game, state, agent) because all the agents want to maximize/minimize the utility of maxPlayer and not their own
        if max_depth == 0:
            return heuristic(game, state, maxPlayer), None

        # Get all the next states (resulting states of all the possible actions from the current state)
        # action_states is a list of tuples (action, state)
        actions_states = [(action, game.get_successor(state, action))
                          for action in game.get_actions(state)]

        # minimax and min Node
        if agent != maxPlayer:
            v = (INFINITY, None)
            # Get the best action (The one with the minimum value) and its value
            for (action, next_state) in actions_states:
                temp, _ = value_minimax(game, next_state,
                                        heuristic, max_depth-1, maxPlayer)
                if temp < v[0]:
                    v = temp, action
            return v
        # minimax and max Node
        else:
            v = (-INFINITY, None)
            # Get the best action (The one with the maximum value) and its value
            for (action, next_state) in actions_states:
                temp, _ = value_minimax(
                    game, next_state, heuristic, max_depth-1, maxPlayer)
                if temp > v[0]:
                    v = temp, action
            return v
##############################################################################################################################
    # The max Node is the root node (the agent that calls the function for the first time)
    maxPlayer = game.get_turn(state)

    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[maxPlayer], None
    # if the max depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, maxPlayer), None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    v = (-INFINITY, None)
    # for each next state
    for (action, next_state) in actions_states:
        temp, _ = value_minimax(
            game, next_state, heuristic, max_depth-1, maxPlayer)
        if temp > v[0]:
            v = temp, action
    return v

##############################################################################################################################

    # Apply Alpha Beta pruning and return the tree value and the best action


def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    def value_alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int, alpha: int, beta: int, maxPlayer: int) -> Tuple[float, A]:

        agent = game.get_turn(state)

        terminal, values = game.is_terminal(state)

        if terminal:
            return values[maxPlayer], None

        if max_depth == 0:
            return heuristic(game, state, maxPlayer), None

        actions_states = [(action, game.get_successor(state, action))
                          for action in game.get_actions(state)]
        # Alphabeta and min Node
        if agent != maxPlayer:
            v = (INFINITY, None)
            # Get the best action (The one with the minimum value) and its value
            for (action, next_state) in actions_states:
                temp, _ = value_alphabeta(
                    game, next_state, heuristic, max_depth-1, alpha, beta, maxPlayer)
                if temp < v[0]:
                    v = temp, action
                if v[0] <= alpha:
                    return v
                beta = min(beta, v[0])
            return v
        # Alphabeta and max Node
        else:
            v = (-INFINITY, None)
            # Get the best action (The one with the maximum value) and its value
            for (action, next_state) in actions_states:
                temp, _ = value_alphabeta(
                    game, next_state, heuristic, max_depth-1, alpha, beta, maxPlayer)
                if temp > v[0]:
                    v = temp, action
                if v[0] >= beta:
                    return v
                alpha = max(alpha, v[0])
            return v
##############################################################################################################################
    maxPlayer = game.get_turn(state)

    v = value_alphabeta(
        game, state, heuristic, max_depth, -INFINITY, INFINITY, maxPlayer)
    return v
    ##############################################################################################################################


def negamax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:

    def value_negamax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int, maxPlayer: int) -> Tuple[float, A]:

        agent = game.get_turn(state)

        terminal, values = game.is_terminal(state)

        if terminal:
            return values[maxPlayer], None

        if max_depth == 0:
            return heuristic(game, state, maxPlayer), None

        actions_states = [(action, game.get_successor(state, action))
                          for action in game.get_actions(state)]
        # negamax with minNode
        if agent != maxPlayer:
            v = (-INFINITY, None)
            # Get the best action (The one with the maximum value) and its value

            for (action, next_state) in actions_states:
                temp, _ = value_negamax(
                    game, next_state, heuristic, max_depth-1, maxPlayer)
                temp = -temp
                if temp > v[0]:
                    v = temp, action
            v = (-v[0], v[1])
            return v
        else:
            v = (-INFINITY, None)
            # Get the best action (The one with the maximum value) and its value
            for (action, next_state) in actions_states:
                temp, _ = value_negamax(
                    game, next_state, heuristic, max_depth-1, maxPlayer)
                if temp > v[0]:
                    v = temp, action
            return v
##############################################################################################################################
    # get the agent index
    maxPlayer = game.get_turn(state)

    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[maxPlayer], None
    # if the max depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, maxPlayer), None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    v = (-INFINITY, None)
    # for each next state
    for (action, next_state) in actions_states:
        temp, _ = value_negamax(
            game, next_state, heuristic, max_depth-1, maxPlayer)
        if temp > v[0]:
            v = temp, action
    return v


##############################################################################################################################

# Apply Expectimax search and return the tree value and the best action


def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:

    def value_expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int, maxPlayer: int) -> Tuple[float, A]:

        agent = game.get_turn(state)

        terminal, values = game.is_terminal(state)

        if terminal:
            return values[maxPlayer], None

        if max_depth == 0:
            return heuristic(game, state, maxPlayer), None

        actions_states = [(action, game.get_successor(state, action))
                          for action in game.get_actions(state)]
        if agent != maxPlayer:
            v = (0, None)
            # Get the best action (The one with the maximum value) and its value based
            for (action, next_state) in actions_states:
                temp, _ = value_expectimax(
                    game, next_state, heuristic, max_depth-1, maxPlayer)
                v = (v[0]+temp, None)
            v = (v[0]/len(actions_states), v[1])
            return v
    # Expectimax and max Node
        else:
            v = (-INFINITY, None)
            # Get the best action (The one with the maximum value) and its value based
            for (action, next_state) in actions_states:
                temp, _ = value_expectimax(
                    game, next_state, heuristic, max_depth-1, maxPlayer)
                if temp > v[0]:
                    v = temp, action
            return v
##############################################################################################################################
    # The max Node is the root node (the agent that calls the function for the first time)
    maxPlayer = game.get_turn(state)

    # Check if this state is a terminal state
    # if it is a terminal state, the second return value will be a list of terminal values for all agents
    # if it is not a terminal state, the second return value will be None
    terminal, values = game.is_terminal(state)

    # if it is a terminal state, return the terminal value and None for actions
    if terminal:
        return values[maxPlayer], None
    # if the max depth is reached, return the heuristic value
    if max_depth == 0:
        return heuristic(game, state, maxPlayer), None

    # Get all the next states (resulting states of all the possible actions from the current state)
    # action_states is a list of tuples (action, state)
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    v = (-INFINITY, None)
    # for each next state
    for (action, next_state) in actions_states:
        temp, _ = value_expectimax(
            game, next_state, heuristic, max_depth-1, maxPlayer)
        if temp > v[0]:
            v = temp, action
    return v
