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
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import code

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def getActions(state, start, end):
  actions = []
  node = end
  while node in state and node != start:
    actions.insert(0, state[node][1])
    node = state[node][0]

  return actions

def search(problem, Q, update=lambda l: l['child'] not in l['closed'], enqueue=lambda l, node, cost: l['Q'].push((node, cost)),
    costMetric=lambda l, node, rootCost: 0):
  start = problem.getStartState()
  closed = set()
  state = {}
  cost = 0
  enqueue(locals(), start, costMetric(locals(), start, 0))
  while not Q.isEmpty():
    node, rootCost = Q.pop()
    if not node in closed:
      closed.add(node)
     # print "Dequeueing: " + str((node, rootCost))
      if problem.isGoalState(node): return getActions(state, start, node)
      for (child, action, cost) in problem.getSuccessors(node):
        totalCost = costMetric(locals(), child, rootCost)
        if update(locals()):
          enqueue(locals(), child, totalCost)
      #    print "Queuing: " + str( (child, totalCost)) + "with cost " + str(cost)
          state[child] = (node, action, totalCost)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return search(problem, util.Stack())

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return search(problem, util.Queue(), lambda l: l['child'] not in l['closed'] and l['child'] not in l['state'])

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    return search(problem, util.PriorityQueue(), lambda l: l['child'] not in l['closed'] and l['child'] not in l['state'] or ( l['child'] in l['state'] and l['totalCost'] < l['state'][l['child']][2]),
        enqueue=lambda l, node, cost: l['Q'].push((node, cost), cost), costMetric=lambda l, node, rootCost: rootCost + l['cost'])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    return search(problem, util.PriorityQueue(), lambda l: l['child'] not in l['closed'] and l['child'] not in l['state'] or ( l['child'] in l['state'] and l['totalCost'] < l['state'][l['child']][2]),
        enqueue=lambda l, node, cost: l['Q'].push((node, cost - heuristic(node, l['problem'])), cost), costMetric=lambda l, node, rootCost: rootCost + l['cost'] + heuristic(node, l['problem']))

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
