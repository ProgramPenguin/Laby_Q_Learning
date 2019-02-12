import numpy as np;

class Labyrinthe:

    def __init__(self, mat_laby):

        self.laby = mat_laby

    def load_labyrinthe(self,path_file):

        # open the selected file and separate its lines
        file = open(path_file, "r")
        file_lines = file.readlines()

        # read the labyrinth's dimensions and initializing
        nb_line = file_lines[0][0]
        nb_col = file_lines[0][2]
        self.laby = np.zeros((int(nb_line),int(nb_col)))

        for line in file_lines[1:]:
            car_line = line.split(" ")
            self.laby[int(car_line[0])][int(car_line[1])]=int(car_line[2])


test = Labyrinthe([])
test.load_labyrinthe("data/test.txt")
print(test.laby)