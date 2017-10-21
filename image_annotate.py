# -*- coding: utf-8 -*-

import sys
import cv2
import numpy as np
from scipy import interpolate
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



class MainWindow(QMainWindow):
    def __init__(self, img_path):
        super(QMainWindow, self).__init__()
        self.img_path = img_path
        self.showWidget = QWidget()
        # left sub window
        self.dirUpdate = QPushButton('update', self.showWidget)
        self.totalLabel = QLabel(self.showWidget)
        self.currentLabel = QLabel(self.showWidget)

        self.dirLE = QLineEdit(self.showWidget)
        self.totalNum = QLabel(self.showWidget)
        self.currentNum = QLabel(self.showWidget)

        self.previousBT = QPushButton('previous', self.showWidget)
        self.nextBT = QPushButton('next', self.showWidget)

        self.saveBT = QPushButton('save', self.showWidget)
        self.quitBT = QPushButton('quit', self.showWidget)

        # right
        # right up
        self.resultLabel = QLabel('result', self.showWidget)
        self.resultLW = QListWidget(self.showWidget)
        # right bottom
        self.boundingBT = QPushButton('bounding', self.showWidget)
        self.pointBT = QPushButton('point', self.showWidget)
        self.fittingBT = QPushButton('fitting', self.showWidget)
        self.zoomSLD = QSlider(Qt.Horizontal, self.showWidget)

        #mem var
        self.point1 = (0, 0)
        self.point2 = (0, 0)
        self.point_list_zoom = []
        self.point_list_ori = []
        self.fitting_point_list = []
        self.bounding_img = None
        self.ori_img = None
        self.zoom_ratio = 1
        self.bounding_coor = None
        self.bounding_winna = 'bounding'
        self.ori_winna = 'ori'
        self.point_winna = 'point'
        self.fitting_winna = 'fitting'

        self.init_ui()
        self.load_img()
        self.event_set()

    def load_img(self):
        self.ori_img = cv2.imread(self.img_path)
        if self.ori_img is None:
            self.statusBar().showMessage('Ready')
            sys.exit(1)

        cv2.imshow('ori',self.ori_img)
        self.bounding_img = self.ori_img
        self.dirLE.setText(self.img_path)


    def init_ui(self):
        self.totalLabel.setText('total:')
        self.currentLabel.setText('current:')
        self.totalNum.setNum(0)
        self.currentNum.setNum(0)
        #setting
        self.boundingBT.setCheckable(True)
        self.pointBT.setCheckable(True)
        self.fittingBT.setCheckable(True)

        #layout
        self.dirUpdate.setFont(QFont("Helvetica", 16, QFont.Black))
        #self.dirUpdate.setAlignment(Qt.AlignBottom)
        self.dirLE.setFont(QFont("Helvetica", 12, QFont.Normal))
        self.totalLabel.setAlignment(Qt.AlignBottom)
        self.totalLabel.setFont(QFont("Helvetica", 14, QFont.Black))
        self.currentLabel.setAlignment(Qt.AlignBottom)
        self.currentLabel.setFont(QFont("Helvetica", 14, QFont.Black))
        pe = QPalette()
        pe.setColor(QPalette.Window, Qt.blue)
        pe.setColor(QPalette.WindowText, Qt.white)
        self.totalNum.setAutoFillBackground(True)
        self.totalNum.setFont(QFont("Helvetica", 14, QFont.Black))
        self.totalNum.setAlignment(Qt.AlignCenter)
        self.totalNum.setPalette(pe)
        self.currentNum.setAlignment(Qt.AlignCenter)
        self.currentNum.setFont(QFont("Helvetica", 14, QFont.Black))
        self.currentNum.setAutoFillBackground(True)
        self.currentNum.setPalette(pe)
        self.previousBT.setFont(QFont("Helvetica", 14, QFont.Black))
        self.nextBT.setFont(QFont("Helvetica", 18, QFont.Black))
        self.saveBT.setFont(QFont("Times", 18, QFont.Bold))
        self.quitBT.setFont(QFont("Times", 18, QFont.Bold))

        self.boundingBT.setFont(QFont("Helvetica", 14, QFont.Black))
        self.fittingBT.setFont(QFont("Helvetica", 14, QFont.Black))
        self.pointBT.setFont(QFont("Helvetica", 14, QFont.Black))

        #layout
        #left
        self.leftUpLayOut = QGridLayout()
        self.leftUpLayOut.addWidget(self.dirLE, 0, 0, 1, 2)
        self.leftUpLayOut.addWidget(self.dirUpdate, 1, 0)
        self.leftUpLayOut.addWidget(self.totalLabel, 2, 0)
        self.leftUpLayOut.addWidget(self.totalNum, 3, 0)
        self.leftUpLayOut.addWidget(self.currentLabel, 2, 1)
        self.leftUpLayOut.addWidget(self.currentNum, 3, 1)
        #self.leftUpLayOut.setColumnStretch(0,1)
        #self.leftUpLayOut.setColumnStretch(1,1)

        self.leftBottomLayOut = QGridLayout()
        self.leftBottomLayOut.addWidget(self.previousBT, 0, 0)
        self.leftBottomLayOut.addWidget(self.nextBT, 0, 1)
        self.leftBottomLayOut.addWidget(self.saveBT, 1, 0)
        self.leftBottomLayOut.addWidget(self.quitBT, 1, 1)
        #self.leftBottomLayOut.setColumnStretch(0,1)
        #self.leftBottomLayOut.setColumnStretch(1,1)
        self.leftLayOut = QVBoxLayout()
        self.leftLayOut.addLayout(self.leftUpLayOut)
        self.leftLayOut.addLayout(self.leftBottomLayOut)

        #right
        self.rightLayOut = QGridLayout()
        self.rightLayOut.addWidget(self.resultLabel, 0, 0)
        self.rightLayOut.addWidget(self.resultLW, 1, 0, 1, 3)
        self.rightLayOut.addWidget(self.boundingBT,2, 0)
        self.rightLayOut.addWidget(self.pointBT, 2, 1)
        self.rightLayOut.addWidget(self.fittingBT, 2, 2)
        self.rightLayOut.addWidget(self.zoomSLD, 3, 0, 1, 3)
        #main
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayOut)
        self.mainLayout.addLayout(self.rightLayOut)
        self.showWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.showWidget)

        self.show()

    def event_set(self):
        self.boundingBT.clicked[bool].connect(self.event_boundingBT)
        self.pointBT.clicked[bool].connect(self.event_pointBT)
        self.fittingBT.clicked[bool].connect(self.event_fittingBT)

    def event_fittingBT(self, pressed):
        if  pressed:
            self.bounding_flag = False
            self.point_flag = False
            self.fitting_flag = True
            self.fitting()
        else:
            self.fitting_flag = False
            # self.fitting_finish()

    def fitting(self):
        if self.point_list_zoom[0][0] > self.point_list_zoom[1][0]:
            flag = -1
        else:
            flag = 1
        x_curve = []
        y_curve = []
        point_to_interpolate = []
        point_to_interpolate.append(self.point_list_zoom[0])
        for i in range(len(self.point_list_zoom) - 1):
            x1 = self.point_list_zoom[i][0]
            x2 = self.point_list_zoom[i+1][0]
            if (x2 - x1) * flag > 0:
                point_to_interpolate.append(self.point_list_zoom[i+1])
            else:
                x_tmp = [j[0] for j in point_to_interpolate]
                y_tmp = [j[1] for j in point_to_interpolate]
                func = interpolate.interp1d(x_tmp, y_tmp, "quadratic")
                if flag > 0:
                    for k in range(x_tmp[0], x_tmp[-1]):
                        x_curve.append(k)
                        y_curve.append(func(k))
                else:
                    for k in range(x_tmp[0], x_tmp[-1], -1):
                        x_curve.append(k)
                        y_curve.append(func(k))
                point_to_interpolate.clear()
                point_to_interpolate.append(self.point_list_zoom[i])
                flag *= -1

        x_tmp = [j[0] for j in point_to_interpolate]
        y_tmp = [j[1] for j in point_to_interpolate]
        func = interpolate.interp1d(x_tmp, y_tmp, "cubic")
        if flag > 0:
            for k in range(x_tmp[0], x_tmp[-1]):
                x_curve.append(k)
                y_curve.append(func(k))
        else:
            for k in range(x_tmp[0], x_tmp[-1], -1):
                x_curve.append(k)
                y_curve.append(func(k))
        '''       
        x = [i[0] for i in self.point_list_zoom]
        y = [i[1] for i in self.point_list_zoom]
        print(x)
        print(y)
        
        func = interpolate.interp1d(x, y, "slinear")
        for i in range(len(x) - 1):
            if x[i+1] >= x[i]:
                func = interpolate.interp1d([x[i],x[i+1]], [y[i], y[i+1]], 'slinear')
                for j in range(x[i], x[i+1]):
                    x_curve.append(j)
                    y_curve.append(func(j))
            else:
                func = interpolate.interp1d([x[i+1], x[i]], [y[i+1], y[i]], 'slinear')
                for j in range(x[i+1], x[i]):
                    x_curve.append(j)
                    y_curve.append(func(j))
        x_min = min(x)
        x_max = max(x)
        x_curve = range(x_min, x_max)
        y_curve = [func(i) for i in x_curve]
        '''
        for i in range(len(x_curve)):
            self.fitting_point_list.append((x_curve[i], y_curve[i]))

        img_tmp = self.zoom_img(self.bounding_img)
        self.draw_point_zoom(img_tmp, 'fitting')
        cv2.imshow(self.fitting_winna, img_tmp)
        cv2.waitKey(0)


    def event_pointBT(self, pressed):
        if pressed:
            self.bounding_flag = False
            self.point_flag = True
            self.fitting_flag = False
            self.point()
        else:
            self.point_flag = False
            #self.point_finish()

    def event_boundingBT(self, pressed):
        if pressed == 0:
            self.bounding_flag = False
            self.bounding_finish()
        else:
            self.bounding_flag = True
            self.point_flag = False
            self.fitting_flag = False
            self.bounding_box()

    def point(self):
        cv2.destroyAllWindows()
        img_tmp = self.zoom_img(self.bounding_img)
        cv2.imshow(self.point_winna, img_tmp)
        cv2.setMouseCallback(self.point_winna, self.point_mouse)
        self.statusBar().showMessage('point')
        cv2.waitKey(0)

    def point_mouse(self, event, x, y, flags, param):
        img_tmp = self.zoom_img(self.bounding_img)
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.add_point(x,y)
            self.draw_point_zoom(img_tmp, 'point')
            cv2.imshow(self.point_winna, img_tmp)

    def add_point(self, x, y):
        self.point_list_zoom.append((x, y))
        self.point_list_ori.append(self.cal_point_coor(x, y))
        # add listwidget

    def cal_point_coor(self, x, y):
        x = x // self.zoom_ratio
        y = y // self.zoom_ratio
        x += self.bounding_coor[0]
        y += self.bounding_coor[1]
        return x, y

    def draw_point_zoom(self, img, mode):
        if mode == 'point':
            for point_coor in self.point_list_zoom:
                cv2.circle(img, point_coor, 10, (255, 0, 0), 5)
        elif mode == 'fitting':
            for point_coor in self.fitting_point_list:
                cv2.circle(img, point_coor, 5, (0, 0, 255), 5)
        return img

    def zoom_img(self,img):
        height, width = img.shape[:2]
        width *= self.zoom_ratio
        height *= self.zoom_ratio
        return cv2.resize(img, (width, height))

    def bounding_box(self):
        cv2.destroyAllWindows()
        cv2.imshow(self.bounding_winna, self.ori_img)
        cv2.setMouseCallback(self.bounding_winna, self.bounding_mouse)
        self.statusBar().showMessage('bounding')
        cv2.waitKey(0)

    def bounding_finish(self):
        cv2.destroyAllWindows()
        self.zoom_ratio = 8
        img_tmp = self.zoom_img(self.bounding_img)
        cv2.imshow(self.bounding_winna, img_tmp)
        self.statusBar().showMessage('bounding OK')
        cv2.waitKey(0)

    def bounding_mouse(self, event, x, y, flags, param):
        img_tmp = self.ori_img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            self.point1 = (x, y)
            cv2.circle(img_tmp, self.point1, 10, (0, 255, 0), 1)
            cv2.imshow(self.bounding_winna, img_tmp)
        elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
            cv2.rectangle(img_tmp, self.point1, (x,y), (0, 255, 0), 1)
            cv2.imshow(self.bounding_winna, img_tmp)
        elif event == cv2.EVENT_LBUTTONUP:
            self.point2 = (x, y)
            cv2.rectangle(img_tmp, self.point1, self.point2, (0, 255, 0), 1)
            cv2.imshow(self.bounding_winna, img_tmp)
            min_x = min(self.point1[0], self.point2[0])
            min_y = min(self.point1[1], self.point2[1])
            width = abs(self.point1[0] - self.point2[0])
            height = abs(self.point1[1] - self.point2[1])
            self.bounding_img = self.ori_img[min_y:min_y + height, min_x:min_x + width ]
            self.bounding_coor = (min_x, min_y, width, height)



if __name__ == '__main__':
    path = '/home/wuyudong/Project/ImageData/guidewire/send_guidewire_img/1.0.png'
    app = QApplication(sys.argv)
    w = MainWindow(sys.argv[1])
    sys.exit(app.exec())
