# -*- coding: utf-8 -*-
#
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    from util import Queue
    from util import PriorityQueue
    from util import Stack
    from game import Directions
    #structures to use
    frontier = Stack()
    partial_sols = {}
    closed = []
    #start Initialize
    start = problem.getStartState()
    frontier.push(start)
    partial_sols[start] = []
    #moving through pathfinding
    while not frontier.isEmpty():
        current = frontier.pop()#extract state
        if problem.isGoalState(current):#check if we reached the goal for return solution
            return partial_sols[current]
        if current not in closed: #check if we visited the current and close if not
            closed.append(current)
            for successor in problem.getSuccessors(current):#adding possible moves
                nextnode,action,action_cost = successor
                solution = partial_sols[current][:]#partial solution
                solution.append(action)
                partial_sols[nextnode] = solution
                frontier.push(nextnode)#put the new state at frontier

def breadthFirstSearch(problem):
    from util import Queue
    from util import PriorityQueue
    from util import Stack
    from game import Directions
    #structures to use
    frontier = Queue()
    partial_sols = {}
    closed = []
    #start Initialize
    start = problem.getStartState()
    frontier.push(start)
    partial_sols[start] = []

    closed.append(start)#close start node(if dont do that idk why but bfs does not works like dfs)
                        #copying dfs and replace Stack for Queue does not pass autograder.
    #moving through pathfinding
    while not frontier.isEmpty():
        current = frontier.pop()
        if problem.isGoalState(current):#check if we reached the goal for return solution
            return partial_sols[current]
        for successor in problem.getSuccessors(current):#adding possible moves
            nextnode,action,action_cost = successor
            if nextnode not in closed: #check if we visited the next move and close if not
                closed.append(nextnode)
                solution = partial_sols[current][:]#partial solution
                solution.append(action)
                partial_sols[nextnode] = solution
                frontier.push(nextnode)#put the new state at frontier


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    from util import Queue
    from util import Stack
    from util import PriorityQueue
    from game import Directions
    #Initialize structures
    start = problem.getStartState()
    frontier =  PriorityQueue()
    cost = {}
    partial_sols = {}
    solution = []
    #Using for start node
    frontier.push(start,0)
    cost[start] = 0
    partial_sols[start] = solution[:]

    #Start moving through nodes
    while not frontier.isEmpty():
        current = frontier.pop()
        solution = partial_sols[current]
        #Check problem solution
        if problem.isGoalState(current):
            return partial_sols[current]
        #possible movements
        for successor in problem.getSuccessors(current):
            nextnode,action,action_cost = successor
            new_cost = cost[current] + action_cost #Amount cost + move cost + heuristics
            if nextnode not in cost or new_cost < cost[nextnode]:#node has no cost assigned or newcost is less than the current cost
                cost[nextnode] = new_cost #update cost
                priority = new_cost + heuristic(nextnode,problem)
                frontier.push(nextnode,priority)#set item with the cost as priority
                newsolution = solution[:]#copy current solution and add the action
                newsolution.append(action)
                partial_sols[nextnode] = newsolution

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
