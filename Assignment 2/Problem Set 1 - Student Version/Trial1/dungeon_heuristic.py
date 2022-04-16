from multiprocessing import managers
from turtle import distance
from winsound import PlaySound
from xml.sax.handler import property_lexical_handler
from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal


def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

# TODO: Import any modules and write any functions you want to use


def DP_DistanceCalculator(problem: DungeonProblem, coins, currentLocation: Point) -> float:
    memo = problem.cache()
    currentState = (currentLocation, coins)
    if(currentState in memo):
        return memo[currentState]

    if(len(coins) == 0):
        return manhattan_distance(currentLocation, problem.layout.exit)

    stateCoins = set(coins)
    iterationCoins = list(coins)
    minDistance = float("inf")
    for coin in iterationCoins:
        stateCoins.remove(coin)
        distance = manhattan_distance(
            currentLocation, coin) + DP_DistanceCalculator(problem, frozenset(stateCoins), coin)
        minDistance = min(minDistance, distance)
        stateCoins.add(coin)

    memo[currentState] = minDistance
    return memo[currentState]


def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    # TODO: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.is_goal" HERE.
    # Calling it here will mess up the tracking of the explored nodes count
    # which is considered the number of is_goal calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    return DP_DistanceCalculator(problem, state.remaining_coins, state.player)
