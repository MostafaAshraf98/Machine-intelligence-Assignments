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
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[str, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {str(state):0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        NotImplemented()
    
    # This function applies value iteration starting from the current utilities stored in the agent 
    # and stores the new utilities in the agent at the end of each iteration
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: int = 1):
        #TODO: Complete this function to apply value iteration for the given number of iterations
        NotImplemented()
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        NotImplemented()
    
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
        #TODO: Complete this function to apply asynchronous value iteration for the given number of iterations
        NotImplemented()
    