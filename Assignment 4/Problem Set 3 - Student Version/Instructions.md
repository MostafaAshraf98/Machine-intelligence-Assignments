# Problem Set 3: Reinforcement Learning

The goal of this problem set is to implement and get familiar with Reinforcement Learning.

To run the autograder, type the following command in the terminal:

    python autograder.py

If you wish to run a certain problem only (e.g. problem 1), type:

    python autograder.py -q 1

where 1 is the number of the problem you wish to run.

## Instructions

In the attached python files, you will find locations marked with:

    #TODO: ADD YOUR CODE HERE
    NotImplemented()

Remove the `NotImplemented()` call and write your solution to the problem. **DO NOT MODIFY ANY OTHER CODE**; The grading of the assignment will be automated and any code written outside the assigned locations will not be included during the grading process.

**IMPORTANT**: You must document your code (explain the algorithm you are implementing in your own words within the code) to get the full grade. Undocumented code will be penalized.

For this assignment, you should submit the following files only:
- `value_iteration.py`
- `reinforcement_learning.py`

Put the two files in a compressed zip file named StudentID_StudentFullName_TutCode_Ass3.zip which you should submit to Blackboard where TutCode refers to the room you take your tutorial in 3706 --> 1 and 3708 --> 2.

---

## Problem Definitions

There is one environment defined in this problem set:
1. **Grid World**: where the environment is a 2D grid where the player can move in one of 4 directions (`U`, `D`, `L`, `R`). The actions are noisy so the end result may be moving along one of the 2 directions orthogonal to the desired direction. For example, if the noise probability is 0.2 and the agent decided to move up, it will end up at the upper cell with probability 0.8 and the orthogonal direction with probability 0.2 (the left cell with probability 0.1 and the right cell with probability 0.1). Some locations `"#"` are occupied with walls so the player cannot stand on them. Some other locations `"T"` are terminal states which ends the episode as soon as the player stands on them. Each location has an associated reward which is given to player if they do an action that gets them to be in that state in the next time step. The markov decision process and environment of the grid world is implemented in `grid.py` and the environment instances are included in the `grids` folder.

You can play a grid world game by running:

    # For playing a grid (e.g. grid1.json)  
    python play.py grids\grid1.json

You can also let an learning agent play the game in your place (e.g. a Q-Learning Agent) as follow:

    python play.py grids\grid1.json -a q_learning -m models/model.json

**NOTE:** In addition to the agent, we supply a model file from which the agent will read its data (e.g. Q-values for Q-learing & SARSA agents, weights for approximate Q-learning and Utilities for value iteration agents). If we don't supply a model file, the agent will play using the initial values of their learnable parameters.

To train an agent and save its data in model file, use `train.py` as follows:

    # For training a q_learning agent on grid1.json for 1000 iterations where each episode is limited to 100 steps only
    python train.py q_learning grids\grid1.json models/model.json -i 1000 -sl 100


The agent options are:
- `human` where the human play via the console
- `random` where the computer plays randomly
- `value_iteration` where the agent uses the learned utilities (via value iteration) and the MDP to decide on the action to take.
- `async_value_iteration` where the agent uses the learned utilities (via asynchronous value iteration -explained below-) and the MDP to decide on the action to take.
- `sarsa` where the agent uses the learned Q-value (via SARSA) to decide on the action to take.
- `q_learning` where the agent uses the learned Q-value (via Q-Learning) to decide on the action to take.
- `q_learning_approx` where the agent uses the learned weights (via Linear Approximate Q-Learning) to decide on the action to take.

To check all the arguments you can specify in play and run commands, run `play.py` and `train.py` with the `-h` flag to get detailed help messages. 

---

## Important Notes

This problem set relies a lot on randomness and Reinforcement Learning usually does not converge to the same results when different random seeds are used. So it is essential to follow the instructions written in the comments around the TODOs to acheive the same results. In addition, while acting, if two actions have the same value (Q-value, expected utilities, etc.), pick the action that appears first in the list returned by `mdp.get_actions` or `env.actions()`.

---

## Problem 1: Value Iteration

Inside `value_iteration.py`, modify the functions marked by a `**TODO**` to complete the `ValueIterationAgent` class. Note that the Reward `R(s, a, s')` is a function of the current state, the action and the next state, so use the appropriate version of the bellman equation:

$$U_{i+1}(s) = \max_{a} \sum_{s'} P(s'|s,a) [ R(s,a,s') + \gamma U_{i}(s')]$$

**NOTE:** Gamma is the discount factor and could be specified using the option `-d`

## Problem 2: Asynchronous Value Iteration
Inside `value_iteration.py`, modify the functions marked by a `**TODO**` to complete the `AsynchronousValueIterationAgent` class. AsynchronousValueIterationAgent takes an MDP on construction and runs cyclic value iteration (described in the next paragraph) for the specified number of iterations.

The reason this class is called AsynchronousValueIterationAgent is because we will update only one state in each iteration using bellman update rule, as opposed to doing a batch-style update (as in question 1). Here is how cyclic value iteration works. In the first iteration, only update the value of the first state in the states list. In the second iteration, only update the value of the second. Keep going until you have updated the value of each state once, then start back at the first state for the subsequent iteration.
Again, here’s the bellman update equation:

$$U_{i+1}(s) = \max_{a} \sum_{s'} P(s'|s,a) [ R(s,a,s') + \gamma U_{i}(s')]$$

## Problem 3: SARSA

Inside `reinforcement_learning.py`, modify the functions marked by a `**TODO**` to complete the `SARSALearningAgent` class. 

$$Q(s,a) \leftarrow Q(s,a) + \alpha(r + \gamma Q(s',a') - Q(s,a))$$

## Problem 4: Q-Learning

Inside `reinforcement_learning.py`, modify the functions marked by a `**TODO**` to complete the `QLearningAgent` class. 

$$Q(s,a) \leftarrow Q(s,a) + \alpha(r + \gamma \max_{a'}Q(s',a') - Q(s,a))$$

## Problem 5: Approximate Q-Learning

Inside `reinforcement_learning.py`, modify the functions marked by a `**TODO**` to complete the `ApproximateQLearningAgent` class. 

$$w_{ia} \leftarrow w_{ia} + \alpha(r + \gamma \max_{a'}Q(s',a') - Q(s,a))w_i$$

where $$w_{ia}$$ is the the weight of the feature $$x_i$$ in $$Q(s,a)$$ and $${x_1, x_2, ..., x_n}$$ are the features of the state $$s$$. Thus the approximate Q-function can be written as follows:

$$Q(s,a) = \sum_i w_{ia}*x_i$$

## Delivery

The delivery deadline is `Sunday May 29th 2022 23:59`. It should be delivered on **Blackboard**. This is an individual assignment. The delivered code should be solely written by the student who delivered it. Any evidence of plagiarism will lead to receiving **zero** points.
