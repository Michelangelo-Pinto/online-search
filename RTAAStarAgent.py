class RTAAStarAgent:
    def __init__(self, problem, cost_function, search_depth=5):
        self.problem = problem
        self.cost_function = cost_function  # Funzione di costo passata
        self.H = {problem.initial: problem.h(problem.initial)}  # Tabella delle euristiche
        self.search_depth = search_depth  # Limite di profondità della ricerca

    def __call__(self, state):
        """Esegui la ricerca A* limitata alla profondità e scegli la migliore azione."""
        if self.problem.goal_test(state):
            return None  # Obiettivo raggiunto

        # Esegui la ricerca A* limitata per determinare il prossimo stato
        result, next_state, closed_list = self.bounded_a_star_search(state, self.search_depth)

        # Aggiorna i valori euristici di tutti gli stati espansi
        self.update_heuristics(closed_list, next_state)

        # Ritorna l'azione migliore per muoversi verso il prossimo stato
        for action in self.problem.actions(state):
            if self.problem.output(state, action) == next_state:
                return action

        return None

    def bounded_a_star_search(self, state, depth_limit):
        """Esegui una ricerca A* limitata al dato depth_limit."""
        frontier = [(self.H[state], state, 0)]  # (costo, stato, profondità)
        explored = set()
        closed_list = []

        while frontier:
            frontier.sort(key=lambda x: x[0])  # Ordina per costo totale (h + g)
            total_cost, current_state, current_depth = frontier.pop(0)

            if self.problem.goal_test(current_state):
                return total_cost, current_state, closed_list

            if current_depth < depth_limit:
                explored.add(current_state)
                closed_list.append(current_state)

                for action in self.problem.actions(current_state):
                    next_state = self.problem.output(current_state, action)
                    if next_state not in explored:
                        g = current_depth + self.problem.c(current_state, action, next_state)
                        h = self.H.get(next_state, self.problem.h(next_state))
                        total_cost = self.cost_function(self.problem, current_state, action, next_state, self.H)
                        frontier.append((total_cost, next_state, current_depth + 1))

        return total_cost, current_state, closed_list

    def update_heuristics(self, closed_list, s_bar):
        """Aggiorna gli heuristics per tutti gli stati nella closed_list."""
        # Assicurati che s_bar abbia un valore euristico
        if s_bar not in self.H:
            self.H[s_bar] = self.problem.h(s_bar)

        # Aggiorna l'euristica per tutti gli stati nella closed_list
        for state in closed_list:
            if state not in self.H:
                self.H[state] = self.problem.h(state)  # Usa h(state) come valore iniziale
            self.H[state] = self.H[s_bar] - self.problem.path_cost(0, state, None, s_bar)
