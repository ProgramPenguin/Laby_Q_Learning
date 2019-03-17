from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication
from PyQt5.QtCore import  pyqtSlot, pyqtSignal
from PyQt5.QtTest import QTest
import QLearning
import numpy as np
import sys
import Labyrinthe

class Interface(QDialog):

    sendfileName = pyqtSignal(str)

    def __init__(self, UiFilePath):
        super().__init__()
        loadUi(UiFilePath,self)
        self.setWindowTitle("Labyrinth")
        self.InitWindow()

        self.qlearn = QLearning.QLearning()

        self.lineEdit_gamma.setText("0.5")
        self.lineEdit_epsillon.setText("0.3")
        self.lineEdit_iteration.setText("5000")

        self.scene = QtWidgets.QGraphicsScene(self.graphicsView_laby)
        self.graphicsView_laby.setScene(self.scene)
        self.pButton_FileSelect.clicked.connect(self.getFile_pBFS_clicked)
        self.pB_launch.clicked.connect(self.up_clr_arrow)
        self.pB_launch.clicked.connect(self.exit_animation)
        self.pB_launch.clicked.connect(self.launch_algos)
        self.sendfileName.connect(self.display_laby)

        self.stopAlgo = True
        self.refreshRate = {}
        self.refreshRate[1] = 25
        self.refreshRate[2] = 50
        self.refreshRate[3] = 120
        self.refreshRate[4] = 750
        self.fp = False
        self.tab_arrow ={}
        self.clr_arw = 0  # on clear à 3

        font_db = QtGui.QFontDatabase()
        font_id = QtGui.QFontDatabase.addApplicationFont("Font/Font Awesome 5 Pro-Solid-900.otf")
        family = font_db.applicationFontFamilies(font_id)
        self.my_font = QtGui.QFont(family[0])
        self.my_font.setPointSize(12)

        self.pos_robot = (0, 0)
        self.pB_launch.setEnabled(False)

        self.lab = Labyrinthe.Labyrinthe([], [])


    def InitWindow(self):
        self.show()


    def getFile_pBFS_clicked(self):
        if self.stopAlgo == False:
            self.exit_animation()
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fn, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        self.sendfileName.emit(fn)


    @pyqtSlot(str)
    def display_laby(self,filepath):


        self.scene.clear()
        self.scene.update()
        self.tab_arrow = {}
        self.clr_arw = 0

        self.image_robot = QtWidgets.QGraphicsTextItem("\uf544")
        self.lab = Labyrinthe.Labyrinthe([], [])
        self.lab.load_labyrinthe(filepath)
        self.item_display_ref = []
        i = 0
        while (i < np.shape(self.lab.laby)[0]):
            j = 0

            while(j < np.shape(self.lab.laby)[1]):
                item = QtWidgets.QGraphicsRectItem(0, 0, 50, 50)
                item.setZValue(-1)
                text = QtWidgets.QGraphicsTextItem("")
                text.setZValue(1)

                # slot types
                # 0 - nothing
                # 1 - entry
                # 2 - exit
                # 3 - wall
                # 4 - trap
                if (self.lab.laby[i][j] == 0):
                    item.setBrush(QtGui.QColor('white'))
                if (self.lab.laby[i][j] == 1):
                    text = QtWidgets.QGraphicsTextItem("\uf6bb")
                    self.pos_robot = (i,j)
                if (self.lab.laby[i][j] == 2):
                    text = QtWidgets.QGraphicsTextItem("\uf024")
                if (self.lab.laby[i][j] == 3):
                    item.setBrush(QtGui.QColor('black'))
                if (self.lab.laby[i][j] == 4):
                    text = QtWidgets.QGraphicsTextItem("\uf06d")

                item.setPos(i*50,j*50)
                text.setPos(i*50 + 25,j*50 + 25)
                text.setFont(self.my_font)


                self.scene.addItem(item)
                self.scene.addItem(text)
                j+=1
            i+=1
        # robot      : \uf544
        self.image_robot.setPos(self.pos_robot[0] * 50 , self.pos_robot[1] * 50)
        self.image_robot.setFont(self.my_font)

        self.scene.addItem(self.image_robot)
        self.scene.update()
        self.pB_launch.setEnabled(True)


    def update_pos_robot(self,dataRob,dataQ_arrows):
        self.image_robot.setPos(dataRob[0]*50,dataRob[1]*50)
        self.pos_robot = dataRob

        #moves format : [up down left right]
        moves = self.lab.get_moves(self.pos_robot[0],self.pos_robot[1])
        val_q = dataQ_arrows[self.pos_robot[0]][self.pos_robot[1]]

        val_triee = []
        for i in moves:
            val_triee.append(val_q[i])
        mx = max(val_triee)

        if val_triee.count(mx) < 2:
            indice = 0
            for i in val_q:
                if i == mx:
                    break
                indice += 1
            if self.tab_arrow.__contains__((self.pos_robot[0],self.pos_robot[1])):
                arrow = self.tab_arrow.get((self.pos_robot[0],self.pos_robot[1]))
                self.scene.removeItem(arrow)
                self.scene.update()



            # arrow down : \uf063
            # arrow left : \uf060
            # arrow right: \uf061
            # arrow up   : \uf062
            if indice == 0:
                arrow = QtWidgets.QGraphicsTextItem("\uf062")
            if indice == 1:
                arrow = QtWidgets.QGraphicsTextItem("\uf063")
            if indice == 2:
                arrow = QtWidgets.QGraphicsTextItem("\uf060")
            if indice == 3:
                arrow = QtWidgets.QGraphicsTextItem("\uf061")

            arrow.setFont(self.my_font)
            arrow.setZValue(1)
            arrow.setPos(50*self.pos_robot[0]+25,50*self.pos_robot[1])
            self.tab_arrow[(self.pos_robot[0],self.pos_robot[1])]=arrow
            self.scene.addItem(arrow)


    def launch_algos(self):
        self.lab.rewards = [-1, -25, 100, -50]
        Q_tab = np.zeros((len(self.lab.laby), len(self.lab.laby[0]), 4))
        pos = self.lab.get_entries()[0]
        tab_moves = []
        historique = []
        nb_finish=0

        gamma = float(self.lineEdit_gamma.text())
        epsillon = float(self.lineEdit_epsillon.text())
        nb_iter = int(self.lineEdit_iteration.text())
        refRateVal = self.hS_disRate.value()

        ql = QLearning.QLearning()

        for nb_move in range(nb_iter):
            Q_tab, pos, historique, nb_finish = ql.exploration(Q_tab, pos, gamma, self.lab, epsillon, 1, historique, nb_finish)
            tab_moves.append(pos)

        self.label_score.setText("Score : " + str(nb_finish))
        self.update_affichage(tab_moves,self.refreshRate[refRateVal],Q_tab)



    def update_affichage(self,tab_moves,refresh_rate,tab_q):
        self.pB_launch.setText("Stop algorithm")
        i = 0
        while ((i < len(tab_moves))and(self.stopAlgo == False)):
            self.update_pos_robot(tab_moves[i],tab_q)
            QTest.qWait(refresh_rate)
            i += 1
        if(self.stopAlgo == False): #si on arrive a la fin de l'animation
            self.exit_animation()
            self.clr_arw +=1
        self.pB_launch.setText("Launch algorithm")


    def up_clr_arrow(self):
        self.clr_arw = self.clr_arw + 1


    def exit_animation(self):
        self.stopAlgo = not self.stopAlgo
        if self.clr_arw >= 3:
            self.clr_arw = 1
            self.clear_arrow()


    def clear_arrow(self):
        for i in self.tab_arrow:
            self.scene.removeItem(self.tab_arrow.get(i))
        self.scene.update()
        self.tab_arrow = {}


App = QApplication(sys.argv)
interface = Interface("Interface/interface.ui")
sys.exit(App.exec())