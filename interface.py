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
import QLearning as ql
import random
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

        self.scene = QtWidgets.QGraphicsScene(self.graphicsView_laby)
        self.graphicsView_laby.setScene(self.scene)
        self.pButton_FileSelect.clicked.connect(self.getFile_pBFS_clicked)
        self.pB_launch.clicked.connect(self.launch_algos)
        self.sendfileName.connect(self.display_laby)



        font_db = QtGui.QFontDatabase()
        font_id = QtGui.QFontDatabase.addApplicationFont("Font/Font Awesome 5 Pro-Solid-900.otf")
        family = font_db.applicationFontFamilies(font_id)
        self.my_font = QtGui.QFont(family[0])
        self.my_font.setPointSize(12)

        self.pos_robot = (0, 0);
        self.image_robot = QtWidgets.QGraphicsTextItem("\uf544")

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

        self.lab = Labyrinthe.Labyrinthe([], [])
        self.lab.load_labyrinthe(filepath)

        self.item_display_ref = []

        i = 0
        while (i < np.shape(self.lab.laby)[0]):
            j = 0
            temp = []
            while(j < np.shape(self.lab.laby)[1]):
                item = QtWidgets.QGraphicsRectItem(0, 0, 50, 50)
                if (self.lab.laby[i][j] == 1):
                    item.setBrush(QtGui.QColor('green'))
                    self.pos_robot = (i,j)

                if (self.lab.laby[i][j] == 2):
                    item.setBrush(QtGui.QColor('orange'))
                if (self.lab.laby[i][j] == 3):
                    item.setBrush(QtGui.QColor('black'))
                if (self.lab.laby[i][j] == 4):
                    item.setBrush(QtGui.QColor('red'))

                item.setPos(i*50,j*50)
                temp.append(item)
                self.scene.addItem(item)
                j+=1
            self.item_display_ref.append(temp)
            i+=1

        # item = self.item_display_ref[3][3]
        # item.setBrush(QtGui.QColor('purple'))

        # arrow down : \uf063
        # arrow left : \uf060
        # arrow right: \uf061
        # arrow up   : \uf062
        # robot      : \uf544



        self.image_robot.setPos(self.pos_robot[0] * 50 , self.pos_robot[1] * 50)
        self.image_robot.setFont(self.my_font)

        self.scene.addItem(self.image_robot)
        # # self.scene.update()
        # item = self.item_display_ref[5][5]
        # item.setBrush(QtGui.QColor('purple'))


    def update_pos_robot(self,probot, tab_Q):
        if probot != self.pos_robot :
            self.image_robot.setPos(probot[0],probot[1])


    def launch_algos(self):
        ql.QLearning.exploration(5000,0.5,self.lab,[-1,-25,100,-50],0.5,0)





App = QApplication(sys.argv)
interface = Interface("Interface/interface.ui")
sys.exit(App.exec())