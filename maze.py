import networkx as nx
import matplotlib.pyplot as plt
import random
from typing import Union,Any
from datetime import datetime
import time


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


def build_superspanning_grid(rows, cols):
    """
    Costruisce un grafo superspanning per una griglia di dimensioni rows x cols
    dove ogni nodo è connesso ai suoi vicini ortogonali e diagonali con peso fisso 1.
    
    rows: Numero di righe della griglia.
    cols: Numero di colonne della griglia.
    """
    G_M = nx.Graph()

    # Aggiungi i nodi al grafo
    for r in range(rows):
        for c in range(cols):
            G_M.add_node((r, c))

    # Aggiungi archi verso i vicini ortogonali e diagonali con peso 1
    for r in range(rows):
        for c in range(cols):
            current_node = (r, c)
            
            # Lista dei possibili spostamenti (ortogonali e diagonali)
            # neighbors = [
            #     (r-1, c-1), (r-1, c), (r-1, c+1),  # Sopra (diagonali e ortogonali)
            #     (r, c-1),            (r, c+1),     # Sinistra e destra
            #     (r+1, c-1), (r+1, c), (r+1, c+1)   # Sotto (diagonali e ortogonali)
            # ]
            # Lista dei possibili spostamenti (solo ortogonali)
            neighbors = [
                (r-1, c),  # Sopra
                (r+1, c),  # Sotto
                (r, c-1),  # Sinistra
                (r, c+1)   # Destra
            ]
            
            # Aggiungi archi se i vicini sono validi
            for neighbor in neighbors:
                nr, nc = neighbor
                if 0 <= nr < rows and 0 <= nc < cols:
                    G_M.add_edge(current_node, neighbor, weight=1)  # Peso fisso 1

    return G_M

def create_maze_with_obstacles(G, start, goal, randWeight: bool = False, randfrom=1, randto=20, obstacle_prob=0.1):
    """
    Crea un maze con la proprietà che ogni punto è raggiungibile da qualsiasi altro punto
    e aggiunge ostacoli in modo tale da mantenere la connettività tra start e goal.
    """
    maze = nx.Graph()
    stack = [start]
    visited = {start}

    # Crea il maze utilizzando DFS
    while stack:
        current = stack[-1]
        neighbors = [n for n in G.neighbors(current) if n not in visited]
        if neighbors:
            neighbor = random.choice(neighbors)
            w = random.randint(randfrom, randto) if randWeight else 1
            maze.add_edge(current, neighbor, weight=w)
            visited.add(neighbor)
            stack.append(neighbor)
        else:
            stack.pop()

    # Aggiungi ostacoli
    obstacles = set()
    nodes = list(maze.nodes)

    for node in nodes:
        # Evita di rimuovere i nodi start e goal
        if node == start or node == goal:
            continue

        if random.random() < obstacle_prob:
            # Crea una copia del grafo senza l'ostacolo e prova a rimuovere l'arco
            maze_copy = maze.copy()
            # Rimuovi tutte le connessioni in cui è coinvolto il nodo come ostacolo (non il nodo stesso)
            neighbors = list(maze_copy.neighbors(node))
            maze_copy.remove_node(node)
            path_exists = nx.has_path(maze_copy, start, goal)

            if path_exists:
                obstacles.add(node)

    return maze, obstacles



    


def draw_large_maze(maze, folder="mazes/xxx", edge_colors='green'):
    """
    Disegna un maze con parametri di disegno dinamici in base alla grandezza del grafo.
    """
    # Ottieni il numero totale di nodi nel grafo
    num_nodes = len(maze.nodes())
    
    # Calcola i parametri dinamici in base al numero di nodi
    scale_factor = max(1, num_nodes // 100)  # Fattore per gestire la densità del grafo
    node_size = max(5, 30 // scale_factor)  # Dimensione dei nodi
    font_size = max(4, 12 // scale_factor)  # Dimensione del font per i nodi
    edge_font_size = max(3, 10 // scale_factor)  # Dimensione del font per i pesi degli archi
    separation_factor = 20 + (scale_factor * 0.5)  # Fattore di separazione tra i nodi
    
    # Crea un layout a griglia con maggiore separazione
    pos = {(x, y): (y * separation_factor, -x * separation_factor) for x, y in maze.nodes()}

    # Genera i colori per gli archi, se non forniti
    if edge_colors is None:
        edge_colors = ['gray' for _ in maze.edges()]
    
    # Imposta la risoluzione dell'immagine
    plt.figure(figsize=(20, 20), dpi=150)
    
    # Disegna il maze con i colori degli archi
    nx.draw(maze, pos=pos, with_labels=False, node_size=node_size, node_color="black", 
            edge_color=edge_colors, width=1.5)
    
    # Aggiungi le etichette dei nodi (stati)
    labels = {node: f"{node}" for node in maze.nodes()}
    nx.draw_networkx_labels(maze, pos, labels, font_size=font_size, font_color="red")
    
    # Aggiungi le etichette degli archi (pesi)
    edge_labels = {(u, v): d['weight'] for u, v, d in maze.edges(data=True)}
    nx.draw_networkx_edge_labels(maze, pos, edge_labels=edge_labels, font_size=edge_font_size, font_color="blue")
    
    # Inverti l'asse y per una visualizzazione corretta
    plt.gca().invert_yaxis()
    
    # Salva il grafico
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = folder+f'/maze_{timestamp}.png'
    plt.savefig(filename, format='png', bbox_inches='tight', dpi=300)



def draw_large_maze_with_obstacles(maze, obstacles):
    """
    Disegna il maze con ostacoli per grafi più grandi, usando un layout `spring_layout` e controllando le dimensioni.
    """
    # Usa il layout a molla (spring_layout) per posizionare i nodi
    pos = nx.spring_layout(maze, k=0.15, iterations=20)  # k controlla la distanza tra i nodi
    
    # Filtra gli ostacoli per includere solo quelli che sono effettivamente presenti nel maze
    obstacles_in_maze = [node for node in obstacles if node in maze.nodes]
    
    # Disegna il maze senza labels, con nodi piccoli e archi sottili
    nx.draw(maze, pos=pos, with_labels=False, node_size=20, node_color="black", edge_color="gray", width=0.5)
    
    # Aggiungi labels agli archi, con colori blu per i pesi degli archi
    edge_labels = {(u, v): d['weight'] for u, v, d in maze.edges(data=True)}
    nx.draw_networkx_edge_labels(maze, pos, edge_labels=edge_labels, font_size=6, font_color="blue")
    
    # Disegna gli ostacoli, colorandoli di rosso
    nx.draw_networkx_nodes(maze, pos, nodelist=obstacles_in_maze, node_color="red", node_size=50)
    
    # Salva il grafico come immagine PNG
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f'large_maze_with_obstacles_{timestamp}.png'
    plt.savefig(filename, format='png')
    
    # Mostra il grafico
    plt.show()

