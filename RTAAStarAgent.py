class RTAAStarAgent:
    def __init__(self, problem, cost_function, search_depth=5, movements=5):
        self.problem = problem
        self.cost_function = cost_function
        self.H = {problem.initial: problem.h(problem.initial)}  # Euristica iniziale
        self.search_depth = search_depth  # Profondità del lookahead
        self.movements = movements  # Numero di movimenti che l'agente esegue dopo ogni ricerca A*
        self.g = {problem.initial: 0}  # Valori g per ogni stato, inizializzando lo stato iniziale a 0
        self.visited = {}  # Dizionario degli stati visitati

    def __call__(self, scurr):
        """Implementa la procedura realtime_adaptive_astar del paper"""

        if self.problem.goal_test(scurr):
            return None

        # Step 2: Determina il numero di stati da espandere (lookahead)
        lookahead = self.search_depth

        # Step 3: Esegui astar() limitato
        s_bar, closed_list = self.astar(scurr, lookahead)

        # Step 4-5: Gestisci il caso di fallimento
        if s_bar is None:
            print("A* search failed")
            return None
        else:
            if s_bar not in self.H:
                self.H[s_bar] = self.problem.h(s_bar)  # Inizializza H[s_bar] se non è presente

        # Step 6-7: Aggiorna le euristiche per tutti gli stati espansi
        for s in closed_list:
            if s not in self.g:
                self.g[s] = float('inf')  # Inizializza g[s] se non è presente
            if s_bar not in self.g:
                self.g[s_bar] = float('inf')  # Inizializza g[s_bar] se non è presente
            if s not in self.H:
                self.H[s] = self.problem.h(s)  # Inizializza H[s] se non è presente

            # Aggiorna l'euristica usando la formula di RTAA*
            if self.g[s] < float('inf') and self.g[s_bar] < float('inf'):
                self.H[s] = self.g[s_bar] + self.H[s_bar] - self.g[s] +(self.visited.get(s, 0) - 1 if s in self.visited else 0) * 10
            else:
                print(f"Warning: Invalid g(s) or g(s_bar) for state {s}")

        # Step 8: Determina il numero di movimenti
        movements = self.movements
        ac_tor = None  # the action to return.

        # Step 9: Muoviti lungo la traiettoria fino a s_bar o fino a esaurire i movimenti
        while scurr != s_bar and movements > 0:
            # Step 10: Seleziona l'azione migliore
            ac_tor = self.select_best_action(scurr, s_bar)

            # Verifica se è stata trovata un'azione valida
            if ac_tor is None:
                print(f"No valid action found from state {scurr}")
                return None

            # Non chiamiamo l'azione, ma la passiamo direttamente a problem.output
            scurr = self.problem.output(scurr, ac_tor)
            movements -= 1

            if scurr not in self.visited:
                self.visited[scurr] = 1
            else:
                self.visited[scurr] += 1


        # Step 13-16: Gestione dei costi dinamici se richiesto
        # Inserisci qui logica per modificare i costi dinamicamente, se necessario
        return ac_tor

    def astar(self, state, lookahead):
        """Esegue una ricerca A* limitata"""

        # La frontiera è una lista di tuple, dove ogni tupla contiene:
        # - il costo totale f (somma di g + h),
        # - lo stato,
        # - la profondità della ricerca (numero di passaggi dal nodo iniziale).
        frontier = [(self.g.get(state,0) + self.H.get(state,self.problem.h(state)), state, 0)]  # (costo totale f, stato, profondità)

        # `explored` è un insieme di stati già esplorati.
        explored = set()

        # `closed_list` tiene traccia degli stati espansi durante la ricerca, che verranno usati per aggiornare le euristiche.
        closed_list = []

        # `g_scores` è un dizionario che contiene i valori g per ogni stato, cioè il costo accumulato per raggiungere lo stato dallo stato iniziale.
        # Lo stato iniziale ha g = 0.
        g_scores = {state: 0}

        # `s_bar` rappresenta lo stato che A* avrebbe espanso per ultimo, è l'ultimo stato esplorato o quello che sarebbe stato esplorato se non ci fosse stato il limite di lookahead.
        s_bar = None

        # Il ciclo continua fino a che ci sono stati nella frontiera e finché non abbiamo espanso il numero di stati definito da `lookahead`.
        while frontier and len(explored) < lookahead:
            # Ordina la frontiera in base al costo totale f = g + h. Questo garantisce che venga espanso prima lo stato con il costo stimato più basso.
            frontier.sort(key=lambda x: x[0])

            # Estrae lo stato con il costo f più basso dalla frontiera. Si rimuove dalla frontiera e si ottiene:
            # - il costo totale (ignorato con `_`),
            # - lo stato corrente da esplorare (`current_state`),
            # - la profondità della ricerca per questo stato (`current_depth`).
            _, current_state, current_depth = frontier.pop(0)

            # Se lo stato corrente è già stato esplorato, lo saltiamo e passiamo allo stato successivo.
            if current_state in explored:
                continue

            # Aggiungi lo stato corrente all'insieme degli stati esplorati.
            explored.add(current_state)

            # Aggiungi lo stato corrente alla lista degli stati espansi (closed list) per l'aggiornamento euristico successivo.
            closed_list.append(current_state)

            # Controlla se lo stato corrente è il goal. Se lo è, termina la ricerca e assegna `s_bar` a questo stato.
            if self.problem.goal_test(current_state):
                s_bar = current_state
                break  # Termina il ciclo perché il goal è stato trovato.

            # Se la profondità dell'espansione è inferiore al limite di `lookahead`, continua ad espandere i successori di `current_state`.
            if current_depth < lookahead:
                # Per ogni azione eseguibile nello stato corrente...
                for action in self.problem.actions(current_state):
                    # Calcola lo stato successivo risultante dall'esecuzione dell'azione.
                    next_state = self.problem.output(current_state, action)

                    # Calcola il costo tentativo g (tentative_g), cioè il costo per raggiungere `next_state` passando da `current_state`.
                    # Si ottiene sommando il costo g di `current_state` con il costo di eseguire l'azione che porta a `next_state`.
                    tentative_g = g_scores[current_state] + self.problem.c(current_state, action, next_state)

                    # Se `next_state` non è ancora stato esplorato (non è in `g_scores`), oppure se il nuovo percorso ha un costo g inferiore rispetto al valore attuale, aggiorna il costo g di `next_state`.
                    if next_state not in g_scores or tentative_g < g_scores[next_state]:
                        # Aggiorna o assegna il valore di g(next_state) con `tentative_g`.
                        g_scores[next_state] = tentative_g

                        # Calcola il costo totale f = g(next_state) + h(next_state), dove:
                        # - g(next_state) è il costo accumulato reale per raggiungere `next_state`,
                        # - h(next_state) è il valore dell'euristica, cioè la stima del costo rimanente per raggiungere il goal.
                        f_value = tentative_g + self.H.get(next_state, self.problem.h(next_state))

                        # Aggiungi `next_state` alla frontiera con il suo costo totale f e la profondità aumentata di 1.
                        frontier.append((f_value, next_state, current_depth + 1))

            # Aggiorna `s_bar` con lo stato che sarebbe stato espanso per ultimo.
            s_bar = current_state

        # Dopo aver terminato la ricerca (quando si esaurisce il lookahead o si trova il goal),
        # aggiorna `self.g` con i valori g trovati durante la ricerca per gli stati espansi.
        for state in closed_list:
            self.g[state] = g_scores.get(state, float('inf'))

        # Restituisce `s_bar` (lo stato che A* avrebbe espanso per ultimo) e `closed_list` (la lista degli stati espansi).
        return s_bar, closed_list


    def select_best_action(self, scurr, s_bar):
        """Seleziona l'azione con il minor costo per raggiungere s_bar"""
        best_action = None
        best_cost = float('inf')

        for action in self.problem.actions(scurr):
            next_state = self.problem.output(scurr, action)
            cost = self.problem.c(scurr, action, next_state) + self.H.get(next_state, self.problem.h(next_state))
            if cost < best_cost:
                best_cost = cost
                best_action = action

        return best_action
