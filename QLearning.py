import Labyrinthe as lb
from random import randint
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

def exploration(nb_max_move,gamma,lab,rewards):

    lab.rewards = rewards
    entries = get_entries(lab)
    pos = entries[0]

    #Pour une case de Q_tab : [qHaut, qDroite, qBas,qGauche]
    Q_tab = np.zeros((len(lab.laby), len(lab.laby[0]), 4))

    for nb_move in range(nb_max_move):

        moves = lab.get_moves(pos[0],pos[1])
        Q_moves = Q_tab[pos[0]][pos[1]]
        Q_moves_max = np.where(Q_moves == max(Q_moves[moves]))
        selected_index = Q_moves_max[0][randint(0,len(Q_moves_max[0])-1)]

        r, new_pos = lab.move(pos[0],pos[1],selected_index)
        Q_tab[pos[0]][pos[1]][selected_index] = r + gamma * max(Q_tab[new_pos[0]][new_pos[1]])
        pos = new_pos
        nb_move = nb_move +1
    return Q_tab




test = lb.Labyrinthe([],[])
test.load_labyrinthe("data/test.txt")
print(test.laby)
exploration(5000,0.5,test,[-1,-25,100,-50])