import time
from  agents.LRTAStarAgent import *
from  agents.RTAAStarAgent import *
from  agents.FRITAgent import *

from agents.RTAAStarAgent import *

import maze
from problems import *


# Esempio di utilizzo
#G = nx.grid_2d_graph(10, 10)  # Crea una griglia 10x10
#maze, obstacles = create_maze_with_obstacles(G, randWeight=True, randfrom=1, randto=10, obstacle_prob=0.1)





def runLRTA(problem):
    lrta_agent = LRTAStarAgent(problem)

    currentState=initial_position

    start_time = time.time()
    while True:
        action=lrta_agent(currentState)

        if action == None: break
        nextState=action()
        currentState=nextState
    end_time=time.time()

    execution_time = end_time - start_time

    print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")

def runLSSLRTA(problem, agent_cost_function,search_depth=5):
    lsslrta_agent = LSS_LRTAStarAgent(problem,agent_cost_function)

    currentState=initial_position
    counter=0

    start_time = time.time()
    while True:
        action=lsslrta_agent(currentState)

        if action == None: break
        nextState=action()
        currentState=nextState
        print(f"i'm in: {currentState} state,count: {counter}")
        counter+=1

    end_time=time.time()

    execution_time = end_time - start_time

    print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")

def runRTAA(problem, search_depth=5):
    rtaa_agent = RTAAStarAgent(problem, search_depth=search_depth)

    currentState=initial_position
    counter=0
    start_time = time.time()
    while True:
        action = rtaa_agent(currentState)

        if action == None: break
        nextState=action()
        currentState=nextState
        counter+=1
        print(f"i'm in: {currentState} state,count: {counter}")

    end_time=time.time()

    execution_time = end_time - start_time

    print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")


def runFRIT(problem, initial_state,goal_state,maze_graph, obstacles):
    # Inizializza il problema del labirinto con ostacoli
    problem = Maze2DProblemObstacles(initial_state, goal_state, maze_graph, obstacles)
    
    # Crea un agente FRIT che usa LRTA* per la riconnessione
    frit_agent = FRITAgent(problem, reconnect_strategy='lrta')
    
    # Crea un agente FRIT che usa RTAA* per la riconnessione
    frit_agent_rtaa = FRITAgent(problem, reconnect_strategy='rtaa')
    
    # Chiamata dell'agente
    current_state = (0, 0)  # Stato iniziale
    action = frit_agent(current_state)  # Restituisce la prossima azione secondo FRIT e la strategia scelta    end_time=time.time()
    end_time=time.time()

    execution_time = end_time - start_time

    print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")

###################################
############ MAIN #################
###################################

# maze settings
rows, cols = 30, 30   # <- change this to scale the problem
initial_position=(0,0)
epoch=0
goal_position=(10,11)

start_time = time.time()
G = maze.create_grid_graph(rows, cols)
#mazeInst=maze.create_maze(G,True)

mazeInst,obstacles = maze.create_maze_with_obstacles(G, initial_position, goal_position, randWeight=True, randfrom=1, randto=10, obstacle_prob=0.3)
print(f"time to create maze: {time.time() - start_time} seconds")

mazeProblem=Maze2DProblem(initial_position,goal_position,mazeInst)

#runLRTA(mazeProblem)
#runRTAA(mazeProblem, search_depth=5)
runFRIT(mazeProblem, initial_position,goal_position,mazeInst, obstacles)
#mazeInst = maze.create_maze(G)
#maze.draw_large_maze(mazeInst)

#maze.draw_dynamic_maze_with_obstacles(mazeInst, obstacles)
#maze.draw_large_maze_with_obstacles(mazeInst, obstacles)


#draw_maze(maze,rows,cols)



#################################################
# todo: to draw the state trajectory
#state_traj=nx.Graph()
#state_traj.add_node(epoch,position=initial_position)
#state_traj.add_node("x",position=goal_position)
#################################################

#mazeProblem=Maze2DProblem(initial_position,goal_position,maze)

#runRTAA(mazeProblem, agent_cost_function, search_depth=5)
#runLSSLRTA(mazeProblem, agent_cost_function, search_depth=5)
#runFRIT(mazeProblem, agent_cost_function)
#reconnectionAlgorithm = ReconnectionAlgorithm(search_depth=5)
#frit_agent = FRITAgent(mazeProblem, agent_cost_function, reconnectionAlgorithm)
#frit_agent.follow_and_reconnect(initial_position, goal_position)
