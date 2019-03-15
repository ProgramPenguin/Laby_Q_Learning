import Labyrinthe as lb
import random
import numpy as np

class QLearning :

    def exploration(self,Q_tab,pos,gamma,lab,epsilon,backtrack,politique):

        new_Q_tab = Q_tab

        # On obtient les mouvements possibles
        moves = lab.get_moves(pos[0],pos[1])
        # On choisit au hasard de façon pondere si on explore ou on exploite
        choix_exp = random.random() # va de 0 a 1
        if 0.0 < choix_exp < epsilon:
            # Exploration
            selected_index = moves[random.randint(0, len(moves)-1)]
        else:
            # Exploitation
            # On recupere les valeurs de Q pour la case
            Q_moves = Q_tab[pos[0]][pos[1]]
            # On recupere les valeurs max de Q pour la case
            Q_moves_max = np.where(Q_moves == max(Q_moves[moves]))

            moves_max = []
            for case in Q_moves_max[0]:
                if case in moves:
                    moves_max.append(case)

            # # On choisit une action au hasard parmis celles avec Q maximal
            # selected_index = Q_moves_max[0][random.randint(0,len(Q_moves_max[0])-1)]
            # On choisit l'action a faire en suivant la politique parmis les Q maximal
            j = 0
            selected_index = politique[j]
            while (not selected_index in moves_max):
                selected_index = politique[j]
                j+=1

        r, new_pos = lab.move(pos[0],pos[1],selected_index)

        new_pos_moves = lab.get_moves(new_pos[0],new_pos[1])
        new_Q_tab[pos[0]][pos[1]][selected_index] = r + gamma * max(Q_tab[new_pos[0]][new_pos[1]][new_pos_moves])
        # Si on arrive a la sortie, on repart a l'entree
        if lab.laby[new_pos[0]][new_pos[1]] == 2:
            new_pos = lab.get_entries()[0]

        return new_Q_tab, new_pos