# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'view.ui'
# Created by: PyQt5 UI code generator 5.13.0
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2
import random
Colors = ["Red" , "Black", "Blue", "Gray"]
size = len(Colors)

bounds = {
    "red": ([17, 15, 100], [50, 56, 200]),
    "blue": ([86, 31, 4], [220, 88, 50]),
    "gray": ([103, 86, 65], [145, 133, 128]),
    "black": ([1,1,1] , [40,40,40])
}

# Filter pixels so determine the arrow using color boundaries
# Note our step is 4 pixels not 1... The point is to make the game more smooth
def filtre(frame, bounds):
    l = list()
    lower = np.array(bounds[0], dtype = "uint8")
    upper = np.array(bounds[1], dtype = "uint8")
    size1 = len(frame)
    size2 = len(frame[0])
    for i in range(0, size1, 4):
        for j in range(0, size2, 4):
            if (frame[i][j] > lower).all() and (frame[i][j] < upper).all():
                l.append((i,j))
    return l

# Find the center of the arrow determined by filter function
def centroid(frame, bounds):
    points = filtre(frame, bounds)
    x_coords = list()
    y_coords = list()
    for i in points:
        x_coords.append(i[0])
        y_coords.append(i[1])
    _len = len(points)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [round(centroid_x), round(centroid_y)]

# our mouse is placed on the grid, We consider it the point (0, 0) since he is the
# center of the movement. this function serves to prepare for the function translation
# cause we want to determine the direction from POV of the mouse meaning from point (0, 0)
def det_trans(og, new):
    return ( (og[0] - new[0]), (og[1] - new[1]) )

# Using this function we determine the translation ray hence direction of the arrow
# using the center of the its head.
def translation(ray, head_pt):
    return (head_pt[0] + ray[0], head_pt[1] + ray[1])

# well loading the mouse on a white grid
mouse = cv2.imread("Sv.png", cv2.IMREAD_COLOR);
image = QtGui.QImage(mouse, mouse.shape[1], mouse.shape[0], mouse.strides[0], QtGui.QImage.Format_RGB888)

# game over 
game = cv2.imread("g.png", cv2.IMREAD_COLOR);

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1059, 799)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.graphicsScene = QtWidgets.QGraphicsScene(self.centralwidget)
        self.graphicsPixmapItem = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("Sv.png").scaled(52,52))
        self.graphicsPixmapItem.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.graphicsScene.addItem(self.graphicsPixmapItem)

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 150, 1061, 601))
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setScene(self.graphicsScene)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(840, 90, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(840, 40, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(130, 40, 73, 22))
        self.comboBox.setObjectName("comboBox")
        for i in range(0, size):
            self.comboBox.addItem(Colors[i])

        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(330, 40, 73, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        for i in range(0, size):
            self.comboBox_2.addItem(Colors[i])

        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(330, 90, 73, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        for i in range(1, 5):
            self.comboBox_3.addItem(str(i))

        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(130, 90, 73, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.targets = dict()
        for i in range(0, 11):
            self.comboBox_4.addItem(str(i))
        self.Obstacles = dict()

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 40, 81, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 40, 91, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(270, 90, 51, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 90, 91, 20))
        self.label_4.setObjectName("label_4")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1059, 26))
        self.menubar.setObjectName("menubar")
        self.menuAide = QtWidgets.QMenu(self.menubar)
        self.menuAide.setObjectName("menuAide")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionHow_to = QtWidgets.QAction(MainWindow)
        self.actionHow_to.setObjectName("actionHow_to")
        self.actionRead_me = QtWidgets.QAction(MainWindow)
        self.actionRead_me.setObjectName("actionRead_me")

        self.menuAide.addSeparator()
        self.menuAide.addAction(self.actionHow_to)
        self.menuAide.addAction(self.actionRead_me)
        self.menubar.addAction(self.menuAide.menuAction())
        self.x_offset = 0
        self.y_offset = 0
        self.mousepos = [(self.x_offset + i, self.y_offset + j) for i in range(52) for j in range(52)]
        self.pas = 0
        self.toe = "Black"
        self.head = "Red"
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start(self):
        # launch the video capture
        self.cap = cv2.VideoCapture(0)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter('test.avi', self.fourcc, 30.0, (640,480))

        while(self.cap.isOpened()):
            # reading each image and flipping it since its reversed
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)                    

            center_1 = center_2 = center = (0, 0)
            try:
                # calculate the center of the head of the arrow
                center_1 = centroid(frame, bounds[self.head.lower()])
                # calculate the center of the toe of the arrow
                center_2 = centroid(frame, bounds[self.toe.lower()])
                # calculate the center of arrow as whole
                center = (round((center_1[0] + center_2[0]) / 2), round((center_1[1] + center_2[1]) / 2))
            except Exception as e:
                pass
            # calculate the direction of the 
            ray = det_trans((0, 0), center)
            # determining the center of arrow's head from mouse POV.
            center_11 = translation(ray, center_1)
            # self pas serves to determine the speed at which the mouse moves with
            # we set 20 as the "slowest limit of the speed", its division so look at it other way 
            direction = (round(center_11[0] / (20 - self.pas)), round(center_11[1] / (20 - self.pas)))
            # get the new mouse position
            self.x_offset = self.x_offset + direction[1]
            self.y_offset = self.y_offset + direction[0]
            self.mousepos = [(self.x_offset + i, self.y_offset + j) for i in range(52) for j in range(52)]
            # update the mouse position on the pixelmap
            self.graphicsPixmapItem.setPos(self.x_offset, self.y_offset)
            # Check if the new position touches the edges of the good cheese
            for fermaga in self.targets.keys():
                x = fermaga[0]
                y = fermaga[1]
                d = 0
                edges_good_cheese = [(x, y), (x + 52, y), (x , y + 52), ( x + 52, y + 52)]
                for i in self.mousepos:
                    if i in edges_good_cheese:
                        self.graphicsScene.removeItem(self.targets[fermaga])
                        self.targets.pop(fermaga)
                        d = 1
                        break
                if d == 1:
                    break
            # Check if the new position touches the edges of the bad cheese
            for fermagapoop in self.Obstacles.keys():
                x = fermagapoop[0]
                y = fermagapoop[1]
                d = 0
                edges_bad_cheese = [(x, y), (x + 52, y), (x , y + 52), ( x + 52, y + 52)]
                for i in self.mousepos:
                    if i in edges_bad_cheese:
                        self.graphicsScene.removeItem(self.graphicsPixmapItem)
                        self.graphicsPixmapItem.setPos(0, 0)
                        self.graphicsScene.addItem(self.graphicsPixmapItem)
                        self.x_offset = 0
                        self.y_offset = 0
                        d = 1
                        cv2.imshow("gameover", game)
                        break
                if d == 1:
                    break

            if ret==True:
                cv2.imshow("camera", frame)
                self.writer.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    def stop(self):
        # empty the whole map
        for i in list(self.targets.keys()):
            self.graphicsScene.removeItem(self.targets[i])
            self.targets.pop(i)
        for i in list(self.Obstacles.keys()):
            self.graphicsScene.removeItem(self.Obstacles[i])
            self.Obstacles.pop(i)

        tts = int(self.comboBox_4.currentText())
        for i in range(0, tts):
            s = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("c.png").scaled(52,52))
            s1 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("c1.png").scaled(52,52))

            x = random.randrange(-530, 530)
            y = random.randrange(-300, 300)
            x1 = random.randrange(-530, 530)
            y1 = random.randrange(-300, 300)
            self.targets[(x, y)] = s 
            self.Obstacles[(x1, y1)] = s1
            s.setPos(x, y)
            s1.setPos(x1, y1)
            self.graphicsScene.addItem(s)
            self.graphicsScene.addItem(s1)

        self.graphicsScene.removeItem(self.graphicsPixmapItem)
        self.graphicsPixmapItem.setPos(0, 0)
        self.graphicsScene.addItem(self.graphicsPixmapItem)
        self.x_offset = 0
        self.y_offset = 0
        try:
            self.cap.release()
            self.writer.release()
            cv2.destroyAllWindows()
        except:
            pass
    
    # UI selection of toe color
    def first(self):
        self.toe = self.comboBox.currentText()
    
    # UI selection of head color
    def second(self):
        self.head = self.comboBox_2.currentText()

    # UI selection of speed
    def third(self):
        self.pas = int(self.comboBox_3.currentText())

    # UI selection of number of obstacles/targets
    def fourth(self):
        for i in list(self.targets.keys()):
            self.graphicsScene.removeItem(self.targets[i])
            self.targets.pop(i)

        tts = int(self.comboBox_4.currentText())
        for i in range(0, tts):
            s = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("c.png").scaled(52,52))
            s1 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("c1.png").scaled(52,52))

            x = random.randrange(-530, 530)
            y = random.randrange(-300, 300)
            x1 = random.randrange(-530, 530)
            y1 = random.randrange(-300, 300)
            self.targets[(x, y)] = s 
            self.Obstacles[(x1, y1)] = s1
            s.setPos(x, y)
            s1.setPos(x1, y1)
            self.graphicsScene.addItem(s)
            self.graphicsScene.addItem(s1)
    
    # function to use for combo box 4 in case you dont want any obstacles on the map
    def fifth(self):
        for i in list(self.targets.keys()):
            self.graphicsScene.removeItem(self.targets[i])
            self.targets.pop(i)

        tts = int(self.comboBox_4.currentText())
        for i in range(0, tts):
            s = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap("c.png").scaled(52,52))
            x = random.randrange(-530, 530)
            y = random.randrange(-300, 300)
            self.targets[(x, y)] = s 
            s.setPos(x, y)
            self.graphicsScene.addItem(s)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Stop/Reset"))
        self.pushButton.clicked.connect(self.stop)

        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.clicked.connect(self.start)

        self.comboBox.activated.connect(self.first)
        self.comboBox_2.activated.connect(self.second)
        self.comboBox_3.activated.connect(self.third)
        # use self.fifth if you dont want any obstacles on the map
        self.comboBox_4.activated.connect(self.fourth)

        self.label.setText(_translate("MainWindow", "born inf color:"))
        self.label_2.setText(_translate("MainWindow", "born sup color:"))
        self.label_3.setText(_translate("MainWindow", "vitesse:"))
        self.label_4.setText(_translate("MainWindow", "trgts / obs:"))

        self.menuAide.setTitle(_translate("MainWindow", "Aide !"))
        self.actionHow_to.setText(_translate("MainWindow", "How to ?"))
        self.actionRead_me.setText(_translate("MainWindow", "Read me !"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())