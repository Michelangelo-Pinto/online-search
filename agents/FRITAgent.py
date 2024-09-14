from problems import Maze2DProblemObstacles
from .LRTAStarAgent import *
from .RTAAStarAgent import *


class FRITAgent:
    def __init__(self, problem, reconnect_strategy='lrta', search_depth=5):
        """
        Inizializza l'agente FRIT.
        :param problem: Il problema del labirinto con ostacoli.
        :param reconnect_strategy: La strategia di riconnessione da usare ('lrta', 'rtaa', ecc.).
        :param search_depth: Limite di profondità per la ricerca di riconnessione.
        """
        self.problem = problem
        self.reconnect_strategy = reconnect_strategy  # Strategia di riconnessione (default: 'lrta')
        self.search_depth = search_depth  # Limite di profondità per la ricerca
        self.ideal_tree = {}  # L'albero ideale
        self.current_plan = []  # Percorso attuale
        self.observed_obstacles = set()  # Ostacoli osservati

    def __call__(self, current_state):
        """Esegue l'agente FRIT a partire dallo stato attuale."""
        if self.problem.goal_test(current_state):
            return None
        
        # Se l'azione corrente non esiste o è vuota, segui l'albero ideale o riconnettiti
        if not self.current_plan:
            action = self.follow_ideal_tree(current_state)
            if action:
                return action
            else:
                # Se incontriamo un ostacolo o il percorso è bloccato, riconnetti usando la strategia selezionata
                return self.reconnect(current_state)

        # Segui il piano corrente se esiste
        return self.execute_next_action(current_state)

    def follow_ideal_tree(self, current_state):
        """Prova a seguire l'albero ideale e restituisce l'azione successiva se possibile."""
        if current_state in self.ideal_tree:
            next_state = self.ideal_tree[current_state]
            if next_state and next_state not in self.observed_obstacles:
                for action in self.problem.actions(current_state):
                    if self.problem.output(current_state, action) == next_state:
                        self.current_plan = [next_state]
                        return action
        return None

    def reconnect(self, current_state):
        """Usa la strategia di riconnessione per trovare un nuovo percorso."""
        self.observed_obstacles.update(self.problem.observe_environment(current_state))

        # Crea un sottoproblema dinamico aggiornato con gli ostacoli osservati
        dynamic_problem = self.create_dynamic_subproblem()

        # Scegli la strategia di riconnessione in base al parametro reconnect_strategy
        if self.reconnect_strategy == 'lrta':
            reconnect_plan = self.lrta_reconnect_strategy(current_state, dynamic_problem)
        elif self.reconnect_strategy == 'rtaa':
            reconnect_plan = self.rtaa_reconnect_strategy(current_state, dynamic_problem)
        else:
            raise ValueError(f"Strategia di riconnessione non supportata: {self.reconnect_strategy}")

        if reconnect_plan:
            self.current_plan = reconnect_plan
            return self.execute_next_action(current_state)
        return None

    def create_dynamic_subproblem(self):
        """Crea un sottoproblema basato sulla conoscenza attuale e gli ostacoli osservati."""
        # Crea una copia del grafo originale e rimuovi gli ostacoli osservati
        dynamic_graph = self.problem.graph.copy()
        for obstacle in self.observed_obstacles:
            if obstacle in dynamic_graph:
                dynamic_graph.remove_node(obstacle)

        # Crea un nuovo problema Maze2DProblemObstacles con la conoscenza attuale
        return Maze2DProblemObstacles(self.problem.initial, self.problem.goal, dynamic_graph)

    def execute_next_action(self, current_state):
        """Esegue la prossima azione nel piano attuale."""
        if self.current_plan:
            next_state = self.current_plan.pop(0)
            for action in self.problem.actions(current_state):
                if self.problem.output(current_state, action) == next_state:
                    return action
        return None

    def initialize_ideal_tree(self, start):
        """Inizializza l'albero ideale (prevede una mappa completa senza ostacoli)."""
        self.ideal_tree = {state: None for state in self.problem.get_all_states()}

    @staticmethod
    def lrta_reconnect_strategy(current_state, problem):
        """Strategia di riconnessione LRTA*."""
        lrta_agent = LRTAStarAgent(problem)
        plan = []
        while current_state != problem.goal:
            action = lrta_agent(current_state)
            if action is None:
                break
            current_state = problem.output(current_state, action)
            plan.append(current_state)
        return plan

    @staticmethod
    def rtaa_reconnect_strategy(current_state, problem, search_depth=5):
        """Strategia di riconnessione RTAA*."""
        rtaa_agent = RTAAStarAgent(problem, search_depth)
        plan = []
        while current_state != problem.goal:
            action = rtaa_agent(current_state)
            if action is None:
                break
            current_state = problem.output(current_state, action)
            plan.append(current_state)
        return plan
