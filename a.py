import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout

class MyComboBox(QComboBox):
    def showPopup(self):
        super().showPopup()
        self.popup_shown.emit()  # 发射自定义信号

    popup_shown = pyqtSignal()  # 定义一个自定义信号

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个自定义的下拉框
        self.comboBox = MyComboBox(self)
        self.comboBox.addItem("Option 1")
        self.comboBox.addItem("Option 2")
        self.comboBox.addItem("Option 3")

        # 创建布局并添加下拉框
        layout = QVBoxLayout(self)
        layout.addWidget(self.comboBox)

        # 连接自定义信号和槽
        self.comboBox.popup_shown.connect(self.onShowPopup)

    def onShowPopup(self):
        # 当下拉框被点击并显示下拉列表时，这个方法会被调用
        print("下拉框被点击，下拉列表显示。")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
