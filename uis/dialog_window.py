import sys
import random
from PyQt5.QtWidgets import  QPushButton, QDialog, QVBoxLayout
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 创建一个弹出的对话框类
class PicWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data=[0]*50

        #创建主窗口
        mainWidget = QWidget()
        self.setGeometry(200,200,800,600)
        self.setCentralWidget(mainWidget)
        layout = QVBoxLayout()
        mainWidget.setLayout(layout)


        #测试按钮
        self.button = QPushButton("点我")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.open_serial_port)
        #创建画布
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)
        #创建定时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)

    def update_plot(self):
        value = random.randint(0, 100)
        if len(self.data) <= 10000:
            self.data = self.data + [value]  # 更新数据
        else:
            self.data = self.data[1:] + [value]
        self.ax.clear()
        self.ax.plot(self.data)
        self.canvas.draw()

    def open_serial_port(self):
        self.timer.start(50)

