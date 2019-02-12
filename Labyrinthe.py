import numpy as np;


# slot types
# 0 - nothing
# 1 - entry
# 2 - exit
# 3 - wall
# 4 - trap


class Labyrinthe:

    def __init__(self, mat_laby):

        self.laby = mat_laby

    def load_labyrinthe(self,path_file):

        # open the selected file and separate its lines
        file = open(path_file, "r")
        file_lines = file.readlines()

        # read the labyrinth's dimensions and initializing
        nb_line = int(file_lines[0][0])+1
        nb_col = int(file_lines[0][2])+1
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
                moves.extend(["left"])
            # checks right
            if (self.laby[pos_x+1][pos_y] != 3):
                moves.extend(["right"])
            # checks up
            if (self.laby[pos_x][pos_y+1] != 3):
                moves.extend(["down"])
            # checks down
            if (self.laby[pos_x][pos_y-1] != 3):
                moves.extend(["up"])
        return moves





test = Labyrinthe([])
test.load_labyrinthe("data/test.txt")
print(test.laby)
print(test.get_moves(1,2))