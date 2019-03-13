import Labyrinthe as lb
import random
import numpy as np

def get_entries(lab):
    nb_lig = len(lab.laby)
    nb_col = len(lab.laby[0])
    list_entries = []

    for i in range(1,nb_lig-1):
        for j in range(1, nb_col - 1):
            if(lab.laby[i][j] == 1):
                list_entries.append((i,j))

    return list_entries


def exploration(nb_max_move,gamma,lab,rewards,epsilon,backtrack):

    lab.rewards = rewards
    entries = get_entries(lab)
    pos = entries[0]

    # Pour une case de Q_tab : [qHaut, qDroite, qBas,qGauche]
    Q_tab = np.zeros((len(lab.laby), len(lab.laby[0]), 4))

    if backtrack != 0:
        historique_moves = []  # historique des mouvements depuis la dernier depart

    for nb_move in range(nb_max_move):

        # On obtient les mouvements possibles
        moves = lab.get_moves(pos[0],pos[1])

        # On choisit au hasard de façon pondere si on explore ou on exploite
        choix_exp = random.random() # va de 0 a 1
        if 0.0 < choix_exp < epsilon:
            # Exploration
            selected_index = random.randint(0, len(moves)-1)
        else:
            # Exploitation
            # On recupere les valeurs de Q pour la case
            Q_moves = Q_tab[pos[0]][pos[1]]
            # On recupere les valeurs max de Q pour la case
            Q_moves_max = np.where(Q_moves == max(Q_moves[moves]))
            # On choisit une action au hasard parmis celles avec Q maximal
            selected_index = Q_moves_max[0][random.randint(0,len(Q_moves_max[0])-1)]

        r, new_pos = lab.move(pos[0],pos[1],selected_index)
        Q_tab[pos[0]][pos[1]][selected_index] = r + gamma * max(Q_tab[new_pos[0]][new_pos[1]])

        # MaJ de l'historique
        if backtrack != 0:
            historique_moves.append([pos[0],pos[1],selected_index])

        # Si on arrive a la sortie, on repart a l'entree
        if lab.laby[new_pos[0]][new_pos[1]] == 2:
            new_pos = entries[0]

            # On effectue le backtracking
            if backtrack != 0:
                val_a_repartir = Q_tab[pos[0]][pos[1]][selected_index]

                # creation de la liste des coefficients a appliquer pour repartir Q de facon decroissante
                coefs = []
                coefs.append(2 ** -(len(historique_moves)+1))
                for i in range(len(historique_moves),0,-1):
                    coefs.append(2**(-i))

                i = 0
                for case in historique_moves:
                    Q_tab[case[0]][case[1]][case[2]] = val_a_repartir*coefs[i]
                    i+=1

                historique_moves = []

        pos = new_pos
    print(Q_tab)
    return Q_tab




test = lb.Labyrinthe([],[])
test.load_labyrinthe("data/test.txt")
print(test.laby)
exploration(5000,0.5,test,[-1,-25,100,-50],0.5,0)