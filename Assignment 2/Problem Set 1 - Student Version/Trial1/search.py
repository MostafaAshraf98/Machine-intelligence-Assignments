from enum import unique
from inspect import formatannotation
from os import remove, stat
from random import vonmisesvariate
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

# TODO: Import any modules you want to use
from queue import PriorityQueue
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # Initialize the Frontier FIFO Queue with the initial state as the only element
    # Queue of tuples
    # First element of tuple is a Node
    # Second element of tuple is a List of actions showing the path from the start to this Node
    frontier = []
    frontier.append((initial_state, []))
    # Initialize the explored Nodes empty set
    explored = set()
    # A Set Keeping only the Nodes in the frontier and not the path as well
    frontierSet = set()
    frontierSet.add(initial_state)

    while(True):
        # If the frontier Queue is empty then no solution no found --> Return failure
        if (not frontier):
            return None
        # Chooses the shallowest node in frontier
        node, path = frontier.pop(0)
        frontierSet.remove(node)
        # Check if this Node is the goal
        if (problem.is_goal(node)):
            # Return the solution
            return path
        # Add it to explored
        explored.add(node)
        # Loop over all the actions that can be preformed on this Node
        for action in problem.get_actions(node):
            # Get the resulting child from this action
            child = problem.get_successor(node, action)
            # If this child is not in explored and not in frontier which means it is not visited before
            if (not(child in explored) and not(child in frontierSet)):
                #  Add this child Node to the frontiers Queue
                newPath = path + [action]
                frontier.append((child, newPath))
                frontierSet.add(child)


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # Initialize the Frontier LIFO Stack with the initial state as the only element
    # Stack of tuples
    # First element of tuple is a Node
    # Second element of tuple is a List of actions showing the path from the start to this Node
    frontier = []
    frontier.append((initial_state, []))
    # Initialize the explored Nodes empty set
    explored = set()
    # A Set Keeping only the Nodes in the frontier and not the path as well
    frontierSet = set()
    frontierSet.add(initial_state)

    while(True):
        # If the frontier Queue is empty then no solution no found --> Return failure
        if (not frontier):
            return None
        # Chooses the deepest node in frontier
        node, path = frontier.pop()
        frontierSet.remove(node)
        # Check if this Node is the goal
        if (problem.is_goal(node)):
            # Return the solution
            return path
        # Add it to explored
        explored.add(node)
        # Loop over all the actions that can be preformed on this Node
        for action in problem.get_actions(node):
            # Get the resulting child from this action
            child = problem.get_successor(node, action)
            # If this child is not in explored and not in frontier which means it is not visited before
            if (not(child in explored)):
                #  Add this child Node to the frontiers Queue
                if(child in frontierSet):
                    # Remove this Node from the frontierSet and frontier queue and add the new one
                    # Because we are searching for the deepest node and not the shallowest
                    frontierSet.remove(child)
                    for n in frontier:
                        if (n[0] == child):
                            frontier.remove(n)
                newPath = path + [action]
                frontier.append((child, newPath))
                frontierSet.add(child)


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # Initialize the Frontier priority queue ordered by PATH-COST with the initial state as the only element
    # Queue of tuples
    # First element of tuple is the PATH COST to this nODE
    # Second element is a counter that serves as the second criteria of comparision for the priority and it is FIFO
    # Third element is the Node
    # Fourth element is the list of actions to get from the start to this Node
    counter = 0
    frontier = PriorityQueue()
    frontier.put((0, counter, initial_state, []))
    # Initialize the explored Nodes empty set
    explored = set()
    while(True):
        # If the frontier Queue is empty then no solution no found --> Return failure
        if (frontier.empty()):
            return None
        # Chooses the lowest cost node in frontier
        cost, _, node, path = frontier.get()

        # We added this condition because a node can exist twice in the frontiers Queue, but once explored when we pop the other one we do not to do the work another time
        if(node in explored):
            continue
        # Check if we reached goal (Here we check after we pop and not when we put)
        if(problem.is_goal(node)):
            return path
        # Add node to explored
        explored.add(node)
        # Loop over all the actions that can be preformed on this Node
        for action in problem.get_actions(node):
            # Get the resulting child from this action
            child = problem.get_successor(node, action)
            # Calculate the new cost
            currentCost = cost + problem.get_cost(node, action)
            # If this child is not in explored which means it is not visited before
            if (not(child in explored)):
                newPath = path + [action]
                counter += 1
                frontier.put((currentCost, counter, child, newPath))


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # Initialize the Frontier priority queue ordered by PATH-COST + Heuristic function with the initial state as the only element
    # Queue of tuples
    # First element of tuple is the PATH COST + Heuristic of this Node
    # Second element is a counter that serves as the second criteria of comparision for the priority and it is FIFO
    # Third element is the Node
    # Fourth element is the list of actions to get from the start to this Node
    counter = 0
    frontier = PriorityQueue()
    frontier.put((0 + heuristic(
        problem, initial_state), counter, initial_state, []))
    # Initialize the explored Nodes empty set
    explored = set()
    while(True):
        # If the frontier Queue is empty then no solution no found --> Return failure
        if (frontier.empty()):
            return None
        # Chooses the lowest cost node in frontier
        cost, _, node, path = frontier.get()

        prevPathCost = cost - heuristic(problem, node)
        # We added this condition because a node can exist twice in the frontiers Queue, but once explored when we pop the other one we do not to do the work another time
        if(node in explored):
            continue
        # Check if we reached goal (Here we check after we pop and not when we put)
        if(problem.is_goal(node)):
            return path
        # Add node to explored
        explored.add(node)
        # Loop over all the actions that can be preformed on this Node
        for action in problem.get_actions(node):
            # Get the resulting child from this action
            child = problem.get_successor(node, action)
            currentCost = prevPathCost + \
                problem.get_cost(node, action) + \
                heuristic(problem, child)
            # If this child is not in explored which means it is not visited before
            if (not(child in explored)):
                newPath = path + [action]
                counter += 1
                frontier.put((currentCost, counter, child, newPath))


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # Initialize the Frontier priority queue ordered by Heuristic function with the initial state as the only element
    # Queue of tuples
    # First element of tuple is the Heuristic of this Node
    # Second element is a counter that serves as the second criteria of comparision for the priority and it is FIFO
    # Third element is the Node
    # Fourth element is the list of actions to get from the start to this Node
    frontier = PriorityQueue()
    counter = 0
    frontier.put((heuristic(
        problem, initial_state), counter, initial_state, []))
    # Initialize the explored Nodes empty set
    explored = set()
    while(True):
        # If the frontier Queue is empty then no solution no found --> Return failure
        if (frontier.empty()):
            return None
        # Chooses the lowest cost node in frontier
        _, _, node, path = frontier.get()

      # We added this condition because a node can exist twice in the frontiers Queue, but once explored when we pop the other one we do not to do the work another time
        if(node in explored):
            continue
        # Check if we reached goal (Here we check after we pop and not when we put)
        if(problem.is_goal(node)):
            return path
        # Add node to explored
        explored.add(node)
        # Loop over all the actions that can be preformed on this Node
        for action in problem.get_actions(node):
            # Get the resulting child from this action
            child = problem.get_successor(node, action)
            currentCost = heuristic(problem, child)
            # If this child is not in explored which means it is not visited before
            if (not(child in explored)):
                newPath = path + [action]
                counter += 1
                frontier.put((currentCost, counter, child, newPath))
