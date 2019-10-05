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
    from util import Stack
    from game import Directions

    frontier = Stack()
    nodes = {}
    closed = []
    solution = []
    frontier.push(problem.getStartState())
    nodes = createNode(problem.getStartState(),solution,None,0,0,nodes)

    while not frontier.isEmpty():
        current = frontier.pop()
        if problem.isGoalState(current):
            return nodes[current]['action']
        if current not in closed:
            print current
            closed.append(current)
            for suc in problem.getSuccessors(current):
                successor_state,action,cost = suc
                solution = nodes[current]['action'][:]
                solution.append(action)
                nodes = createNode(successor_state,solution,current,nodes[current]['cost'] + cost,nodes[current]['depth'] + 1,nodes)
                frontier.push(successor_state)

def createNode(state,action,parent,cost,depth,nodes):
    nodes[state] = {'action':action,'parent':parent,'cost':cost,'depth':depth}
    return nodes

def breadthFirstSearch(problem):
    from util import Queue
    from util import Stack
    from game import Directions

    frontier =  Queue()
    nodes = {}
    closed = []
    solution = []
    frontier.push(problem.getStartState())
    nodes = createNode(problem.getStartState(),solution,None,0,0,nodes)

    while not frontier.isEmpty():
        current = frontier.pop()
        if problem.isGoalState(current):
            return nodes[current]['action']
        if current not in closed:
            closed.append(current)
            for suc in problem.getSuccessors(current):
                successor_state,action,cost = suc
                solution = nodes[current]['action'][:]
                solution.append(action)
                nodes = createNode(successor_state,solution,current,nodes[current]['cost'] + cost,nodes[current]['depth'] + 1,nodes)
                frontier.push(successor_state)


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

    frontier =  PriorityQueue()
    nodes = {}
    closed = []
    solution = []
    start = problem.getStartState()
    frontier.push(start,0)
    nodes = createNode(start,solution,heuristic(start,problem),0,0,nodes)

    while not frontier.isEmpty():
        current = frontier.pop()
        if problem.isGoalState(current):
            print(nodes[current]['cost'])
            return nodes[current]['action']
        if current not in closed:
            closed.append(current)
            for suc in problem.getSuccessors(current):
                successor_state,action,cost = suc
                solution = nodes[current]['action'][:]
                solution.append(action)
                nodes = createNode(successor_state,solution,current,cost + heuristic(successor_state,problem)
                ,nodes[current]['depth'] + 1,nodes)
                frontier.push(successor_state,nodes[successor_state]['cost'])

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
