import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import threading
import time
import serial
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

from scipy.constants import value

from save_data import *
from uis.dialog_window import PicWindow
from PyQt5.QtCore import QThread


class WorkerThread(QThread):
    data_ready = pyqtSignal(list)
    def __init__(self, serial_port,nums):
        super().__init__()
        self.running = False
        self.buff = []
        self.nums=nums
        self.serial_port = serial_port
        for i in range(self.nums):
            self.buff.append([])
    def run(self):
        while self.running:
            if self.serial_port:
                try:
                    if self.serial_port.isOpen():
                        data = self.serial_port.readline().decode().strip()
                        if data:
                            data = data[2:]
                            data = data[0:-2]
                            data=data.split(',')
                            for i in range(self.nums):
                                _value=float(data[i])
                                if len(self.buff[i]) <= 10000:
                                    self.buff[i] += [_value]
                                else:
                                    self.buff[i] = self.buff[1:]
                                    self.buff[i] += [_value]
                            self.data_ready.emit(self.buff)
                except:
                    self.stop_thread()
    def start_thread(self):
        self.running = True
        if not self.isRunning():
            self.start()

    def stop_thread(self):
        self.running = False


class PortBox(QComboBox):
    def showPopup(self):
        super().showPopup()
        self.popup_shown.emit()  # 发射自定义信号

    popup_shown = pyqtSignal()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pic_list = []
        self.data = []
        self.buff=[]
        self.setWindowTitle("串口数据可视化")
        self.setGeometry(100, 100, 1000, 800)
        self.serial_port = None
        self.cnt = 0
        self.bits = ["115200", "2400", "4800", "9600", "19200", "38400", "57600"]
        self.last_data = []
        self.t = None
        self.nums=0
        # 初始化数据缓冲区
        # 主控件
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)

        # 布局
        layout = QVBoxLayout()
        mainWidget.setLayout(layout)

        # 串口选择下拉菜单
        self.combobox = PortBox()
        layout.addWidget(self.combobox)
        self.combobox.popup_shown.connect(self.update_ports)

        self.bit_cm = QComboBox()
        layout.addWidget(self.bit_cm)
        self.update_bit()

        # 打开串口按钮
        self.button = QPushButton("打开串口")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.open_serial_port)

        # 保存数据按钮
        # self.save_button = QPushButton("保存数据")
        # layout.addWidget(self.save_button)
        # self.save_button.clicked.connect(self.save_data)

        # 用于显示数据的Matplotlib图表
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)
        #创建一个传输数据的定时器，每隔30ms更新一次数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)

        # 将串口添加到拉选框中
        self.ports = serial.tools.list_ports.comports()
        for port in self.ports:
            self.combobox.addItem(port.device)

    def update_bit(self):
        for bit in self.bits:
            self.bit_cm.addItem(bit)

    def update_ports(self):
        # 更新串口号
        ports = serial.tools.list_ports.comports()
        self.combobox.clear()
        for port in ports:
            self.combobox.addItem(port.device)

    def open_serial_port(self):
        self.cnt+=1
        if not self.serial_port:
            port = self.combobox.currentText()
            bit = self.bit_cm.currentText()
            try:
                self.serial_port = serial.Serial(port=port,baudrate=bit, timeout=3)
            except:
                print("弹出错误窗口")
            if self.serial_port:
                print("打开成功")
            else:
                print("打开失败")
            #根据数据个数声明数据
            if self.cnt==1:
                if self.serial_port.isOpen():
                    data = self.serial_port.readline().decode().strip()
                    print("开始读取数据")
                    # 读取数据确定数据长度
                    if data:
                        data = data[2:]
                        data = data[0:-2]
                        data = data.split(",")
                        self.nums = len(data)
                for i in range(self.nums):
                    self.last_data.append([])
                    self.data.append([])
                    self.buff.append([])
            self.t = WorkerThread(self.serial_port, self.nums)
            self.t.data_ready.connect(self.handle_data)
            self.t.start_thread()
            self.button.setText("关闭串口")
            #有几个数据就创建几个窗口
            for i in range(self.nums):
                self.pic_list.append(PicWindow())
                self.pic_list[i].show()
            self.timer.start(30)

        else:
            self.button.setText("打开串口")
            for i in range(self.nums):
                self.last_data[i] = self.pic_list[i].data
                self.pic_list[i].close()
            self.t.stop_thread()
            self.t.wait()
            self.pic_list.clear()
            self.serial_port.close()
            self.serial_port = None
            self.timer.stop()

    def handle_data(self, buff):
        self.buff = buff
    def update_data(self):
        for i in range(self.nums):
            self.data[i] = self.last_data[i]+self.buff[i]
            self.pic_list[i].set_data(self.data[i])
            self.pic_list[i].update_plot()
    def save_data(self):
        write_data(self.data)



