import numpy as np;


# slot types
# 0 - nothing
# 1 - entry
# 2 - exit
# 3 - wall
# 4 - trap


class Labyrinthe:

    def __init__(self, mat_laby,list_rewards):

        self.laby = mat_laby
        self.rewards = list_rewards

    def load_labyrinthe(self,path_file):

        # open the selected file and separate its lines
        file = open(path_file, "r")
        file_lines = file.readlines()

        # read the labyrinth's dimensions and initializing
        header = file_lines[0].split(" ")
        nb_line = int(header[0])+2
        nb_col = int(header[1])+2
        self.laby = np.zeros((nb_line,nb_col))

        for line in file_lines[1:]:
            car_line = line.split(" ")
            self.laby[int(car_line[0])+1][int(car_line[1])+1]=int(car_line[2])

        #fill borders with walls
        for i in range(nb_col):
            self.laby[0][i]=3
            self.laby[nb_line-1][i] = 3
        for i in range(1,nb_line-1):
            self.laby[i][0] = 3
            self.laby[i][nb_col-1] = 3


    def get_moves(self,pos_x,pos_y):

        moves = []

        # if we are on a wall
        if(self.laby[pos_x][pos_y] == 3):
            return moves
        else :
            # check left
            if(self.laby[pos_x-1][pos_y] != 3):
                moves.extend([3])
            # checks right
            if (self.laby[pos_x+1][pos_y] != 3):
                moves.extend([1])
            # checks up
            if (self.laby[pos_x][pos_y+1] != 3):
                moves.extend([2])
            # checks down
            if (self.laby[pos_x][pos_y-1] != 3):
                moves.extend([0])
        return moves

    def move(self,pos_x,pos_y,dir):
        moves = self.get_moves(pos_x,pos_y)

        if dir in moves:
            # update position
            if (dir == 3):
                new_pos_x = pos_x - 1
                new_pos_y = pos_y
            if (dir == 1):
                new_pos_x = pos_x + 1
                new_pos_y = pos_y
            if (dir == 0):
                new_pos_x = pos_x
                new_pos_y = pos_y - 1
            if (dir == 2):
                new_pos_x = pos_x
                new_pos_y = pos_y + 1

            # assign reward
            new_type = self.laby[new_pos_x][new_pos_y]
            if (new_type == 0):
                reward = self.rewards[0]
            if (new_type == 1):
                reward = self.rewards[0]
            if (new_type == 2):
                reward = self.rewards[2]
            if (new_type == 3):
                reward = self.rewards[3]
            if (new_type == 4):
                reward = self.rewards[1]

            return reward, (new_pos_x,new_pos_y)
        else:
            return 0, (pos_x,pos_y)
