import argparse
from datetime import datetime
import time,json,maze,os
import ast  # Per convertire le stringhe in tuple
from  agents.LRTAStarAgent import *
from  agents.RTAAStarAgent import *
from  agents.FRITAgent import *
from agents.RTAAStarAgent import *
from problems import *
import gc

import pickle

def export_graph(graph, file_name):
    """
    Esporta il grafo in formato GraphML in un file.
    
    Args:
        graph: Il grafo di tipo networkx.Graph da esportare.
        file_name: Il nome del file (includere l'estensione .graphml).
    """
    try:
        #nx.write_graphml(graph, file_name)
        with open(file_name, "wb") as f:  # 'wb' sta per write-binary
            pickle.dump(graph, f)
        print(f"Grafo esportato con successo in {file_name}")
    except Exception as e:
        print(f"Errore durante l'esportazione del grafo: {e}")



def convert_node_str_to_tuple(node):
    try:
        return ast.literal_eval(node)  # Converte la stringa in una tupla
    except (ValueError, SyntaxError):
        return node  # Se la conversione fallisce, lascia il nodo invariato


def import_graph(file_name):
    """
    Importa un grafo da un file GraphML.
    
    Args:
        file_name: Il nome del file GraphML da cui importare il grafo.
    
    Returns:
        graph: Il grafo importato di tipo networkx.Graph.
    """
    graph = None
    try:
        starttime=time.time()
        #graph = nx.read_graphml(file_name)
        with open(file_name, "rb") as f:  # 'rb' sta per read-binary
            graph = pickle.load(f)
        print(f"Grafo importato con successo da {file_name} in {time.time() - starttime} secondi")
#        return graph
    except Exception as e:
        print(f"Errore durante l'importazione del grafo: {e}")
        return None
    
    print("Converting node strings to tuples...")
    # Creare un nuovo grafo con i nodi riconvertiti
    starttime=time.time()
    ok_graph = nx.Graph()
    for node in graph.nodes():
        new_node = convert_node_str_to_tuple(node)
        ok_graph.add_node(new_node)

    # Aggiungi gli archi con i nuovi nodi convertiti
    for u, v, data in graph.edges(data=True):
        ok_graph.add_edge(convert_node_str_to_tuple(u), convert_node_str_to_tuple(v), **data)
    del graph
    print(f"Conversione completata in {time.time() - starttime} secondi")
    gc.collect()

    return ok_graph

    

def runLRTAexperiment(problem):
    print("Begin LRTA*")

    lrta_agent = LRTAStarAgent(problem)

    currentState=problem.initial
    
    trajectory=[]
    trajectory.append(currentState)
    start_time = time.time()
    while True:
        action=lrta_agent(currentState)
        if action == None: break
        currentState=action()
        trajectory.append(currentState)
        print(f"LRTA>> current state: {currentState}")
    end_time=time.time()

    execution_time = end_time - start_time

    ###metric collections
    trajectory_cost=0
    for i in range(len(trajectory)-1):
        trajectory_cost+=problem.c(trajectory[i],None,trajectory[i+1])
    print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")
    return {"execution_time": execution_time, "trajectory": trajectory, "trajectory_cost": trajectory_cost}



def runRTAAexperiment(problem, search_depth,movements):
    print("Begin RTAA*")
    rtaa_agent = RTAAStarAgent(problem, search_depth,movements,True)

    currentState=problem.initial

    trajectory=[]
    trajectory.append(currentState)

    start_time = time.time()
    while True:
        actions = rtaa_agent(currentState)
        if actions == None: break
        for action in actions:
            currentState=action()
            trajectory.append(currentState)
            print(f"RTAA>> current state: {currentState}")

    trajectory.append(currentState)

    end_time=time.time()
    execution_time = end_time - start_time
    trajectory_cost=0
    for i in range(len(trajectory)-1):
        trajectory_cost+=problem.c(trajectory[i],None,trajectory[i+1])

    print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")
    return execution_time, trajectory, trajectory_cost



def runFRITexperiment(problem, G_M, algorithm, search_depth=1, movements=1):
    # Inizializza il problema del labirinto con ostacoli
    
    # Crea un agente FRIT che usa LRTA* per la riconnessione
    frit_agent = FRITAgent(problem, G_M, algorithm ,search_depth,movements)
    frit_agent()
    end_time=time.time()

    execution_time = end_time - start_time

    print(f"Il tempo di esecuzione della funzione è: {execution_time} secondi")



def load_experiment(file_name):
    """
    Carica il file JSON e restituisce i dati dell'esperimento.
    
    Args:
        file_name: Il nome del file JSON da caricare.
    
    Returns:
        experiment_data: I dati dell'esperimento contenuti nel file JSON.
    
    Raises:
        FileNotFoundError: Se il file non esiste.
        json.JSONDecodeError: Se il file non è un JSON valido.
    """
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"Il file {file_name} non esiste.")
    
    with open(file_name, 'r') as file:
        try:
            experiment_data = json.load(file)
            print(f"Esperimento caricato da {file_name}")
            return experiment_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Errore nel parsing del file JSON: {e}")






def main():
    
    RESULTS_FOLDER = "results"
    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)


    # Crea il parser per gli argomenti
    parser = argparse.ArgumentParser(description="Carica un esperimento da file JSON ed eseguilo")
    
    # Aggiungi un argomento posizionale per il file JSON
    parser.add_argument('experiment', type=str, help="Nome dell'esperimento da eseguire (senza estensione)")
    
    # Esegui il parsing degli argomenti
    args = parser.parse_args()

    

    # Carica l'esperimento dal file
    try:
        experiment_data = load_experiment("experiments/"+args.experiment+".json")
        INPUTFOLDER = experiment_data["input_folder"]
        if not os.path.exists(INPUTFOLDER):
            os.makedirs(INPUTFOLDER)
            os.makedirs(INPUTFOLDER+"/sspanning")
    except FileNotFoundError as e:
        print(f"Errore: {e}")
    except ValueError as e:
        print(f"Errore: {e}")


    ROWS = experiment_data["rows"]
    COLUMNS = experiment_data["columns"]
    START = experiment_data["start"]
    GOAL = experiment_data["goal"]
    WEIGHTS = experiment_data["weights"]
    ALGORITHM = experiment_data["algorithm"]
    SEARCH_DEPTH= experiment_data["search_depth"]
    MOVEMENTS= experiment_data["movements"]

    MAZE_PATH=INPUTFOLDER+"/maze.graphml"
    SUPERGRAPH_PATH=INPUTFOLDER+"/supergraph.graphml"
    
    mazegraph = None
    supermazegraph = None

    if os.path.exists(MAZE_PATH):
        try:
            print(f"Importazione del grafo da {MAZE_PATH}...")
            start_time = time.time()
            mazegraph = import_graph(MAZE_PATH)
            print(f"Grafo importato con successo da {MAZE_PATH} in {time.time() - start_time} secondi")

        #     if ALGORITHM == "FRIT-LRTA*" or ALGORITHM == "FRIT-RTAA*":
        #         start_time = time.time()
        #         supermazegraph = import_graph(SUPERGRAPH_PATH)
        #         print(f"SuperGrafo importato con successo da {SUPERGRAPH_PATH} in {time.time() - start_time} secondi")
        except Exception as e:
            print(f"Errore durante l'importazione del grafo: {e}")
            return None
    else:
        print("Creazione del grafo del labirinto...")
        start_time = time.time()
        G = maze.create_grid_graph(ROWS, COLUMNS)
        print(f"Grid graph creato con successo in {time.time() - start_time} secondi")

        start_time = time.time() 
        mazegraph = maze.create_maze(G,WEIGHTS)
        print(f"Grafo maze creato con successo in {MAZE_PATH} in {time.time() - start_time} secondi")
        del G
        gc.collect() # Garbage collection for memory optimization
        try:
            start_time = time.time()
            #nx.write_graphml(mazegraph, MAZE_PATH)
            export_graph(mazegraph, MAZE_PATH)
            print(f"Grafo esportato con successo in {MAZE_PATH} in {time.time() - start_time} secondi")
        except Exception as e:
            print(f"Errore durante l'esportazione del grafo: {e}")
            return None
        
        if ROWS*COLUMNS<=10000:
            maze.draw_large_maze(mazegraph, INPUTFOLDER)

            start_time = time.time()
            supermazegraph=maze.build_superspanning_grid(ROWS,COLUMNS)
            print(f"Grafo maze superspanning creato con successo in {MAZE_PATH} in {time.time() - start_time} secondi")
            maze.draw_large_maze(supermazegraph, INPUTFOLDER+"/sspanning")




    initial_position=(START['x'],START['y'])
    epoch=0
    goal_position=(GOAL['x'],GOAL['y'])
    mazeProblem=Maze2DProblem(initial_position,goal_position,mazegraph)


    EXP_RESULTS_FOLDER = RESULTS_FOLDER+"/"+args.experiment
    if not os.path.exists(EXP_RESULTS_FOLDER):
        os.makedirs(EXP_RESULTS_FOLDER)

    if ALGORITHM == "LRTA*":
        results=runLRTAexperiment(mazeProblem)        
        jsonResults = json.dumps({
            "execution_time": results["execution_time"],
            "movements": len(results["trajectory"]),
            "trajectory_cost": results["trajectory_cost"],
            "trajectory": results["trajectory"]
        }, indent=4)

    elif ALGORITHM == "RTAA*":
        runRTAAexperiment(mazeProblem, SEARCH_DEPTH, MOVEMENTS)


    elif ALGORITHM == "FRIT-LRTA*":
        start_time = time.time()
        supermazegraph=maze.build_superspanning_grid(ROWS,COLUMNS)
        print(f"Grafo maze superspanning creato con successo in {MAZE_PATH} in {time.time() - start_time} secondi")

        runFRITexperiment(mazeProblem, supermazegraph, FRITAgent.LRTA_STRATEGY)
    elif ALGORITHM == "FRIT-RTAA*":
        start_time = time.time()
        supermazegraph=maze.build_superspanning_grid(ROWS,COLUMNS)
        print(f"Grafo maze superspanning creato con successo in {MAZE_PATH} in {time.time() - start_time} secondi")
        runFRITexperiment(mazeProblem, supermazegraph, FRITAgent.RTAA_STRATEGY, SEARCH_DEPTH, MOVEMENTS)
    else:
        print(f"Algorithm {ALGORITHM} not recognized.")

    if ROWS*COLUMNS<=10000:
        print(f"Risultati: \n {jsonResults}")
    file_name = EXP_RESULTS_FOLDER+f"/results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(file_name, 'w') as json_file:
        json.dump(jsonResults, json_file, indent=4)


if __name__ == "__main__":
    main()
