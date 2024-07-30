from typing import Any, Tuple, Union,List,Dict, Hashable
import networkx as nx


def add_node_with_parent(graph, node, parent):
    graph.add_node(node)
    graph.add_edge(node, parent)
    
def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


class OnlineSearchProblem(Problem):
    """
    A problem which is solved by an agent executing
    actions, rather than by just computation.
    Carried in a deterministic and a fully observable environment."""

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, state):
        return self.graph.graph_dict[state].keys()

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError


    def output(self, state, action):
        return self.graph.graph_dict[state][action]

    def h(self, state):
        """Returns least possible cost to reach a goal for the given state."""
        return self.graph.least_costs[state]

    def c(self, s, a, s1):
        """Returns a cost estimate for an agent to move from state 's' to state 's1'."""
        return 1

    def update_state(self, percept):
        raise NotImplementedError

    def goal_test(self, state):
        if state == self.goal:
            return True
        return False


class MazeProblem(OnlineSearchProblem):
    
    """
    A problem which is solved by an agent executing
    actions, rather than by just computation.
    Carried in a deterministic and a fully observable environment."""

    def __init__(self, initial_state, goal_state,world: nx.Graph):
        super().__init__(initial_state, goal_state,world)

    def actions(self, state):
    
        def goTo(position):
            return position
        
        neighbors_world_list = list(self.graph.neighbors(state))
        actions=set()
        for neigh in neighbors_world_list:
            action=lambda: goTo(neigh)
            action.cost=self.graph[state][neigh]['weight']
            actions.add(action)
        
        return actions
        
    def output(self, state, action):
        return action()

    def h(self, state):
        """Returns least possible cost to reach a goal for the given state."""
        #return nx.dijkstra_path_length(self.world, position, self.goal_state['position'], weight='weight')
        #return nx.shortest_path_length(self.graph, state, self.goal)
        return abs(state[0] - self.goal[0]) + abs(state[1] - self.goal[1])

    def c(self, s, a, s1):
        """Returns a cost estimate for an agent to move from state 's' to state 's1'.
                    we are assuming it's the actual cost"""
        return self.graph[s][s1]['weight']

    def update_state(self, percept):
        raise NotImplementedError

    def goal_test(self, state):
        if state == self.goal:
            return True
        return False

