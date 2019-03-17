import sys
from PyQt5.QtWidgets import QApplication
import interface

App = QApplication(sys.argv)
interface = interface.Interface("Interface/interface.ui")
sys.exit(App.exec())