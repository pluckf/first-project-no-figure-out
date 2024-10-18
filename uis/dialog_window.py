from PyQt5.QtWidgets import  QPushButton, QDialog, QVBoxLayout
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# 创建一个弹出的对话框类
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()