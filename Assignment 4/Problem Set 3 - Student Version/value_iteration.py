from asyncio.windows_events import INFINITE
from typing import Dict
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json

'''
Some useful mdp methods you will use:
    mdp.get_states()
    mdp.get_actions(state)
    mdp.get_successor(state, action)
    mdp.get_reward(state, action, next_state)
    mdp.is_terminal(state)

You can find methods definitions in grid.py
'''
#########################################
#########   Value Iteration    ##########
#########################################

# This is a class for a generic Value Iteration agent


class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A]  # The MDP used by this agent for training
    utilities: Dict[str, float]  # The computed utilities
    # The key is the string representation of the state and the value is the utility
    discount_factor: float  # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # We initialize all the utilities to be 0
        self.utilities = {str(state): 0 for state in self.mdp.get_states()}
        self.discount_factor = discount_factor

    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        # Check if this state is a final state, if it is, return 0
        if (self.mdp.is_terminal(state)):
            return 0.0
        # Otherwise, compute the utility using the bellman equation
        # Variables to keep track of the max utility
        max = -INFINITE

        # Loop through all the states and compute the utility for each one
        for action in self.mdp.get_actions(state):
            result = 0
            # Loop through all the possible next states
            for (next_state, prob) in self.mdp.get_successor(state, action):
                # Get the reward for this staste taking this action
                reward = self.mdp.get_reward(state, action, next_state)
                gamma = self.discount_factor
                result += prob * \
                    (reward + gamma * self.compute_bellman(next_state))
            if result > max:
                max = result
        return max

    # This function applies value iteration starting from the current utilities stored in the agent
    # and stores the new utilities in the agent at the end of each iteration
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)

    def train(self, iterations: int = 1):
        # Starting from the current utilities stored in the agent

        # Apply value iteration for a number of iterations
        for _ in range(iterations):
            # Loop over all the states in self
            for state in self.mdp.get_states():
                # Compute the utility for this state
                self.utilities[str(state)] = self.compute_bellman(state)

    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None

    def act(self, env: Environment[S, A], state: S) -> A:
        # If the state is terminal, return None
        if self.mdp.is_terminal(state):
            return None
        # Otherwise, return the best action

        # Variable to hold the final best action
        best_action = None
        # Variable to hold the best utility of the current best action
        max = -INFINITE
        # Loop over the actions
        for action in self.mdp.get_actions(state):
            sum = 0
            # Loop over all the resultant next states of this action
            for (next_state, prob) in self.mdp.get_successor(state, action):
                utility = self.utilities[str(next_state)]
                sum += prob * utility
            if sum > max:
                max = sum
                best_action = action
        return best_action

    # Save the utilities to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.utilities, f, indent=2, sort_keys=True)

    # loads the utilities from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.utilities = json.load(f)

########################################################
#########   Asynchronous Value Iteration      ##########
########################################################


class AsynchronousValueIterationAgent(ValueIterationAgent):
    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        ValueIterationAgent.__init__(self, mdp, discount_factor)

    # This function applies asynchronous value iteration cycles
    # It updates the utility of one state each iteration using the current utilities stored in the agent
    # Again: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: int = 10):
        # TODO: Complete this function to apply asynchronous value iteration for the given number of iterations
        NotImplemented()
