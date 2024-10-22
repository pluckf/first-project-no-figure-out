import random
from PyQt5.QtWidgets import QPushButton, QDialog, QVBoxLayout
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 创建一个弹出的对话框类
class PicWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 创建主窗口
        mainWidget = QWidget()
        self.setGeometry(200, 200, 800, 600)
        self.setCentralWidget(mainWidget)
        layout = QVBoxLayout()
        mainWidget.setLayout(layout)
        self.data = None
        # 创建画布
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)

    def set_data(self, data):
        self.data = data

    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.data)
        self.canvas.draw()



