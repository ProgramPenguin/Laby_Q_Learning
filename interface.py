# from PyQt5.QtGui import QPixmap, QGuiApplication, QIcon ,QImage
# from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtWidgets import QDialog, QListWidgetItem, QListView, QListWidgetItem
# from PyQt5.uic import loadUi
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication
# import sys

from PyQt5 import QtWidgets, QtGui,Qt, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QFileDialog, QApplication, QGraphicsEllipseItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QRectF, QStringListModel
from PyQt5.QtTest import QTest
import QLearning
import random
import numpy as np
import sys
import Labyrinthe
import time

class Interface(QDialog):

    sendfileName = pyqtSignal(str)
    sendPos = pyqtSignal(object)

    def __init__(self, UiFilePath):
        super().__init__()
        loadUi(UiFilePath,self)
        self.setWindowTitle("Labyrinth")
        self.InitWindow()

        self.sendPos.connect(self.update_pos_robot)

        self.qlearn = QLearning.QLearning()

        self.lineEdit_gamma.setText("0.5")
        self.lineEdit_epsillon.setText("0.3")
        self.lineEdit_iteration.setText("5000")

        self.scene = QtWidgets.QGraphicsScene(self.graphicsView_laby)
        self.graphicsView_laby.setScene(self.scene)
        self.pButton_FileSelect.clicked.connect(self.getFile_pBFS_clicked)
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

        font_db = QtGui.QFontDatabase()
        font_id = QtGui.QFontDatabase.addApplicationFont("Font/Font Awesome 5 Pro-Solid-900.otf")
        family = font_db.applicationFontFamilies(font_id)
        self.my_font = QtGui.QFont(family[0])
        self.my_font.setPointSize(12)

        self.pos_robot = (0, 0)
        self.image_robot = QtWidgets.QGraphicsTextItem("\uf544")
        self.pB_launch.setEnabled(False)

        self.lab = Labyrinthe.Labyrinthe([], [])


    def InitWindow(self):
        self.show()

    def getFile_pBFS_clicked(self):
        options = QFileDialog.Options()

        options |= QFileDialog.DontUseNativeDialog
        fn, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        self.sendfileName.emit(fn)


    @pyqtSlot(str)
    def display_laby(self,filepath):

        if self.fp == False:
            self.scene.clear()
            self.scene.update()
            self.fp = True


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

        # arrow down : \uf063
        # arrow left : \uf060
        # arrow right: \uf061
        # arrow up   : \uf062
        # robot      : \uf544


        self.image_robot.setPos(self.pos_robot[0] * 50 , self.pos_robot[1] * 50)
        self.image_robot.setFont(self.my_font)

        self.scene.addItem(self.image_robot)
        self.scene.update()
        self.pB_launch.setEnabled(True)


    # @pyqtSlot(object)
    def update_pos_robot(self,dataRob):
        if dataRob != self.pos_robot :
            self.image_robot.setPos(dataRob[0]*50,dataRob[1]*50)
            self.pos_robot = dataRob


    def launch_algos(self):
        self.lab.rewards = [-1, -25, 100, -50]
        Q_tab = np.zeros((len(self.lab.laby), len(self.lab.laby[0]), 4))
        pos = self.lab.get_entries()[0]
        tab_moves = []

        gamma = float(self.lineEdit_gamma.text())
        epsillon = float(self.lineEdit_epsillon.text())
        nb_iter = int(self.lineEdit_iteration.text())
        refRateVal = self.hS_disRate.value()

        ql = QLearning.QLearning()

        for nb_move in range(nb_iter):
            Q_tab, pos = ql.exploration(Q_tab, pos, gamma, self.lab, epsillon, 0,[1, 2, 3, 0])
            tab_moves.append(pos)

        self.update_affichage(tab_moves,self.refreshRate[refRateVal])



    def update_affichage(self,tab_moves,refresh_rate):
        self.pB_launch.setText("Stop algorithm")

        i = 0


        while ((i < len(tab_moves))and(self.stopAlgo == False)):

            self.update_pos_robot(tab_moves[i])
            QTest.qWait(refresh_rate)
            i += 1
        if(self.stopAlgo == False):
            self.exit_animation()

        self.pB_launch.setText("Launch algorithm")

    def exit_animation(self):
        self.stopAlgo = not self.stopAlgo

App = QApplication(sys.argv)
interface = Interface("Interface/interface.ui")
sys.exit(App.exec())