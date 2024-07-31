import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import Union,Any
from datetime import datetime
import time

from  LRTAStarAgent import *
from problems import Maze2DProblem

def create_grid_graph(rows, cols) -> nx.Graph: 
    G:nx.Graph = nx.grid_2d_graph(rows, cols)
    return G

def create_maze(G, randWeight: bool = False, randfrom=1, randto=20):
    """# The function is designed to ensure that every reachable point in the maze is accessible from any other reachable point.
    """
    # Create a new graph to represent the maze
    maze = nx.Graph()
    
    # Define the starting point of the maze
    start = (0, 0)
    
    # Initialize the stack with the starting point and mark it as visited
    stack = [start]
    visited = {start}

    # Perform a depth-first search (DFS) to create the maze
    while stack:
        # Get the current node from the top of the stack
        current = stack[-1]
        
        # Get all unvisited neighbors of the current node
        neighbors = [n for n in G.neighbors(current) if n not in visited]
        
        if neighbors:
            # Randomly select one of the unvisited neighbors
            neighbor = random.choice(neighbors)
            
            # Determine the weight of the edge
            # If randWeight is True, assign a random weight between randfrom and randto
            # Otherwise, assign a weight of 1
            w = random.randint(randfrom, randto) if randWeight else 1
            
            # Add an edge between the current node and the selected neighbor with the specified weight
            maze.add_edge(current, neighbor, weight=w)
            
            # Mark the neighbor as visited and push it onto the stack
            visited.add(neighbor)
            stack.append(neighbor)
        else:
            # If there are no unvisited neighbors, pop the current node from the stack
            stack.pop()
    
    return maze


def draw_maze(maze, rows, cols):
    # Define the position of nodes in the plot
    # Positions are given by a dictionary where keys are nodes and values are tuples (y, -x)
    # This layout visually arranges nodes in a grid format
    pos = {(x, y): (y, -x) for x, y in maze.nodes()}
    
    # Draw the maze without labels
    # Node size is set to 10, node color is black, and edge color is gray
    nx.draw(maze, pos=pos, with_labels=False, node_size=10, node_color="black", edge_color="gray")
    
    # Add labels to the nodes
    # Labels are created as a dictionary where keys are nodes and values are the string representation of nodes
    labels = {node: f"{node}" for node in maze.nodes()}
    nx.draw_networkx_labels(maze, pos, labels, font_size=8, font_color="red")
    
    # Add edge weight labels
    # Edge labels are created as a dictionary where keys are tuples (u, v) representing edges and values are the weights
    edge_labels = {(u, v): d['weight'] for u, v, d in maze.edges(data=True)}
    nx.draw_networkx_edge_labels(maze, pos, edge_labels=edge_labels, font_size=8, font_color="blue")
    
    # Invert the y-axis for correct visualization: origin in bottom-left
    plt.gca().invert_yaxis()
    
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    
    # Save the plotted graph as a PNG image
    filename = f'graph_{timestamp}.png'
    plt.savefig(filename, format='png')
        
    # Show the plotted graph
    #plt.show()    
    
###################################
############ MAIN #################
###################################

# maze settings
rows, cols = 700, 700   # <- change this to scale the problem

G = create_grid_graph(rows, cols)

start_time = time.time()
maze = create_maze(G)
print(f"time to create maze: {time.time() - start_time} seconds")
time.sleep(3)

#draw_maze(maze,rows,cols)


initial_position=(0,0)
epoch=0
goal_position=(500,500)


#################################################
# todo: to draw the state trajectory
#state_traj=nx.Graph()
#state_traj.add_node(epoch,position=initial_position)
#state_traj.add_node("x",position=goal_position)
#################################################

mazeProblem=Maze2DProblem(initial_position,goal_position,maze)

lrta_agent = MazeLRTAStarAgent(mazeProblem)

currentState=initial_position

start_time = time.time()
while True:
#    lrta_agent = LRTAStarAgent(mazeProblem)
    action=lrta_agent(currentState)
    if action == None: break
    nextState=action()
    #if nextState:
    #    state_traj.add_edge(currentState,nextState)
    currentState=nextState
end_time=time.time()

execution_time = end_time - start_time

print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")