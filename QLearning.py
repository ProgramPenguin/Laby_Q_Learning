import Labyrinthe as lb
import random
import numpy as np

class QLearning :

    def backtrack(self,Q_tab,historique,reward,lab):
        # Calcul de la recompense a ajouter à chaque case
        reward_case = reward/len(historique)

        for move in historique:
            Q_tab[move[0]][move[1]][move[2]] = Q_tab[move[0]][move[1]][move[2]] + reward_case

        return Q_tab



    def exploration(self,Q_tab,pos,gamma,lab,epsilon,backtrack,historique,nb_finish):

        new_Q_tab = Q_tab.copy()

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
            selected_index = moves_max[random.randint(0,len(moves_max)-1)]

        r, new_pos = lab.move(pos[0],pos[1],selected_index)
        historique.append((pos[0],pos[1],selected_index))

        new_pos_moves = lab.get_moves(new_pos[0],new_pos[1])
        new_Q_tab[pos[0]][pos[1]][selected_index] = r + gamma * max(Q_tab[new_pos[0]][new_pos[1]][new_pos_moves])
        test = new_Q_tab[pos[0]][pos[1]]
        if(test[selected_index] > 0):
            print()
        Q_case = new_Q_tab[pos[0]][pos[1]].copy()
        # Si on arrive a la sortie, on repart a l'entree
        if lab.laby[new_pos[0]][new_pos[1]] == 2:
            nb_finish+=1
            new_pos = lab.get_entries()[0]
            if(backtrack != 0):
                self.backtrack(new_Q_tab,historique,r,lab)
                historique = []

        return new_Q_tab, new_pos, historique, nb_finish, Q_case
