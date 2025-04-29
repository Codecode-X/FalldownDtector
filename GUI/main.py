import shutil
import sys
import os
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtWidgets import QMainWindow, QFileDialog
from PySide2.QtGui import QImageReader
from mainwindow import Ui_MainWindow
import detect

# 常量和变量
EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMES = 2
MAR_THRESH = 0.65
MOUTH_AR_CONSEC_FRAMES = 3
COUNTER = 0
TOTAL = 0
mCOUNTER = 0
mTOTAL = 0
ActionCOUNTER = 0
Roll = 0
Rolleye = 0
Rollmouth = 0


# 常量
current_dir = os.path.dirname(os.path.abspath(__file__))
source = os.path.join(current_dir, "input.jpg")
save_path = os.path.join(current_dir, "output.jpg")
pt_path = os.path.join(current_dir, "best.pt")

# 定义主窗口类
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.f_type = 0

    # 初始化窗口
    def window_init(self):
        # 设置标签和菜单的初始文本
        self.menu.setTitle("菜单")
        self.detect_bt.setText("检测")

        # 绑定点击事件和触发事件
        self.imgLabel.clicked.connect(self.upload_img)  # 图像 label
        self.detect_bt.triggered.connect(self.detect)
        self.imgLabel.setScaledContents(True)

        # 设置背景颜色
        self.setStyleSheet("background-color: Dark;")

    def upload_img(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "选择图像文件", "", "Images (*.png *.jpg *.bmp);;All Files (*)",
                                                   options=options)
        if file_name:
            # 将图像复制到保存的目录
            shutil.copyfile(file_name, source)
            print(f"图像已保存到：{source}")
            pixmap = QtGui.QPixmap(file_name)
            self.imgLabel.setPixmap(pixmap.scaled(self.imgLabel.size()))

    def detect(self):
        result = detect.detect_down(source, save_path, pt_path)
        if result:
            pixmap = QtGui.QPixmap(save_path)
            self.imgLabel.setPixmap(pixmap.scaled(self.imgLabel.size()))
            window.printf("------------检测结果解释--------------")
            window.printf("检测到有人跌倒！！！")
            window.printf("-----------------------------------")
            return True
        else:
            pixmap = QtGui.QPixmap(save_path)
            self.imgLabel.setPixmap(pixmap.scaled(self.imgLabel.size()))
            window.printf("------------检测结果解释--------------")
            window.printf("~~~安全~~~")
            window.printf("-----------------------------------")
            return True


# 主程序入口
if __name__ == '__main__':
    QImageReader.supportedImageFormats()  # 支持的图像格式
    app = QtWidgets.QApplication(sys.argv)  # 创建应用程序对象
    app.addLibraryPath(os.path.join(os.path.dirname(QtCore.__file__), "plugins"))  # 添加库路径
    window = MainWindow()  # 创建主窗口
    window.window_init()  # 初始化主窗口
    window.show()  # 显示主窗口
    sys.exit(app.exec_())  # 运行应用程序
