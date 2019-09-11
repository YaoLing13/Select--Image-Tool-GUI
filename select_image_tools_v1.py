import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import glob
import cv2
import shutil

def get_imags(dir):
    images_1 = os.listdir(dir)
    images_1.sort()
    images = []
    for image in images_1:
        images.extend([dir + '/' + image])
    return images


class SelectImage(QMainWindow):

    def __init__(self, size_w, size_h, pos_w, pos_h, Title):
        super().__init__()
        self.src_dir = ''
        self.save_dir = ''
        self.del_dir = './del'
        self.key_value = -1
        self.initUI(size_w, size_h, pos_w, pos_h, Title)
        self.src_line = self.src_dir_text()
        self.btn_src_open_dir()
        self.save_line = self.save_dir_text()
        self.btn_save_open_dir()
        self.del_line = self.del_dir_text()
        self.btn_del_open_dir()
        self.btn_start()
        self.show()

    def initUI(self, size_w, size_h, pos_w, pos_h, Title):
        # self.setGeometry(pos_w,pos_h, size_w,size_h)
        # exitAction = QAction(QIcon('exit.jpeg'), '&Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(qApp.quit)

        self.resize(size_w, size_h)
        self.center()
        self.setWindowTitle(Title)
        self.setWindowIcon(QIcon('./icon/image.png'))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_push(self, name, s_w, s_h, p_w, p_h, tip=''):
        QToolTip.setFont(QFont('SansSerif', 10))
        button = QPushButton(name, self)
        button.setToolTip(tip)
        button.resize(s_w, s_h) # button size
        button.move(p_w, p_h,) # button position: W,H
        return button

    def set_text(self, s_w, s_h, p_w, p_h, holdtext=''):
        lineEdit = QLineEdit(self)
        lineEdit.resize(s_w, s_h)
        lineEdit.move(p_w, p_h)
        lineEdit.setPlaceholderText(holdtext)
        lineEdit.setEchoMode(QLineEdit.Normal)
        return lineEdit

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
    #          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def open_src_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "select file", "./")  # start file
        self.src_line.setText(directory)
        self.src_dir = directory

    def btn_src_open_dir(self):
        name = "Open Src Dir"
        s_w, s_h = 150, 30
        p_w, p_h = 30, 70
        tip = 'dir of source images'
        btn = self.button_push(name, s_w, s_h, p_w, p_h, tip)
        btn.clicked.connect(self.open_src_dir)


    def open_save_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "select file", self.src_dir)  # start file
        self.save_line.setText(directory)
        self.save_dir = directory

    def src_dir_text(self):
        s_w, s_h = 200, 30
        p_w, p_h = 200, 70
        holdtext = 'source dir'
        lineEdit = self.set_text(s_w, s_h, p_w, p_h, holdtext)
        lineEdit.setReadOnly(True)
        return lineEdit


    def btn_save_open_dir(self):
        name = "Open Save Dir"
        s_w, s_h = 150, 30
        p_w, p_h = 30, 120
        tip = 'dir of save images'
        btn = self.button_push(name, s_w, s_h, p_w, p_h, tip)
        btn.clicked.connect(self.open_save_dir)


    def save_dir_text(self):
        s_w, s_h = 200, 30
        p_w, p_h = 200, 120
        holdtext = 'save dir'
        lineEdit = self.set_text(s_w, s_h, p_w, p_h, holdtext)
        lineEdit.setReadOnly(True)
        return lineEdit


## delete file
    def open_del_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "select file", self.src_dir)  # start file
        self.del_line.setText(directory)
        self.del_dir = directory

    def del_dir_text(self):
        s_w, s_h = 200, 30
        p_w, p_h = 200, 170
        holdtext = 'source dir'
        lineEdit = self.set_text(s_w, s_h, p_w, p_h, holdtext)
        lineEdit.setReadOnly(True)
        return lineEdit


    def btn_del_open_dir(self):
        name = "Open Del Dir"
        s_w, s_h = 150, 30
        p_w, p_h = 30, 170
        tip = 'dir of del images'
        btn = self.button_push(name, s_w, s_h, p_w, p_h, tip)
        btn.clicked.connect(self.open_del_dir)



    def show_images(self, event):
        if (self.src_dir == ''):
            QMessageBox.warning(self, 'Message', "Please choose source directoty of images !")
        elif (self.save_dir == ''):
            QMessageBox.warning(self, 'Message', "Please choose source directoty of images !")
        elif (self.del_dir == './del'):
            QMessageBox.warning(self, 'Message', "del file is default: ./del")
        else:
            images = get_imags(self.src_dir)
            print("src_dir: %s " % self.src_dir)
            print("save_dir: %s " % self.save_dir)
            if not os.path.exists(self.del_dir):
                os.mkdir(self.del_dir)
            print("del_dir: %s " % self.del_dir)
            save_num = 0
            index = 0
            cv2.namedWindow("src", cv2.WINDOW_NORMAL)
            while True:
                img = cv2.imread(images[index])
                cv2.imshow("src", img)
                c = cv2.waitKey(0)
                # print(c)
                if c == 97:  ## last image - 'a'
                    index -= 1
                    if index < 0:
                        index = len(images)-1
                    else:
                        pass
                    continue
                if c == 32 or c == 115: # save image - 's' or 'Spave'
                    shutil.copy(images[index], self.save_dir)
                    save_num += 1
                    print("**** %d - dir: %s" % (save_num,images[index]))
                    index += 1
                    continue
                if c == 13: # next image- 'Enter'
                    print(images[index])
                    index += 1
                    if index > (len(images)-1):
                        index = 0
                    else:
                        pass
                    continue
                if c == 255: # delete image - 'Del'
                    print("*********delete: %s" % images[index])
                    # os.remove(images[index])
                    shutil.move(images[index], self.del_dir)
                    index += 1
                if c == 27: # Quit - 'ESC'
                    print("*********End: %s" % images[index])
                    print("Quit!")
                    cv2.destroyAllWindows()
                    break
            print("Save image: %d" % save_num)
        return


    def btn_start(self):
        name = "Begin"
        s_w, s_h = 100, 50
        p_w, p_h = 150, 220
        tip = 'Begin select'
        btn = self.button_push(name, s_w, s_h, p_w, p_h, tip)
        btn.clicked.connect(self.show_images)


if __name__ == '__main__':
    app = QApplication(sys.argv) # app instance
    # w = QWidget() # window instance
    # w.resize(960,640) ## windoe size: (W, H)
    # w.move(600, 300) ## (W, H): show window position (left top), if not parent win, desktop will be parent
    # w.setWindowTitle("Select images to save")  ## Window title
    # w.show() # show win
    se = SelectImage(450, 300, 600, 300, "Select images to save") # size_w, size_h, pos_w, pos_h
    sys.exit(app.exec_())
