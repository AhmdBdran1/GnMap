import math  # for calculation
import random  # to simulate random values etc.
import os  # to work with files
import sys  # to get parameters from command line
import tkinter as tk
import numpy as np
from PIL import ImageTk, Image
from operator import itemgetter
import matplotlib as plt
import PyQt5.QtWidgets
import subprocess
from PyQt5.QtWidgets import (
    QLineEdit,
    QFileDialog,
    QMainWindow,
    QApplication,
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore, QtGui
import PyQt5.QtWidgets
from PyQt5.QtWidgets import (
    QDialog,
    QApplication,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
import time
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import threading
from PyQt5.QtCore import QThread, pyqtSignal
from scipy.cluster.hierarchy import single, fcluster
from scipy.spatial.distance import pdist
import networkx as nx
from networkx.algorithms import cycles


points = []
arrays = []


class Window2(QDialog):
    def __init__(self, parent=None):
        super(Window2, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.hBox = QHBoxLayout()
        self.label = QLabel(
            "  Press calculate button to show the graph of circles and the amount of circles in the graph  ",
            self,
        )

        self.label.setFixedHeight(20)
        self.label.setStyleSheet("font: bold 18px;")

        self.hbox = QHBoxLayout()
        self.label1 = QLabel("  Minimum cluster size: ", self)
        self.label1.setStyleSheet("font: bold 16px;")

        self.line_edit1 = QLineEdit(self)
        self.line_edit1.setStyleSheet("background-color: white;")
        self.line_edit1.setFixedWidth(50)
        self.label2 = QLabel("  Thresholds: ", self)
        self.label2.setStyleSheet("font: bold 16px;")

        self.line_edit2 = QLineEdit(self)
        self.line_edit2.setStyleSheet("background-color: white;")
        self.line_edit2.setFixedWidth(50)
        self.button = QPushButton("Calculte", self)
        self.button.setFixedWidth(100)
        self.button.setStyleSheet(
            "background-color: black; color: white; font-size: 20px;"
        )
        self.button.clicked.connect(self.clicker1)
        self.exceptionLabel = QLabel("")
        self.exceptionLabel.setFixedHeight(20)
        self.exceptionLabel.setStyleSheet("color: red; font: bold 18px;")

        self.button1 = QPushButton("Restart", self)

        self.button1.setStyleSheet(
            "background-color:blue; color: white; font-size: 20px;"
        )
        self.button1.clicked.connect(self.clicker2)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)

        layout.addWidget(self.canvas)
        layout.addWidget(self.label)

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.label1)
        self.hBox.addWidget(self.line_edit1)
        self.hBox.addWidget(self.label2)
        self.hBox.addWidget(self.line_edit2)
        self.hBox.addSpacing(30)
        self.hBox.addWidget(self.button)
        self.hBox.addSpacing(20)
        self.hBox.addWidget(self.exceptionLabel)
        self.hBox.addSpacerItem(spacer)
        self.hBox.addWidget(self.button1)
        Window2.setStyleSheet(self, "background-color:rgb(213, 246, 255);")
        layout.addLayout(self.hBox)

        self.setLayout(layout)

    def clicker2(self):
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def clicker1(self):
        self.button.setEnabled(False)
        flag = 0
        text = self.line_edit1.text()
        text1 = self.line_edit2.text()

        try:
            thresholds = float(text1)
            numInCluster = float(text)
        except ValueError:
            self.exceptionLabel.setText("Please Enter valid Data")
            self.button.setEnabled(True)
            flag = 1

        if flag == 0:
            window2 = Window2()
            self.figure.clear()
            plottt(self, thresholds, numInCluster)
            widget.addWidget(window2)
            widget.setCurrentIndex(widget.currentIndex() + 1)


def plottt(self, thresholds, numInCluster):
    global points
    points = np.array(points)
    # Calculate the pairwise distances between samples
    distances = pdist(points)

    # Perform single-linkage clustering
    Z = single(distances)

    # Calculate the cluster labels for a threshold of 2
    labels = fcluster(Z, thresholds, criterion="distance")

    # Print the elements of each cluster
    arrays = []
    for cluster in set(labels):
        if np.sum(labels == cluster) > numInCluster:
            arrays.append(points[labels == cluster])

    nodes_array = []
    for arr in arrays:
        min_point = min(arr, key=lambda point: point[0])
        max_point = max(arr, key=lambda point: point[0])
        minmax_points = []
        minmax_points.append(min_point)

        minmax_points.append(max_point)
        minmax_points = np.array(minmax_points)
        nodes_array.append(minmax_points)

    sortedByX = sort_by_x(nodes_array)
    sortedByY = sort_by_y(nodes_array)
    # Create an empty graph
    plt.clf()
    G = nx.Graph()
    G.clear()

    for pair in sortedByX:
        # Convert the points to tuples
        pair = [tuple(point) for point in pair]
        # Get the x and y coordinates of the points
        x = [point[0] for point in pair]
        y = [point[1] for point in pair]
        # Draw a line between the points
        plt.plot(x, y)

    for array in sortedByX:
        for point in array:
            print(point)
            point = tuple(point)

            G.add_node(point)

    for i in range(len(sortedByX) - 1):
        first_array = [tuple(point) for point in sortedByX[i]]
        second_array = [tuple(point) for point in sortedByX[i + 1]]
        # Sort the points in each array by x-coordinate
        first_array = sorted(first_array, key=lambda x: x[0])
        second_array = sorted(second_array, key=lambda x: x[0])
        # Get the point with the highest x-coordinate in the first array
        point1 = max(first_array, key=lambda x: x[0])
        # Get the point with the lowest x-coordinate in the second array
        point2 = min(second_array, key=lambda x: x[0])

        # Add an edge between the selected points
        G.add_edge(point1, point2)

    for i in range(len(sortedByY) - 1):
        first_array = [tuple(point) for point in sortedByY[i]]
        second_array = [tuple(point) for point in sortedByY[i + 1]]
        # Sort the points in each array by x-coordinate
        first_array = sorted(first_array, key=lambda x: x[1])
        second_array = sorted(second_array, key=lambda x: x[1])
        # Get the point with the highest x-coordinate in the first array
        point1 = max(first_array, key=lambda x: x[1])
        # Get the point with the lowest x-coordinate in the second array
        point2 = min(second_array, key=lambda x: x[1])

        # Add an edge between the selected points
        G.add_edge(point1, point2)

    pos = {}
    for point in G.nodes:
        x, y = point
        pos[point] = (x, y)
    # Set the positions of the nodes
    nx.set_node_attributes(G, pos, "pos")

    if len(nx.cycle_basis(G)) > 0:
        num_cycles = len(list(nx.find_cycle(G)))
        plt.text(
            0.5,
            0.01,
            "Number of cycles in the graph: " + str(num_cycles),
            fontsize=18,
            horizontalalignment="center",
            verticalalignment="bottom",
            transform=plt.gca().transAxes,
        )

    else:
        plt.text(
            0.5,
            0.01,
            "no cycles in the graph",
            fontsize=18,
            horizontalalignment="center",
            verticalalignment="bottom",
            transform=plt.gca().transAxes,
        )

    # Draw the graph
    nx.draw_networkx(G, pos, with_labels=False, node_size=3)


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.hBox = QHBoxLayout()
        self.label1 = QLabel(
            "  Press calculate button to show the graph of circles and the amount of circles in the graph ",
            self,
        )

        self.label1.setStyleSheet("font: bold 16px;")

        """
		self.label=QLabel("please enter minimum cluster size and thresholds of cluster and thin calculate the number of circles in graph :", self)
		self.label.setFixedHeight(20)


		self.hbox = QHBoxLayout()
		self.label1 = QLabel("  Cluster size: ", self)
		
		self.line_edit1 = QLineEdit(self)
		self.line_edit1.setFixedWidth(50)
		self.label2 = QLabel("  Thresholds: ", self)
		
		self.line_edit2 = QLineEdit(self)
		self.line_edit2.setFixedWidth(50)
		self.button = QPushButton("Calculte", self)
		self.button.setFixedWidth(100)
		self.button.setStyleSheet("background-color: black; color: white; font-size: 20px;")
		spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
		"""
        self.button = QPushButton("Calculte", self)
        self.button.setFixedWidth(100)
        self.button.setStyleSheet(
            "background-color: black; color: white; font-size: 20px;"
        )
        self.button.clicked.connect(self.clicker1)

        self.button1 = QPushButton("Restart", self)

        self.button1.setStyleSheet(
            "background-color:blue; color: white; font-size: 20px;"
        )
        self.button1.clicked.connect(self.clicker2)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)

        layout.addWidget(self.canvas)
        """
		layout.addWidget(self.label)
		
		self.hBox=QHBoxLayout()
		self.hBox.addWidget(self.label1)
		self.hBox.addWidget(self.line_edit1)
		self.hBox.addWidget(self.label2)
		self.hBox.addWidget(self.line_edit2)
		self.hBox.addSpacerItem(spacer)
		self.hBox.addWidget(self.button)

		layout.addLayout(self.hBox)
		"""
        self.hBox.addWidget(self.label1)

        self.hBox.addWidget(self.button)
        self.hBox.addSpacerItem(spacer)
        self.hBox.addWidget(self.button1)
        Window.setStyleSheet(self, "background-color:rgb(213, 246, 255);")
        layout.addLayout(self.hBox)
        self.setLayout(layout)


    def clicker2(self):
        os.execv(sys.executable, [sys.executable] + sys.argv)


    def clicker1(self):
        window2 = Window2()
        plottt(self, 0.0003, 200)
        widget.addWidget(window2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def plot(self):
        self.figure.clear()
        oxfordplot(self)
        self.canvas.draw()


def oxfordplot(self):

    f = open("graphProba___1.txt", "r")
    temp = f.readline()
    title = temp[1:]
    print(title)

    f.readline()
    Xtemp = f.readline()
    temp = Xtemp.split()
    xMinLim = int(temp[1])
    xMaxLim = int(temp[2])
    print(xMaxLim, xMinLim)

    Ytemp = f.readline()
    temp = Ytemp.split()
    yMinLim = int(temp[1])
    yMaxLim = int(temp[2])
    print(yMaxLim, yMinLim)

    f.readline()

    # plt.figure(figsize=(12, 12))
    plt.xlim([xMinLim, xMaxLim])
    plt.ylim([yMinLim, yMaxLim])
    plt.margins(10, 10)

    noMoreMarkers = False

    while not noMoreMarkers:
        line = f.readline()

        Line = line.split()

        if Line[0] != "points":
            noMoreMarkers = True
        else:
            x1 = float(Line[1])
            y1 = float(Line[2])
            a = [[x1, y1]]
            plt.plot(*zip(*a), marker=".", markersize=0.5, color="k", ls="")
            points.append((x1, y1))

    xlabelTemp = f.readline()
    xlabel = xlabelTemp[5:]

    noMoreFloridanusContigs = False
    temp = 0
    flag2 = False

    while not noMoreFloridanusContigs:
        if not flag2:
            contigNameTemp = f.readline()

        if contigNameTemp[:3] != "#NW":
            print(contigNameTemp[:3])
            noMoreFloridanusContigs = True
        else:
            flag2 = False
            arrows = f.readline()
            x = arrows.split()
            x_1 = float(x[1])
            y_1 = float(x[2])
            x_2 = float(x[3])
            y_2 = float(x[4])
            plt.plot(
                [x_1, x_2],
                [y_1, y_2],
                marker=">",
                linewidth=0.5,
                markersize=4,
                color="b",
                clip_on=False,
            )
            # print(x_1,y_1,x_2,y_2)

            segments = f.readline()
            Segments = segments.split()
            if Segments[0][:8] == "segments":
                x_11 = float(Segments[1])
                y_11 = float(Segments[2])
                x_22 = float(Segments[3])
                y_22 = float(Segments[4])
                plt.plot([x_11, x_22], [y_11, y_22], linewidth=0.5, color="b")
                # print(x_11,y_11,x_22,y_22)

            else:
                flag2 = True
                contigNameTemp = segments

            """ y"""

    text1 = ""
    noMoreFloridanusContigs = False
    temp = 0
    flag2 = False

    while not noMoreFloridanusContigs:
        if not flag2:
            contigNameTemp = f.readline()

        if contigNameTemp[:3] != "#Sc":
            text1 = contigNameTemp
            noMoreFloridanusContigs = True
        else:
            flag2 = False
            arrows = f.readline()
            x = arrows.split()
            x_1 = float(x[1])
            y_1 = float(x[2])
            x_2 = float(x[3])
            y_2 = float(x[4])
            markerType = int(x[8])
            marker1 = ""
            if markerType == 1:
                marker1 = "v"
            else:
                marker1 = "^"

            plt.plot(
                [x_1, x_2],
                [y_1, y_2],
                marker=marker1,
                markersize=4,
                linewidth=0.5,
                color="b",
                clip_on=False,
            )
            # print(x_1,y_1,x_2,y_2)

            segments = f.readline()
            Segments = segments.split()
            if Segments[0][:8] == "segments":
                x_11 = float(Segments[1])
                y_11 = float(Segments[2])
                x_22 = float(Segments[3])
                y_22 = float(Segments[4])
                plt.plot([x_11, x_22], [y_11, y_22], linewidth=0.5, color="k")
                # print(x_11,y_11,x_22,y_22)

            else:
                flag2 = True
                contigNameTemp = segments

    while text1[:4] == "text":

        textArr = text1.split()
        if float(textArr[1]) > -2 and float(textArr[2]) > -2:
            if textArr[7] == "1":
                plt.text(
                    float(textArr[1]),
                    float(textArr[2]) - 2.5,
                    textArr[3],
                    fontsize=7,
                    style="oblique",
                    ha="center",
                    va="top",
                    wrap=True,
                )
            else:
                plt.text(
                    float(textArr[1]) - 3,
                    float(textArr[2]),
                    textArr[3],
                    fontsize=7,
                    style="oblique",
                    ha="right",
                    va="center",
                    wrap=True,
                )
        elif float(textArr[1]) > -2:
            plt.text(
                float(textArr[1]),
                float(textArr[2]) - 1,
                textArr[3],
                fontsize=12,
                style="oblique",
                ha="center",
                va="center",
                wrap=True,
            )
        elif float(textArr[2]) > -2:
            plt.text(
                float(textArr[1]) - 5.5,
                float(textArr[2]),
                textArr[3],
                rotation=90,
                fontsize=12,
                style="oblique",
                ha="center",
                va="center",
                wrap=True,
            )

        text1 = f.readline()




class Thread(QThread):
    _signal = pyqtSignal(float)
    def __init__(self,progressBarr,label):
        super(Thread, self).__init__()
        self.progressBar=progressBarr
        self.label=label
    def __del__(self):
        self.wait()

    def run(self):
        i=0.0
        x=0.02
        flag=True
        while flag:
            time.sleep(x)
            if self.progressBar.value() >= 98 and t2.is_alive()==True:
                time.sleep(1)
                i=0.0
                self.label.setText("preparing for plot ...")
                
            if t2.is_alive()==False:
                x=0.001
            if t2.is_alive()==False and self.progressBar.value() >= 98:
                flag=False
                
            self._signal.emit(i)
            i=i+1/10
            
            #start thread to plot 
        
        i=0.0
        x=0.02
        flag=True
        t1.start()
        
        while flag:
            time.sleep(x)
            if self.progressBar.value() >= 98 and t1.is_alive()==True:
                time.sleep(1)
                i=0.0
            if t1.is_alive()==False:
                x=0.01
            
            self._signal.emit(i)
            self.label.setText("Please wait while we plot ...")
            i=i+1/10
            
        
        
            







class Progress(QWidget):
    def __init__(self):
        super(Progress,self).__init__()
        uic.loadUi("C:\\Users\\User\\.spyder-py3\\progress.ui",self)
        self.lay=self.findChild(QVBoxLayout,"verticalLayout")
        
        self.progressBar=self.findChild(QProgressBar,"progressBar")
        self.label=self.findChild(QLabel,"label")
        self.progressBar.setValue(0)
        self.thread = Thread(self.progressBar,self.label)
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()
        t2.start()
        #t2.join()
        #t1.start()
        
      

        
       

    def signal_accept(self, msg):
        self.progressBar.setValue(int(msg))
        if self.progressBar.value() == 99 and t2.is_alive()==False:
            t1.join()
			
		
            widget.addWidget(window)
            widget.setCurrentIndex(widget.currentIndex()+1)
			
            

class UI(QMainWindow):
    def __init__(self, filesNames):
        super(UI, self).__init__()
        uic.loadUi("C:\\Users\\User\\.spyder-py3\\aaa.ui", self)
        filesNames = ["", "", "", "", ""]
        self.setWindowTitle("GnMap")

        self.pb1 = self.findChild(QPushButton, "pb1")
        self.pb2 = self.findChild(QPushButton, "pb2")
        self.pb3 = self.findChild(QPushButton, "pb3")
        self.pb4 = self.findChild(QPushButton, "pb4")
        self.pb5 = self.findChild(QPushButton, "pb5")

        self.le1 = self.findChild(QLineEdit, "le1")
        self.le2 = self.findChild(QLineEdit, "le2")
        self.le3 = self.findChild(QLineEdit, "le3")
        self.le4 = self.findChild(QLineEdit, "le4")
        self.le5 = self.findChild(QLineEdit, "le5")
        self.label=self.findChild(QLabel,"label")
        self.label.setStyleSheet("font: bold 18px;")
        self.label1=self.findChild(QLabel,"label_2")
        self.label1.setStyleSheet("color: red; font: bold 18px;")

        self.pushButton1 = self.findChild(QPushButton, "pushButton")

        self.pb1.clicked.connect(self.pb1Func)
        self.pb2.clicked.connect(self.pb2Func)
        self.pb3.clicked.connect(self.pb3Func)
        self.pb4.clicked.connect(self.pb4Func)
        self.pb5.clicked.connect(self.pb5Func)

        self.pushButton1.clicked.connect(self.clicker1)
        self.setWindowIcon(QtGui.QIcon("icon.png"))

    def pb1Func(self):
        self.temp = QFileDialog.getOpenFileName(
            self, "Open File", "", "Fasta Files (*.fasta)"
        )
        self.le1.setText(str(self.temp[0]))
        filesNames[0] = self.temp[0]

    def pb2Func(self):
        self.temp = QFileDialog.getOpenFileName(
            self, "Open File", "", "Fasta Files (*.fasta)"
        )
        self.le2.setText(str(self.temp[0]))

        filesNames[1] = self.temp[0]

    def pb3Func(self):
        self.temp = QFileDialog.getOpenFileName(
            self, "Open File", "", "Fasta Files (*.fasta)"
        )
        self.le3.setText(str(self.temp[0]))
        filesNames[2] = self.temp[0]

    def pb4Func(self):
        self.temp = QFileDialog.getOpenFileName(
            self, "Open File", "", "Fasta Files (*.txt)"
        )
        self.le4.setText(str(self.temp[0]))
        filesNames[3] = self.temp[0]

    def pb5Func(self):
        self.temp = QFileDialog.getOpenFileName(
            self, "Open File", "", "Fasta Files (*.txt)"
        )
        self.le5.setText(str(self.temp[0]))
        filesNames[4] = self.temp[0]

    def clicker1(self):
        flag=True
        for file in filesNames:
            if file=="":
                self.label1.setText("Please upload valid files to run")
                flag=False

        if flag:
            self.label1.setText("")
            progressWidget = Progress()
            widget.addWidget(progressWidget)
            widget.setCurrentIndex(widget.currentIndex() + 1)


        """
        self.pushButton1=self.findChild(QPushButton,"pushButton")
        self.pushButton2=self.findChild(QPushButton,"pushButton_2")
   
        self.textEdit=self.findChild(QTextEdit,"textEdit")
        self.textEdit2=self.findChild(QTextEdit,"textEdit_2")
        
        
        self.pushButton1.clicked.connect(self.clicker1)
        self.pushButton2.clicked.connect(self.clicker2)
        
        
    def clicker1(self):
         fname=QFileDialog.getOpenFileName(self,"Open File","","Fasta Files (*.fasta)")
         self.textEdit.setText(str(fname[0]))
        
         
        
    def clicker2(self):
         fname=QFileDialog.getOpenFileName(self,"Open File","","Fasta Files (*.fasta)")
         self.textEdit2.setText(str(fname[0]))
         
"""


def WindowInit(
    window,
):
    window.plot()


# pip install matplotlib
# pip install statistics
# import statistics
# import numpy as np
# import matplotlib.pyplot as plt #pip install matplotlib

# alpha=numpy.
# C:\Frenkel\LTCPython\LTC_original\ConvexRcoloring\TreeRecoloring_pp.py
# win-search -> cmd
# 1

# cd C:\Frenkel\LTCPython\VovaPy\
# C:\Python27\python.exe C:\Frenkel\LTCPython\VovaPy\rec.py
# python "C:\Frenkel\LTCPython\VovaPy\rec.py"
# stop: ctrl+c

# old:
# C:\Python27\python.exe C:\Frenkel\LTCPython\LTC_original\ConvexRcoloring\TreeRecoloring_pp.py
# C:\Users\user>C:\Python27amd64\python.exe C:\Frenkel\LTCPython\VovaPy\rec.py
# pip
# pip install <package>
# python studio:
# 		anaconda ()
# 		spider
# 		jupyter (uchebnik)
# 		WinSCP
# stop: ctrl+c
# import <vovafile.py> #mozhno py ne pisat'
#
# old:
# search in windows "cmd" or "command prompt"
# in command prompt: cd C:\Frenkel\LTCPython\VovaPy\
# C:\Python27\python.exe rec.py
class clVovaMath:
    def __init__(self):
        self.vvSortedAndNoOutLiersIfNeed___k = 3
        self.vvSortedAndNoOutLiersIfNeed___nMaxDone = -1
        self.vvSortedAndNoOutLiersIfNeed___vmaxVarRelativeToKK = []

    def makeListOfAllPermutation(self, myList, n):
        # n=len(myList)
        if n <= 0:
            return [], 0
        if n == 1:
            return [myList[0]], 1
        if n == 2:
            res = []
            res.append([myList[0], myList[1]])
            res.append([myList[1], myList[0]])
            return res, 2
        res = []
        nPerm = 0
        for i in range(n):
            listCurrent = []
            for j in range(n):
                if j != i:
                    listCurrent.append(myList[j])
            res0, n0 = self.makeListOfAllPermutation(listCurrent, n - 1)
            for perm in res0:
                perm.append(myList[i])
                res.append(perm)
                nPerm += 1
        return res, nPerm

    def makeListOfAllPermutation_test(self):
        n = 3
        # n=5, nPerm=120
        # n=7, nPerm=5,040
        # n=10, nPerm=3,628,800
        myList = []
        for i in range(n):
            myList.append(i)
        res, nPerm = self.makeListOfAllPermutation(myList, n)
        print("makeListOfAllPermutation_test: n=" + str(n) + ", nPerm=" + str(nPerm))
        if n <= 5:
            print(str(res))

    def bCodeNext(self, vCode, n, vCodeMax, bStartFrom0):
        # vCodeMax=[1]*n#[1,1,1,..,1]
        # vCodeMax=[4]*n#[4,4,4,..,4]
        if len(vCode) == 0:
            if bStartFrom0:
                vCode = [0] * n  # [0,0,0,..,0]
            else:
                vCode = [1] * n  # [1,1,1,..,1]
            # print str(vCode)
            return True, vCode
        else:
            i0 = -1
            for i in range(n):
                if vCode[i] < vCodeMax[i]:
                    i0 = i
            if i0 < 0:
                return False, vCode
            vCode[i0] += 1
            if i0 < n - 1:
                for i in range(i0 + 1, n):
                    vCode[i] = 0 if bStartFrom0 else 1
            return True, vCode

    def median(self, vv):
        n = len(vv)
        if n < 1:
            return 0
        if n == 1:
            return vv[0]
        if n == 2:
            return 0.5 * (vv[0] + vv[1])
        vvSorted = sorted(vv)
        if (n % 2) == 1:
            return vvSorted[int(0.5 * (n + 1))]
        return 0.5 * (vv[int(0.5 * n)] + vv[int(0.5 * n) + 1])

    def quantile(self, vv, p):  # q=
        n = len(vv)
        if n < 1:
            return 0
        if n == 1:
            return vv[0]
        if n == 2:
            return self.yByLin(0, vv[0], 1, vv[1], p)
        vvSorted = sorted(vv)
        i = int(float(n) * p)
        return vvSorted[i]

    def quantiles(self, vv, nQ):  # vq=
        n = len(vv)
        if n <= nQ:
            vq = []
            for i in range(nQ + 1):
                vq.append(0)
            return vq
        vvSorted = sorted(vv)
        vq = []
        for i in range(nQ + 1):
            p = float(i) / nQ
            j = int(p * n)
            if j >= n:
                j = n - 1
            # print str(j)
            vq.append(vvSorted[j])
        return vq

    def mean(self, vv):  # mean=
        n = 0
        sum = 0
        for a in vv:
            n += 1
            sum += a
        if n == 0:
            return 0
        return float(sum) / n

    def var(self, vv):  # S^2=
        n = len(vv)
        if n < 2:
            return 0
        m = self.mean(vv)
        sum = 0
        for a in vv:
            sum += (a - m) * (a - m)
        return float(sum) / (n - 1)

    def STDV(self, vv):
        return math.sqrt(self.var(vv))

    def NandL(self, vv, bSorted, proc):  # N50, L50
        lenSum = sum(vv)
        lenGet = lenSum * proc * 0.01
        nn = 0
        ll = 0
        lenSum = 0
        vvSorted = vv
        if not bSorted:
            vvSorted = []
            for v in vv:
                vvSorted.append(v)
            vvSorted.sort()
        for v in vvSorted:
            lenSum += v
            ll += 1
            if lenSum >= lenGet:
                nn = v
                return nn, ll
        return nn, ll

    def valOnly(self, vv, vb):
        vvPP = []
        n = len(vv)
        for i in range(n):
            if vb[i]:
                vvPP.append(vv[i])
        return vvPP

    def ffNormalDistribution(self, x):  # p=
        # Pr(X<x)
        if x < 0:
            return 1 - self.ffNormalDistribution(-x)
        if x == 0:
            return 0.5
        # table of normal distribution: (x, Pr(X<x))
        vt = [
            [0, 0.5],
            [0.1, 0.54],
            [0.2, 0.58],
            [0.3, 0.62],
            [0.4, 0.66],
            [0.5, 0.69],
            [0.6, 0.73],
            [0.7, 0.76],
            [0.8, 0.79],
            [0.9, 0.82],
            [1.0, 0.84],
            [1.5, 0.93],
            [2.0, 0.9772],
            [2.5, 0.9938],
            [3.0, 0.9987],
            [3.2, 0.9993],
            [3.5, 0.9998],
            [3.7, 0.9999],
            [4.0, 0.999937],
            [5.0, 0.9999994],
            [6.0, 0.999999998],
        ]
        n = len(vt)
        for i in range(1, n):
            if x < vt[i][0]:
                return self.yByLin(vt[i - 1][0], vt[i - 1][1], vt[i][0], vt[i][1], x)
        return 1  # >0.999,999,998

    def zNormalDistribution(self, a):  # z=
        # z_a: Pr(X<z_a)=a, Pr(X>z_{1-a})=1-(1-a)=a
        if a < 0.5:
            return -self.zNormalDistribution(1 - a)
        if a == 0.5:
            return 0
        # table of normal distribution: (x, Pr(X<x))
        vt = [
            [0, 0.5],
            [0.1, 0.54],
            [0.2, 0.58],
            [0.3, 0.62],
            [0.4, 0.66],
            [0.5, 0.69],
            [0.6, 0.73],
            [0.7, 0.76],
            [0.8, 0.79],
            [0.9, 0.82],
            [1.0, 0.84],
            [1.5, 0.93],
            [2.0, 0.9772],
            [2.5, 0.9938],
            [3.0, 0.9987],
            [3.2, 0.9993],
            [3.5, 0.9998],
            [3.7, 0.9999],
            [4.0, 0.999937],
            [5.0, 0.9999994],
            [6.0, 0.999999998],
        ]
        n = len(vt)
        for i in range(1, n):
            if a < vt[i][1]:
                return self.yByLin(vt[i - 1][1], vt[i - 1][0], vt[i][1], vt[i][0], a)
        return 1  # >0.999,999,998

    def ffStudent(self, x, df):  # p=
        # Pr(X<x)
        # NB! poka for df>15
        if df > 15:
            sigma2 = float(df) / (df - 2)
            sigma = math.sqrt(sigma2)
            xNorm = x / sigma
        else:
            xNorm = 5
        return self.ffNormalDistribution(xNorm)

    def pValChi2(self, x, df):  # p=
        # Pr(X>x)
        if df > 30:
            # chi^2 ~ N(df, 2df)
            xNorm = float(x - df) / math.sqrt(2 * df)
            return 1 - ffNormalDistribution(xNorm)
        vP = [0.2, 0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001]
        # x[i]: Pr(X<x[i])=vP[i]
        vVal = []
        if df == 1:
            vVal = [
                1.642374415,
                2.705543454,
                3.841458821,
                6.634896601,
                7.879438577,
                10.82756617,
                12.11566515,
                15.13670523,
            ]
        if df == 2:
            vVal = [
                3.218875825,
                4.605170186,
                5.991464547,
                9.210340372,
                10.59663473,
                13.81551056,
                15.20180492,
                18.42068074,
            ]
        if df == 3:
            vVal = [
                4.641627676,
                6.251388631,
                7.814727903,
                11.34486673,
                12.83815647,
                16.2662362,
                17.72999623,
                21.10751347,
            ]
        if df == 4:
            vVal = [
                5.988616694,
                7.77944034,
                9.487729037,
                13.27670414,
                14.860259,
                18.46682695,
                19.997355,
                23.51274244,
            ]
        if df == 5:
            vVal = [
                7.289276127,
                9.2363569,
                11.07049769,
                15.08627247,
                16.74960234,
                20.51500565,
                22.10532678,
                25.74483196,
            ]
        if df == 6:
            vVal = [
                8.55805972,
                10.64464068,
                12.59158724,
                16.81189383,
                18.54758418,
                22.45774448,
                24.10279899,
                27.85634124,
            ]
        if df == 7:
            vVal = [
                9.8032499,
                12.01703662,
                14.06714045,
                18.47530691,
                20.27773987,
                24.32188635,
                26.01776771,
                29.87750391,
            ]
        if df == 8:
            vVal = [
                11.03009143,
                13.36156614,
                15.50731306,
                20.09023503,
                21.95495499,
                26.12448156,
                27.8680464,
                31.827628,
            ]
        if df == 9:
            vVal = [
                12.24214547,
                14.68365657,
                16.9189776,
                21.66599433,
                23.58935078,
                27.87716487,
                29.6658081,
                33.71994844,
            ]
        if df == 10:
            vVal = [
                13.44195757,
                15.98717917,
                18.30703805,
                23.20925116,
                25.18817957,
                29.58829845,
                31.41981251,
                35.56401394,
            ]
        if df == 11:
            vVal = [
                14.63142051,
                17.27500852,
                19.67513757,
                24.72497031,
                26.75684892,
                31.26413362,
                33.136615,
                37.36698644,
            ]
        if df == 12:
            vVal = [
                15.81198622,
                18.54934779,
                21.02606982,
                26.21696731,
                28.29951882,
                32.90949041,
                34.82127464,
                39.13440388,
            ]
        if df == 13:
            vVal = [
                16.98479702,
                19.81192931,
                22.36203249,
                27.68824961,
                29.81947122,
                34.52817897,
                36.47779372,
                40.87065501,
            ]
        if df == 14:
            vVal = [
                18.15077056,
                21.06414421,
                23.6847913,
                29.14123774,
                31.31934962,
                36.12327368,
                38.10940393,
                42.57928895,
            ]
        if df == 15:
            vVal = [
                19.31065711,
                22.30712958,
                24.99579014,
                30.57791417,
                32.80132065,
                37.69729822,
                39.71875979,
                44.26322494,
            ]
        if df == 16:
            vVal = [
                20.46507929,
                23.54182892,
                26.2962276,
                31.99992691,
                34.26718654,
                39.25235479,
                41.30807372,
                45.92489905,
            ]
        if df == 17:
            vVal = [
                21.61456053,
                24.76903534,
                27.58711164,
                33.40866361,
                35.71846566,
                40.79021671,
                42.87921296,
                47.56636956,
            ]
        if df == 18:
            vVal = [
                22.75954582,
                25.98942308,
                28.86929943,
                34.80530573,
                37.15645146,
                42.31239633,
                44.43377074,
                49.18939447,
            ]
        if df == 19:
            vVal = [
                23.90041722,
                27.20357103,
                30.14352721,
                36.19086913,
                38.58225655,
                43.82019596,
                45.97311956,
                50.79548967,
            ]
        if df == 20:
            vVal = [
                25.03750564,
                28.41198058,
                31.41043284,
                37.56623479,
                39.99684631,
                45.31474662,
                47.49845189,
                52.38597327,
            ]
        if df == 21:
            vVal = [
                26.17109994,
                29.61508944,
                32.67057334,
                38.93217268,
                41.40106477,
                46.79703804,
                49.0108116,
                53.96200012,
            ]
        if df == 22:
            vVal = [
                27.30145403,
                30.81328234,
                33.92443847,
                40.28936044,
                42.795655,
                48.26794229,
                50.51111876,
                55.52458878,
            ]
        if df == 23:
            vVal = [
                28.42879252,
                32.00689968,
                35.17246163,
                41.63839812,
                44.18127525,
                49.72823247,
                52.00018929,
                57.07464314,
            ]
        if df == 24:
            vVal = [
                29.55331524,
                33.19624429,
                36.4150285,
                42.97982014,
                45.55851194,
                51.17859778,
                53.47875077,
                58.61296975,
            ]
        if df == 25:
            vVal = [
                30.67520089,
                34.38158702,
                37.65248413,
                44.3141049,
                46.92789016,
                52.61965578,
                54.94745532,
                60.14029191,
            ]
        if df == 26:
            vVal = [
                31.79461007,
                35.56317127,
                38.88513866,
                45.64168267,
                48.28988233,
                54.05196239,
                56.40689012,
                61.65726128,
            ]
        if df == 27:
            vVal = [
                32.9116877,
                36.74121675,
                40.11327207,
                46.96294212,
                49.6449153,
                55.47602021,
                57.85758614,
                63.16446742,
            ]
        if df == 28:
            vVal = [
                34.02656512,
                37.91592254,
                41.33713815,
                48.27823577,
                50.99337627,
                56.89228539,
                59.30002543,
                64.66244583,
            ]
        if df == 29:
            vVal = [
                35.1393618,
                39.08746977,
                42.5569678,
                49.58788447,
                52.33561779,
                58.30117349,
                60.73464717,
                66.15168463,
            ]
        if df == 30:
            vVal = [
                36.25018678,
                40.25602374,
                43.77297183,
                50.89218131,
                53.67196193,
                59.7030643,
                62.16185287,
                67.63263026,
            ]
        if x < vVal[0]:
            return 1  # ns
        n = len(vVal)
        if x > vVal[n - 1]:
            return 0  # highly significant
        for i in range(1, n):
            if x <= vVal[i]:
                return self.yByLin(vVal[i - 1], vP[i - 1], vVal[i], vP[i], x)
        return vP[n - 1]  # no need

    def pEqFreq(self, pObs, pExp, n):  # p=
        if pExp == 0:
            if pObs > 0:
                return 0
            return 1
        if pExp == 1:
            if pObs < 1:
                return 0
            return 1
        X2 = n * float((pObs - pExp) * (pObs - pExp)) / (pExp * (1 - pExp))
        return self.pValChi2(X2, 1)

    def tTest_pValTwoTails(self, t, df):  # p=
        # Pr(|T|>t)
        if df > 0:
            return 2 * (1 - self.ffStudent(abs(t), df))
        else:
            return 1

    def tTestOneSample(self, vv, mu0):  # p=
        # vv ~ N(a,sigma2)
        # H0: E(X)=mu0, variance unknown => z=(mean(vv)-mo0)/sqr(S2/n) ~ studentDistr(df=n-1)
        n = len(vv)
        s2 = self.var(vv)
        m = self.mean(vv)
        s = math.sqrt(s2)
        if n < 2:
            return 1  # ns
        if s == 0:
            if m == m0:
                return 1  # ns
            return 0  # significant
        t = float(m - mu0) / (float(s) / math.sqrt(n))
        df = n - 1
        return self.tTest_pValTwoTails(t, df)

    def tTestTwoSamplesEqVar(self, vv1, vv2):  # p=
        # vv1 ~ N(a1,sigma12)
        # vv2 ~ N(a2,sigma22)
        # H0: sigma12=sigma22 => (mean(vv1)-mean(vv2))/S2 ~ studentDistr(df=n1+n2-2)
        m1 = self.mean(vv1)
        s12 = self.var(vv1)
        m2 = self.mean(vv2)
        s22 = self.var(vv2)
        n1 = len(vv1)
        n2 = len(vv2)
        df = n1 + n2 - 2
        sp = math.sqrt(float((n1 - 1) * s12 + (n2 - 1) * s22) / df)
        t = float(m1 - m2) / (sp * math.sqrt(float(1) / n1 + float(1) / n2))
        return self.tTest_pValTwoTails(t, df)

    def tTestTwoSamplesDiffVar(self, vv1, vv2):  # p=
        # vv1 ~ N(a1,sigma12)
        # vv2 ~ N(a2,sigma22)
        # H0: a1=a2 => (mean(vv1)-mean(vv2))/sd ~ studentDistr
        m1 = self.mean(vv1)
        s12 = self.var(vv1)
        m2 = self.mean(vv2)
        s22 = self.var(vv2)
        n1 = len(vv1)
        n2 = len(vv2)
        if n1 < 2 or n2 < 2:
            # print str(vv1)
            # print str(vv2)
            return 1
        ss1 = float(s12) / n1
        ss2 = float(s22) / n2
        sss1 = float(ss1 * ss1) / (n1 - 1)
        sss2 = float(ss2 * ss2) / (n2 - 1)
        sd2 = ss1 + ss2
        sd = math.sqrt(sd2)
        if sd > 0:
            t = float(m1 - m2) / sd
            df = int(float(sd2 * sd2) / (sss1 + sss2))
            return self.tTest_pValTwoTails(t, df)
        if m1 == m2:
            return 0.5
        return 0

    def PEV(self, vv1, vv2):  # pev=
        # P.E.V.=percentage of explained variance
        # (how much subdivision onto 2 groups reduce variance within groups)
        # https://en.wikipedia.org/wiki/Fraction_of_variance_unexplained
        m1 = self.mean(vv1)
        m2 = self.mean(vv2)
        # s12=self.var(vv1)
        # s22=self.var(vv2)
        vv = []
        vv0 = []
        for v in vv1:
            vv.append(v)
            vv0.append(v - m1)
        for v in vv2:
            vv.append(v)
            vv0.append(v - m2)
        s2 = self.var(vv)
        s02 = self.var(vv0)
        if s2 <= 0:
            return 0
        return float(s2 - s02) / s2

    def corrPearson(self, vv1, vv2):  # corr=
        # regular correlation coeffecient
        n = len(vv1)
        if n < 2:
            return 0
        if n != len(vv2):
            print("corrPearson n(vv1)=" + str(n) + "=/=" + str(len(vv2)) + "=n(vv2)")
            return 1 / (1 - 1)  # error
        m1 = self.mean(vv1)
        s12 = self.var(vv1)
        m2 = self.mean(vv2)
        s22 = self.var(vv2)
        if s12 * s22 == 0:
            return 0
        cov = 0
        for i in range(n):
            cov += (vv1[i] - m1) * (vv2[i] - m2)
        cov = float(cov) / (n - 1)
        corr = float(cov) / math.sqrt(s12 * s22)
        return corr

    def corrAndP(self, vv1, vv2):  # corr,p=
        # H0: rho=0 => t_(n-2)=r sqr(n-2)/sqr(1-r2) ~ studentDistr(df=n-2)
        corr = self.corrPearson(vv1, vv2)
        n = len(vv1)
        df = n - 2
        t = 100000000
        p = 0
        if abs(corr) < 0.9999999 and n > 1:
            t = float(corr * math.sqrt(n - 2)) / math.sqrt(1 - corr * corr)
            # print str(t)
            p = self.tTest_pValTwoTails(t, df)
        return corr, p

    def corrSpearmanRank(self, vx, vy):  # corrRank,p=
        (
            vrankFloat_x,
            vrankInt_x,
            vAddressInInitArrayOfElementOfSortedArray_x,
        ) = self.vrank(vx)
        (
            vrankFloat_y,
            vrankInt_y,
            vAddressInInitArrayOfElementOfSortedArray_y,
        ) = self.vrank(vy)
        corrRank, p = self.corrAndP(vrankFloat_x, vrankFloat_y)
        return corrRank, p

    def vrank(
        self, vx
    ):  # vrankFloat,vrankInt,vAddressInInitArrayOfElementOfSortedArray=
        vq = []
        i = 0
        for x in vx:
            vq.append([x, i, i, i])
            i += 1

        def MyFunc0(q):
            return q[0]

        def MyFunc1(q):
            return q[1]

        vq.sort(key=MyFunc0)
        i = 0
        i0 = 0
        vAddressInInitArrayOfElementOfSortedArray = []
        for q in vq:
            vAddressInInitArrayOfElementOfSortedArray.append(q[1])
            q[2] = i
            if vq[i0][0] < q[0]:
                ipp = 0.5 * (i0 + (i - 1))
                for j in range(i0, i):
                    vq[j][3] = ipp
                i0 = i
            i += 1
        ipp = 0.5 * (i0 + (i - 1))
        for j in range(i0, i):
            vq[j][3] = ipp
        vq.sort(key=MyFunc1)
        vrankInt = []
        vrankFloat = []
        for q in vq:
            vrankInt.append(q[2])
            vrankFloat.append(q[3])
        return vrankFloat, vrankInt, vAddressInInitArrayOfElementOfSortedArray

    def pValNormPos(self, x):
        # P(X>x)
        return 1 - self.ffNormalDistribution(x)

    def pValNormNeg(self, x):
        # P(X<x)
        return self.ffNormalDistribution(x)

    def pValNormAbs(self, x):
        # P(|X|>x)
        return 2 * (1 - self.ffNormalDistribution(abs(x)))

    def WilcoxonTest(self, vv1, vv2):  # uu,p=
        """
        #Wilcoxon-Mann-Whitney test
        #https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test
        #seq = sorted(x)
        #index = [seq.index(v) for v in x]
        """
        vv = []
        j = 0
        i = 0
        for v in vv1:
            vv.append([j, v, 1, i])
            i += 1
            j += 1
        i = 0
        for v in vv2:
            vv.append([j, v, 2, i])
            i += 1
            j += 1

        def MyFunc(q):
            return q[1]

        vv.sort(key=MyFunc)

        def avrank(vv, i0, i, vt):
            ii = (
                0.5 * (i0 + i - 1) + 1
            )  # +1 because ranks should start from 1, but i0 starts from 0
            vt.append(i - i0)
            for j in range(i0, i):
                vv[j][0] = ii

        i0 = 0
        v0 = vv[i0][1]
        vt = []
        i = 0
        for q in vv:
            if q[1] > v0:
                avrank(vv, i0, i, vt)
                v0 = q[1]
                i0 = i
            i += 1
        avrank(vv, i0, i, vt)

        r1 = 0
        for q in vv:
            if q[2] == 1:
                r1 += q[0]

        n1 = len(vv1)
        n2 = len(vv2)
        m = n1 * n2 * 0.5
        nnm1 = (n1 + n2) * (n1 + n2 - 1)
        sum = 0
        for t in vt:
            sum += float(t * t * t - t) / nnm1
        sigma2 = (float(1) / 12) * n1 * n2 * (n1 + n2 + 1 - sum)
        sigma = math.sqrt(sigma2)
        uu = r1 - 0.5 * n1 * (n1 + 1)
        p = 1
        if sigma > 0:
            xi = float(uu - m) / sigma
            p = self.pValNormAbs(xi)
        return uu, p

    def chi2_H0_p0_eq_p1(self, n0, n1):
        # H0: Pr(X=0)=Pr(X=1) => (n0-n1)^2 / (n1+n0) ~ chi^2(df=1)
        # chi^2=sum_i (nObs_i-nExp_i)^2/nExp_i, df=1
        # =(n0-0.5(n0+n1))^2 / (0.5(n0+n1)) + (n1-0.5(n0+n1))^2 / (0.5(n0+n1))
        if n0 + n1 < 1:
            return 0
        return float((n1 - n0) * (n1 - n0)) / (n1 + n0)

    def chi2_2x2(self, n00, n01, n10, n11):  # X2,df,nExpMin=
        # H0: Pr(X1=1, X2=1)=Pr(X1=1)*Pr(X2=1), i.e. X1 and X2 are independent => X2 ~ chi^2(df=1)
        n0_ = n00 + n01
        n1_ = n10 + n11
        n_1 = n01 + n11
        n_0 = n00 + n10
        if n0_ * n1_ * n_0 * n_1 == 0:
            return 0  # ns
        n = n0_ + n1_
        n00exp = (float(n0_) / n) * (float(n_0) / n) * n
        n01exp = (float(n0_) / n) * (float(n_1) / n) * n
        n10exp = (float(n1_) / n) * (float(n_0) / n) * n
        n11exp = (float(n1_) / n) * (float(n_1) / n) * n

        df = 1
        nExpMin = min(n00exp, n01exp, n10exp, n11exp)
        X2 = 0
        if nExpMin >= 5:
            X2 = float((n00 - n00exp) * (n00 - n00exp)) / n00exp
            X2 += float((n01 - n01exp) * (n01 - n01exp)) / n01exp
            X2 += float((n10 - n10exp) * (n10 - n10exp)) / n10exp
            X2 += float((n11 - n11exp) * (n11 - n11exp)) / n11exp
        else:
            pass  # need Fisher exact test
        return X2, df, nExpMin

    def chi2_mxn(self, vvn):  # X2,df,nExpMin=
        # H0: Pr(X1=a, X2=b)=Pr(X1=a)*Pr(X2=b), i.e. X1 and X2 are independent => X2 ~ chi^2(df=(nRows-1)*(nCols-1))
        nRows = len(vvn)
        nCols = len(vvn[0])
        vnRow = []
        vnCol = []
        n = 0
        for i in range(nRows):
            vnRow.append(0)
        for j in range(nCols):
            vnCol.append(0)
        for i in range(nRows):
            for j in range(nCols):
                v = vvn[i][j]
                n += v
                vnRow[i] += v
                vnCol[j] += v
        nExpMin = n
        X2 = 0
        df = (nRows - 1) * (nCols - 1)
        for i in range(nRows):
            for j in range(nCols):
                nExp = (float(vnRow[i]) / n) * vnCol[j]
                if nExpMin > nExp:
                    nExpMin = nExp
                if nExp > 0:
                    d = vvn[i][j] - nExp
                    X2 += float(d * d) / nExp
        return X2, df, nExpMin

    def yByLin(self, x1, y1, x2, y2, x):  # y=
        # y=ax+b, y1=a*x1+b, y2=a*x2+b => (y-y1)/(y2-y1)=(x-x1)/(x2-x1)
        if y2 == y1:
            return y1
        if x2 == x1:
            return 0.5 * (y1 + y2)
        return y1 + float((y2 - y1) * (x - x1)) / (x2 - x1)

    def notInUse_sortedAndNoOutLiersIfNeed(self, vv):  # vvPP=
        vvPP = []
        for v in vv:
            vvPP.append(float(v))
        vvPP.sort()
        return vvPP

    def rndNorm(self, a=0, sigma2=1):  # X=
        # ~N(a,sigma2)
        return random.gauss(a, math.sqrt(sigma2))

    def vvSortedAndNoOutLiersIfNeed___MonteCarlo(self, n, k=3, bPrint=False):
        """
        maxVarRelativeToKK=[]
        for ks in range(0,k):
                for ke in range(n-k,n):
                        maxVarRelativeToKK.append(1)

        nRuns=10
        for iRun in range(nRuns):
                vv=[]
                for i in range(n):
                        vv.append(self.rndNorm())
                vv.sort()
                #print str(vv)

                i=0
                v0=self.var(vv)
                vkk=self.var(vv[k:n-k])
                #print str(iRun)+": v0="+str(v0)+"\tvkk="+str(vkk)+"\tn="+str(len(vv))
                for ks in range(0,k):
                        for ke in range(n-k,n):
                                vvv=vv[ks:ke+1]
                                v=self.var(vvv)
                                #print str(ks)+"\t"+str(ke)+"\t"+str(v)+"\t"+str(len(vvv))
                                if maxVarRelativeToKK[i]<float(v)/vkk:
                                        maxVarRelativeToKK[i]=float(v)/vkk
                                i+=1
        if bPrint:
                print "vvSortedAndNoOutLiersIfNeed___MonteCarlo n="+str(n)+":"
        i=0
        for ks in range(0,k):
                for ke in range(n-k,n):
                        if bPrint:
                                print str(ks)+"\t"+str(ke)+"\t"+str(maxVarRelativeToKK[i])
                        i+=1
        return maxVarRelativeToKK
        """
        maxVarRelativeToKK = 1

        nRuns = 10
        for iRun in range(nRuns):
            vv = []
            for i in range(n):
                vv.append(self.rndNorm())
            vv.sort()
            # print str(vv)

            i = 0
            v0 = self.var(vv)
            vkk = self.var(vv[k : n - k])

            if maxVarRelativeToKK < float(v0) / vkk:
                maxVarRelativeToKK = float(v0) / vkk
        if bPrint:
            print(
                "vvSortedAndNoOutLiersIfNeed___MonteCarlo n="
                + str(n)
                + ", maxVarRelativeToKK="
                + str(maxVarRelativeToKK)
            )
        return maxVarRelativeToKK

    def vvSortedAndNoOutLiersIfNeed___vmaxVarRelativeToKK__make(self, nMax, k=3):
        vmaxVarRelativeToKK = []
        for n in range(nMax + 1):
            v = -1
            if n > 3 * k:
                v = self.vvSortedAndNoOutLiersIfNeed___MonteCarlo(n, k, False)
            vmaxVarRelativeToKK.append(v)
        self.vvSortedAndNoOutLiersIfNeed___k = k
        self.vvSortedAndNoOutLiersIfNeed___nMaxDone = nMax
        self.vvSortedAndNoOutLiersIfNeed___vmaxVarRelativeToKK = vmaxVarRelativeToKK

    def vvSortedAndNoOutLiersIfNeed(self, vv, nSet, k=3, bPrint=False):
        n = len(vv)
        vvCopy = []
        bTest = n < 1
        if bTest:
            n = nSet
            for i in range(n - 2):
                vvCopy.append(self.rndNorm())
            # vvCopy.append(0)
            # vvCopy.append(0)
            # vvCopy.append(self.rndNorm())
            # vvCopy.append(self.rndNorm())
            vvCopy.append(-3.5)
            vvCopy.append(3.5)
        else:
            for v in vv:
                vvCopy.append(v)
        if bPrint:
            print("vvSortedAndNoOutLiersIfNeed n=" + str(n) + ":")

        vvCopy.sort()
        if n <= 3 * k:
            return vvCopy  # can't exclude outliers from too short list
        nZeros = 0
        for v in vv:
            if v == 0:
                nZeros += 1
        if nZeros > 0.5 * n:
            return vvCopy  # too many zeros to make decizion on outliers
        iq1 = int(0.25 * n)
        iq3 = int(0.75 * n)
        if vvCopy[iq1] == vvCopy[iq3]:
            return vvCopy  # too many equal values to make decizion
        iq1 = int(0.15 * n)
        iq3 = int(0.65 * n)
        if vvCopy[iq1] == vvCopy[iq3]:
            return vvCopy  # too many equal values to make decizion
        iq1 = int(0.35 * n)
        iq3 = int(0.85 * n)
        if vvCopy[iq1] == vvCopy[iq3]:
            return vvCopy  # too many equal values to make decizion

        v0 = self.var(vvCopy[k : n - k])
        maxVarRelativeToKK = -1
        if (
            n <= self.vvSortedAndNoOutLiersIfNeed___nMaxDone
            and self.vvSortedAndNoOutLiersIfNeed___k >= k
        ):
            maxVarRelativeToKK = self.vvSortedAndNoOutLiersIfNeed___vmaxVarRelativeToKK[
                n
            ]
            # print "no monte carlo, n="+str(n)
        else:
            print(
                "MonteCarlo n="
                + str(n)
                + ", nDone="
                + str(self.vvSortedAndNoOutLiersIfNeed___nMaxDone)
            )
            maxVarRelativeToKK = self.vvSortedAndNoOutLiersIfNeed___MonteCarlo(
                n, k, bPrint
            )
        """
		i=0
		vb=[]
		#print str(iRun)+": v0="+str(v0)+"\t"+str(len(vv))
		print "ks\tke\tvCur\tvMaxExp\tp\to\t"+str(v0)
		for ks in range(0,k):
			for ke in range(n-k,n):
				vvv=vvCopy[ks:ke+1]
				v=self.var(vvv)
				vm=v0*maxVarRelativeToKK[i]
				vb.append(v<=vm)
				print str(ks)+"\t"+str(ke)+"\t"+str(v)+"\t"+str(vm)+"\t"+str(maxVarRelativeToKK[i])+"\t"+str(vb[i])
				i+=1
		"""
        m = self.mean(vvCopy)
        s = math.sqrt(v0 * maxVarRelativeToKK)
        if bPrint:
            print(
                "maxVarRelativeToKK="
                + str(maxVarRelativeToKK)
                + ", s="
                + str(s)
                + ", 3s="
                + str(3 * s)
            )
        vvPP = []
        for v in vvCopy:
            o = True
            if s > 0:
                x = float(v - m) / s
                o = abs(x) < 3
            else:
                o = v == 0
            if bPrint:
                print(str(v) + "\t" + str(x) + "\t" + str(o))
            if o:
                vvPP.append(v)
        if len(vv) - len(vvPP) > 4 * k:
            print(
                "k="
                + str(k)
                + ", n0="
                + str(len(vv))
                + ", nNoOutliers="
                + str(len(vvPP))
            )
            print(str(vv))
            print(str(vvPP))
            return vvCopy  # too many excluded
        return vvPP

    def permTest(self, vv1, vv2, nPerm=100000, kMax=5):  # m10,m20,d,pPerm=
        # H0: E(X1)=E(X2) => U=(k+1)/(nPerm-1) ~ U[0,1], pPerm=Pr(U<u_obs), kMax is for reduce the number of permutations to made
        m10 = self.mean(vv1)
        m20 = self.mean(vv2)
        d0 = abs(m10 - m20)
        n1 = len(vv1)
        n2 = len(vv2)
        vv = []
        for v in vv1:
            vv.append(v)
        for v in vv2:
            vv.append(v)
        k = 0
        for i in range(nPerm):
            random.shuffle(vv)
            m1 = self.mean(vv[0:n1])
            m2 = self.mean(vv[n1:])
            d = abs(m1 - m2)
            if d >= d0:
                k += 1
                if k >= kMax:
                    p = float(k + 1) / ((i + 1) + 1)
                    return m10, m20, d0, p
        p = float(k + 1) / (nPerm + 1)
        return m10, m20, d0, p

    def bDigit(self, s):
        return s in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def bNumberWithTest(self, s):  # f,b=
        n = len(s)
        if n == 0:
            return -1, False
        if n == 1:
            if self.bDigit(s):
                return int(s), True
            return -1, False
        ip = -1
        b = True
        for i in range(n):
            b = self.bDigit(s[i])
            if not b:
                if ip < 0:
                    if s[i] == ".":
                        ip = i
                        b = True
                if i == 0:
                    if s[i] == "-" or s[i] == "+":
                        b = True
        if s == "-." or s == "+.":
            return 0, True
        if b:
            return float(s), True
        return -1, False

    def is_number(self, s):  # f,b=
        try:
            x = float(s)
            return x, True
        except ValueError:
            return -1, False

    def vqValuesFDR(self, vp, n):  # vq=
        np = len(vp)
        if n < np:
            n = np
        if np < 1:
            return []
        if n == 1:
            return [vp[1]]

        vq = []
        vqq = []
        i = 0
        for p in vp:
            vqq.append([i, p, -1, p])
            i += 1

        def MyFunc1(q):
            return q[1]

        def MyFunc0(q):
            return q[0]

        vqq.sort(key=MyFunc1)
        for i in range(np):
            vqq[i][2] = i  # rank in sorted array
            vq.append(-1)

        FDR = 1
        for i in range(np):
            j = np - i - 1
            q = vqq[j]
            p = q[1]
            qVal = p * float(n + 1) / (j + 1)
            if FDR > qVal:
                FDR = qVal
            q[3] = FDR
            vq[q[0]] = q[3]
        return vq

    def vIndices_get(self, lst, element):
        # list of indexes where element <element> is situated in list <lst>
        result = []
        offset = -1
        while True:
            try:
                offset = lst.index(element, offset + 1)
            except ValueError:
                return result
            result.append(offset)

    # matrices (from https://integratedmlai.com/matrixinverse/)
    def matrix_print(self, Title, M):
        print(Title)
        for row in M:
            print([round(x, 3) + 0 for x in row])

    def matrix_pair_print(self, sAction, Title1, M1, Title2, M2):
        print(sAction)
        print(Title1, "\t" * int(len(M1) / 2) + "\t" * len(M1), Title2)
        for i in range(len(M1)):
            row1 = ["{0:+7.3f}".format(x) for x in M1[i]]
            row2 = ["{0:+7.3f}".format(x) for x in M2[i]]
            print(row1, "\t", row2)

    def matrix_0(self, rows, cols):  # A=
        A = []
        for i in range(rows):
            A.append([])
            for j in range(cols):
                A[-1].append(0.0)
        return A

    def matrix_copy(self, M):  # A=
        rows = len(M)
        cols = len(M[0])
        MC = self.matrix_0(rows, cols)
        for i in range(rows):
            for j in range(rows):
                MC[i][j] = M[i][j]
        return MC

    def matrix_multiply(self, A, B):  # C=
        rowsA = len(A)
        colsA = len(A[0])

        rowsB = len(B)
        colsB = len(B[0])
        if colsA != rowsB:
            print("Number of A columns must equal number of B rows.")
            sys.exit()
        C = self.matrix_0(rowsA, colsB)
        for i in range(rowsA):
            for j in range(colsB):
                total = 0
                for ii in range(colsA):
                    total += A[i][ii] * B[ii][j]
                C[i][j] = total
        return C

    # from https: //stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
    def matrix_gaussManipulations(self, A):  # B=
        def eliminate(r1, r2, col, target=0):
            fac = (r2[col] - target) / r1[col]
            for i in range(len(r2)):
                r2[i] -= fac * r1[i]

        n = len(A)
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[i][j] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    print("MATRIX NOT INVERTIBLE")
                    return -1
            for j in range(i + 1, n):
                eliminate(A[i], A[j], i)
        for i in range(n - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                eliminate(A[i], A[j], i)
        for i in range(n):
            eliminate(A[i], A[i], i, target=1)
        return A

    def inverse(a):

        tmp = [[] for _ in a]
        for i, row in enumerate(a):
            assert len(row) == len(a)
            tmp[i].extend(row + [0] * i + [1] + [0] * (len(a) - i - 1))
        gauss(tmp)
        ret = []
        for i in range(len(tmp)):
            ret.append(tmp[i][len(tmp[i]) // 2 :])
        return ret


class clTableOfTxt:
    def __init__(self):
        self.rows = []
        self.shapka = self.clRow()
        self.nRows = 0
        self.nCols = 0

        self.vColText = []
        self.vCol_iCol = -1

    class clRow:
        def __init__(self):
            self.vCellText = []
            self.id = -1

        def readRowFromString(self, s, bFirstColNoNeedToRead):
            ss = s.split("\n")  # max split = 1
            s1 = ss[0]
            self.vCellText = s1.split("\t")
            if bFirstColNoNeedToRead:
                self.vCellText = self.vCellText[1:]

        def s_get(self):
            ic = 0
            s = ""
            for sc in self.vCellText:
                if ic > 0:
                    s += "\t"
                s += sc
                ic += 1
            return s

    def printToFile(self, sFileName, bShapka):
        f = open(sFileName, "w")
        if bShapka:
            s = "iRow"
            for s1 in self.shapka.vCellText:
                s += "\t" + s1
            f.write(s + "\n")
        iRow = 0
        for row in self.rows:
            s = str(iRow)
            for s1 in row.vCellText:
                s += "\t" + s1
            f.write(s + "\n")
            iRow += 1
        f.close

    def readFromFile(self, sFileName, bShapka, bFirstColNoNeedToRead):
        self.rows = []
        self.shapka = self.clRow()
        self.nRows = 0
        self.nCols = 0
        f = open(sFileName, "r")
        # usually newline=chr(10)="\n"=<LF> in Linux, chr(13)+chr(10)=<CR>+<LF> in windows
        n = 0
        s1 = ""
        for s in f:
            s1 = s
            n += 1
        f.close()
        f = open(sFileName, "r") if n > 1 else s1.split(chr(13))
        for s in f:
            # print "832"
            if bShapka:
                self.shapka.readRowFromString(s, bFirstColNoNeedToRead)
                self.nCols = len(self.shapka.vCellText)
                # print str(self.nCols)
                bShapka = False
            else:
                row = self.clRow()
                row.readRowFromString(s, bFirstColNoNeedToRead)
                nColsInRow = len(row.vCellText)
                if nColsInRow > self.nCols:
                    self.nCols = nColsInRow
                # print row.vCellText
                self.rows.append(row)
                self.nRows += 1
                # print str(self.nRows)
        if n > 1:
            f.close

    def vColText_make(self, vCol_iCol):
        self.vCol_iCol = vCol_iCol
        self.vColText = []
        # print "vCol_iCol="+str(vCol_iCol)
        for row in self.rows:
            self.vColText.append(row.vCellText[vCol_iCol])
            # print "vCol_iCol="+row.vCellText[vCol_iCol]
            pass

    def iRow_get(self, textCol, iCol):
        if iCol != self.vCol_iCol:
            self.vColText_make(iCol)
        iRow = -1
        if textCol in self.vColText:
            iRow = self.vColText.index(textCol)
        return iRow

    def iRows_get(self, textCol, iCol):
        if iCol != self.vCol_iCol:
            self.vColText_make(iCol)

        # def get_indexes(x, xs):
        get_indexes = lambda x, xs: [i for (y, i) in zip(xs, range(len(xs))) if x == y]
        return get_indexes(textCol, self.vColText)

    def sWithoutChr10Chr13(self, s0):
        s = ""
        for s1 in s0:
            if s1 != chr(10) and s1 != chr(13):
                s += s1
        return s

    def sChangeAllTabsToSpace(self, s0):
        s = ""
        for s1 in s0:
            if s1 != "\t":
                s += s1
            else:
                s += " "
        return s

    def sNoFinishingSpaces(self, s0):
        sSS = ""
        s = ""
        for s1 in s0:
            if s1 != " ":
                if len(sSS) > 0:
                    s += sSS
                    sSS = ""
                s += s1
            else:
                sSS += " "
        return s

    def sChangeGroupOfSpacesToSingleTab(self, s0):
        sSS = ""
        s = ""
        for s1 in s0:
            if s1 != " ":
                if len(sSS) > 0:
                    s += "\t"
                    sSS = ""
                s += s1
            else:
                sSS += " "
        if len(sSS) > 0:
            s += "\t"
        return s


class clKorol:
    def vrnd(self, nInd, index=0):
        vx = []
        for iInd in range(nInd):
            x = 0
            if index == 0:
                x = random.gauss(0, 1)
            vx.append(x)
        return vx

    def vBootstreap(self, vx):
        vb = []
        nInd = len(vx)
        for iInd in range(nInd):
            vb.append(vx[random.randrange(0, nInd)])
        return vb

    def vJackknife(self, vx, p):
        nToSelect = int(p * len(vx))
        # print "nToSelect="+str(nToSelect)+", len(vx)="+str(len(vx))
        vy = random.sample(vx, nToSelect)
        return vy

    def pValBasedOnConfidenceIntervals(self, n1, oneMa1, n2, oneMa2):
        # X~N(0,1)
        # Y~N(0,1)
        # mean(X)~N(0,1/nX)
        # mean(Y)~N(0,1/nY)
        # mean(X)-mean(Y)~N(0,1/nX+1/nY)
        # Pr(|(X-EX)/sqrt(Var(X))|<z_{1-a/2})=1-a
        # Pr(-z_{1-a/2}<(X-EX)/sqrt(Var(X))<z_{1-a/2})=1-a
        # Pr(-z_{1-a/2}<(mean(X)-a)/sqrt(1/nX)<z_{1-a/2})=1-a
        # Pr(mean(X)-sqrt(1/nX)*z_{1-a/2} < a < mean(X)+sqrt(1/nX)*z_{1-a/2})=1-a
        # Pr(mean(X)-mean(Y)<sqrt(1/nX+1/nY) z_{1-a})=1-a
        # Pr(|mean(X)-mean(Y)|<sqrt(1/nX+1/nY) z_{1-a/2})=1-a
        # Pr(|mean(X)-mean(Y)|>sqrt(1/nX+1/nY) z_{1-a/2})=a
        # Pr(|mean(X)-mean(Y)|>sqrt(1/nX)*z_{1-aX/2}+sqrt(1/nY)*z_{1-aY/2})=a
        # => sqrt(1/nX)*z_{1-aX/2}+sqrt(1/nY)*z_{1-aY/2}=sqrt(1/nX+1/nY) z_{1-a}
        # => z_{1-a/2} = (sqrt(nY)*z_{1-aX/2}+sqrt(nX)*z_{1-aY/2})/sqrt(nX+nY)
        VovaMath = clVovaMath()
        a1 = 1 - oneMa1
        a2 = 1 - oneMa1
        z1 = VovaMath.zNormalDistribution(1 - 0.5 * a1)
        z2 = VovaMath.zNormalDistribution(1 - 0.5 * a2)
        z = (float(math.sqrt(n2) * z1 + math.sqrt(n1) * z2)) / math.sqrt(n1 + n2)
        oneMaD2 = VovaMath.ffNormalDistribution(z)
        a = 2 * (1 - oneMaD2)
        return a

    def pValBasedOnConfidenceIntervals_test(self):
        vn = [10, 20, 30, 40, 50, 100, 500, 1000]
        voneMa = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
        print("n1" + "\t" + "n2" + "\t" + "b1" + "\t" + "b2" + "\t" + "p")
        for n1 in vn:
            for n2 in vn:
                if n2 <= n1:
                    for oneMa1 in voneMa:
                        for oneMa2 in voneMa:
                            p = self.pValBasedOnConfidenceIntervals(
                                n1, oneMa1, n2, oneMa2
                            )
                            print(
                                str(n1)
                                + "\t"
                                + str(n2)
                                + "\t"
                                + str(oneMa1)
                                + "\t"
                                + str(oneMa2)
                                + "\t"
                                + str(p)
                            )

    def testResampling(self, nResampling, vx, p=-1):  # mm,s2m,ms2,s2s2=
        # E(m)=EX=0
        # Var(m)=Var(x)/n=1/n
        # STDV(m)=sqrt(Var(m))=1/sqrt(n)
        #
        # S2*(n-1)/Var(x) ~ chi^2_{df=n-1}, E(chi^2_{df})=df, Var(chi^2_{df})=2 df
        # E(S2)=Var(x)=1
        # Var(S2)=2/(n-1)
        # STDV(S2)=sqrt(2/n-1)=[n=100]=0.14
        #
        vm = []
        vs2 = []
        VovaMath = clVovaMath()
        for iResampling in range(nResampling):
            vb = self.vJackknife(vx, p) if p >= 0 else self.vBootstreap(vx)
            m = VovaMath.mean(vb)
            s2 = VovaMath.var(vb)
            vm.append(m)
            vs2.append(s2)
        mm = VovaMath.mean(vm)
        s2m = VovaMath.var(vm)
        ms2 = VovaMath.mean(vs2)
        s2s2 = VovaMath.var(vb)
        return mm, s2m, ms2, s2s2

    class cltestResampling_res:
        def __init__(self, n=100, nInd=100, nResampling=10000, p=-1, index=0):
            if n > 0:
                Korol = clKorol()
                vmm = []
                vs2m = []
                vms2 = []
                vs2s2 = []
                VovaMath = clVovaMath()
                for i in range(n):
                    vx = Korol.vrnd(nInd, index)
                    mm, s2m, ms2, s2s2 = Korol.testResampling(nResampling, vx, p)
                    vmm.append(mm)
                    vs2m.append(s2m)
                    vms2.append(ms2)
                    vs2s2.append(s2s2)
                self.mmm = VovaMath.mean(vmm)
                self.s2mm = VovaMath.var(vmm)
                self.mms2 = VovaMath.mean(vms2)
                self.s2ms2 = VovaMath.var(vms2)
                self.ms2m = VovaMath.mean(vs2m)
                self.s2s2m = VovaMath.var(vs2m)
                self.ms2s2 = VovaMath.mean(vs2s2)
                self.s2s2s2 = VovaMath.var(vs2s2)

        def sShapka(self):
            return (
                "\t"
                + "mmm"
                + "\t"
                + "s2mm"
                + "\t"
                + "mms2"
                + "\t"
                + "s2ms2"
                + "\t"
                + "ms2m"
                + "\t"
                + "s2s2m"
                + "\t"
                + "ms2s2"
                + "\t"
                + "s2s2s2"
            )

        def s(self):
            s1 = "\t" + str(self.mmm) + "\t" + str(math.sqrt(self.s2mm))
            s1 += (
                "\t"
                + str(math.sqrt(self.mms2))
                + "\t"
                + str(math.sqrt(math.sqrt(self.s2ms2)))
            )
            s1 += (
                "\t"
                + str(math.sqrt(self.ms2m))
                + "\t"
                + str(math.sqrt(math.sqrt(self.s2s2m)))
            )
            s1 += (
                "\t"
                + str(math.sqrt(math.sqrt(self.ms2s2)))
                + "\t"
                + str(math.sqrt(math.sqrt(math.sqrt(self.s2s2s2))))
            )
            return s1

    def studyResambling(self):
        n = 10000
        # ds=0.1
        # sMax=10
        VovaMath = clVovaMath()
        vnInd = [10, 20, 30, 40, 50, 100, 150, 200, 500, 1000, 5000, 10000]
        vnResampling = [10, 100, 1000, 10000, 100000]
        vp = [
            -1,
            95,
            90,
            85,
            80,
            75,
            70,
            65,
            60,
            55,
            50,
            45,
            40,
            35,
            30,
            25,
            20,
            15,
            10,
            5,
        ]

        n = 100
        vnInd = [100]
        vnResampling = [100, 1000]
        # vp=[-1,80]

        i = 0
        for p in vp:
            p *= 0.01
            vp[i] = p
            i += 1

        sFileName = "Korol_studyResambling.txt"
        f = open(sFileName, "w")

        index = 0
        mmm = self.cltestResampling_res(0)
        s = "nResampling" + "\t" + "nInd" + "\t" + "p" + mmm.sShapka()
        print(s)
        f.write(s + "\n")
        for nResampling in vnResampling:
            for nInd in vnInd:
                for p in vp:
                    mmm = self.cltestResampling_res(n, nInd, nResampling, p, index)

                    s1 = "BS" if p <= 0 else "JK" + str(int(p * 100)) + "%"
                    s = str(nResampling) + "\t" + str(nInd) + "\t" + s1 + mmm.s()
                    print(s)
                    f.write(s + "\n")
        f.close()


class clVovaServ:
    def listOfFiles_get(self, sPath, bPrint, sExt):
        sFiles = []
        # r=root, d=directories, f = files
        # sExt='.txt'
        for r, d, f in os.walk(sPath):
            for file in f:
                s = os.path.join(r, file)
                b = sExt == ".*"
                if not b:
                    if len(s) > len(sExt):
                        if s[len(s) - len(sExt) : len(s)] == sExt:
                            b = True
                if b:
                    sFiles.append(s)
                    # files.append(f)
        if bPrint:
            for f in sFiles:
                print(f)
        return sFiles

    def sFilePureName_get(self, s):
        n = len(s)
        a = 0
        b = n
        for i in range(n):
            if s[i] == "\\":
                a = i + 1
            if s[i] == ".":
                b = i
        return s[a:b]

    def mergeFiles(self, sPath, bPrint, sExt, sFileName, bAddFileName):
        print("mergeFiles...")
        sFiles = self.listOfFiles_get(sPath, False, sExt)
        fileMerged = open(sFileName, "w")
        n = 0
        for s in sFiles:
            f = open(s, "r")
            k = 0
            sss = self.sFilePureName_get(s)
            for ss in f:
                k += 1
                n += 1
                # text_file.write("Purchase Amount: %s" % TotalAmount)
                if bAddFileName:
                    ss = sss + "\t" + ss
                fileMerged.write(ss)
            f.close
            print(s + "\t" + str(k))
        fileMerged.close
        print(
            "Total:\t"
            + str(n)
            + "\tlines were merged from "
            + str(len(sFiles))
            + " files"
        )
        print("mergeFiles...Finished")

    def nRowsInFile_get(self, sFileName):
        # n = len(open(sFileName).readlines(  ))
        n = 0
        # for line in open(sFileName).xreadlines(  ):
        # 	n += 1
        def _make_gen(reader):
            b = reader(1024 * 1024)
            while b:
                yield b
                b = reader(1024 * 1024)

        def rawgencount(filename):
            f = open(filename, "rb")
            f_gen = _make_gen(f.raw.read)
            return sum(buf.count(b"\n") for buf in f_gen)

        # return n
        return rawgencount(sFileName)

    def vSortAndDelRepeats_get(
        self, v
    ):  # vSortAndDelRepeats=clVovaServ().vSortAndDelRepeats_get(v)
        vSort = []
        for a in v:
            vSort.append(a)
        vSort.sort()
        vSortAndDelRepeats = []
        i = 0
        a_prev = ""
        for a in vSort:
            if i == 0:
                vSortAndDelRepeats.append(a)
            else:
                if a != a_prev:
                    vSortAndDelRepeats.append(a)
            i += 1
            a_prev = a
        return vSortAndDelRepeats


class clRecombination:
    def __init__(self):
        self.r = 0

    def rByDist(self, d_cM):  # r=
        # Haldane
        if d_cM <= 0:
            return 0
        return 0.5 * (1 - math.exp(-float(d_cM) * 2 / 100))

    def distByR(self, r):  # d_cM=
        # Haldane
        if r <= 0:
            return 0
        rMax = 0.5 - 0.01
        if r > rMax:
            return self.distByR(rMax)
        return -math.log(1 - 2 * r) * 100 / 2

    def rML(self, nRec, nNotRec):  # rObs=
        n = nRec + nNotRec
        if n == 0:
            return 0.5  # no data => no linkage
        return float(nRec) / n

    def rSTDV(self, r, n):  # STDV(rObs)=
        if r <= 0 or r >= 0.5 or n < 2:
            return 0
        return math.sqrt(r * (1 - r) / n)

    def rMin(self, nRec, nNotRec, alphaSTDV):
        # lower bound of confidece interval for r
        r = self.rML(nRec, nNotRec)
        s = self.rSTDV
        r = r - alphaSTDV * s
        if r <= 0:
            return 0
        return r

    # @staticmethod
    def rMax(self, nRec, nNotRec, alphaSTDV):
        # upper bound of confidece interval for r
        r = self.rML(nRec, nNotRec)
        s = self.rSTDV(r, nRec + nNotRec)
        r = r + alphaSTDV * s
        if r >= 0.5:
            return 0.5
        return r

    # @staticmethod
    def rMaxInCaseZero(self, nNotRec, pZero):
        # pZero=(1-r)^nNotRec = probability to observe no recombination (in nNotRec observations)
        # =>1-r=pZero^(1/nNotRec)
        # =>r=1-pZero^(1/nNotRec)
        if nNotRec == 0:
            return 0
        r = 1 - math.exp(1 / float(nNotRec) * math.log(pZero))
        if r < 0:
            return r
        if r > 0.5:
            return 0.5
        return r

    def nnn(self, g1, g2, bPhasesAreGiven):  # nR,nN,nMissed=
        # g1 = array of genotypes in marker1 for n individuals
        # g2 = array of genotypes in marker2 for n individuals
        # g[i]=-1 => missing
        # nR = number of individuals with recombination between marker1 and marker2
        # nN = number of individuals with no recombination between marker1 and marker2
        # nMissing = number of individuals with missed allele in marker1 or in marker2
        nMissed = 0
        nR = 0
        nN = 0
        n = len(g1)
        for i in range(n):
            a1 = g1[i]
            a2 = g2[i]
            if a1 < 0 or a2 < 0:
                nMissed += 1
            else:
                if a1 == a2:
                    nN += 1
                else:
                    nR += 1
        if not bPhasesAreGiven:
            if nR > nN:
                return nN, nR, nMissed
        return nR, nN, nMissed


class clMarkerName:
    # ne gotovo, not in use
    def __init__(self, s):
        # NODE_10007_length_5053_cov_2.49574
        # NODE_10018_length_5038_cov_2.43377_B0_start3811,4147,4147,4147
        # NODE_11682_length_3520_cov_1.99117___2864
        # scaffold1|size1555347___99
        # tig00000049___15616
        # s1p1327199
        # scaffold1p3196252
        # ScbnsAo_1___161534

        self.s = s  # original inputed name
        self.bScaffold = False
        self.sCoor = ""
        self.sMapPart = ""
        self.sMapPartFull = ""
        self.sSize = ""
        self.MapPartSize = None
        self.coor = None
        self.bOk = False
        if len(s) >= len("scaffold"):
            # scaffold1|size1555347___99
            # scaffold1p3196252
            if s[0:8] == "scaffold" or s[0:8] == "Scaffold":
                self.bScaffold = True
                sPP = s[8:]
                self.sMapPartFull = s[0:8]  # "scaffold"
                if "|" in sPP:  # 1|size1555347___99
                    ss = sPP.split("|")
                    self.sMapPart = ss[0]  # 1
                    if len(ss[1]) > 4:
                        sPP = ss[1]  # size1555347___99
                        if sPP[0:4] == "size":
                            if "___" in sPP:
                                ss = sPP.split("___")
                                self.sSize = ss[0][4:]  # 1555347
                                self.sCoor = ss[1]  # 99
                                self.MapPartSize = int(self.sSize)  # 1555347
                                self.coor = float(self.sCoor)  # 99
                                self.bOk = True
                else:
                    if "p" in sPP:  # 1p3196252
                        ss = sPP.split("p")
                        self.sMapPart = ss[0]  # 1
                        self.sCoor = ss[1]  # 3196252
                        self.coor = float(self.sCoor)  # 3196252
                        self.bOk = True
                if self.bOk:
                    self.sMapPartFull += self.sMapPart  # scaffold1
        if not self.bOk:
            if "___" in s:
                # NODE_11682_length_3520_cov_1.99117___2864
                # scaffold1|size1555347___99
                # tig00000049___15616
                # ScbnsAo_1___161534
                ss = s.split("___")
                # self.sMapPart=ss[0][1:]#1
                self.sMapPartFull = ss[0]  # NODE_11682_length_3520_cov_1.99117
                self.sCoor = ss[1]  # "2864"
                self.coor = float(self.sCoor)  # 2864
                self.bOk = True
            else:
                if (s[0] == "s") and ("p" in s):
                    # s1p1327199
                    ss = s.split("p")
                    # self.sMapPart=ss[0][1:]#1
                    self.sMapPartFull = ss[0]  # s1
                    self.sCoor = ss[1]  # 1327199
                    self.coor = float(self.sCoor)  # 3196252
                    self.bOk = True

    def s___scaffold_iScaf_p_iCoor(self):  # scaffold1p3196252
        return "scaffold" + self.sMapPart + "p" + str(int(self.sCoor))

    def sCtg_coor_get(self, bAllBefore___=False):
        # scaffold39p2193284
        # ss=s.split('p')
        # return ss[0],int(ss[1])
        if bAllBefore___:
            vs = self.s.split("___")
            return vs[0], int(self.coor)
        return self.sMapPartFull, int(self.coor)


class clMarkerWithGenotypesOfAllIndivids:
    def __init__(self):
        self.id = -1
        self.g = []  # array of "-1" = missing data, 0 or 1, [iInd]
        self.nIndivids = 0
        # self.ploidy=1#vsegda

        self.sState0 = "0"
        self.sState1 = "1"
        self.sState2 = "2"
        self.sStateMissing = "-"

        self.phase = (
            -1
        )  # unknown (to identify from what parent allele 0; allele 1 from the another) (-1=unknown, 0 or 1)

        self.sSep = ""  # symbol(s) used for separation between individuals, e.g., "", \t, " ", etc.

        self.sMarker = ""

        self.idType = 0
        # 0: only two states: 0, 1, -1=missing (good for di-allelic: haploids (A/a/Missing), RILs (AA/aa/(Aa or Missing)), Backccross(aa/Aa/Missing))
        # 1-3: di-haploid F1xF1:
        # 	Two parent lines, all loci are di-allelic. Types of markers:
        # 			1 - Aa in mother, aa in father (expected A:a= 0.25:0.75), but in children aa:Aa=0.5:0.5
        # 			2 - aa in mother, Aa in father (expected A:a= 0.25:0.75), but in children aa:Aa=0.5:0.5
        # 			3 - Aa in mother, Aa in father (expected A:a= 0.5:0.5)
        # 		NB! impossible to score recombination rates between markers of type 1 and 2
        # 		NB! calculation of recombination rates within classes is regular (like in idType=0, hence we use 0 and 1 for aa and Aa within classes)
        # 		NB! calculation of recombination within class 2: can be zero, one in mother, one in father, two recombinations
        # 		Let designate in class 3: 0 for aa, 1 for Aa, 2 for aa
        # 		NB! for markers of type 2 phase is vector: (phaseMother, phaseFather)
        # 		In short distances we expect small recombination rates between markers of types 1 and 3 or 2 and 3
        # 4: diploid, unknown phases. Three states: 0(aa), 1(Aa), 2(AA), -1=missing data

        # from vcf file
        self.sChr = ""  # seq ctg
        self.pos = 0  # pos on seq ctg
        # self.vPos=[]#list of positions on seq ctg

        # basic statistics
        self.nIndWithState = []  # [iState], iState=0 or 1
        self.nIndMissed = 0

        self.nHapWithState = []  # [iState], iState=0 or 1
        self.nHapMissed = 0
        self.nDipWithState = []  # [iState], iState=0 , 1 or 2
        self.nDipMissed = 0

        self.pp = 0  # polymorphism value: P=min(p[0],p[1])
        self.chi2 = 0  # chi2 of equal segregation

        # privmanMap information (if avaliable)
        #
        # physical position of marker on physical contig based on marker name only (if vcf file is not avaliable)
        # NODE_10702_length_4364_cov_2.38953_B0_start1463,1743
        # NODE_10702_length_4364_cov_2.38953	1743
        self.PrivmanCtgIndex = -1  # 10702
        self.ctgLength = -1  # 4364
        self.vPrivmanvPosOnCtg = []  # [1463,1743]
        #
        # position on Privman's genetic map
        # 	temporally: first only
        self.PrivmanLG = ""
        self.PrivmanCoorOnLG = -1

    def sg(self, sSep, bAlleleNumbers=False, iMSTformat=0):
        s = ""
        i = 0
        if iMSTformat > 0:
            # poka tak. see http://www.mstmap.org/
            # indeed, for RIL possible also "X" for heterozygotes
            s0 = "A"
            s1 = "B"
            if iMSTformat == 2:
                s0 = "B"
                s1 = "A"
            if iMSTformat == 3:
                if self.nIndWithState[1] > self.nIndWithState[0]:
                    s0 = "B"
                    s1 = "A"
            for a in self.g:

                i = i + 1
                if i > 1:
                    s = s + "\t"
                if a < 0:
                    s = s + "-"
                if a == 0:
                    s = s + s0
                if a == 1:
                    s = s + s1
            return s
        for a in self.g:
            i = i + 1
            if i > 1:
                s = s + sSep
            if a < 0:
                s = s + self.sStateMissing
            else:
                if bAlleleNumbers:
                    s += str(a)
                else:
                    if self.idType == 0:
                        if a == 0:
                            s = s + self.sState0
                        if a == 1:
                            s = s + self.sState1
                        if a == 2:
                            s = s + self.sState2
                    if self.idType == 4:
                        if a == 0:
                            s = s + self.sState0  # homo allele0
                        if a == 1:
                            s = s + self.sState2  # Hetero
                        if a == 2:
                            s = s + self.sState1  # homo allele1

        return s

    def s(self, sSep, bAlleleNumbers=False, iMSTformat=False):
        s0 = self.sMarker
        if iMSTformat == 1:
            s0 = "1" + s0
        if iMSTformat == 2:
            s0 = "2" + s0
        return s0 + "\t" + self.sg(sSep, bAlleleNumbers, iMSTformat)

    def sStatistics(self, bShapka=False):
        s0 = "marker"
        if not bShapka:
            s0 = self.sMarker
        s = s0

        s0 = "n0+n1"
        if not bShapka:
            n = self.nIndWithState[0] + self.nIndWithState[1] + self.nIndWithState[2]
            s0 = str(n)
        s = s + "\t" + s0

        s0 = "nMiss"
        if not bShapka:
            s0 = str(self.nIndMissed)
        s = s + "\t" + s0

        s0 = "P"
        if not bShapka:
            s0 = "{:1.2f}".format(self.pp)
        s = s + "\t" + s0

        s0 = "Chi2"
        if not bShapka:
            s0 = "{:1.2f}".format(self.chi2)
        s = s + "\t" + s0

        if self.idType == 4:
            He_exp = 0
            He_obs = 0
            F_IT = 0
            n = 0
            if not bShapka:
                """
                if self.pp>0:
                        n=self.nIndWithState[0]+self.nIndWithState[1]+self.nIndWithState[2]
                        p0=float(2*self.nIndWithState[0]+self.nIndWithState[1])/(2*n)
                        p1=float(2*self.nIndWithState[2]+self.nIndWithState[1])/(2*n)
                        He_exp=2*p0*p1
                        He_obs=float(self.nIndWithState[1])/n
                        F_IT=1-float(He_obs)/He_exp
                """
                n, pp, He_obs, He_exp, F_IT = self.n_pp_Hobs_Hexp_F_IT(
                    self.nIndWithState
                )
            s = s + "\t" + ("He_exp" if bShapka else "{:1.2f}".format(He_exp))
            s = s + "\t" + ("He_obs" if bShapka else "{:1.2f}".format(He_obs))
            s = s + "\t" + ("F_IT" if bShapka else "{:1.2f}".format(F_IT))
        return s

    def bGood(self, nNotMissedMin=51):
        nNotMissed = self.nIndWithState[0] + self.nIndWithState[1]
        bOk = nNotMissed >= nNotMissedMin
        if bOk:
            bOk = (nNotMissed + (3 - self.chi2) * 50) > 0
        return bOk

    def bMayBeInteresting(self, nNotMissedMin=10):
        return (self.nIndWithState[0] >= nNotMissedMin) and (
            self.nIndWithState[1] >= nNotMissedMin
        )

    def get(self, g, nIndivids, sMarker, sChr, pos):
        self.g = []
        if nIndivids > 0:
            self.nIndivids = nIndivids
            for i in range(nIndivids):
                self.g.append(-1)
            i = 0
            for a in g:
                self.g[i] = a
                i += 1
        # poka
        self.sState0 = "0"
        self.sState1 = "1"
        self.sState2 = "2"
        self.sStateMissing = "-"
        self.sSep = ""

        self.sMarker = sMarker
        self.sChr = sChr
        self.pos = pos
        self.calc()

    def readSimple(self, s, sSep, sState0, sState1, sStateMissing, nIndivids, idType):
        self.idType = idType
        if not (idType == 0 or idType == 4):
            return 1 / (1 - 1)  # error (poka)
        self.sState0 = sState0
        self.sState1 = sState1
        self.sState2 = "2"  # poka
        self.sStateMissing = sStateMissing
        self.sSep = sSep

        # del \n in the end of string
        ss = s.split("\n")  # max split = 1
        s = ss[0]

        s0 = s.split("\t", 1)  # max split = 1
        self.sMarker = s0[0]

        # read genotypes
        ssg = []
        sg = []
        if len(s0) > 1:
            sg = s0[1]
            if len(self.sSep) > 0:
                ssg = sg.split(self.sSep)
            else:
                ssg = sg
        self.g = []
        self.nIndivids = 0
        for sa in ssg:
            if nIndivids == 0 or self.nIndivids < nIndivids:
                g = -1
                if sa == self.sState0:
                    g = 0
                if sa == self.sState1:
                    g = 1
                if idType == 4:
                    if sa == self.sState2:
                        g = 2
                self.nIndivids = self.nIndivids + 1
                self.g.append(g)
        while self.nIndivids < nIndivids:
            g = -1
            self.g.append(g)
            self.nIndivids = self.nIndivids + 1

        self.calc()
        # print(self.sMarker)
        # print(ssg)
        # print(self.g)
        # print(self.nIndWithState)
        # print(self.nIndMissed)
        # print(self.nIndivids)
        # s1=s.split(self.sSep)
        pass

    def readDiHaploidF1xF1(self, s):
        # Order	Linkage Group (LG)	Marker Name	Position	Mb111	Mb121	P1	P2	P3	P4	P5	P6	P7	P8	P9	P10	P11	P12	P13	P14	P15	P16	P17	P18	P19	P21	P22	P23	P24	P25	P26	P27	P28	P29	P30	P31	P32	P33	P34	P35	P36	P37	P38	P39	P40	P41	P42	P43	P44	P45	P46	P47	P48	P49	P50	P51	P52	P53	P54	P55	P56	P57	P58	P59	P60	P61	P62	P63	P64	P65	P66	P67	P68	P69	P70	P71	P72	P73	P74	P75	P76	P77	P78	P79	P80	P81	P82	P83	P84	P86	P87	P88	P89	P90	P91	P92	P93	P94	P95	P96	P101	P102	P103	P104	P105	P106	P107	P108	P109	P110	P111	P113	P114	P115	P116	P117	P118	P119	P120	P121	P122	P123	P125	P126	P127	P128	P129	P130	P131	P132	P133	P134	P135	P137	P138	P139	P140	P141	P142	P143	P144	P145	P146	P147	P149	P150	P151	P153	P154	P155	P156	P157	P158	P159	P161	P162	P163	P164	P165	P166	P167	P168	P169	P170	P171	P173	P174	P175	P176	P177	P178	P179	P180	P181	P182	P183	P185	P186	P187	P188	P189	P191	P192	P193	P194	P195
        # 1	LG1	M10597	0.000	lm	ll	lm	ll	lm	lm	lm	lm	lm	lm	lm	lm	lm	ll	--	lm	lm	lm	lm	lm	lm	lm	lm	lm	ll	lm	ll	lm	lm	lm	ll	lm	ll	ll	ll	lm	ll	ll	lm	lm	ll	lm	ll	lm	ll	ll	lm	lm	ll	lm	lm	ll	--	--	lm	lm	--	ll	lm	ll	lm	ll	lm	lm	lm	ll	lm	ll	ll	lm	lm	lm	lm	ll	lm	ll	lm	ll	lm	lm	lm	lm	lm	lm	ll	lm	lm	lm	lm	lm	ll	ll	lm	lm	lm	lm	ll	lm	ll	--	--	--	lm	ll	--	ll	lm	ll	ll	lm	lm	lm	lm	--	--	--	--	lm	lm	lm	lm	ll	--	--	--	--	lm	lm	--	--	ll	lm	--	--	lm	ll	ll	ll	lm	--	lm	ll	ll	--	ll	--	--	lm	--	ll	lm	--	lm	ll	lm	lm	ll	lm	lm	lm	lm	lm	--	lm	ll	lm	--	lm	lm	ll	lm	lm	lm	lm	lm	lm	lm	ll	lm	ll	lm	ll
        # ...
        # 3	LG1	M55765	3.783	nn	np	--	nn	np	np	np	np	np	np	np	np	np	nn	nn	nn	--	--	np	np	np	--	np	np	nn	np	nn	nn	np	np	nn	nn	nn	nn	nn	np	nn	nn	nn	--	nn	np	nn	nn	nn	nn	np	nn	--	np	np	--	np	nn	nn	nn	nn	nn	--	np	nn	nn	np	nn	--	nn	np	nn	nn	np	--	--	np	nn	np	np	np	nn	np	np	nn	np	--	nn	nn	--	--	np	nn	--	nn	np	np	np	np	np	nn	np	--	nn	--	--	np	nn	nn	np	np	nn	np	--	--	nn	np	--	np	np	np	np	np	np	--	nn	nn	np	np	nn	np	--	--	nn	np	np	np	--	np	nn	nn	np	--	--	np	nn	nn	--	nn	np	--	--	nn	--	np	np	nn	nn	--	--	nn	--	nn	nn	np	nn	nn	nn	--	nn	np	np	np	nn	--	np	np	np	np	np	--	--	nn	nn	--	np
        # ...
        # 11	LG1	M08944	11.230	hk	hk	hk	hk	hk	hh	hh	hh	hk	hk	hh	hh	hh	kk	hk	hk	hk	--	hk	hh	hk	hh	hh	hk	kk	hk	kk	hk	hk	--	kk	hk	kk	kk	kk	hk	kk	kk	hk	hh	kk	hk	kk	hk	kk	kk	hk	hk	kk	hh	hk	hk	hk	hk	hk	hk	hk	kk	hh	hk	hk	kk	hk	hk	hh	kk	hh	kk	kk	hh	hh	hk	hk	kk	hk	hk	hh	kk	hh	hh	hk	hk	hh	kk	kk	hk	hh	hh	hk	hh	hk	kk	hk	hh	hk	hh	kk	hk	kk	hh	hk	hh	hh	kk	hk	hk	h-	kk	hk	hh	hh	hk	hh	hk	hk	hk	hh	hk	hh	hh	hh	kk	hk	hh	hh	hk	hh	hk	hk	hk	kk	hh	hh	kk	hh	kk	kk	hk	k-	k-	hh	hk	kk	hk	kk	hk	--	hk	kk	hk	hh	hk	hk	kk	hk	hh	kk	k-	k-	hk	h-	hk	hk	hk	kk	hk	hk	--	hk	hh	hh	hh	hh	hk	hh	hh	hk	kk	hk	kk	hk	hk
        # ...
        ss = s.split("\n")  # max split = 1
        ss = ss[0].split("\t")
        self.sStateMissing = "--"

        self.sSep = "\t"
        idMarker = int(ss[0])
        self.sChr = ss[1]
        self.sMarker = ss[2]
        self.pos = float(ss[3])
        if ss[4] == "lm":
            self.idType = 1
            self.sState0 = "ll"
            self.sState1 = "lm"
        if ss[4] == "nn":
            self.idType = 2
            self.sState0 = "nn"
            self.sState1 = "np"
        if ss[4] == "hk":
            self.idType = 3
            self.sState0 = "hh"
            self.sState1 = "hk"
            self.sState2 = "kk"
        self.g = []
        n = len(ss) - 6
        for i in range(n):
            col = i + 6
            sg = ss[col]

            a = -1
            if sg == self.sStateMissing or sg == "h-" or sg == "k-":
                a = -1
            else:
                if sg == self.sState0:
                    a = 0
                if sg == self.sState1:
                    a = 1
                if sg == self.sState2:
                    a = 2
                if a < 0:
                    print("<" + sg + ">")
                    a = 1 / 0
            self.g.append(a)
        self.nIndivids = len(self.g)
        self.phase = [-1, -1]
        # print str(self.nIndivids)
        self.calc()

    def readVCF(
        self,
        s,
        iColName,
        iColPos,
        iColS0,
        iColS1,
        iColFormat,
        nIndivids,
        nReadsMinBeSureNotHeterozygote,
        idType,
        vIndPloidy=[],
        ploidyNeed=0,
    ):
        # s = string of .vcf file
        # iColName=0 #chromosome
        # iColPos=1 #position on chromosome
        # iColS0=3 #name of allele
        # iColS1=4 #name of alternative allele
        # iColFormat=8 #column fhere format
        # nIndivids
        # nReadsMinBeSureNotHeterozygote
        # idType (1=haploid, 4 can be heterozygote, unknown phases)

        # ploidyNeed=0 All
        # ploidyNeed=1 Haploids only
        # ploidyNeed=2 Diploids only
        """
        ##fileformat=VCFv4.2
        ##fileDate=20200108
        ##source="Stacks v2.2"
        ##INFO=<ID=AD,Number=R,Type=Integer,Description="Total Depth for Each Allele">
        ##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
        ##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
        ##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
        ##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allele Depth">
        ##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
        ##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
        ##FORMAT=<ID=GL,Number=G,Type=Float,Description="Genotype Likelihood">
        ##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
        ##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
        ##FORMAT=<ID=MIN_DP,Number=1,Type=Integer,Description="Minimum DP observed within the GVCF block">
        ##FORMAT=<ID=PGT,Number=1,Type=String,Description="Physical phasing haplotype information, describing how the alternate alleles are phased in relation to one another">
        ##FORMAT=<ID=PID,Number=1,Type=String,Description="Physical phasing ID information, where each unique ID within a given sample (but not across samples) connects records within a phasing group">
        ##FORMAT=<ID=PL,Number=G,Type=Integer,Description="Normalized, Phred-scaled likelihoods for genotypes as defined in the VCF specification">
        ##FORMAT=<ID=RGQ,Number=1,Type=Integer,Description="Unconditional reference genotype confidence, encoded as a phred quality -10*log10 p(genotype call is wrong)">
        ##INFO=<ID=loc_strand,Number=1,Type=Character,Description="Genomic strand the corresponding Stacks locus aligns on">
        ss[iColFormat-1]="NS=31;AF=0.032"
        ss[iColFormat]="GT:DP:AD:GL" in file with haploid males (genetic mapping and QTL)
        ss[iColFormat]="GT:DP:AD:GQ:GL" in file with colonies (GWAS)
        ss[iColFormat]="GT:AD:DP:GQ:PL" in file with inds (GWAS)
        """
        ss = s.split("\n")  # max split = 1
        s = ss[0]
        # print s
        ss = s.split("\t")
        self.g = []
        self.nIndivids = nIndivids
        # print(s)
        # print(ss)
        # print(str(iColS0))
        self.sState0 = ss[iColS0]
        self.sState1 = ss[iColS1]
        self.sState2 = "H"  # heterozygous
        self.sStateMissing = "-"
        self.sSep = ""
        self.sChr = ss[iColName]
        self.pos = int(ss[iColPos])
        self.sMarker = ss[iColName] + "___" + ss[iColPos]
        self.idType = idType

        iCol = 0
        sss = ss[iColFormat].split(":")  # "GT:DP:AD:GQ:GL"
        iDP = sss.index("DP")
        iInd = 0
        for s0 in ss:
            if iCol > iColFormat:
                # "GT:DP:AD:GQ:GL"
                # 0/1:5:1,4:31:-12.12,-0.00,-2.54
                # <Genotype>:<ReadDepth>:<Allele0depth>,<Allele1depth>:<GenotypeQuality>:<-log(Likelihood(aa))>,<-log(Likelihood(aA))>,<-log(Likelihood(AA))>
                sss = s0.split(":")
                # print s0
                # print sss
                sssGT = sss[0].split("/")  # "0/1"->["0","1"]
                a0 = -1
                a1 = -1
                if sssGT[0] != ".":
                    a0 = int(sssGT[0])  # 0 or 1
                if sssGT[1] != ".":
                    a1 = int(sssGT[1])  # 0 or 1

                IndPloidy = 0  # unknown
                if len(vIndPloidy) > 0:
                    IndPloidy = vIndPloidy[iInd]
                if IndPloidy == ploidyNeed or ploidyNeed == 0:
                    a = -1
                    if a0 >= 0 and a1 >= 0:
                        if self.idType == 0:  # no expected heterozygotes
                            if a0 == a1:
                                a = a0  # 0 or 1
                        if (
                            self.idType == 4 or self.idType == 5
                        ):  # expected heterozygotes
                            if (
                                sss[iDP] == "."
                            ):  # if DP is unknown then such genotype is questional
                                print(s)
                                print(ss[iColFormat])
                                print(sss)
                            else:
                                DP = int(
                                    sss[iDP]
                                )  # ReadDepth, number of reads. Higher DP correspond to higher quality (more sure) genotype
                                # may be heterozygote but we observe only one allele
                                # formally, no need to check for heterozygote. but without this heterozyzous have higher chance to be non-missed, as result, negative F_IT?!
                                if DP >= nReadsMinBeSureNotHeterozygote:
                                    if IndPloidy == 1:
                                        if a0 == a1:
                                            a = a0  # 0 or 1
                                    if IndPloidy == 2 or IndPloidy == 0:
                                        if a0 == a1:
                                            a = 2 * a0  # a0=a1 (0 or 2)
                                        else:
                                            a = 1  # Aa

                    self.g.append(a)
                iInd += 1
            iCol += 1
        # print("nInd="+str(len(self.g))+" "+str(ploidyNeed))
        if self.idType == 5:
            self.idType = 0
            n = [0, 0, 0]
            for a in self.g:
                if a >= 0:
                    n[a] += 1
            nn = len(self.g)
            # print(str(n[0])+","+str(n[1])+","+str(n[2]))
            if n[0] <= 3 and n[2] >= 3:
                for i in range(nn):
                    if self.g[i] == 0:
                        self.g[i] = -1
                    else:
                        if self.g[i] == 2:
                            self.g[i] = 0
            else:
                for i in range(nn):
                    if self.g[i] == 2:
                        self.g[i] = -1
        if ploidyNeed == 0:
            self.calc(vIndPloidy)
        else:
            self.calc()  # all of the same ploidy

    def readSimple_indNames(self, s, sSep):
        self.sSep = sSep

        # del \n in the end of string
        ss = s.split("\n")  # max split = 1
        s = ss[0]

        s0 = s.split("\t", 1)  # max split = 1
        # self.sMarker=s0[0]
        sg = s0[1]
        ssg = sg.split(self.sSep)
        return ssg

    def calc(self, vIndPloidy=[]):
        self.nIndWithState = []
        self.nIndMissed = 0
        self.nHapWithState = []  # [iState], iState=0 or 1
        self.nHapMissed = 0
        self.nDipWithState = []  # [iState], iState=0, 1,2
        self.nDipMissed = 0

        for i in range(10):
            self.nIndWithState.append(0)
            self.nHapWithState.append(0)
            self.nDipWithState.append(0)
        i = 0
        for a in self.g:
            ploidy = 0
            if len(vIndPloidy) > 0:
                ploidy = vIndPloidy[i]
            if a < 0 or a >= 10:
                self.nIndMissed = self.nIndMissed + 1
                if ploidy == 1:
                    self.nHapMissed += 1
                if ploidy == 2:
                    self.nDipMissed += 1
            else:
                self.nIndWithState[a] = self.nIndWithState[a] + 1
                if ploidy == 1:
                    self.nHapWithState[a] += 1
                if ploidy == 2:
                    self.nDipWithState[a] += 1
            i += 1

        n0 = 0
        n1 = 0
        if self.idType in [0, 1, 2]:
            n0 = self.nIndWithState[0]
            n1 = self.nIndWithState[1]
            # print(str(n0)+" "+str(n1))
            # i=1/0
        if self.idType in [3, 4]:
            n0 = 2 * self.nIndWithState[0] + self.nIndWithState[1]
            n1 = 2 * self.nIndWithState[2] + self.nIndWithState[1]
        self.pp = 0
        self.chi2 = 0
        if n1 + n0 > 0:
            self.pp = float(min(n0, n1)) / (n0 + n1)
            # print str(self.pp)
            VovaMath = clVovaMath()
            self.chi2 = VovaMath.chi2_H0_p0_eq_p1(n0, n1)

        # NODE_10007_length_5053_cov_2.49574
        # NODE_10018_length_5038_cov_2.43377_B0_start3811,4147,4147,4147
        # NODE_11682_length_3520_cov_1.99117___2864
        # scaffold1|size1555347___99
        # tig00000049___15616
        self.ctgLength = -1
        self.PrivmanCtgIndex = -1
        self.vPrivmanvPosOnCtg = []
        if "|size" in self.sMarker:  # scaffold1|size1555347___99
            ss = self.sMarker.split("|size")  # ["scaffold1","1555347___99"]
            self.PrivmanCtgIndex = int(ss[0][8:])  # "scaffold1" -> 1
            ss = ss[1].split("___")  # ["1555347","99"]
            self.ctgLength = int(ss[0])  # 1555347
            self.vPrivmanvPosOnCtg.append(int(ss[1]))  # 99
            return
        if "tig0" in self.sMarker:  # tig00000049___15616
            ss = self.sMarker.split("___")  # [tig00000049","15616]
            sIndex = ss[0][3:]  # 00000049
            i = 0
            b = True
            for s in sIndex:
                if (s == "0") and b:
                    i += 1
                else:
                    b = False
            if isinstance(sIndex[i:], int) and isinstance(
                ss[1], int
            ):  # if ss[1] is integer number
                self.PrivmanCtgIndex = int(sIndex[i:])  # 49
                self.vPrivmanvPosOnCtg.append(int(ss[1]))  # 15616
            return
        if len(self.sMarker) > 5:
            ss = self.sMarker.split("_")
            if len(ss) > 3:
                # print self.sMarker
                if isinstance(ss[1], int):  # if ss[1] is integer number
                    self.PrivmanCtgIndex = int(ss[1])
                    if ss[2] == "length":
                        sLen = ss[3]
                        if len(sLen) > 0:
                            # if sLen.isnumeric():
                            self.ctgLength = int(sLen)
            if len(ss) > 7:
                if len(ss[7]) > 5:
                    if ss[7][0:5] == "start":
                        sss = ss[7][5:]
                        ssss = sss.split(",")
                        for sPos in ssss:
                            self.vPrivmanvPosOnCtg.append(
                                int(sPos)
                            )  # for good my markers
                if len(ss) > 8:
                    if isinstance(ss[8], int):  # if ss[8] is integer number
                        self.vPrivmanvPosOnCtg.append(int(ss[8]))  # for bad my markers

    def vnAlleleCombination(self, vIndivids):  # vn,n=
        n = 0
        if self.idType in [0, 1, 2]:
            vn = [0, 0]
            for i in vIndivids:
                a = self.g[i]
                if a >= 0:
                    vn[a] += 1
                    n += 1
            return vn, n
        if self.idType == 4:
            vn = [0, 0, 0]
            for i in vIndivids:
                a = self.g[i]
                if a >= 0:
                    vn[a] += 1
                    n += 1
            return vn, n

    def vvnAlleleCombination(self, m, vIndivids):  # vvn,n=
        n = 0
        if self.idType in [0, 1, 2]:
            vvn = [[0, 0], [0, 0]]
            for i in vIndivids:
                am = m.g[i]
                if am >= 0:
                    a = self.g[i]
                    if a >= 0:
                        vvn[am][a] += 1
                        n += 1
            return vvn, n
        if self.idType == 4:
            vvn = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for i in vIndivids:
                am = m.g[i]
                if am >= 0:
                    a = self.g[i]
                    if a >= 0:
                        vvn[am][a] += 1
                        n += 1
            return vvn, n

    def p0p1(self, vn, n):  # p0,p1=
        p0 = 0
        p1 = 0
        if n > 0:
            if self.idType in [0, 1, 2]:  # [n_a, n_A]
                p0 = float(vn[0]) / n
                p1 = float(vn[1]) / n
            if self.idType == 4:  # [n_aa, n_Aa, n_AA]
                p0 = float(2 * vn[0] + vn[1]) / (2 * n)
                p1 = float(2 * vn[2] + vn[1]) / (2 * n)
        return p0, p1

    def n_pp_Hobs_Hexp_F_IT(self, vn):  # n,pp,He_obs,He_exp,F_IT=
        if self.idType == 4:
            n = vn[0] + vn[1] + vn[2]
            pp = 0
            He_obs = 0
            He_exp = 0
            F_IT = 0
            if n > 0:
                p0, p1 = self.p0p1(vn, n)
                pp = min(p0, p1)
                if pp > 0:
                    He_exp = 2 * p0 * p1
                    He_obs = float(vn[1]) / n

                    # https://en.wikipedia.org/wiki/F-statistics
                    F_IT = 1 - float(He_obs) / He_exp
                if pp > 1 or He_obs > 1 or He_exp > 1 or F_IT > 1:
                    print("vn=" + str(vn) + ", n=" + str(n))
                    print(
                        "pp="
                        + str(pp)
                        + ", He_obs="
                        + str(He_obs)
                        + ", He_exp="
                        + str(He_exp)
                        + ", F_IT="
                        + str(F_IT)
                    )
                    a = 1 / (1 - 1)
            return n, pp, He_obs, He_exp, F_IT

    def F_ST_and_F_IS(self, vvIndivids):  # F_ST,F_IS=
        # https://en.wikipedia.org/wiki/F-statistics
        # http://www.uwyo.edu/dbmcd/molmark/practica/fst.html
        # F_IS=1-H_I/H_S
        # F_ST=1-H_S/H_T
        # F_IT=1-H_I/H_T
        # here:
        # H_I = weighted average observed heterozygosity
        # H_S = weighted average expected heterozygosity
        # H_T = 2*p_total*(1-p_total)
        # (1-F_IS)*(1-F_ST)=1-F_IT
        p0 = 0
        p1 = 0
        He_exp_ave = 0  # H_S
        n = 0
        H_I = 0
        for vIndivids in vvIndivids:
            vn_pop, n_pop = self.vnAlleleCombination(vIndivids)
            # n_pop,pp_pop,He_obs_pop,He_exp_pop,F_IT_pop=self.n_pp_Hobs_Hexp_F_IT(vn_pop):#
            p0_pop, p1_pop = self.p0p1(vn_pop, n_pop)
            He_exp_pop = 2 * p0_pop * p1_pop
            He_exp_ave += n_pop * He_exp_pop
            p0 += n_pop * p0_pop
            p1 += n_pop * p1_pop
            if self.idType == 4:
                H_I += vn_pop[1]
            n += n_pop
        if n > 0:
            He_exp_ave = float(He_exp_ave) / n  # H_S
            p0 = float(p0) / n
            p1 = float(p1) / n
            He_exp_tot = 2 * p0 * p1  # H_T
            H_I = float(H_I) / n  # H_I
            if He_exp_tot > 0:
                F_ST = 1 - float(He_exp_ave) / He_exp_tot  # F_ST=1-H_S/H_T
                F_IS = 1 - float(H_I) / He_exp_ave  # F_IS=1-H_I/H_S
                return F_ST, F_IS
            else:
                return 0, 0
        else:
            return 0, 0

    def compareWithMarkerLDchi2(
        self, m, vIndivids
    ):  # X2,df,nExpMin, LD, LD_tag, r, p, rec =
        vvn, n = self.vvnAlleleCombination(m, vIndivids)
        VovaMath = clVovaMath()

        def LD_get(pA, pB, pAB):  # LD,LD_tag=
            # LD_tag=normalized LD, =LD/LD_max in [-1,1]
            LD = pAB - pA * pB
            LD_tag = 0
            if LD > 0:
                LD_max = min(pA, pB) - pA * pB
                LD_tag = LD / LD_max
            if LD < 0:
                LD_max = max(0, pA + pB - 1) - pA * pB
                LD_tag = LD / LD_max
            return LD, LD_tag

        if self.idType in [0, 1, 2]:
            # r=correlation between alleles, from [-1,1]
            # p=p-value in t-test (H0: r=corr(A,B)=0)
            # rec=estimated recombination rate, from [0,1], i.e. can be >0.5 if phases are known, if not then need after min(rec,1-rec)
            X2, df, nExpMin = VovaMath.chi2_2x2(
                vvn[0][0], vvn[0][1], vvn[1][0], vvn[1][1]
            )
            LD = 0
            LD_tag = 0
            r = 0
            p = 1
            rec = -1
            if n > 1:
                pA = float(vvn[1][0] + vvn[1][1]) / n
                pB = float(vvn[0][1] + vvn[1][1]) / n
                pAB = float(vvn[1][1]) / n
                LD, LD_tag = LD_get(pA, pB, pAB)
                if LD != 0:
                    r = float(LD) / math.sqrt(pA * (1 - pA) * pB * (1 - pB))
                    if n > 2:
                        if r * r < 1:
                            t = float(r * math.sqrt(n - 2)) / math.sqrt(1 - r * r)
                            # print str(t)
                            myMath = clVovaMath()
                            p = myMath.tTest_pValTwoTails(t, n - 2)
                        else:
                            p = 0  # highly significant
            if n >= 10 and self.idType == 0:
                rec = float(vvn[1][0] + vvn[0][1]) / n
            return X2, df, nExpMin, LD, LD_tag, r, p, rec
        if self.idType == 4:
            X2, df, nExpMin = VovaMath.chi2_mxn(vvn)
            LD = 0
            LD_tag = 0
            r = 0
            p = 1
            if n > 1:
                pAA = float(vvn[2][0] + vvn[2][2]) / n
                pBB = float(vvn[0][2] + vvn[2][2]) / n
                pAABB = float(vvn[2][2]) / n
                LD, LD_tag = LD_get(pAA, pBB, pAABB)
                vv1 = []
                vv2 = []
                for i in [0, 1, 2]:
                    for j in [0, 1, 2]:
                        for k in range(vvn[i][j]):
                            vv1.append(i)
                            vv2.append(j)
            r, p = VovaMath.corrAndP(vv1, vv2)
            return X2, df, nExpMin, LD, LD_tag, r, p

    def compareWithMarker(
        self, m, vIndivids
    ):  # nIndividsGenotypesEqual, nIndividsGenotypesDifferent, nToImprove=
        nIndividsGenotypesEqual = 0  # number of individuals where self.g[i]=m.g[i]
        nIndividsGenotypesDifferent = (
            0  # number of individuals where self.g[i]=/=m.g[i]
        )
        nToImprove = (
            0  # number of individuals where self.g[i] is missed but m.g[i] not missed
        )
        if self.idType == m.idType:
            if self.idType in [0, 1, 2]:
                for i in vIndivids:
                    am = m.g[i]
                    if am >= 0:
                        a = self.g[i]
                        if a >= 0:
                            if a == am:
                                nIndividsGenotypesEqual += 1
                            else:
                                nIndividsGenotypesDifferent += 1
                        else:
                            nToImprove += 1
                if self.phase != m.phase:
                    if self.phase >= 0 and m.phase >= 0:
                        return (
                            nIndividsGenotypesDifferent,
                            nIndividsGenotypesEqual,
                            nToImprove,
                        )
                return (
                    nIndividsGenotypesEqual,
                    nIndividsGenotypesDifferent,
                    nToImprove,
                )  # =compareWithMarker(self,m,vIndivids)

            if self.idType in [3, 4]:
                nIndividsGenotypesEqual0 = 0
                nIndividsGenotypesEqual1 = 0
                nIndividsGenotypesEqual2 = 0
                nIndividsGenotypesDifferent01 = 0
                nIndividsGenotypesDifferent02 = 0
                nIndividsGenotypesDifferent12 = 0
                for i in vIndivids:
                    am = m.g[i]
                    if am >= 0:
                        a = self.g[i]
                        if a >= 0:
                            if a == am:
                                if a == 0:
                                    nIndividsGenotypesEqual0 += 1
                                if a == 1:
                                    nIndividsGenotypesEqual1 += 1
                                if a == 2:
                                    nIndividsGenotypesEqual2 += 1
                            else:
                                if (a == 0 and am == 1) or (a == 1 and am == 0):
                                    nIndividsGenotypesDifferent01 += 1
                                if (a == 0 and am == 2) or (a == 2 and am == 0):
                                    nIndividsGenotypesDifferent02 += 1
                                if (a == 1 and am == 2) or (a == 2 and am == 1):
                                    nIndividsGenotypesDifferent12 += 1
                        else:
                            nToImprove += 1
                if (self.phase[0] < 0 or m.phase[0] < 0) and (
                    self.phase[1] < 0 or m.phase[1] < 0
                ):
                    if (
                        nIndividsGenotypesEqual0 + nIndividsGenotypesEqual2
                        >= nIndividsGenotypesDifferent02
                    ):
                        nIndividsGenotypesEqual = (
                            nIndividsGenotypesEqual0 + nIndividsGenotypesEqual2
                        )
                        nIndividsGenotypesDifferent = (
                            nIndividsGenotypesDifferent01
                            + nIndividsGenotypesDifferent12
                            + 2 * nIndividsGenotypesDifferent02
                        )
                    else:
                        nIndividsGenotypesEqual = nIndividsGenotypesDifferent02
                        nIndividsGenotypesDifferent = (
                            nIndividsGenotypesDifferent01
                            + nIndividsGenotypesDifferent12
                            + 2 * (nIndividsGenotypesEqual0 + nIndividsGenotypesEqual2)
                        )
                    return (
                        nIndividsGenotypesEqual,
                        nIndividsGenotypesDifferent,
                        nToImprove,
                    )
                else:
                    pass  # (nIndividsGenotypesEqual gotovo)
        if (self.idType == 3 and m.idType in [1, 2]) or (
            m.idType == 3 and self.idType in [1, 2]
        ):
            for i in vIndivids:
                am = m.g[i]
                if am >= 0:
                    a = self.g[i]
                    if a >= 0:
                        if m.idType == 2:
                            a = 2 - a  # 0<->2, 1<->1
                        if self.idType == 2:
                            am = 2 - am  # 0<->2, 1<->1
                        if a == am:
                            nIndividsGenotypesEqual += 1
                        else:
                            nIndividsGenotypesDifferent += 1
            if (self.phase[0] < 0 or m.phase[0] < 0) and (
                self.phase[1] < 0 or m.phase[1] < 0
            ):
                if nIndividsGenotypesEqual < nIndividsGenotypesDifferent:
                    return (
                        nIndividsGenotypesDifferent,
                        nIndividsGenotypesEqual,
                        nToImprove,
                    )
                return nIndividsGenotypesEqual, nIndividsGenotypesDifferent, nToImprove
            else:
                pass  # (nIndividsGenotypesEqual gotovo)
        return (
            nIndividsGenotypesEqual,
            nIndividsGenotypesDifferent,
            nToImprove,
        )  # =compareWithMarker(self,m,vIndivids)

    def compareWithGPhased(
        self, g, vIndivids
    ):  # nIndividsGenotypesEqual,nIndividsGenotypesDifferent=
        # rr=clRecombination()
        nIndividsGenotypesEqual = 0
        nIndividsGenotypesDifferent = 0
        g1 = self.gPhased()
        for i in vIndivids:
            if g[i] >= 0 and g1[i] >= 0:
                if g[i] == g1[i]:
                    nIndividsGenotypesEqual += 1
                else:
                    nIndividsGenotypesDifferent += 1
        return nIndividsGenotypesEqual, nIndividsGenotypesDifferent

    def improveByMarker(self, m, bTheSamePhase):
        if bTheSamePhase:
            for i in range(self.nIndivids):
                if m.g[i] >= 0 and self.g[i] < 0:
                    self.g[i] = m.g[i]
        else:
            for i in range(self.nIndivids):
                if m.g[i] >= 0 and self.g[i] < 0:
                    self.g[i] = 1 - m.g[i]  # 1 <-> 0

    def phaseSetAccordingToCloseMarker(self, m, vIndivids):
        if m.phase >= 0:  # 0 or 1
            (
                nIndividsGenotypesEqual,
                nIndividsGenotypesDifferent,
                nToImprove,
            ) = self.compareWithMarker(m, vIndivids)
            if nIndividsGenotypesEqual >= nIndividsGenotypesDifferent:
                self.phase = m.phase
            else:
                self.phase = 1 - m.phase  # 1 <-> 0

    def vIndividsAll_get(self):  # vIndivids=
        vIndivids = []
        for i in range(self.nIndivids):
            vIndivids.append(i)
        return vIndivids

    def vIndividsBootstreap_get(self):  # vIndivids=
        vIndivids = []
        n = self.nIndivids
        for i in range(n):
            # random.choices(
            vIndivids.append(random.randrange(n))
        return vIndivids

    def aPhased(self, i):
        if self.g[i] < 0:
            return self.g[i]
        if self.idType in [0, 1, 2]:
            if self.phase <= 0:
                return self.g[i]
            return 1 - self.g[i]  # 1<->0
        if self.idType == 3:
            if self.phase[0] <= 0:
                if self.phase[1] <= 0:
                    return self.g[i]
                else:
                    pass  # ne gotovo
                    return self.g[i]
            if self.phase[1] > 0:
                return 2 - self.g[i]  # 2<->0
            else:
                pass  # ne gotovo
                return self.g[i]
        if self.idType == 4:
            if self.phase <= 0:
                return self.g[i]
            return 2 - self.g[i]  # 2<->0

    def gPhased(self):
        if self.idType in [0, 1, 2]:
            if self.phase <= 0:
                return self.g
            else:
                g = []
                for i in range(self.nIndivids):
                    a = self.g[i]
                    if a >= 0:
                        a = 1 - a  # 0<->1
                    g.append(a)
                return g
        if self.idType == 3:
            pass  # ne gotovo
        if self.idType == 4:
            if self.phase <= 0:
                return self.g
            else:
                g = []
                for i in range(self.nIndivids):
                    a = self.g[i]
                    if a >= 0:
                        a = 2 - a  # 0<->2
                    g.append(a)
                return g

    def readLineOfPrivman(self, s):
        # lines of file: Cnig_gn2.concatScaf2ChrByMap.3.map
        # chr1	285558	[NODE_679_POS_38001]	14	1.0:1.1	0.95
        # chr1	285498	NODE_679_POS_38061	12	1.0:1.1	2.87
        # here:
        # LG	coorPhys	marker	nMissed	segregation	coor

        def processMarkerPrivman(s):
            # "NODE_10018_length_5038_cov_2.43377_B0_start3811,4147,4147,4147"
            # "NODE_10067_POS_2432"
            # print "s="+s
            sError = "426:len(s)<10"
            if len(s) >= 10:
                ss = s.split("_")
                # print "ss="+str(ss)
                sError = "430:len(ss)<=3"
                if len(ss) > 3:
                    sError = "432:" + ss[0] + "-" + ss[2]
                    if ss[0] == "NODE" and ss[2] == "POS":
                        # "NODE_10067_POS_2432"
                        PrivmanCtgIndex = int(ss[1])  # 10067
                        PrivmanPosOnCtg = int(ss[3])  # 2432
                        return (
                            PrivmanCtgIndex,
                            PrivmanPosOnCtg,
                            "ok",
                        )  # processMarkerPrivman(s)
            return -1, -1, sError

        sLG = -1
        PrivmanCtgIndex = -1
        sError = "525:len(s)<=10"
        PrivmanPosOnCtg = -1
        nMissed = -1
        coor = -1
        bInBrackets = False
        # print "405: "+s
        if len(s) > 10:
            ss = s.split("\t")
            # print "408: "+str(ss)
            sError = "529:len(ss)<=5"
            if len(ss) > 5:
                sLG = ss[0]
                s1 = ss[2]
                n = len(s1)
                # print
                if n > 2:
                    if s1[0] == "[" and s1[n - 1] == "]":
                        bInBrackets = True
                        s1 = s1[1 : n - 1]
                # print "417: "+str(s1)
                sError = str(sError)
                PrivmanCtgIndex, PrivmanPosOnCtg, sError = processMarkerPrivman(s1)
                nMissed = int(ss[3])
                coor = float(ss[5])
        return (
            sLG,
            PrivmanCtgIndex,
            PrivmanPosOnCtg,
            nMissed,
            coor,
            bInBrackets,
            sError,
        )  # =readLineOfPrivman(self,s)

    def processTrait(self, trait, myMath=clVovaMath()):  # s=
        # self.valAllInds=[]
        # self.bVal=[]
        # self.nVal=0
        n = self.nIndivids
        if n < 1:
            s = ""
            s += "\t" + trait.name
            s += "\t" + "n00" + "\t" + "n10"
            s += "\t" + "n0" + "\t" + "n1"
            s += "\t" + "m0" + "\t" + "m1" + "\t" + "m1-m0"
            s += "\t" + "STDV0" + "\t" + "STDV1"
            s += "\t" + "P.E.V."
            s += "\t" + "pPerm" + "\t" + "pWilcoxon" + "\t" + "ptTestTwoSamplesDiffVar"
            sShort = "\t" + trait.name
            return s, sShort
        if myMath.vvSortedAndNoOutLiersIfNeed___nMaxDone < n:
            k = myMath.vvSortedAndNoOutLiersIfNeed___k
            myMath.vvSortedAndNoOutLiersIfNeed___vmaxVarRelativeToKK__make(n, k)
        vv0 = []
        vv1 = []
        for i in range(n):
            g = self.g[i]
            if trait.bVal[i] and g >= 0:
                if self.phase == 1:
                    g = 1 - g  # 0<->1
                if g == 0:
                    vv0.append(trait.valAllInds[i])
                else:
                    vv1.append(trait.valAllInds[i])
        n00 = len(vv0)
        n10 = len(vv1)
        vv0 = myMath.vvSortedAndNoOutLiersIfNeed(vv0, -1)
        vv1 = myMath.vvSortedAndNoOutLiersIfNeed(vv1, -1)

        m0 = myMath.mean(vv0)
        s02 = myMath.var(vv0)
        m1 = myMath.mean(vv1)
        s12 = myMath.var(vv1)
        s0 = math.sqrt(s02)
        s1 = math.sqrt(s12)
        n0 = len(vv0)
        n1 = len(vv1)
        pev = myMath.PEV(vv0, vv1)

        m10, m20, d, pPerm = myMath.permTest(vv0, vv1, 100000, 5)
        uu, pWilcoxon = myMath.WilcoxonTest(vv0, vv1)
        ptTestTwoSamplesDiffVar = myMath.tTestTwoSamplesDiffVar(vv0, vv1)

        s = ""
        s += "\t" + trait.name
        s += "\t" + str(n00) + "\t" + str(n10)
        s += "\t" + str(n0) + "\t" + str(n1)
        s += "\t" + str(m0) + "\t" + str(m1) + "\t" + str(m1 - m0)
        s += "\t" + str(s0) + "\t" + str(s1)
        s += "\t" + str(pev)
        s += (
            "\t"
            + str(pPerm)
            + "\t"
            + str(pWilcoxon)
            + "\t"
            + str(ptTestTwoSamplesDiffVar)
        )
        sShort = "\t" + str(pPerm)
        return s, sShort


class clMarkersWithMultiplePos:
    def __init__(self):
        self.vsMapName = []  # [iMap]
        self.vMap = []  # iMap
        self.vMarkerWithMultiplePos = []  # [iMarker]
        self.vsMarkerName = []  # e.g., NODE_99_length_95174_cov_2.74245___72999

        # self.vvsPartName=[]#[iMap][iCtg]
        # 	self.vMap[iMap].vPartOfMap[iCtg].name
        # 	self.vMap[iMap].vsPartName
        # 	self.vMap[iMap].addPart(sName,length=-1)
        # self.vvvidMarker=[]#[iMap][iCtg][m]
        # 	self.vMap[iMap].vPartOfMap[iCtg].vidMarker[m]

    class clMap:
        class clPartOfMap:
            def __init__(self, sName, length=-1, lengthSumOfPrev=-1):
                self.name = sName
                self.length = length
                self.lengthSumOfPrev = lengthSumOfPrev
                self.vidMarker = []

        def __init__(self, sMapName, iMap=-1):
            self.iMap = iMap
            self.sMapName = sMapName
            self.vsPartName = []
            self.vPartOfMap = []
            self.sScale = ""  # bp, cM, kbp, Mbp
            self.SecCtgs = clSecCtgs()

        def addPart(self, sName, length=-1, lengthSumOfPrev=-1):
            self.vsPartName.append(sName)
            self.vPartOfMap.append(self.clPartOfMap(sName, length, lengthSumOfPrev))
            lengthSumOfPrev += length
            return lengthSumOfPrev

        def addPartIfNoWithSuchName(self, sName, coor):
            if sName != "":
                if not (sName in self.vsPartName):
                    self.addPart(sName, coor)
                    iPart = self.vsPartName.index(sName)
                    if iPart == 0:
                        self.vPartOfMap[iPart].lengthSumOfPrev = 0
                    else:
                        self.vPartOfMap[iPart].lengthSumOfPrev = (
                            self.vPartOfMap[iPart - 1].lengthSumOfPrev
                            + self.vPartOfMap[iPart - 1].length
                        )
                else:
                    iPart = self.vsPartName.index(sName)
                    if self.vPartOfMap[iPart].length < coor:
                        self.vPartOfMap[iPart].length = coor

        def iPart(self, sPart):
            if sPart == "":
                return -1
            return self.vsPartName.index(sPart) if (sPart in self.vsPartName) else -1

        def lengthSumOfPrev_make(self):
            x = 0
            for part in self.vPartOfMap:
                part.lengthSumOfPrev = x
                x += part.length

        def Ranking_get(self, vMarkerInteresting, clMarkersWithMultiplePos):  # Ranking=
            def MyFunc0(q):
                return q[0]

            Ranking = self.clRanking()
            for part in self.vPartOfMap:
                # part=self.vMap[self.iMap].vPartOfMap[iPart]
                Ranking.vvMarkerOnPart.append([])
                Ranking.vvCoorOnPart.append([])
                Ranking.vvRankOnPart.append([])
            nmTotal = len(clMarkersWithMultiplePos.vMarkerWithMultiplePos)
            for m in range(nmTotal):
                Ranking.vRankingPos.append([])
            for Marker in vMarkerInteresting:
                vPosOnMap = Marker.vvPosOnMap[self.iMap]
                if len(vPosOnMap) > 0:
                    pos = vPosOnMap[0]
                    # for pos in vPosOnMap:
                    # 	if pos.iPart==iPart:
                    # 		break
                    Ranking.vvMarkerOnPart[pos.iPart].append(Marker)
                    Ranking.vvCoorOnPart[pos.iPart].append(pos.coor)
            iPart = 0
            for part in self.vPartOfMap:
                vq = []  # [pos.coor,Marker]
                nm = len(Ranking.vvMarkerOnPart[iPart])
                for m in range(nm):
                    Marker = Ranking.vvMarkerOnPart[iPart][m]
                    coor = Ranking.vvCoorOnPart[iPart][m]
                    vq.append([coor, Marker])
                if len(vq) > 1:
                    vq.sort(key=MyFunc0)

                m = 0
                rankOnPart = 0
                coor_prev = -1
                for q in vq:
                    Marker = q[1]
                    coor = q[0]
                    if m > 0:
                        if coor_prev < coor:
                            rankOnPart += 1
                    else:
                        rankOnPart = 1

                    Ranking.vvRankOnPart[iPart].append(
                        rankOnPart
                    )  # rank of coordinate on the part (<=nm)
                    Ranking.vvCoorOnPart[iPart][m] = coor
                    Ranking.vRankingPos[Marker.id] = [iPart, m]
                    m += 1
                    coor_prev = coor
                iPart += 1
            return Ranking

        class clRanking:
            def __init__(self):
                self.vvMarkerOnPart = []  # [iPart,iMarkerOnPart]
                self.vvCoorOnPart = []  # [iPart,iMarkerOnPart]
                self.vvRankOnPart = []  # [iPart,iMarkerOnPart]
                self.vRankingPos = (
                    []
                )  # [Marker.id]:   Ranking.vRankingPos[Marker.id]=[iPart,m]

            def rankMax_get(self, iPart):
                vRankOnPart = self.vvRankOnPart[iPart]
                n = len(vRankOnPart)
                if n <= 0:
                    return 0
                return vRankOnPart[n - 1]

    class clMarkerWithMultiplePos:
        class clPosOnMap:
            def __init__(self, iPart, coor, iType):
                self.iPart = iPart
                self.coor = coor
                self.iType = iType  # user dependent, e.g., =0.5 for markers with position estimated by another map

            def s(self):  # not in use
                return str(self.iPart) + "\t" + str(self.coor) + "\t" + str(self.iType)

        def __init__(self):
            self.id = -1
            self.sName = ""
            self.sName_sourse = ""
            self.vsName_mapSpecific = []  # iMap
            self.vvPosOnMap = []  # iMap
            self.nPosMax = 0
            self.MarkersWithMultiplePos = clMarkersWithMultiplePos()

        def nPos(self, iMap):
            # print "iMap="+str(iMap)
            return len(self.vvPosOnMap[iMap])

        def addPosOnMap(self, iMap, iPart, coor, iType):
            PosOnMap = self.clPosOnMap(iPart, coor, iType)
            # print str(iMap)
            # n=len(self.vvPosOnMap)
            # for i in range(iMap-n+1):
            # 	self.vvPosOnMap.append([])
            if not (
                self.id
                in self.MarkersWithMultiplePos.vMap[iMap].vPartOfMap[iPart].vidMarker
            ):
                self.MarkersWithMultiplePos.vMap[iMap].vPartOfMap[
                    iPart
                ].vidMarker.append(self.id)
            self.vvPosOnMap[iMap].append(PosOnMap)
            if self.nPosMax < len(self.vvPosOnMap[iMap]):
                self.nPosMax = len(self.vvPosOnMap[iMap])

        def posiotionPossible_get(
            self, iMapOk, iMapToImpute
        ):  # [coorMarker_MapOk,Marker_oneOfUsed,iCtg1_MapToImpute,coor1_iMapToImpute]
            # relevant only for markers having unique position on map #iMapOk and no positions on map #iMapToImpute
            def MyFunc(q):
                return q[0]

            # bNeed=True
            vPosOnMap0 = self.vvPosOnMap[iMapOk]
            vPosOnMap1 = self.vvPosOnMap[iMapToImpute]
            if len(vPosOnMap0) == 1 and len(vPosOnMap1) == 0:
                map0 = self.MarkersWithMultiplePos.vMap[iMapOk]
                # map1=self.MarkersWithMultiplePos.vMap[iMapToImpute]
                iPart0 = vPosOnMap0[0].iPart
                Part0 = map0.vPartOfMap[iPart0]
                coor0 = vPosOnMap0[0].coor

                # build vq for markers having unique position on #iMapOk and #iMapToImpute, where in #iMapOk it is on Part0
                vq = []
                vidMarker = Part0.vidMarker
                for idMarker in vidMarker:
                    Marker = self.MarkersWithMultiplePos.vMarkerWithMultiplePos[
                        idMarker
                    ]
                    vPosOnMap00 = Marker.vvPosOnMap[iMapOk]
                    vPosOnMap01 = Marker.vvPosOnMap[iMapToImpute]
                    if len(vPosOnMap00) == 1 and len(vPosOnMap01) == 1:
                        q = [
                            vPosOnMap00[0].coor,
                            Marker,
                            vPosOnMap01[0].iPart,
                            vPosOnMap01[0].coor,
                        ]
                        vq.append(q)

                print("imp: " + self.sName + str(len(vq)))

                if len(vq) == 0:
                    return []  # impossible to do

                if len(vq) == 1:
                    return vq[0]  # only one anchoring marker => unknown orientation

                vq.sort(key=MyFunc)
                if vq[0][0] >= coor0:
                    return vq[0]  # all anchoring markers are after this marker

                # searching for position of Marker (self) in vq
                qPrev = vq[0]
                for q in vq:
                    if q[0] >= coor0:
                        if q[2] == qPrev[2]:  # iPart
                            if q[3] == qPrev[3]:
                                return q
                            else:
                                VovaMath = clVovaMath()
                                coorPP = VovaMath.yByLin(
                                    qPrev[0], qPrev[3], q[0], q[3], coor0
                                )  # yByLin(self,x1,y1,x2,y2,x)
                                q[3] = coorPP
                                return q
                        else:  # flanking markers are in different parts in MapToImpute
                            return []
                    qPrev = q
                return vq[len(vq) - 1]  # all anchoring markers are before this marker
            return []

        def vPosOnMap_onPartOfMap_get(self, iMap, iPart):
            vPosOnMap = []
            for pos in self.vvPosOnMap[iMap]:
                if pos.iPart == iPart:
                    vPosOnMap.append(pos)
            return vPosOnMap

    def iMap(self, sMap):
        return self.vsMapName.index(sMap) if sMap in self.vsMapName else -1

    def addMap(self, sMap):
        self.vsMapName.append(sMap)
        iMap = len(self.vMap)
        self.vMap.append(self.clMap(sMap, iMap))
        for m in self.vMarkerWithMultiplePos:
            m.vvPosOnMap.append([])
        print("addMap:" + sMap + ", nMapsLoadedBefore=" + str(len(self.vMap) - 1))

    def addMarker(self, MarkerWithMultiplePos):  # no position defined in this stage!
        n = len(MarkerWithMultiplePos.vvPosOnMap)
        nMaps = len(self.vsMapName)
        for i in range(nMaps - n):
            MarkerWithMultiplePos.vvPosOnMap.append([])
        MarkerWithMultiplePos.MarkersWithMultiplePos = self
        MarkerWithMultiplePos.id = len(self.vsMarkerName)
        self.vMarkerWithMultiplePos.append(MarkerWithMultiplePos)
        self.vsMarkerName.append(MarkerWithMultiplePos.sName)

    def bvsName_mapSpecific(self):
        o = False
        for m in self.vMarkerWithMultiplePos:
            if len(m.vsName_mapSpecific) > 0:
                o = True
        return o

    def printToFile(self, sFileName, bAllPos):
        f = open(sFileName, "w")

        bvsName_mapSpecific = self.bvsName_mapSpecific()

        # shapka
        s1 = "iRow" + "\t" + "m" + "\t" + "marker" + "\t" + "marker" + "\t" + "nPosMax"
        f.write(s1)
        s = "\t" + "iPos"
        for sMapName in self.vsMapName:
            s += (
                "\t"
                + sMapName
                + "_part"
                + "\t"
                + sMapName
                + "_pos"
                + "\t"
                + sMapName
                + "_iType"
            )
            if bvsName_mapSpecific:
                s += "\t" + "sName_mapSpecific"
        f.write(s)
        f.write("\n")

        iRow = 0
        im = 0
        for m in self.vMarkerWithMultiplePos:
            n = m.nPosMax if bAllPos else 1
            if n > 0:
                for iPos in range(n):
                    s = "\t" + str(iPos)
                    iMap = 0
                    for sMapName in self.vsMapName:
                        nPos = m.nPos(iMap)
                        if iPos < nPos:
                            vPosOnMap = m.vvPosOnMap[iMap]
                            PosOnMap = vPosOnMap[iPos]
                            s += (
                                "\t"
                                + self.vMap[iMap].vPartOfMap[PosOnMap.iPart].name
                                + "\t"
                                + str(PosOnMap.coor)
                                + "\t"
                                + str(PosOnMap.iType)
                            )
                            if bvsName_mapSpecific:
                                sName_mapSpecific = ""
                                if len(m.vsName_mapSpecific) > iMap:
                                    sName_mapSpecific = m.vsName_mapSpecific[iMap]
                                s += "\t" + sName_mapSpecific
                        else:
                            s += "\t" + "" + "\t" + "" + "\t" + ""
                            if bvsName_mapSpecific:
                                s += "\t" + ""
                        iMap += 1
                    s1 = (
                        str(iRow)
                        + "\t"
                        + str(im)
                        + "\t"
                        + m.sName
                        + "\t"
                        + m.sName_sourse
                        + "\t"
                        + str(m.nPosMax)
                    )
                    f.write(s1)
                    f.write(s)
                    f.write("\n")
                    iRow += 1
            else:
                s1 = (
                    str(iRow)
                    + "\t"
                    + str(im)
                    + "\t"
                    + m.sName
                    + "\t"
                    + m.sName_sourse
                    + "\t"
                    + str(m.nPosMax)
                )
                f.write(s1)
                f.write("\n")
            im += 1

        f.close()

    def readFromFile(self, sFileName):
        TableOfTxt = clTableOfTxt()
        TableOfTxt.readFromFile(sFileName, True, False)
        nCols = TableOfTxt.nCols

        PrivmanLab = clPrivmanLab()

        # self.vsMapName
        iCol = 0
        nMaps = 0
        for s in TableOfTxt.shapka.vCellText:
            # iRow	m	marker	marker	nPosMax	iPos	Cnig_gn1_part	Cnig_gn1_pos	Cnig_gn1_iType
            if iCol >= 6:
                nMaps = int((iCol - 6) / 3) + 1
                if (iCol - 6) % 3 == 0:
                    i = s.index("_part")
                    sMap = s[0:i]
                    if PrivmanLab.MyData.iFastaByName(sMap) >= 0:
                        self.addMapFromFasta(sMap)
                    else:
                        self.addMap(sMap)
            iCol += 1

        # names of parts
        for iMap in range(nMaps):
            if PrivmanLab.MyData.iFastaByName(self.vMap[iMap].sMapName) < 0:
                for row in TableOfTxt.rows:
                    iCol = 6 + iMap * 3
                    # print row.vCellText[0]
                    # print str(len(row.vCellText))+" "+str(iCol)
                    s = row.vCellText[iCol] if iCol < len(row.vCellText) else ""

                    length = float(row.vCellText[iCol + 1]) if s != "" else -1
                    self.vMap[iMap].addPartIfNoWithSuchName(s, length)

        # self.vMarkerWithMultiplePos
        for row in TableOfTxt.rows:
            MarkerWithMultiplePos = self.clMarkerWithMultiplePos()
            if not (row.vCellText[2] in self.vsMarkerName):
                MarkerWithMultiplePos = self.clMarkerWithMultiplePos()
                MarkerWithMultiplePos.sName = row.vCellText[2]
                self.addMarker(MarkerWithMultiplePos)
                MarkerWithMultiplePos.sName_sourse = row.vCellText[3]
                MarkerWithMultiplePos.nPosMax = int(row.vCellText[4])
            else:
                i = self.vsMarkerName.index(row.vCellText[2])
                MarkerWithMultiplePos = self.vMarkerWithMultiplePos[i]
            for iMap in range(nMaps):
                iCol = 6 + iMap * 3
                s = row.vCellText[iCol] if iCol < len(row.vCellText) else ""
                # if iMap==3:
                # 	#print s
                iPart = self.vMap[iMap].iPart(s)
                if iPart >= 0:
                    coor = float(row.vCellText[iCol + 1])
                    iType = int(row.vCellText[iCol + 2])
                    MarkerWithMultiplePos.addPosOnMap(iMap, iPart, coor, iType)

        # self.printToFile("test.txt",True)

        # self.anchorMapToMap(2,3)
        # self.anchorMapToMap(1,3,0,-1)
        # self.anchorMapToMap(1,2,0,-1)
        pass

    def addMapFromFasta(self, sFastaName, sFileNameFasta=""):  # iMap=
        iMap = self.iMap(sFastaName)
        if iMap < 0:
            iMap = len(self.vsMapName)
            self.addMap(sFastaName)

            if sFileNameFasta == "":
                PrivmanLab = clPrivmanLab()
                dataFasta = PrivmanLab.SecCtgsByName(sFastaName, True)  # clSecCtgs()
            else:
                dataFasta = clSecCtgs()
                dataFasta.readFromFastaFile(sFileNameFasta, -1, False)

            for ctg in dataFasta.vCtg:
                #'CM020805.1 Formica selysi isolate DE90_pool_M chromosome 1, whole genome shotgun sequence' -> "CM020805.1"
                sCtgName = ctg.name
                ss = sCtgName.split(" ")
                sPartName = (
                    sCtgName if len(ss) < 2 else ss[0]
                )  # take oly part till the first space:
                length = ctg.seqLength
                self.vMap[iMap].addPart(sPartName, length)
            self.vMap[iMap].SecCtgs = dataFasta
            self.vMap[iMap].lengthSumOfPrev_make()
        return iMap

    def addMarkersWithNameOfSeqContigInTheName(
        self, vsMarkerWithNameOfSeqContigInTheName, sOriginalDataName
    ):
        PrivmanLab = clPrivmanLab()
        dataFasta = PrivmanLab.SecCtgsByName(sOriginalDataName, True)  # clSecCtgs()
        bAllCtgNamesFromFasta = len(dataFasta.vCtg) > 0

        iMap = len(self.vsMapName)  # 0
        print("addMarkersWithNameOfSeqContigInTheName: sMap=" + sOriginalDataName)
        if sOriginalDataName in self.vsMapName:
            iMap = self.vsMapName.index(sOriginalDataName)
            print("known map: iMap=" + str(iMap))
        else:
            self.addMap(sOriginalDataName)
            print("adding new map")

            if bAllCtgNamesFromFasta:
                for ctg in dataFasta.vCtg:
                    #'CM020805.1 Formica selysi isolate DE90_pool_M chromosome 1, whole genome shotgun sequence' -> "CM020805.1"
                    sCtgName = ctg.name
                    ss = sCtgName.split(" ")
                    sPartName = (
                        sCtgName if len(ss) < 2 else ss[0]
                    )  # take oly part till the first space:
                    length = ctg.seqLength
                    self.vMap[iMap].addPart(sPartName, length)
            else:
                for (
                    sMarkerWithNameOfSeqContigInTheName
                ) in vsMarkerWithNameOfSeqContigInTheName:
                    ss = sMarkerWithNameOfSeqContigInTheName.split(
                        "___"
                    )  # NODE_13_length_173790_cov_2.7937___8823
                    sCtg = ss[0]  # NODE_13_length_173790_cov_2.7937
                    coor = int(ss[1])
                    self.vMap[iMap].addPartIfNoWithSuchName(sCtg, coor)

        LinkageGroup = clLinkageGroup()
        id = 0
        vCopies = []  # [iMarker]
        sNamePrev = ""
        for sMarkerWithNameOfSeqContigInTheName in vsMarkerWithNameOfSeqContigInTheName:
            # print("marker "+sMarkerWithNameOfSeqContigInTheName)
            vCopies.append([])
            if sMarkerWithNameOfSeqContigInTheName == sNamePrev:
                # MarkerWithMultiplePos=self.vMarkerWithMultiplePos[id-1]
                vPosOnMap = MarkerWithMultiplePos.vvPosOnMap[iMap]
                # print(str(len(vPosOnMap)))
                vPosOnMap[0].iType += 1
            else:
                ss = sMarkerWithNameOfSeqContigInTheName.split(
                    "___"
                )  # NODE_13_length_173790_cov_2.7937___8823
                sCtg = ss[0]  # NODE_13_length_173790_cov_2.7937
                coor = int(ss[1])  # 8823

                iCtg = self.vMap[iMap].iPart(sCtg)
                MarkerWithMultiplePos = self.clMarkerWithMultiplePos()
                MarkerWithMultiplePos.sName = sMarkerWithNameOfSeqContigInTheName
                MarkerWithMultiplePos.sName_sourse = sOriginalDataName  # poka
                self.addMarker(
                    MarkerWithMultiplePos
                )  # here we also resize vvPosOnMap but we need the name (to add for faster search)
                iType = 0  # original marker
                MarkerWithMultiplePos.addPosOnMap(iMap, iCtg, coor, iType)
                id += 1
            sNamePrev = sMarkerWithNameOfSeqContigInTheName
        print("addMarkersWithNameOfSeqContigInTheName...Finished")

    def addMarkers_FastaOnly(
        self, sDataName, bTillFirstSpaceOnly=True, sFileNameFasta=""
    ):
        print("addMarkers_FastaOnly...")
        if sFileNameFasta == "":
            PrivmanLab = clPrivmanLab()
            dataFasta = PrivmanLab.SecCtgsByName(sDataName, True)  # clSecCtgs()
        else:
            dataFasta = clSecCtgs()
            dataFasta.readFromFastaFile(sFileNameFasta, -1, False)

        for sCtg in dataFasta.vCtgName:
            MarkerWithMultiplePos = self.clMarkerWithMultiplePos()
            if bTillFirstSpaceOnly:
                vs = sCtg.split(" ")
                sCtg = vs[0]
            MarkerWithMultiplePos.sName = sCtg
            MarkerWithMultiplePos.sName_sourse = sDataName
            self.addMarker(MarkerWithMultiplePos)
        print("addMarkers_FastaOnly...Done")

    def addMarkers_Dist(self, sMapName, x0=50, d=3000):
        print("addMarkers_Dist...")
        iMap = self.vsMapName.index(sMapName)
        myMap = self.vMap[iMap]
        # PrivmanLab=clPrivmanLab()
        # dataFasta=PrivmanLab.SecCtgsByName(sDataName,True)#clSecCtgs()
        iPart = 0
        for PartOfMap in myMap.vPartOfMap:
            sPartOfMap = PartOfMap.name
            xMax = PartOfMap.length
            x = x0
            while x <= PartOfMap.length - x0:
                MarkerWithMultiplePos = self.clMarkerWithMultiplePos()
                MarkerWithMultiplePos.sName = sPartOfMap + "___" + str(x)
                self.addMarker(MarkerWithMultiplePos)
                MarkerWithMultiplePos.sName_sourse = sMapName
                MarkerWithMultiplePos.nPosMax = 1
                MarkerWithMultiplePos.addPosOnMap(iMap, iPart, x, 0)
                x += d
            iPart += 1
        print("addMarkers_Dist...Done")

    def addPhysicalMap_byBlastResults(
        self,
        sOriginalDataName,
        sDataName,
        sFileNameBlastRes="",
        sFileNameFasta_OriginalData="",
    ):
        class clvMyInfoOnOverlap:
            def __init__(self):
                self.vMyInfoOnOverlap = []

            class clMyInfoOnOverlap:
                def __init__(self):
                    self.i_vsDB = -1  # index in vsDB
                    self.coorDB = -1  # coor on ctg from DB
                    self.lenght = -1  # length of overlap
                    self.bPosOrientation = (
                        True  # indicator that orientation is positive
                    )
                    self.sCtgDB = ""

                def fromLineOfBlastRes_get(self, coor, i, LineOfBlastRes, vsDB, lenght):

                    # no need
                    # coorPP=coor
                    # if coor<0:
                    # 	coorPP=vstartQ[i]
                    # coorDB=ReferenceGenome.attachMarkersToAnotherAssembly_simple___coorDB(coorPP,vstartQ[i],vstartDB[i],vendDB[i])

                    coorDB = LineOfBlastRes.coorDB_get(coor, -1)
                    bPosOrientation = LineOfBlastRes.bPosOrientation_get()
                    i_vsDB = vsDB.index(
                        vsDB[i]
                    )  # index in vsDB (i_vsDB <= i: unique => "=", else the most significant (first in the list))

                    self.i_vsDB = i_vsDB
                    self.coorDB = coorDB
                    self.lenght = lenght
                    self.bPosOrientation = bPosOrientation
                    self.sCtgDB = vsDB[i]

            def fromLinesOfBlastRes_get(self, coor, LinesOfBlastRes):
                vsDB = LinesOfBlastRes.vsDB_get()  # contig names from in Cnig_gn1
                vnLen = LinesOfBlastRes.vnLen_get()
                vstartQ = LinesOfBlastRes.vstartQ_get()
                vendQ = LinesOfBlastRes.vendQ_get()
                # vstartDB=LinesOfBlastRes.vstartDB_get()
                # vendDB=LinesOfBlastRes.vendDB_get()
                n = len(vsDB)

                vMyInfoOnOverlap = []
                # LinesOfBlastRes.makeArrays()
                for i in range(n):
                    if (coor >= vstartQ[i] and coor <= vendQ[i]) or (coor == -1):
                        LineOfBlastRes = LinesOfBlastRes.LinesOfBlastRes[i]
                        lenght = vnLen[i]
                        MyInfoOnOverlap = self.clMyInfoOnOverlap()
                        MyInfoOnOverlap.fromLineOfBlastRes_get(
                            coor, i, LineOfBlastRes, vsDB, lenght
                        )
                        vMyInfoOnOverlap.append(MyInfoOnOverlap)

                # select from vMyInfoOnOverlap only the longest overlap for each ctg from vsDB
                #
                # sort
                def MyFunc(MyInfoOnOverlap):
                    return (
                        MyInfoOnOverlap.i_vsDB * 1000000000 - MyInfoOnOverlap.lenght
                    )  # i_vsDB*100000000 - <length of overlap>

                vMyInfoOnOverlap.sort(key=MyFunc)
                #
                self.vMyInfoOnOverlap = []
                i_vsDB_done = -1
                for MyInfoOnOverlap in vMyInfoOnOverlap:
                    i_vsDB = MyInfoOnOverlap.i_vsDB
                    if i_vsDB > i_vsDB_done:
                        self.vMyInfoOnOverlap.append(MyInfoOnOverlap)
                        i_vsDB_done = i_vsDB

            def addPositionsOfMarkerToMap(
                self, MarkerWithMultiplePos, iMap, vsPartName, iTypeVersion=1
            ):
                nCopies = len(
                    self.vMyInfoOnOverlap
                )  # number of contigs from DB covering the marker (or quary)
                if nCopies > 0:
                    # vCopies[LGmarker.m.id]
                    for iCopy in range(nCopies):
                        MyInfoOnOverlap = self.vMyInfoOnOverlap[iCopy]
                        sCtgNameDB = MyInfoOnOverlap.sCtgDB
                        coorOnCtgDB = MyInfoOnOverlap.coorDB
                        lengthOfOverlap_ctgQ_ctgDB = (
                            MyInfoOnOverlap.lenght
                        )  # not in use
                        bPosOrientation = MyInfoOnOverlap.bPosOrientation

                        # vCopies[LGmarker.m.id].append([iCtg,sCtgNameDB,coorOnCtgDB])#[iCtg in Cnig_gn2, name of ctg from Cnig_gn1, coor on ctg from Cnig_gn1]
                        # s=str(iMarker)+"\t"+LGmarker.m.sMarker
                        # s+="\t"+str(iCopy)+"\t"+str(nCopies)
                        # s+="\t"+sCtgNameDB+"\t"+str(coorOnCtgDB)+"\t"+str(lengthOfOverlap_ctgQ_ctgDB)
                        # f1.write(s+"\n")

                        if not (sCtgNameDB in vsPartName):
                            print(str(vsPartName))
                        iCtg1 = vsPartName.index(sCtgNameDB)

                        # iType
                        if iTypeVersion == 0:  # old
                            iType = (
                                nCopies - 1
                            )  # number of copies found by blast-1 => 0 is ok
                        if iTypeVersion == 1:  # new:
                            if nCopies == 1:
                                iType = 0 if bPosOrientation else -0.001
                            else:
                                iType = iCopy if bPosOrientation else -iCopy

                        MarkerWithMultiplePos.addPosOnMap(
                            iMap, iCtg1, coorOnCtgDB, iType
                        )
                        # print MarkerWithMultiplePos.sName
                        # print "len(self.vvPosOnMap[iMap])="+str(len(MarkerWithMultiplePos.vvPosOnMap[iMap]))
                        # print "nPosMax="+str(MarkerWithMultiplePos.nPosMax)

        def vMarkerWithMultiplePos_iCtg_get(
            iMapOriginal, MapOriginal, LinesOfBlastRes, vMarkerAll, vsMarkerNameAll
        ):  # vMarkerWithMultiplePos, iCtg=
            # vMarkerWithMultiplePos = list of markers on query contig (or entier query contig)
            # iCtg is -1 of index of quary contig
            #
            # iCtg=fasta1.vCtgName.index(LinesOfBlastRes.sQ) #iCtg in Cnig_gn2
            # self.attachMarkersToAnotherAssembly___processBlock(iQ,vsDB,vnLen,vstartQ,vendQ,vstartDB,vendDB,f1,fasta1,fasta2,markersOnRefGenome)
            iCtg = -1
            id = -1
            vMarkerWithMultiplePos = []
            if iMapOriginal >= 0:
                vsPartNameOriginal = MapOriginal.vsPartName
                iCtg = vsPartNameOriginal.index(
                    LinesOfBlastRes.sQ
                )  # local marker number (sequence number in fasta)
                for id in MapOriginal.vPartOfMap[iCtg].vidMarker:
                    vMarkerWithMultiplePos.append(vMarkerAll[id])
            else:
                id = vsMarkerNameAll.index(LinesOfBlastRes.sQ)
                vMarkerWithMultiplePos.append(vMarkerAll[id])

            if bPrintDetails:
                print(str(len(vMarkerWithMultiplePos)) + " " + str(iMapOriginal))
            # print LinesOfBlastRes.sQ+": iCtg="+str(iCtg)+" n="+str(len(vMarkerWithMultiplePos))+" iMapOriginal="+str(iMapOriginal)
            # print LinesOfBlastRes.sQ+": id="+str(id)+" n="+str(len(vMarkerWithMultiplePos))+" iMapOriginal="+str(iMapOriginal)

            # reference genome is Q
            return vMarkerWithMultiplePos, iCtg

        def PosOnMap_get(
            MarkerWithMultiplePos,
            iMapOriginal,
            sOriginalDataName,
            dataFasta,
            LinesOfBlastRes,
            bPrintDetails,
        ):
            vPosOnMap = (
                []
            )  # position on query contig (usualy single; if marker is entire contig then -1)
            if iMapOriginal >= 0:
                vPosOnMap = MarkerWithMultiplePos.vvPosOnMap[iMapOriginal]
            else:
                # print "2476"
                if bPrintDetails:
                    print(
                        MarkerWithMultiplePos.sName_sourse
                        + " "
                        + sOriginalDataName
                        + "  "
                        + MarkerWithMultiplePos.sName
                        + " "
                        + LinesOfBlastRes.sQ
                    )
                if (
                    MarkerWithMultiplePos.sName_sourse == sOriginalDataName
                    and MarkerWithMultiplePos.sName == LinesOfBlastRes.sQ
                ):
                    # print "3020"
                    # print "dataFasta.vCtgName="+str(dataFasta.vCtgName)
                    # if MarkerWithMultiplePos.sName in dataFasta.vCtgName:
                    if MarkerWithMultiplePos.sName in dataFasta.vCtgNameTillFirstSpace:
                        # print "2480"
                        iPart = dataFasta.vCtgNameTillFirstSpace.index(
                            MarkerWithMultiplePos.sName
                        )
                        iCtg = iPart
                        coor = -1
                        iType = 0
                        PosOnMap = MarkerWithMultiplePos.clPosOnMap(iPart, coor, iType)
                        vPosOnMap.append(PosOnMap)

            # print str(vPosOnMap)
            if len(vPosOnMap) > 0:
                if bPrintDetails:
                    print("PosOnMap=" + vPosOnMap[0].s())
                return vPosOnMap[
                    0
                ]  # if not position on MapOriginal (quary) is not single, then we use only the first one
            else:
                if bPrintDetails:
                    print("PosOnMap is empty: " + dataFasta.vCtgName[0])
                return None

        # update self.vMarkerWithMultiplePos
        print(
            "addPhysicalMap_byBlastResults "
            + sOriginalDataName
            + " vs "
            + sDataName
            + "..."
        )
        iMapOriginal = self.iMap(sOriginalDataName)  # markers
        iMap = self.addMapFromFasta(sDataName)  # chromosomes

        MapOriginal = None
        if iMapOriginal >= 0:  # hence, each query contig can have several markers
            MapOriginal = self.vMap[iMapOriginal]
        vsPartName = self.vMap[iMap].vsPartName

        # ReferenceGenome=clReferenceGenome()
        dataFasta = clSecCtgs()
        if sFileNameBlastRes == "":
            PrivmanLab = clPrivmanLab()
            if iMapOriginal < 0:  # hence, each query contig is a single marker
                dataFasta = PrivmanLab.SecCtgsByName(
                    sOriginalDataName, True
                )  # clSecCtgs()   sDataName
            iBlastResIndex = PrivmanLab.MyData.iBlastResIndex_get(
                sOriginalDataName, sDataName
            )
            if iBlastResIndex < 0:
                print("no such blast result!")
                return
            sFileNameBlastRes = PrivmanLab.MyData.vBlastRes[
                iBlastResIndex
            ].sFileNameBlastRes
        else:
            if iMapOriginal < 0:  # hence, each query contig is a single marker
                # dataFasta=PrivmanLab.SecCtgsByName(sOriginalDataName,True)
                dataFasta.readFromFastaFile(sFileNameFasta_OriginalData, -1, False)

        f = open(sFileNameBlastRes, "r")  # reference genome (e.g., Cnig_gn1) is DB

        myBlastRes = clBlastRes()
        iMarker = 0
        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        # markersOnRefGenome=[]
        bPrintDetails = False  # True #
        while bContinue:
            iBlock += 1
            if bPrintDetails:
                if iBlock % 100 == 1:
                    print("attachMarkersToAnotherAssembly_simple..." + str(iBlock))
            LinesOfBlastRes = myBlastRes.clLinesOfBlastRes(
                sFirstStringOfBlockOfFastaResult, f
            )
            sFirstStringOfBlockOfFastaResult = (
                LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
            )
            bContinue = LinesOfBlastRes.bNotTheLastBlock
            vMarkerAll = self.vMarkerWithMultiplePos
            vsMarkerNameAll = self.vsMarkerName
            vMarkerWithMultiplePos, iCtg = vMarkerWithMultiplePos_iCtg_get(
                iMapOriginal, MapOriginal, LinesOfBlastRes, vMarkerAll, vsMarkerNameAll
            )
            LinesOfBlastRes.makeArrays()

            for MarkerWithMultiplePos in vMarkerWithMultiplePos:
                PosOnMap = PosOnMap_get(
                    MarkerWithMultiplePos,
                    iMapOriginal,
                    sOriginalDataName,
                    dataFasta,
                    LinesOfBlastRes,
                    bPrintDetails,
                )  # position on original map
                if bPrintDetails:
                    print("iPart=" + str(PosOnMap.iPart) + ", iCtg=" + str(iCtg))
                if not (PosOnMap is None):
                    if (iMapOriginal < 0) or (PosOnMap.iPart == iCtg):
                        coor = (
                            PosOnMap.coor
                        )  # physical position on ctg (OriginalData); =-1 for entire contig
                        Marker_vMyInfoOnOverlap = clvMyInfoOnOverlap()
                        Marker_vMyInfoOnOverlap.fromLinesOfBlastRes_get(
                            coor, LinesOfBlastRes
                        )
                        Marker_vMyInfoOnOverlap.addPositionsOfMarkerToMap(
                            MarkerWithMultiplePos, iMap, vsPartName
                        )
                        iMarker += 1
        f.close()
        print(
            "addPhysicalMap_byBlastResults "
            + sOriginalDataName
            + " vs "
            + sDataName
            + "...Done"
        )

    def OLDaddPhysicalMap_byBlastResults(self, sOriginalDataName, sDataName):
        class clMyInfoOnOverlap:
            def __init__(self, i, coorDB, lenght, bPosOrientation):
                self.i_in_vsDB = i  # index in vsDB
                self.coor_on_ctgDB = coorDB  # coor on ctg from DB
                self.lenght = lenght  # length of overlap
                self.bPosOrientation = (
                    bPosOrientation  # indicator that orientation is positive
                )

        # update self.vMarkerWithMultiplePos
        print(
            "addPhysicalMap_byBlastResults "
            + sOriginalDataName
            + " vs "
            + sDataName
            + "..."
        )
        iMapOriginal = self.iMap(sOriginalDataName)  # markers
        iMap = self.addMapFromFasta(sDataName)  # chromosomes

        vsPartNameOriginal = []
        if iMapOriginal >= 0:  # hence, each query contig can have several markers
            vsPartNameOriginal = self.vMap[iMapOriginal].vsPartName
        vsPartName = self.vMap[iMap].vsPartName

        # ReferenceGenome=clReferenceGenome()

        PrivmanLab = clPrivmanLab()
        dataFasta = clSecCtgs()
        if iMapOriginal < 0:  # hence, each query contig is a single marker
            dataFasta = PrivmanLab.SecCtgsByName(
                sOriginalDataName, True
            )  # clSecCtgs()   sDataName
        iBlastResIndex = PrivmanLab.MyData.iBlastResIndex_get(
            sOriginalDataName, sDataName
        )
        if iBlastResIndex < 0:
            print("no such blast result!")
            return
        sFileNameBlastRes = PrivmanLab.MyData.vBlastRes[
            iBlastResIndex
        ].sFileNameBlastRes
        f = open(sFileNameBlastRes, "r")  # reference genome (e.g., Cnig_gn1) is DB

        myBlastRes = clBlastRes()
        iMarker = 0
        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        # markersOnRefGenome=[]
        bPrintDetails = True  # False
        while bContinue:
            iBlock += 1
            if bPrintDetails:
                if iBlock % 100 == 1:
                    print("attachMarkersToAnotherAssembly_simple..." + str(iBlock))
            LinesOfBlastRes = myBlastRes.clLinesOfBlastRes(
                sFirstStringOfBlockOfFastaResult, f
            )
            sFirstStringOfBlockOfFastaResult = (
                LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
            )
            bContinue = LinesOfBlastRes.bNotTheLastBlock

            # vMarkerWithMultiplePos = list of markers on query contig (or entier query contig)
            #
            # iCtg=fasta1.vCtgName.index(LinesOfBlastRes.sQ) #iCtg in Cnig_gn2
            # self.attachMarkersToAnotherAssembly___processBlock(iQ,vsDB,vnLen,vstartQ,vendQ,vstartDB,vendDB,f1,fasta1,fasta2,markersOnRefGenome)
            iCtg = -1
            id = -1
            vMarkerWithMultiplePos = []
            if iMapOriginal >= 0:
                iCtg = vsPartNameOriginal.index(
                    LinesOfBlastRes.sQ
                )  # local marker number (sequence number in fasta)
                for id in self.vMap[iMapOriginal].vPartOfMap[iCtg].vidMarker:
                    vMarkerWithMultiplePos.append(self.vMarkerWithMultiplePos[id])
            else:
                id = self.vsMarkerName.index(LinesOfBlastRes.sQ)
                vMarkerWithMultiplePos.append(self.vMarkerWithMultiplePos[id])
            if bPrintDetails:
                print(str(len(vMarkerWithMultiplePos)) + " " + str(iMapOriginal))
            # print LinesOfBlastRes.sQ+": iCtg="+str(iCtg)+" n="+str(len(vMarkerWithMultiplePos))+" iMapOriginal="+str(iMapOriginal)
            # print LinesOfBlastRes.sQ+": id="+str(id)+" n="+str(len(vMarkerWithMultiplePos))+" iMapOriginal="+str(iMapOriginal)

            # reference genome is Q
            vsDB = LinesOfBlastRes.vsDB_get()  # contig names from in Cnig_gn1
            vnLen = LinesOfBlastRes.vnLen_get()
            vstartQ = LinesOfBlastRes.vstartQ_get()
            vendQ = LinesOfBlastRes.vendQ_get()
            vstartDB = LinesOfBlastRes.vstartDB_get()
            vendDB = LinesOfBlastRes.vendDB_get()
            LinesOfBlastRes.makeArrays()

            n = len(vsDB)
            for MarkerWithMultiplePos in vMarkerWithMultiplePos:
                vPosOnMap = (
                    []
                )  # position on query contig (usualy single; if marker is entire contig then -1)
                if iMapOriginal >= 0:
                    vPosOnMap = MarkerWithMultiplePos.vvPosOnMap[iMapOriginal]
                else:
                    # print "2476"
                    if bPrintDetails:
                        print(
                            MarkerWithMultiplePos.sName_sourse
                            + " "
                            + sOriginalDataName
                            + "  "
                            + MarkerWithMultiplePos.sName
                            + " "
                            + LinesOfBlastRes.sQ
                        )
                    if (
                        MarkerWithMultiplePos.sName_sourse == sOriginalDataName
                        and MarkerWithMultiplePos.sName == LinesOfBlastRes.sQ
                    ):
                        # print "2478"
                        # print "dataFasta.vCtgName="+str(dataFasta.vCtgName)
                        if MarkerWithMultiplePos.sName in dataFasta.vCtgName:
                            # print "2480"
                            iPart = dataFasta.vCtgName.index(
                                MarkerWithMultiplePos.sName
                            )
                            iCtg = iPart
                            coor = -1
                            iType = 0
                            PosOnMap = MarkerWithMultiplePos.clPosOnMap(
                                iPart, coor, iType
                            )
                            vPosOnMap.append(PosOnMap)

                # print str(vPosOnMap)
                if len(vPosOnMap) > 0:
                    PosOnMap = vPosOnMap[
                        0
                    ]  # if not position on MapOriginal (quary) is not single, then we use only the first one
                    if PosOnMap.iPart == iCtg:
                        coor = (
                            PosOnMap.coor
                        )  # physical position on ctg (OriginalData); =-1 for entire contig

                        qqq = (
                            []
                        )  # [index in vsDB, coor on ctg from Cnig_gn1, length of overlap,bPosOrientation]
                        for i in range(n):
                            if (coor >= vstartQ[i] and coor <= vendQ[i]) or (
                                coor == -1
                            ):
                                coorPP = coor  # no need
                                if coor < 0:
                                    coorPP = vstartQ[i]
                                # coorDB=ReferenceGenome.attachMarkersToAnotherAssembly_simple___coorDB(coorPP,vstartQ[i],vstartDB[i],vendDB[i])
                                # LinesOfBlastRes.makeArrays()
                                coorDB = LinesOfBlastRes.LinesOfBlastRes[i].coorDB_get(
                                    coor, -1
                                )
                                bPosOrientation = LinesOfBlastRes.LinesOfBlastRes[
                                    i
                                ].bPosOrientation_get()
                                i_vsDB = vsDB.index(
                                    vsDB[i]
                                )  # index in vsDB (i_vsDB <= i: unique => "=", else the most significant (first in the list))
                                qqq.append(
                                    [i_vsDB, coorDB, vnLen[i], bPosOrientation]
                                )  # [index in vsDB, coor on ctg from Cnig_gn1, length of overlap,bPosOrientation]

                        # select from qqq only the longest overlap for each ctg from vsDB
                        def MyFunc(q):
                            return (
                                q[0] * 1000000000 - q[2]
                            )  # i_vsDB*100000000 - <length of overlap>

                        qqq.sort(key=MyFunc)
                        qqqq = []
                        i_vsDB_done = -1
                        for q in qqq:
                            i_vsDB = q[0]
                            if i_vsDB > i_vsDB_done:
                                qqqq.append(q)
                                i_vsDB_done = i_vsDB

                        nCopies = len(
                            qqqq
                        )  # number of contigs from Cnig_gn1 covering the marker (from Cnig_gn2)
                        if nCopies > 0:
                            # vCopies[LGmarker.m.id]
                            for iCopy in range(nCopies):
                                q = qqqq[iCopy]
                                sCtgNameDB = vsDB[q[0]]
                                coorOnCtgDB = q[1]
                                lengthOfOverlap_ctgQ_ctgDB = q[2]  # not in use
                                bPosOrientation = q[3]

                                # vCopies[LGmarker.m.id].append([iCtg,sCtgNameDB,coorOnCtgDB])#[iCtg in Cnig_gn2, name of ctg from Cnig_gn1, coor on ctg from Cnig_gn1]
                                # s=str(iMarker)+"\t"+LGmarker.m.sMarker
                                # s+="\t"+str(iCopy)+"\t"+str(nCopies)
                                # s+="\t"+sCtgNameDB+"\t"+str(coorOnCtgDB)+"\t"+str(lengthOfOverlap_ctgQ_ctgDB)
                                # f1.write(s+"\n")

                                if not (sCtgNameDB in vsPartName):
                                    print(str(vsPartName))
                                iCtg1 = vsPartName.index(sCtgNameDB)

                                # old
                                iType = (
                                    nCopies - 1
                                )  # number of copies found by blast-1 => 0 is ok
                                #
                                # new:
                                if nCopies == 1:
                                    iType = 0 if bPosOrientation else -0.001
                                else:
                                    iType = iCopy if bPosOrientation else -iCopy

                                MarkerWithMultiplePos.addPosOnMap(
                                    iMap, iCtg1, coorOnCtgDB, iType
                                )
                                # print MarkerWithMultiplePos.sName
                                # print "len(self.vvPosOnMap[iMap])="+str(len(MarkerWithMultiplePos.vvPosOnMap[iMap]))
                                # print "nPosMax="+str(MarkerWithMultiplePos.nPosMax)
                        iMarker += 1
        f.close()
        print(
            "addPhysicalMap_byBlastResults "
            + sOriginalDataName
            + " vs "
            + sDataName
            + "...Done"
        )

    def noNeed_______attachMarkersToAnotherAssembly_simple(
        self, Genotypes, MarkersWithMultiplePos
    ):
        """
        #Genotypes: clGenotypes()
        #used to
        #1. map markers from Cnig_gn2(original for GWAS) to Cnig_gn1(reference, i.e., self)
        #or
        #2. map markers from Cnig_gn1(original for genetic mapping based on 117 males) to new assemblies(reference, i.e., self)
        #
        #Output file 1: (only for markers in overlaps found by BLAST)
        #shapka: iMarker markerName iCopy nCopies ctg_Cnig_gn1 coor_Cnig_gn1 lengthOverlap
        #
        #Output file 2: (for all markers)
        #shapka: iMarker markerName nCopies
        #
        #
        #names of ctg of marker: scaffold1|size1555347 (GWAS markers are on Cnig_gn2 contigs)
        #name of marker: scaffold22|size714790___151541
        #name from DB: NODE_343_length_67353_cov_2.59656 (reference genome is Cnig_gn1)

        #poka new/ in Future it can be loaded and updated


        print "attachMarkersToAnotherAssembly_simple..."
        myBlastRes=clBlastRes()

        fasta1=self.originalDataFasta#e.g., Cnig_gn2
        print "originalDataFasta file is "+self.originalDataFasta.fasta

        if len(self.dataFasta.vCtgName)==0:
                #self.name="Formica"
                self.dataFasta=PrivmanLab.SecCtgsByName(self.name)

        iMapOriginal=len(MarkersWithMultiplePos.vsMapName)#0
        MarkersWithMultiplePos.addMap(self.originalDataName)
        vsPartName=self.originalDataFasta.vCtgName
        MarkersWithMultiplePos.vvsPartName.append(vsPartName)

        iMap=len(MarkersWithMultiplePos.vsMapName)
        MarkersWithMultiplePos.addMap(self.name)
        vsPartName=self.dataFasta.vCtgName
        MarkersWithMultiplePos.vvsPartName.append(vsPartName)

        LinkageGroup=clLinkageGroup()
        id=0
        vCopies=[]#[iMarker]
        sNamePrev=""
        for m in Genotypes.vMarker:
                vCopies.append([])
                if m.sMarker==sNamePrev:
                        MarkerWithMultiplePos=MarkersWithMultiplePos.vMarkerWithMultiplePos[id-1]
                        MarkerWithMultiplePos.vvPosOnMap[iMapOriginal][0].iType+=1
                else:
                        LGmarker=LinkageGroup.clMarkerOfLG()#No real LG here
                        LGmarker.m=m

                        m.id=id
                        ss=m.sMarker.split('___')#NODE_13_length_173790_cov_2.7937___8823
                        sCtg=ss[0]#NODE_13_length_173790_cov_2.7937
                        coor=int(ss[1])#8823

                        iCtg=fasta1.vCtgName.index(sCtg)
                        ctg=fasta1.vCtg[iCtg]#original contig (e.g., from Cnig_gn2)
                        ctg.vLGmarker.append(LGmarker)

                        m.vPrivmanvPosOnCtg=[coor]

                        MarkerWithMultiplePos=MarkersWithMultiplePos.clMarkerWithMultiplePos()
                        MarkerWithMultiplePos.sName=m.sMarker
                        MarkerWithMultiplePos.sName_sourse=self.originalDataName#poka
                        MarkersWithMultiplePos.addMarker(MarkerWithMultiplePos)#here we also resize vvPosOnMap but we need the name (to add for faster search)
                        iType=0#original marker
                        MarkerWithMultiplePos.addPosOnMap(iMapOriginal,iCtg,coor,iType)
                        id+=1
                sNamePrev=m.sMarker
        #fasta1.readCoorFromLGs(vLG,ReferenceGenome,sSeqOriginalForMarkers,sSeqAssemblyName)

        print "len(MarkersWithMultiplePos.vMarkerWithMultiplePos)="+str(len(MarkersWithMultiplePos.vMarkerWithMultiplePos))

        f=open(self.sFileNameBlastResMeDB,'r')#reference genome (e.g., Cnig_gn1) is DB

        #Output file 1: (only for markers in overlaps found by BLAST)
        sFileOut=self.attachMarkersToAnotherAssembly_simple___sFileOut

        #poka not in use
        #sFileNameCtg_Cnig_gn1_onMyAssembly="C:\\Frenkel\\LTCPython\\VovaPy\\20200531a\\MappingReport.txt"

        f1=open(sFileOut,'w')
        s="iMarker"+"\t"+"marker"
        s+="\t"+"iCopy"+"\t"+"nCopies"
        s+="\t"+"ctgDB"+"\t"+"coorOnCtgDB"+"\t"+"lengthOverlap"
        f1.write(s+"\n")

        iMarker=0
        sFirstStringOfBlockOfFastaResult=""
        bContinue=True
        iBlock=0
        #markersOnRefGenome=[]
        bPrintDetails=False
        while bContinue:
                iBlock+=1
                if bPrintDetails:
                        if iBlock%100==1:
                                print "attachMarkersToAnotherAssembly_simple..."+str(iBlock)
                LinesOfBlastRes=myBlastRes.clLinesOfBlastRes(sFirstStringOfBlockOfFastaResult,f)
                sFirstStringOfBlockOfFastaResult=LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
                bContinue=LinesOfBlastRes.bNotTheLastBlock

                iCtg=fasta1.vCtgName.index(LinesOfBlastRes.sQ) #iCtg in Cnig_gn2
                #self.attachMarkersToAnotherAssembly___processBlock(iQ,vsDB,vnLen,vstartQ,vendQ,vstartDB,vendDB,f1,fasta1,fasta2,markersOnRefGenome)

                #reference genome is Q
                vsDB=LinesOfBlastRes.vsDB_get()#contig names from in Cnig_gn1
                vnLen=LinesOfBlastRes.vnLen_get()
                vstartQ=LinesOfBlastRes.vstartQ_get()
                vendQ=LinesOfBlastRes.vendQ_get()
                vstartDB=LinesOfBlastRes.vstartDB_get()
                vendDB=LinesOfBlastRes.vendDB_get()

                n=len(vsDB)
                ctg=fasta1.vCtg[iCtg]#in Cnig_gn2
                for LGmarker in ctg.vLGmarker:
                        #poka
                        MarkerWithMultiplePos=MarkersWithMultiplePos.vMarkerWithMultiplePos[LGmarker.m.id]

                        coor=LGmarker.m.vPrivmanvPosOnCtg[0]#physical position on ctg from assembly in Cnig_gn2
                        qqq=[]
                        for i in range(n):
                                if coor>=vstartQ[i] and coor <=vendQ[i]:
                                        coorDB=self.attachMarkersToAnotherAssembly_simple___coorDB(coor,vstartQ[i],vstartDB[i],vendDB[i])
                                        i_vsDB=vsDB.index(vsDB[i])#index in vsDB (i_vsDB <= i: unique => "=", else the most significant (first in the list))
                                        qqq.append([i_vsDB,coorDB,vnLen[i]])#[index in vsDB, coor on ctg from Cnig_gn1, length of overlap]

                        #select from qqq only the longest overlap for each ctg from Cnig_gn1
                        def MyFunc(q):
                                return q[0]*1000000000-q[2]#i_vsDB*100000000 - <length of overlap>
                        qqq.sort(key=MyFunc)
                        qqqq=[]
                        i_vsDB_done=-1
                        for q in qqq:
                                i_vsDB=q[0]
                                if i_vsDB>i_vsDB_done:
                                        qqqq.append(q)
                                        i_vsDB_done=i_vsDB

                        nCopies=len(qqqq)#number of contigs from Cnig_gn1 covering the marker (from Cnig_gn2)
                        if nCopies>0:
                                #vCopies[LGmarker.m.id]
                                for iCopy in range(nCopies):
                                        q=qqqq[iCopy]
                                        sCtgNameDB=vsDB[q[0]]
                                        coorOnCtgDB=q[1]
                                        lengthOfOverlap_ctgQ_ctgDB=q[2]

                                        vCopies[LGmarker.m.id].append([iCtg,sCtgNameDB,coorOnCtgDB])#[iCtg in Cnig_gn2, name of ctg from Cnig_gn1, coor on ctg from Cnig_gn1]
                                        s=str(iMarker)+"\t"+LGmarker.m.sMarker
                                        s+="\t"+str(iCopy)+"\t"+str(nCopies)
                                        s+="\t"+sCtgNameDB+"\t"+str(coorOnCtgDB)+"\t"+str(lengthOfOverlap_ctgQ_ctgDB)
                                        f1.write(s+"\n")

                                        if not (sCtgNameDB in self.dataFasta.vCtgName):
                                                print str(self.dataFasta.vCtgName)
                                        iCtg1=self.dataFasta.vCtgName.index(sCtgNameDB)
                                        iType=nCopies-1#number of copies found by blast-1 => 0 is ok
                                        MarkerWithMultiplePos.addPosOnMap(iMap,iCtg1,coorOnCtgDB,iType)
                                        #print MarkerWithMultiplePos.sName
                                        #print "len(self.vvPosOnMap[iMap])="+str(len(MarkerWithMultiplePos.vvPosOnMap[iMap]))
                                        #print "nPosMax="+str(MarkerWithMultiplePos.nPosMax)
                        iMarker+=1
        f.close()
        f1.close()

        #Output file 2: (for all markers)
        #shapka: iMarker markerName nCopies
        sFileOut1=self.attachMarkersToAnotherAssembly_simple___sFileOut1
        f1=open(sFileOut1,'w')

        s="iMarker"+"\t"+"marker"+"\t"+"nCopies"
        f1.write(s+"\n")

        n=len(Genotypes.vMarker)
        for i in range(n):
                s=str(i)+"\t"+Genotypes.vMarker[i].sMarker+"\t"+str(len(vCopies[i]))
                f1.write(s+"\n")
        f1.close()
        print "attachMarkersToAnotherAssembly_simple...Finished. see two files"
        print "1: "+sFileOut
        print "2: "+sFileOut1
        return MarkersWithMultiplePos
        """

    def addGeneticMap_from_vLG(self, vLG):
        self.addMap("Genetic")
        iMap = self.iMap("Genetic")
        for LG in vLG:
            length = -1  # poka
            self.vMap[iMap].addPart(LG.name, length)

        ggg = clGenotypes()
        VovaServ = clVovaServ()
        iLG = 0
        nNotFound = 0
        for LG in vLG:
            for LGmarker in LG.vLGmarkerOrderedByCoorOnLG:
                m = LGmarker.m
                sMyNameOfGoodMarker = (
                    LGmarker.m.sMarker
                )  # sMarker=NODE_1000_length_42440_cov_2.75993_B0_start18296,23592,23592,32628
                coorOnLG = LGmarker.coorOnLG
                iType = (
                    0 if LGmarker.indexOnPath >= 0 else 1
                )  # 0 - skeleton, 1 - good but not skeleton
                (
                    sChr,
                    iBlockOnChr,
                    vPosBp,
                ) = ggg.compressMarkersOfAllCtgs_ctg_sMarkerDeshifrate(
                    sMyNameOfGoodMarker
                )
                vPosBp = VovaServ.vSortAndDelRepeats_get(vPosBp)
                for PosBp in vPosBp:
                    ss = (
                        sChr + "___" + str(PosBp)
                    )  # NODE_1000_length_42440_cov_2.75993___18296
                    if ss in self.vsMarkerName:
                        im = self.vsMarkerName.index(ss)
                        MarkerWithMultiplePos = self.vMarkerWithMultiplePos[im]
                        MarkerWithMultiplePos.sName_sourse += "," + sMyNameOfGoodMarker
                        MarkerWithMultiplePos.addPosOnMap(iMap, iLG, coorOnLG, iType)
                    else:
                        nNotFound += 1
                        print("can't find marker " + str(nNotFound) + ": " + ss)
            iLG += 1
        self.vMap[iMap].lengthSumOfPrev_make()

    def addGeneticMap_from_geneticMap(
        self, geneticMap, sMapName, iChrNamingVersion=0, bData_For_Cnig_gn3=False
    ):
        print("addGeneticMap_from_geneticMap...")
        self.addMap(sMapName)
        iMap = self.iMap(sMapName)
        for Chromosome in geneticMap.vChromosome:
            length = Chromosome.length
            if length <= 0:
                length = Chromosome.geneticLengthBasedOnSkeletonMarlers_cM
            sChrName = Chromosome.vsName[iChrNamingVersion]
            self.vMap[iMap].addPart(sChrName, length)

        # print geneticMap.vsMarkerName
        # ggg=clGenotypes()
        i = 0
        for MarkerWithMultiplePos in self.vMarkerWithMultiplePos:
            iMarker = -1
            if bData_For_Cnig_gn3:
                ss = MarkerWithMultiplePos.sName.split(
                    "_"
                )  # NODE_1000_length_42440_cov_2.75993___18296
                if (
                    len(ss) > 8
                ):  # others markers (e.g., transcriptom) are not suitable for this
                    sCtg = ss[1]
                    posPhysOnCtg = int(ss[8])
                    iMarker, sMarker = geneticMap.iMarkerBy_sCtg_posPhysOnCtg(
                        sCtg, posPhysOnCtg
                    )
                    # print str(i)+"\t"+MarkerWithMultiplePos.sName+"\t"+sMarker+"\t"+str(iMarker)
            else:
                if MarkerWithMultiplePos.sName in geneticMap.vsMarkerName:
                    iMarker = geneticMap.vsMarkerName.index(MarkerWithMultiplePos.sName)
            if iMarker >= 0:
                Marker = geneticMap.vMarker[iMarker]
                iChr = Marker.Chromosome.id
                coorOnChr = Marker.coor
                iType = Marker.iType
                MarkerWithMultiplePos.addPosOnMap(iMap, iChr, coorOnChr, iType)
            i += 1
        self.vMap[iMap].lengthSumOfPrev_make()
        print("addGeneticMap_from_geneticMap...Done")

    def addGeneticMap_with_renamed_and_reoriented_chromosomes(
        self,
        sMapToRename="Genetic",
        sMapChrNameAndOrientation="Besan",
        sMapNew="mapGenetic",
    ):
        print("addGeneticMap_with_renamed_and_reoriented_chromosomes...")
        sFileNameLog = "addGeneticMap_with_renamed_and_reoriented_chromosomes.txt"
        f = open(sFileNameLog, "w")

        self.addMap(sMapNew)
        iMapToRename = self.iMap(sMapToRename)
        iMapChrNameAndOrientation = self.iMap(sMapChrNameAndOrientation)
        iMapNew = self.iMap(sMapNew)
        MapToRename = self.vMap[iMapToRename]
        MapChrNameAndOrientation = self.vMap[iMapChrNameAndOrientation]
        MapNew = self.vMap[iMapNew]
        MapNew.sScale = MapToRename.sScale  # bp, cM

        vsPart_sMapToRename_toExclude = []
        if sMapToRename == "Genetic":
            vsPart_sMapToRename_toExclude = [
                "LG25",
                "LG26",
            ]  # these linkage groups have zero length in genetic map. Eyal: Don't give name of chromosome

        # vsPartName=[]
        # vPartOfMap=[]
        iPart_MapToRename = -1
        for PartOfMap_MapToRename in MapToRename.vPartOfMap:

            vvCoor_MapToRename_MapChrNameAndOrientation = []
            for (
                PartOfMap_MapChrNameAndOrientation
            ) in MapChrNameAndOrientation.vPartOfMap:
                vvCoor_MapToRename_MapChrNameAndOrientation.append([])

            length_MapToRename = 0
            for idMarker in PartOfMap_MapToRename.vidMarker:
                Marker = self.vMarkerWithMultiplePos[idMarker]
                PosOnMap_MapToRename = Marker.vvPosOnMap[iMapToRename][0]
                coor_MapToRename = PosOnMap_MapToRename.coor

                if length_MapToRename < coor_MapToRename:
                    length_MapToRename = coor_MapToRename
                if Marker.nPos(iMapChrNameAndOrientation) == 1:
                    PosOnMap_ChrNameAndOrientation = Marker.vvPosOnMap[
                        iMapChrNameAndOrientation
                    ][0]
                    iPart_ChrNameAndOrientation = PosOnMap_ChrNameAndOrientation.iPart
                    coor_ChrNameAndOrientation = PosOnMap_ChrNameAndOrientation.coor

                    Coor_MapToRename_MapChrNameAndOrientation = [
                        coor_MapToRename,
                        coor_ChrNameAndOrientation,
                    ]
                    vvCoor_MapToRename_MapChrNameAndOrientation[
                        iPart_ChrNameAndOrientation
                    ].append(Coor_MapToRename_MapChrNameAndOrientation)

            # test
            bNeed = True
            if (PartOfMap_MapToRename.name in vsPart_sMapToRename_toExclude) or (
                length_MapToRename == 0
            ):
                print(
                    PartOfMap_MapToRename.name
                    + " is excluded, L="
                    + str(length_MapToRename)
                )
                bNeed = False
            else:
                print(
                    PartOfMap_MapToRename.name
                    + " is not in "
                    + str(vsPart_sMapToRename_toExclude)
                )

            if bNeed:
                iPart_MapToRename += 1

                # new chromosome name
                iPart_ChrNameAndOrientation = 0
                n = len(vvCoor_MapToRename_MapChrNameAndOrientation[0])
                i = 0
                k = n
                for (
                    vCoor_MapToRename_MapChrNameAndOrientation
                ) in vvCoor_MapToRename_MapChrNameAndOrientation:
                    if i > 0:
                        k = len(vCoor_MapToRename_MapChrNameAndOrientation)
                        if n < k:
                            n = k
                            iPart_ChrNameAndOrientation = i
                    s = (
                        PartOfMap_MapToRename.name
                        + "\t"
                        + MapChrNameAndOrientation.vPartOfMap[i].name
                        + "\t"
                        + str(k)
                    )
                    f.write(s + "\n")
                    i += 1

                sName = MapChrNameAndOrientation.vPartOfMap[
                    iPart_ChrNameAndOrientation
                ].name
                MapNew.addPart(sName, length_MapToRename)

                # orientation
                vCoor_MapToRename_MapChrNameAndOrientation = (
                    vvCoor_MapToRename_MapChrNameAndOrientation[
                        iPart_ChrNameAndOrientation
                    ]
                )

                def MyFunc(q):
                    return q[0]

                vCoor_MapToRename_MapChrNameAndOrientation.sort(key=MyFunc)
                nP = 0
                nM = 0
                iq = -1
                q_prev = []
                for q in vCoor_MapToRename_MapChrNameAndOrientation:
                    iq += 1
                    if iq == 0:
                        q_prev = vCoor_MapToRename_MapChrNameAndOrientation[0]
                    if q[0] > q_prev[0]:
                        if q[1] > q_prev[1]:
                            nP += 1
                        else:
                            nM += 1
                    q_prev = q
                f.write("\n")
                s = (
                    sName
                    + "\t"
                    + str(n)
                    + "\t"
                    + str(nP)
                    + "\t"
                    + str(nM)
                    + "\t"
                    + str(nP - nM)
                    + "\t"
                    + str(length_MapToRename)
                )
                f.write(s + "\n\n")

                # add marker positions to MapNew
                for idMarker in PartOfMap_MapToRename.vidMarker:
                    Marker = self.vMarkerWithMultiplePos[idMarker]
                    PosOnMap_MapToRename = Marker.vvPosOnMap[iMapToRename][0]
                    coor_MapToRename = PosOnMap_MapToRename.coor
                    coor = (
                        coor_MapToRename
                        if nP >= nM
                        else length_MapToRename - coor_MapToRename
                    )
                    iType = PosOnMap_MapToRename.iType
                    Marker.addPosOnMap(iMapNew, iPart_MapToRename, coor, iType)
        f.close()
        self.vMap[iMapNew].lengthSumOfPrev_make()
        print("addGeneticMap_with_renamed_and_reoriented_chromosomes...Finished")

    def GeneticMap__get(self, sMap, sMap_set=""):
        # only one position for each marker

        GeneticMap = clGeneticMap()
        # self.vsMarkerName=[]
        # self.vMarker=[]
        # self.vChromosome=[]
        #
        # self.vsChrNamingVersionName=[]
        # self.sNameOfMap=""
        # self.GenomeMapComparisonGraph_map=None
        if sMap_set == "":
            sMap_set = sMap
        GeneticMap.sNameOfMap = sMap_set
        iMap = self.iMap(sMap)
        myMap = self.vMap[iMap]
        iChr = 0
        for PartOfMap in myMap.vPartOfMap:
            myChr = GeneticMap.clChromosome()
            GeneticMap.vChromosome.append(myChr)
            myChr.id = iChr
            myChr.vsName = [PartOfMap.name]  # [iVersion]
            myChr.geneticLengthBasedOnSkeletonMarlers_cM = PartOfMap.length
            myChr.length = PartOfMap.length  # poka
            for idMarker in PartOfMap.vidMarker:
                Marker = self.vMarkerWithMultiplePos[idMarker]
                sMarkerName = Marker.sName
                if not (sMarkerName in GeneticMap.vsMarkerName):
                    vPosOnMap = Marker.vvPosOnMap[iMap]

                    # coor=-1
                    # for PosOnMap in vPosOnMap:
                    # 	if PosOnMap.iPart==iChr:
                    # 		coor=PosOnMap.coor
                    # 		break
                    vPosOnMap = Marker.vPosOnMap_onPartOfMap_get(iMap, iChr)
                    PosOnMap = vPosOnMap[0]
                    coor = PosOnMap.coor
                    iType = PosOnMap.iType

                    indexOnPath = -1  # unknown here
                    # iType=len(vPosOnMap)
                    myMarker = myChr.clMarker(sMarkerName, myChr, iType, coor)
                    myChr.vMarker.append(myMarker)
                    GeneticMap.vsMarkerName.append(sMarkerName)
                    GeneticMap.vMarker.append(myMarker)
            iChr += 1
        return GeneticMap

    def imputation(self, iMapOk, iMapToImpute):
        # def #[coorMarker,Marker,iCtg1,coor1]
        vq = []
        # here we separate searching for posiotionPossible_get and imputation to protect from imputation-by-imputation
        for MarkerWithMultiplePos in self.vMarkerWithMultiplePos:
            vq.append(
                MarkerWithMultiplePos.posiotionPossible_get(iMapOk, iMapToImpute)
            )  # [coorMarker,Marker,iCtg1,coor1]
        m = 0
        for MarkerWithMultiplePos in self.vMarkerWithMultiplePos:
            q = vq[m]
            if len(q) > 0:
                # Marker=q[1]
                MarkerWithMultiplePos.addPosOnMap(iMapToImpute, q[2], q[3], 0.5)
                print("imputation " + MarkerWithMultiplePos.sName)
            m += 1

    class clAnchoringStatisticsPartToPart:
        def __init__(self, vMarkerAnchoredToTwoMaps):
            ##array of clMarkerAnchoredToTwoMaps
            # NB: all q in vMarkerAnchoredToTwoMaps are from the same part and ordered on PosOnMap1.coor
            self.MyCoorMin = 0  # coor on ctg
            self.MyCoorMax = 0  # coor on ctg
            self.MyGapMax = 0

            self.nIncr = 0
            self.nDecr = 0
            self.coorMin = 0
            self.coorMax = 0
            self.gapMax = 0

            self.n = len(vMarkerAnchoredToTwoMaps)
            self.start(vMarkerAnchoredToTwoMaps)

        def start(self, vq):
            iq = 0
            coorPrev = 0
            coorMyPrev = 0
            for q in vq:
                # q=[MarkerWithMultiplePos.sName,n,iPos,PosOnMap,vPosOnMapReference[0]]
                coorMy = q.PosOnMap1.coor
                coor = q.PosOnMap2.coor
                # print q[0]+" "+str(coorMy)+" "+str(coor)+"   "+str(coor-coorPrev)
                self.MyCoorMax = coorMy
                if iq == 0:
                    self.MyCoorMin = coorMy

                    self.coorMin = coor
                    self.coorMax = coor
                else:
                    if self.MyGapMax < coorMy - coorMyPrev:
                        self.MyGapMax = coorMy - coorMyPrev

                    if self.coorMin > coor:
                        self.coorMin = coor
                    if self.coorMax < coor:
                        self.coorMax = coor

                    if coor - coorPrev > 0:
                        self.nIncr += 1
                        if self.gapMax < coor - coorPrev:
                            self.gapMax = coor - coorPrev
                    if coor - coorPrev < 0:
                        self.nDecr += 1
                        if self.gapMax < -(coor - coorPrev):
                            self.gapMax = -(coor - coorPrev)
                coorPrev = coor
                coorMyPrev = coorMy
                iq += 1

        def appdate_vAssemblyElement(
            self,
            vq,
            aStart_set,
            aEnd_set,
            AssemblyMy,
            vAssemblyElement,
            bSubdivideOnOrderedParts=False,
            bFrom0=True,
            bToEndOfCtg=True,
        ):
            # usually:
            # parts of map1 = physical contigs
            # parts of map2 = genetic linkage groups (chromosomes)

            # poka:
            # bSubdivideOnOrderedParts=False => we add only one AssemblyMy to vAssemblyElement
            if len(vq) == 0:
                return  # no need to update

            # sort by coordinate within map1
            def MyFunc1(q):
                return q.PosOnMap1.coor

            # sort by coordinate within map2
            def MyFunc2(q):
                return q.PosOnMap2.coor

            # poka
            coorOnLG_min = vq[0].PosOnMap2.coor
            coorOnLG_max = vq[len(vq) - 1].PosOnMap2.coor

            # q.indexOfCoorOnMap2
            vq.sort(key=MyFunc2)
            iq = 0
            q_prev = -1
            for q in vq:
                if iq == 0:
                    q.indexOfCoorOnMap2 = 0
                else:
                    i = 0 if q.PosOnMap2.coor == q_prev.PosOnMap2.coor else 1
                    q.indexOfCoorOnMap2 = q_prev.indexOfCoorOnMap2 + i
                iq += 1
                q_prev = q

            vq.sort(key=MyFunc1)

            iPartMap1 = vq[0].PosOnMap1.iPart
            iPartMap2 = vq[0].PosOnMap2.iPart
            iPos = -1  # not defined
            iq = 0
            orientation = 0
            q_prev = vq[0]
            q_start = vq[0]
            q_end = vq[0]
            aStart = aStart_set
            aEnd = aEnd_set
            bToEndOfCtg_set = bToEndOfCtg
            vsMarkers = []
            vCoorOnCtg = []
            vCoorOnLG = []
            nP = 0
            nM = 0
            for q in vq:
                if iq == 0:
                    q_prev = q
                if q.indexOfCoorOnMap2 - q_prev.indexOfCoorOnMap2 != 0:
                    if q.indexOfCoorOnMap2 - q_prev.indexOfCoorOnMap2 > 0:
                        nP += 1
                    else:
                        nM += 1
                    if orientation == 0:
                        orientation = (
                            1 if q.indexOfCoorOnMap2 > q_prev.indexOfCoorOnMap2 else -1
                        )
                    else:
                        if bSubdivideOnOrderedParts:
                            if (
                                orientation
                                * (q.indexOfCoorOnMap2 - q_prev.indexOfCoorOnMap2)
                                < 0
                            ):
                                coorOnLG_min = (
                                    q_start.PosOnMap2.coor
                                    if orientation >= 0
                                    else q_end.PosOnMap2.coor
                                )
                                coorOnLG_max = (
                                    q_end.PosOnMap2.coor
                                    if orientation >= 0
                                    else q_start.PosOnMap2.coor
                                )
                                vAssemblyElement.append(
                                    AssemblyMy.clAssemblyElement(
                                        iPartMap2,
                                        iPartMap1,
                                        iPos,
                                        coorOnLG_min,
                                        coorOnLG_max,
                                        aStart,
                                        aEnd,
                                        orientation,
                                        vsMarkers,
                                        vCoorOnCtg,
                                        vCoorOnLG,
                                        bFrom0,
                                        bToEndOfCtg,
                                    )
                                )
                                aStart = q.PosOnMap1.coor
                                bFrom0 = False
                                q_start = q
                                orientation = 0
                                vsMarkers = []
                                vCoorOnCtg = []
                                vCoorOnLG = []
                q_end = q
                aEnd = q.PosOnMap1.coor
                bToEndOfCtg = False
                vsMarkers.append(q.sMarkerName)
                vCoorOnCtg.append(q.PosOnMap1.coor)
                vCoorOnLG.append(q.PosOnMap2.coor)
                iq += 1
                q_prev = q
            aEnd = aEnd_set
            bToEndOfCtg = bToEndOfCtg_set
            if bSubdivideOnOrderedParts:
                coorOnLG_min = (
                    q_start.PosOnMap2.coor if orientation >= 0 else q_end.PosOnMap2.coor
                )
                coorOnLG_max = (
                    q_end.PosOnMap2.coor if orientation >= 0 else q_start.PosOnMap2.coor
                )
            else:
                if nM == nP:
                    orientation = 0
                else:
                    if nM < nP:
                        orientation = 1
                    else:
                        orientation = -1
            vAssemblyElement.append(
                AssemblyMy.clAssemblyElement(
                    iPartMap2,
                    iPartMap1,
                    iPos,
                    coorOnLG_min,
                    coorOnLG_max,
                    aStart,
                    aEnd,
                    orientation,
                    vsMarkers,
                    vCoorOnCtg,
                    vCoorOnLG,
                    bFrom0,
                    bToEndOfCtg,
                )
            )

        def sShapka(self):
            s1 = "\t" + "coorMin" + "\t" + "coorMax" + "\t" + "maxGap"
            s1 += "\t" + "coorMinRef" + "\t" + "coorMaxRef" + "\t" + "maxGapRef"
            s1 += "\t" + "n" + "\t" + "nIncr" + "\t" + "nDecr"
            s1 += "\t" + "abs(nIncr-nDecr)" + "\t" + "orientation"
            return s1

        def s(self):
            s1 = (
                "\t"
                + str(self.MyCoorMin)
                + "\t"
                + str(self.MyCoorMax)
                + "\t"
                + str(self.MyGapMax)
            )
            s1 += (
                "\t"
                + str(self.coorMin)
                + "\t"
                + str(self.coorMax)
                + "\t"
                + str(self.gapMax)
            )
            s1 += "\t" + str(self.n) + "\t" + str(self.nIncr) + "\t" + str(self.nDecr)
            s1 += "\t" + str(abs(self.nIncr - self.nDecr)) + "\t"
            s1 += (
                "1"
                if self.nIncr > self.nDecr
                else ("-1" if self.nIncr < self.nDecr else "0")
            )
            return s1

    class clMarkerAnchoredToTwoMaps:
        def __init__(self, sMarkerName, nPosOnMap1, iPosRelevant, PosOnMap1, PosOnMap2):
            self.sMarkerName = sMarkerName  # for control only
            self.nPosOnMap1 = nPosOnMap1  # for control only
            self.iPosRelevant = iPosRelevant  # for control only
            self.PosOnMap1 = PosOnMap1  # pos on physical map
            self.PosOnMap2 = PosOnMap2  # pos on genetic map
            self.indexOfCoorOnMap2 = -1  # poka

    def anchorPartToPart(
        self,
        vvAssemblyElementMap,
        vvAssemblyElementMapRef,
        iMap,
        iPart,
        iMapReference,
        bTryToAddUnmapped,
        sMapGoodGenome="Formica",
        iTypeMax=0,
        iTypeMaxRef=0,
    ):  # viPartRef,vAnchoringStatisticsPartToPart0=
        PartOfMap = self.vMap[iMap].vPartOfMap[iPart]

        vq = []  # array of clMarkerAnchoredToTwoMaps
        viPartRef = (
            []
        )  # array of all iPartRef such that vPartOfMap[iPart] has common marker with PartOfMapRef[iPartRef]
        #
        # select only relevant markers
        vidMarkerWithMultiplePos = PartOfMap.vidMarker
        vMarkerWithMultiplePos = []
        for id in vidMarkerWithMultiplePos:
            vMarkerWithMultiplePos.append(self.vMarkerWithMultiplePos[id])
        #
        for MarkerWithMultiplePos in vMarkerWithMultiplePos:
            vPosOnMap = MarkerWithMultiplePos.vvPosOnMap[iMap]
            vPosOnMapReference = MarkerWithMultiplePos.vvPosOnMap[iMapReference]
            n = len(vPosOnMap)
            nRef = len(vPosOnMapReference)
            # print MarkerWithMultiplePos.sName+" "+str(n)+str(nRef)
            if nRef > 0 and n > 0:
                PosOnMapReference = vPosOnMapReference[
                    0
                ]  # only the first position on the reference genome is considered
                iPos = 0
                # print MarkerWithMultiplePos.sName
                for (
                    PosOnMap
                ) in (
                    vPosOnMap
                ):  # marker can have several positions on physical map (because of repeats and blast-based mapping) but has unique position on genetic map
                    if PosOnMap.iPart == iPart and (
                        iTypeMax == -1 or PosOnMap.iType <= iTypeMax
                    ):
                        q = self.clMarkerAnchoredToTwoMaps(
                            MarkerWithMultiplePos.sName,
                            n,
                            iPos,
                            PosOnMap,
                            PosOnMapReference,
                        )
                        vq.append(q)
                        iPartRef = PosOnMapReference.iPart
                        if not (iPartRef in viPartRef):
                            viPartRef.append(iPartRef)
                    iPos += 1

        # sort by coordinate within map vMap[iMap] (all elements of vq are from the same PartOfMap)
        def MyFunc(q):
            return q.PosOnMap1.coor

        vq.sort(key=MyFunc)

        bPrint = False
        if bPrint:
            print(PartOfMap.name)

        viPartRef0 = []
        vAnchoringStatisticsPartToPart0 = []
        AssemblyMy = clAssemblyMy(clSecCtgs(), "")

        partLength = PartOfMap.length

        bCanBeSeveralCopies = False
        if bCanBeSeveralCopies:
            for iPartRef in viPartRef:
                vqPP = []
                vqPP0 = []
                vAssemblyElement = []
                for q in vq:
                    if q.PosOnMap2.iPart == iPartRef:
                        vqPP.append(q)
                        if (iTypeMaxRef < 0) or (q.PosOnMap2.iType <= iTypeMaxRef):
                            vqPP0.append(q)
                if bPrint:
                    print(self.vMap[iMapReference].vPartOfMap[iPartRef].name)
                    print("All:")
                AnchoringStatisticsPartToPart = self.clAnchoringStatisticsPartToPart(
                    vqPP
                )

                if bPrint:
                    print("0 only:")
                AnchoringStatisticsPartToPart0 = self.clAnchoringStatisticsPartToPart(
                    vqPP0
                )
                AnchoringStatisticsPartToPart0.appdate_vAssemblyElement(
                    vqPP0,
                    0,
                    partLength,
                    AssemblyMy,
                    vAssemblyElement,
                    False,
                    True,
                    True,
                )
                for AssemblyElement in vAssemblyElement:
                    vvAssemblyElementMap[iPart].append(AssemblyElement)
                    vvAssemblyElementMapRef[iPartRef].append(AssemblyElement)
                print("nAssemblyElement=" + str(len(vAssemblyElement)))
                if len(vqPP0) > 0:
                    viPartRef0.append(iPartRef)
                    vAnchoringStatisticsPartToPart0.append(
                        AnchoringStatisticsPartToPart0
                    )
                if bPrint:
                    print(AnchoringStatisticsPartToPart.sShapka())
                    print("All:")
                    # print str(vqPP)
                    print(AnchoringStatisticsPartToPart.s())
                    print("0 only:")
                    # print str(vqPP)
                    print(AnchoringStatisticsPartToPart0.s())
        else:  # contigs with markers from different chromosomes are cut into parts from the same chromosomes
            # def excludeOverlapsOnSecCtg(self,vAssemblyElement):#lenOk,lenLayerMore0=
            nAssemblyElementMap = 0

            bChimera = False
            iPartRef = -1
            vqPP0 = []
            vAssemblyElement = []
            aStart_set = 0
            iUnmapped = 1  # number of parts of the PartOfMap that are unmaped
            # initially: entire PartOfMap is unmapped
            # if it will be mapped properly => will be irrelevant
            # if PartOfMap is chimera than part between markers from different chromosomes will be unmapped

            iPos = -1  # not defined
            for q in vq:
                if (iTypeMaxRef < 0) or (q.PosOnMap2.iType <= iTypeMaxRef):
                    if (
                        q.PosOnMap2.iPart != iPartRef
                    ):  # marker with new PosOnMap2.iPart (including the first one)
                        if (
                            len(vqPP0) > 0
                        ):  # already were markers with different PosOnMap2.iPart
                            # chimera:
                            # first part -> one or several AssemblyElement-s in the same chromosome (several if the care on the ordering)
                            # second part -> unmapped AssemblyElement
                            # third part is processed later
                            #
                            bChimera = True
                            #
                            # first part
                            AnchoringStatisticsPartToPart0 = (
                                self.clAnchoringStatisticsPartToPart(vqPP0)
                            )
                            AnchoringStatisticsPartToPart0.appdate_vAssemblyElement(
                                vqPP0,
                                aStart_set,
                                aEnd_set,
                                AssemblyMy,
                                vAssemblyElement,
                                False,
                                True,
                                False,
                            )
                            for AssemblyElement in vAssemblyElement:
                                vvAssemblyElementMap[iPart].append(AssemblyElement)
                                vvAssemblyElementMapRef[iPartRef].append(
                                    AssemblyElement
                                )
                                nAssemblyElementMap += 1
                            viPartRef0.append(iPartRef)
                            vAnchoringStatisticsPartToPart0.append(
                                AnchoringStatisticsPartToPart0
                            )
                            #
                            # second part
                            vvAssemblyElementMap[iPart].append(
                                AssemblyMy.clAssemblyElement(
                                    -iUnmapped,
                                    iPart,
                                    iPos,
                                    -1,
                                    -1,
                                    aEnd_set,
                                    q.PosOnMap1.coor,
                                    0,
                                    [],
                                    [],
                                    [],
                                    False,
                                    False,
                                )
                            )
                            nAssemblyElementMap += 1
                            iUnmapped += 1
                            #
                            # for third part
                            aStart_set = q.PosOnMap1.coor
                        vqPP0 = []
                        vAssemblyElement = []
                        iPartRef = q.PosOnMap2.iPart
                        aEnd_set = q.PosOnMap1.coor
                    vqPP0.append(q)
            if len(vqPP0) > 0:
                AnchoringStatisticsPartToPart0 = self.clAnchoringStatisticsPartToPart(
                    vqPP0
                )
                bFrom0 = not bChimera
                AnchoringStatisticsPartToPart0.appdate_vAssemblyElement(
                    vqPP0,
                    aStart_set,
                    partLength,
                    AssemblyMy,
                    vAssemblyElement,
                    False,
                    bFrom0,
                    True,
                )
                for AssemblyElement in vAssemblyElement:
                    vvAssemblyElementMap[iPart].append(AssemblyElement)
                    vvAssemblyElementMapRef[iPartRef].append(AssemblyElement)
                    nAssemblyElementMap += 1
                viPartRef0.append(iPartRef)
                vAnchoringStatisticsPartToPart0.append(AnchoringStatisticsPartToPart0)
                if not bChimera and len(vAssemblyElement) == 1:
                    if AssemblyElement.orientation == 0:
                        self.setPositionOrOrientationBasedOnMapMarkersToGoodGenome(
                            sMapGoodGenome, AssemblyElement, iMap, True
                        )
                        if AssemblyElement.orientation != 0:
                            print(PartOfMap.name + ": orientation")
            if nAssemblyElementMap == 0 and bTryToAddUnmapped:
                AssemblyElement = AssemblyMy.clAssemblyElement(
                    -iUnmapped,
                    iPart,
                    iPos,
                    -1,
                    -1,
                    0,
                    partLength,
                    0,
                    [],
                    [],
                    [],
                    True,
                    True,
                )
                vvAssemblyElementMap[iPart].append(AssemblyElement)
                nAssemblyElementMap += 1
                self.setPositionOrOrientationBasedOnMapMarkersToGoodGenome(
                    sMapGoodGenome, AssemblyElement, iMap, False
                )
                if AssemblyElement.iLG >= 0:
                    print(
                        "3227:"
                        + str(AssemblyElement.iLG)
                        + " -> 0.."
                        + str(len(vvAssemblyElementMapRef) - 1)
                    )
                    vvAssemblyElementMapRef[AssemblyElement.iLG].append(AssemblyElement)
                    print(PartOfMap.name + ": position")
                # print "iPart="+str(iPart)
        return viPartRef0, vAnchoringStatisticsPartToPart0, nAssemblyElementMap

    def anchorMapToMap(
        self,
        iMap,
        iMapReference,
        sMapGoodGenome="Formica",
        iTypeMax=0,
        iTypeMaxRef=0,
        sPath="",
    ):  # vvAssemblyElementMap,vvAssemblyElementMapRef=
        # self.anchorPartToPart(2,0,3)
        sFileName = (
            sPath
            + "anchorMapToMap_"
            + self.vsMapName[iMap]
            + "_"
            + self.vsMapName[iMapReference]
            + ".txt"
        )
        sFileName1 = (
            sPath
            + "anchorMapToMap_"
            + self.vsMapName[iMap]
            + "_"
            + self.vsMapName[iMapReference]
            + "_Map.txt"
        )
        sFileName2 = (
            sPath
            + "anchorMapToMap_"
            + self.vsMapName[iMap]
            + "_"
            + self.vsMapName[iMapReference]
            + "_MapRef.txt"
        )
        f = open(sFileName, "w")
        AnchoringStatisticsPartToPart = self.clAnchoringStatisticsPartToPart([])

        bPrint = False

        # shapka
        s = (
            "i"
            + "\t"
            + "sPart"
            + "\t"
            + "sPartLength"
            + "\t"
            + "n"
            + "\t"
            + "i"
            + "\t"
            + "chr"
            + "\t"
            + "chrLength"
            + AnchoringStatisticsPartToPart.sShapka()
        )
        if bPrint:
            print(s)
        f.write(s + "\n")

        vvAssemblyElementMap = []  # [iPartOfMap]
        vvAssemblyElementMapRef = []  # [iPartOfMapRef]
        for iPart in range(len(self.vMap[iMap].vPartOfMap)):
            vvAssemblyElementMap.append([])
        for iPart in range(len(self.vMap[iMapReference].vPartOfMap)):
            vvAssemblyElementMapRef.append([])

        for iPart in range(len(self.vMap[iMap].vPartOfMap)):
            (
                viPartRef0,
                vAnchoringStatisticsPartToPart0,
                nAssemblyElementMap,
            ) = self.anchorPartToPart(
                vvAssemblyElementMap,
                vvAssemblyElementMapRef,
                iMap,
                iPart,
                iMapReference,
                False,
                sMapGoodGenome,
                iTypeMax,
                0,
            )
            b = nAssemblyElementMap == 0  # sill unmapped
            if b:
                (
                    viPartRef0,
                    vAnchoringStatisticsPartToPart0,
                    nAssemblyElementMap,
                ) = self.anchorPartToPart(
                    vvAssemblyElementMap,
                    vvAssemblyElementMapRef,
                    iMap,
                    iPart,
                    iMapReference,
                    True,
                    sMapGoodGenome,
                    iTypeMax,
                    iTypeMaxRef,
                )

            # control only
            sPart = self.vMap[iMap].vPartOfMap[iPart].name
            length = self.vMap[iMap].vPartOfMap[iPart].length
            #
            s1 = (
                str(iPart)
                + "\t"
                + sPart
                + "\t"
                + str(length)
                + "\t"
                + str(len(viPartRef0))
            )
            if bPrint:
                print(s1)
            f.write(s1 + "\n")
            i = 1
            for iPartRef in viPartRef0:
                sPartNameRef = self.vMap[iMapReference].vPartOfMap[iPartRef].name
                length = self.vMap[iMapReference].vPartOfMap[iPartRef].length
                s = (
                    s1
                    + "\t"
                    + str(i)
                    + "\t"
                    + sPartNameRef
                    + "\t"
                    + str(length)
                    + vAnchoringStatisticsPartToPart0[i - 1].s()
                )
                if bPrint:
                    print(s)
                f.write(s + "\n")
                i += 1
        f.close()
        self.anchorMapToMap__control(
            vvAssemblyElementMap, sFileName1, iMap, iMapReference, False
        )
        self.anchorMapToMap__control(
            vvAssemblyElementMapRef, sFileName2, iMap, iMapReference, True
        )
        return vvAssemblyElementMap, vvAssemblyElementMapRef

    def anchorMapToMap__control(
        self, vvAssemblyElement, sFileName, iMap, iMapReference, bFirstMapReference
    ):
        f = open(sFileName, "w")
        iPart = -1

        # shapka
        AssemblyMy = clAssemblyMy()
        AssemblyElement = AssemblyMy.clAssemblyElement()
        s = ""
        if bFirstMapReference:
            s = (
                "iPartMapRef"
                + "\t"
                + "sPartMapRef"
                + "\t"
                + "lenMapRef"
                + "\t"
                + "iPartMap"
                + "\t"
                + "sPartMap"
            )
        else:
            s = (
                "iPartMap"
                + "\t"
                + "sPartMap"
                + "\t"
                + "lenMap"
                + "\t"
                + "iPartMapRef"
                + "\t"
                + "sPartMapRef"
            )
        s = s + "\t" + AssemblyElement.sShapka(bDetails=True)
        f.write(s + "\n")

        for vAssemblyElement in vvAssemblyElement:
            iPart += 1
            i = -1
            for AssemblyElement in vAssemblyElement:
                i += 1
                sPart = ""
                sPart1 = ""
                length = -1
                iPart1 = -1
                if bFirstMapReference:
                    sPart = self.vMap[iMapReference].vPartOfMap[iPart].name
                    length = self.vMap[iMapReference].vPartOfMap[iPart].length
                    iPart1 = AssemblyElement.iCtg
                    sPart1 = self.vMap[iMap].vPartOfMap[iPart1].name
                else:
                    sPart = self.vMap[iMap].vPartOfMap[iPart].name
                    length = self.vMap[iMap].vPartOfMap[iPart].length
                    iPart1 = AssemblyElement.iLG
                    if iPart1 >= 0:
                        sPart1 = self.vMap[iMapReference].vPartOfMap[iPart1].name
                    else:
                        sPart1 = "no"
                s = (
                    str(iPart)
                    + "\t"
                    + sPart
                    + "\t"
                    + str(length)
                    + "\t"
                    + str(i)
                    + "\t"
                    + sPart1
                )
                s = s + "\t" + AssemblyElement.s(bDetails=True)
                f.write(s + "\n")
        f.close()

    def anchor_sMap_To_sMap(
        self,
        sMap,
        sMapReference,
        sMapGoodGenome="Formica",
        iTypeMax=0,
        iTypeMaxRef=0,
        sPath="",
    ):
        iMap = self.iMap(sMap)
        iMapReference = self.iMap(sMapReference)
        return self.anchorMapToMap(
            iMap, iMapReference, sMapGoodGenome, iTypeMax, iTypeMaxRef, sPath=sPath
        )

    def build_AssemblyMy(self):
        # self.mapMarkersToFormica()

        # iVariant=0#asm, 3aMM
        # iVariant=1#3
        # iVariant=3#3.1
        iVariant = 3  # 3a.1
        bWithOrientationOnly = True
        sSeqAssemblyName = ""
        sAssemblyName = ""
        sMapGoodGenome = "Formica"
        sPath = "C:\\Frenkel\\LTCPython\\VovaPy\\"
        if iVariant == 0:  # old
            sSeqAssemblyName = "asm"
            bWithOrientationOnly = False
            # sPath="C:\\Frenkel\\LTCPython\\VovaPy\\20210322\\"
            sPath = "C:\\Frenkel\\LTCPython\\VovaPy\\20210611\\"
        if iVariant == 1:  # old
            sAssemblyName = "Cnig_gn3"
            sSeqAssemblyName = "Cnig_gn3.contigs"
            bWithOrientationOnly = True
            # sPath="C:\\Frenkel\\LTCPython\\VovaPy\\20210530\\"
            sPath = "C:\\Frenkel\\LTCPython\\VovaPy\\20210610\\"
        if iVariant == 2:  # old
            sAssemblyName = "Cnig_gn3a"
            sSeqAssemblyName = "Cnig_gn3a.contigs"  # "300-500.pilon"
            bWithOrientationOnly = False
            # sPath="C:\\Frenkel\\LTCPython\\VovaPy\\20210502\\"
            sPath = "C:\\Frenkel\\LTCPython\\VovaPy\\20210612\\"
        if iVariant == 3:
            sAssemblyName = "Cnig_gn3.1"
            sSeqAssemblyName = "Cnig_gn3.contigs"
            sPath += "20211004\\Cnig_gn3.1\\"
            sMapGoodGenome = "Cnig_gn3a.1"  # poka netu
            # sMapGoodGenome="Formica"#poka
            bWithOrientationOnly = True
        if iVariant == 4:
            sAssemblyName = "Cnig_gn3a.1"
            sSeqAssemblyName = "Cnig_gn3a.contigs"  # "300-500.pilon"
            sPath += "20211004\\Cnig_gn3a.1\\"
            sMapGoodGenome = "Formica"
            bWithOrientationOnly = False

        # sMapRef="Genetic" #my map with my version of chromosome name and orientation
        sMapRef = "mapGenetic"  # (mapGenetic is already take into account my genetic map, new chromosome name and orientation (approved by Eyal))
        iMap = self.iMap(sSeqAssemblyName)

        vChrLength_cM = []
        vChrName = []
        iMapRef = self.iMap(sMapRef)
        for PartOfMap in self.vMap[iMapRef].vPartOfMap:
            vChrLength_cM.append(PartOfMap.length)
            vChrName.append(PartOfMap.name)

        vvAssemblyElementMap, vvAssemblyElementMapRef = self.anchor_sMap_To_sMap(
            sSeqAssemblyName, sMapRef, sMapGoodGenome, iTypeMaxRef=1, sPath=sPath
        )

        PrivmanLab = clPrivmanLab()
        # self.vMap[0].SecCtgs=self.vMap[iMap].SecCtgs
        # SecCtgs=self.vMap[iMap].SecCtgs
        # for map in self.vMap:
        # 	map.SecCtgs=[]
        #
        # now we need sequence
        SecCtgs = PrivmanLab.SecCtgsByName(sSeqAssemblyName, False)
        AssemblyMy = clAssemblyMy(SecCtgs, sAssemblyName, sPath)
        #
        # sequence length of contigs
        for vAssemblyElementMap in vvAssemblyElementMap:
            for AssemblyElement in vAssemblyElementMap:
                iCtgOriginal = AssemblyElement.iCtg
                ctg = SecCtgs.vCtg[iCtgOriginal]
                seqLength = ctg.seqLength
                AssemblyElement.totalLengthOfCtg_set(seqLength, True)

        AssemblyMy.vLGwithSeq_make_new(
            vvAssemblyElementMap,
            vvAssemblyElementMapRef,
            vChrLength_cM,
            vChrName,
            bWithOrientationOnly,
        )

    def mapMarkersToFormica(self):
        # not in use

        # def addMarkerformicaGenet():

        iPart = 0
        for part in self.vMap[iMap].vPartOfMap:
            # coor_prev=0
            # if nGood>0:

            iPart += 1
        if False:
            vvAssemblyElementMap, vvAssemblyElementMapRef = self.anchor_sMap_To_sMap(
                sSeqAssemblyName, sMapRef
            )
            iPartMap = 0
            for vAssemblyElementMap in vvAssemblyElementMap:
                vidMarkerWithMultiplePos = self.vMap[iMap].vPartOfMap[iPart].vidMarker
                for AssemblyElementMap in vAssemblyElementMap:
                    vsMarkers = AssemblyElementMap.vsMarkers
                iPartMap += 1

    def setPositionOrOrientationBasedOnMapMarkersToGoodGenome(
        self, sMapGoodGenome, AssemblyElement, iMap, bOrientationOnly
    ):
        # sMapRef="Genetic" old version: my version of chromosome naming (LG1,..,LG27) and orientation
        sMapRef = "mapGenetic"
        # iMap #Cnig_gn3.contigs
        iMapRefF = self.iMap(sMapGoodGenome)  # Formica
        iMapRefG = self.iMap(sMapRef)  # mapGenetic

        def MyFunc1(q):
            return q[1]

        def MyFunc3(q):
            return q[3]

        def MyFunc5(q):
            return q[5]

        iPart = AssemblyElement.iCtg
        part = self.vMap[iMap].vPartOfMap[iPart]
        vidMarker = part.vidMarker

        # all markers on ctg
        viPartF = []
        vvCoorF = []
        viPartG = []
        vvCoorG = []
        vq = []
        for im in vidMarker:
            PosOnMap = self.vMarkerWithMultiplePos[im].vvPosOnMap[iMap][0]
            if PosOnMap.iPart == iPart and PosOnMap.iType == 0:
                coor = PosOnMap.coor
                iPartF = -1
                coorF = -1
                iPartG = -1
                coorG = -1
                if len(self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefF]) > 0:
                    PosOnMapF = self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefF][0]
                    if PosOnMapF.iType == 0:
                        iPartF = PosOnMapF.iPart
                        coorF = PosOnMapF.coor
                        if not (iPartF in viPartF):
                            viPartF.append(iPartF)
                            vvCoorF.append([])
                        if not (coorF in vvCoorF[viPartF.index(iPartF)]):
                            vvCoorF[viPartF.index(iPartF)].append(coorF)
                if len(self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG]) > 0:
                    PosOnMapG = self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG][0]
                    if PosOnMapG.iType == 0:
                        iPartG = PosOnMapG.iPart
                        coorG = PosOnMapG.coor
                        if not (iPartG in viPartG):
                            viPartG.append(iPartG)
                            vvCoorG.append([])
                        if not (coorG in vvCoorG[viPartG.index(iPartG)]):
                            vvCoorG[viPartG.index(iPartG)].append(coorG)
                bCoorGReal = iPartG >= 0
                vq.append([im, coor, iPartF, coorF, iPartG, coorG, bCoorGReal])

        bWeCanTry = True
        if len(vq) < 1:
            bWeCanTry = False
        if bOrientationOnly and len(vq) < 2:
            bWeCanTry = False
        if len(viPartF) != 1:  # else we can't
            bWeCanTry = False
        if len(viPartG) > 1:  # else we can't
            bWeCanTry = False
        if bOrientationOnly and len(viPartG) == 0:  # else we can't
            bWeCanTry = False
        if bWeCanTry:
            vq.sort(key=MyFunc1)
            coorFmin = min(vvCoorF[0])
            coorFmax = min(vvCoorF[0])
            iPartF = viPartF[0]

            partF = self.vMap[iMapRefF].vPartOfMap[iPartF]
            vqF = []
            vidMarkerF = partF.vidMarker
            for im in vidMarkerF:
                PosOnMapF = self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefF][0]
                if PosOnMapF.iPart == iPartF and PosOnMapF.iType == 0:
                    if len(self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG]) > 0:
                        PosOnMapG = self.vMarkerWithMultiplePos[im].vvPosOnMap[
                            iMapRefG
                        ][0]
                        if PosOnMapG.iType == 0:
                            iPartG = PosOnMapG.iPart
                            coorG = PosOnMapG.coor
                            iPartF = PosOnMapF.iPart
                            coorF = PosOnMapF.coor
                            vqF.append([im, -1, iPartF, coorF, iPartG, coorG, True])
            vqPP = []
            vim = []
            for q in vq:
                vqPP.append(q)
                vim.append(q[0])
            for q in vqF:
                if not (q[0] in vim):
                    vqPP.append(q)
            vqPP.sort(key=MyFunc3)
            qLeft = [-1]
            qRight = [-1]
            iq = 0
            for q in vqPP:
                if q[6] and (not (bOrientationOnly) or q[4] == viPartG[0]):
                    qLeft = q
                else:
                    qRight = [-1]
                    iq1 = iq + 1
                    while iq1 < len(vqPP) and qRight[0] == -1:
                        q1 = vqPP[iq1]
                        if q1[6] and (not (bOrientationOnly) or q1[4] == viPartG[0]):
                            qRight = q1
                        iq1 += 1

                    if qLeft[0] < 0 and qRight[0] >= 0:
                        if qRight[3] - q[3] < 100000:
                            q[4] = qRight[4]
                            q[5] = qRight[5]
                            if not (q[4] in viPartG):
                                viPartG.append(q[4])
                                vvCoorG.append([])
                    if qLeft[0] >= 0 and qRight[0] < 0:
                        if q[3] - qLeft[3] < 100000:
                            q[4] = qLeft[4]
                            q[5] = qLeft[5]
                            if not (q[4] in viPartG):
                                viPartG.append(q[4])
                                vvCoorG.append([])
                    if qLeft[0] >= 0 and qRight[0] >= 0:
                        if not (qLeft[4] in viPartG):
                            viPartG.append(qLeft[4])
                            vvCoorG.append([])
                        if not (qRight[4] in viPartG):
                            viPartG.append(qRight[4])
                            vvCoorG.append([])
                        if qLeft[4] == qRight[4]:
                            q[4] = qLeft[4]
                            q[5] = qLeft[5]
                            if qLeft[3] < qRight[3]:
                                q[5] = qLeft[5] + (
                                    float((q[3] - qLeft[3])) / (qRight[3] - qLeft[3])
                                )
                iq += 1
            if len(viPartG) != 1:
                bWeCanTry = False
            if bWeCanTry:
                print("viPartG=" + str(viPartG))
                print("vvCoorG=" + str(vvCoorG))
                print("viPartF=" + str(viPartF))
                print("vvCoorF=" + str(vvCoorF))
                vqPPPP = []
                for q in vqPP:
                    if q[1] >= 0 and q[4] >= 0:
                        vqPPPP.append(q)
                        if not q[5] in vvCoorG[0]:
                            vvCoorG[0].append(q[5])
                if bOrientationOnly and len(vvCoorG[0]) < 2:
                    bWeCanTry = False
                n = len(vqPPPP)
                if n < 1:
                    bWeCanTry = False
                if bWeCanTry:
                    vqPPPP.sort(key=MyFunc5)
                    AssemblyElement.iLG = viPartG[0]
                    if not bOrientationOnly:
                        AssemblyElement.coorOnLG_min = vqPPPP[0][5]
                        AssemblyElement.coorOnLG_max = vqPPPP[n - 1][5]
                    AssemblyElement.orientation = 0
                    if vqPPPP[0][1] < vqPPPP[n - 1][1]:
                        AssemblyElement.orientation = 1
                    if vqPPPP[0][1] > vqPPPP[n - 1][1]:
                        AssemblyElement.orientation = -1
        """
		iPartRef_prev=-1
		coor_prev=0
		nGood=0
		if len(vq)>1:
			iq=0
			iq0=-1
			viqGood=[]
			for q in vq:
				im=q[0]
				vPosOnMap2=self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG]
				if len(vPosOnMap2)>0:
					PosOnMap2=vPosOnMap2[0]
					if PosOnMap2.iType==0:
						iPartRef=PosOnMap2.iPart
						coorRef=PosOnMap2.coor
						q[2]=iPartRef
						q[3]=coorRef
						q[4]=True
						nGood+=1
						viqGood.append(iq)
						if iPartRef_prev<0:
							iPartRef_prev=iPartRef
							iq0=iq
						else:
							#no need
							iqPrev=viqGood[nGood-1]
							qPrev=vq[iqPrev]
							qPrev[5]=iPartRef
							qPrev[6]=coorRef
				iq+=1
			if len(viqGood)>0:
				for iq in range(iq0):
					if vq[iq0][1]-vq[iq][1]<1000:
						vq[iq][2]=vq[iq0][2]#iPartRef
						vq[iq][3]=vq[iq0][3]#coorRef
						im=vq[iq][0]
						PosOnMap2=self.vMarkerWithMultiplePos[im].clPosOnMap(vq[iq0][2],vq[iq0][3],0)
						self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG].append(PosOnMap2)
						self.vMap[iMapRefG].vPartOfMap[vq[iq0][2]].vidMarker.append(im)
				for iGood in range(nGood):
					iq0=viqGood[iGood]
					if iGood<nGood-1:
						iq1=viqGood[iGood+1]
						if vq[iq0][2]==vq[iq1][2]:
							if vq[iq1][1]-vq[iq0][1]<50000 and vq[iq1][1]-vq[iq0][1]>0 and abs(vq[iq1][3]-vq[iq0][3])<5:
								for iq in range(iq0+1,iq1):
									vq[iq][2]=vq[iq0][2]#iPartRef
									vq[iq][3]=vq[iq0][3]+(vq[iq1][3]-vq[iq0][3])*(float(vq[iq][1]-vq[iq0][1])/(vq[iq1][1]-vq[iq0][1]))
									im=vq[iq][0]
									PosOnMap2=self.vMarkerWithMultiplePos[im].clPosOnMap(vq[iq0][2],vq[iq0][3],0)
									self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG].append(PosOnMap2)
									self.vMap[iMapRefG].vPartOfMap[vq[iq0][2]].vidMarker.append(im)
							else:
								for iq in range(iq0+1,iq1):
									bOk=False
									if vq[iq][1]-vq[iq0][1]<1000:
										bOk=True
										vq[iq][3]=vq[iq0][3]
									if vq[iq1][1]-vq[iq][1]<1000:
										bOk=True
										vq[iq][3]=vq[iq1][3]
									if bOk:
										vq[iq][2]=vq[iq0][2]#iPartRef
										im=vq[iq][0]
										PosOnMap2=self.vMarkerWithMultiplePos[im].clPosOnMap(vq[iq0][2],vq[iq0][3],0)
										self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG].append(PosOnMap2)
										self.vMap[iMapRefG].vPartOfMap[vq[iq0][2]].vidMarker.append(im)
					else:
						for iq in range(viqGood[nGood-1]+1,len(vq)):
							if vq[iq][1]-vq[iq0][1]<1000:
								vq[iq][2]=vq[iq0][2]#iPartRef
								vq[iq][3]=vq[iq0][3]#coorRef
								im=vq[iq][0]
								PosOnMap2=self.vMarkerWithMultiplePos[im].clPosOnMap(vq[iq0][2],vq[iq0][3],0)
								self.vMarkerWithMultiplePos[im].vvPosOnMap[iMapRefG].append(PosOnMap2)
								self.vMap[iMapRefG].vPartOfMap[vq[iq0][2]].vidMarker.append(im)
		"""
        pass

    def print_bim_file_forPnina(self):
        # https://www.cog-genomics.org/plink/2.0/formats
        # format:
        # iChr	sMarker	coorGenetic	coorPhys	sAltAllele	sRefAllele
        #
        # example:
        # 1	N289P44703	34.76966308	1039192	1	0
        # 1	N289P53592	34.76966308	1048081	1	0
        vMarkerBim = []
        sMapGenetic = "mapGenetic"
        sMapPhys = "Cnig_gn3.1"
        iMapGenetic = self.iMap(sMapGenetic)
        iMapPhys = self.iMap(sMapPhys)
        for MarkerWithMultiplePos in self.vMarkerWithMultiplePos:

            # sMarker
            sMarker = ""
            # MarkerWithMultiplePos.sName=NODE_4707_length_15209_cov_2.30379___4984
            bOk = False
            ss = MarkerWithMultiplePos.sName.split("_")  # ss[1]="4707", ss[8]=4908
            if len(ss) > 8:
                if ss[0] == "NODE" and ss[2] == "length":
                    sMarker = "N" + ss[1] + "P" + ss[8]
                    bOk = True

            if bOk:
                bOk = False
                if MarkerWithMultiplePos.nPosMax == 1:
                    if (
                        len(MarkerWithMultiplePos.vvPosOnMap[iMapGenetic]) == 1
                        and len(MarkerWithMultiplePos.vvPosOnMap[iMapPhys]) == 1
                    ):
                        PosOnMapGenetic = MarkerWithMultiplePos.vvPosOnMap[iMapGenetic][
                            0
                        ]
                        PosOnMapPhys = MarkerWithMultiplePos.vvPosOnMap[iMapPhys][0]
                        sChr = self.vMap[iMapPhys].vsPartName[
                            PosOnMapPhys.iPart
                        ]  # .name#chr01
                        if len(sChr) == 5:
                            iChr = (
                                int(sChr[4]) if sChr[3] == "0" else int(sChr[3 : 4 + 1])
                            )
                            coorGenetic = PosOnMapGenetic.coor
                            coorPhys = int(PosOnMapPhys.coor)
                            iTypeGenetic = PosOnMapGenetic.iType
                            MarkerBim = [
                                iChr,
                                sMarker,
                                coorGenetic,
                                coorPhys,
                                iTypeGenetic,
                            ]
                            vMarkerBim.append(MarkerBim)

        # sort by chr, by physical position
        def MyFunc1(MarkerBim):
            return MarkerBim[0] * 1000000000 + MarkerBim[3]

        vMarkerBim.sort(key=MyFunc1)

        # vvChr_MarkerBim
        vvChr_MarkerBim = []
        vChr_MarkerBim = []
        iChrPrev = -1
        iChr = 0
        for MarkerBim in vMarkerBim:
            if iChrPrev != MarkerBim[0]:
                if len(vChr_MarkerBim) > 0:
                    vvChr_MarkerBim.append(vChr_MarkerBim)
                vChr_MarkerBim = []
            vChr_MarkerBim.append(MarkerBim)
            iChrPrev = MarkerBim[0]
        vvChr_MarkerBim.append(vChr_MarkerBim)

        # control
        iChr = 0
        vn = []
        for vChr_MarkerBim in vvChr_MarkerBim:
            iChr += 1
            print(
                str(iChr)
                + "\t"
                + "chr"
                + str(vChr_MarkerBim[0][0])
                + "\t"
                + str(len(vChr_MarkerBim))
            )
            vn.append(len(vChr_MarkerBim))

        # filters
        def vMarkerBim_byIndex(vMarkerBim, index):
            vMarkerBim_sel = []
            for MarkerBim in vMarkerBim:
                if MarkerBim[4] == index:
                    vMarkerBim_sel.append(MarkerBim)
            return vMarkerBim_sel

        def vnErr_get(vMarkerBim, index0, index1, bPrint, bPrintDetails):
            vnErr = []
            nErrMax = 0
            inErrMax = 0

            vsMarkers = []
            vx0 = []
            vvx = []

            n = len(vMarkerBim)
            for i in range(n):
                nErr = 0
                vx = []
                x0 = vMarkerBim[i][2]
                if vMarkerBim[i][4] == index0:
                    for j in range(n):
                        if vMarkerBim[j][4] == index1:
                            x = vMarkerBim[j][2]
                            if (j < i and x > x0) or (j > i and x < x0):
                                nErr += 1
                                if not (x in vx):
                                    vx.append(x)

                nErr = len(vx)
                vnErr.append(nErr)
                if nErr > nErrMax:
                    inErrMax = i
                    nErrMax = nErr
                    vsMarkers = []
                    vx0 = []
                    vvx = []
                if nErr == nErrMax:
                    vsMarkers.append(vMarkerBim[i][1])
                    vx0.append(x0)
                    vvx.append(vx)
            if bPrint:
                s0 = "_" + str(index0) + str(index1) if bPrintDetails else ""
                print("nErrMax" + s0 + "=" + str(nErrMax))
                if nErrMax > 0:
                    nn = len(vx0)
                    for i in range(nn):
                        print(
                            str(i)
                            + "\t"
                            + vsMarkers[i]
                            + "\t"
                            + str(vx0[i])
                            + "\t"
                            + str(vvx[i])
                        )
            return vnErr, nErrMax, inErrMax  # ,vsMarkers,vx0,vvx

        def vMarkerBim_excludeBy_vnErr(vMarkerBim, vnErr, nErrMax):
            vMarkerBimPP = []
            n = len(vMarkerBim)
            for i in range(n):
                if vnErr[i] < nErrMax:
                    vMarkerBimPP.append(vMarkerBim[i])
            return vMarkerBimPP

        def filtering(vChr_MarkerBim, index0, index1):  # vChr_MarkerBim=
            vnErr, nErrMax, inErrMax = vnErr_get(
                vChr_MarkerBim, index0, index1, True, True
            )
            while nErrMax > 0:
                vChr_MarkerBim = vMarkerBim_excludeBy_vnErr(
                    vChr_MarkerBim, vnErr, nErrMax
                )
                vnErr, nErrMax, inErrMax = vnErr_get(
                    vChr_MarkerBim, index0, index1, True, False
                )
            return vChr_MarkerBim

        iChr = 0
        for vChr_MarkerBim in vvChr_MarkerBim:
            print("chr=" + str(iChr))

            # vMarkerBim_0=vMarkerBim_byIndex(vChr_MarkerBim,0)

            # filter_1 0's only
            vChr_MarkerBim = filtering(vChr_MarkerBim, 0, 0)

            # filter_2 1 vs. 0
            vChr_MarkerBim = filtering(vChr_MarkerBim, 1, 0)

            # filter_3 1 vs. 1
            vChr_MarkerBim = filtering(vChr_MarkerBim, 1, 1)

            vvChr_MarkerBim[iChr] = vChr_MarkerBim
            iChr += 1

        # control
        iChr = 0
        for vChr_MarkerBim in vvChr_MarkerBim:
            iChr += 1
            print(
                str(iChr)
                + "\t"
                + "chr"
                + str(vChr_MarkerBim[0][0])
                + "\t"
                + str(len(vChr_MarkerBim))
                + "\t"
                + str(vn[iChr - 1])
                + "\t"
                + str(len(vChr_MarkerBim) - vn[iChr - 1])
            )

        # vMarkerBim
        vMarkerBim = []
        for vChr_MarkerBim in vvChr_MarkerBim:
            for MarkerBim in vChr_MarkerBim:
                vMarkerBim.append(MarkerBim)

        # print to file
        nNotGood = 0
        sFileName = "ants_20211018.bim"
        f = open(sFileName, "w")
        coorPrev = -1
        iChrPrev = -1
        for MarkerBim in vMarkerBim:
            if MarkerBim[0] != iChrPrev:
                coorPrev = -1
            sNotGood = ""
            if MarkerBim[2] < coorPrev:
                nNotGood += 1
                sNotGood = str(MarkerBim[2]) + "<" + str(coorPrev)
            s = (
                str(MarkerBim[0])
                + "\t"
                + MarkerBim[1]
                + "\t"
                + str(MarkerBim[2])
                + "\t"
                + str(MarkerBim[3])
                + "\t"
                + "1"
                + "\t"
                + "0"
            )
            # s+='\t'+str(MarkerBim[4])+'\t'+sNotGood
            f.write(s + "\n")

            iChrPrev = MarkerBim[0]
            coorPrev = MarkerBim[2]
        print("nNotGood=" + str(nNotGood))
        f.close()

    # def print_data_to_drew_map_comparison(self):
    def vIdMarkerUniqueOnBothMaps_get(self, iMap1, iMap2):  # vIdMarkerUniqueOnBothMaps=
        vIdMarkerUniqueOnBothMaps = []
        for MarkerWithMultiplePos in self.vMarkerWithMultiplePos:
            if (
                len(MarkerWithMultiplePos.vvPosOnMap[iMap1]) == 1
                and len(MarkerWithMultiplePos.vvPosOnMap[iMap2]) == 1
            ):
                vIdMarkerUniqueOnBothMaps.append(MarkerWithMultiplePos.id)
        return vIdMarkerUniqueOnBothMaps

    def vMarkerById__get(self, vMarkerId):  # vMarker=
        vMarker = []
        for MarkerId in vMarkerId:
            vMarker.append(self.vMarkerWithMultiplePos[MarkerId])
        return vMarker

    def vMarkerId_get(self, vMarker):  # vMarkerId=
        vMarkerId = []
        for Marker in vMarker:
            vMarkerId.append(Marker.id)
        return vMarkerId

    def searchForProvenDifferencesBetweenTheMaps(self, viMap, vbMapProven, sPath):

        vvvDifferences = []
        i0 = 0
        for iMap0 in viMap:
            bMapProven0 = vbMapProven[i0]
            sMap0 = self.vMap[iMap0].sMapName
            print("searchForProvenDifferencesBetweenTheMaps: " + sMap0)

            for Marker in self.vMarkerWithMultiplePos:
                Marker.temp_iStatus = []
                Marker.temp_iPart = []
                Marker.temp_coor = []
                Marker.temp_s = []
                for map in self.vMap:
                    Marker.temp_iStatus.append(None)
                    Marker.temp_iPart.append(None)
                    Marker.temp_coor.append(None)
                    Marker.temp_s.append("none" + "\t" + "none")
                Marker.temp_iStatus[iMap0] = 0
                # Marker.temp_s[iMap0]="none"+"\t"+"none"

            i1 = 0
            for iMap1 in viMap:
                bMapProven1 = vbMapProven[i1]

                if iMap1 != iMap0:
                    sMap1 = self.vMap[iMap1].sMapName
                    print(
                        "searchForProvenDifferencesBetweenTheMaps: "
                        + sMap0
                        + " and "
                        + sMap1
                    )

                    vIdMarkerUniqueOnBothMaps = self.vIdMarkerUniqueOnBothMaps_get(
                        iMap0, iMap1
                    )
                    vMarkerUniqueOnBothMaps = self.vMarkerById__get(
                        vIdMarkerUniqueOnBothMaps
                    )
                    Ranking0 = self.vMap[iMap0].Ranking_get(
                        vMarkerUniqueOnBothMaps, self
                    )
                    Ranking1 = self.vMap[iMap1].Ranking_get(
                        vMarkerUniqueOnBothMaps, self
                    )
                    # self.vvMarkerOnPart=[]#[iPart,iMarkerOnPart]
                    # self.vvCoorOnPart=[]#[iPart,iMarkerOnPart]
                    # self.vvRankOnPart=[]#[iPart,iMarkerOnPart]
                    # self.vRankingPos

                    iPart0 = -1
                    for part0 in self.vMap[iMap0].vPartOfMap:
                        iPart0 += 1
                        vMarkerOnPart0 = Ranking0.vvMarkerOnPart[iPart0]
                        nm = len(vMarkerOnPart0)
                        rankMax0 = Ranking0.rankMax_get(iPart0)

                        iPart1_prev = -1
                        m1_prev = -1
                        nm1_prev = -1
                        rank1_prev = -1
                        rankMax1_prev = -1
                        m = -1
                        for Marker in vMarkerOnPart0:

                            m += 1
                            RankingPos1 = Ranking1.vRankingPos[
                                Marker.id
                            ]  # Ranking.vRankingPos[Marker.id]=[iPart,m]
                            iPart1 = RankingPos1[0]
                            m1 = RankingPos1[1]
                            nm1 = len(Ranking1.vvMarkerOnPart[iPart1])
                            rankMax1 = Ranking1.rankMax_get(iPart1)

                            rank0 = Ranking0.vvRankOnPart[iPart0][m]
                            rank1 = Ranking1.vvRankOnPart[iPart1][m1]

                            Marker.temp_iPart[iMap0] = iPart0
                            Marker.temp_coor[iMap0] = Ranking0.vvCoorOnPart[iPart0][m]
                            Marker.temp_iPart[iMap1] = iPart1
                            Marker.temp_coor[iMap1] = Ranking1.vvCoorOnPart[iPart1][m1]

                            if m == 0:
                                Marker.temp_iStatus[iMap1] = 0  # Part0 start
                            else:
                                if iPart1 == iPart1_prev:
                                    if (
                                        abs(rank1 - rank1_prev) <= 1
                                    ):  # "=" => in the same position
                                        Marker.temp_iStatus[
                                            iMap1
                                        ] = 1  # proven interval
                                    else:
                                        Marker.temp_iStatus[
                                            iMap1
                                        ] = -1  # local difference
                                        Marker.temp_iStatus[iMap0] += 1
                                else:
                                    # b=((m1==0) or (m1==nm1-1))
                                    # b1=((m1_prev==0) or (m1_prev==nm1_prev-1))
                                    b = (rank1 == 1) or (rank1 == rankMax1)
                                    b1 = (rank1_prev == 1) or (
                                        rank1_prev == rankMax1_prev
                                    )
                                    if b:
                                        if b1:
                                            Marker.temp_iStatus[iMap1] = 0  # break
                                        else:
                                            Marker.temp_iStatus[iMap1] = -2
                                            Marker.temp_iStatus[iMap0] += 1
                                    else:
                                        if b1:
                                            Marker.temp_iStatus[iMap1] = -3
                                            Marker.temp_iStatus[iMap0] += 1
                                        else:
                                            Marker.temp_iStatus[iMap1] = -4
                                            Marker.temp_iStatus[iMap0] += 1
                            s0 = (
                                "p"
                                + str(iPart0)
                                + "m"
                                + str(m)
                                + "nm"
                                + str(nm)
                                + "r"
                                + str(rank0)
                                + "rm"
                                + str(rankMax0)
                            )
                            s1 = (
                                "p"
                                + str(iPart1)
                                + "m"
                                + str(m1)
                                + "nm"
                                + str(nm1)
                                + "r"
                                + str(rank1)
                                + "rm"
                                + str(rankMax1)
                            )
                            Marker.temp_s[iMap1] = s0 + "\t" + s1

                            iPart1_prev = iPart1
                            m1_prev = m1
                            nm1_prev = nm1
                            rank1_prev = rank1
                            rankMax1_prev = rankMax1
                    i1 += 1
            print("searchForProvenDifferencesBetweenTheMaps: printing...")

            sFileName = (
                sPath + "searchForProvenDifferencesBetweenTheMaps_" + sMap0 + ".txt"
            )
            file = open(sFileName, "w")
            sFileName = (
                sPath + "searchForProvenDifferencesBetweenTheMapsPP_" + sMap0 + ".txt"
            )
            filePP = open(sFileName, "w")

            def iMap_get(i, i0, viMap):  # iMap=
                iMap = viMap[i]
                if i <= i0:
                    if i == 0:
                        iMap = viMap[i0]
                    else:
                        iMap = viMap[i - 1]
                return iMap

            def MyFunc0(Marker):
                return Marker.temp_coor[iMap0]

            s = "marker"
            for i in range(len(viMap)):
                iMap = iMap_get(i, i0, viMap)
                sMap = self.vMap[iMap].sMapName
                s += (
                    "\t"
                    + sMap
                    + "_part"
                    + "\t"
                    + sMap
                    + "_coor"
                    + "\t"
                    + sMap
                    + "_iStatus"
                    + "\tM0\tM1"
                )
            file.write(s + "\n")
            filePP.write(s + "\n")

            vvMarker = []
            iPart0 = -1
            for part0 in self.vMap[iMap0].vPartOfMap:
                iPart0 += 1
                vvMarker.append([])
            for Marker in self.vMarkerWithMultiplePos:
                if not (Marker.temp_iPart[iMap0] is None):
                    iPart0 = Marker.temp_iPart[iMap0]
                    vvMarker[iPart0].append(Marker)
            iPart0 = -1
            for part0 in self.vMap[iMap0].vPartOfMap:
                iPart0 += 1
                vMarker = vvMarker[iPart0]
                if len(vMarker) > 1:
                    vMarker.sort(key=MyFunc0)
                for Marker in vMarker:
                    s = Marker.sName
                    for i in range(len(viMap)):
                        iMap = iMap_get(i, i0, viMap)
                        sMap = self.vMap[iMap].sMapName

                        if Marker.temp_iPart[iMap] is None:
                            sPart = ""
                        else:
                            iPart = Marker.temp_iPart[iMap]
                            sPart = self.vMap[iMap].vPartOfMap[iPart].name
                        sCoor = (
                            ""
                            if Marker.temp_coor[iMap] is None
                            else str(Marker.temp_coor[iMap])
                        )
                        sStatus = (
                            ""
                            if Marker.temp_iStatus[iMap] is None
                            else str(Marker.temp_iStatus[iMap])
                        )
                        s += "\t" + sPart + "\t" + sCoor + "\t" + sStatus
                        s += "\t" + Marker.temp_s[iMap]
                    file.write(s + "\n")
                    if not (Marker.temp_iStatus[iMap0] is None):
                        if Marker.temp_iStatus[iMap0] > 0:
                            filePP.write(s + "\n")
            file.close()
            filePP.close()
            i0 += 1
        print("searchForProvenDifferencesBetweenTheMaps: Done")


class clGenomeMapComparisonGraph:
    def __init__(self):
        self.vMap = []
        self.type = 0  # 0 - Oxford plot, 1- parallel, 2-radial
        self.xmin = 0
        self.xmax = 100
        self.ymin = 0
        self.ymax = 100
        self.vmarker = []
        self.vmarkerName = []

    class clMap:
        def __init__(self):
            self.caption = ""
            self.name = ""
            self.id = -1
            self.vPart = []
            self.TotalMapLength = 0
            self.vsPartName = []
            self.nParts = 0

            self.ToPrint_v_iPart_orientation = []
            self.ToPrint_TotalMapLength = 0
            self.ToPrint_vsPartName = []
            self.ToPrint_nParts = 0
            self.ToPrint_bGrid = True
            self.ToPrint_GridLenMin = 0
            self.ToPrint_sColor = "black"
            self.ToPrint_bUse_sColor_forAllMarkers = False

            self.d0 = 0.05
            self.type = -1
            #
            self.x0 = -1
            self.y0 = -1
            self.x1 = -1
            self.y1 = -1
            #
            self.r = -1
            self.alpha0 = -1  # grad
            self.alpha1 = -1  # grad

        def type_set(self, type):
            self.type = type
            for MapPart in self.vPart:
                MapPart.type = type

        class clMapPart:
            def __init__(self, sCaption, sName, length, type, orientation):
                self.caption = sCaption
                self.name = sName
                self.length = length
                self.coor0 = 0
                self.orientation = orientation  # temory (1 or -1)

                self.type = type
                #
                self.x0 = -1
                self.y0 = -1
                self.x1 = -1
                self.y1 = -1
                #
                self.r = -1
                self.alpha0 = -1  # grad
                self.alpha1 = -1  # grad
                #
                self.col = "blue"
                self.w = 3

            def xy_get(self, coorOnPart, orientation):  # x,y,alpha=
                VovaMath = clVovaMath()
                alpha = -1
                if self.type == 0 or self.type == 1:
                    if orientation == 1:
                        x = VovaMath.yByLin(
                            0, self.x0, self.length, self.x1, coorOnPart
                        )
                        y = VovaMath.yByLin(
                            0, self.y0, self.length, self.y1, coorOnPart
                        )
                        return x, y, alpha
                    if orientation == -1:
                        x = VovaMath.yByLin(
                            0, self.x1, self.length, self.x0, coorOnPart
                        )
                        y = VovaMath.yByLin(
                            0, self.y1, self.length, self.y0, coorOnPart
                        )
                        return x, y, alpha
                if self.type == 2:
                    alpha = (
                        VovaMath.yByLin(
                            0, self.alpha0, self.length, self.alpha1, coorOnPart
                        )
                        if orientation == 1
                        else VovaMath.yByLin(
                            0, self.alpha1, self.length, self.alpha0, coorOnPart
                        )
                    )
                    x = self.x0 + self.r * math.cos(alpha * float(2 * 3.1415 / 360))
                    y = self.y0 + self.r * math.sin(alpha * float(2 * 3.1415 / 360))
                    return x, y, alpha

        def addPart(self, sCaption, sName, length, orientation):
            MapPart = self.clMapPart(sCaption, sName, length, self.type, orientation)
            if self.nParts > 0:
                partPrev = self.vPart[self.nParts - 1]
                MapPart.coor0 = partPrev.coor0 + partPrev.length
            self.vPart.append(MapPart)
            self.vsPartName.append(sName)
            self.TotalMapLength += length
            self.nParts += 1

        def ipart_coor_get(
            self, coorGlobal
        ):  # ipart,coor= #for simulated data or for data already drawn
            if coorGlobal <= 0:
                return 0, coorGlobal
            if coorGlobal >= self.TotalMapLength:
                return (
                    self.nParts - 1,
                    self.TotalMapLength - self.vPart[self.nParts - 1].coor0,
                )
            ip = 0
            for part in self.vPart:
                if coorGlobal >= part.coor0 and coorGlobal <= part.coor0 + part.length:
                    return ip, coorGlobal - part.coor0
                ip += 1
            return (
                self.nParts - 1,
                self.TotalMapLength - self.vPart[self.nParts - 1].coor0,
            )

        def ToPrint_start(self, bAll_and_intialOrientation, v_iPart_orientation=[]):
            self.ToPrint_v_iPart_orientation = []
            self.ToPrint_TotalMapLength = 0
            self.ToPrint_vsPartName = []
            self.ToPrint_nParts = 0
            if bAll_and_intialOrientation:
                self.ToPrint_nParts = self.nParts
                for iPart in range(self.ToPrint_nParts):
                    part = self.vPart[iPart]
                    self.ToPrint_v_iPart_orientation.append([iPart, part.orientation])
                    self.ToPrint_TotalMapLength += part.length
                    self.ToPrint_vsPartName.append(part.name)
            else:
                for iPart_orientation in v_iPart_orientation:
                    iPart = iPart_orientation[0]
                    orientation = iPart_orientation[1]
                    self.ToPrint_v_iPart_orientation.append([iPart, orientation])
                    part = self.vPart[iPart]
                    self.ToPrint_nParts += 1
                    self.ToPrint_TotalMapLength += part.length
                    self.ToPrint_vsPartName.append(part.name)

        def ToPrint_calcCoorForSelectedParts(self, bPrintDetails):
            print("ToPrint_calcCoorForSelectedParts...")
            d0 = self.d0
            # d=float(d0)/self.nParts if self.nParts>0 else 0
            if self.type == 0 or 1:
                if self.type == 0:
                    d0 = 0  # no need gap
                cx = (1 - d0) * (float(self.x1 - self.x0) / self.ToPrint_TotalMapLength)
                cy = (1 - d0) * (float(self.y1 - self.y0) / self.ToPrint_TotalMapLength)
                dx = (
                    d0 * (float(self.x1 - self.x0) / (self.ToPrint_nParts - 1))
                    if self.ToPrint_nParts > 1
                    else 0
                )
                dy = (
                    d0 * (float(self.y1 - self.y0) / (self.ToPrint_nParts - 1))
                    if self.ToPrint_nParts > 1
                    else 0
                )
                x0 = self.x0
                y0 = self.y0
                if bPrintDetails:
                    print(
                        "self.ToPrint_TotalMapLength="
                        + str(self.ToPrint_TotalMapLength)
                    )
                for iPart_orientation in self.ToPrint_v_iPart_orientation:
                    iPart = iPart_orientation[0]
                    orientation = iPart_orientation[1]
                    MapPart = self.vPart[iPart]
                    MapPart.orientation = orientation

                    x1 = x0 + cx * MapPart.length
                    y1 = y0 + cy * MapPart.length
                    MapPart.x0 = x0
                    MapPart.y0 = y0
                    MapPart.x1 = x1
                    MapPart.y1 = y1
                    if bPrintDetails:
                        print(
                            MapPart.name
                            + "\t"
                            + str(MapPart.length)
                            + "\t"
                            + str(cx * MapPart.length)
                            + "\t"
                            + str(cy * MapPart.length)
                            + "\t"
                            + str(x0)
                            + "\t"
                            + str(x1)
                            + "\t"
                            + str(y0)
                            + "\t"
                            + str(y1)
                        )
                    x0 = x1 + dx
                    y0 = y1 + dy
            if self.type == 2:
                calpha = (1 - d0) * (
                    float(self.alpha1 - self.alpha0) / self.ToPrint_TotalMapLength
                )
                dalpha = (
                    d0 * (float(self.alpha1 - self.alpha0) / (self.ToPrint_nParts))
                    if self.ToPrint_nParts > 0
                    else 0
                )
                x0 = self.x0
                y0 = self.y0
                r = self.r
                alpha0 = self.alpha0
                for iPart_orientation in self.ToPrint_v_iPart_orientation:
                    iPart = iPart_orientation[0]
                    orientation = iPart_orientation[1]
                    MapPart = self.vPart[iPart]
                    MapPart.orientation = orientation

                    alpha1 = alpha0 + calpha * MapPart.length
                    MapPart.x0 = x0
                    MapPart.y0 = y0
                    MapPart.r = r
                    MapPart.alpha0 = alpha0
                    MapPart.alpha1 = alpha1
                    alpha0 = alpha1 + dalpha
            print("ToPrint_calcCoorForSelectedParts...Finished")

        def part_get(self, name):
            iPart = self.vsPartName.index(name)
            return self.vPart[iPart]

        def get_fromGeneticMap(
            self,
            GenomeMapComparisonGraph,
            sMapName,
            GeneticMap,
            bAddMarkers=False,
            imap=-1,
        ):
            # only parts, no markers
            self.caption = sMapName
            self.name = sMapName
            for myChr in GeneticMap.vChromosome:
                sChr = myChr.vsName[0]
                length = myChr.geneticLengthBasedOnSkeletonMarlers_cM
                if length <= 0:
                    length = myChr.length
                self.addPart(sChr, sChr, length, 1)
            if bAddMarkers:
                for geneticMarker in GeneticMap.vMarker:
                    sMarkerName = geneticMarker.sName
                    im = -1
                    if sMarkerName in GenomeMapComparisonGraph.vmarkerName:
                        im = GenomeMapComparisonGraph.vmarkerName.index(sMarkerName)
                    else:
                        Marker = GenomeMapComparisonGraph.clMarker(sMarkerName)
                        GenomeMapComparisonGraph.vmarker.append(Marker)
                        GenomeMapComparisonGraph.vmarkerName.append(sMarkerName)
                        im = GenomeMapComparisonGraph.vmarkerName.index(sMarkerName)
                    Marker = GenomeMapComparisonGraph.vmarker[im]
                    partname = geneticMarker.Chromosome.vsName[0]
                    coor = geneticMarker.coor
                    caption = str(
                        geneticMarker.iType
                    )  # 0 - skeleton, 1 - close to skeleton (about twin), 2 - added from up, 3 - added from down
                    pos = Marker.clpos(imap, partname, coor)
                    pos.caption = caption
                    Marker.vpos.append(pos)

        def reordering_and_reorientation(
            self, GenomeMapComparisonGraph, imap0, index=-1
        ):
            bPrintDetails = False
            VovaMath = clVovaMath()

            map0 = GenomeMapComparisonGraph.vMap[imap0]
            v_iPart_orientation_copy = []
            vvCoorOnPart = []
            vvx = []
            vvy = []
            vvalpha = []
            for iPart_orientation in self.ToPrint_v_iPart_orientation:
                iPart = iPart_orientation[0]
                orientation = iPart_orientation[1]
                v_iPart_orientation_copy.append([iPart, orientation])
                vvCoorOnPart.append([])
                vvx.append([])
                vvy.append([])
                vvalpha.append([])
                # print(str([iPart,orientation]))
            # print ""

            vxAll = []
            vyAll = []
            for marker in GenomeMapComparisonGraph.vmarker:
                vPos0 = marker.vPosToPrint_get(map0, False)
                vPos1 = marker.vPosToPrint_get(self, True)
                if len(vPos0) > 0 and len(vPos1) > 0:
                    i1 = self.ToPrint_vsPartName.index(vPos1[0].partname)
                    # 	iPart_orientation=map0.ToPrint_v_iPart_orientation[i]
                    # 	iPart=iPart_orientation[0]
                    vx = []
                    vy = []
                    valpha = []
                    for pos in vPos0:
                        i = map0.ToPrint_vsPartName.index(pos.partname)
                        iPart_orientation = map0.ToPrint_v_iPart_orientation[i]
                        iPart = iPart_orientation[0]
                        orientation = iPart_orientation[1]
                        part0 = map0.vPart[iPart]
                        x, y, alpha = part0.xy_get(pos.coor, orientation)
                        vx.append(x)
                        vy.append(y)
                        valpha.append(alpha)
                    vCoor = []
                    for pos in vPos1:
                        vCoor.append(pos.coor)
                    x = VovaMath.mean(vx)
                    y = VovaMath.mean(vy)
                    alpha = VovaMath.mean(valpha)
                    coor = VovaMath.mean(vCoor)
                    vvx[i1].append(x)
                    vvy[i1].append(y)
                    vvalpha[i1].append(alpha)
                    vvCoorOnPart[i1].append(coor)
                    vxAll.append(x)
                    vyAll.append(y)

            bx = VovaMath.var(vxAll) >= VovaMath.var(vyAll)
            vq = []
            i = 0
            for iPart_orientation in v_iPart_orientation_copy:
                iPart = iPart_orientation[0]
                # orientation=iPart_orientation[1]
                vx = []
                if index == -1:
                    vx = vvx[i] if bx else vvy[i]
                if index == 0:
                    vx = vvx[i]
                if index == 1:
                    vx = vvy[i]
                if index == 2:
                    vx = vvalpha[i]
                x = VovaMath.mean(vx)
                if bPrintDetails:
                    print(str(iPart) + " " + str(x) + ": " + str(vx))
                vCoorOnPart = vvCoorOnPart[i]
                corrRank, p = VovaMath.corrSpearmanRank(vx, vCoorOnPart)
                orientation = 1 if corrRank >= 0 else -1
                vq.append([x, iPart, orientation])
                i += 1

            def MyFunc0(q):
                return q[0]

            vq.sort(key=MyFunc0)

            if bPrintDetails:
                print("reordering_and_reorientation:")
            v_iPart_orientation = []
            for q in vq:
                if bPrintDetails:
                    print(str(q))
                v_iPart_orientation.append([q[1], q[2]])
            self.ToPrint_start(False, v_iPart_orientation)
            self.ToPrint_calcCoorForSelectedParts(bPrintDetails)

    class clMarker:
        def __init__(self, name):
            self.name = name
            self.vpos = []
            self.color = "black"  # "gray"
            self.w = 0.5

        class clpos:
            def __init__(self, imap, partname, coor):
                self.imap = imap
                self.partname = partname
                # no need iPart here because this parameter is not stable here: we don't try to drew Graph with all
                self.coor = coor
                self.caption = ""

        def addpos(self, imap, partname, coor):
            pos = self.clpos(imap, partname, coor)
            self.vpos.append(pos)

        def addpos___basedOnGeneticMap(self, imap, sMarkerNameOnGeneticMap, GeneticMap):
            if sMarkerNameOnGeneticMap in GeneticMap.vsMarkerName:
                im = GeneticMap.vsMarkerName.index(sMarkerNameOnGeneticMap)
                m = GeneticMap.vMarker[im]
                partname = m.Chromosome.vsName[0]
                coor = m.coor
                self.addpos(imap, partname, coor)

        def vPosToPrint_get(self, map, bOnePartOnly):
            vPos = []
            iMap = map.id
            for pos in self.vpos:
                if pos.imap == iMap:
                    if pos.partname in map.ToPrint_vsPartName:
                        vPos.append(pos)
            if bOnePartOnly and len(vPos) > 1:
                s = vPos[0].partname
                for pos in vPos:
                    if pos.partname != s:
                        return []
            return vPos

    def addMap(self, map):
        nmaps = len(self.vMap)
        map.id = nmaps
        self.vMap.append(map)

    def ToPrint_printToFile(self, bConseqMapMarkersOnly=True):
        bMarkersOfLargePartsOnly = False
        ##data for comparison
        # xlim	0	100	10
        # ylim	0	100	10
        # text	10	0	"ctg"	cex	0.65	pos	1	col	"black"
        # segments	10	0	10	30	col	"darkgreen"	lwd	5	lty	"dotted"
        # draw.arc	50	50	20	30	90	col	"green"	lwd	"solid"
        # draw.arc	50	20	20	0	360	col	"red"	lwd	"solid"
        # points	50	20	col	"red"
        sFileName = "graphProba___1.txt"
        file = open(sFileName, "w")
        s = "#clGenomeMapComparisonGraph"
        file.write(s + "\n")

        # to help r to know the number of columns
        s = "for R"
        for i in range(15):
            s += "\ta"
        file.write(s + "\n")

        # limits
        s = "xlim\t" + str(self.xmin) + "\t" + str(self.xmax) + "\t10"
        file.write(s + "\n")
        s = "ylim\t" + str(self.ymin) + "\t" + str(self.ymax) + "\t10"
        file.write(s + "\n")

        # markers
        s = "#Markers:"
        file.write(s + "\n")
        #
        # print("nmarkers="+str(len(self.vmarker)))
        for marker in self.vmarker:
            np = len(marker.vpos)
            # print marker.name+"\t"+str(len(marker.vpos))
            for ip1 in range(np - 1):
                pos1 = marker.vpos[ip1]
                # print str(pos1)
                map1 = self.vMap[pos1.imap]
                if pos1.partname in map1.ToPrint_vsPartName:
                    part1 = map1.part_get(pos1.partname)  # vPart[pos1.ipart]
                    i1 = map1.ToPrint_vsPartName.index(pos1.partname)
                    orientation1 = map1.ToPrint_v_iPart_orientation[i1][1]
                    x0, y0, alpha0 = part1.xy_get(pos1.coor, orientation1)

                    for ip2 in range(ip1 + 1, np):
                        pos2 = marker.vpos[ip2]
                        # print str(pos2)
                        map2 = self.vMap[pos2.imap]
                        b = pos2.partname in map2.ToPrint_vsPartName
                        if b:
                            if bConseqMapMarkersOnly:
                                if (abs(pos1.imap - pos2.imap)) != 1:
                                    b = False
                        if b:
                            i2 = map2.ToPrint_vsPartName.index(pos2.partname)
                            orientation2 = map2.ToPrint_v_iPart_orientation[i2][1]
                            part2 = map2.part_get(pos2.partname)  # vPart[pos2.ipart]
                            x1, y1, alpha1 = part2.xy_get(pos2.coor, orientation2)

                            if bMarkersOfLargePartsOnly:
                                b = part2.length > 2000000
                                # print(pos2.partname+" "+str(part2.length))
                                # i=1/0
                                if b and pos1.imap > 0:
                                    b = part1.length > 2000000
                        if b:
                            if self.type == 0:
                                sColor = marker.color
                                if map2.ToPrint_bUse_sColor_forAllMarkers:
                                    sColor = map2.ToPrint_sColor
                                # points	50	20	col	"red"
                                s = "points\t" + str(x0) + "\t" + str(y1)
                                s += "\tcol\t" + sColor
                                s += (
                                    "\t#"
                                    + marker.name
                                    + " "
                                    + self.vMap[pos1.imap].caption
                                    + " "
                                    + pos1.partname
                                    + " "
                                    + str(pos1.coor)
                                    + "   "
                                    + " "
                                    + self.vMap[pos2.imap].caption
                                    + " "
                                    + pos2.partname
                                    + " "
                                    + str(pos2.coor)
                                )
                                s += (
                                    " "
                                    + str(part2.x0)
                                    + " "
                                    + str(part2.x1)
                                    + " "
                                    + str(part2.y0)
                                    + " "
                                    + str(part2.y1)
                                    + " "
                                    + str(part2.length)
                                )
                                file.write(s + "\n")
                            if self.type == 1 or self.type == 2:
                                s = "segments\t" + str(x0) + "\t" + str(y0)
                                s += "\t" + str(x1) + "\t" + str(y1)
                                s += "\tcol\t" + marker.color
                                s += "\tlwd\t" + str(marker.w)
                                s += "\tlty\t" + "solid"
                                s += "\t#" + marker.name
                                file.write(s + "\n")
        # parts
        s = "#parts"
        file.write(s + "\n")
        iMap = 0
        for map in self.vMap:
            s = "#map " + map.caption
            file.write(s + "\n")

            # for part in map.vPart:
            for iPart_orientation in map.ToPrint_v_iPart_orientation:
                iPart = iPart_orientation[0]
                orientation = iPart_orientation[1]
                part = map.vPart[iPart]

                s = "#" + part.caption
                file.write(s + "\n")

                # print(str(part.type))
                if part.type == 0 or part.type == 1:
                    # segments
                    # s="segments\t"+str(part.x0)+"\t"+str(part.y0)
                    # s+="\t"+str(part.x1)+"\t"+str(part.y1)
                    #
                    # arrows
                    self.vMap
                    s = "arrows\t" + str(part.x0) + "\t" + str(part.y0)
                    s += "\t" + str(part.x1) + "\t" + str(part.y1)
                    s += "\tlength\t0.05"

                    if orientation < 0:
                        s += "\tcode\t1"  # from (x1,y1) to (x0,y0)
                    else:
                        s += "\tcode\t2"  # from (x0,y0) to (x1,y1)
                    #
                    # https://search.r-project.org/CRAN/refmans/shape/html/Arrows.html
                    # Arrows(x0, y0, x1, y1, code = 2, arr.length = 0.4,
                    # 	arr.width = arr.length/2, arr.adj = 0.5, arr.type = "curved",
                    # 	segment = TRUE, col = "black", lcol = col, lty = 1, arr.col = lcol,
                    # 	lwd = 1, arr.lwd = lwd, ...)
                    # s="Arrows\t"+str(part.x0)+"\t"+str(part.y0)
                    # s+="\t"+str(part.x1)+"\t"+str(part.y1)
                    # s+="\tcol\t"+part.col
                    #
                    s += "\tcol\t" + part.col
                    s += "\tlwd\t" + str(part.w)
                    s += "\tlty\t" + "solid"
                    file.write(s + "\n")

                    # grid
                    if map.ToPrint_bGrid:
                        if part.type == 0:
                            sColor = part.col
                            if iMap >= 1:
                                sColor = map.ToPrint_sColor
                            if iMap == 0:
                                s = "segments\t" + str(part.x1) + "\t" + str(part.y1)
                                s += "\t" + str(part.x1) + "\t" + str(self.ymax)
                                s += "\tcol\t" + sColor
                                s += "\tlwd\t" + str(0.01)
                                s += "\tlty\t" + "solid"
                                file.write(s + "\n")
                            if iMap > 0:
                                if part.length >= map.ToPrint_GridLenMin:
                                    s = (
                                        "segments\t"
                                        + str(part.x1)
                                        + "\t"
                                        + str(part.y1)
                                    )
                                    s += "\t" + str(self.xmax) + "\t" + str(part.y1)
                                    s += "\tcol\t" + sColor
                                    s += "\tlwd\t" + str(0.01)
                                    s += "\tlty\t" + "solid"
                                    file.write(s + "\n")
                if part.type == 2:  # radial
                    s = (
                        "draw.arc\t"
                        + str(part.x0)
                        + "\t"
                        + str(part.y0)
                        + "\t"
                        + str(part.r)
                    )
                    s += "\t" + str(part.alpha0) + "\t" + str(part.alpha1)
                    s += "\tcol\t" + part.col
                    s += "\tlwd\t" + str(part.w)
                    s += "\tlty\t" + "solid"
                    file.write(s + "\n")
            iMap += 1

        # captions
        iMap = 0
        for map in self.vMap:
            sColor = "black"
            if iMap > 1:
                sColor = map.ToPrint_sColor

            # maps
            if map.type == 0:  # oxford
                if iMap == 0:
                    s = (
                        "text\t"
                        + str(0.5 * (map.x0 + map.x1))
                        + "\t"
                        + str(map.y0 - 5)
                        + "\t"
                        + map.caption
                        + "\tcex\t0.65\tpos\t1\tcol\tblack"
                    )
                    file.write(s + "\n")
                if iMap >= 1:
                    s = (
                        "text\t"
                        + str(map.x0 - 5)
                        + "\t"
                        + str(0.5 * (map.y0 + map.y1) - (iMap - 1) * 5)
                        + "\t"
                        + map.caption
                        + "\tcex\t0.65\tpos\t2\tcol\t"
                        + sColor
                    )
                    file.write(s + "\n")

            if map.type == 1:  # parallel
                s = (
                    "text\t"
                    + str(map.x0)
                    + "\t"
                    + str(map.y0)
                    + "\t"
                    + map.caption
                    + "\tcex\t0.65\tpos\t1\tcol\tblack"
                )
                file.write(s + "\n")

            # parts
            # for part in map.vPart:
            for iPart_orientation in map.ToPrint_v_iPart_orientation:
                iPart = iPart_orientation[0]
                part = map.vPart[iPart]
                if part.type == 0:
                    if iMap == 0:
                        s = (
                            "text\t"
                            + str(0.5 * (part.x0 + part.x1))
                            + "\t"
                            + str(0.5 * (part.y0 + part.y1))
                            + "\t"
                            + part.caption
                            + "\tcex\t0.65\tpos\t1\tcol\tblack"
                        )
                        file.write(s + "\n")
                    if iMap >= 1:
                        s = (
                            "text\t"
                            + str(0.5 * (part.x0 + part.x1))
                            + "\t"
                            + str(0.5 * (part.y0 + part.y1))
                            + "\t"
                            + part.caption
                            + "\tcex\t0.65\tpos\t2\tcol\t"
                            + sColor
                        )
                        file.write(s + "\n")
                if part.type == 1:
                    s = (
                        "text\t"
                        + str(0.5 * (part.x0 + part.x1))
                        + "\t"
                        + str(0.5 * (part.y0 + part.y1))
                        + "\t"
                        + part.caption
                        + "\tcex\t0.65\tpos\t2\tcol\tblack"
                    )
                    file.write(s + "\n")
            iMap += 1

        file.close()

    def test(self):
        map1 = self.clMap()
        map1.caption = "Map 1"
        map1.addPart("chr01", "chr01", 100, 1)
        map1.addPart("chr02", "chr02", 80, 1)
        map1.addPart("chr03", "chr03", 50, 1)
        ##
        map2 = self.clMap()
        map2.caption = "Map 2"
        map2.addPart("ctg1", "ctg1", 10, 1)
        map2.addPart("ctg2", "ctg2", 8, -1)

        nMarkers = 100
        for i in range(nMarkers):
            s = "marker_" + str(i + 1)
            marker = self.clMarker(s)
            coorGlobal = map1.TotalMapLength * float(i) / nMarkers
            ipart, coor = map1.ipart_coor_get(coorGlobal)
            partname = map1.vsPartName[ipart]
            if partname in map1.vsPartName:
                marker.addpos(0, partname, coor)

            coorGlobal = map2.TotalMapLength * float(i) / nMarkers
            ipart, coor = map2.ipart_coor_get(coorGlobal)
            partname = map2.vsPartName[ipart]
            if partname in map2.vsPartName:
                marker.addpos(1, partname, coor)

            self.vmarker.append(marker)
            self.vmarkerName.append(marker.name)
        self.type = 1
        self.GenomeMapComparisonGraph_2maps___run(map1, map2, self.vmarker, self.type)

    def TestLinkagesForSingleGeneticMap___vmarker_get(
        self, Genotypes, GeneticMap, indexMarkerNameTransform=0, cutOffToShow=0.3
    ):  # vmarker=
        print("TestLinkagesForSingleGeneticMap___vmarker_get...")

        def markerNamesOnMap_get(s1, s2, indexMarkerNameTransform):  # s1pp,s2pp=
            s1pp = s1
            s2pp = s2
            if indexMarkerNameTransform == 0:
                pass  # the same names
            if indexMarkerNameTransform == 1:
                # scaffold1p1327199 -> s1p1327199
                ss = s1.split("d")  # ["scaffol","1p1327199"]
                s1pp = "s" + ss[1]  # "s1p1327199"

                ss = s2.split("d")
                s2pp = "s" + ss[1]
            return s1pp, s2pp

        recVova = clRecombination()

        vmarker = []
        im = 0
        nm = len(Genotypes.vMarker)
        for m1 in Genotypes.vMarker:
            s1 = m1.sMarker
            for m2 in Genotypes.vMarker:
                s2 = m2.sMarker

                nR, nN, nMissed = recVova.nnn(m1.g, m2.g, False)
                r = recVova.rML(nR, nN)
                dGenetic = recVova.distByR(r)

                if r <= cutOffToShow:
                    s1pp, s2pp = markerNamesOnMap_get(s1, s2, indexMarkerNameTransform)
                    s = s1pp + "_" + s2pp

                    marker = self.clMarker(s)
                    if dGenetic > 1:
                        marker.color = "blue3"
                    if dGenetic > 5:
                        marker.color = "blue"
                    if dGenetic > 10:
                        marker.color = "red"
                    if dGenetic > 15:
                        marker.color = "violet"
                    if dGenetic > 20:
                        marker.color = "tan1"
                    if dGenetic > 25:
                        marker.color = "yellow"
                    if dGenetic > 35:
                        marker.color = "snow2"

                    vmarker.append(marker)

                    marker.addpos___basedOnGeneticMap(0, s1pp, GeneticMap)
                    marker.addpos___basedOnGeneticMap(1, s2pp, GeneticMap)
            im += 1
            if im % 100 == 1:
                print(str(im) + " of " + str(nm))
        print("TestLinkagesForSingleGeneticMap___vmarker_get...Finished")
        return vmarker

    def TestLinkagesForSingleGeneticMap(
        self,
        Genotypes,
        GeneticMap,
        sMap,
        indexMarkerNameTransform=0,
        cutOffToShow=0.3,
        bReorderingAndReorientationMap2=False,
    ):
        map1 = self.clMap()
        map1.get_fromGeneticMap(self, sMap, GeneticMap)
        map2 = self.clMap()
        map2.get_fromGeneticMap(self, sMap, GeneticMap)
        vmarker = self.TestLinkagesForSingleGeneticMap___vmarker_get(
            Genotypes, GeneticMap, indexMarkerNameTransform, cutOffToShow
        )
        iType = 0  # oxford
        bAll_and_intialOrientation = True
        # bAll_and_intialOrientation=False
        if not bAll_and_intialOrientation:
            # Example:
            # map1.ToPrint_v_iPart_orientation=[[0,1]]
            # map2.ToPrint_v_iPart_orientation=[[0,1]]
            map1.ToPrint_v_iPart_orientation = [[12, 1]]
            map2.ToPrint_v_iPart_orientation = [[12, 1]]
            map1.ToPrint_v_iPart_orientation = [[2, 1]]
            map2.ToPrint_v_iPart_orientation = [[2, 1]]
        self.GenomeMapComparisonGraph_2maps___run(
            map1,
            map2,
            vmarker,
            iType,
            bAll_and_intialOrientation,
            bReorderingAndReorientationMap2,
        )

    def GenomeMapComparisonGraph_2maps___run(
        self,
        map1,
        map2,
        vmarker,
        iType,
        bAll_and_intialOrientation=True,
        bReorderingAndReorientationMap2=True,
    ):
        self.vmarker = vmarker
        self.vmarkerName = []
        for marker in vmarker:
            self.vmarkerName.append(marker.name)
        self.type = iType
        if self.type == 0:  # oxford
            map1.x0 = 0
            map1.x1 = 100
            map1.y0 = 0  # -5
            map1.y1 = 0  # -5
            map2.x0 = 0  # -5
            map2.x1 = 0  # -5
            map2.y0 = 0
            map2.y1 = 100
        if self.type == 1:  # parallel
            map1.x0 = 10
            map1.x1 = 10
            map1.y0 = 0
            map1.y1 = 100
            map2.x0 = 20
            map2.x1 = 20
            map2.y0 = 0
            map2.y1 = 100
        if self.type == 2:  # radial
            map1.x0 = 50
            map1.y0 = 50
            map2.x0 = 50
            map2.y0 = 50
            map1.r = 25
            map2.r = 30
            map1.alpha0 = -90
            map1.alpha1 = 270
            map2.alpha0 = -90
            map2.alpha1 = 270

        map1.type_set(self.type)
        map2.type_set(self.type)
        self.vMap = []
        self.addMap(map1)
        self.addMap(map2)

        for map in self.vMap:
            if bAll_and_intialOrientation:
                map.ToPrint_start(True)
                if bReorderingAndReorientationMap2 and map.id == 1:
                    index = -1
                    if self.type == 2:
                        index = 2
                    map2.reordering_and_reorientation(self, 0, index)
            else:
                v_iPart_orientation = []
                for iPart_orientation in map.ToPrint_v_iPart_orientation:
                    v_iPart_orientation.append(iPart_orientation)
                map.ToPrint_start(False, v_iPart_orientation)
            map.ToPrint_calcCoorForSelectedParts(False)
        self.ToPrint_printToFile()

    def GenomeMapComparisonGraph_severalMaps(
        self, MarkersWithMultiplePos, vsMap, viReordering_and_reorientation=[]
    ):
        self.type = 1  # parallel   #2#0#oxford
        nMaps = len(vsMap)
        iMap = 0
        for sMap in vsMap:
            GeneticMap = MarkersWithMultiplePos.GeneticMap__get(sMap)
            map = self.clMap()
            map.get_fromGeneticMap(self, sMap, GeneticMap, True, iMap)
            map.type_set(self.type)
            self.addMap(map)

            if nMaps > 2:
                x = 10 + float((100 - 10) * iMap) / (nMaps - 1)  # 10,..,100
            if nMaps == 2:
                x = 10 + iMap * 10  # 10,20
            map.x0 = x
            map.x1 = x
            map.y0 = 0
            map.y1 = 100
            iMap += 1

        if len(viReordering_and_reorientation) == 0:
            iMap = 0
            for sMap in vsMap:
                if iMap == 0:
                    viReordering_and_reorientation.append(-1)
                else:
                    viReordering_and_reorientation.append(iMap - 1)
                iMap += 1
        # vmarker=GenomeMapComparisonGraph.vmarker

        bAll_and_intialOrientation = True
        # GenomeMapComparisonGraph=clGenomeMapComparisonGraph()
        # self.GenomeMapComparisonGraph_2maps___run(map1,map2,vmarker,iType,bAll_and_intialOrientation)
        for map in self.vMap:
            if bAll_and_intialOrientation:
                map.ToPrint_start(bAll_and_intialOrientation)

                # if bReorderingAndReorientationMap2 and map.id==1:
                # 	index=-1
                # 	if self.type==2:
                # 		index=2
                # 	map2.reordering_and_reorientation(self,0,index)
            else:
                v_iPart_orientation = []
                for iPart_orientation in map.ToPrint_v_iPart_orientation:
                    v_iPart_orientation.append(iPart_orientation)
                map.ToPrint_start(bAll_and_intialOrientation, v_iPart_orientation)
            map.ToPrint_calcCoorForSelectedParts(False)  # bPrintDetails

        iMap = 0
        for map in self.vMap:
            if viReordering_and_reorientation[iMap] >= 0:
                map.reordering_and_reorientation(
                    self, viReordering_and_reorientation[iMap], self.type
                )
            if iMap > 0:
                ToPrint_vsPartNamePP = []

                # map.ToPrint_vsPartName=ToPrint_vsPartNamePP
            iMap += 1
        for marker in self.vmarker:
            marker.color = "grey91"

        self.ToPrint_printToFile(bConseqMapMarkersOnly=True)

    def GenomeMapComparisonGraphOxford_severalMaps(
        self,
        MarkersWithMultiplePos,
        vsMap,
        vsColor=[],
        viReordering_and_reorientation=[],
        vbChromosomes=[],
        yToPrint_GridLenMin=2000000,
    ):
        self.type = 0  # oxford
        nMaps = len(vsMap)
        iMap = 0
        for sMap in vsMap:
            GeneticMap = MarkersWithMultiplePos.GeneticMap__get(sMap)
            map = self.clMap()
            map.get_fromGeneticMap(self, sMap, GeneticMap, True, iMap)
            map.type_set(self.type)
            self.addMap(map)

            if iMap == 0:
                map.x0 = 0
                map.x1 = 100
                map.y0 = 0
                map.y1 = 0
            else:
                map.x0 = 0
                map.x1 = 0
                map.y0 = 0
                map.y1 = 100
            iMap += 1

        if len(vsColor) == 0:
            vsColor = [
                "black",
                "black",
                "red",
                "blue",
                "green",
                "yellow",
                "lightblue1",
                "lawngreen",
                "grey1",
                "yellow",
            ]
        if len(viReordering_and_reorientation) == 0:
            iMap = 0
            for sMap in vsMap:
                if iMap == 0:
                    viReordering_and_reorientation.append(-1)
                else:
                    viReordering_and_reorientation.append(0)
                iMap += 1
        if len(vbChromosomes) == 0:
            for sMap in vsMap:
                vbChromosomes.append(True)
        # vmarker=GenomeMapComparisonGraph.vmarker

        bAll_and_intialOrientation = True
        # GenomeMapComparisonGraph=clGenomeMapComparisonGraph()
        # self.GenomeMapComparisonGraph_2maps___run(map1,map2,vmarker,iType,bAll_and_intialOrientation)
        for map in self.vMap:
            if bAll_and_intialOrientation:
                map.ToPrint_start(bAll_and_intialOrientation)

                # if bReorderingAndReorientationMap2 and map.id==1:
                # 	index=-1
                # 	if self.type==2:
                # 		index=2
                # 	map2.reordering_and_reorientation(self,0,index)
            else:
                v_iPart_orientation = []
                for iPart_orientation in map.ToPrint_v_iPart_orientation:
                    v_iPart_orientation.append(iPart_orientation)
                map.ToPrint_start(bAll_and_intialOrientation, v_iPart_orientation)
            map.ToPrint_calcCoorForSelectedParts(False)  # bPrintDetails

        iMap = 0
        for map in self.vMap:
            if viReordering_and_reorientation[iMap] >= 0:
                map.reordering_and_reorientation(
                    self, viReordering_and_reorientation[iMap], self.type
                )
            # if iMap>0:
            # 	ToPrint_vsPartNamePP=[]
            # 	#map.ToPrint_vsPartName=ToPrint_vsPartNamePP
            iMap += 1
        # for marker in self.vmarker:
        # 	marker.color="grey91"

        iMap = 0
        for map in self.vMap:
            map.ToPrint_bGrid = vbChromosomes[iMap]
            map.ToPrint_bUse_sColor_forAllMarkers = True
            map.ToPrint_sColor = vsColor[iMap]
            if iMap > 0:
                map.ToPrint_GridLenMin = yToPrint_GridLenMin
            iMap += 1
        print("nMaps=" + str(len(self.vMap)))
        self.ToPrint_printToFile(bConseqMapMarkersOnly=False)

    def printTableOfMarkers(
        self, sFileName="TableOfMarkers_byMaps.txt", Genotypes=None
    ):
        vsmarker = []
        if not (Genotypes is None):
            vsmarker = []
            for Marker in Genotypes.vMarker:
                vsmarker.append(Marker.sMarker)
        f = open(sFileName, "w")

        # shapka
        s = "marker"
        for map in self.vMap:
            s += "\t" + map.name + "\t" + "part" + "\t" + "comment"
        if not (Genotypes is None):
            s += "\tn0\tn1\tn2\tnHap0\tnHap1\tnDip0\tnDip1"
        f.write(s + "\n")

        for marker in self.vmarker:
            vvpos = []
            for map in self.vMap:
                vvpos.append([])
            for pos in marker.vpos:
                imap = pos.imap
                vvpos[imap].append(pos)
            s = marker.name
            imap = 0
            for map in self.vMap:
                if len(vvpos[imap]) == 0:
                    s += "\t" + "no" + "\t" + "no" + "\t" + "no"
                else:
                    s1 = ""
                    s2 = ""
                    s3 = ""
                    ipos = 0
                    for pos in vvpos[imap]:
                        if ipos > 0:
                            s1 += ","
                            s2 += ","
                            s3 += ","
                        s1 += pos.partname
                        s2 += str(pos.coor)
                        s3 += pos.caption
                        ipos += 1
                    s += "\t" + s1 + "\t" + s2 + "\t" + s3
                imap += 1
            if not (Genotypes is None):
                i = vsmarker.index(marker.name)
                Marker = Genotypes.vMarker[i]
                s += (
                    "\t"
                    + str(Marker.nIndWithState[0])
                    + "\t"
                    + str(Marker.nIndWithState[1])
                    + "\t"
                    + str(Marker.nIndWithState[2])
                )
                if len(Marker.nHapWithState) > 0:
                    s += (
                        "\t"
                        + str(Marker.nHapWithState[0])
                        + "\t"
                        + str(Marker.nHapWithState[0])
                    )
                    s += (
                        "\t"
                        + str(Marker.nDipWithState[0])
                        + "\t"
                        + str(Marker.nDipWithState[1])
                    )
            f.write(s + "\n")
        f.close()

    def vvvmarkers_get(self, imap1, imap2):  # vvvmarkers=
        vvvmarkers = []  # [iPartMap1,iPartMap2]
        for part1 in self.vMap[imap1].vPart:
            vvmarkers = []
            for part2 in self.vMap[imap2].vPart:
                vmarkers = []
                vvmarkers.append(vmarkers)
            vvvmarkers.append(vvmarkers)
        for marker in self.vmarker:
            vip1 = []
            vip2 = []
            for pos in marker.vpos:
                if pos.imap == imap1:
                    ip1 = self.vMap[imap1].vsPartName.index(pos.partname)
                    vip1.append(ip1)
                if pos.imap == imap2:
                    ip2 = self.vMap[imap2].vsPartName.index(pos.partname)
                    vip2.append(ip2)
            for ip1 in vip1:
                for ip2 in vip2:
                    vvvmarkers[ip1][ip2].append(marker)
        return vvvmarkers

    def printTableOfMaps(self, sFileName="TableOfMaps.txt"):
        f = open(sFileName, "w")

        s = "map statistics:"
        f.write(s + "\n")
        s = "map"
        for map in self.vMap:
            s += "\t" + map.name
            # f.write(s+'\n')
        f.write(s + "\n")
        #
        s = "len"
        for map in self.vMap:
            s += "\t" + str(map.TotalMapLength)
            # f.write(s+'\n')
        f.write(s + "\n")
        #
        s = "nParts"
        for map in self.vMap:
            s += "\t" + str(len(map.vPart))
            # f.write(s+'\n')
        f.write(s + "\n")
        #
        # N50 etc
        vvlen = []
        for map in self.vMap:
            vlen = []
            for part in map.vPart:
                vlen.append(part.length)
            vlen.sort()
            vvlen.append(vlen)
        for i in range(9):
            s = "N" + str((i + 1) * 10) + "(L" + str(i * 10) + ")"
            imap = 0
            for map in self.vMap:
                vlen = vvlen[imap]
                np = 0
                lp = 0
                for ll in vlen:
                    np += 1
                    lp += ll
                    if ll > i * 0.01 * map.TotalMapLength:
                        break
                s += "\t" + str(vlen[np - 1]) + "(" + str(np) + ")"
                imap += 1
            f.write(s + "\n")
        #
        s = "nMarkers"
        vvvpos = []
        for marker in self.vmarker:
            vvpos = []
            for map in self.vMap:
                vvpos.append([])
            for pos in marker.vpos:
                imap = pos.imap
                vvpos[imap].append(pos)
            vvvpos.append(vvpos)
        imap = 0
        for map in self.vMap:
            n = 0
            for vvpos in vvvpos:
                vpos = vvpos[imap]
                if len(vpos) > 0:
                    n += 1
            s += "\t" + str(n)
            imap += 1
        f.write(s + "\n")

        f.write("\n")
        # f.write('\n')
        # f.write('\n')

        imap = 0
        for map in self.vMap:
            f.write("\n")
            s = "map" + "\t" + map.name + "\t" + str(len(map.vPart)) + "\t" + "parts"
            f.write(s + "\n")
            s = "partName" + "\t" + "partcaption" + "\t" + "partLen"
            imap1 = 0
            for map1 in self.vMap:
                if imap1 != imap:
                    s += "\t" + map1.name
                imap1 += 1
            f.write(s + "\n")

            vvvvmarkers = []  # [imap1,iPartMap,iPartMap1,m]
            for imap1 in range(len(self.vMap)):
                vvvmarkers = self.vvvmarkers_get(imap, imap1)  # [iPartMap,iPartMap1,m]
                vvvvmarkers.append(vvvmarkers)
            ip = 0
            for part in map.vPart:
                s = part.name + "\t" + part.caption + "\t" + str(part.length)
                imap1 = 0
                for map1 in self.vMap:
                    if imap1 != imap:
                        vip1 = (
                            []
                        )  # list of iPart of map1 that are overlapped with part (of map)
                        vvmarkers = vvvvmarkers[imap1][ip]  # [iPartMap1,m]
                        ip1 = 0
                        for vmarkers in vvmarkers:
                            if len(vmarkers) > 0:
                                vip1.append(ip1)
                            ip1 += 1

                        s += "\t" + str(len(vip1))
                        if len(vip1) > 0:
                            s += ":"
                            iip1 = 0
                            for ip1 in vip1:
                                if iip1 > 0:
                                    s += ","
                                # print str(imap1)+" "+str(ip1)
                                s += self.vMap[imap1].vPart[ip1].name
                                vmarkers = vvmarkers[ip1]
                                s += "(" + str(len(vmarkers))
                                s += ":"
                                for marker in vmarkers:
                                    s += " " + marker.name
                                s += ")"
                                iip1 += 1
                    imap1 += 1
                f.write(s + "\n")
                ip += 1
            imap += 1
        f.close()

    def GenomeMapComparisonGraph_2maps___runSimple(
        self, sMap1, sMap2, GeneticMap1, GeneticMap2, sPathOutput
    ):  # "Males","Mix"
        GenomeMapComparisonGraph = (
            clGenomeMapComparisonGraph()
        )  # temporal additional copy
        map1 = GenomeMapComparisonGraph.clMap()
        map1.get_fromGeneticMap(GenomeMapComparisonGraph, sMap1, GeneticMap1, True, 0)
        GenomeMapComparisonGraph.addMap(map1)
        #
        map2 = GenomeMapComparisonGraph.clMap()
        map2.get_fromGeneticMap(GenomeMapComparisonGraph, sMap2, GeneticMap2, True, 1)
        GenomeMapComparisonGraph.addMap(map2)
        #
        vmarker = GenomeMapComparisonGraph.vmarker

        iType = 0  # 2#0#oxford
        bAll_and_intialOrientation = True
        # GenomeMapComparisonGraph=clGenomeMapComparisonGraph()
        self.GenomeMapComparisonGraph_2maps___run(
            map1, map2, vmarker, iType, bAll_and_intialOrientation
        )

        sFileName = (
            sPathOutput + "\\TableOfMarkers_byMaps_" + sMap1 + "_and_" + sMap2 + ".txt"
        )
        self.printTableOfMarkers(sFileName)
        sFileName = sPathOutput + "\\TableOfMaps_" + sMap1 + "_and_" + sMap2 + ".txt"
        self.printTableOfMaps(sFileName)

    def vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
        self, Genotypes, GeneticMap0, GeneticMap1, iFormat0=0, iFormat1=0, iFormatOut=0
    ):  # vmarker
        def sPP(s, iFormat, iFormatOut):
            if iFormat == iFormatOut:
                return s
            if iFormat == 1 and iFormatOut == 0:
                # s1p1327199 -> scaffold1p1327199
                return "scaffold" + s[1:]
            if iFormat == 0 and iFormatOut == 1:
                # scaffold1p1327199 -> s1p1327199
                ss = s.split("d")
                sAlex = "s" + ss[1]
                return sAlex

        vmarker = []
        for m in Genotypes.vMarker:
            s = m.sMarker
            marker = self.clMarker(s)
            vmarker.append(marker)

            marker.addpos___basedOnGeneticMap(
                0, sPP(s, iFormat0, iFormatOut), GeneticMap0
            )
            marker.addpos___basedOnGeneticMap(
                1, sPP(s, iFormat1, iFormatOut), GeneticMap1
            )
        return vmarker


class clGenotypes:
    def __init__(self):
        self.vMarker = []  # list of markers with genotypes of all individuals
        self.vsMarkerName = []  # names of markers
        self.nIndivids = 0  # number of individuals
        self.vsInd = []  # names of individuals
        self.vIndPloidy = []

        self.indexData = -1  # sourse of data
        self.sPath = ""  # path for relevant files (input/output)
        # good markers
        self.sFileName_genotypesOfGoodMarkers_inFormatChr = (
            ""  # table markers vs individuals (was sFileNamePPPP)
        )
        self.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
            ""  # table markers vs individuals (was sFileNamePPPPmm)
        )

    def marker_byName_get(self, sMarkerName):
        if len(self.vsMarkerName) == 0:
            self.vsMarkerName = self.vsMarkerName_get()
        if sMarkerName in self.vsMarkerName:
            im = self.vsMarkerName.index(sMarkerName)
            return self.vMarker[im]
        else:
            print("no such marker " + sMarkerName + " in genotypes")
            i = 1 / 0

    def readFromFileSimple(
        self, sFileName, bIndNames, sSep, idType, bPrint=False, bPrintDetails=False
    ):
        self.__init__()
        if bPrint:
            print("read genotypes from file " + sFileName + "...")
        fileWithGenotypes = open(sFileName, "r")
        iRow = 0
        n = 0
        if bPrintDetails:
            ##n = len(open(sFileName).readlines(  ))
            # n = 0
            # for line in open(sFileName).xreadlines(  ):
            # 	n += 1
            VovaServ = clVovaServ()
            n = VovaServ.nRowsInFile_get(sFileName)
        for s in fileWithGenotypes:
            # print(s)
            m = clMarkerWithGenotypesOfAllIndivids()
            if iRow == 0:
                if bIndNames:
                    self.vsInd = m.readSimple_indNames(s, sSep)
                    self.nIndivids = len(self.vsInd)
                    # print(self.nIndivids)
                    # print(self.vsInd)
                else:
                    m.readSimple(s, sSep, "0", "1", "-", self.nIndivids, idType)
                    self.vMarker.append(m)

                    # names
                    self.nIndivids = len(m.g)
                    self.vsInd = []
                    i = 0
                    for a in m.g:
                        i = i + 1
                        self.vsInd.append("ind" + str(i))
            else:
                m.readSimple(s, sSep, "0", "1", "-", self.nIndivids, idType)
                self.vMarker.append(m)
            iRow = iRow + 1
            if bPrintDetails:
                if iRow % 1000 == 1:
                    print(str(iRow) + " of " + str(n) + " markers are inputed")
        if bPrintDetails:
            print("nInd=" + str(self.nIndivids) + ", nMarkers=" + str(iRow))
            print("names: " + str(self.vsInd))
        fileWithGenotypes.close
        if bPrint:
            print("read genotypes from file " + sFileName + "...Finished")
        self.vsMarkerName = self.vsMarkerName_get()

    def readFromFileDiHaploidF1xF1(self, sFileName):
        self.__init__()
        bPrint = True
        bPrintDetails = True
        if bPrint:
            print("read genotypes from file " + sFileName + "...")
        fileWithGenotypes = open(sFileName, "r")

        # count rows
        n = 0
        if bPrintDetails:
            # n = len(open(sFileName).readlines(  ))
            n = 0
            for line in open(sFileName).xreadlines():
                n += 1

        iRow = 0
        sShapka = ""
        for s in fileWithGenotypes:
            # print(s)
            if iRow == 0:
                ss = s.split("\n")
                ss = ss[0].split("\t")
                self.vsInd = ss[6:]
                self.nIndivids = len(self.vsInd)
            else:
                m = clMarkerWithGenotypesOfAllIndivids()
                m.readDiHaploidF1xF1(s)
                self.vMarker.append(m)
            iRow = iRow + 1
            if bPrintDetails:
                if iRow % 1000 == 1:
                    print(str(iRow) + " of " + str(n) + " markers are inputed")
        if bPrintDetails:
            print("nInd=" + str(self.nIndivids) + ", nMarkers=" + str(iRow))
            print("names: " + str(self.vsInd))
        fileWithGenotypes.close
        if bPrint:
            print("read genotypes from file " + sFileName + "...Finished")
        self.vsMarkerName = self.vsMarkerName_get()

    def readFromFileVCF(
        self,
        sFileName,
        bPrint=False,
        bPrintDetails=False,
        nOfStateMin=15,
        nReadsMinBeSureNotHeterozygote=6,
        idType=0,
        ploidy=0,
    ):
        # idType: type of population
        # 0 - haploid (H), di-haploid (DH): only two genotypes can be presented (alternative alleles)
        # 1-3: ?
        # 4: heterozygous are possible
        # 5: backcross (BC), one homozygote and heterozygote
        #
        # ploidy:
        # 0 - unknown, all equal or individual specific
        # 1 - haploid
        # 2 - diploid

        # self.__init__()
        self.vMarker = []  # list of markers with genotypes of all individuals
        self.nIndivids = 0  # number of individuals
        self.vsInd = []

        if bPrint:
            print("read genotypes from file " + sFileName + "...")
        fileWithGenotypes = open(sFileName, "r")
        iRow = 0
        n = 0
        if bPrintDetails:
            # n = len(open(sFileName).readlines(  ))
            n = 0
            for line in open(sFileName).xreadlines():
                n += 1

        iColName = 0
        iColPos = 1
        iColS0 = 3
        iColS1 = 4
        iColFormat = 8
        nOk = 0
        for s in fileWithGenotypes:
            if len(s) > 2:
                # print(s)
                if s[0] == "#":
                    # number of individuals and individuals names
                    if s[1] != "#":
                        ss = s.split("\n")  # max split = 1
                        print(str(len(ss)))
                        if len(ss) == 1:
                            ss = s.split(chr(10))  # linux
                            print(" " + str(len(ss)))
                        s = ss[0]
                        ss = s.split("\t")
                        print("nTabs=" + str(len(ss)))
                        # CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT
                        self.nIndivids = 0
                        self.vsInd = []
                        iCol = 0
                        for s0 in ss:
                            if iCol > iColFormat:
                                self.nIndivids += 1
                                self.vsInd.append(s0)
                            iCol += 1
                        if (
                            sFileName
                            == "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\20220728\\populations.snps.vcf"
                        ):
                            self.vIndPloidy_by_name()
                        if ploidy > 0:
                            self.nIndivids = 0
                            for IndPloidy in self.vIndPloidy:
                                if IndPloidy == ploidy:
                                    self.nIndivids += 1
                        print("nIndivids=" + str(self.nIndivids))
                else:
                    # genotypes (only ok are stored)
                    g = clMarkerWithGenotypesOfAllIndivids()
                    g.readVCF(
                        s,
                        iColName,
                        iColPos,
                        iColS0,
                        iColS1,
                        iColFormat,
                        self.nIndivids,
                        nReadsMinBeSureNotHeterozygote,
                        idType,
                        self.vIndPloidy,
                        ploidy,
                    )
                    bOk = False
                    if idType == 0 or idType == 5:
                        # no heterozygotes
                        bOk = (
                            g.nIndWithState[0] >= nOfStateMin
                            and g.nIndWithState[1] >= nOfStateMin
                        )
                    if idType == 4:
                        # heterozygous (state=1) are possible
                        #
                        # vv=[g.nIndWithState[0],g.nIndWithState[1],g.nIndWithState[2]]
                        # vv.sort()
                        # bOk=vv[1]>=nOfStateMin
                        bOk = min(g.nIndWithState[0], g.nIndWithState[2]) >= nOfStateMin
                        if not bOk:
                            # bOk=min(g.nIndWithState[1],max(g.nIndWithState[0],g.nIndWithState[2]))>2*nOfStateMin
                            bOk = (
                                min(
                                    g.nIndWithState[1],
                                    g.nIndWithState[0] + g.nIndWithState[2],
                                )
                                > 2 * nOfStateMin
                            )
                    if (
                        sFileName
                        == "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\20220728\\populations.snps.vcf"
                    ):
                        if ploidy == 1:
                            bOk = (
                                g.nIndWithState[0] >= nOfStateMin
                                and g.nIndWithState[1] >= nOfStateMin
                            )
                        if ploidy == 2:
                            bOk = (
                                g.nIndWithState[0] >= nOfStateMin
                                and g.nIndWithState[1] >= nOfStateMin
                                and g.nIndWithState[2] == 0
                            )
                        if ploidy == 0:
                            # bOk=g.nHapWithState[0]>=nOfStateMin and g.nHapWithState[1]>=nOfStateMin and g.nDipWithState[0]>=nOfStateMin and g.nDipWithState[1]>=nOfStateMin and g.nIndWithState[2]==0
                            bOk = g.nIndWithState[2] <= 2
                            if bOk and g.nIndWithState[2] > 0:
                                ia = 0
                                for a in g.g:
                                    if a == 2:
                                        g.g[ia] = -1
                                    ia += 1
                            if bOk:
                                bOk = (
                                    g.nIndWithState[0] >= nOfStateMin
                                    and g.nIndWithState[1] >= nOfStateMin
                                )
                            if bOk:
                                bOk = (
                                    g.nHapWithState[0] >= 3
                                    and g.nHapWithState[1] >= 3
                                    and g.nDipWithState[0] >= 3
                                    and g.nDipWithState[1] >= 3
                                )
                                if not bOk:
                                    bOk = (
                                        g.nHapWithState[0] >= nOfStateMin
                                        and g.nHapWithState[1] >= nOfStateMin
                                    )
                                    if bOk:
                                        ia = 0
                                        for p in self.vIndPloidy:
                                            if p == 2:
                                                g.g[ia] = -1
                                            ia += 1
                                    else:
                                        bOk = (
                                            g.nDipWithState[0] >= nOfStateMin
                                            and g.nDipWithState[1] >= nOfStateMin
                                        )
                                        if bOk:
                                            ia = 0
                                            for p in self.vIndPloidy:
                                                if p == 1:
                                                    g.g[ia] = -1
                                                ia += 1

                        g.idType = 0
                    bOk = True
                    if bOk:
                        nOk += 1
                        # print str(nOk)
                        self.vMarker.append(g)
                        # print(str(len(g.g)))
                    iRow = iRow + 1
                    if bPrintDetails:
                        if iRow % 1000 == 1:
                            print(
                                str(iRow)
                                + " of "
                                + str(n)
                                + " markers are inputed nOk="
                                + str(nOk)
                            )
        if bPrintDetails:
            print("nInd=" + str(self.nIndivids) + ", nMarkers=" + str(iRow))
            print("names: " + str(self.vsInd))
        fileWithGenotypes.close
        if bPrint:
            print(
                "read genotypes from file " + sFileName + "...Finished, nOk=" + str(nOk)
            )
        self.vsMarkerName = self.vsMarkerName_get()

    def printGenotypes(
        self,
        sFileName,
        bAlleleNumbers=False,
        bPrint=False,
        bPrintDetails=False,
        bMSTformat=False,
    ):
        if bPrint:
            print("print genotypes to file " + sFileName + "...")
        fileWithGenotypes = open(sFileName, "w")
        # for MST software:
        # locus_name	i1	i2	i3	i4	i5	i6	i7	i8	i9	i10	i11	i12	i13	i14	i15	i16	i17	i18	i19	i20	i21	i22	i23	i24	i25	i26	i27	i28	i29	i30	i31	i32	i33	i34	i35	i36	i37	i38	i39	i40	i41	i42	i43	i44	i45	i46	i47	i48	i49	i50	i51	i52	i53	i54	i55	i56	i57	i58	i59	i60	i61	i62	i63	i64	i65	i66	i67	i68	i69	i70	i71	i72	i73	i74	i75	i76	i77	i78	i79	i80	i81	i82	i83	i84	i85	i86	i87	i88	i89	i90	i91	i92	i93	i94	i95	i96	i97	i98	i99	i100	i101	i102	i103	i104	i105	i106	i107	i108	i109	i110	i111	i112	i113	i114	i115	i116
        # scaffold1p67320	A	A	B	B	A	B	B	A	A	B	A	A	B	B	B	B	B	B	A	B	A	B	A	B	B	B	A	A	B	A	B	B	B	B	B	B	B	A	B	A	A	B	B	-	B	A	B	A	B	A	A	A	B	A	B	A	A	B	A	A	B	B	A	A	A	A	B	B	A	A	B	-	A	B	A	B	A	A	A	B	A	B	B	A	A	A	A	A	B	B	A	B	A	B	B	A	A	A	A	B	A	A	A	B	B	B	B	B	B	A	A	B	A	A	B	B
        if bMSTformat:
            s = "locus_name"
            if len(self.vsInd) == 0:
                for i in range(self.nIndivids):
                    s += "\t" + "i" + str(i + 1)
            else:
                for s1 in self.vsInd:
                    s += "\t" + s1
            fileWithGenotypes.write(s + "\n")
        n = len(self.vMarker)
        i = 0
        for g in self.vMarker:
            # text_file.write("Purchase Amount: %s" % TotalAmount)

            if bMSTformat:
                ##iMSTformat=3
                # s=g.s("",bAlleleNumbers,iMSTformat)
                ##print(s)
                # fileWithGenotypes.write(s)
                # fileWithGenotypes.write('\n')
                s = g.s("", bAlleleNumbers, 1)
                fileWithGenotypes.write(s)
                fileWithGenotypes.write("\n")
                s = g.s("", bAlleleNumbers, 2)
                fileWithGenotypes.write(s)
                fileWithGenotypes.write("\n")
            else:
                s = g.s("", bAlleleNumbers, 0)
                # print(s)
                fileWithGenotypes.write(s)
                fileWithGenotypes.write("\n")
            i = i + 1
            if bPrintDetails:
                if i % 10000 == 1:
                    print(str(i) + " of " + str(n) + " markers are printed")
        fileWithGenotypes.close()
        if bPrint:
            print("print genotypes to file " + sFileName + "...Finished")

    def vMarkerBest(self, vIndivids):  # vMarker=
        vMarker = []
        nn = len(vIndivids)
        for g in self.vMarker:
            vn, n = g.vnAlleleCombination(vIndivids)
            if n > 0.8 * nn:
                if vn[0] + vn[2] > 0.3 * nn:
                    if min(vn[0] + 0.5 * vn[1], vn[2] + 0.5 * vn[1]) > 0.2 * n:
                        vMarker.append(g)
        print(str(len(vMarker)) + " are selected from " + str(len(self.vMarker)))
        return vMarker

    def printLDchi2(self, vIndivids, sFileNameLD, dMax, bFiltr=True):
        bPrint = True
        bPrintDetails = True
        if bPrint:
            print("print LD to file " + sFileNameLD + "...")
        fileWithLDs = open(sFileNameLD, "w")  # detailed points
        fileWithLDs_LTC = open(
            sFileNameLD + "LTCgraph.txt", "w"
        )  # points simple to drew by LTC or R
        fileWithLDs_hyst = open(sFileNameLD + "hyst.txt", "w")  #

        vvVal = []
        vBound = [
            10,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            100,
            150,
            200,
            500,
            1000,
            3000,
            10000,
            20000,
            50000,
            100000,
            150000,
            200000,
        ]  # for hystogrames, d (bp)
        vqp = [10, 25, 50, 75, 90]  # percentages for quantiles
        for Bound in vBound:
            vvVal.append([])
        nBounds = len(vBound)
        VovaMath = clVovaMath()

        # shapka
        s = "i" + "\t" + "j" + "\t" + "marker_i" + "\t" + "marker_j"
        s += "\t" + "d(bp)"
        s += "\t" + "X^2" + "\t" + "nExpMin"
        s += "\t" + "LD" + "\t" + "LD_tag"
        s += "\t" + "r^2" + "\t" + "p-val"
        fileWithLDs.write(s + "\n")

        vMarker = self.vMarkerBest(vIndivids)
        n = len(vMarker)
        i = 0
        for g in vMarker:
            for j in range(i + 1, n):
                g1 = vMarker[j]
                if g1.PrivmanCtgIndex == g.PrivmanCtgIndex:
                    d = abs(g1.vPrivmanvPosOnCtg[0] - g.vPrivmanvPosOnCtg[0])
                    if d <= dMax:
                        X2, df, nExpMin, LD, LD_tag, r, p = g.compareWithMarkerLDchi2(
                            g1, vIndivids
                        )
                        if (not bFiltr) or ((X2 > 2 and nExpMin >= 5) or (p < 0.01)):
                            s = (
                                str(i)
                                + "\t"
                                + str(j)
                                + "\t"
                                + g.sMarker
                                + "\t"
                                + g1.sMarker
                            )
                            s += "\t" + str(d)
                            s += "\t" + str(X2) + "\t" + str(nExpMin)
                            s += "\t" + str(LD) + "\t" + str(LD_tag)
                            s += "\t" + str(r * r) + "\t" + str(p)
                            fileWithLDs.write(s + "\n")

                            sColor = "Light Yellow"
                            if bFiltr:
                                if p < 0.01:
                                    sColor = "Light Green"
                                if p < 0.001:
                                    sColor = "Light Red"
                                if p < 0.0001:
                                    sColor = "Black"
                            else:
                                sColor = "Black"
                            s = (
                                "point"
                                + "\t"
                                + str(d)
                                + "\t"
                                + str(r * r)
                                + "\t"
                                + sColor
                            )
                            fileWithLDs_LTC.write(s + "\n")
                        for k in range(nBounds):
                            if d < vBound[k]:
                                vvVal[k].append(r * r)
                                break
                else:
                    j = n
            i = i + 1
            if bPrintDetails:
                if i % 1000 == 1:
                    print(str(i) + " of " + str(n) + " markers are printed")

                    # shapka
                    s = "v0" + "\t" + "v1" + "\t" + "n" + "\t" + "mean" + "\t" + "stdv"
                    for qp in vqp:
                        s += "\t" + "q" + str(qp) + "%"
                    print(s)
                    fileWithLDs_hyst.write(s + "\n")
                    #
                    for j in range(nBounds):
                        v1 = vBound[j]
                        v0 = 0
                        if j > 0:
                            v0 = vBound[j - 1] + 1
                        nPoints = len(vvVal[j])
                        mean = VovaMath.mean(vvVal[j])
                        stdv = math.sqrt(VovaMath.var(vvVal[j]))
                        # VovaMath.quantile(vvVal[j],p)
                        vq = VovaMath.quantiles(vvVal[j], 100)
                        s = str(v0) + "\t" + str(v1) + "\t" + str(nPoints)
                        s += (
                            "\t"
                            + "{:1.3f}".format(mean)
                            + "\t"
                            + "{:1.3f}".format(stdv)
                        )
                        for qp in vqp:
                            s += "\t" + "{:1.3f}".format(vq[qp])
                        print(s)
                        fileWithLDs_hyst.write(s + "\n")

        fileWithLDs.close()
        fileWithLDs_LTC.close()
        fileWithLDs_hyst.close()
        if bPrint:
            print("print LDs to file " + sFileNameLD + "...Finished")

    def printStatistics(self, sFileName, bPrint=False, bPrintDetails=False):
        if bPrint:
            print("print statistics on markers to file " + sFileName + "...")
        fileWithGenotypes = open(sFileName, "w")
        n = len(self.vMarker)
        i = 0
        for g in self.vMarker:
            # text_file.write("Purchase Amount: %s" % TotalAmount)
            if i == 0:
                s = str(i) + "\t" + g.sStatistics(True)
                # print(s)
                fileWithGenotypes.write(s)
                fileWithGenotypes.write("\n")

            i = i + 1
            s = str(i) + "\t" + g.sStatistics()
            # print(s)
            fileWithGenotypes.write(s)
            fileWithGenotypes.write("\n")
            if bPrintDetails:
                if i % 10000 == 1:
                    print(str(i) + " of " + str(n) + " markers are printed")

        fileWithGenotypes.write("\n")
        fileWithGenotypes.write("Missing data in individuals:\n")
        fileWithGenotypes.write("i\tind\tnMissed")
        if len(self.vIndPloidy) > 0:
            fileWithGenotypes.write("\tploidy")
        fileWithGenotypes.write("\n")
        for i in range(self.nIndivids):
            s = str(i) + "\t" + self.vsInd[i] + "\t" + str(self.nMissed(i))
            # print(s)
            if len(self.vIndPloidy) > 0:
                p = self.vIndPloidy[i]
                s += "\t" + str(p)
            fileWithGenotypes.write(s)
            fileWithGenotypes.write("\n")

        fileWithGenotypes.close()
        if bPrint:
            print("print statistics on markers to file " + sFileName + "...Finished")

    def nMissed(self, iIndivid):
        # print str(iIndivid)
        n = 0
        if iIndivid < 0 or iIndivid >= self.nIndivids:
            return 0
        for g in self.vMarker:
            if g.g[iIndivid] < 0:
                n = n + 1
        return n

    def compressMarkersOfAllCtgs(self, sFileNameLog):
        bPrint = True
        bPrintDetails = True
        if bPrint:
            print("Compressing of markers by contigs...")
        genotypesNew = clGenotypes()
        genotypesNew.nIndivids = self.nIndivids
        genotypesNew.vsInd = []
        for s in self.vsInd:
            genotypesNew.vsInd.append(s)

        genotypesMM = clGenotypes()
        genotypesMM.nIndivids = self.nIndivids
        genotypesMM.vsInd = []
        for s in self.vsInd:
            genotypesMM.vsInd.append(s)

        sChrCurrent = ""
        mm = []
        i = 0
        n = len(self.vMarker)
        for m in self.vMarker:
            if m.sChr == sChrCurrent:
                mm.append(m)
            else:
                self.compressMarkersOfAllCtgs_ctg(
                    mm, sFileNameLog, genotypesNew, genotypesMM
                )
                mm = []
                sChrCurrent = m.sChr
                mm.append(m)
            i += 1
            if bPrintDetails:
                if i % 10000 == 1:
                    print(str(i) + " of " + str(n) + " markers done")
        self.compressMarkersOfAllCtgs_ctg(mm, sFileNameLog, genotypesNew, genotypesMM)
        if bPrint:
            print("Compressing of markers by contigs...Finished")

        genotypesNew.indexData = self.indexData
        genotypesMM.indexData = self.indexData
        genotypesNew.sPath = self.sPath
        genotypesMM.sPath = self.sPath
        genotypesNew.sFileName_genotypesOfGoodMarkers_inFormatChr = (
            self.sFileName_genotypesOfGoodMarkers_inFormatChr + "New.txt"
        )
        genotypesMM.sFileName_genotypesOfGoodMarkers_inFormatChr = (
            self.sFileName_genotypesOfGoodMarkers_inFormatChr + "MM.txt"
        )
        genotypesNew.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
            self.sFileName_genotypesOfNotGoodMarkers_inFormatChr + "New.txt"
        )
        genotypesMM.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
            self.sFileName_genotypesOfNotGoodMarkers_inFormatChr + "MM.txt"
        )
        return genotypesNew, genotypesMM

    def compressMarkersOfAllCtgs_ctg_sMarkerNameStart(self, sChr, iBlockOnChr, posBp):
        return sChr + "_B" + str(iBlockOnChr) + "_start" + str(posBp)

    def compressMarkersOfAllCtgs_ctg_sMarkerAddPos(self, sMarkerName, posBp):
        return sMarkerName + "," + str(posBp)

    def compressMarkersOfAllCtgs_ctg_sMarkerDeshifrate(
        self, sMarkerName
    ):  # sChr,iBlockOnChr,vPosBp=
        # NODE_99_length_95174_cov_2.74245_B1_start51631,58047,64305,64473
        ss = sMarkerName.split("_start")
        ss1 = ss[0].split("_B")
        sChr = ss1[0]  # NODE_99_length_95174_cov_2.74245
        iBlockOnChr = int(ss1[1])  # 1
        vsPosBp = ss[1].split(",")
        vPosBp = []
        for sPosBp in vsPosBp:
            vPosBp.append(int(sPosBp))
        return sChr, iBlockOnChr, vPosBp

    def compressMarkersOfAllCtgs_ctg(self, mm, sFileNameLog, genotypesNew, genotypesMM):
        # mm = list of all markers from sequence ctg
        # output:
        # genotypesNew=list of informative markers with good segregation (compressed by sequence within ctg, may be several blocks)
        # genotypesMM=list of low informative markers (only for ctg with no good markers)
        n = len(mm)
        if n == 0:
            # log shapka
            fileLog = open(sFileNameLog, "w")
            fileLog.close()
            fileLog = open(sFileNameLog, "a")
            s = "ctg" + "\t" + "length"
            s = s + "\t" + "nOk"
            s = s + "\t" + "nBlocks"
            s = s + "\t" + "dBlocksMax"
            s = s + "\t" + "dBlocks"
            s = s + "\t" + "nBad"
            s = s + "\t" + "Good"
            s = s + "\t" + "Bad"
            s += "\t" + "nTry"
            s = s + "\n"
            fileLog.write(s)
            fileLog.close()
        else:
            fileLog = open(sFileNameLog, "a")
            nMarkersExcludedByQual = 0
            nMarkersInAllBlocks = 0
            nBlocks = 0
            sMarkersExcludedByQual = ""
            mmPP = []
            mmMM = []
            vIndivids = mm[0].vIndividsAll_get()

            # mmPP = {m from mm: list of markers from sequence ctg with at least 50 non-missed and segregation close to p(0)=p(1)=0.5 (based on chi^2 test) }
            # mmMM = (mm\mmPP)n{m: min(m.nIndWithState[0],m.nIndWithState[1])>=10}
            for m in mm:
                if m.bGood():
                    mmPP.append(m)
                    nMarkersInAllBlocks += 1
                else:
                    nMarkersExcludedByQual += 1
                    if len(sMarkersExcludedByQual) > 0:
                        sMarkersExcludedByQual += ","
                    nNotMissed = m.nIndWithState[0] + m.nIndWithState[1]
                    sMarkersExcludedByQual += (
                        str(m.pos)
                        + ":"
                        + str(nNotMissed)
                        + ":"
                        + "{:1.1f}".format(m.chi2)
                        + ":"
                        + "{:1.1f}".format(m.pp)
                    )
                    if m.bMayBeInteresting():
                        mmMM.append(m)

            sMarkersInAllBlocks = ""  # string to control markers
            sdBlocks = ""  # string to control difference of marker m from current compressed genotype
            dBlocksMax = 0
            if len(mmPP) > 0:
                # no need genotypesMM.vMarker.append()

                nBlocks = 0
                dBlocksMax = 0
                mNew = (
                    clMarkerWithGenotypesOfAllIndivids()
                )  # zipper of few markers with close genotypes
                for m in mmPP:
                    bAddBlock = nBlocks == 0
                    if nBlocks > 0:
                        nE, nN, nToImprove = mNew.compareWithMarker(m, vIndivids)
                        if (nE > 0 and nN > 0) or (nE + nN < 10):
                            bAddBlock = True
                            if nBlocks > 1:
                                sdBlocks += (
                                    ","  # block will be added, hence>1, not only >2
                                )
                            if nE > 0 and nN > 0:
                                dBlock = (
                                    nN if nN <= nE else nE
                                )  # difference of marker m from current compressed genotype
                                sdBlocks += str(dBlock)
                                if dBlocksMax < dBlock:
                                    dBlocksMax = dBlock
                            else:
                                sdBlocks += "missed"
                        else:
                            if nToImprove > 0:
                                bTheSamePhase = nE > 0  # hence, nN=0 (see above)
                                mNew.improveByMarker(m, bTheSamePhase)
                            sMarkersInAllBlocks += (
                                "," + str(m.pos) + "(" + str(nToImprove) + ")"
                            )
                            # mNew.sMarker+=','+str(m.pos)
                            mNew.sMarker = (
                                self.compressMarkersOfAllCtgs_ctg_sMarkerAddPos(
                                    mNew.sMarker, m.pos
                                )
                            )

                    if bAddBlock:
                        # print "2427"
                        mNew = clMarkerWithGenotypesOfAllIndivids()
                        # sCompressedMarkerName=m.sChr+"_B"+str(nBlocks)+"_start"+str(m.pos)
                        sCompressedMarkerName = (
                            self.compressMarkersOfAllCtgs_ctg_sMarkerNameStart(
                                m.sChr, nBlocks, m.pos
                            )
                        )
                        mNew.get(m.g, self.nIndivids, sCompressedMarkerName, m.sChr, 0)
                        genotypesNew.vMarker.append(mNew)
                        if nBlocks > 0:
                            sMarkersInAllBlocks += "|"
                        sMarkersInAllBlocks += "B" + str(nBlocks) + ":" + str(m.pos)
                        nBlocks += 1
                        # print "2438"
            else:  # poka
                for m in mmMM:
                    # standartizition of allele names
                    m.sState0 = "0"
                    m.sState1 = "1"

                    genotypesMM.vMarker.append(m)

            # update log:
            s = mm[0].sChr + "\t" + str(mm[0].ctgLength)
            s = s + "\t" + str(nMarkersInAllBlocks)
            s = s + "\t" + str(nBlocks)
            s = s + "\t" + str(dBlocksMax)
            s = s + "\t" + sdBlocks
            s = s + "\t" + str(nMarkersExcludedByQual)
            s = s + "\t" + sMarkersInAllBlocks
            s = s + "\t" + sMarkersExcludedByQual
            s = s + "\t" + str(len(mmMM))
            s = s + "\n"
            fileLog.write(s)
            fileLog.close()
        genotypesNew.vsMarkerName = genotypesNew.vsMarkerName_get()

    def printNDist(self, sFileName, bPrint=False, bPrintDetails=False):
        if bPrint:
            print("print nDist for markers to file " + sFileName + "...")
        file = open(sFileName, "w")
        n = len(self.vMarker)
        d = 0.01
        nd = 20 + 1
        s = "m"
        for id in range(nd):
            s += "\t" + str(d * id)
        file.write(s + "\n")

        recVova = clRecombination()
        i = 0
        vIndividsAll = self.vMarker[0].vIndividsAll_get()
        for m in self.vMarker:
            i = i + 1
            s = m.sMarker
            dd = []
            for id in range(nd):
                dd.append(0)

            # i<2
            if True:
                j = 0
                for m1 in self.vMarker:
                    j += 1
                    nR = 0
                    nN = 0
                    if m.idType == 0 and m1.idType == 0:
                        nR, nN, nMissed = recVova.nnn(m.g, m1.g, False)
                    else:
                        nE, nNotE, nToImprove = m.compareWithMarker(
                            m1, vIndividsAll
                        )  # nE, nN, nToImprove=
                        nR = nNotE
                        nN = nE
                    r = recVova.rML(nR, nN)
                    # print(str(j)+' '+str(nR)+' '+str(nN)+' '+str(nMissed)+' '+str(r))
                    for id in range(nd):
                        if r <= d * id:
                            dd[id] += 1

            for id in range(nd):
                s += "\t" + str(dd[id])
            file.write(s + "\n")

            if bPrintDetails:
                if i % 100 == 1:
                    print(str(i) + " of " + str(n) + " markers are printed")
        file.close()
        if bPrint:
            print("print nDist for markers to file " + sFileName + "...Finished")

    def printNetPajek(
        self, sFileName, dMax=0.15, bPrint=False, bPrintDetails=False
    ):  # r<=dMax
        if bPrint:
            print("print net to file " + sFileName + "...")
        file = open(sFileName, "w")

        # *Network
        # *Vertices 3
        # 1 "pe0" ic LightGreen 0.5 0.5 box
        # 2 "pe1" ic LightYellow 0.8473 0.4981 ellipse
        # 3 "pe2" ic LightYellow 0.6112 0.8387 triangle
        # *Arcs
        # 1 2 1 c black
        # 1 3 -1 c red
        # *Edges
        # 2 3 1 c black

        n = len(self.vMarker)
        net = clNetVova()
        net.printToFilePajek__shapka(file, n)
        for i in range(n):
            # 1 "pe0" ic LightGreen 0.5 0.5 box

            # caption of node
            # s=str(i)
            s = self.vMarker[i].sMarker
            # s='\"'+s+'\"'

            # file.write(str(i+1)+" "+s+" ic Red ellipse"+'\n')
            node = net.clNode()
            node.get(
                id=i,
                index=-1,
                caption=s,
                bCoorKnown=False,
                x=0,
                y=0,
                ic="red",
                bc="black",
                shape="ellipse",
            )
            node.printToFilePajek(i + 1, file)
            # no adding to net
        net.printToFilePajek__shapkaEdges(file)
        recVova = clRecombination()
        vIndividsAll = self.vMarker[0].vIndividsAll_get()
        i = 0
        idEdge = 0
        for m in self.vMarker:
            for j in range(i + 1, n):
                m1 = self.vMarker[j]
                nR = 0
                nN = 0
                if m.idType == 0 and m1.idType == 0:
                    nR, nN, nMissed = recVova.nnn(m.g, m1.g, False)
                else:
                    nE, nNotE, nToImprove = m.compareWithMarker(
                        m1, vIndividsAll
                    )  # nE, nN, nToImprove=
                    nR = nNotE
                    nN = nE
                r = recVova.rML(nR, nN)
                # print(str(j)+' '+str(nR)+' '+str(nN)+' '+str(nMissed)+' '+str(r))
                if r <= dMax:
                    # 2 3 1 c black
                    """
                    s="black"
                    if r>0.02:
                            s="blue"
                    if r>0.05:
                            s="red"
                    if r>0.1:
                            s="LightGreen"
                    if r>0.12:
                            s="yellow"
                    file.write(str(i+1)+' '+str(j+1)+" "+'{:1.2f}'.format(r)+" c "+s+'\n')
                    """
                    e = net.clEdge()
                    e.get(idStart=i, idEnd=j, val=r, sc=e.colorGet(r), w=1)
                    e.printToFilePajek(file, i + 1, j + 1)
                    idEdge += 1
                    # no adding to net
            i += 1

            if bPrintDetails:
                if i % 100 == 1:
                    print(str(i) + " of " + str(n) + " markers are printed")
        file.close()
        if bPrint:
            print("print net to file " + sFileName + "...Finished")
        net.readFromFilePajek(sFileName, bPrint, bPrintDetails)
        return net

    def listOfMarkersIdGet(self, net, idNodes):
        names = []
        NodeCaptionsNotInList = []
        for m in self.vMarker:
            names.append(m.sMarker)
        listOfMarkersId = []
        for idNode in idNodes:
            s = net.node[idNode].caption
            if s in names:
                i = names.index(s)
                listOfMarkersId.append(i)
            else:
                NodeCaptionsNotInList.append(s)
        if len(NodeCaptionsNotInList) > 0:
            print(
                "listOfMarkersIdGet: nodes "
                + str(NodeCaptionsNotInList)
                + " are not in list "
                + str(names)
            )
        return listOfMarkersId, NodeCaptionsNotInList

    def readFileCoorPrivman(self, sFileName, sFileNameLog):
        bPrint = True
        if bPrint:
            print("readFileCoorPrivman " + sFileName + "...")
        vPrivmanCtgIndex = []
        for m in self.vMarker:
            vPrivmanCtgIndex.append(m.PrivmanCtgIndex)  # -1
        fileCoorPrivman = open(sFileName, "r")
        fileLogPrivman = open(sFileNameLog, "w")

        # chr15	8736568	[NODE_2726_POS_22248]	9	1.0:1.6	162.12
        s1 = (
            "vovaCommentAndPrivmanLG"
            + "\t"
            + "index(notInUse)"
            + "\t"
            + "markerPrivman"
            + "\t"
            + "nMissed"
            + "\t"
            + "segregation"
            + "\t"
            + "coorPrivman"
        )
        fileLogPrivman.write(s1 + "\n")

        iRow = 0
        m0 = self.vMarker[0]
        nNotGood = 0
        nCtgPrivmanNotInVova = 0
        nOk = 0
        nNotOk = 0
        vNotVova = []
        VovaMath = clVovaMath()
        for s in fileCoorPrivman:
            # if True:
            # s=fileCoorPrivman[0]
            ss = s.split("\n")  # max split = 1
            s = ss[0]
            (
                sLG,
                PrivmanCtgIndex,
                PrivmanPosOnCtg,
                nMissed,
                coor,
                bInBrackets,
                sError,
            ) = m0.readLineOfPrivman(s)
            if PrivmanCtgIndex >= 0:
                vIndices = VovaMath.vIndices_get(vPrivmanCtgIndex, PrivmanCtgIndex)
                if len(vIndices) > 0:
                    i0 = -1
                    for i in vIndices:
                        if PrivmanPosOnCtg in self.vMarker[i].vPrivmanvPosOnCtg:
                            if i0 < 0:
                                self.vMarker[i].PrivmanLG = sLG
                                self.vMarker[i].PrivmanCoorOnLG = coor
                            i0 = i
                    if i0 >= 0:
                        nOk += 1  # I have such marker in list of good
                    else:
                        # Marker is not good but I have good marker from the same sequence contig
                        nNotOk += 1
                        s1 = "nNotOk=" + str(nNotOk) + ": " + s
                        print(s1)
                        fileLogPrivman.write(s1 + "\n")
                else:
                    # I have no such ctg
                    nCtgPrivmanNotInVova += 1
                    if not (PrivmanCtgIndex in vNotVova):
                        vNotVova.append(PrivmanCtgIndex)
                    s1 = "nCtgPrivmanNotInVova=" + str(nCtgPrivmanNotInVova) + ": " + s
                    print(s1)
                    fileLogPrivman.write(s1 + "\n")
            else:
                # wrong format in Privman file
                nNotGood += 1
                s1 = "nNotGood=" + str(nNotGood) + ": " + s + "\t" + sError
                print(s1)
                fileLogPrivman.write(s1 + "\n")
            iRow += 1
        s = "nNotGood=" + str(nNotGood)
        s += ", nCtgPrivmanNotInVova=" + str(nCtgPrivmanNotInVova)
        s += ", nNotOk=" + str(nNotOk) + ", nOk=" + str(nOk)
        print(s)
        fileLogPrivman.write(s + "\n")
        s = (
            "In total, "
            + str(len(vNotVova))
            + " sequence contigs mapped on genetic map of Privman are not mapped to map of Vova:"
        )
        print(s)
        fileLogPrivman.write(s + "\n")
        vNotVova.sort()
        print(str(vNotVova))
        for v in vNotVova:
            fileLogPrivman.write(str(v) + "\n")
        fileCoorPrivman.close
        fileLogPrivman.close
        if bPrint:
            print("readFileCoorPrivman " + sFileName + "...Finished")

    def readFromVCF_compress_statistics_printInMultiQTLformat(
        self,
        sFileNameVCF,
        bPrintStatistics=False,
        bPrintGenotypes=False,
        bCompress=True,
        nOfStateMin=25,
        nReadsMinBeSureNotHeterozygote=6,
        idType=0,
    ):
        self.readFromFileVCF(
            sFileNameVCF,
            True,
            True,
            nOfStateMin,
            nReadsMinBeSureNotHeterozygote,
            idType,
        )
        if bPrintStatistics:
            sFileNameS = self.sPath + "s.txt"  # statistics for Real data
            self.printStatistics(sFileNameS, True, True)
        if bPrintGenotypes:
            # all markers after filtration based on nOfStateMin
            sFileNamePP = (
                self.sPath + "gPP_all"
            )  # Real data Eyal in MultiQTL format, all
            if not bCompress:
                sFileNamePP = self.sPath + "gPP_all_nc"
            self.printGenotypes(sFileNamePP + "_al.txt", False, True, True)  # A,C,G,T
            self.printGenotypes(sFileNamePP + "_an.txt", True, True, True)  # 0,1,2
        # if False:
        if bCompress:
            sFileNameLog = self.sPath + "log.txt"  # log
            sFileNameSpp = self.sPath + "sPP.txt"  # statistics for compressed data
            sFileNameSppmm = (
                self.sPath + "sPP_fromCtgWithNoGoods.txt"
            )  # statistics for real data from bad contigsOnly
            gg, ggMM = self.compressMarkersOfAllCtgs(sFileNameLog)
            print("--")
            print(self.sPath)
            print(self.sFileName_genotypesOfGoodMarkers_inFormatChr)
            print("--")
            gg.printGenotypes(
                self.sFileName_genotypesOfGoodMarkers_inFormatChr, True, True
            )
            gg.printStatistics(sFileNameSpp, True, True)
            ggMM.printGenotypes(
                self.sFileName_genotypesOfNotGoodMarkers_inFormatChr, True, True
            )
            ggMM.printStatistics(sFileNameSppmm, True, True)

    def vsMarkerName_get(self):
        vsMarkerName = []
        for Marker in self.vMarker:
            vsMarkerName.append(Marker.sMarker)
        return vsMarkerName

    def vIndPloidy_by_name(self, index=0):
        self.vIndPloidy = []
        if index == 0:  # Lasius
            for sInd in self.vsInd:
                # Lfu11-M9.sort	1421
                # Lfu11-W1.sort
                s = sInd[6]  # M or W
                p = -1
                if s == "M":
                    p = 1
                if s == "W":
                    p = 2
                self.vIndPloidy.append(p)


class clBuildingGeneticMap:
    def __init__(self, Genotypes, sPathOutput=""):
        self.Genotypes = Genotypes
        self.sPathOutput = sPathOutput
        if self.sPathOutput == "":
            self.sPathOutput = Genotypes.sPath
        self.bExcludeNodesCausingNonLinearClusters = False  # to simplify repeat
        self.sFileNamePajek = ""  # self.sPathOutput+"netPajek.net"
        self.sFileNamePajekPP = ""  # self.sPathOutput+"netPajekPP.net"
        self.bCoorPrivman = False
        self.index = 0

        self.vLG = []
        self.setParam()

    def setParam(self):
        if self.index == 0:
            # 117 males
            self.bNodeTest = True
            self.bEdgeTest = False
            self.NodeTest_cutoff = 0.15
            self.NodeTest_cutoffParallel = 0.25
            self.cutoffVerticesLinked = self.NodeTest_cutoff
            self.Net_cutoff = 0.2
            self.Clustering_cutoff = 0.15
        if self.index == 1:
            # campanotus
            self.bNodeTest = True
            self.bEdgeTest = True
            self.NodeTest_cutoff = 0.15
            self.NodeTest_cutoffParallel = 0.25
            self.cutoffVerticesLinked = 0.1
            self.Net_cutoff = 0.25  # 0.21
            self.Clustering_cutoff = 0.25  # 0.15#0.25#0.21

    def startStandard(self, bFirst, dMax=0.25):
        sdMax = str(int(dMax * 100 + 0.000001))  # 0.25->"25"
        self.sFileNamePajek = self.sPathOutput + "PajekAll0p" + sdMax + ".txt"
        self.sFileNamePajekPP = self.sPathOutput + "PajekAll0p" + sdMax + "_pp.txt"
        if bFirst:  # if False:
            self.Genotypes.printGenotypes(
                self.sPathOutput + "g.txt", True, True, True, False
            )  # 0,1,2
            self.Genotypes.printGenotypes(
                self.sPathOutput + "gMSTformat.txt", False, True, True, True
            )  # 0,1,2
            # x=1/0
            sFileNameS = self.sPathOutput + "s.txt"  # statistics for Real data
            self.Genotypes.printStatistics(sFileNameS, True, True)
            # x=1/0
            sFileNameD = self.sPathOutput + "distMatrix.txt"
            self.Genotypes.printNDist(sFileNameD, True, True)
            # x=1/0
            self.Genotypes.printNetPajek(self.sFileNamePajek, dMax, True, True)
            # NB! to view this file in my program (Visual Basic LTC) need to add manually number of edges and change .txt to .net
            # x=1/0

        # self.bNodeTest=False
        # self.bEdgeTest=False

        self.buildGeneticMap()
        vLG = self.vLG
        print("nLG=" + str(len(vLG)))
        for LG in vLG:
            print(LG.name + ": nM=" + str(LG.nMarkers))

    def buildGeneticMap(self):
        net = clNetVova()
        bPrintClusters = not self.bExcludeNodesCausingNonLinearClusters

        clusters, inCluster = net.makeLinearContigClusters(
            self.bExcludeNodesCausingNonLinearClusters,
            self.sFileNamePajek,
            self.sFileNamePajekPP,
            self.sPathOutput,
            bPrintClusters,
            self.bNodeTest,
            self.bEdgeTest,
            self.NodeTest_cutoff,
            self.NodeTest_cutoffParallel,
            self.cutoffVerticesLinked,
            self.Net_cutoff,
            self.Clustering_cutoff,
        )

        # cutoffToProcess >= Clustering_cutoff
        cutoffToProcess = self.Clustering_cutoff

        # idType=0
        # self.readFromFileSimple(sFileNamePPPP,False,'',idType,True,False)
        if self.bCoorPrivman:
            sFileNamePrivmanMap = "C:\\Frenkel\\Privman\\GeneticMapping\\Cataglyphis_117males\\Cnig_gn2.concatScaf2ChrByMap.3.map"
            self.Genotypes.readFileCoorPrivman(
                sFileNamePrivmanMap, sFileNamePrivmanMap + "_Log.txt"
            )
        # vLG=self.processClusters(net,cutoffToProcess,[clusters[0]],self.sPathOutput)#only first cluster
        # vLG=self.processClusters(net,cutoffToProcess,clusters[0:2],self.sPathOutput)
        self.vLG = self.processClusters(
            net, cutoffToProcess, clusters, self.sPathOutput
        )

    def processClusters(self, net, cutoffToProcess, clusters, sPath):
        n = len(clusters)
        bPrint = True
        bPrintDetails = False
        if n < 2:
            bPrintDetails = True
        if bPrint:
            print("")
            print("processClusters for " + str(n) + " clusters...")
            print("")
        vLG = []
        vNodeCaptionsNotInList_LG = []
        for i in range(n):
            bFirst = i == 0
            net1 = net.subnet(clusters[i], cutoffToProcess)  # 0.2)
            # print("ne1="+str(len(net1.node[0].edges)))
            # net1.printToFilePajek(sFileNamePajekPPPP,0.2,True,True)
            # print("ne2="+str(len(net1.node[0].edges)))
            # net2=net1.MST(bPrint=True,bPrintDetails=False)
            # sFileNamePajekMST=sPath+"netPajekMST.net"#Pajek
            # net2.printToFilePajek(sFileNamePajekMST,0.2,True,True)
            # net2.calcRanksOfNodes(0,True)
            idNodesPath = net1.idNodesOnPathLongest(bPrint, bPrintDetails)

            sNameLG = "LG" + str(i + 1)
            LG, NodeCaptionsNotInList_LG = self.LG_get(net1, idNodesPath, sNameLG, i)
            vNodeCaptionsNotInList_LG.append(NodeCaptionsNotInList_LG)

            # sFileName=sPath+sNameLG+".txt"
            # LG.printToFile(sFileName,bGenotype=True,bGenotypePhased=True,bAppend=False)
            LG.jumpsOfIndividuals(bPrint, bPrintDetails, sPath, bFirst)

            # all individs
            vIndivids = self.Genotypes.vMarker[0].vIndividsAll_get()

            LG.coorForPath(sPath + "PathCoorControl.txt", vIndivids, bFirst)

            # LG.testMapVsObsRec_pathOnly(sPath)

            LG.coorForNotPath(vIndivids)
            LG.vLGmarkerOrderedByCoorOnLG_make()

            sFileName = sPath + "CoorControl.txt"
            LG.printToFile(sFileName, True, True, bFirst)
            if bPrint:
                print(
                    "processClusters for " + str(n) + " clusters...iCluster=" + str(i)
                )
                print("")
            vLG.append(LG)
        if bPrint:
            print("")
            print("processClusters for " + str(n) + " clusters...Finished")

            n = 0
            for NodeCaptionsNotInList_LG in vNodeCaptionsNotInList_LG:
                n += len(NodeCaptionsNotInList_LG)
            s = (
                "no"
                if n == 0
                else format(n) + " markers: " + str(vNodeCaptionsNotInList_LG)
            )
            print("markers presented in net but not in genotypes: " + s)
            print()
        return vLG

    def LG_get(self, net, idNodesPath, sNameLG, idSet):
        idNodesLG = []
        for i in range(net.nNodes):
            idNodesLG.append(i)

        LG = clLinkageGroup()
        LG.id = idSet
        LG.name = sNameLG
        ii, NodeCaptionsNotInList_LG = self.Genotypes.listOfMarkersIdGet(net, idNodesLG)
        iii, NodeCaptionsNotInList_Path = self.Genotypes.listOfMarkersIdGet(
            net, idNodesPath
        )
        for i in ii:
            m = self.Genotypes.vMarker[i]
            LG.addMarker(m)
        LG.idOnLG_path = []
        LG.nIdOnLG_path = 0
        for i in iii:
            idOnLG = ii.index(i)
            # LG.idOnLG_path[LG.nIdOnLG_path]=idOnLG
            LG.idOnLG_path.append(idOnLG)
            LG.nIdOnLG_path += 1
            LG.vLGmarker[idOnLG].indexOnPath = LG.nIdOnLG_path
        LG.phaseSet()
        return LG, NodeCaptionsNotInList_LG


class clDataAnts:
    def __init__(self, Genotypes_set):
        self.Genotypes = Genotypes_set

        # array to simplify search in self.vInd()
        self.vsIndStandard = (
            []
        )  # names of all individuals (not only presented in self.Genotypes). NB! first - individuals with genotypes, after them all others

        # array to simplify search in self.vColony()
        self.vsColonyName = []

        self.vInd = []
        self.vColony = []
        self.vTrait = []

    class clInd:
        def __init__(self):
            self.id = -1
            self.colony = -1  # clColony()
            self.sIndStandard = ""  # sample_1_14.a or colony10
            self.nMissingData = 0
            self.bGenotype = False
            self.bTraits = False

    class clColony:
        def __init__(self):
            self.id = -1
            self.name = ""
            self.nInds = 0
            self.vInd = []
            self.bAveCalculated = False
            self.pp_ave = -1
            self.Hobs_ave = -1
            self.Hexp_ave = -1
            self.F_IT_ave = -1

        def idIndInColony_Smallest_nMissingData(self):
            idIndInColony = 0
            v0 = self.vInd[0].nMissingData
            bGenotype = self.vInd[0].bGenotype
            for i in range(self.nInds):
                if self.vInd[i].bGenotype:
                    v = self.vInd[i].nMissingData
                    b = not (bGenotype)
                    if not (b):
                        b = v < v0
                    if b:
                        idIndInColony = i
                        v0 = v
            return idIndInColony

        def vIndividsID_get(self, bWithGenotypeOnly, bWithTraitsOnly):
            vIndividsID = []
            for Ind in self.vInd:
                b = True
                if bWithGenotypeOnly:
                    b = Ind.bGenotype
                if b:
                    if bWithTraitsOnly:
                        b = Ind.bTraits
                if b:
                    vIndividsID.append(Ind.id)
            return vIndividsID

        def F_IT_make(self, Genotypes):
            vIndividsID = self.vIndividsID_get(True, False)
            im = 0
            vpp = []
            vHe_obs = []
            vHe_exp = []
            vF_IT = []
            for m in Genotypes.vMarker:
                vn, n = m.vnAlleleCombination(vIndividsID)
                n, pp, He_obs, He_exp, F_IT = m.n_pp_Hobs_Hexp_F_IT(vn)
                vpp.append(pp)
                vHe_obs.append(He_obs)
                vHe_exp.append(He_exp)
                vF_IT.append(F_IT)
                im += 1
            VovaMath = clVovaMath()

            self.pp_ave = VovaMath.mean(vpp)
            self.Hobs_ave = VovaMath.mean(vHe_obs)
            self.Hexp_ave = VovaMath.mean(vHe_exp)
            self.F_IT_ave = VovaMath.mean(vF_IT)
            self.bAveCalculated = True

        def sText(self):  # s=
            s = (
                "Colony id="
                + str(self.id)
                + " ("
                + self.name
                + "): n="
                + str(self.nInds)
            )
            iArgMin = self.idIndInColony_Smallest_nMissingData()
            s += ", iArgMin=" + str(iArgMin)
            if self.bAveCalculated:
                s += ", pp_ave=" + str(self.pp_ave)
                s += ", Hobs_ave=" + str(self.Hobs_ave)
                s += ", Hexp_ave=" + str(self.Hexp_ave)
                s += ", F_IT_ave=" + str(self.F_IT_ave)
            return s

    def addNewInd(self, sIndStandard, bGenotype, bTraits):
        iInd = len(self.vsIndStandard)
        self.vsIndStandard.append(sIndStandard)
        ant = self.clInd()
        ant.id = iInd
        ant.sIndStandard = sIndStandard

        # sColonyName
        sColonyName = sIndStandard
        ss = sIndStandard.split("_")
        if len(ss) > 1:
            sColonyName = ss[1]

        # ant.colony
        if sColonyName in self.vsColonyName:
            ant.colony = self.vColony[self.vsColonyName.index(sColonyName)]
        else:
            ant.colony = self.clColony()
            ant.colony.id = len(self.vsColonyName)
            ant.colony.name = sColonyName
            self.vsColonyName.append(sColonyName)
            self.vColony.append(ant.colony)
        ant.colony.nInds += 1
        ant.colony.vInd.append(ant)

        ant.bGenotype = bGenotype
        ant.bTraits = bTraits
        self.vInd.append(ant)

    def readFromFile_indNames(self, sFileName):
        f = open(sFileName, "r")
        ng = self.Genotypes.nIndivids
        for s in f:  # indeed, only one row

            # ss
            ss = s.split("\n")  # max split = 1
            if len(ss) > 0:
                s = ss[0]
            ss = s.split("\t")

            # add individuals
            self.vsIndStandard = []
            for sIndStandard in ss:
                bGenotype = len(self.vsIndStandard) < ng
                bTraits = False  # poka
                self.addNewInd(sIndStandard, bGenotype, bTraits)
        f.close

    def print_nMissinData(self):
        print("ind" + "\t" + "nMissingData" + "\t" + "bGenotype" + "\t" + "bTraits")
        for Ind in self.vInd:
            print(
                Ind.sIndStandard
                + "\t"
                + str(Ind.nMissingData)
                + "\t"
                + str(Ind.bGenotype)
                + "\t"
                + str(Ind.bTraits)
            )

    def nMissingData_make(self, bPrint=True, bPrintDetails=True):
        n = len(self.vInd)
        print("n of ind names = " + str(n))
        im = 0
        for m in self.Genotypes.vMarker:
            i = 0
            for a in m.g:
                if i >= n:
                    print("im=" + str(im))
                    print("len(g)=" + str(len(m.g)))
                    print("i=" + str(i) + ">=n=" + str(n))
                if a < 0:
                    self.vInd[i].nMissingData += 1
                i += 1
            im += 1
        if bPrint:
            self.print_nMissinData()
        self.printColonies(bPrintDetails)

    def printColonies(self, bCalculateF_IT):
        vpp = []
        vHe_obs = []
        vHe_exp = []
        vF_IT = []
        vvIndividsID = []
        print("")
        for Colony in self.vColony:
            if bCalculateF_IT:
                Colony.F_IT_make(self.Genotypes)
                vpp.append(Colony.pp_ave)
                vHe_obs.append(Colony.Hobs_ave)
                vHe_exp.append(Colony.Hexp_ave)
                vF_IT.append(Colony.F_IT_ave)

            vIndividsID = Colony.vIndividsID_get(False, False)
            vIndividsID_g = Colony.vIndividsID_get(True, False)
            vIndividsID_t = Colony.vIndividsID_get(False, True)
            vIndividsID_gt = Colony.vIndividsID_get(True, True)
            vvIndividsID.append(vIndividsID_g)

            print(Colony.sText())

            for Ind in Colony.vInd:
                print(Ind.sIndStandard + "\t" + str(Ind.nMissingData))

        if bCalculateF_IT:
            VovaMath = clVovaMath()

            pp_ave = VovaMath.mean(vpp)
            Hobs_ave = VovaMath.mean(vHe_obs)
            Hexp_ave = VovaMath.mean(vHe_exp)
            F_IT_ave = VovaMath.mean(vF_IT)
            s = "by all " + str(len(self.vColony)) + " colonies:"
            s += " pp_ave=" + str(pp_ave)
            s += " Hobs_ave=" + str(Hobs_ave)
            s += " Hexp_ave=" + str(Hexp_ave)
            s += " F_IT_ave=" + str(F_IT_ave)
            print(s)

            vIndividsID_totalPop = self.Genotypes.vMarker[0].vIndividsAll_get()
            pop_All = self.subpop_get(vIndividsID_totalPop, "Total population")
            pop_All.F_IT_make(self.Genotypes)
            print(pop_All.sText())

            print(str(vvIndividsID))

            vF_ST = []
            vF_IS = []
            im = 0
            for m in self.Genotypes.vMarker:
                F_ST, F_IS = m.F_ST_and_F_IS(vvIndividsID)
                vF_ST.append(F_ST)
                vF_IS.append(F_IS)
                im += 1
                if im < 10:
                    print(str(im))
            F_ST_ave = VovaMath.mean(vF_ST)
            F_IS_ave = VovaMath.mean(vF_IS)
            #
            s = "F_ST_Total_ave=" + str(F_ST_ave)
            print(s)
            s = "F_IS_Total_ave=" + str(F_IS_ave)
            print(s)

    def vIndividsID_Smallest_nMissingData(self, bPrint=True):
        vIndividsID = []
        if bPrint:
            print("")
            print("vIndividsID_Smallest_nMissingData:")
            print("bestInd: nMissing")
        for Colony in self.vColony:
            idIndInColony = Colony.idIndInColony_Smallest_nMissingData()
            Ind = Colony.vInd[idIndInColony]
            id = Ind.id
            vIndividsID.append(id)
            if bPrint:
                print(
                    self.vInd[id].sIndStandard + ": " + str(self.vInd[id].nMissingData)
                )
        return vIndividsID

    def subpop_get(self, vIndividsID, sName):
        pop = self.clColony()
        pop.name = sName
        for id in vIndividsID:
            ant = self.vInd[id]
            pop.nInds += 1
            pop.vInd.append(ant)
        pop.F_IT_make(self.Genotypes)
        return pop

    def vTrait_ants(self, vsIndName, vsTraitName, vvbVal, vvVal):
        print("Individuals with trait, without genotypes:")
        n = 0
        for sIndName in vsIndName:
            iInd = -1
            if sIndName in self.vsIndStandard:
                iInd = self.vsIndStandard.index(sIndName)
                self.vInd[iInd].bTraits = True
            else:
                bGenotype = False
                bTraits = True
                self.addNewInd(sIndName, bGenotype, bTraits)
                n += 1
                print(sIndName)
        print("n=" + str(n))

        print("Individuals with genotypes, without trait:")
        n = 0
        for ant in self.vInd:
            if not (ant.bTraits):
                print(ant.sIndStandard)
                n += 1
        print("n=" + str(n))

        self.vTrait = []
        iTrait = 0
        for sTraitName in vsTraitName:
            Trait = clTrait()
            Trait.name = sTraitName
            Trait.nIndivids = len(self.vsIndStandard)
            Trait.valAllInds = []
            Trait.bVal = []
            Trait.nVal = 0
            for iInd in range(Trait.nIndivids):
                Trait.valAllInds.append(-1)
                Trait.bVal.append(False)

            iIndTrait = 0
            for sIndName in vsIndName:
                # iInd=-1
                # if sIndName in self.vsIndStandard:
                iInd = self.vsIndStandard.index(sIndName)
                if vvbVal[iIndTrait][iTrait]:
                    Trait.valAllInds[iInd] = vvVal[iIndTrait][iTrait]
                    Trait.bVal[iInd] = True
                    Trait.nVal += 1
                iIndTrait += 1
            self.vTrait.append(Trait)
            iTrait += 1

    def printTraitsOrderingByColonyAverageOrderingByVal(self, sPath):
        file = open(sPath + "TraitsOrderedByVova.txt", "w")
        VovaMath = clVovaMath()

        s = (
            "iTrait"
            + "\t"
            + "Trait"
            + "\t"
            + "iColonyOrdered"
            + "\t"
            + "iInColonyOrdered"
            + "\t"
            + "Ind"
            + "\t"
            + "val"
            + "\t"
            + "valAveColony"
            + "\t"
            + "valAveAll"
        )
        file.write(s + "\n")

        iTrait = 0
        for Trait in self.vTrait:
            iTrait += 1

            # trait_valAveAll
            vValAll = []
            i = 0
            for Ind in self.vInd:
                if Ind.bTraits:
                    if Trait.bVal[i]:
                        vValAll.append(Trait.valAllInds[i])
                i += 1
            trait_valAveAll = VovaMath.mean(vValAll)

            # vTrait_valColony
            vTrait_valColony = []
            for Colony in self.vColony:
                vVal = []
                for Ind in Colony.vInd:
                    i = Ind.id
                    if Ind.bTraits:
                        if Trait.bVal[i]:
                            vVal.append(Trait.valAllInds[i])
                trait_valAveColony = VovaMath.mean(vVal)
                vTrait_valColony.append(trait_valAveColony)

            vq = []
            for Colony in self.vColony:
                iColony = Colony.id
                iInColonyWithData = 0
                # print str(iColony)
                for Ind in Colony.vInd:
                    i = Ind.id
                    # print "ind:"+str(i)
                    if Ind.bTraits:
                        # print "->2779"
                        if Trait.bVal[i]:
                            q = [
                                iColony,
                                iInColonyWithData,
                                Ind.sIndStandard,
                                Trait.valAllInds[i],
                                vTrait_valColony[iColony],
                            ]
                            vq.append(q)
                            iInColonyWithData += 1

            def MyFunc(q):
                return q[4] * 10000 + q[3]

            vq.sort(key=MyFunc)
            for q in vq:
                s = str(iTrait) + "\t" + Trait.name
                s += (
                    "\t"
                    + str(q[0])
                    + "\t"
                    + str(q[1])
                    + "\t"
                    + str(q[2])
                    + "\t"
                    + str(q[3])
                )
                s += "\t" + str(q[4]) + "\t" + str(trait_valAveAll)
                file.write(s + "\n")
        file.close()

        # fileR=open(sPath+"TraitsOrderedByVovaR.txt",'w')
        # fileR.close()
        pass

    def saveTraitsOfQTLmalesInFormatOfGWAS(self, vsTraitName_GWAS, sPath, index):
        sFileName_QTL = ""
        sFileNameTraitsQTLinFormatGWAS = ""
        iCol = -1
        if index == 0:
            sFileName_QTL = (
                "C:\\Frenkel\\Privman\\QTL\\allTraits\\allTraits.Original_vova.tra"
            )
            sFileNameTraitsQTLinFormatGWAS = (
                sPath + "TraitsQTLinFormatGWAS_original.txt"
            )
            iCol = 4
        if index == 1:
            sFileName_QTL = "C:\\Frenkel\\Privman\\QTL\\allTraits\\Transformed.Traits Data_merged_vova.txt"
            sFileNameTraitsQTLinFormatGWAS = (
                sPath + "TraitsQTLinFormatGWAS_tranformed.txt"
            )
            iCol = 6
        if index == 2:
            sFileName_QTL = "C:\\Frenkel\\Privman\\QTL\\allTraits\\MultiQTL Input Data X10000 and transformed_merged_vova.txt"
            sFileNameTraitsQTLinFormatGWAS = (
                sPath + "TraitsQTLinFormatGWAS_tranformed_DataX10000.txt"
            )
            iCol = 8

        Trait = clTrait()
        vTraitQTL = Trait.vTraitFromFile(sFileName_QTL)

        vsNameQTL = []
        vsNameGWAS = []
        sFileName_traitRename = (
            "C:\\Frenkel\\Privman\\GWAS\\ind\\traitNamesVariations.txt"
        )
        f = open(sFileName_traitRename, "r")
        for s in f:
            # ss
            ss = s.split("\n")  # max split = 1
            if len(ss) > 0:
                s = ss[0]
            ss = s.split("\t")

            # iAll	iGWAS	GWAS_data	iQTL	QTL_data	iQTLtransf	QTL_datatransformed	i	MultiQTL Input Data X10000 and transformed	iQTL	Paper_QTL	Chemestry
            # 2	3	C25m3	2	TC25Me3	1	TC25Me3	1	TC25Me3	2	3Me-C25	3-MeC25

            vsNameGWAS.append(ss[2])
            vsNameQTL.append(ss[iCol])
        f.close

        file = open(sFileNameTraitsQTLinFormatGWAS, "w")

        # shapka
        s = "male"
        for Trait in self.vTrait:
            s += "\t" + Trait.name
        file.write(s + "\n")

        # vIndexInQTL
        vIndexInQTL = []
        for Trait in self.vTrait:
            IndexInQTL = -1
            if Trait.name in vsNameGWAS:
                IndexInQTL = vsNameGWAS.index(Trait.name)
                sNameQTL = vsNameQTL[IndexInQTL]

                if len(sNameQTL) < 2:
                    print(
                        "strange name of QTL trait: <"
                        + str(sNameQTL)
                        + "> for GWAS trait"
                        + Trait.name
                    )
                IndexInQTL = -1
                i = 0
                for TraitQTL in vTraitQTL:
                    if TraitQTL.name == sNameQTL:
                        IndexInQTL = i
                    i += 1
                print(Trait.name + " -> " + sNameQTL + " index=" + str(IndexInQTL))
                if IndexInQTL < 0:
                    print(
                        "strange name of QTL trait: <"
                        + str(sNameQTL)
                        + "> for GWAS trait"
                        + Trait.name
                        + " ---> -1"
                    )
            else:
                print("strange name of GWAS trait: <" + str(Trait.name) + ">")
            vIndexInQTL.append(IndexInQTL)

        nMales = vTraitQTL[0].nIndivids
        for i in range(nMales):
            s = "male_" + str(i)
            it = 0
            for Trait in self.vTrait:
                s1 = "NA"
                itpp = vIndexInQTL[it]
                if itpp >= 0:
                    if vTraitQTL[itpp].bVal[i]:
                        s1 = str(vTraitQTL[itpp].valAllInds[i])
                s += "\t" + s1
                it += 1
            file.write(s + "\n")
        file.close()


class clLinkageGroup:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.vLGmarker = []
        self.nMarkers = 0
        self.idOnLG_path = []
        self.nIdOnLG_path = 0
        self.vLGmarkerOrderedByCoorOnLG = []

    class clMarkerOfLG:
        def __init__(self):
            self.LGid = -1
            self.idOnLG = -1
            self.m = clMarkerWithGenotypesOfAllIndivids()
            self.indexOnPath = -1
            self.coorOnLG = -1
            self.idOnLG_closestOnPath = -1

        def s_get(self, bShapka, bGenotype, bGenotypePhased):
            s = "marker"
            if not bShapka:
                s = self.m.sMarker

            if bGenotype:
                if bGenotypePhased:
                    if bShapka:
                        s += "\tgenotypePhased"
                    else:
                        if self.m.phase == 0:
                            s += "\t" + self.m.sg("")
                        else:
                            m = self.m
                            m1 = clMarkerWithGenotypesOfAllIndivids()
                            m1.get(m.g, m.nIndivids, m.sMarker, m.sChr, m.pos)
                            for i in range(m.nIndivids):
                                if m1.g[i] >= 0:
                                    m1.g[i] = 1 - m1.g[i]  # 0 <->1
                            s += "\t" + m1.sg("")
                else:
                    if bShapka:
                        s += "\tgenotype"
                    else:
                        s += "\t" + self.m.sg("")

            if bShapka:
                s += "\tphase"
            else:
                s += "\t" + str(self.m.phase)

            if bShapka:
                s += "\tidOnLG"
            else:
                s += "\t" + str(self.idOnLG)

            if bShapka:
                s += "\tindexOnPath"
            else:
                s += "\t" + str(self.indexOnPath)

            if bShapka:
                s += "\tcoorOnLG"
            else:
                s += "\t" + "{:1.2f}".format(self.coorOnLG)

            if bShapka:
                s += "\tidOnLG_closestOnPath"
            else:
                s += "\t" + str(self.idOnLG_closestOnPath)

            if bShapka:
                s += "\tLG_privman\tcoor_privman"
            else:
                s += (
                    "\t"
                    + self.m.PrivmanLG
                    + "\t"
                    + "{:1.2f}".format(self.m.PrivmanCoorOnLG)
                )

            return s

    def printToFile(self, sFileName, bGenotype=True, bGenotypePhased=True, bFirst=True):
        o = "a"
        if bFirst:
            o = "w"
        file = open(sFileName, o)
        if bFirst:
            file.write(
                "LG"
                + "\t"
                + self.vLGmarker[0].s_get(True, bGenotype, bGenotypePhased)
                + "\n"
            )
        for LGmarker in self.vLGmarkerOrderedByCoorOnLG:
            file.write(
                self.name
                + "\t"
                + LGmarker.s_get(False, bGenotype, bGenotypePhased)
                + "\n"
            )
        file.close()

    def addMarker(self, m):
        mPP = self.clMarkerOfLG()
        mPP.idOnLG = self.nMarkers
        mPP.m = m
        mPP.LGid = self.id
        self.vLGmarker.append(mPP)
        self.nMarkers += 1

    def phaseSet_path(self, vIndivids):
        bStart = True
        i = self.idOnLG_path[0]
        mPrev = self.vLGmarker[i].m  # self.vMarker[listOfMarkersId[0]]
        for i in self.idOnLG_path:
            m = self.vLGmarker[i].m
            if bStart:
                bStart = False
                n0 = m.nIndWithState[0]
                n1 = m.nIndWithState[1]
                if n0 >= n1:
                    m.phase = 0
                else:
                    m.phase = 1
            else:
                m.phaseSetAccordingToCloseMarker(mPrev, vIndivids)
            mPrev = m

    def phaseSet(self):
        m = self.vLGmarker[0].m
        vIndivids = m.vIndividsAll_get()
        self.phaseSet_path(vIndivids)
        recVova = clRecombination()
        vIndividsAll = self.vLGmarker[0].m.vIndividsAll_get()
        for mLG in self.vLGmarker:
            if mLG.indexOnPath < 0:
                m = mLG.m

                # mLG.idOnLG_closestOnPath
                d = -1
                for i in self.idOnLG_path:
                    mLG1 = self.vLGmarker[i]
                    m1 = mLG1.m
                    nR, nN, nMissed = recVova.nnn(m.g, m1.g, False)
                    r = recVova.rML(nR, nN)
                    if d < 0:
                        d = r
                        mLG.idOnLG_closestOnPath = mLG1.idOnLG
                    else:
                        if d > r:
                            d = r
                            mLG.idOnLG_closestOnPath = mLG1.idOnLG

                # phaseSet
                i = mLG.idOnLG_closestOnPath
                mLG1 = self.vLGmarker[i]
                m1 = mLG1.m
                m.phaseSetAccordingToCloseMarker(m1, vIndivids)

    def jumpsOfIndividuals(self, bPrint, bPrintDetails, sPath, bFirst):
        if bPrint:
            print("jumpsOfIndividuals for " + self.name + "...")

        sFileName = sPath + "jumpsOfIndividuals.txt"
        o = "a"
        if bFirst:
            o = "w"
        fileLog = open(sFileName, o)
        if bFirst:
            s = "individ" + "\tnMarkersShortestSeq" + "\tnMissedMarkersOnPath"
            s += "\tvLenNoRec" + "\tvLenGaps"
            fileLog.write("LG\t" + s + "\n")
            if bPrint:
                print(s)

        blocks = []
        n = self.vLGmarker[0].m.nIndivids
        nn = 0
        nr = 0
        for i in range(n):
            b = []
            gaps = []
            currentBlockSize = 0
            currentGapSize = 0
            nMissed = 0
            state = -1
            mStart = -1
            mEnd = -1
            j = 0
            nm = len(self.idOnLG_path)
            for idOnLG in self.idOnLG_path:
                m = self.vLGmarker[idOnLG].m
                a = m.aPhased(i)
                if a < 0:
                    nMissed += 1
                    currentGapSize += 1
                else:
                    if mStart < 0:
                        mStart = j
                    if state >= 0:
                        if a != state:
                            b.append(currentBlockSize)
                            gaps.append(currentGapSize)
                            currentBlockSize = 0
                        currentGapSize = 0
                    state = a
                    currentBlockSize += 1
                    mEnd = j
                j += 1
            if currentBlockSize > 0:
                b.append(currentBlockSize)
            nMin = -1
            if len(b) > 0:
                nMin = min(b)
            bb = [nMin, nMissed, b, gaps]

            s = str(i) + "\t" + str(nMin) + "\t" + str(nMissed)
            s += "\t" + str(b) + "\t" + str(gaps)
            fileLog.write(self.name + "\t" + s + "\n")
            if bPrintDetails:
                print(s)

            blocks.append(bb)
            if mEnd - mStart > 0:
                if mEnd - mStart > 0.7 * nm or len(b) > 1:
                    nn += 1
                    nr += len(b) - 1
        averageNumberOfCrossingoversPerLG = float(nr) / nn if nn > 0 else -1
        s = (
            "nInterestingIndivids="
            + str(nn)
            + ", averageNumberOfCrossingoversPerLG="
            + str(averageNumberOfCrossingoversPerLG)
        )
        fileLog.write(self.name + "\t" + s + "\n")
        fileLog.close()
        if bPrint:
            print(s)
            print("jumpsOfIndividuals for " + self.name + "...Finished")

    def aOfInterval(self, i, indexOnPath, idOnLG_pathMy):
        # i - individ
        # indexOnPath=0 - before first on pathMy
        # indexOnPath=len(idOnLG_pathMy) - after the last marker on pathMy
        # a0
        a0 = -1
        if indexOnPath > 0:
            indexOnPath1 = indexOnPath - 1
            idOnLG = idOnLG_pathMy[indexOnPath1]
            a0 = self.vLGmarker[idOnLG].m.aPhased(i)
            while a0 < 0 and indexOnPath1 > 0:
                indexOnPath1 -= 1
                idOnLG = idOnLG_pathMy[indexOnPath1]
                a0 = self.vLGmarker[idOnLG].m.aPhased(i)
        # a1
        a1 = -1
        nn = len(idOnLG_pathMy)
        if indexOnPath < nn:
            indexOnPath1 = indexOnPath
            idOnLG = idOnLG_pathMy[indexOnPath1]
            a1 = self.vLGmarker[idOnLG].m.aPhased(i)
            while a1 < 0 and indexOnPath1 < nn - 1:
                indexOnPath1 += 1
                idOnLG = idOnLG_pathMy[indexOnPath1]
                a1 = self.vLGmarker[idOnLG].m.aPhased(i)
        if a0 >= 0:
            if a1 >= 0 and a0 != a1:
                return -1
            else:
                return a0
        else:
            if a1 >= 0:
                return a1
            else:
                return -1

    def gOfInterval(self, indexOnPath, idOnLG_pathMy):
        g = []
        n = self.vLGmarker[0].m.nIndivids
        for i in range(n):
            a = self.aOfInterval(i, indexOnPath, idOnLG_pathMy)
            g.append(a)
        return g

    def vgOfInterval(self, idOnLG_pathMy):
        vg = []
        n = len(idOnLG_pathMy) + 1
        for indexOnPath in range(n):
            g = self.gOfInterval(indexOnPath, idOnLG_pathMy)
            vg.append(g)
        return vg

    def coorForPath(self, sFileName, vIndivids, bFirst):
        o = "a"
        if bFirst:
            o = "w"
        file = open(sFileName, o)
        bGenotype = True
        bGenotypePhased = True
        idOnLG = self.idOnLG_path[0]
        mmPrev = self.vLGmarker[idOnLG]

        if bFirst:
            s = mmPrev.s_get(True, bGenotype, bGenotypePhased) + "\tcoor\tr\trMax"
            file.write("LG" + "\t" + s + "\n")

        mmPrev.coorOnLG = 0
        rrr = clRecombination()

        j = 0
        nm = len(self.idOnLG_path)
        for idOnLG in self.idOnLG_path:
            mm = self.vLGmarker[idOnLG]
            sCoor = "0"
            sr = "-"
            srMax = "-"
            if j > 0:
                nNotRec, nRec, nToImprove = mm.m.compareWithMarker(mmPrev.m, vIndivids)
                # print(str(nNotRec)+" "+str(nRec))
                r = rrr.rML(nRec, nNotRec)
                sr = "{:1.3f}".format(r)
                d = rrr.distByR(r)
                mm.coorOnLG = mmPrev.coorOnLG + d
                sCoor = "{:1.2f}".format(mm.coorOnLG)
                rMax = rrr.rMax(nRec, nNotRec, 3)
                if rMax < 0.01:
                    rMax = rrr.rMaxInCaseZero(nNotRec, 0.01)
                srMax = "{:1.3f}".format(rMax)
                """
				rByDist(self, d_cM):
	def distByR(self, r):
	def rML(self,nRec,nNotRec):
	def rMin(self,nRec,nNotRec,alphaSTDV):
	def rMax(self,nRec,nNotRec,alphaSTDV):
	def rMaxInCaseZero(self,nNotRec,pZero)
				"""
            s = (
                mm.s_get(False, bGenotype, bGenotypePhased)
                + "\t"
                + sCoor
                + "\t"
                + sr
                + "\t"
                + srMax
            )
            file.write(self.name + "\t" + s + "\n")
            j += 1
            mmPrev = mm
        file.close()

    def coorForNotPath(self, vIndivids):
        idOnLG_pathMy = self.idOnLG_path
        vg = self.vgOfInterval(idOnLG_pathMy)
        rr = clRecombination()
        nn = len(vg)
        for marker in self.vLGmarker:
            if marker.indexOnPath < 0:
                idOnLG = marker.idOnLG_closestOnPath
                iBest = self.vLGmarker[idOnLG].indexOnPath
                g = vg[iBest]
                ne, nd = marker.m.compareWithGPhased(g, vIndivids)
                rMin = rr.rML(nd, ne)
                for j in range(nn):
                    g = vg[j]
                    ne, nd = marker.m.compareWithGPhased(g, vIndivids)
                    r = rr.rML(nd, ne)
                    if r < rMin:
                        rMin = r
                        iBest = j
                d0 = -1
                d1 = -1
                x0 = -1
                x1 = -1
                if iBest > 0:
                    idOnLG = idOnLG_pathMy[iBest - 1]
                    nE, nN, nToImprove = marker.m.compareWithMarker(
                        self.vLGmarker[idOnLG].m, vIndivids
                    )
                    r = rr.rML(nN, nE)
                    d0 = rr.distByR(r)
                    x0 = self.vLGmarker[idOnLG].coorOnLG
                if iBest < nn - 1:
                    idOnLG = idOnLG_pathMy[iBest]
                    nE, nN, nToImprove = marker.m.compareWithMarker(
                        self.vLGmarker[idOnLG].m, vIndivids
                    )
                    r = rr.rML(nN, nE)
                    d1 = rr.distByR(r)
                    x1 = self.vLGmarker[idOnLG].coorOnLG
                if iBest == 0:
                    marker.coorOnLG = x1 - d1
                else:
                    if iBest == nn - 1:
                        marker.coorOnLG = x0 + d0
                    else:
                        if d0 + d1 > 0:
                            marker.coorOnLG = (
                                float(d1) / (d0 + d1) * x0 + float(d0) / (d0 + d1) * x1
                            )
                        else:
                            marker.coorOnLG = 0.5 * (x0 + x1)
                if marker.coorOnLG < 0:
                    print(
                        "coorForNotPath: NB! x<0, x="
                        + str(marker.coorOnLG)
                        + ", x0="
                        + str(x0)
                        + ", x1="
                        + str(x1)
                        + ", d0="
                        + str(d0)
                        + ", d1="
                        + str(d1)
                    )

    def testMapVsObsRec_pathOnly(self, sPath):
        file = open(sPath + "distPath.txt", "w")
        file.write("i\tj\tj-i\tdMap\tdObs\tdPrivman" + "\n")
        # self.idOnLG_path=[]
        rrr = clRecombination()

        # all individs
        vIndivids = self.vLGmarker[0].m.vIndividsAll_get()
        for i in range(self.nIdOnLG_path):
            for j in range(i + 1, self.nIdOnLG_path):
                print(
                    str(i)
                    + " "
                    + str(j)
                    + " "
                    + str(self.nIdOnLG_path)
                    + ": "
                    + str(self.idOnLG_path)
                )
                i1 = self.idOnLG_path[i]
                j1 = self.idOnLG_path[j]
                dMap = self.vLGmarker[j1].coorOnLG - self.vLGmarker[i1].coorOnLG

                nNotRec, nRec, nToImprove = self.vLGmarker[j1].m.compareWithMarker(
                    self.vLGmarker[i1].m, vIndivids
                )
                # print(str(nNotRec)+" "+str(nRec))
                r = rrr.rML(nRec, nNotRec)
                dObs = rrr.distByR(r)

                dPrivman = -1
                if (
                    self.vLGmarker[j1].m.PrivmanCoorOnLG < 0
                    or self.vLGmarker[i1].m.PrivmanCoorOnLG < 0
                ):
                    pass
                else:
                    dPrivman = abs(
                        self.vLGmarker[j1].m.PrivmanCoorOnLG
                        - self.vLGmarker[i1].m.PrivmanCoorOnLG
                    )
                s = (
                    str(i)
                    + "\t"
                    + str(j)
                    + "\t"
                    + str(j - i)
                    + "\t"
                    + "{:1.2f}".format(dMap)
                    + "\t"
                    + "{:1.2f}".format(dObs)
                    + "\t"
                    + "{:1.2f}".format(dPrivman)
                )
                file.write(s + "\n")
        file.close()

    def vLGmarkerOrderedByCoorOnLG_make(self):
        vq = []
        im = 0
        for LGmarker in self.vLGmarker:
            vq.append([LGmarker.coorOnLG, im])
            im += 1

        def MyFunc(q):
            return q[0]

        vq.sort(key=MyFunc)
        # print str(vq)
        # d=1/0

        self.vLGmarkerOrderedByCoorOnLG = []
        for im in range(self.nMarkers):
            im_inNonOrdered = vq[im][1]
            LGmarker = self.vLGmarker[im_inNonOrdered]
            self.vLGmarkerOrderedByCoorOnLG.append(LGmarker)
            # print str(LGmarker.coorOnLG)
        # d=1/0


class clNetVova:
    def __init__(self):
        self.node = []
        self.edge = []
        self.nNodes = 0
        self.nEdges = 0

    class clNode:
        def __init__(self):
            self.id = -1
            self.index = -1  # e.g., marker id
            self.caption = ""
            self.bCoorKnown = False
            self.x = 0
            self.y = 0
            self.ic = "red"
            self.bc = "black"
            self.shape = "ellipse"
            self.edges = []

        def get(
            self,
            id=-1,
            index=-1,
            caption="",
            bCoorKnown=False,
            x=0,
            y=0,
            ic="red",
            bc="black",
            shape="ellipse",
        ):
            self.id = id
            self.index = index  # e.g., marker id
            self.caption = caption
            self.bCoorKnown = bCoorKnown
            self.x = x
            self.y = y
            self.ic = ic
            self.bc = bc
            self.shape = shape
            self.edges = []

        def copy(self, idSet, parent):
            myNode = parent.clNode()
            myNode.id = idSet
            myNode.index = self.index  # e.g., marker id
            myNode.caption = self.caption
            myNode.bCoorKnown = self.bCoorKnown
            myNode.x = self.x
            myNode.y = self.y
            myNode.ic = self.ic
            myNode.bc = self.bc
            myNode.shape = self.shape
            myNode.edges = []
            return myNode

        def printToFilePajek(self, iToPrint, file):
            # 1 "pe0" ic LightGreen 0.5 0.5 box
            # 1 "NODE_1000_length_42440_cov_2.75993_B0" 16.165 -0.638 sh ellipse x_fact 1 y_fact 1 ic red bc black
            s = str(iToPrint) + ' "' + self.caption + '"'
            if self.bCoorKnown:
                s += " " + str(self.x)
                s += " " + str(self.y)
            s += " sh " + self.shape
            s += " ic " + self.ic
            s += " bc " + self.bc
            file.write(s + "\n")

        def bShape(self, s):
            if s in ["box", "ellipse", "triangle"]:
                return True
            return False

        def getFromS(self, s):
            # print("read from :"+s)
            ss = s.split(" ")
            # id=self.nNodes
            id = int(ss[0]) - 1
            k = len(ss[1]) - 1
            sss = ss[1][1:k]
            sShape = "ellipse"
            sic = "red"
            sbc = "black"
            i = 0
            for s0 in ss:
                if self.bShape(s0):
                    sShape = s0
                if s0 == "sh":
                    if self.bShape(ss[i + 1]):
                        sShape = ss[i + 1]
                if s0 == "ic":
                    sic = ss[i + 1]
                if s0 == "bc":
                    sbc = ss[i + 1]
                i += 1
            self.get(
                id=id,
                index=-1,
                caption=sss,
                bCoorKnown=False,
                x=0,
                y=0,
                ic=sic,
                bc=sbc,
                shape=sShape,
            )

        def bExistEdgeToNodeID(self, idTo):
            for e in self.edges:
                if e.idStart == idTo:
                    return True
                if e.idEnd == idTo:
                    return True
            return False

    class clEdge:
        def __init__(self):
            self.id = -1
            self.idStart = -1
            self.idEnd = -1
            self.val = 1
            self.sc = "black"
            self.w = 1
            self.sp = "Solid"
            self.sl = ""

        def get(self, idStart=-1, idEnd=-1, val=1, sc="black", w=1, sp="Solid", sl=""):
            # self.id=id
            self.idStart = idStart
            self.idEnd = idEnd
            self.val = val
            self.sc = sc
            self.w = w
            self.sp = sp
            self.sl = sl

        def copy(self, idStart, idEnd, parent):
            e = parent.clEdge()
            # e.id=-1 #id
            e.idStart = idStart
            e.idEnd = idEnd
            e.val = self.val
            e.sc = self.sc
            e.w = self.w
            e.sp = self.sp
            e.sl = self.sl
            return e

        def colorGet(self, r):
            if r <= 0.01:
                return "black"
            if r <= 0.03:
                return "blue"
            if r <= 0.05:
                return "red"
            if r <= 0.1:
                return "LightGreen"
            if r <= 0.15:
                return "yellow"
            return "white"  # "LightGray"

        def printToFilePajek(self, file, idStartToPrint, idEndToPrint):
            sc = " c " + self.sc
            sc = " c " + self.colorGet(self.val)

            sv = " " + "{:1.2f}".format(self.val)

            sw = ""
            if self.w > 0:
                sw = " w " + str(self.w)

            s = str(idStartToPrint) + " " + str(idEndToPrint)
            bSimple = False
            if bSimple:
                # 2 3 1 c black
                s = s + sv + sc + sw + "\n"
            else:
                # for LTC
                # 19 182 0.15 w 1 c yellow p Solid l ""
                sv = " 1"
                sp = " p " + self.sp  # "Solid"
                sl = ' l "' + "{:1.2f}".format(self.val) + '"'
                s = s + sv + sw + sc + sp + sl + "\n"
            file.write(s)

        def getFromS(self, s):
            # already without \n
            # 2 3 1 c black w 1
            # 19 182 0.15 w 1 c yellow p Solid l ""
            ss = s.split(" ")

            sc = "black"
            ww = 1
            sp = "Solid"
            sl = ""
            i = 0
            for s0 in ss:
                if s0 == "c":
                    sc = ss[i + 1]
                if s0 == "w":
                    ww = int(ss[i + 1])
                if s0 == "p":
                    sp = ss[i + 1]
                if s0 == "l":
                    k = len(ss[i + 1]) - 1
                    if k > 0:
                        sl = ss[i + 1][1:k]
                i += 1
            v = float(ss[2])
            if v == 1 and len(sl) > 0:
                v = float(sl)
            self.get(
                idStart=int(ss[0]) - 1,
                idEnd=int(ss[1]) - 1,
                val=v,
                sc=sc,
                w=ww,
                sp="Solid",
                sl=sl,
            )

        def idNodeEnd(self, iBegin):
            if self.idStart == iBegin:
                return self.idEnd
            else:
                if self.idEnd == iBegin:
                    return self.idStart
                else:
                    print(
                        "idNodeEnd: iBegin="
                        + str(iBegin)
                        + ", s="
                        + str(self.idStart)
                        + ", e="
                        + str(self.idEnd)
                    )
                    return -1

        def sort2(self, a, b):
            if a <= b:
                return a, b
            else:
                return b, a

        def s_shapka_get(self):
            s = (
                "id"
                + "\t"
                + "caption"
                + "\t"
                + "val"
                + "\t"
                + "idStart"
                + "\t"
                + "idEnd"
                + "\t"
                + "Start"
                + "\t"
                + "End"
            )
            return s

        def s_get(self, NetVova):
            s = (
                str(self.id)
                + "\t"
                + self.sl
                + "\t"
                + str(self.val)
                + "\t"
                + str(self.idStart)
                + "\t"
                + str(self.idEnd)
                + "\t"
                + NetVova.node[self.idStart].caption
                + "\t"
                + NetVova.node[self.idEnd].caption
            )
            return s

    def addNode(
        self,
        id=-1,
        index=-1,
        caption="",
        bCoorKnown=False,
        x=0,
        y=0,
        ic="red",
        bc="black",
        shape="ellipse",
    ):
        v = self.clNode()
        v.get(id, index, caption, bCoorKnown, x, y, ic, bc, shape)
        self.node.append(v)
        self.nNodes += 1

    def addNodeFromS(self, s):
        v = self.clNode()
        v.getFromS(s)
        self.node.append(v)
        self.nNodes += 1

    def printToFilePajek__shapka(self, file, nNodesToPrint):
        file.write("*Network" + "\n")
        file.write("*Vertices " + str(nNodesToPrint) + "\n")

    def printToFilePajek__shapkaEdges(self, file, nEdges=-1):
        s = ""
        if nEdges >= 0:
            s = " " + str(nEdges)
        file.write("*Edges" + s + "\n")

    def printToFilePajek(self, sFileName, dMax, bPrint=False, bPrintDetails=False):
        if bPrint:
            print("print net to file " + sFileName + "...")
        file = open(sFileName, "w")

        # *Network
        # *Vertices 3
        # 1 "pe0" ic LightGreen 0.5 0.5 box
        # 2 "pe1" ic LightYellow 0.8473 0.4981 ellipse
        # 3 "pe2" ic LightYellow 0.6112 0.8387 triangle
        # *Arcs
        # 1 2 1 c black
        # 1 3 -1 c red
        # *Edges
        # 2 3 1 c black w 1

        n = len(self.node)
        self.printToFilePajek__shapka(file, n)
        for i in range(n):
            self.node[i].printToFilePajek(i + 1, file)

        # nNodes
        i = 0
        for e in self.edge:
            if (dMax < 0 or e.val <= dMax) and (e.idStart < e.idEnd):
                i += 1
        self.printToFilePajek__shapkaEdges(file, i)

        i = 0
        for e in self.edge:
            if (dMax < 0 or e.val <= dMax) and (e.idStart < e.idEnd):
                e.printToFilePajek(file, e.idStart + 1, e.idEnd + 1)
            i += 1

            if bPrintDetails and self.nEdges > 10000:
                if i % 1000 == 1:
                    print(str(i) + " of " + str(self.nEdges) + " edges are processed")
        file.close()
        if bPrint:
            print("print net to file " + sFileName + "...Finished")

    def printToFilePajek__selectedNodesOnly(
        self, sFileName, dMax, listOfIndexesToSelect, bPrint=False, bPrintDetails=False
    ):
        if bPrint:
            print("print net to file " + sFileName + "...")
        file = open(sFileName, "w")

        n = len(self.node)
        i = 0
        g = []
        for i in range(n):
            g.append(-1)
        for a in listOfIndexesToSelect:
            if a >= 0 and a < n:
                g[a] = 0
        nCorrected = 0
        for i in range(n):
            if g[i] >= 0:
                g[i] = nCorrected
                nCorrected += 1

        self.printToFilePajek__shapka(file, nCorrected)
        for i in range(n):
            if g[i] >= 0:
                self.node[i].printToFilePajek(g[i] + 1, file)

        """
		self.printToFilePajek__shapkaEdges(file)
		i=0
		for e in self.edge:
			if (dMax<0 or e.val<=dMax)and(e.idStart<e.idEnd): 
				if g[e.idStart]>=0 and g[e.idEnd]>=0:
					e.printToFilePajek(file,g[e.idStart]+1,g[e.idEnd]+1)
			i+=1
			
			if bPrintDetails:
				if i%100==1:
					print(str(i)+" of "+str(self.nEdges)+" edges are processed")
		"""
        i = 0
        for e in self.edge:
            if (dMax < 0 or e.val <= dMax) and (e.idStart < e.idEnd):
                if g[e.idStart] >= 0 and g[e.idEnd] >= 0:
                    # e.printToFilePajek(file,g[e.idStart]+1,g[e.idEnd]+1)
                    i += 1

            if bPrintDetails:
                if i % 1000 == 1:
                    print(str(i) + " of " + str(self.nEdges) + " edges are processed")

        self.printToFilePajek__shapkaEdges(file, i)
        i = 0
        for e in self.edge:
            if (dMax < 0 or e.val <= dMax) and (e.idStart < e.idEnd):
                if g[e.idStart] >= 0 and g[e.idEnd] >= 0:
                    e.printToFilePajek(file, g[e.idStart] + 1, g[e.idEnd] + 1)
            i += 1

            if bPrintDetails:
                if i % 1000 == 1:
                    print(str(i) + " of " + str(self.nEdges) + " edges are processed")

        file.close()

        if bPrint:
            print("print net to file " + sFileName + "...Finished")

    def addEdge(self, e):
        if (
            e.idStart >= 0
            and e.idEnd >= 0
            and e.idStart < self.nNodes
            and e.idEnd < self.nNodes
        ):
            e.id = self.nEdges
            self.edge.append(e)
            self.node[e.idStart].edges.append(e)
            self.node[e.idEnd].edges.append(e)
            self.nEdges += 1

    def readFromFilePajek(self, sFileName, bPrint=False, bPrintDetails=False):
        # see: http://vlado.fmf.uni-lj.si/pub/networks/pajek/SVGanim/1.10.7.1/PajekToSvgAnim.pdf
        self.__init__()
        if bPrint:
            print("read net from file " + sFileName + "...")
        fileWithNet = open(sFileName, "r")
        VovaServ = clVovaServ()
        nRowsInFile = VovaServ.nRowsInFile_get(sFileName) if bPrintDetails else 0
        iRow = 0
        bNode = False
        bEdge = False
        nn = 0
        for s in fileWithNet:
            # print(s)
            if len(s) > 2:
                ss = s.split("\n")  # max split = 1
                s = ss[0]
                if s[0] == "*":
                    if s[1] == "N":
                        pass
                    if s[1] == "V":
                        bNode = True
                        bEdge = False
                        ss = s.split(" ")
                        nn = int(ss[1])
                    if s[1] == "E":
                        bEdge = True
                        bNode = False
                else:

                    if bNode:
                        self.addNodeFromS(s)
                    if bEdge:
                        e = self.clEdge()
                        e.getFromS(s)
                        self.addEdge(e)
            iRow = iRow + 1
            if bPrintDetails:
                if iRow % 10000 == 1:
                    print(str(iRow) + " of " + str(nRowsInFile) + " rows are inputed")
        if bPrintDetails:
            print("nNodes=" + str(self.nNodes) + ", nEdges=" + str(self.nEdges))
            # print("names: "+str(self.vsInd))
        fileWithNet.close
        if bPrint:
            print("read net from file " + sFileName + "...Finished")

    def singleLinkageClustering(self, cutoff, bPrint=False, bPrintDetails=False):
        clusters = []  # [iSet],Set=array of idNode
        inCluster = []
        rankMax = []
        nClusters = 0
        n = len(self.node)
        if bPrint:
            print(
                "clustering of net with nNodes="
                + str(n)
                + " and nEdges="
                + str(self.nEdges)
                + "..."
            )
        for i in range(n):
            inCluster.append(-1)
        for i in range(n):
            if inCluster[i] < 0:
                if bPrintDetails:
                    print("started from " + str(i) + " ...")
                nClusters += 1
                iCluster = nClusters - 1
                inCluster[i] = iCluster
                rankMax.append(0)
                r = 0
                currentSet = [i]
                set = [i]
                while len(currentSet) > 0:
                    nextSet = []
                    for j in currentSet:
                        m = self.node[j]
                        for e in m.edges:
                            k = e.idNodeEnd(j)
                            if inCluster[k] < 0:
                                if e.val <= cutoff:
                                    nextSet.append(k)
                                    inCluster[k] = iCluster
                                    set.append(k)
                    if len(nextSet) > 0:
                        r += 1
                        if bPrintDetails:
                            print("rank=" + str(r) + ", nAdd=" + str(len(nextSet)))
                    currentSet = nextSet
                rankMax[iCluster] = r
                clusters.append(set)
                if bPrintDetails:
                    print("started from " + str(i) + " ...Finished: n=" + str(len(set)))
        if bPrint:
            print(
                "clustering of net with nNodes="
                + str(n)
                + " and nEdges="
                + str(self.nEdges)
                + "...Finished"
            )
            print("nClusters=" + str(len(clusters)))
            if bPrintDetails:
                print("Sizes:")
                for c in clusters:
                    print(" " + str(len(c)) + ": " + str(c))
        return clusters, inCluster

    def MST(self, bPrint=False, bPrintDetails=False):
        net = clNetVova()
        i = 0
        for v in self.node:
            vpp = v.copy(i, self)
            i += 1
            net.node.append(vpp)
            net.nNodes += 1
        if self.nEdges < 1:
            return net

        rankInMST = []  # rank in MST
        idEdgeShortestFromMST = []
        n = len(self.node)
        if bPrint:
            print(
                "Minimal spanning tree (MST) for net with nNodes="
                + str(n)
                + " and nEdges="
                + str(self.nEdges)
                + "..."
            )
        for i in range(n):
            rankInMST.append(-1)
            idEdgeShortestFromMST.append(-1)
        """
		idEdgeShortest=0
		lenMin=self.edge[idEdgeShortest].val
		for e in self.edge:
			if e.val<lenMin:
				idEdgeShortest=e.id
				lenMin=e.val
		idV=self.edge[idEdgeShortest].idStart
		>=0 and e.idEnd
		"""
        i = 0
        r = 0
        rankInMST[i] = r
        linkedWithMST = []
        m = self.node[i]
        idsNodeInMST = [i]
        for e in m.edges:
            k = e.idNodeEnd(i)
            if k > i:
                linkedWithMST.append(k)
                idEdgeShortestFromMST[k] = e.id
        # print("1138: linkedWithMST: "+str(linkedWithMST))
        # print("ne="+str(len(m.edges))+" N="+str(len(linkedWithMST)))
        while len(linkedWithMST) > 0:
            bStop = False
            iNodeAdd = linkedWithMST[0]
            minLength = self.edge[idEdgeShortestFromMST[iNodeAdd]].val
            for i in linkedWithMST:
                myLen = self.edge[idEdgeShortestFromMST[i]].val
                if i in idsNodeInMST:
                    print("problem here: i=" + str(i))
                    bStop = True
                    print("idsNodeInMST: " + str(idsNodeInMST))
                    print("linkedWithMST: " + str(linkedWithMST))
                if minLength > myLen:
                    minLength = myLen
                    iNodeAdd = i

            # add
            e = self.edge[idEdgeShortestFromMST[iNodeAdd]]
            k = e.idNodeEnd(iNodeAdd)
            idStart, idEnd = e.sort2(e.idStart, e.idEnd)
            eNew = e.copy(idStart, idEnd, self)
            #
            net.addEdge(eNew)
            rankInMST[iNodeAdd] = rankInMST[k] + 1
            if rankInMST[iNodeAdd] < 0:
                print("ptoblem")
            idsNodeInMST.append(iNodeAdd)

            # update arrays
            # print(str(iNodeAdd))
            # print("1166: linkedWithMST: "+str(linkedWithMST))
            linkedWithMST.remove(iNodeAdd)
            # print("1168: linkedWithMST: "+str(linkedWithMST))
            v = self.node[iNodeAdd]
            for e in v.edges:
                k = e.idNodeEnd(iNodeAdd)
                if rankInMST[k] < 0:
                    if not (k in linkedWithMST):
                        if (k in linkedWithMST) or (k in idsNodeInMST):
                            print(
                                "problem: k=" + str(k) + ", rank=" + str(rankInMST[k])
                            )
                            print(str(linkedWithMST))
                            print(idsNodeInMST)
                        linkedWithMST.append(k)
                        idEdgeShortestFromMST[k] = e.id
                    else:
                        e1 = self.edge[idEdgeShortestFromMST[k]]
                        if e.val < e1.val:
                            idEdgeShortestFromMST[k] = e.id
            if bPrintDetails:
                print("in MST " + str(len(idsNodeInMST)) + " of n=" + str(n))
            if bStop:
                linkedWithMST = []
        if bPrint:
            print(
                "Minimal spanning tree (MST) for net with nNodes="
                + str(n)
                + " and nEdges="
                + str(self.nEdges)
                + "...Finished"
            )
            if bPrintDetails:
                idsNodeInMST.sort()
                print(str(idsNodeInMST))
                print(str(rankInMST))
        return net

    def calcRanksOfNodes(self, idNodeStart, bPrint):
        rank = []
        n = len(self.node)
        if bPrint:
            print(
                "calcRanksOfNodes=" + str(n) + " and nEdges=" + str(self.nEdges) + "..."
            )
        for i in range(n):
            rank.append(-1)
        rank[idNodeStart] = 0
        currentSet = [idNodeStart]
        # set=[idNodeStart]
        set = []
        r = 0
        while len(currentSet) > 0:
            nextSet = []
            for j in currentSet:
                m = self.node[j]
                for e in m.edges:
                    k = e.idNodeEnd(j)
                    if rank[k] < 0:
                        nextSet.append(k)
                        rank[k] = r + 1
                        set.append(k)
            if len(nextSet) > 0:
                r += 1
                bPrintDetails = False
                if bPrintDetails:
                    print("rank=" + str(r) + ", nAdd=" + str(len(nextSet)))
            currentSet = nextSet
        rankMax = max(rank)
        withRank = []
        # print("rank: "+str(rank))
        # print("rankMax: "+str(rankMax))
        for i in range(rankMax + 1):
            withRank.append([])
        for i in range(n):
            # rank[i]
            withRank[rank[i]].append(i)
        # print("withRank: "+str(withRank))
        if bPrint:
            print("rankMax: " + str(rankMax))
            print(
                "calcRanksOfNodes="
                + str(n)
                + " and nEdges="
                + str(self.nEdges)
                + "...Finished"
            )
        return rank, rankMax, withRank

    def idNodesOnPathLongest(self, bPrint, bPrintDetails):
        if bPrint:
            print("idNodesOnPathLongest for net of " + str(self.nNodes) + " nodes...")
        netMST = self.MST(bPrint=False, bPrintDetails=False)
        rank, rankMax, withRank = netMST.calcRanksOfNodes(0, False)
        starts = withRank[rankMax]
        myList = []
        argMax = -1
        for start in starts:
            rank, rankMax, withRank = netMST.calcRanksOfNodes(start, False)
            if argMax < 1:
                argMax = 0
                myList = [rank, rankMax, withRank]
            else:
                if argMax > myList[1]:
                    myList = [rank, rankMax, withRank]
        if bPrintDetails:
            print("LenOfLongestPath=" + str(rankMax + 1)) + " nodes"

        idNode = withRank[rankMax][0]
        idNodes = [idNode]
        r = rankMax
        while r > 0:
            idNodeNext = -1
            for e in netMST.node[idNode].edges:
                k = e.idNodeEnd(idNode)
                if rank[k] < r:
                    idNodeNext = k
            idNodes.append(idNodeNext)
            r -= 1
            idNode = idNodeNext
        if bPrintDetails:
            print("Nodes of path: " + str(idNodes))
        i = 0
        if bPrintDetails:
            print("i\tidInLG\tnameOfNode")
        for id in idNodes:
            i += 1
            if bPrintDetails:
                print(str(i) + " " + str(id) + " " + self.node[id].caption)
            # begin: NODE_11323_length_3805_cov_2.15481_B0
            # end: NODE_7765_length_7967_cov_2.01428_B0
        if bPrint:
            print(
                "idNodesOnPathLongest for net of "
                + str(self.nNodes)
                + " nodes...Finished"
            )
        return idNodes

    def printToFilePajek_allCluster(self, dMax, sName, clusters, inCluster, sPath):
        sFileName = sPath + sName + "_in_" + str(len(clusters)) + "_Clusters.txt"
        file = open(sFileName, "w")
        file.write("i\tmarker\tLG\tn\n")
        for i in range(self.nNodes):
            file.write(
                str(i)
                + "\t"
                + self.node[i].caption
                + "\t"
                + str(inCluster[i])
                + "\t"
                + str(len(clusters[inCluster[i]]))
                + "\n"
            )
        file.close()
        n = len(clusters)
        for i in range(n):
            sFileNamePajekPP = (
                sPath
                + sName
                + "_cl"
                + str(i + 1)
                + "_"
                + str(len(clusters[i]))
                + ".net"
            )
            self.printToFilePajek__selectedNodesOnly(
                sFileNamePajekPP, dMax, clusters[i], True, False
            )
        print("all clusters are printed")

    def nodesIDUnprovenByParallelpaths(self, cutoff, cutoffParallel):
        ids = []
        print("nodesIDUnprovenByParallelpaths...")
        bPrintDetails = False
        for v in self.node:
            vidNode = []
            for e in v.edges:
                if e.val <= cutoff:
                    idNode = e.idNodeEnd(v.id)
                    if bPrintDetails:
                        print("cutoff=" + str(cutoff))
                    if not (idNode in vidNode):
                        vidNode.append(idNode)
                        if bPrintDetails:
                            print(str(idNode) + "\t" + e.s_get(self))
            net1 = self.subnet(vidNode, cutoffParallel)
            clusters, inCluster = net1.singleLinkageClustering(
                cutoffParallel, False, False
            )
            if len(clusters) > 1:
                ids.append(v.id)

                if bPrintDetails:
                    print(str(v.id) + "\t" + v.caption + "\t" + str(len(vidNode)))
                    for idNode in vidNode:
                        v1 = self.node[idNode]
                        print(str(v1.id) + "\t" + v1.caption)
                    for e in v.edges:
                        print(e.s_get(self))

                # t=1/0
            if v.id % 200 == 1:
                print(str(v.id) + " of " + str(self.nNodes) + " nodes are processed")
        print("nodesIDUnprovenByParallelpaths...Finished")
        print(str(len(ids)) + " nodes to exclude:")
        for id in ids:
            print(str(id) + " " + self.node[id].caption)
        return ids

    def sClusters_get(self, vvidNode):
        iCluster = 1
        for vidNode in vvidNode:
            pass
        return s

    def edgesUnprovenByParallelpaths(
        self,
        cutoffEdgeTotest,
        cutoffVerticesLinked,
        nMinVerticesLinkedToEnd,
        cutoffParallel,
        sPath,
    ):
        vidEdge = []
        print("edgesIDUnprovenByParallelpaths...")
        sFileName = (
            sPath
            + "edgesUnprovenByParallelpaths_"
            + str(cutoffVerticesLinked)
            + "_"
            + str(cutoffParallel)
            + ".txt"
        )
        f = open(sFileName, "w")
        for edge in self.edge:
            if edge.val <= cutoffEdgeTotest:
                v1 = self.node[edge.idStart]
                v2 = self.node[edge.idEnd]

                bControl = False
                # if (v1.caption=="scaffold125p41705" and v2.caption=="scaffold24p1171444")or(v2.caption=="scaffold125p41705" and v1.caption=="scaffold24p1171444"):
                # 	bControl=True
                # 	print "control control control control"

                vidNode = []
                n1 = 0
                for e in v1.edges:
                    if e.val <= cutoffVerticesLinked:
                        idNode = e.idNodeEnd(v1.id)
                        if not (idNode in vidNode):
                            vidNode.append(idNode)
                        if idNode != edge.idEnd:
                            n1 += 1
                n2 = 0
                for e in v2.edges:
                    if e.val <= cutoffVerticesLinked:
                        idNode = e.idNodeEnd(v2.id)
                        if not (idNode in vidNode):
                            vidNode.append(idNode)
                        if idNode != edge.idStart:
                            n2 += 1
                if bControl:
                    print("n1,n2=" + str(n1) + "," + str(n2))
                if n1 >= nMinVerticesLinkedToEnd and n2 >= nMinVerticesLinkedToEnd:
                    net1 = self.subnet(vidNode, cutoffParallel, [edge.id])
                    if bControl:
                        self.printToFilePajek("control_All.net", cutoffParallel)
                        net1.printToFilePajek("control1.net", cutoffParallel)
                    clusters, inCluster = net1.singleLinkageClustering(
                        cutoffParallel, False, False
                    )
                    if len(clusters) > 1:
                        vidEdge.append(edge.id)
                        s = (
                            str(edge.id)
                            + "\t"
                            + v1.caption
                            + "\t"
                            + v2.caption
                            + "\t"
                            + str(edge.val)
                            + "\t"
                            + len(str(clusters))
                        )

                        f.write(s + "\n")
            if edge.id % 200 == 1:
                print(
                    str(edge.id) + " of " + str(len(self.edge)) + " edges are processed"
                )
        f.close()
        print("edgesIDUnprovenByParallelpaths...Finished")
        print(str(len(vidEdge)) + " edges to exclude:")

        print(self.edge[0].s_shapka_get())
        for id in vidEdge:
            # print(str(id)+" "+self.node[id].caption)
            print(self.edge[id].s_get(self))
        return vidEdge

    def netWithoutNodesFromList(self, idsExclude, cutoff):
        idsOk = []
        for i in range(self.nNodes):
            if not (i in idsExclude):
                idsOk.append(i)
        return self.subnet(idsOk, cutoff)

    def vidNode_all(self):
        vidNode = []
        for node in self.node:
            vidNode.append(node.id)
        return vidNode

    def subnet(self, ids, cutoff, vidEdgesToExclude=[]):
        net = clNetVova()
        idnew = []
        idsPP = []
        idMy = []
        for i in range(self.nNodes):
            idnew.append(-1)
        i = 0
        for v in self.node:
            if v.id in ids:
                vpp = v.copy(i, self)
                idnew[v.id] = i
                idsPP.append(i)
                idMy.append(v.id)
                i += 1
                net.node.append(vpp)
                net.nNodes += 1
                # if i==1:
                # 	print("nEdges0="+str(len(vpp.edges)))
        if False:
            print(len(idMy))
            print(len(ids))
            for i in ids:
                if not (i in idMy):
                    print(str(i))
            print(ids)
            print(str(self.node[0].id))
            print(str(self.node[1].id))
            print(str(self.node[2].id))

        for i in idsPP:
            j = idMy[i]
            for e in self.node[j].edges:
                # print(str(i)+" "+str(idnew[i])+" "+str(idnew[k])+" "+str(k))
                if e.val <= cutoff and not (e.id in vidEdgesToExclude):
                    k = e.idNodeEnd(j)
                    if idnew[k] >= 0:
                        # print(str(i)+" "+str(idnew[j])+" "+str(idnew[k])+" "+str(k))
                        if idnew[j] < idnew[k]:
                            epp = e.copy(idnew[j], idnew[k], self)
                            net.addEdge(epp)
        return net

    def test(self, sFileNamePajek):
        net.readFromFilePajek(sFileNamePajek, True, True)
        dMax = 0.2
        # clustering and revision with LTC:
        ##net.printToFilePajek(sFileNamePajekPP,dMax,True,True)
        ##net.printToFilePajek__selectedNodesOnly(sFileNamePajekPP,dMax,[0,13,283],True,True)
        # clusters, inCluster = net.singleLinkageClustering(dMax,True,False)
        # net.printToFilePajek__selectedNodesOnly(sFileNamePajekPP,dMax,clusters[0],True,False)
        # print str(clusters[0])
        dMax = 0.25
        # net.printToFilePajek_allCluster(dMax,"clusters_0p2",clusters, inCluster,sPath)
        # result: 16 clusters,
        # 1 non-linear -> 10 linear, parallel proven
        # 2 of 16-1 are linked via 0.17 and 0.19
        pass

    def makeLinearContigClusters(
        self,
        bExcludeNodesCausingNonLinearClusters,
        sFileNamePajek,
        sFileNamePajekPP,
        sPath,
        bPrintClusters,
        bNodeTest,
        bEdgeTest,
        NodeTest_cutoff,
        NodeTest_cutoffParallel,
        cutoffVerticesLinked,
        Net_cutoff,
        Clustering_cutoff,
    ):
        # clusters, inCluster
        if bExcludeNodesCausingNonLinearClusters:
            self.readFromFilePajek(sFileNamePajek, True, True)

            # dealing with non-linear cluster: subdivide automatically
            # dMax=0.2
            # net1=net.subnet(clusters[0],dMax)
            # net1.printToFilePajek(sFileNamePajekPP,dMax,True,True)
            if bNodeTest:
                net1 = self

                if bEdgeTest:
                    # edgesUnprovenByParallelpaths(self,cutoffEdgeTotest,cutoffVerticesLinked,nMinVerticesLinkedToEnd,cutoffParallel,sPath)
                    cutoffEdgeTotest = Net_cutoff
                    # cutoffVerticesLinked=NodeTest_cutoff
                    nMinVerticesLinkedToEnd = 0
                    cutoffParallel = NodeTest_cutoffParallel
                    vidEdgesToExclude = self.edgesUnprovenByParallelpaths(
                        cutoffEdgeTotest,
                        cutoffVerticesLinked,
                        nMinVerticesLinkedToEnd,
                        cutoffParallel,
                        sPath,
                    )
                    # def subnet(self,ids,cutoff,vidEdgesToExclude=[])
                    vidNode = self.vidNode_all()
                    net1 = self.subnet(vidNode, cutoffParallel, vidEdgesToExclude)

                idsExclude = net1.nodesIDUnprovenByParallelpaths(
                    NodeTest_cutoff, NodeTest_cutoffParallel
                )  # cutoff,cutoffParallel
                # two nodes were excluded (correctly)
                # NODE_9542_length_5590_cov_9.67185_B0
                # NODE_4626_length_15504_cov_4.52318_B1
                net2 = net1.netWithoutNodesFromList(idsExclude, NodeTest_cutoffParallel)
                net2.printToFilePajek(sFileNamePajekPP, Net_cutoff, True, True)

        if sFileNamePajekPP == "":
            sFileNamePajekPP = sFileNamePajek
        self.readFromFilePajek(sFileNamePajekPP, True, True)
        # print("ne0="+str(len(net.node[0].edges)))
        # clustering with cutoff 0.5 (to split non-linear, 2 of 16-1 also splited - no matter, seem ok to split: too large gap)
        clusters, inCluster = self.singleLinkageClustering(
            Clustering_cutoff, True, False
        )
        bPrintClusters = True
        if bPrintClusters:
            self.printToFilePajek_allCluster(
                Net_cutoff, "clusters_" + str(Net_cutoff), clusters, inCluster, sPath
            )

            print(len(clusters))
            # result:
            # 27 linear clusters
            #
            # was 5466 markers
            #
            # data in QTL format:
            # see Drive/Cataglyphis/117males/map/Data/data.txt
            # Genetic map and assembly Cnig_gn2:
            # see Drive/Cataglyphis/117males/map/transferMapToAssembly/Cnig_gn2.concatScaf2ChrByMap.3.map
        return clusters, inCluster


class clTrait:
    def __init__(self):
        self.name = ""
        self.nIndivids = 0
        self.valAllInds = []
        self.bVal = []
        self.nVal = 0

    def tratNamesVariations(self):
        """
        QTL mapping (33 traits):
                        Tc25
                        TC25Me3
                        TC25Me5
                        Tc26
                        TC26Di4Me12
                        TC26ME4
                        TC26Me10
                        TC27
                        Tc27di7me11
                        Tc27di11me15
                        TC27Me3
                        TC27Me5
                        TC27Me11-13
                        TC27tri7-11Me15
                        TC28
                        Tc28di4me12
                        Tc28me2
                        Tc28me4Di8Me12
                        Tc28me12
                        TC29
                        Tc29di11me15
                        Tc29me3
                        Tc29me11-13
                        Tc29tri7-11me15
                        TC30
                        Tc30me2
                        Tc30me4
                        Tc30me14
                        TC31
                        Tc31di11me15
                        TC31me13-15
                        Tc31tri7-11me15
                        TOTAL
        GWAS: 34 traits:
                        C25
                        C25m5
                        C25m3
                        C26
                        C26m10
                        C26m4
                        C26dm4_12
                        C27
                        C27m11m13
                        C27m5
                        C27dm11_15
                        C27dm7_11
                        C27m3
                        C27tm7_11_15
                        C28
                        C28m12
                        C28m4dm8_12
                        C28m2
                        C28dm4_12
                        C29
                        C29m11m13
                        C29dm11_15
                        C29me3
                        C29tm7_11_15
                        C30
                        C30m14
                        C30m4
                        C30m2
                        C31
                        C31m13m15
                        C31dm11_15
                        C31tm7_11_15
                        C32
                        C33
        canonical names representing structure:
                konkurenti:

        """
        pass

    def readFromString(self, s):
        ss = s.split("\t")
        # print "ss="+str(ss)
        n = len(ss)
        for i in range(n):
            if i == 0:
                self.name = ss[i]
            else:
                self.nIndivids += 1
                mm = clVovaMath()
                v, b = mm.bNumberWithTest(ss[i])
                self.bVal.append(b)
                self.valAllInds.append(v)
                if b:
                    self.nVal += 1

    def test(self):
        mm = clVovaServ()
        # mm.listOfFiles_get("C:\\Frenkel\\LTCPython\\VovaPy\\",True,".txt")
        sFileNameTraitsAll = "trtMergedAll.txt"
        indexData = 1
        if indexData == 0:
            sPathMultiQTLdata = "C:\\Frenkel\\Privman\\MultiQTL Input Data-20200419T140318Z-001\\MultiQTL Input Data"  #'c25.trt'
            mm.mergeFiles(sPathMultiQTLdata, True, ".trt", sFileNameTraitsAll, True)
        if indexData == 1:
            sFileNameTraitsAll = (
                "C:\\Frenkel\\Privman\\QTL\\allTraits\\allTraits.Original_vova.tra"
            )

        vTrait = self.vTraitFromFile(sFileNameTraitsAll)

        """
		tt=clTrait()
		#print "nu"
		f=open(sFileNameTraitsAll,'r')
		for s in f:
			ss=s[0:len(s)-1]
			tt=clTrait()
			tt.readFromString(ss)
			print tt.name+'\t'+str(tt.nVal)
		f.close
		"""

    def vTraitFromFile(self, sFileNameTraitsAll):  # vTrait=
        vTrait = []
        f = open(sFileNameTraitsAll, "r")
        for s in f:
            ss = s[0 : len(s) - 1]
            tt = clTrait()
            tt.readFromString(ss)
            print(tt.name + "\t" + str(tt.nVal))
            vTrait.append(tt)
        f.close
        return vTrait

    def singleMarkerTestAllTraitsAllMarkers(self, vLG):
        print("singleMarkerTestAllTraitsAllMarkers...")
        sFileNameTraitsAll = (
            "C:\\Frenkel\\Privman\\QTL\\allTraits\\allTraits.Original_vova.tra"
        )
        vTrait = self.vTraitFromFile(sFileNameTraitsAll)

        myMath = clVovaMath()
        m = clMarkerWithGenotypesOfAllIndivids()

        f1 = open("singleMarkerTestAllTraitsAllMarkers.txt", "w")
        f2 = open("singleMarkerTestAllTraitsAllMarkers_permTestOnly.txt", "w")
        s = "sMarker\tidLG\tcoor"
        s1 = "sMarker\tidLG\tcoor"
        for t in vTrait:
            s0, sShort = m.processTrait(t, myMath)
            s += s0
            s1 += sShort
        f1.write(s + "\n")
        f2.write(s1 + "\n")

        im = 0
        imMax = 20
        imMax = -1  # all
        for LG in vLG:
            for LGmarker in LG.vLGmarkerOrderedByCoorOnLG:
                print(str(im))
                m = LGmarker.m
                coor = LGmarker.coorOnLG
                idLG = LG.id
                s = m.sMarker + "\t" + str(idLG) + "\t" + str(coor)
                s1 = m.sMarker + "\t" + str(idLG) + "\t" + str(coor)
                it = 0
                for t in vTrait:
                    # print "trait "+format(it)+": "+t.name
                    s0, sShort = m.processTrait(t, myMath)
                    s += s0
                    s1 += sShort
                    it += 1
                f1.write(s + "\n")
                f2.write(s1 + "\n")
                im += 1

                if imMax >= 0:
                    if im > imMax:
                        break
            if imMax >= 0:
                if im > imMax:
                    break
        f1.close
        print("singleMarkerTestAllTraitsAllMarkers...Finished")

    def readTraitDataIndsAreRowsGWAS(
        self, sFileName
    ):  # vsIndName,vsTraitName,vvbVal,vvVal=
        vsIndName = []
        vsTraitName = []
        vvbVal = []
        vvVal = []
        f = open(sFileName, "r")
        iInd = 0
        nCols = 0
        mm = clVovaMath()
        nErr = 0
        for s in f:
            s1 = s[0 : len(s) - 1]  # exclude \n
            ss = s1.split("\t")
            if iInd == 0:
                nCols = len(ss)
                for iCol in range(1, nCols):
                    vsTraitName.append(ss[iCol])
            else:
                vsIndName.append(ss[0])
                vbVal = []
                vVal = []
                for iCol in range(1, nCols):
                    sVal = ss[iCol]
                    val, b = mm.is_number(sVal)
                    vbVal.append(b)
                    vVal.append(val)
                    if not b:
                        nErr += 1
                        print(
                            "nonNumeric: iRow="
                            + str(iInd)
                            + ", iCol="
                            + str(iCol)
                            + ": <"
                            + sVal
                            + ">"
                        )
                vvbVal.append(vbVal)
                vvVal.append(vVal)
            iInd += 1
        f.close
        print("nonNumeric: n=" + str(nErr))
        return vsIndName, vsTraitName, vvbVal, vvVal


class clMultiQTL:
    # /cygdrive/c/Frenkel/LTCPython/VovaPy/20200520/singleMarkerTestAllTraitsAllMarkers_permTestOnly.txt
    def __init__(self):
        self.vMarkerT = (
            []
        )  # [m] #array of markers characterized by associations with trait (see below)
        self.vsTrait = []  # [it] #array of trait names
        self.viLG = []  # list of iLG presented in the data
        self.vQTL = []  # [iQTL]  list of QTLs
        self.sTraitShapka = "<trait>	n00	n10	n0	n1	m0	m1	m1-m0	STDV0	STDV1	P.E.V.	pPerm	pWilcoxon	ptTestTwoSamplesDiffVar"  # shapka for output

    def start(self):
        sFileName = "C:\\Frenkel\\LTCPython\\VovaPy\\20200520\\singleMarkerTestAllTraitsAllMarkers_permTestOnly.txt"
        sFileName = "C:\\Frenkel\\LTCPython\\VovaPy\\20200520\\singleMarkerTestAllTraitsAllMarkers.txt"
        f = open(sFileName, "r")
        s = f.readline()
        ss = s.split("\t")
        self.tratNamesRead(ss)
        # print s

        f1 = open("p01.txt", "w")
        f1.close()

        s = f.readline()
        while s:
            ss = s.split("\t")
            self.vMarkerT.append(self.clMarkerT(ss, self.viLG))
            s = f.readline()
        f.close()

        # def MyFunc(q):
        # 	return 1000*q.idLG+q.coor
        # self.vMarkerT.sort(key=MyFunc)
        self.vMarkerT = sorted(self.vMarkerT, key=lambda x: (x.sLG, x.coor))
        # for MarkerT in self.vMarkerT:
        # 	print "rrr_"+MarkerT.sLG+"  rrr_"+str(MarkerT.coor)
        self.FDRonAllMarkers()
        self.QTLsSet()
        self.printListOfQTLs()

    class clMarkerT:
        def __init__(self, ss, viLG, vsLG=[]):
            self.vResForTrait = []  # [it]
            # sMarker	idLG	coor
            self.sMarker = ss[0]
            # self.idLG=int(ss[1])
            self.sLG = ss[1]
            self.iLG = vslG.index(self.sLG) if len(vsLG) > 0 else int(self.sLG)
            if not (self.iLG in viLG):
                viLG.append(self.iLG)
            self.coor = float(ss[2])
            self.start(ss)

        def start(self, ss):
            # self.tratNamesRead(ss)
            i = 3
            n = len(ss)
            while i < n:
                ss1 = []
                for j in range(14):  # poka
                    ss1.append(ss[i])
                    i += 1
                self.vResForTrait.append(self.clResForTrait(ss1))

        class clResForTrait:
            def __init__(self, ss):
                self.n00 = int(ss[1])  # n0 before excluding outliers
                self.n10 = int(ss[2])  # n1 before excluding outliers
                self.n0 = int(ss[3])
                self.n1 = int(ss[4])
                self.m0 = float(ss[5])  # mean for allele 0
                self.m1 = float(ss[6])  # mean for allele 1
                self.dm = float(ss[7])  # m1-m0

                self.STDV0 = float(ss[8])  # STDV for allele 0
                self.STDV1 = float(ss[9])  # STDV for allele 1
                self.PEV = float(ss[10])  # Percentage of explained variance

                self.pPerm = float(ss[11])
                self.pWilcoxon = float(ss[12])
                self.ptTestTwoSamplesDiffVar = float(ss[13])

                f = open("p01.txt", "a")
                if (
                    self.ptTestTwoSamplesDiffVar <= 0.01
                    or self.pWilcoxon < 0.01
                    or self.pPerm <= 0.01
                ):
                    s = ""
                    for i in range(14):
                        s += "\t" + ss[i]
                    f.write(s + "\n")
                f.close()

    def tratNamesRead(self, ss):
        self.vsTrait = []
        nCols = len(ss)
        for iCol in range(nCols):
            if (iCol % 14) == 3:
                self.vsTrait.append(ss[iCol])
                print(ss[iCol])

    def FDRonAllMarkers(self):
        vp = []
        for m in self.vMarkerT:
            for t in m.vResForTrait:
                vp.append(t.pPerm)
        print(str(len(self.vMarkerT[0].vResForTrait)))
        mymath = clVovaMath()
        vq = mymath.vqValuesFDR(vp, -1)  # vq=

        f = open("q.txt", "w")
        iq = 0
        for m in self.vMarkerT:
            s = m.sMarker + "\t" + m.sLG + "\t" + str(m.coor)
            for t in m.vResForTrait:
                s += "\t" + str(vq[iq])
                iq += 1
            f.write(s + "\n")
        f.close()

    def FDR_singleTrait_singleQTL_perChr(self):
        vvpp = []
        nt = len(self.vsTrait)
        nLG = len(self.viLG)
        # inicializate
        for it in range(nt):
            vpp = []
            for iLG in self.viLG:
                vpp.append(1)
            vvpp.append(vpp)

        for QTL in self.vQTL:
            if len(QTL.vIdTraits) == 1:
                it = QTL.vIdTraits[0]  # self.vsTrait.index()
                iLG = QTL.MarkerT_start.iLG
                if vvpp[it][iLG] > QTL.pVal:
                    vvpp[it][iLG] = QTL.pVal
        vp = []
        vvpTrait = []
        for it in range(nt):
            vpTrait = []
            for iLG in self.viLG:
                vp.append(vvpp[it][iLG])
                vpTrait.append(vvpp[it][iLG])
            vvpTrait.append(vpTrait)

        mymath = clVovaMath()
        vq = mymath.vqValuesFDR(vp, -1)
        vvqq = []
        vvqTrait = []
        iq = 0
        for it in range(nt):
            vqq = []
            vqTrait = mymath.vqValuesFDR(vvpTrait[it], -1)
            for iLG in self.viLG:
                vqq.append(vq[iq])
                iq += 1
            vvqq.append(vqq)
            vvqTrait.append(vqTrait)
        for QTL in self.vQTL:
            if len(QTL.vIdTraits) == 1:
                it = QTL.vIdTraits[0]  # self.vsTrait.index()
                iLG = QTL.MarkerT_start.iLG
                QTL.qValAllTraits = vvqq[it][iLG]
                QTL.qValTrait = vvqTrait[it][iLG]

    class clQTL:
        def __init__(
            self,
            MarkerT_start,
            MarkerT_end,
            MarkerT_mostSignif,
            MarkerT_highestPEV,
            MarkerT_confInterval_left,
            MarkerT_confInterval_right,
            vIdTraits,
            PEV,
        ):
            self.vIdTraits = vIdTraits
            self.MarkerT_start = MarkerT_start
            self.MarkerT_end = MarkerT_end
            self.MarkerT_mostSignif = MarkerT_mostSignif
            self.MarkerT_highestPEV = MarkerT_highestPEV
            self.MarkerT_confInterval_left = MarkerT_confInterval_left
            self.MarkerT_confInterval_right = MarkerT_confInterval_right
            self.pVal = 1
            self.qValTrait = 1
            self.qValAllTraits = 1
            self.PEV = PEV
            self.x1 = 0
            self.x2 = 0
            self.xx()

        def xx(self):
            dMinFromX0 = 7.5  # cM
            dMinForAccuracy = 3
            x0 = self.MarkerT_mostSignif.coor
            x1 = self.MarkerT_confInterval_left.coor + dMinForAccuracy
            x2 = self.MarkerT_confInterval_right.coor - dMinForAccuracy
            if x0 - x1 < dMinFromX0:
                x1 = x0 - dMinFromX0
            if x2 - x0 < dMinFromX0:
                x2 = x0 + dMinFromX0
            self.x1 = x1
            self.x2 = x2

    def QTLsSet(self):
        iQTL = 0
        for idTrait in range(len(self.vsTrait)):
            iMarkerT = 0
            while iMarkerT < len(self.vMarkerT):
                MarkerT = self.vMarkerT[iMarkerT]
                if MarkerT.vResForTrait[idTrait].pPerm < 0.001:
                    sChrCurrent = MarkerT.sLG
                    MarkerT_start = MarkerT
                    MarkerT_end = MarkerT
                    MarkerT_mostSignif = MarkerT
                    MarkerT_highestPEV = MarkerT
                    vIdTraits = [idTrait]
                    sChr = MarkerT.sLG

                    # print "iQTL="+str(iQTL)+", idTrait="+str(idTrait)+", iMarkerT="+str(iMarkerT)+" sChr="+sChr+", coor="+str(MarkerT.coor)
                    MarkerT.coor
                    iMarkerTmin = iMarkerT
                    iMarkerTmax = iMarkerT

                    # iMarkerTmax
                    coor = MarkerT.coor
                    if iMarkerT < len(self.vMarkerT) - 1:
                        iMarkerT1 = iMarkerT + 1
                        MarkerT1 = self.vMarkerT[iMarkerT1]
                        bContinue = True
                        # print str(MarkerT1.vResForTrait[idTrait].pPerm)
                        while (
                            (MarkerT1.coor - coor < 15)
                            and sChr == MarkerT1.sLG
                            and bContinue
                        ):
                            if (
                                MarkerT1.vResForTrait[idTrait].pPerm < 0.01
                                and MarkerT1.coor - coor < 10
                            ) or MarkerT1.vResForTrait[idTrait].pPerm < 0.001:
                                coor = MarkerT1.coor
                                iMarkerTmax = iMarkerT1
                            # print "coor="+str(coor)+", iMarkerT1+="+str(iMarkerT1)+" p="+str(MarkerT1.vResForTrait[idTrait].pPerm)

                            iMarkerT1 += 1
                            if iMarkerT1 <= len(self.vMarkerT) - 1:
                                MarkerT1 = self.vMarkerT[iMarkerT1]
                                # print "d="+str(MarkerT1.coor-coor)+", p="+str(MarkerT1.vResForTrait[idTrait].pPerm)
                            else:
                                bContinue = False
                                # print "oioioi"

                    # iMarkerTmin
                    coor = MarkerT.coor
                    if iMarkerT > 0:
                        iMarkerT1 = iMarkerT - 1
                        MarkerT1 = self.vMarkerT[iMarkerT1]
                        bContinue = True
                        while (
                            coor - MarkerT1.coor < 10
                            and sChr == MarkerT1.sLG
                            and bContinue
                        ):
                            if MarkerT1.vResForTrait[idTrait].pPerm < 0.01:
                                coor = MarkerT1.coor
                                iMarkerTmin = iMarkerT1
                                # print "coor="+str(coor)+", iMarkerT1-="+str(iMarkerT1)
                            iMarkerT1 -= 1
                            if iMarkerT1 >= 0:
                                MarkerT1 = self.vMarkerT[iMarkerT1]
                            else:
                                bContinue = False

                    MarkerT_start = self.vMarkerT[iMarkerTmin]
                    MarkerT_end = self.vMarkerT[iMarkerTmax]
                    MarkerT_confInterval_left = self.vMarkerT[iMarkerTmax]
                    MarkerT_confInterval_right = self.vMarkerT[iMarkerTmax]
                    if iMarkerTmax > iMarkerTmin:
                        # pBest=MarkerT_start.vResForTrait[idTrait].pPerm
                        for iMarker in range(iMarkerTmin, iMarkerTmax + 1):
                            MarkerT = self.vMarkerT[iMarker]
                            if (
                                MarkerT_highestPEV.vResForTrait[idTrait].PEV
                                < MarkerT.vResForTrait[idTrait].PEV
                            ):
                                MarkerT_highestPEV = MarkerT
                            if (
                                MarkerT_mostSignif.vResForTrait[idTrait].pPerm
                                > MarkerT.vResForTrait[idTrait].pPerm
                            ):
                                MarkerT_mostSignif = MarkerT
                        LOD0 = -math.log(MarkerT_mostSignif.vResForTrait[idTrait].pPerm)
                        bMarkerT_confInterval_left = False
                        for iMarker in range(iMarkerTmin, iMarkerTmax + 1):
                            MarkerT = self.vMarkerT[iMarker]
                            LOD = -math.log(MarkerT.vResForTrait[idTrait].pPerm)
                            if LOD0 - LOD <= 1.55:
                                if not bMarkerT_confInterval_left:
                                    bMarkerT_confInterval_left = True
                                    MarkerT_confInterval_left = MarkerT
                                MarkerT_confInterval_right = MarkerT
                    PEV = MarkerT_highestPEV.vResForTrait[idTrait].PEV
                    QTL = self.clQTL(
                        MarkerT_start,
                        MarkerT_end,
                        MarkerT_mostSignif,
                        MarkerT_highestPEV,
                        MarkerT_confInterval_left,
                        MarkerT_confInterval_right,
                        vIdTraits,
                        PEV,
                    )

                    # poka
                    QTL.pVal = MarkerT_mostSignif.vResForTrait[idTrait].pPerm

                    self.vQTL.append(QTL)

                    iMarkerT = iMarkerTmax
                    # print str(iMarkerT)
                    iQTL += 1
                    # if iQTL>3:
                    # 	return
                iMarkerT += 1
        self.FDR_singleTrait_singleQTL_perChr()

    def printListOfQTLs(self):
        f = open("QTLs.txt", "w")
        s = "iQTL" + "\t" + "traits" + "\t" + "chr"
        s += "\t" + "coorMin" + "\t" + "coorMax" + "\t" + "d"
        s += "\t" + "coorBestP" + "\t" + "coorBestPEV"
        s += "\t" + "confInt_left" + "\t" + "confInt_right" + "\t" + "d"
        s += "\t" + "confInt_leftPP" + "\t" + "confInt_rightPP" + "\t" + "dPP"
        s += "\t" + "PEV" + "\t" + "pVal" + "\t" + "qValTrait" + "\t" + "qValAllTraits"
        s += (
            "\t"
            + "M_coorMin"
            + "\t"
            + "M_coorMax"
            + "\t"
            + "M_coorBestP"
            + "\t"
            + "M_coorBestPEV"
        )
        s += "\t" + "M_confInt_left" + "\t" + "M_confInt_right"
        f.write(s + "\n")

        iQTL = 0
        for QTL in self.vQTL:
            i = 0
            sTraits = ""
            for IdTrait in QTL.vIdTraits:
                if len(sTraits) > 0:
                    sTraits += ","
                sTraits += self.vsTrait[IdTrait]

            sChr = QTL.MarkerT_start.sLG
            s = str(iQTL) + "\t" + sTraits + "\t" + sChr
            s += (
                "\t"
                + str(QTL.MarkerT_start.coor)
                + "\t"
                + str(QTL.MarkerT_end.coor)
                + "\t"
                + str(QTL.MarkerT_end.coor - QTL.MarkerT_start.coor)
            )
            s += (
                "\t"
                + str(QTL.MarkerT_mostSignif.coor)
                + "\t"
                + str(QTL.MarkerT_highestPEV.coor)
            )
            s += (
                "\t"
                + str(QTL.MarkerT_confInterval_left.coor)
                + "\t"
                + str(QTL.MarkerT_confInterval_right.coor)
                + "\t"
                + str(
                    QTL.MarkerT_confInterval_right.coor
                    - QTL.MarkerT_confInterval_left.coor
                )
            )
            s += "\t" + str(QTL.x1) + "\t" + str(QTL.x2) + "\t" + str(QTL.x2 - QTL.x1)
            s += (
                "\t"
                + str(QTL.PEV)
                + "\t"
                + str(QTL.pVal)
                + "\t"
                + str(QTL.qValTrait)
                + "\t"
                + str(QTL.qValAllTraits)
            )
            s += (
                "\t"
                + str(QTL.MarkerT_start.sMarker)
                + "\t"
                + str(QTL.MarkerT_end.sMarker)
                + "\t"
                + str(QTL.MarkerT_mostSignif.sMarker)
                + "\t"
                + str(QTL.MarkerT_highestPEV.sMarker)
            )
            s += (
                "\t"
                + str(QTL.MarkerT_confInterval_left.sMarker)
                + "\t"
                + str(QTL.MarkerT_confInterval_right.sMarker)
            )
            f.write(s + "\n")
            iQTL += 1
        f.close()

    class clChromTrait:
        def __init__(self):
            self.nInds = 0
            self.nTraits = 1
            self.nMarkers = 0
            self.nPerm = 0  # not include initial
            self.vvTrait = []  # ind,it
            self.vTraitsAreDefined = []  # ind
            self.vMarkerChr = []  # m
            self.index = 0  # see criterion()
            self.TraitNoMissingData = True
            self.vdMax = []

        class clMarkerChr:
            def __init__(self):
                self.vg = []  # int
                self.valPerm = []  # perm
                self.valPermIsDefined = []  # perm

                self.k = -1
                self.vOrdered = []

            def k_and_vOrdered_Make(self, TraitNoMissingData):
                n = len(self.valPermIsDefined)
                self.k = n
                b = TraitNoMissingData
                if not b:
                    b = self.valPermIsDefined[0]
                if b:
                    k = 0
                    v0 = self.valPerm[0]
                    if TraitNoMissingData:
                        for v in self.valPerm:
                            self.vOrdered.append(v)
                    else:
                        iPerm = 0
                        for b in self.valPermIsDefined:
                            if b:
                                v = self.valPerm[iPerm]
                                self.vOrdered.append(v)
                            iPerm += 1
                    self.vOrdered.sort()
                    for v in self.vOrdered:
                        if v >= v0:
                            k += 1
                    self.k = k

        def simulateData(self):  # nr,vt00,vt01,vt10,vt11=
            self.nInds = 100
            self.nTraits = 1
            self.nMarkers = 100
            self.vMarkerChr = []
            self.vvTrait = []
            self.vTraitsAreDefined = []
            self.TraitNoMissingData = True
            for im in range(self.nMarkers):
                m = self.clMarkerChr()
                for i in range(self.nInds):
                    m.vg.append(-1)
                self.vMarkerChr.append(m)

            # genotypes and phenotypes
            iq = 30
            nr = 0
            vt00 = []  # ind
            vt01 = []  # ind
            vt10 = []  # ind
            vt11 = []  # ind
            for i in range(self.nInds):
                a = random.randint(0, 1)
                im = 0
                for m in self.vMarkerChr:
                    if im == iq:
                        if random.random() < 0.8 or self.TraitNoMissingData:
                            self.vTraitsAreDefined.append(True)
                            t = random.gauss(0, 1)
                            # a=0 or 1
                            t0 = a + t + random.gauss(0, 0.001)
                            t1 = a + t + random.gauss(0, 0.001)

                            # a=0 or 1
                            t0 = a
                            t1 = a
                            self.vvTrait.append([t0, t1])
                            if a == 0:
                                vt00.append(t0)
                                vt01.append(t1)
                            else:
                                vt10.append(t0)
                                vt11.append(t1)
                        else:
                            self.vTraitsAreDefined.append(False)
                            self.vvTrait.append([-1, -1])
                    if random.random() < 0.98:
                        m.vg[i] = a
                    if random.random() < 0.01:
                        a = 1 - a
                        nr += 1
                    im += 1
            return nr, vt00, vt01, vt10, vt11

        def pForRealData(self, vLG, Trait, nPermutations=10000, bPrint=False):  # p=
            self.TraitNoMissingData = True

            VovaMath = clVovaMath()
            k = VovaMath.vvSortedAndNoOutLiersIfNeed___k
            VovaMath.vvSortedAndNoOutLiersIfNeed___vmaxVarRelativeToKK__make(100, k)

            vt = []
            for iInd in range(Trait.nIndivids):
                if Trait.bVal[iInd]:
                    v = Trait.valAllInds[iInd]
                    vt.append(v)
            vt = VovaMath.vvSortedAndNoOutLiersIfNeed(vt, -1)
            vMin = vt[0]
            vMax = vt[len(vt) - 1]

            # inicialization of arrays
            self.nInds = len(vt)
            self.nTraits = 1
            self.nMarkers = 0
            for LG in vLG:
                self.nMarkers += LG.nMarkers
            self.vMarkerChr = []
            self.vvTrait = []
            self.vTraitsAreDefined = []
            for im in range(self.nMarkers):
                m = self.clMarkerChr()
                for i in range(self.nInds):
                    m.vg.append(-1)
                self.vMarkerChr.append(m)

            i = 0
            for iInd in range(Trait.nIndivids):
                if Trait.bVal[iInd]:
                    v = Trait.valAllInds[iInd]
                    if v >= vMin and v <= vMax:
                        self.vvTrait.append([v])
                        self.vTraitsAreDefined.append(True)
                        im = 0
                        for LG in vLG:
                            for LGmarker in LG.vLGmarkerOrderedByCoorOnLG:
                                m = self.vMarkerChr[im]
                                if bPrint:
                                    if i == 0:
                                        print(
                                            str(im)
                                            + " "
                                            + str(LGmarker.coorOnLG)
                                            + " "
                                            + LGmarker.m.sMarker
                                        )
                                m.vg[i] = LGmarker.m.g[iInd]
                                im += 1
                        i += 1

            bdMaxOnly = True
            bPrint = True
            self.makeAllPermutations(nPermutations, bdMaxOnly, bPrint)

            p = 1
            if bdMaxOnly:
                d0 = self.vdMax[0]
                n = 0
                k = 0
                for d in self.vdMax:
                    if d >= d0:
                        k += 1
                    n += 1
                p = float(k) / n
            else:
                p = self.pPermCalc_basedOnMinPValInPermTestsOnly(nPermutations, False)
            print("p=" + str(p))
            return p

        def testBySimul(self):
            self.simulateData()

            # print
            bPrint = False
            if bPrint:
                im = 0
                for m in self.vMarkerChr:
                    s = "m" + str(im) + "\t"
                    for i in range(self.nInds):
                        if m.vg[i] < 0:
                            s += "-"
                        else:
                            s += str(m.vg[i])
                    print(s)
                    im += 1

            VovaMath = clVovaMath()
            if bPrint:
                print("r=" + str(float(nr) / (self.nInds * self.nMarkers)))
                print("rho0=" + str(VovaMath.corrAndP(vt00, vt01)))  # corr,p=)
                print("rho1=" + str(VovaMath.corrAndP(vt10, vt11)))  # corr,p=)
                print(
                    "m0="
                    + str(VovaMath.mean(vt00))
                    + ", stdv="
                    + str(math.sqrt(VovaMath.var(vt00)))
                )
                print(
                    "m1="
                    + str(VovaMath.mean(vt10))
                    + ", stdv="
                    + str(math.sqrt(VovaMath.var(vt10)))
                )
                print("PEV0mm=" + str(VovaMath.PEV(vt00, vt10)))
                print("PEV1mm=" + str(VovaMath.PEV(vt01, vt11)))
                print("PEV0=" + str(VovaMath.PEV(vt00, vt01)))
                print("PEV1=" + str(VovaMath.PEV(vt10, vt11)))
                # print "rhomm="+str(VovaMath.corrAndP(vt10,vt01))#corr,p=)
                print("")

            # nPermutations
            self.index = 1
            bdMaxOnly = False
            # self.makeAllPermutations(1000,bdMaxOnly,bPrint)#16 sec, ~0.02, 3 sec without perm of perm
            nPermutations = 10000
            self.makeAllPermutations(nPermutations, bdMaxOnly, False)
            # 30 sec without perm of perm for 10,000
            p = 10  # self.pPermCalc()
            p = self.pPermCalc_basedOnMinPValInPermTestsOnly(nPermutations, False)
            print("p=" + str(p))
            return p

        def makeAllPermutations(self, nPermutations, bdMaxOnly, bPrint):
            for m in self.vMarkerChr:
                m.valPerm = []  # perm
                m.valPermIsDefined = []
            self.nPerm = -1
            viIndPermutated = []
            for i in range(self.nInds):
                viIndPermutated.append(i)
            self.vdMax = []
            VovaMath = clVovaMath()

            dMax = self.addPermutation(viIndPermutated, bdMaxOnly, bPrint, VovaMath)
            dMax0 = dMax
            nAtLeastdMax0 = 0
            self.vdMax.append(dMax)
            for iPerm in range(nPermutations):
                if self.nMarkers >= 500:
                    if iPerm % 10 == 0:
                        print(
                            str(iPerm) + " of " + str(nPermutations) + " nPermutations"
                        )
                random.shuffle(viIndPermutated)
                dMax = self.addPermutation(viIndPermutated, bdMaxOnly, bPrint, VovaMath)
                self.vdMax.append(dMax)
                if dMax >= dMax0:
                    nAtLeastdMax0 += 1
                if bdMaxOnly:
                    if nAtLeastdMax0 >= 5:
                        break

        def addPermutation(self, viIndPermutated, bdMaxOnly, bPrint, VovaMath):  # dMax=
            self.nPerm += 1
            im = 0
            dMax = -1
            s = ""
            idMax = -1
            nOk = 0
            for m in self.vMarkerChr:
                vv0 = []
                vv1 = []
                for i in range(self.nInds):
                    iIndPermutated = viIndPermutated[i]
                    b = self.TraitNoMissingData
                    if not b:
                        b = self.vTraitsAreDefined[iIndPermutated]
                    if b:
                        if m.vg[i] == 0:
                            vv0.append(self.vvTrait[iIndPermutated])
                        if m.vg[i] == 1:
                            vv1.append(self.vvTrait[iIndPermutated])

                if len(vv0) < 6 or len(vv1) < 6:
                    if not bdMaxOnly:
                        m.valPermIsDefined.append(False)
                        m.valPerm.append(-1)
                else:
                    # poka: single trait,mean
                    # potom: median, multitrait
                    v0 = []
                    v1 = []
                    for vv in vv0:
                        v0.append(vv[0])
                    for vv in vv1:
                        v1.append(vv[0])

                    index = 6
                    d = -1
                    if index == 0:
                        # smallest p-value of permutation test
                        # not good: far markers are not linked, in some permutation have max => lost of significance
                        pass
                    if index == 1:
                        # not good: in some markers missing data and unfiltered outliers cause high d even in permutated data
                        m0 = VovaMath.mean(v0)
                        m1 = VovaMath.mean(v1)
                        d = abs(m1 - m0)
                    if index == 2:
                        # not good: in some markers missing data cause high d even in permutated data
                        m0 = VovaMath.median(v0)
                        m1 = VovaMath.median(v1)
                        d = abs(m1 - m0)
                    if index == 3:
                        n0 = str(len(v0))
                        n1 = str(len(v1))
                        m0 = VovaMath.mean(v0)
                        m1 = VovaMath.mean(v1)
                        d = abs(m1 - m0)
                        uu, p = VovaMath.WilcoxonTest(v0, v1)
                        if bPrint:
                            s += (
                                " "
                                + str(im)
                                + ":"
                                + str(d)
                                + " "
                                + str(m0)
                                + " "
                                + str(m1)
                                + " "
                                + str(n0)
                                + " "
                                + str(n1)
                                + " pW="
                                + str(p)
                            )
                        d = -p
                    if index == 4:
                        pM = VovaMath.tTestTwoSamplesDiffVar(v0, v1)
                        if pM <= 0.002:
                            uu, pW = VovaMath.WilcoxonTest(v0, v1)
                            if pW <= 0.003:
                                PEV = VovaMath.PEV(v0, v1)
                                d = PEV
                    if index == 5:
                        # too long, not so regular
                        # v0=VovaMath.vvSortedAndNoOutLiersIfNeed(v0,-1)
                        # v1=VovaMath.vvSortedAndNoOutLiersIfNeed(v1,-1)

                        # not enought
                        pM = VovaMath.tTestTwoSamplesDiffVar(v0, v1)
                        if pM <= 0.005:
                            uu, pW = VovaMath.WilcoxonTest(v0, v1)
                            if pW <= 0.01:
                                PEV = VovaMath.PEV(v0, v1)
                                if PEV > 0.07:  # 0.11:
                                    nOk += 1
                                    d = nOk
                    if index == 6:
                        pM = VovaMath.tTestTwoSamplesDiffVar(v0, v1)
                        if pM <= 0.001:
                            uu, pW = VovaMath.WilcoxonTest(v0, v1)
                            if pW <= 0.003:
                                PEV = VovaMath.PEV(v0, v1)
                                if PEV > 0.12:
                                    nOk += 1
                                    d = nOk
                    if dMax < d:
                        dMax = d
                        idMax = im

                    if not bdMaxOnly:
                        m.valPermIsDefined.append(True)
                        m.valPerm.append(d)
                im += 1
            if bPrint:
                if index == 3:
                    print(s)
                print("dmax=" + str(dMax) + ", idMax=" + str(idMax))
            return dMax

        def vpPerm_get(self, iPerm, nPerm):
            vpPerm = []
            b = (
                self.TraitNoMissingData
                if self.TraitNoMissingData
                else m.valPermIsDefined[iPerm]
            )
            for m in self.vMarkerChr:
                if b:
                    v0 = m.valPerm[iPerm]
                    k = 0
                    n = 0
                    if self.TraitNoMissingData:
                        for v in m.valPerm:
                            n += 1
                            if v >= v0:
                                k += 1
                    else:
                        for iPerm1 in range(nPerm):
                            if m.valPermIsDefined[iPerm1]:
                                n += 1
                                if m.valPerm[iPerm1] >= v0:
                                    k += 1
                    if iPerm > nPerm - 1:
                        n += 1
                        k += 1
                    vpPerm.append(float(k) / n)
                else:
                    vpPerm.append(1)
            return vpPerm

        def criterion(self, vpPerm):
            if self.index == 0:  # -log(minPval), 80%, ave 0.05(60% ave 0.1)
                return -math.log(min(vpPerm))
            if self.index == 1:  # n less alpha, 75%, ave 0.07
                alpha = 0.01
                sum = 0
                for p in vpPerm:
                    if p <= alpha:
                        sum += 1
                return sum
            if self.index == 2:  # sum -log(p), 55%, ave 0.085
                sum = 0
                for p in vpPerm:
                    sum += -math.log(p)
                return sum
            if self.index == 3:  # sum -log(p_less_alpha), 70%, 0.26
                alpha = 0.01
                sum = 0
                for p in vpPerm:
                    if p <= alpha:
                        sum += -math.log(p)
                return sum

        def pPermBasedOndMax(self):  # p=
            pass

        def pPermCalc(self):  # p=
            nPerm = self.nPerm  # can be less to make calculation faster
            vpPerm = self.vpPerm_get(0, nPerm)  # list of p-values in the initial data
            v = self.criterion(vpPerm)
            k = 0
            for iPerm in range(self.nPerm):
                vpPerm = self.vpPerm_get(
                    iPerm + 1, nPerm
                )  # list of p-values in permutated data
                v1 = self.criterion(vpPerm)
                if v1 >= v:
                    k += 1
            return float(k + 1) / (self.nPerm + 1)

        def pPermCalc_basedOnMinPValInPermTestsOnly(self, nPermutations, bPrint):  # p=
            kMin = nPermutations + 1
            for m in self.vMarkerChr:
                m.k_and_vOrdered_Make(self.TraitNoMissingData)
                if kMin > m.k:
                    kMin = m.k
            if bPrint:
                print("kMin=" + str(kMin))
            viPermSignif = []
            if self.TraitNoMissingData:
                for m in self.vMarkerChr:
                    n = len(m.vOrdered)
                    v1 = m.vOrdered[n - kMin]
                    iPerm = 0
                    for v in m.valPerm:
                        if v >= v1:
                            if not (iPerm in viPermSignif):
                                viPermSignif.append(iPerm)
                        iPerm += 1
            else:
                for m in self.vMarkerChr:
                    n = len(m.vOrdered)
                    v1 = m.vOrdered[n - kMin]
                    for iPerm in range(nPermutations):
                        if m.valPermIsDefined[iPerm]:
                            if m.valPerm[iPerm] >= v1:
                                if not (iPerm in viPermSignif):
                                    viPermSignif.append(iPerm)
            # viPermSignif=list(dict.fromkeys(viPermSignif))#remove repeats
            k = len(viPermSignif)
            if bPrint:
                print("nkMin=" + str(k) + ", viPermSignif=" + str(viPermSignif))
            return float(k) / (nPermutations + 1)


class clBlastRes:
    def __init__(self):
        self.quaries = clSecCtgs()  # not in use
        self.DB = clSecCtgs()  # not in use

    """
	# BLASTN 2.2.30+
	# Query: NODE_11_length_463706_cov_0.703814
	# Database: SPades_M4B_K13-123_28_2_2017_B.scaffolds.fasta
	# Fields: query id, subject id, % identity, alignment length, mismatches, gap opens, q. start, q. end, s. start, s. end, evalue, bit score
	# 14 hits found
	NODE_11_length_463706_cov_0.703814	NODE_9_length_225546_cov_0.261207	100.00	225414	0	0	121021	346434	133	225546	0.0	4.163e+05
	NODE_11_length_463706_cov_0.703814	NODE_10_length_190194_cov_0.285862	99.98	117389	4	3	346335	463706	117387	2	0.0	2.166e+05
	"""

    class clLineOfBlastRes:
        def __init__(self, s):
            if s != "":
                ss = s.split("\t")
                # test
                if len(ss) < 12:
                    print(s)
                # self.s=s
                self.sQ = ss[0]
                self.sDB = ss[1]
                self.nLen = int(ss[3])
                self.nM = int(ss[4])
                self.nD = int(ss[5])
                self.startQ = int(ss[6])
                self.endQ = int(ss[7])
                self.startDB = int(ss[8])
                self.endDB = int(ss[9])
                self.sEval = ss[10]
                self.smLogP = ss[11]
                # 0.0 -> 1000
                # 5.24e-13 -> -log10(5.24*10^-13)=13-log10(5.24)
                # 0.22 -> 0 #not interesting
                if self.sEval == "0.0":
                    self.mLog10EVal = 1000
                else:
                    k = self.sEval.find("e-")
                    if k <= 0:
                        self.mLog10EVal = 0
                    else:
                        a = float(self.sEval[0:k])
                        b = int(self.sEval[k + 2 :])
                        self.mLog10EVal = b - math.log10(a)

        def copy(self):
            BlastRes = clBlastRes()
            x = BlastRes.clLineOfBlastRes("")
            x.sQ = self.sQ
            x.sDB = self.sDB
            x.nLen = self.nLen
            x.nM = self.nM
            x.nD = self.nD
            x.startQ = self.startQ
            x.endQ = self.endQ
            x.startDB = self.startDB
            x.endDB = self.endDB
            x.sEval = self.sEval
            x.smLogP = self.smLogP
            x.mLog10EVal = self.mLog10EVal
            return x

        def q(self):
            return [self.startQ, self.endQ]  # ,self.startDB,self.endDB]

        def coorDB_get(self, coor, startQ=-1, startDB=-1, endDB=-1):  # coorDB=
            if startQ < 0:
                startQ = self.startQ
                startDB = self.startDB
                endDB = self.endDB
            # coorDB = calculated coordinate in another (genome, assembly etc.)#Cnig_gn1
            coorDB = startDB
            if startDB < endDB:
                # DB:  .......1,2,.,sDB,.,aDB,...,eDB,...,endDB
                #                   |......|......|
                # q:  1,2,.........,sQ,...,aQ,...,eQ,................,endQ
                # aDB=sDB+(aQ-sQ)
                coorDB += coor - startQ
            else:
                # DB:  .....endDB,.,sDB,.,aDB,...,eDB,...,2,1
                #                   |......|......|
                # q:  1,2,.........,sQ,...,aQ,...,eQ,................,endQ
                # aDB=sDB-(aQ-sQ)
                coorDB -= coor - startQ
            return coorDB

        def bPosOrientation_get(self):
            return self.endDB >= self.startDB

    class clLinesOfBlastRes:
        def __init__(self, sFirstStringOfBlockOfFastaResult, f):
            self.sQ = ""
            self.vsDB = []  # names of sDB overlapping with quary sequence sQ
            self.LinesOfBlastRes = []  # array of clLineOfBlastRes()
            self.bLinesOfBlastRes = False

            # to help read from large file
            self.bNotTheLastBlock = False
            self.sFirstStringOfNextBlockOfFastaResult = ""

            if sFirstStringOfBlockOfFastaResult != "no need":
                self.start(sFirstStringOfBlockOfFastaResult, f)

        def start(self, sFirstStringOfBlockOfFastaResult, f):
            myBlastRes = clBlastRes()
            sDB = ""
            vq = []
            myLineOfBlastRes_prev = []
            if sFirstStringOfBlockOfFastaResult != "":
                myLineOfBlastRes_prev = myBlastRes.clLineOfBlastRes(
                    sFirstStringOfBlockOfFastaResult
                )
                self.LinesOfBlastRes.append(myLineOfBlastRes_prev)
                self.sQ = myLineOfBlastRes_prev.sQ
                sDB = myLineOfBlastRes_prev.sDB
                vq.append(myLineOfBlastRes_prev.q())
                # print "sQ(5167)="+self.sQ
                if False:
                    print("vq=" + str(vq))
            self.sFirstStringOfNextBlockOfFastaResult = ""
            self.bNotTheLastBlock = False

            bCompress = True
            # Compress=False

            nLines = 0
            s = f.readline()
            while s:
                bNeedToReadNextLine = True
                if len(s) > 1:
                    if s[0] != "#":  # no need rows with comments
                        nLines += 1
                        if nLines % 10000 == 9999:
                            print(str(nLines + 1))
                            if bCompress:
                                self.compress_vq(vq)
                                # print "len(vq)="+str(len(vq))
                        myLineOfBlastRes = myBlastRes.clLineOfBlastRes(s)
                        # sQnext,sDB,nLen,nM,nD,startQ,endQ,startDB,endDB,sEval,smLogP=clLineOfBlastRes(s)
                        if self.sQ == "":
                            self.sQ = myLineOfBlastRes.sQ
                            sDB = myLineOfBlastRes.sDB
                            # print "sQ(5180)="+self.sQ
                        if myLineOfBlastRes.sQ == self.sQ:
                            if bCompress:
                                if myLineOfBlastRes.sDB != sDB:
                                    # print "6998    len(vq)="+str(len(vq))+" "+myLineOfBlastRes.sDB+" "+sDB+" "+myLineOfBlastRes_prev.sDB
                                    self.compress_vq(vq)
                                    self.append_LinesOfBlastRes_by_vq(vq)
                                    vq = []
                                    self.LinesOfBlastRes.append(myLineOfBlastRes)
                                vq.append(myLineOfBlastRes.q())
                                if len(vq) == 1:
                                    self.LinesOfBlastRes.append(myLineOfBlastRes)
                            else:
                                self.LinesOfBlastRes.append(myLineOfBlastRes)
                        else:
                            self.sFirstStringOfNextBlockOfFastaResult = s
                            self.bNotTheLastBlock = True
                            bNeedToReadNextLine = False
                        myLineOfBlastRes_prev = myLineOfBlastRes
                if bNeedToReadNextLine:
                    s = f.readline()
                else:
                    s = False
            if bCompress:
                self.append_LinesOfBlastRes_by_vq(vq)

        def compress_vq(self, vq):
            def MyFunc(q):
                # return -(q[1]-q[0]+1)
                return q[0]

            # poka: ne smotrim coordinates on DB
            n = len(vq)
            if n > 10:
                vq.sort(key=MyFunc)
                vIntervals = []
                q = vq[0]
                myInterval = [q[0], q[1]]  # ,min(q[2],q[3]),max(q[2],q[3])]
                for q in vq:
                    if q[0] <= myInterval[1]:
                        if q[1] > myInterval[1]:
                            myInterval[1] = q[1]
                    else:
                        vIntervals.append(myInterval)
                        myInterval = [q[0], q[1]]  # ,min(q[2],q[3]),max(q[2],q[3])]
                vq = vIntervals
            # print str(vq)
            # i=1/0

        def append_LinesOfBlastRes_by_vq(self, vq):
            n = len(self.LinesOfBlastRes)
            nvq = len(vq)
            # if nvq>10:
            # 	nnn=
            if n > 0:
                myLineOfBlastRes = self.LinesOfBlastRes[n - 1]
                iq = 0
                for q in vq:
                    myLineOfBlastRes1 = myLineOfBlastRes.copy()
                    myLineOfBlastRes1.startQ = q[0]
                    myLineOfBlastRes1.endQ = q[1]
                    # myLineOfBlastRes1.startDB=q[2]
                    # myLineOfBlastRes1.endDB=q[3]
                    myLineOfBlastRes1.nLen = abs(q[1] - q[0] + 1)
                    # print str(iq)+" "+str(myLineOfBlastRes1)
                    self.LinesOfBlastRes.append(myLineOfBlastRes1)
                    iq += 1
            # i=1/0

        # vsDB,vnLen,vnM,vnD,vstartQ,vendQ,vstartDB,vendDB,vsEval,vsmLogP
        def vsDB_get(self):
            vsDB = []
            for LineOfBlastRes in self.LinesOfBlastRes:
                vsDB.append(LineOfBlastRes.sDB)
            return vsDB

        def vnLen_get(self):
            vnLen = []
            for LineOfBlastRes in self.LinesOfBlastRes:
                vnLen.append(LineOfBlastRes.nLen)
            return vnLen

        def vstartQ_get(self):
            vstartQ = []
            for LineOfBlastRes in self.LinesOfBlastRes:
                vstartQ.append(LineOfBlastRes.startQ)
            return vstartQ

        def vendQ_get(self):
            vendQ = []
            for LineOfBlastRes in self.LinesOfBlastRes:
                vendQ.append(LineOfBlastRes.endQ)
            return vendQ

        def vstartDB_get(self):
            vstartDB = []
            for LineOfBlastRes in self.LinesOfBlastRes:
                vstartDB.append(LineOfBlastRes.startDB)
            return vstartDB

        def vendDB_get(self):
            vendDB = []
            for LineOfBlastRes in self.LinesOfBlastRes:
                vendDB.append(LineOfBlastRes.endDB)
            return vendDB

        def makeArrays(self):
            # print "makeArrays"
            self.vsDB = self.vsDB_get()  # contig names from in Cnig_gn1
            self.vnLen = self.vnLen_get()
            self.vstartQ = self.vstartQ_get()
            self.vendQ = self.vendQ_get()
            self.vstartDB = self.vstartDB_get()
            self.vendDB = self.vendDB_get()

        def sCtgDB_coorCtgDB_qqqq_get(self, coor):  # sCtgDB,coorCtgDB,qqqq=
            n = len(self.vsDB)
            qqq = []  # array of [index in vsDB, coor ctgDB, length of overlap]
            for i in range(n):
                if coor >= self.vstartQ[i] and coor <= self.vendQ[i]:
                    # coorDB=self.attachMarkersToAnotherAssembly_simple___coorDB(coor,vstartQ[i],vstartDB[i],vendDB[i])
                    # self.makeArrays()
                    coorDB = self.LinesOfBlastRes[i].coorDB_get(coor, -1)
                    i_vsDB = self.vsDB.index(
                        self.vsDB[i]
                    )  # index in vsDB (i_vsDB <= i: unique => "=", else the most significant (first in the list))
                    qqq.append(
                        [i_vsDB, coorDB, self.vnLen[i]]
                    )  # [index in vsDB, coor ctgDB, length of overlap]

            # select from qqq only the longest overlap for each ctg from Cnig_gn1
            def MyFunc(q):
                return (
                    q[0] * 1000000000 - q[2]
                )  # i_vsDB*100000000 - <length of overlap>

            qqq.sort(key=MyFunc)
            qqqq = []
            i_vsDB_done = -1
            for q in qqq:
                i_vsDB = q[0]
                if i_vsDB > i_vsDB_done:
                    qqqq.append(q)
                    i_vsDB_done = i_vsDB

            # sort by length overlap (longest to shorter)
            if len(qqqq) > 1:

                def MyFunc1(q):
                    return -q[2]  # i_vsDB*100000000 - <length of overlap>

                qqqq.sort(key=MyFunc1)

            sCtgDB = ""
            coorCtgDB = -1
            if len(qqqq) > 0:
                q = qqqq[0]
                sCtgDB = self.vsDB[q[0]]
                coorCtgDB = q[1]
                lengthOfOverlap_ctgQ_ctgDB = q[2]
            return sCtgDB, coorCtgDB, qqqq

    class clOverlapOfQuaryWithSequencesOfDB:
        # blockOfBlastResults_intervalsOnQ
        def __init__(self, sQ="", nOverlapsMAX=4):
            self.sQ = sQ  # Quary name
            # print "len="+str(len(LinesOfBlastRes.LinesOfBlastRes))
            # print "sQ="+self.sQ
            self.vsDBnoRepeats = []  # list of sDB without repeats

            self.vOverlapOfQuaryWithCtgOfDB = (
                []
            )  # array of clOverlapOfQuaryWithCtgOfDB, one per CtgOfDB (from self.vsDBnoRepeats)

            self.vIntervalFromAllsDB_ends = []
            self.dCovered1 = 0  # total length of single sDB overlap
            self.dCovered2andMore = 0  # total length covered by more than one sDB
            self.vvCovered = (
                []
            )  # list of sDB covering interval ie, array of [iStart,iEnd,k,vsDBCovering]
            self.nOverlapsMAX = nOverlapsMAX  # cutoff to define multicoverage
            self.vqq = []  # array of [iStart,iEnd,coverage1orMore1]

            # parts of 50000 bp
            self.vvsDB = []
            self.lenPart = 50000
            self.minProc = 0.6
            self.lenCtgQ = -1  # not defined
            self.vdCovered1 = []  # length of single sDB overlap
            self.vdCovered2andMore = []  # length covered by more than one sDB

        def update_vvsDB(self, sDB, vq):
            print("update_vvsDB...")
            nnn = len(self.vvsDB)
            if nnn == 0:
                lll = self.lenCtgQ
                while lll > self.lenPart * self.minProc:
                    lll -= self.lenPart
                    self.vvsDB.append([])
                nnn = len(self.vvsDB)
            vlen = []
            for i in range(nnn + 1):
                vlen.append(0)
            # print "7172: nnn="+str(nnn)+" sDB="+sDB+" sQ="+self.sQ
            for q in vq:
                i = int((q[0] - 1) / self.lenPart)
                x1 = (i + 1) * self.lenPart
                x0 = q[0]
                while x1 < q[1]:
                    d = x1 - x0 + 1
                    if i >= nnn:
                        print(
                            "q="
                            + str(q)
                            + ", i="
                            + str(i)
                            + ", lenCtgQ="
                            + str(self.lenCtgQ)
                        )
                    vlen[i] += d
                    x0 = x1
                    i += 1
                    x1 = (i + 1) * self.lenPart
                d = q[1] - x0 + 1
                vlen[i] += d
            if len(vq) > 0:
                for i in range(nnn):
                    if vlen[i] >= self.lenPart * self.minProc:
                        if not (sDB in self.vvsDB[i]):
                            self.vvsDB[i].append(sDB)
            print("update_vvsDB...Finished")

        def update_vdCovered(self):
            print("update_vdCovered...")
            self.dCovered1 = 0  # total length of single sDB overlap
            self.dCovered2andMore = 0  # total length covered by more than one sDB

            nnn = len(self.vvsDB)
            self.vdCovered1 = []  # length of single sDB overlap
            self.vdCovered2andMore = []  # length covered by more than one sDB
            for i in range(nnn):
                self.vdCovered1.append(0)
                self.vdCovered2andMore.append(0)
            for qq in self.vqq:
                k = qq[2]
                d = qq[1] - qq[0] + 1
                if k == 1:
                    self.dCovered1 += d
                else:
                    self.dCovered2andMore += d

                # by parts
                vlen = self.vdCovered1 if k == 1 else self.vdCovered2andMore
                i = int((qq[0] - 1) / self.lenPart)
                x1 = (i + 1) * self.lenPart
                x0 = qq[0]
                while x1 < qq[1]:
                    d = x1 - x0 + 1
                    if i < nnn:
                        vlen[i] += d
                        if self.vdCovered1[i] > self.lenPart + 1:
                            print(str(qq))
                            print("i=" + str(i))
                            print(str(self.vqq[0:10]))
                            i = 1 / 0
                    x0 = x1
                    x1 += self.lenPart
                    i += 1
                d = qq[1] - x0 + 1
                if i < nnn:
                    vlen[i] += d
            print("update_vdCovered...Finished")

        def add_sDB(self, sDB, vq):
            print("add_sDB...")

            def MyFunc(q):
                return q[0]

            self.vsDBnoRepeats.append(sDB)
            for q in vq:
                qq = [q[0], q[1], 1]
                self.vqq.append(qq)
            if len(self.vqq) > 1:
                self.vqq.sort(key=MyFunc)
                vqq = self.vqq
                self.vqq = []
                qqPrev = vqq[0]
                endMore1 = 0 if qqPrev[2] == 1 else qqPrev[1]
                iqq = 0
                for qq in vqq:
                    # print "qqPrev="+str(qqPrev)+" qq="+str(qq)+" endMore1="+str(endMore1)
                    if iqq > 0:
                        if qq[0] <= qqPrev[1]:
                            # *******
                            #    *******
                            if qq[1] <= endMore1:
                                # ======----
                                #  ***
                                # print "7258"
                                pass
                                # ======----
                            else:
                                if qq[0] <= endMore1:
                                    # ======------
                                    #  *******??????
                                    if qqPrev[1] >= qq[1]:
                                        # ======------
                                        #  *******
                                        endMore1 = qq[1]
                                        # =========---
                                        # print "7270"
                                    else:
                                        # ======------
                                        #  ****************
                                        endMore1 = qqPrev[1] if qq[2] == 1 else qq[1]
                                        qqPrev[1] = qq[1]
                                        # ============******
                                        # print "7277"
                                else:
                                    # ======------
                                    #        **?????
                                    self.add_sDB___update_vqq(
                                        qqPrev[0], qq[0] - 1, endMore1
                                    )
                                    qqPrev[0] = qq[0]
                                    if qq[1] <= qqPrev[1]:
                                        #    ----
                                        #    **
                                        endMore1 = qq[1]
                                        #    ==--
                                        # print "7288"
                                    else:
                                        #    ----
                                        #    *******
                                        endMore1 = qqPrev[1] if qq[2] == 1 else qq[1]
                                        qqPrev[1] = qq[1]
                                        #    ====***
                                        # print "7295"
                        else:
                            # ======------
                            #               ***
                            self.add_sDB___update_vqq(qqPrev[0], qqPrev[1], endMore1)
                            qqPrev = qq
                            endMore1 = qqPrev[0] - 1 if qqPrev[2] == 1 else qqPrev[1]
                            # print "7301"
                    iqq += 1
                self.add_sDB___update_vqq(qqPrev[0], qqPrev[1], endMore1)
                # print "7304"
            print("add_sDB...Finished")

        def add_sDB___update_vqq(self, iStart, iEnd, endMore1):
            # ===-------
            if iStart <= endMore1:
                # ===
                qq = [iStart, endMore1, 2]
                self.vqq.append(qq)
                # print "7304: qq="+str(qq)
            if endMore1 + 1 <= iEnd:
                # -------
                qq = [endMore1 + 1, iEnd, 1]
                self.vqq.append(qq)
                # print "7309: qq="+str(qq)
            n = len(self.vqq)
            if n > 1:
                if self.vqq[n - 1][0] < self.vqq[n - 2][0]:
                    i = 1 / 0

        class clOverlapOfQuaryWithCtgOfDB:  # one quary with one ctgOfDB (can be based on several lines)
            def __init__(self, sDB):
                self.sDB = sDB
                self.vIntervalsOnCtgQuary = (
                    []
                )  # vvIntervalsOnCtgQuary=[]#lists of intervals on Quary
                self.vIntervalsOnCtgQuaryPP = (
                    []
                )  # lists of intervals on Quary (non-overlapped within one sDB)
                self.MinPosOnQ = 1000000000
                self.MaxPosOnQ = -1

                # poka: predpolagaem chto ctgQ presented only in one region of sDB
                self.MinPosOnQ_excludedMultiCoverage = 1000000000
                self.MaxPosOnQ_excludedMultiCoverage = -1

                self.generalOrientation = 0  # undefined
                self.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage = -1
                self.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage = -1

                self.sFirstStringOfNextBlockOfFastaResult = ""
                self.bNotTheLastBlock = False

            def readFromBlockOfRowsOfBlastResFile_sQ_sDB_vq(
                self, sFirstStringOfBlockOfFastaResult, f
            ):  # sQ,sDB,vq,exitCode=    (here q=[iStart,iEnd])
                vq = (
                    []
                )  # array of intervals [iStart,iEnd] poka: ne smotrim coordinates on DB

                def compress_vq(vq):
                    def MyFunc(q):
                        # return -(q[1]-q[0]+1)
                        return q[0]

                    n = len(vq)
                    if n > 1:
                        vq.sort(key=MyFunc)
                        vqCompressed = []
                        qPrev = vq[0]
                        for q in vq:
                            if q[0] <= qPrev[1]:
                                if q[1] > qPrev[1]:
                                    qPrev[1] = q[1]
                            else:
                                vqCompressed.append(qPrev)
                                qPrev = q
                        vqCompressed.append(qPrev)
                        vq = vqCompressed
                    # print str(vq)
                    # i=1/0

                def faster_q(s):  # sQ,sDB,q
                    ss = s.split("\t")
                    return ss[0], ss[1], [int(ss[6]), int(ss[7])]  # sQ,sDB,q

                myBlastRes = clBlastRes()
                sQ = ""
                sDB = ""
                nLines = 0
                # print sFirstStringOfBlockOfFastaResult
                if sFirstStringOfBlockOfFastaResult != "":
                    myLineOfBlastRes = myBlastRes.clLineOfBlastRes(
                        sFirstStringOfBlockOfFastaResult
                    )
                    sQ = myLineOfBlastRes.sQ
                    sDB = myLineOfBlastRes.sDB
                    vq.append(myLineOfBlastRes.q())
                    nLines += 1
                    # print "sQ(5167)="+sQ
                    # print "vq="+str(vq)
                self.sFirstStringOfNextBlockOfFastaResult = ""
                self.bNotTheLastBlock = False

                s = f.readline()
                exitCode = 0  # file is finished
                while s:
                    bNeedToReadNextLine = True
                    if len(s) > 1:
                        if s[0] != "#":  # no need rows with comments
                            nLines += 1
                            if nLines % 10000 == 9999:
                                print(str(nLines + 1))
                                compress_vq(vq)
                                print("compressed to " + str(len(vq)) + " parts")
                                # print "len(vq)="+str(len(vq))
                            if False:
                                myLineOfBlastRes = myBlastRes.clLineOfBlastRes(s)
                                # sQnext,sDB,nLen,nM,nD,startQ,endQ,startDB,endDB,sEval,smLogP=clLineOfBlastRes(s)
                                s_q = myLineOfBlastRes.q()
                                s_sQ = myLineOfBlastRes.sQ
                                s_sDB = myLineOfBlastRes.sDB
                            s_sQ, s_sDB, s_q = faster_q(s)
                            if sQ == "":
                                sQ = s_sQ
                                sDB = s_sDB
                                # print "sQ(5180)="+sQ
                            # print "sQ="+sQ+","+s_sQ+"   sDB="+sDB+","+s_sDB
                            if s_sQ == sQ and s_sDB == sDB:
                                if s_q[1] - s_q[0] > 2500:
                                    vq.append(s_q)
                            else:
                                if s_sQ != sQ:
                                    exitCode = 1  # next sQ
                                else:
                                    exitCode = 2  # next sDB
                                self.sFirstStringOfNextBlockOfFastaResult = s
                                # print "?"
                                self.bNotTheLastBlock = True
                                bNeedToReadNextLine = False
                            # sFirstStringOfBlockOfFastaResult=s
                    if bNeedToReadNextLine:
                        s = f.readline()
                    else:
                        s = False
                    # print str(nLines+1)+"end of block"
                    compress_vq(vq)
                # print "nLines="+str(nLines)
                # print self.sFirstStringOfNextBlockOfFastaResult
                print("Finished " + sDB + " for " + sQ)
                return sQ, sDB, vq, exitCode, nLines

            def vIntervalsOnCtgQuaryPP_make(
                self, vIntervalFromAllsDB_ends
            ):  # ,vIntervalsOnCtgQuaryPPMinAndMax,vIntervalsOnCtgQuaryPPMinAndMaxSorted
                # NB! hard in case of too many overlaps
                def MyFunc(q):
                    # sort intervals by left end, the longest are first
                    return q[0] - 0.000000001 * (q[1] - q[0])

                def vIntervalsOnCtgQuaryPP_and_vIntervalFromAllsDB_ends_update(
                    vIntervalsOnCtgQuaryPP, iStart, iEnd, vIntervalFromAllsDB_ends
                ):
                    self.vIntervalsOnCtgQuaryPP.append([iStart, iEnd])
                    # vIntervalFromAllsDB.append([iStart,iEnd])
                    if not (iStart in vIntervalFromAllsDB_ends):
                        vIntervalFromAllsDB_ends.append(iStart)
                    if not ((iEnd + 1) in vIntervalFromAllsDB_ends):
                        vIntervalFromAllsDB_ends.append((iEnd + 1))

                self.vIntervalsOnCtgQuary.sort(key=MyFunc)

                # vIntervalFromAllsDB_ends is array of all interval ends (ordered, no repeats)
                iStart = -1
                iEnd = -1
                nq = len(self.vIntervalsOnCtgQuary)
                iq = 0
                for q in self.vIntervalsOnCtgQuary:
                    if iq == 0:
                        iStart = q[0]
                        iEnd = q[1]
                    if q[0] > iEnd + 1:  # new interval
                        vIntervalsOnCtgQuaryPP_and_vIntervalFromAllsDB_ends_update(
                            self.vIntervalsOnCtgQuaryPP,
                            iStart,
                            iEnd,
                            vIntervalFromAllsDB_ends,
                        )
                        iStart = q[0]
                    else:
                        # print str(iq)+"\t"+str(nq)+"\t"+str(q)+"\t"+str(iStart)+"\t"+str(iEnd)
                        pass
                    iEnd = q[1]
                    if iq == nq - 1:
                        vIntervalsOnCtgQuaryPP_and_vIntervalFromAllsDB_ends_update(
                            self.vIntervalsOnCtgQuaryPP,
                            iStart,
                            iEnd,
                            vIntervalFromAllsDB_ends,
                        )
                    iq += 1

                iStart = -1
                iEnd = -1
                lenvIntervalsOnCtgQuaryPP = len(self.vIntervalsOnCtgQuaryPP)
                if lenvIntervalsOnCtgQuaryPP > 0:  # vsegda
                    self.MinPosOnQ = self.vIntervalsOnCtgQuaryPP[0][0]
                    self.MaxPosOnQ = self.vIntervalsOnCtgQuaryPP[
                        lenvIntervalsOnCtgQuaryPP - 1
                    ][1]

            def bPresentedAfterExcludedMultiCoverage(self):
                # print "3762"
                b = (
                    self.MinPosOnQ_excludedMultiCoverage
                    < self.MaxPosOnQ_excludedMultiCoverage
                )
                # print "3764"+str(b)+"<-"
                return b

            def PosOnCtgDB(self, vsDB, vstartQ, vendQ, vstartDB, vendDB):
                # self.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage
                # self.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage
                # self.generalOrientation

                iRow = 0
                mymath = clVovaMath()
                x_min = self.MinPosOnQ_excludedMultiCoverage
                x_max = self.MaxPosOnQ_excludedMultiCoverage
                for sDB in vsDB:
                    if sDB == self.sDB:
                        x1 = vstartQ[iRow]
                        x2 = vendQ[iRow]
                        y1 = vstartDB[iRow]
                        y2 = vendDB[iRow]
                        if self.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage < 0:
                            if x_min >= x1 and x_min <= x2:
                                self.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage = int(
                                    mymath.yByLin(x1, y1, x2, y2, x_min)
                                )
                        if self.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage < 0:
                            if x_max >= x1 and x_max <= x2:
                                self.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage = int(
                                    mymath.yByLin(x1, y1, x2, y2, x_max)
                                )
                    iRow += 1

                # self.generalOrientation
                if (
                    self.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage >= 0
                    and self.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage >= 0
                ):
                    self.generalOrientation = (
                        1
                        if (
                            self.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage
                            > self.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage
                        )
                        else -1
                    )

        def processBlockOfBlastResults_simple(
            self, sFirstStringOfBlockOfFastaResult, f, myFastaQ
        ):  # exitCode,sFirstStringOfBlockOfFastaResult=
            print("processBlockOfBlastResults_simple...")
            nLines = 0
            myBlastRes = clBlastRes()
            overlap = self.clOverlapOfQuaryWithCtgOfDB("")  # sDB
            (
                sQ_prev,
                sDB,
                vq,
                exitCode,
                nLinesBlock,
            ) = overlap.readFromBlockOfRowsOfBlastResFile_sQ_sDB_vq(
                sFirstStringOfBlockOfFastaResult, f
            )

            nLines += nLinesBlock
            print("start of Block " + str(nLines) + " lines: sQ=" + sQ_prev)
            nLinesPrev = nLines

            iCtgQ = myFastaQ.vCtgName.index(sQ_prev)
            self.lenCtgQ = myFastaQ.vCtg[iCtgQ].seqLength
            self.sQ = sQ_prev
            self.update_vvsDB(sDB, vq)
            self.add_sDB(sDB, vq)
            exitCode = 0  # end of file
            if overlap.bNotTheLastBlock:
                exitCode = 1
                sFirstStringOfBlockOfFastaResult = (
                    overlap.sFirstStringOfNextBlockOfFastaResult
                )
                myLineOfBlastRes = myBlastRes.clLineOfBlastRes(
                    sFirstStringOfBlockOfFastaResult
                )
                sQ = myLineOfBlastRes.sQ
                while sQ == sQ_prev and exitCode == 1:
                    (
                        sQ_prev,
                        sDB,
                        vq,
                        exitCode,
                        nLinesBlock,
                    ) = overlap.readFromBlockOfRowsOfBlastResFile_sQ_sDB_vq(
                        sFirstStringOfBlockOfFastaResult, f
                    )
                    nLines += nLinesBlock
                    if nLinesPrev + 100000 < nLines:
                        print("added 100,000 lines")
                        nLinesPrev = nLines

                    self.update_vvsDB(sDB, vq)
                    self.add_sDB(sDB, vq)
                    exitCode = 0  # end of file
                    if overlap.bNotTheLastBlock:
                        exitCode = 1
                        sFirstStringOfBlockOfFastaResult = (
                            overlap.sFirstStringOfNextBlockOfFastaResult
                        )
                        myLineOfBlastRes = myBlastRes.clLineOfBlastRes(
                            sFirstStringOfBlockOfFastaResult
                        )
                        sQ = myLineOfBlastRes.sQ
            self.update_vdCovered()
            print("processBlockOfBlastResults_simple...Finished")
            return exitCode, sFirstStringOfBlockOfFastaResult

        def processBlockOfBlastResults_simple_print(self, f):
            i = 0
            for vsDB in self.vvsDB:
                d = self.vdCovered1[i] + self.vdCovered2andMore[i]
                s = (
                    str(i)
                    + "\t"
                    + str(i * self.lenPart)
                    + "\t"
                    + str((i + 1) * self.lenPart)
                    + "\t"
                    + str(self.lenPart)
                )
                s += (
                    "\t"
                    + str(self.vdCovered1[i])
                    + "\t"
                    + str(self.vdCovered2andMore[i])
                    + "\t"
                    + str(float(d) / self.lenPart)
                )
                s += "\t" + str(len(vsDB)) + "\t" + str(vsDB)
                f.write(s + "\n")
                i += 1

        def processBlockOfBlastResults_simple_print_shapka(self, f):
            s = "iPart" + "\t" + "iStart" + "\t" + "iEnd" + "\t" + "len"
            s += "\t" + "len_d1" + "\t" + "len_d>1" + "\t" + "pCov"
            s += "\t" + "n>60%" + "\t" + "sDB"
            f.write(s + "\n")

        def processBlockOfBlastResults(self, LinesOfBlastRes):
            vsDB = LinesOfBlastRes.vsDB_get()
            vstartQ = LinesOfBlastRes.vstartQ_get()
            vendQ = LinesOfBlastRes.vendQ_get()
            vstartDB = LinesOfBlastRes.vstartDB_get()
            vendDB = LinesOfBlastRes.vendDB_get()

            self.vsDBnoRepeats = []
            self.vOverlapOfQuaryWithCtgOfDB = []
            for sDB in vsDB:
                if not (sDB in self.vsDBnoRepeats):
                    self.vsDBnoRepeats.append(sDB)
                    self.vOverlapOfQuaryWithCtgOfDB.append(
                        self.clOverlapOfQuaryWithCtgOfDB(sDB)
                    )  # define class (element of array)

            # self.vOverlapOfQuaryWithCtgOfDB[idsDB].vIntervalsOnCtgQuary[]
            nRows = len(vsDB)
            for i in range(nRows):
                startQ = vstartQ[i]
                endQ = vendQ[i]
                posOnCtgMinOVLP = min([startQ, endQ])
                posOnCtgMaxOVLP = max([startQ, endQ])

                idsDB = self.vsDBnoRepeats.index(vsDB[i])
                self.vOverlapOfQuaryWithCtgOfDB[idsDB].vIntervalsOnCtgQuary.append(
                    [posOnCtgMinOVLP, posOnCtgMaxOVLP]
                )

            # self.vOverlapOfQuaryWithCtgOfDB[idsDB].vIntervalsOnCtgQuaryPP[]
            nCtgsDB = len(self.vsDBnoRepeats)
            for idsDB in range(nCtgsDB):
                self.vOverlapOfQuaryWithCtgOfDB[idsDB].vIntervalsOnCtgQuaryPP_make(
                    self.vIntervalFromAllsDB_ends
                )  # self.vIntervalsOnCtgQuaryPPMinAndMax,self.vIntervalsOnCtgQuaryPPMinAndMaxSorted

            self.vIntervalFromAllsDB_ends.sort()

            # self.vvCovered
            # self.vOverlapOfQuaryWithCtgOfDB[iDBCovering].MinPosOnQ_excludedMultiCoverage
            # self.vOverlapOfQuaryWithCtgOfDB[iDBCovering].MaxPosOnQ_excludedMultiCoverage
            self.dCoveredCalc()

            for OverlapOfQuaryWithCtgOfDB in self.vOverlapOfQuaryWithCtgOfDB:
                if OverlapOfQuaryWithCtgOfDB.bPresentedAfterExcludedMultiCoverage():
                    OverlapOfQuaryWithCtgOfDB.PosOnCtgDB(
                        vsDB, vstartQ, vendQ, vstartDB, vendDB
                    )
                    # self.vOverlapOfQuaryWithCtgOfDBok.append(OverlapOfQuaryWithCtgOfDB)
            # print str(self.vIntervalFromAllsDB_ends)
            pass

        def dCoveredCalc(self):
            ne = len(self.vIntervalFromAllsDB_ends) - 1
            nCtgsDB = len(self.vsDBnoRepeats)
            if ne > 0:
                for ie in range(ne):  # on all ntervals
                    iStart = self.vIntervalFromAllsDB_ends[ie]
                    iEnd = self.vIntervalFromAllsDB_ends[ie + 1] - 1
                    d = iEnd - iStart + 1
                    nOverlaps = 0
                    vsDBCovering = []
                    viDBCovering = []

                    # for q in vIntervalFromAllsDB:
                    iDB = 0
                    for OverlapOfQuaryWithCtgOfDB in self.vOverlapOfQuaryWithCtgOfDB:
                        for q in OverlapOfQuaryWithCtgOfDB.vIntervalsOnCtgQuaryPP:
                            b = True
                            if q[0] > iEnd or q[1] < iStart:
                                b = False
                            if b:
                                nOverlaps += 1
                                vsDBCovering.append(OverlapOfQuaryWithCtgOfDB.sDB)
                                viDBCovering.append(iDB)
                        iDB += 1

                    if nOverlaps > 0:
                        if nOverlaps == 1:
                            self.dCovered1 += d
                        else:
                            self.dCovered2andMore += d
                        self.vvCovered.append([iStart, iEnd, nOverlaps, vsDBCovering])

                    if nOverlaps > 0 and nOverlaps < self.nOverlapsMAX and d >= 50:
                        for iDBCovering in viDBCovering:
                            if (
                                self.vOverlapOfQuaryWithCtgOfDB[
                                    iDBCovering
                                ].MinPosOnQ_excludedMultiCoverage
                                > iStart
                            ):
                                self.vOverlapOfQuaryWithCtgOfDB[
                                    iDBCovering
                                ].MinPosOnQ_excludedMultiCoverage = iStart
                            if (
                                self.vOverlapOfQuaryWithCtgOfDB[
                                    iDBCovering
                                ].MaxPosOnQ_excludedMultiCoverage
                                < iEnd
                            ):
                                self.vOverlapOfQuaryWithCtgOfDB[
                                    iDBCovering
                                ].MaxPosOnQ_excludedMultiCoverage = iEnd
            # for OverlapOfQuaryWithCtgOfDB in self.vOverlapOfQuaryWithCtgOfDB:
            # 	.MaxPosOnQ_excludedMultiCoverage
            pass

        def s_shapka(self, bDetails=True):
            s = (
                "sQ"
                + "\t"
                + "dCovered1"
                + "\t"
                + "dCovered2andMore"
                + "\t"
                + "[MinMaxFor_sDB: [xMin,xMax,sDB,yMin,yMax,generalOrientation,xL,yL]]"
                + "\t"
                + "{intervals_sDB}"
                + "\t"
                + "all intervals: {iStart,iEnd:coverage:vsDBCovering}"
            )
            return s

        def s_get(self, bDetails=True):
            def MyFunc(q):
                # sort intervals by left end, the longest are first
                return q[0] - 0.000000001 * (q[1] - q[0])

            vvIntervalsOnCtgQuaryPPMinAndMaxSorted = []
            # print "3833 "+str(len(self.vOverlapOfQuaryWithCtgOfDB))
            for OverlapOfQuaryWithCtgOfDB in self.vOverlapOfQuaryWithCtgOfDB:
                # print "3835"
                if OverlapOfQuaryWithCtgOfDB.bPresentedAfterExcludedMultiCoverage():
                    # print "3837"
                    xMin = OverlapOfQuaryWithCtgOfDB.MinPosOnQ_excludedMultiCoverage
                    xMax = OverlapOfQuaryWithCtgOfDB.MaxPosOnQ_excludedMultiCoverage
                    sDB = OverlapOfQuaryWithCtgOfDB.sDB
                    yMin = (
                        OverlapOfQuaryWithCtgOfDB.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage
                    )
                    yMax = (
                        OverlapOfQuaryWithCtgOfDB.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage
                    )
                    generalOrientation = OverlapOfQuaryWithCtgOfDB.generalOrientation
                    xL = abs(xMax - xMin) + 1
                    yL = abs(yMax - yMin) + 1
                    q = [xMin, xMax, sDB, yMin, yMax, generalOrientation, xL, yL]
                    vvIntervalsOnCtgQuaryPPMinAndMaxSorted.append(q)
                # print "3839"
            vvIntervalsOnCtgQuaryPPMinAndMaxSorted.sort(key=MyFunc)

            # "sQ"+"\t"+"dCovered1"+"\t"+"dCovered2andMore"
            s = self.sQ
            s += "\t" + str(self.dCovered1)
            s += "\t" + str(self.dCovered2andMore)

            # "[MinMaxFor_sDB]"
            s1 = ""
            # for q in vvIntervalsOnCtgQuaryPPMinAndMax:
            for q in vvIntervalsOnCtgQuaryPPMinAndMaxSorted:
                s1 += str(q)
            s += "\t[" + s1 + "]"

            # "{intervals_sDB}" intervals without multicoverage
            s1 = ""
            for OverlapOfQuaryWithCtgOfDB in self.vOverlapOfQuaryWithCtgOfDB:
                if OverlapOfQuaryWithCtgOfDB.bPresentedAfterExcludedMultiCoverage():
                    vIntervals = OverlapOfQuaryWithCtgOfDB.vIntervalsOnCtgQuaryPP
                    ss1 = "{"
                    for q in vIntervals:
                        ss1 += str(q)
                    ss1 += "}"
                    s1 += ss1
            if s1 == "":
                s1 = "all are MultiCoverage"
            s += "\t" + s1

            # "all intervals"
            s2 = ""
            nIntervalsOnQ = len(self.vvCovered)
            if nIntervalsOnQ < 10:
                for vCovered in self.vvCovered:
                    iStart = vCovered[0]
                    iEnd = vCovered[1]
                    k = vCovered[2]
                    vsDBCovering = vCovered[3]
                    ss2 = (
                        "{"
                        + str(iStart)
                        + ","
                        + str(iEnd)
                        + ":"
                        + str(k)
                        + ":"
                        + str(vsDBCovering)
                    )
                    ss2 += "}"
                    s2 += ss2
            else:
                s2 = str(nIntervalsOnQ) + " intervals"
            s += "\t" + s2

            return s

    def uniteBlasResToSingleFile(self):
        sPath = "C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\res_Cnig_gn1_vs_FormicaSelysi"
        mm = clVovaServ()
        sFileNameAll = "res_Cnig_gn1_vs_FormicaSelysi_e70.out"
        mm.mergeFiles(sPath, True, ".out", sFileNameAll, False)

    def vsQ_get(self, sFileName_blastRes):  # vsQ=
        print("vsQ_get...")
        vsQ = []
        f = open(sFileName_blastRes, "r")

        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        # markersOnRefGenome=[]
        bPrintDetails = False
        while bContinue:
            iBlock += 1
            if bPrintDetails:
                if iBlock % 100 == 1:
                    pass
            LinesOfBlastRes = self.clLinesOfBlastRes(
                sFirstStringOfBlockOfFastaResult, f
            )
            vsQ.append(LinesOfBlastRes.sQ)
            sFirstStringOfBlockOfFastaResult = (
                LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
            )
            bContinue = LinesOfBlastRes.bNotTheLastBlock
        f.close()
        print("vsQ_get...Done")
        return vsQ

    def LinesOfBlastRes_for_sQ(
        self,
        sQ,
        sQ_prev,
        LinesOfBlastRes_prev,
        f,
        sFirstStringOfBlockOfFastaResult,
        bContinue,
        iBlock,
    ):  # LinesOfBlastRes,sQ_prev,sFirstStringOfBlockOfFastaResult,bContinue,iBlock=
        if sQ == sQ_prev:
            return (
                LinesOfBlastRes_prev,
                sQ,
                sFirstStringOfBlockOfFastaResult,
                bContinue,
                iBlock,
            )
        bFound = False
        bPrintDetails = False
        while bContinue and not bFound:
            iBlock += 1
            if bPrintDetails:
                if iBlock % 100 == 1:
                    pass
            LinesOfBlastRes = self.clLinesOfBlastRes(
                sFirstStringOfBlockOfFastaResult, f
            )
            sFirstStringOfBlockOfFastaResult = (
                LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
            )
            bContinue = LinesOfBlastRes.bNotTheLastBlock
            if LinesOfBlastRes.sQ == sQ:
                bFound = True
                LinesOfBlastRes.makeArrays()
                return (
                    LinesOfBlastRes,
                    sQ,
                    sFirstStringOfBlockOfFastaResult,
                    bContinue,
                    iBlock,
                )
        # if not bFound:
        LinesOfBlastRes = self.clLinesOfBlastRes("no need", f)
        return LinesOfBlastRes, sQ, sFirstStringOfBlockOfFastaResult, bContinue, iBlock


class clBlastResFormat0:
    def __init__(self, SecCtgs):
        self.quaries = SecCtgs
        self.vMarker = []
        self.vBLASTinterval = []

    class clMarker:
        def __init__(
            self, sQueryShortName, iCtg, iPos, sRefAllele, sAltAllele, iBLASTinterval
        ):
            self.sQueryShortName = sQueryShortName
            self.iCtg = iCtg
            self.iPos = iPos
            self.sRefAllele = sRefAllele
            self.sAltAllele = sAltAllele
            self.iBLASTinterval = iBLASTinterval

        def shapka(self):
            return (
                "sQ" + "\t" + "iPos" + "\t" + "m" + "\t" + "M" + "\t" + "iBLASTinterval"
            )

        def s(self):
            s = self.sQueryShortName + "\t" + str(self.iPos)
            s += (
                "\t"
                + self.sRefAllele
                + "\t"
                + self.sAltAllele
                + "\t"
                + str(self.iBLASTinterval)
            )
            return s

        # def copy(self):
        # 	BlastResFormat0=clBlastResFormat0()
        # 	Marker=BlastResFormat0.clMarker(self.sQueryShortName,self.iCtg,self.iPos,self.sRefAllele,sAltAllele)

    class clBLASTinterval:
        def __init__(self, iCtg, iPosStart, iPosEnd):
            self.iCtg = iCtg
            self.iPosStart = iPosStart
            self.iPosEnd = iPosEnd

        def shapka(self):
            return "iCtg" + "\t" + "iPosStart" + "\t" + "iPosEnd"

        def s(self):
            return (
                str(self.iCtg) + "\t" + str(self.iPosStart) + "\t" + str(self.iPosEnd)
            )

    def makeListOfMarkersBasedOnBlastRes(self, sFileBlastResFormat0):
        # ...
        # Query= JAEQMK010000016.1 Solenopsis invicta isolate M01_SB chromosome 16,
        # ...
        # Query  20587021  atatatatatatatatacacatatatatatTTTAT--AATTATAACTAGTTGCATTGATA  20587080
        #                 ||||||||||||||| | | |||||||||||||||  ||||| |||||||||||||||||
        # Sbjct  4970994   ATATATATATATATACATATATATATATATTTTATGGAATTA-AACTAGTTGCATTGATA  4970935
        def sSeqQName_get(s):
            # Query= JAEQMK010000016.1 Solenopsis invicta isolate M01_SB chromosome 16,
            ss = s.split(" ")
            return ss[1]  # JAEQMK010000016.1

        def processIndel(
            prevIndel, n0, n, sQ, sDB, prevIndel_sRefAllele, prevIndel_sAltAllele
        ):
            # sQ ="atatatatatatatatacacatatatatatTTTAT--AATTATAACTAGTTGCATTGATA"
            # sDB="ATATATATATATATACATATATATATATATTTTATGGAATTA-AACTAGTTGCATTGATA"
            k = 0
            if prevIndel > 0:
                for i in range(n0, n):
                    if sQ[i] == "-":
                        k += 1
                    else:
                        break
                if k > 0:
                    prevIndel_sAltAllele = prevIndel_sAltAllele + sDB[n0 : n0 + k]
            else:
                for i in range(n0, n):
                    if sDB[i] == "-":
                        k += 1
                    else:
                        break
                if k > 0:
                    prevIndel_sRefAllele = prevIndel_sRefAllele + sQ[n0 : n0 + k]
            # print "k="+str(k)+"\tn0="+str(n0)+"\tprevIndel_sRefAllele="+prevIndel_sRefAllele+"\tprevIndel_sAltAllele="+prevIndel_sAltAllele
            # i=1/0
            return k, prevIndel_sRefAllele, prevIndel_sAltAllele

        def processBlock_fast(
            sQ,
            sCorr,
            sDB,
            iStart,
            sQueryShortName,
            iCtg,
            prevIndel,
            prevIndel_iPos,
            prevIndel_len,
            prevIndel_sRefAllele,
            prevIndel_sAltAllele,
        ):  # prevIndel,prevIndel_iPos,prevIndel_len,prevIndel_sRefAllele,prevIndel_sAltAllele=
            # sQ   ="atatatatatatatatacacatatatatatTTTAT--AATTATAACTAGTTGCATTGATA"
            # sCorr="|||||||||||||||||||||||||||||||||||  ||||| ||||||| |||||||||"
            # sDB  ="ATATATATATATATACATATATATATATATTTTATGGAATTA-AACTAGTAGCATTGATA"
            #
            # prevIndel:
            # -1 = insertion (DB shorter than Quary)
            # +1 = deletion (DB longer than Quary)
            n = len(sCorr)
            k = 0
            if prevIndel != 0:
                k, prevIndel_sRefAllele, prevIndel_sAltAllele = processIndel(
                    prevIndel, 0, n, sQ, sDB, prevIndel_sRefAllele, prevIndel_sAltAllele
                )
                if k == n:
                    return (
                        prevIndel,
                        prevIndel_iPos,
                        prevIndel_len + n,
                        prevIndel_sRefAllele,
                        prevIndel_sAltAllele,
                    )
                marker = self.clMarker(
                    sQueryShortName,
                    iCtg,
                    prevIndel_iPos,
                    prevIndel_sRefAllele,
                    prevIndel_sAltAllele,
                    len(self.vBLASTinterval),
                )
                self.vMarker.append(marker)
                prevIndel = 0
                if k > 0:
                    n = n - k
                    sQ = sQ[k:]
                    sCorr = sCorr[k:]
                    sDB = sDB[k:]
                    iStart = iStart + k
                # ,prevIndel_iPos,prevIndel_len+n,prevIndel_sRefAllele,prevIndel_sAltAllele
            k1 = sCorr.find(" ")
            if k1 < 0:
                return (
                    0,
                    -1,
                    0,
                    "",
                    "",
                )  # prevIndel,prevIndel_iPos,prevIndel_len+n,prevIndel_sRefAllele,prevIndel_sAltAllele#no markers
            # indices = [i for i, x in enumerate(sCorr) if x == ' ']
            # n=len(sCorr)

            while k1 >= 0:
                prevIndel = 0
                k = 1
                prevIndel_iPos = iStart + k1 - 1
                if sDB[k1] == "-":
                    prevIndel = -1
                if sQ[k1] == "-":
                    prevIndel = 1
                if prevIndel != 0:
                    prevIndel_sRefAllele = ""
                    prevIndel_sAltAllele = ""
                    k, prevIndel_sRefAllele, prevIndel_sAltAllele = processIndel(
                        prevIndel,
                        k1,
                        n,
                        sQ,
                        sDB,
                        prevIndel_sRefAllele,
                        prevIndel_sAltAllele,
                    )
                    if k1 + k >= n:
                        return (
                            prevIndel,
                            prevIndel_iPos,
                            k,
                            prevIndel_sRefAllele,
                            prevIndel_sAltAllele,
                        )
                    marker = self.clMarker(
                        sQueryShortName,
                        iCtg,
                        prevIndel_iPos,
                        prevIndel_sRefAllele,
                        prevIndel_sAltAllele,
                        len(self.vBLASTinterval),
                    )
                    self.vMarker.append(marker)
                else:
                    # SNP
                    prevIndel_sRefAllele = sQ[k1]
                    prevIndel_sAltAllele = sDB[k1]
                    marker = self.clMarker(
                        sQueryShortName,
                        iCtg,
                        prevIndel_iPos,
                        prevIndel_sRefAllele,
                        prevIndel_sAltAllele,
                        len(self.vBLASTinterval),
                    )
                    self.vMarker.append(marker)
                n = n - k - k1
                sQ = sQ[k + k1 :]
                sCorr = sCorr[k + k1 :]
                sDB = sDB[k + k1 :]
                iStart = iStart + k + k1
                k1 = sCorr.find(" ")
            return 0, -1, 0, "", ""

        def processBlock(sQ, sCorr, sDB):  # sQ_pp,sCorr_pp,sDB_pp,iStart=
            # Query  1     TAACAGACAGCAAAATTGGATACCATGGATGCTCGTTAATTAATTACCTACCACTCGAAT  60
            #             ||||||||||||  ||||||||||||||||||||||||||||||||||||||||||||||
            # Sbjct  1     TAACAGACAGCATTATTGGATACCATGGATGCTCGTTAATTAATTACCTACCACTCGAAT  60
            # ...
            # Query  20587021  ata
            # ...
            ss = sQ.split(" ")
            n = len(ss)
            sPosQStart = ss[2]
            iStart = int(sPosQStart)
            sQ_pp = ss[n - 3]

            i0 = 7 + len(sPosQStart)
            i1 = 2
            b = False
            for i in range(3, n):
                i0 += 1
                if len(ss[i]) > 0:
                    break
            nn = len(sQ_pp)
            i1 = i0 + nn
            sCorr_pp = sCorr[i0:i1]
            sDB_pp = sDB[i0:i1]
            return sQ_pp, sCorr_pp, sDB_pp, iStart

        f = open(sFileBlastResFormat0, "r")
        sQueryShortName = ""
        iCtg = -1  # iCtg=self.quaries.vCtgName.index(sQueryShortName)
        index = -1
        sQ = ""
        sCorr = ""
        sDB = ""

        prevIndel = 0
        prevIndel_iPos = -1
        prevIndel_len = 0
        prevIndel_sRefAllele = 0
        prevIndel_sAltAllele = 0
        iStart_prev = -1
        iStartBLAST = -1
        for s in f:
            if len(s) > 6:
                if s[0:6] == "Query=":
                    if iStart_prev >= 0:
                        self.vBLASTinterval.append(
                            self.clBLASTinterval(iCtg, iStartBLAST, iStart_prev)
                        )

                    sQueryShortName = sSeqQName_get(s)
                    iCtg = self.quaries.vCtgName.index(sQueryShortName)
                    index = 0

                    prevIndel = 0
                    prevIndel_iPos = -1
                    prevIndel_len = 0
                    prevIndel_sRefAllele = 0
                    prevIndel_sAltAllele = 0
                    iStart_prev = -1
                    iStartBLAST = -1
                if s[0:6] == "Query ":
                    sQ = s
                    index = 1
                else:
                    if index == 1:  #                    |  ||
                        sCorr = s
                        index = 2
                    else:
                        if index == 2:  # Sbjct
                            sDB = s
                            sQ_pp, sCorr_pp, sDB_pp, iStart = processBlock(
                                sQ, sCorr, sDB
                            )
                            if iStart_prev >= 0:
                                if abs(iStart - iStart_prev) > 100:
                                    self.vBLASTinterval.append(
                                        self.clBLASTinterval(
                                            iCtg, iStartBLAST, iStart_prev
                                        )
                                    )

                                    iStartBLAST = iStart
                            if iStartBLAST == -1:
                                iStartBLAST = iStart
                            iStart_prev = iStart
                            (
                                prevIndel,
                                prevIndel_iPos,
                                prevIndel_len,
                                prevIndel_sRefAllele,
                                prevIndel_sAltAllele,
                            ) = processBlock_fast(
                                sQ_pp,
                                sCorr_pp,
                                sDB_pp,
                                iStart,
                                sQueryShortName,
                                iCtg,
                                prevIndel,
                                prevIndel_iPos,
                                prevIndel_len,
                                prevIndel_sRefAllele,
                                prevIndel_sAltAllele,
                            )
                            index = 0
        if iStart_prev >= 0:
            self.vBLASTinterval.append(
                self.clBLASTinterval(iCtg, iStartBLAST, iStart_prev)
            )
        f.close()

        def MyFunc(Marker):
            return 10000000000 * Marker.iCtg + Marker.iPos

        def MyFunc1(BLASTinterval):
            return (
                10000000000 * BLASTinterval.iCtg
                + BLASTinterval.iPosStart
                + BLASTinterval.iPosEnd * 0.00000001
            )

        self.vMarker.sort(key=MyFunc)

    def sFileNameMarkers(self, sDobaffka="1"):
        return "proba_markers" + sDobaffka + ".txt"

    def printMarkers(self, sDobaffka="1"):
        f = open(self.sFileNameMarkers(sDobaffka), "w")
        if len(self.vMarker) == 0:
            f.write("No markers" + "\n")
        else:
            s = "i" + "\t" + self.vMarker[0].shapka()
            s += "\t" + self.vBLASTinterval[0].shapka()
            f.write(s + "\n")
            i = 0
            for Marker in self.vMarker:
                i += 1
                s = str(i) + "\t" + Marker.s()
                s += "\t" + self.vBLASTinterval[Marker.iBLASTinterval].s()
                f.write(s + "\n")
                self.vBLASTinterval

            if len(self.vBLASTinterval) > 0:
                f.write(self.vBLASTinterval[0].shapka() + "\n")
                for BLASTinterval in self.vBLASTinterval:
                    f.write(BLASTinterval.s() + "\n")
        f.close()


class clTwoBlastResFormat0:
    class clMarkerWithGenotype:
        def __init__(self, Marker, nInd, iInd=-1):
            self.sQueryShortName = Marker.sQueryShortName
            self.iCtg = Marker.iCtg
            self.iPos = Marker.iPos
            self.sRefAllele = Marker.sRefAllele
            self.vsAltAllele = [Marker.sAltAllele]
            self.nInd = nInd
            self.vGenotype = []
            for i in range(nInd):
                self.vGenotype.append([])
            if iInd >= 0:
                self.vGenotype[iInd] = [0]

        def shapka(self):
            s = "sQ" + "\t" + "iPos" + "\t" + "m" + "\t" + "vM"
            for i in range():
                s += "\t" + str(i)
            return s

        def s(self):
            s = (
                self.sQueryShortName
                + "\t"
                + str(self.iPos)
                + "\t"
                + self.sRefAllele
                + "\t"
                + str(self.vsAltAllele)
            )
            for i in range(self.nInd):
                s0 = "-"
                Genotype = self.vGenotype[i]
                if len(Genotype) > 0:
                    s0 = ""
                    j = 0
                    for a in Genotype:
                        if j > 0:
                            s0 += ","
                        s0 += str(a)
                        j += 1
                s += "\t" + s0
            return s

        def addIndividByMarker(self, Marker, iInd):
            if not (Marker.sAltAllele in self.vsAltAllele):
                self.vsAltAllele.append(Marker.sAltAllele)
            if iInd >= 0 and iInd < nInd:
                i = self.vsAltAllele.index(Marker.sAltAllele)
                if not (i in self.vGenotype[iInd]):
                    self.vGenotype[iInd].append(i)

    def __init__(self):
        sFileNameFastaQ = "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\referenceGenome\\JAEQMK01.1.fsa_nt\\JAEQMK01.1.fsa_nt_chr16.fasta"
        SecCtgs = clSecCtgs()
        # readFromFastaFile(self,sFileName,indexOfFormatSequenceName=-1,bSeqNeed=True):
        SecCtgs.readFromFastaFile(sFileNameFastaQ, 2, False)
        # print SecCtgs.vCtgName[0]

        sFileBlastResFormat0_1 = "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_chr16ref_vs_b_e150_0.txt"
        sFileBlastResFormat0_2 = "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_chr16ref_vs_bb_e150_0.txt"
        BlastResFormat0_1 = clBlastResFormat0(SecCtgs)
        BlastResFormat0_1.makeListOfMarkersBasedOnBlastRes(sFileBlastResFormat0_1)
        BlastResFormat0_1.printMarkers("b")
        BlastResFormat0_2 = clBlastResFormat0(SecCtgs)
        BlastResFormat0_2.makeListOfMarkersBasedOnBlastRes(sFileBlastResFormat0_2)
        BlastResFormat0_2.printMarkers("bb")

        # BlastResFormat0_1.sFileNameMarkers("b")
        # BlastResFormat0_1.sFileNameMarkers("bb")

    # ,vPloydy,bExcludeMonomorphic
    def compressMarkers_MakeGenotypes(self, vBlastResFormat0):
        vMarkerWithGenotype = []
        iBlastResFormat0 = 0
        for BlastResFormat0 in vBlastResFormat0:
            for Marker in BlastResFormat0.vMarker:
                MarkerWithGenotype = self.clMarkerWithGenotype()
                vMarkerWithGenotype.append(MarkerWithGenotype)
            iBlastResFormat0 += 1

        # unite and sort
        def MyFunc(q):
            Marker = q[0]
            return 10000000000 * Marker.iCtg + Marker.iPos

        vq = []

        vq.sort(key=MyFunc)

        vMarkerPP = []

        BlastResFormat0 = clBlastResFormat0(vBlastResFormat0[0].quaries)
        BlastResFormat0.vMarker = vMarkerPP
        BlastResFormat0.printMarkers("compressed")


class clSecCtgs:
    # list of sequence contigs
    def __init__(self):
        self.fasta = ""  # file name of fasta files from where these contigs were loaded
        self.vCtg = []  # list of sequece contigs

        # list of sequence contig names to simplify search in self.vCtg
        self.vCtgName = []
        self.vCtgNameTillFirstSpace = []

        self.bvLineOf_gff = (
            False  # is presented information from gff file within self.vCtg
        )

    class clSecCtg:
        def __init__(self):
            self.name = ""
            self.nameTillFirstSpace = ""
            # self.vLG=[]
            # self.vcoor=[]
            self.seqLength = 0
            self.bSeqLengthWasDefinedBySeqName = False
            self.seq = []
            self.shortName = ""
            self.coverage = -1  # unknown

            # mapping info
            self.vPos = (
                []
            )  # list of candidate positions (based on only one of possible ways)
            self.vPosAll = []
            #
            self.basedOnGoodMarkersOnly = False  # Way 1
            self.basedOnBadMarkersOnly = False  # Way 2 (if no good markers)

            self.vPosOnRefGenomeMapped = []  # Way 3 (based on Formica)

            self.iBasedOnClusterOfBlastRes = 0  # Way 4 (if no markers, build net of ctgs, if resulted cluster contains contig with marker)
            self.idOfFastaFileInUseToMapContigsWithoutMarkers = 0  # Way 5 (no markers, cluster from Way 4 are too large, use cluster with rank 2 if contains marker)
            #
            # presumably usable
            self.vPosOnRefGenomeNonMapped = (
                []
            )  # Way 6 (based on Formica, but these parts of formica are not mapped to our, manual inspection presumably can help)
            self.vLGmarker = []  # good
            self.vLGmarkerBad = []

            self.vLineOf_gff = []

        def sPos(self):
            s = ""
            for pos in self.vPos:
                if len(s) > 0:
                    s += ","
                s += pos.s()
            return "[" + s + "]"

        def vPosAll_update(self, iLG, coorGenet, coorOnCntg):
            pos = self.clPos()
            pos.iLG = iLG
            pos.coor = coorGenet
            # pos.markersGood=[]
            # pos.markersBad=[]
            pos.coorOnCntg = coorOnCntg
            self.vPosAll.append(pos)

        def sPosAll(self):
            s = ""
            iPos = 0
            for pos in self.vPosAll:
                iPos += 1
                if iPos > 1:
                    s += ","
                s += (
                    "["
                    + str(pos.iLG)
                    + ","
                    + str(pos.coor)
                    + ","
                    + str(pos.coorOnCntg)
                    + "]"
                )
            s = "[" + s + "]"
            return s

        def vPosAll_get(self, s):
            self.vPosAll = []
            sNoSkob = s[1 : (len(s) - 2)]
            ss = sNoSkob.split("],")
            for s1 in ss:
                # sNoSkob1=s1[1:(len(s1)-1)]
                sNoSkob1 = s1[1:]
                ss1 = sNoSkob1.split(",")
                # print s
                # print ss
                # print s1
                # print str(ss1)
                self.vPosAll_update(int(ss1[0]), float(ss1[1]), int(ss1[2]))

        class clPos:
            def __init__(self):
                self.iLG = -1
                self.coor = -1
                self.markersGood = []
                self.markersBad = []
                self.coorOnCntg = -1

            def s(self):
                sG = ""
                sB = ""
                for marker in self.markersGood:
                    if len(sG) > 0:
                        sG += ","
                    sG += marker.m.sMarker
                for m in self.markersBad:
                    if len(sB) > 0:
                        sB += ","
                    sB += m.sMarker
                return (
                    "["
                    + str(self.iLG)
                    + ","
                    + str(self.coor)
                    + ",["
                    + sG
                    + "]"
                    + ",["
                    + sB
                    + "]"
                    + "]"
                )

        def nameProcess(self, indexOfFormatSequenceName):
            ss = self.name.split(" ")
            self.nameTillFirstSpace = ss[0]

            if indexOfFormatSequenceName == 0:
                # self.name=NODE_1_length_992370_cov_1.03732
                ss = self.name.split("_")
                if len(ss) >= 6:
                    self.shortName = ss[1]  # 1
                    self.seqLength = int(ss[3])  # 992370
                    self.bSeqLengthWasDefinedBySeqName = True
                    self.coverage = float(ss[5])  # 1.03732
            if indexOfFormatSequenceName == 1:
                # self.name=scaffold10|size849347
                ss = self.name.split("|")
                if len(ss) >= 2:
                    self.shortName = ss[1]  # scaffold10 #NB 2021.03.11: why not 0?
                    sss = ss[1]
                    if len(sss) > 4:
                        if sss[0:4] == "size":
                            self.seqLength = int(sss[4:])  # 849347
                            self.bSeqLengthWasDefinedBySeqName = True
            if indexOfFormatSequenceName == 2:
                # self.name=
                # >CM020829.1 Formica selysi isolate DE90_pool_M chromosome 25, whole genome shotgun sequence
                # >WHNR01000498.1 Formica selysi isolate DE90_pool_M Contig470, whole genome shotgun sequence
                # >CM020864.1 Formica selysi isolate DE90_pool_M mitochondrion, complete sequence, whole genome shotgun sequence
                # >tig00000002 len=10662 reads=10 class=contig suggestRepeat=no suggestBubble=yes suggestCircular=no trim=0-10662
                # >JAEQMK010000001.1 Solenopsis invicta isolate M01_SB chromosome 1, whole genome shotgun sequence
                ss = self.name.split(",")
                self.name = ss[
                    0
                ]  # CM020829.1 Formica selysi isolate DE90_pool_M chromosome 25
                ss = self.name.split(" ")
                self.name = ss[0]  # CM020829.1
                self.shortName = self.name  # CM020829.1
                if len(ss) > 5:
                    self.shortName = ss[5]  # chromosome
                if len(ss) > 6:
                    self.shortName += "_" + ss[6]  # chromosome_25

        def printSeqToFile(self, f, sDobaffka, nNNNaddAtleast, bPrintName):
            if bPrintName:
                f.write(">" + self.name + sDobaffka + chr(10))  #'\n')
            iRow = 0
            n = len(self.seq)
            nNNNadded = 0
            nInRow = 60  # poka
            for s in self.seq:
                if iRow + 1 == n:  # the last row
                    if nNNNaddAtleast > 0:
                        nn = len(s) - 1
                        s = s[0:nn]  # cut \n
                        nNNNadded = nInRow - nn  # n letters to end of row
                        for i in range(nNNNadded):
                            s += "N"
                        s += chr(10)  # "\n"
                f.write(s)
                iRow += 1
            if nNNNaddAtleast > 0:
                if nNNNadded < nNNNaddAtleast:
                    # row of "N"s
                    s = ""
                    for i in range(nInRow):
                        s += "N"
                    s += chr(10)  # "\n"

                    while nNNNadded < nNNNaddAtleast:
                        f.write(s)
                        nNNNadded += nInRow
            return nNNNadded

        def printToFilePart(self, f, start, end):
            file.write(">" + self.name + "_" + str(start) + "_" + str(end) + "\n")
            prev = 0
            for s in self.seq:
                next = prev + len(s) - 1  # -1 because of \n
                if start > prev:
                    if start <= next:
                        if end > next:
                            file.write(s[start - prev - 1 :])
                        else:
                            file.write(s[start - prev - 1 : end - prev] + "\n")
                else:
                    if end > prev:
                        if end >= next:
                            file.write(s)
                        else:
                            file.write(s[0 : end - prev] + "\n")
                prev = next

        class clSyntheny:
            def __init__(self, iChromosome, y1, y2, x1, x2, generalOrientation):
                self.iChrOfRefGenome = iChromosome
                self.posOnchrRefGenome1 = y1
                self.posOnchrRefGenome2 = y2
                self.posOnMyCtg1 = x1
                self.posOnMyCtg2 = x2
                self.generalOrientationRelativeRefGenome = generalOrientation

            def s_Syntheny(self):  # q=[iChromosome,y1,y2,x1,x2,generalOrientation]
                # q=[iChromosome,y1,y2,x1,x2,generalOrientation]
                s = (
                    "["
                    + str(self.iChrOfRefGenome)
                    + ","
                    + str(self.posOnchrRefGenome1)
                    + ","
                    + str(self.posOnchrRefGenome2)
                )  # +"("++")"
                s += (
                    ","
                    + str(self.posOnMyCtg1)
                    + ","
                    + str(self.posOnMyCtg2)
                    + ","
                    + str(self.generalOrientationRelativeRefGenome)
                    + "]"
                )
                return s

        def s_vSyntheny(self, vSyntheny):
            s = ""
            i = 0
            for Syntheny in vSyntheny:
                if i > 0:
                    s += ","
                s += Syntheny.s_Syntheny()
                i += 1
            return s

        class clLineOf_gff:
            def __init__(self, s):
                self.s = s
                ss = s.split("\t")
                # NODE_2488_length_25343_cov_3.23236	maker	mRNA	11524	14587	1302	+	.	ID=maker-NODE_2488_length_25343_cov_3.23236-exonerate_protein2genome-gene-0.0-mRNA-1;Parent=maker-NODE_2488_length_25343_cov_3.23236-exonerate_protein2genome-gene-0.0;Name=maker-NODE_2488_length_25343_cov_3.23236-exonerate_protein2genome-gene-0.0-mRNA-1;_AED=0.34;_eAED=0.34;_QI=0|0|0|1|0|0|5|0|433
                if len(ss) > 4:
                    self.seqNameOriginal = ss[0]
                    self.coorStart = int(ss[3])
                    self.coorEnd = int(ss[4])

            def sBasedOnNewAssembly(self, seqNameNew, coorOfStart):  # s=
                ss = self.s.split("\t")
                n = len(ss)
                s = seqNameNew
                for i in range(1, n):
                    if i == 3 or i == 4:
                        s += "\t" + str(int(ss[i]) + coorOfStart - 1)
                    else:
                        s += "\t" + ss[i]
                return s

            # >maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1 protein AED:0.01 eAED:0.01 QI:0|-1|0|1|-1|0|1|0|453
            # >maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1 transcript offset:0 AED:0.01 eAED:0.01 QI:0|-1|0|1|-1|0|1|0|453
            # NODE_1_length_992370_cov_1.03732	maker	gene	22993	24354	.	-	.	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4;Name=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4
            # NODE_1_length_992370_cov_1.03732	maker	mRNA	22993	24354	1362	-	.	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1;Parent=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4;Name=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1;_AED=0.01;_eAED=0.01;_QI=0|-1|0|1|-1|0|1|0|453
            # NODE_1_length_992370_cov_1.03732	maker	exon	22993	24354	.	-	.	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1:exon:0;Parent=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1
            # NODE_1_length_992370_cov_1.03732	maker	CDS	22993	24354	.	-	0	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1:cds;Parent=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1
            #
            # maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1
            # ->
            # gN1L992370c0p4
            def transformNameOfGene(self, s):
                # s="maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1"
                # print s
                ss = s.split("-")
                if len(ss) < 5:
                    print(s)
                sCtg = ss[1]  # NODE_1_length_992370_cov_1.03732
                sPosOnCtg = ss[4]  # 0.4
                sss1 = sCtg.split("_")  # "NODE","1","length","992370","cov","1.03732"
                sss2 = sPosOnCtg.split(".")  # "0","4"
                return "gN" + sss1[1] + "L" + sss1[3] + "c" + sss2[0] + "p" + sss2[1]

        def sSeq_get(self):
            s = ""
            for s1 in self.seq:
                print(str(len(s1)) + " " + str(len(s)) + "")
                s += s1[0 : len(s1) - 1]  # exclude endOfLine symbol
            return s

    def bAddPosition_get(self, vPos, iLG, x, dist_cM_accuracy=3):
        # search for genetic position (iLG,x) in array of positions vPos
        # return: bAdd = no such position => need to add
        #        bAdd=False => i=index in array of closest position
        bAdd = True
        i = len(vPos)
        p = -1
        for pos in vPos:
            p += 1
            if pos.iLG == iLG:
                if abs(pos.coor - x) <= dist_cM_accuracy:
                    bAdd = False
                    i = p
        return bAdd, i

    def vPos_update(self, vPos, iLG, x, vLGmarker, vmBad, dist_cM_accuracy=3):  # vPos=
        # vPos=self.vCtg[i].vPos
        # LGmarker=[LG.vLGmarker[idOnLG]]
        # vmBad=[m]
        bAdd, a = self.bAddPosition_get(vPos, iLG, x, dist_cM_accuracy)
        ctg = self.clSecCtg()
        pos = ctg.clPos()
        if not bAdd:
            pos = vPos[a]
        for m in vmBad:
            if not (m in pos.markersBad):
                pos.markersBad.append(m)
        for LGmarker in vLGmarker:
            if not (LGmarker in pos.markersGood):
                pos.markersGood.append(LGmarker)
        if bAdd:
            pos.iLG = iLG
            pos.coor = x
            vPos.append(pos)
        return vPos

    def readFromFastaFile(self, sFileName, indexOfFormatSequenceName=-1, bSeqNeed=True):
        print("readFromFastaFile " + sFileName + "...")
        self.fasta = sFileName
        self.vCtg = []
        self.vCtgName = []
        self.vCtgNameTillFirstSpace = []
        f = open(sFileName, "r")
        ctg = self.clSecCtg()
        for s in f:
            if len(s) > 1:
                if s[0] == ">":
                    if ctg.name != "":
                        self.vCtg.append(ctg)
                        self.vCtgName.append(ctg.name)
                        self.vCtgNameTillFirstSpace.append(ctg.nameTillFirstSpace)
                    ctg = self.clSecCtg()
                    ctg.name = s[1 : len(s) - 1]  # delete ">"
                    ctg.nameProcess(indexOfFormatSequenceName)
                    # poka
                    # ctg.vLG=[-1]
                    # ctg.vcoor=[len(self.vCtg)]
                else:
                    if bSeqNeed:
                        ctg.seq.append(s)
                    if not (ctg.bSeqLengthWasDefinedBySeqName):
                        ctg.seqLength += len(s) - 1
            # print tt.name+'\t'+str(tt.nVal)
        if ctg.name != "":
            self.vCtg.append(ctg)
            self.vCtgName.append(ctg.name)
            self.vCtgNameTillFirstSpace.append(ctg.nameTillFirstSpace)
        f.close()
        print(
            "readFromFastaFile "
            + sFileName
            + "...Finished, nSeq="
            + str(len(self.vCtg))
        )

    def ctgBasedOnMyNameOfGoodMarker(self, sMyNameOfGoodMarker):  # ctg=
        # search for ctg in self.vCtg[] based on the name of good marker

        # ss=LGmarker.m.sChr
        #
        # print "ss="+ss
        # print "sMarker="+LGmarker.m.sMarker
        # sMarker=NODE_1000_length_42440_cov_2.75993_B0_start18296,23592,23592,32628
        iii = sMyNameOfGoodMarker.index("B")
        ss = sMyNameOfGoodMarker[0 : iii - 1]
        # print "ss="+ss

        iCtg = self.vCtgName.index(ss)
        ctg = self.vCtg[iCtg]
        return ctg

    def ctgBasedOnMyNameOfBadMarker(self, sMyNameOfBadMarker):  # ctg=
        # search for ctg in self.vCtg[] based on the name of bad marker

        # NODE_10236_length_4810_cov_1.91871___1663
        iii = sMyNameOfBadMarker.find("___")
        ss = sMyNameOfBadMarker[0:iii]
        iCtg = self.vCtgName.index(ss)
        ctg = self.vCtg[iCtg]
        return ctg

    def readCoorFromLGs(
        self, vLG, ReferenceGenome, sSeqOriginalForMarkers, sSeqAssemblyName
    ):
        # set coordinates on genetic map for contigs from self.vCtg[] based on good markers from these sequence contigs
        dist_cM_accuracy = 3

        # sSeqOriginalForMarkers=="Cnig_gn1" and sSeqAssemblyName="asm":#was made for Aparna
        def TableOfGeneticMarkersMapped_asm___get():
            TableOfTxt = clTableOfTxt()
            sFileName = "C:\\Frenkel\\Privman\\Aparna\\drafts\\markers117males_Cnig_gn1_on_asm.txt"
            bShapka = True
            bFirstColNoNeedToRead = True
            TableOfTxt.readFromFile(sFileName, bShapka, bFirstColNoNeedToRead)
            print("nRows=" + str(TableOfTxt.nRows))
            # TableOfTxt.printToFile(sFileName+".txt",bShapka)
            # iCol=3
            # textCol="tig00001985"
            # iRows=TableOfTxt.iRows_get(textCol,iCol)
            # print str(iRows)
            # iRow=TableOfTxt.iRow_get("NODE_1371_length_36652_cov_2.40195___32150",0)
            # print "NODE_1371_length_36652_cov_2.40195___32150: iRow="+str(iRow)
            # NODE_13_length_173790_cov_2.7937___8823
            iRow = TableOfTxt.iRow_get("NODE_13_length_173790_cov_2.7937___8823", 0)
            # print "NODE_13_length_173790_cov_2.7937___8823: iRow="+str(iRow)
            # print str(TableOfTxt.vColText)
            return TableOfTxt

        # general
        def TableOfGeneticMarkersMapped___get(ReferenceGenome):
            TableOfTxt = clTableOfTxt()
            sFileName = ReferenceGenome.attachMarkersToAnotherAssembly_simple___sFileOut
            bShapka = True
            bFirstColNoNeedToRead = True
            TableOfTxt.readFromFile(sFileName, bShapka, bFirstColNoNeedToRead)
            print("nRows=" + str(TableOfTxt.nRows))
            return TableOfTxt

        TableOfTxt = clTableOfTxt()
        if sSeqOriginalForMarkers == sSeqAssemblyName:  # original
            pass
        else:
            if (
                sSeqOriginalForMarkers == "Cnig_gn1" and sSeqAssemblyName == "asm"
            ):  # was made for Aparna
                TableOfTxt = TableOfGeneticMarkersMapped_asm___get()
                dist_cM_accuracy = 1000  # poka
            else:
                TableOfTxt = TableOfGeneticMarkersMapped___get(
                    ReferenceGenome
                )  # general
                dist_cM_accuracy = 1000  # poka

        nLG = len(vLG)
        nNot = 0
        nOk = 0
        for iLG in range(nLG):
            LG = vLG[iLG]
            # s=LG.name
            for (
                LGmarker
            ) in LG.vLGmarkerOrderedByCoorOnLG:  # only good markers are in LG
                x = LGmarker.coorOnLG
                coorOnCntg = -1
                if sSeqOriginalForMarkers == sSeqAssemblyName:  # original
                    ctg = self.ctgBasedOnMyNameOfGoodMarker(LGmarker.m.sMarker)
                    coorOnCntg = -1  # ne gotovo

                    ctg.vPos = self.vPos_update(
                        ctg.vPos, iLG, x, [LGmarker], [], dist_cM_accuracy
                    )
                    ctg.vPosAll_update(iLG, x, coorOnCntg)
                    ctg.basedOnGoodMarkersOnly = True
                    ctg.vLGmarker.append(LGmarker)
                else:
                    if (
                        sSeqOriginalForMarkers == "Cnig_gn1"
                        and sSeqAssemblyName == "asm"
                    ):  # was made for Aparna
                        sMyNameOfGoodMarker = (
                            LGmarker.m.sMarker
                        )  # sMarker=NODE_1000_length_42440_cov_2.75993_B0_start18296,23592,23592,32628
                        iii = sMyNameOfGoodMarker.index("B")
                        sCtg_Cnig_gn1 = sMyNameOfGoodMarker[
                            0 : iii - 1
                        ]  # NODE_1000_length_42440_cov_2.75993
                        ss = sMyNameOfGoodMarker.split("start")
                        ss = ss[1].split(",")  # [18296,23592,23592,32628]
                        iii = int(ss[0])  # 18296
                        ss = (
                            sCtg_Cnig_gn1 + "___" + str(iii)
                        )  # NODE_1000_length_42440_cov_2.75993___18296

                        # iMarker	marker	iCopy	nCopies	ctgDB	coorOnCtgDB	length
                        # 7299	NODE_1000_length_42440_cov_2.75993___18296	0	1	tig00000215	978534	30873
                        iRow = TableOfTxt.iRow_get(ss, 0)
                        if iRow >= 0:
                            sCtg = TableOfTxt.rows[iRow].vCellText[3]  # tig00000215
                            coorOnCntg = TableOfTxt.rows[iRow].vCellText[4]  # 978534
                            iCtg = self.vCtgName.index(sCtg)
                            ctg = self.vCtg[iCtg]
                            nOk += 1

                            ctg.vPos = self.vPos_update(
                                ctg.vPos, iLG, x, [LGmarker], [], dist_cM_accuracy
                            )
                            ctg.vPosAll_update(iLG, x, coorOnCntg)
                            ctg.basedOnGoodMarkersOnly = True
                            ctg.vLGmarker.append(LGmarker)
                        else:
                            nNot += 1
                            print(
                                "(nOk="
                                + str(nOk)
                                + ", nNot="
                                + str(nNot)
                                + ")marker not in asm: "
                                + sMyNameOfGoodMarker
                            )
                            print(ss)
                    else:
                        sMyNameOfGoodMarker = (
                            LGmarker.m.sMarker
                        )  # sMarker=NODE_1000_length_42440_cov_2.75993_B0_start18296,23592,23592,32628
                        ggg = clGenotypes()
                        (
                            sChr,
                            iBlockOnChr,
                            vPosBp,
                        ) = ggg.compressMarkersOfAllCtgs_ctg_sMarkerDeshifrate(
                            sMyNameOfGoodMarker
                        )
                        for PosBp in vPosBp:
                            ss = (
                                sChr + "___" + str(PosBp)
                            )  # NODE_1000_length_42440_cov_2.75993___18296
                            iRow = TableOfTxt.iRow_get(ss, 0)
                            if iRow >= 0:
                                sCtg = TableOfTxt.rows[iRow].vCellText[3]  # tig00000215
                                coorOnCntg = TableOfTxt.rows[iRow].vCellText[
                                    4
                                ]  # 978534
                                iCtg = self.vCtgName.index(sCtg)
                                ctg = self.vCtg[iCtg]
                                nOk += 1

                                ctg.vPos = self.vPos_update(
                                    ctg.vPos, iLG, x, [LGmarker], [], dist_cM_accuracy
                                )
                                ctg.vPosAll_update(iLG, x, coorOnCntg)
                                ctg.basedOnGoodMarkersOnly = True
                                ctg.vLGmarker.append(LGmarker)
                            else:
                                nNot += 1
                                print(
                                    "(nOk="
                                    + str(nOk)
                                    + ", nNot="
                                    + str(nNot)
                                    + ")marker not in ReferenceGenome: "
                                    + sMyNameOfGoodMarker
                                )
                                print(ss)

    def setCoorBasedOnBadMarkers(self, sFileName, vLG):
        # set coordinates on genetic map for contigs from self.vCtg[] based on bad markers from these sequence contigs

        print("setCoorBasedOnBadMarkers...")

        # def readFromFileSimple(self,sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
        g = clGenotypes()
        idType = 0
        g.readFromFileSimple(sFileName, False, "", idType, True, False)
        LGnotInUse = clLinkageGroup()
        nMarkersNotFound = 0
        nFarMarkers = 0
        im = 0
        rMax = -1
        for m in g.vMarker:

            bFound = False
            LGmarkerBad = LGnotInUse.clMarkerOfLG()
            LGmarkerBad.m = m

            # d_best
            iLG_best = -1
            idOnLG_best = -1
            d_best = -1
            iLG = 0
            vIndivids = m.vIndividsAll_get()
            for LG in vLG:
                for idOnLG in LG.idOnLG_path:
                    m1 = LG.vLGmarker[idOnLG].m
                    nE, nN, nToImprove = m1.compareWithMarker(m, vIndivids)
                    # print str(m1.g)
                    # print str(m.g)
                    # print "im="+str(im)+", iLG="+str(iLG)+", nE="+str(nE)+", nN="+str(nN)
                    if nE + nN >= 6:
                        bFound = True
                        r = float(nN) / (nN + nE)
                        if nE < nN:
                            r = float(nE) / (nN + nE)

                        bNewBest = iLG_best < 0
                        if not bNewBest:
                            bNewBest = r < d_best
                        if bNewBest:
                            iLG_best = iLG
                            idOnLG_best = idOnLG
                            d_best = r
                            LGmarkerBad.LGid = iLG_best
                            LGmarkerBad.idOnLG_closestOnPath = idOnLG_best
                            LGmarkerBad.coorOnLG = LG.vLGmarker[idOnLG].coorOnLG
                iLG += 1

            if not bFound:
                nMarkersNotFound += 1
                print("non-mapped marker" + str(nMarkersNotFound) + ": " + m.sMarker)
            else:
                if rMax < 0:
                    rMax = d_best
                else:
                    if rMax < d_best:
                        rMax = d_best
                        print("new max: rMax=" + str(rMax) + ", m=" + m.sMarker)
                if d_best > 0.15:
                    nFarMarkers += 1
                    print(
                        "too far marker "
                        + str(nFarMarkers)
                        + ": "
                        + m.sMarker
                        + ", rMin="
                        + str(d_best)
                    )

            ctg = self.ctgBasedOnMyNameOfBadMarker(m.sMarker)
            ctg.vLGmarkerBad.append(LGmarkerBad)

            iLG = 0
            for LG in vLG:
                for idOnLG in LG.idOnLG_path:
                    m1 = LG.vLGmarker[idOnLG].m
                    nE, nN, nToImprove = m1.compareWithMarker(m, vIndivids)
                    if nE + nN >= 6:
                        r = float(nN) / (nN + nE)
                        if nE < nN:
                            r = float(nE) / (nN + nE)
                        if r <= d_best * 1.1:
                            x = LG.vLGmarker[idOnLG].coorOnLG
                            ctg.vPos = self.vPos_update(
                                ctg.vPos, iLG, x, [LG.vLGmarker[idOnLG]], [m]
                            )
                            ctg.basedOnBadMarkersOnly = True
                iLG += 1
            im += 1
            if im % 100 == 1:
                print(str(im) + " of " + str(len(g.vMarker)))
        print(
            "setCoorBasedOnBadMarkers...Finished: nMarkersNotFound="
            + str(nMarkersNotFound)
            + ", rMax="
            + str(rMax)
            + ", nFarMarkers="
            + str(nFarMarkers)
        )

    def addCoorOnGeneticMapToContigsWithoutGeneticMarkersBasedOnBlastResWithRelativeGenomes(
        self,
    ):
        # sFileBLAST=sPath+"res_diploid_vs_Cnig_gn1_e150.out"#results of BLAST vs Diploid
        # sFileBLAST1=sPath+"res_Solenopsis_invicta_vs_Cnig_gn1_e30.out"#results of BLAST vs Solenopsis_invicta
        # self.setCoorBasedOnBLAST(sFileBLAST)
        myBlastRes = clBlastRes()

        bDiploid = True
        if bDiploid:
            sFileNameBlast = (
                "C:\\Frenkel\\Privman\\Cnig_gn1\\res_diploid_vs_Cnig_gn1_e150.out"
            )
            myNetBasedOnBlastRes = clNetBasedOnBlastRes(sFileNameBlast, 1, self)
            myNetBasedOnBlastRes.ClusteringAndReport()
        bSolenopsisInvicta = True
        if bSolenopsisInvicta:
            sFileNameBlast = "C:\\Frenkel\\Privman\\Cnig_gn1\\res_Solenopsis_invicta_vs_Cnig_gn1_e30.out"
            myNetBasedOnBlastRes = clNetBasedOnBlastRes(sFileNameBlast, 2, self)
            myNetBasedOnBlastRes.ClusteringAndReport()

    def attachSequences(
        self,
        vLG,
        sFileName_genotypesOfNotGoodMarkers_inFormatChr,
        sSeqOriginalForMarkers,
        sSeqAssemblyName,
    ):
        PrivmanLab = clPrivmanLab()
        self = PrivmanLab.SecCtgsByName(sSeqAssemblyName, False)

        # Good markers (way 1)
        ReferenceGenome = clReferenceGenome(sSeqOriginalForMarkers, sSeqAssemblyName)
        self.readCoorFromLGs(
            vLG, ReferenceGenome, sSeqOriginalForMarkers, sSeqAssemblyName
        )

        if sSeqAssemblyName == "Cnig_gn1":  # poka
            # Bad markers (way 2)
            self.setCoorBasedOnBadMarkers(
                sFileName_genotypesOfNotGoodMarkers_inFormatChr, vLG
            )

            # Way 3 (based on Formica)
            # if False:
            if True:
                # ReferenceGenome=clReferenceGenome("Cnig_gn1","Formica")
                if False:
                    markersOnRefGenome = ReferenceGenome.attachMarkersToAnotherAssembly(
                        vLG
                    )
                    ReferenceGenome.attachMarkersToAnotherAssembly__makeBlocksOfRefGenome(
                        vLG, markersOnRefGenome
                    )
                    # [iDB,sDB,vcoorDB[i],LGmarker]
                    for q in markersOnRefGenome:
                        # ","+LGmarker.m.sMarker+"]"+
                        # print "q=["+str(q[0])+","+q[1]+","+str(q[2])+","+str(q[3].LGid)+","+str(q[3].coorOnLG)
                        pass
                else:
                    ReferenceGenome.readFromFile_Chromosome_vBlockOfSyntheny()
                self.mapContigsBasedOnReferenceGenome(ReferenceGenome)

            # Ways 4 and 5
            bUseBlastRes = True
            if bUseBlastRes:
                self.addCoorOnGeneticMapToContigsWithoutGeneticMarkersBasedOnBlastResWithRelativeGenomes()

            # poka tut
            bGff = True
            if bGff:
                self.QTLsBesan()
                # i=1/0

        # print final results
        bPrintSeqAllPartsOrdered = True
        if bPrintSeqAllPartsOrdered:
            if sSeqAssemblyName == "Cnig_gn1":
                self.QTLsBesanPP()
            else:
                # self.vLineOf_gff_make()
                AssemblyMy = clAssemblyMy(
                    self, vLG, sSeqAssemblyName
                )  # old, not working
                AssemblyMy.vLGwithSeq_make(vLG, sSeqAssemblyName)

    def QTLsBesanPP(self):
        # ne gotovo
        self.vLineOf_gff_make()
        AssemblyMy = clAssemblyMy(self, vLG, "Cnig_gn1")  # old, not working
        AssemblyMy.vLGwithSeq_make(vLG, sSeqAssemblyName)

        AssemblyMy.print_mapped_gff(14, 255.6, 274.8, "1\tC28", True, True)
        AssemblyMy.print_mapped_gff(14, 267.3, 291.4, "2\t2Me-C30", True, False)
        AssemblyMy.print_mapped_gff(2, 133, 148.1, "3\t2Me-C30", True, False)
        AssemblyMy.print_mapped_gff(18, 45.13, 60.14, "4\tTotal", True, False)
        AssemblyMy.print_mapped_gff(26, 59.3, 74.4, "5\tC27", True, False)
        AssemblyMy.print_mapped_gff(13, 62.8, 77.9, "6\tC27", True, False)
        AssemblyMy.print_mapped_gff(13, 56.7, 71.8, "7\t13+15Me-C31", True, False)
        AssemblyMy.print_mapped_gff(4, 13.5, 28.52, "8\t2Me-C30", True, False)

    def QTLsBesan(self):
        self.vLineOf_gff_make()
        sFileName = "selected.gff"
        f = open(sFileName, "w")

        # QTLs of Besan good also by me
        bByBesan = False
        if bByBesan:
            # original by Besan
            self.LineOf_gff_interval_addToFile(f, 1, 14, 259, 276, "C28")
            self.LineOf_gff_interval_addToFile(f, 2, 14, 267, 284, "2Me-C30")
            self.LineOf_gff_interval_addToFile(f, 3, 2, 143, 152, "2Me-C30")
            self.LineOf_gff_interval_addToFile(f, 4, 18, 49, 61, "Total")
            self.LineOf_gff_interval_addToFile(f, 5, 26, 64, 84, "C27")
            self.LineOf_gff_interval_addToFile(f, 6, 13, 62, 72, "C27")
            self.LineOf_gff_interval_addToFile(f, 7, 13, 78, 70, "13+15Me-C31")
            self.LineOf_gff_interval_addToFile(f, 8, 4, 10, 26, "2Me-C30")
        else:
            # corrected by vova (each QTL at least 7.5 from max of LOD, hence each interval>=15 cM)
            self.LineOf_gff_interval_addToFile(f, 1, 14, 255.6, 274.8, "C28")
            self.LineOf_gff_interval_addToFile(f, 2, 14, 267.3, 291.4, "2Me-C30")
            self.LineOf_gff_interval_addToFile(f, 3, 2, 133, 148.1, "2Me-C30")
            self.LineOf_gff_interval_addToFile(f, 4, 18, 45.13, 60.14, "Total")
            self.LineOf_gff_interval_addToFile(f, 5, 26, 59.3, 74.4, "C27")
            self.LineOf_gff_interval_addToFile(f, 6, 13, 62.8, 77.9, "C27")
            self.LineOf_gff_interval_addToFile(f, 7, 13, 56.7, 71.8, "13+15Me-C31")
            self.LineOf_gff_interval_addToFile(f, 8, 4, 13.5, 28.52, "2Me-C30")
        f.close()

    def LineOf_gff_interval_addToFile(self, f, iQTL, iLG, coorStart, coorEnd, sTrait):
        for ctg in self.vCtg:
            for pos in ctg.vPos:
                if pos.iLG == iLG and pos.coor >= coorStart and pos.coor <= coorEnd:
                    for LineOf_gff in ctg.vLineOf_gff:
                        s = (
                            str(iQTL)
                            + "\t"
                            + sTrait
                            + "\t"
                            + str(pos.iLG)
                            + "\t"
                            + str(pos.coor)
                            + "\t"
                            + LineOf_gff.s
                        )
                        f.write(s + "\n")

    def printSeqFromIntervalAllCandidates(
        self, iLG, coorStartInclude, coorEndNotInclude, sFileName, bFirst
    ):
        if bFirst:
            f = open(sFileName, "w")
            f.close()
        f = open(sFileName, "a")
        # f.write(s)
        for ctg in self.vCtg:
            iPos = 0
            for pos in ctg.vPos:
                if pos.iLG == iLG:
                    if pos.coor >= coorStartInclude and pos.coor < coorEndNotInclude:
                        # sDobaffka=", "+str(iLG)+"->"+str(jLG)+":"+str(ctg.vcoor[jLG])
                        sDobaffka = (
                            "___copy_"
                            + str(iPos + 1)
                            + "_LG_"
                            + str(iLG + 1)
                            + "_coor_"
                            + str(pos.coor)
                        )
                        ctg.printSeqToFile(f, sDobaffka, 0, True)
                iPos += 1
        f.close()

    def mapContigsBasedOnReferenceGenome(self, ReferenceGenome):
        bPrint = True
        f = open(
            ReferenceGenome.sFileNameBlastRes.MeDB, "r"
        )  # reference genome is DB, our contigs are quary
        myBlastRes = clBlastRes()
        sFileName1 = "blockOfBlastResults_intervalsOnQ.txt"
        f1 = open(sFileName1, "w")
        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        # ctg0=self.clSecCtg()
        while bContinue:
            iBlock += 1
            if iBlock % 100 == 1:
                print("mapContigsBasedOnReferenceGenome..." + str(iBlock))
            LinesOfBlastRes = myBlastRes.clLinesOfBlastRes(
                sFirstStringOfBlockOfFastaResult, f
            )
            sFirstStringOfBlockOfFastaResult = (
                LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
            )
            bContinue = LinesOfBlastRes.bNotTheLastBlock
            OverlapOfQuaryWithSequencesOfDB = (
                myBlastRes.clOverlapOfQuaryWithSequencesOfDB(LinesOfBlastRes.sQ)
            )
            OverlapOfQuaryWithSequencesOfDB.processBlockOfBlastResults(LinesOfBlastRes)

            f1.write(OverlapOfQuaryWithSequencesOfDB.s_get() + "\n")
            iCtg = self.vCtgName.index(LinesOfBlastRes.sQ)
            ctg = self.vCtg[iCtg]
            ctg.vPosOnRefGenomeMapped = []  # Way 5 (based on Formica)
            #
            # presumably usable
            ctg.vPosOnRefGenomeNonMapped = []

            # viChromosome=[]
            # Pos=ctg.clPos()
            vPos = []
            for (
                OverlapOfQuaryWithCtgOfDB
            ) in OverlapOfQuaryWithSequencesOfDB.vOverlapOfQuaryWithCtgOfDB:
                if OverlapOfQuaryWithCtgOfDB.bPresentedAfterExcludedMultiCoverage():
                    sDB = OverlapOfQuaryWithCtgOfDB.sDB
                    x1 = (
                        OverlapOfQuaryWithCtgOfDB.MinPosOnQ_excludedMultiCoverage
                    )  # pos on ctg
                    x2 = OverlapOfQuaryWithCtgOfDB.MaxPosOnQ_excludedMultiCoverage
                    generalOrientation = OverlapOfQuaryWithCtgOfDB.generalOrientation
                    y1 = (
                        OverlapOfQuaryWithCtgOfDB.PosOnCtgDB_MinPosOnQ_excludedMultiCoverage
                    )  # pos on ref
                    y2 = (
                        OverlapOfQuaryWithCtgOfDB.PosOnCtgDB_MaxPosOnQ_excludedMultiCoverage
                    )
                    iChromosome = ReferenceGenome.iChromosome_get(
                        sDB
                    )  # chr on reference genome
                    q = ctg.clSyntheny(iChromosome, y1, y2, x1, x2, generalOrientation)
                    bPos = False
                    iLG, coorOnLG = ReferenceGenome.posOnGeneticMapBasedOnRefGenome(
                        sDB, y1
                    )
                    if iLG >= 0:
                        bPos = True
                        vPos = self.vPos_update(vPos, iLG, coorOnLG, [], [])
                    iLG, coorOnLG = ReferenceGenome.posOnGeneticMapBasedOnRefGenome(
                        sDB, y2
                    )
                    if iLG >= 0:
                        bPos = True
                        vPos = self.vPos_update(vPos, iLG, coorOnLG, [], [])
                    if bPos:
                        ctg.vPosOnRefGenomeMapped.append(q)
                    else:
                        ctg.vPosOnRefGenomeNonMapped.append(q)
                    # viChromosome.append()
            # if iBlock>20:
            # 	bContinue=False
            if len(ctg.vPos) == 0:
                ctg.vPos = vPos
        f.close()
        f1.close()
        print("mapContigsBasedOnReferenceGenome...Finished, see file " + sFileName1)

    def vLineOf_gff_make(self):
        if self.bvLineOf_gff:
            return
        print("vLineOf_gff_make...")
        sFileName = "C:\\Frenkel\\Privman\\Cnig_gn1\\annotation\\maker_master_all.log.all.gff\\Cnig_gn1___genesOnly_.gff"
        f = open(sFileName, "r")
        iRow = 0
        iCtg = -1
        sCtg = ""
        for s in f:
            if len(s) > 1:  # and iRow>0
                s = s[0 : len(s) - 1]  # cut \n
                ss = s.split("\t")
                if sCtg != ss[0]:
                    sCtg = ss[0]
                    iCtg = self.vCtgName.index(sCtg)
                ctg = self.vCtg[iCtg]
                ctg.vLineOf_gff.append(ctg.clLineOf_gff(s))
        self.bvLineOf_gff = True
        print("vLineOf_gff_make...Done")

    def printReportOnFastaFile(self, sFileName="ReportOnFastaFile.txt"):
        f = open(sFileName, "w")

        s = "report for\t" + self.fasta
        f.write(s + "\n")

        nCtgs = len(self.vCtg)
        s = "nContigs\t" + "{:,}".format(nCtgs)
        f.write(s + "\n")

        vLen = []
        nnn = 0
        for ctg in self.vCtg:
            nnn += ctg.seqLength
            vLen.append(ctg.seqLength)
        VovaMath = clVovaMath()

        s = "lenTotal\t" + "{:,}".format(nnn)
        f.write(s + "\n")

        if nCtgs > 1:
            s = "lenMean\t" + "{:,.1f}".format(VovaMath.mean(vLen))
            f.write(s + "\n")
            s = "lenSTDV\t" + "{:,.1f}".format(VovaMath.STDV(vLen))
            f.write(s + "\n")

            s = ""
            vLen.sort()
            i = 0
            for l in vLen:
                i += 1
                if i < 10 or nCtgs - i < 10:
                    if i > 1:
                        s += ", "
                    s += "{:,}".format(l)
                else:
                    if i == 10:
                        s += " ,..."
            s = "lengths:\t" + s
            f.write(s + "\n")

            # N50, L50 etc.
            s = "\np\tN,bp\tL,ctgs\tlenToCover\tlenCovered"
            f.write(s + "\n")
            lenCovered = 0
            iCtg = nCtgs
            ll = (
                0  # e.g., L50 is minimal number of contigs to cover 50% of all assembly
            )
            nn = 0  # e.g., N50 is length of the shortest contig in coverage of 50% of assembly by the longest contigs
            for i in range(9):
                p = (i + 1) * 10  # 10,20,...,50,...,90
                lenToCover = p * 0.01 * nnn
                while lenCovered < lenToCover and iCtg > 0:
                    iCtg -= 1
                    lenCovered += vLen[iCtg]
                    nn = vLen[iCtg]
                    ll += 1
                s = (
                    str(p)
                    + "\t"
                    + "{:,}".format(nn)
                    + "\t"
                    + "{:,}".format(ll)
                    + "\t"
                    + "{:,}".format(lenToCover)
                    + "\t"
                    + "{:,}".format(lenCovered)
                )
                f.write(s + "\n")

        f.write("\nctg\tlen\n")
        for ctg in self.vCtg:
            s = ctg.name + "\t" + "{:,}".format(ctg.seqLength)
            f.write(s + "\n")
        f.close()

    def printSeqsBasedOnListOfName(
        self, vsPartOfSeqName, sDobaffka, sFileNameFasta, indexOfFormatSequenceName=-1
    ):
        self.readFromFastaFile(sFileNameFasta, -1, True)
        sFileName = sFileNameFasta + "_" + sDobaffka + ".fasta"
        f = open(sFileName, "w")
        for ctg in self.vCtg:
            b = False
            for s in vsPartOfSeqName:
                if ctg.name.find(s) >= 0:
                    b = True
            if b:
                # def printSeqToFile(self,f,sDobaffka,nNNNaddAtleast,bPrintName)
                ctg.printSeqToFile(f, "", 0, True)
        f.close()


class clSeq:
    def __init__(self):
        self.seq = ""
        self.nLetters = [0, 0, 0, 0, 0, 0]
        self.pLetters = [0, 0, 0, 0, 0, 0]
        self.nACGT = 0
        self.pGC = 0
        self.nPeriodMax = 20
        self.pPeriodicityE = []  # Exact
        self.pPeriodicityT = []  # Toleranted
        self.pPeriodicityE_exp = 0  # Exact
        self.pPeriodicityT_exp = 0  # Toleranted
        self.nPletMax = 2  # 3
        self.vvsPlet = [[]]  # [["AA","AC",...,"TT"],["AAA","AAC",...,"TTT"],...]
        self.vvpPlet = [[]]  # [[p_AA,p_AC,...,p_TT],[p_AAA,p_AAC,...,p_TTT],...]
        self.vvpPlet_exp = [[]]  # [[p_AA,p_AC,...,p_TT],[p_AAA,p_AAC,...,p_TTT],...]

    def i_s_get(self, s):
        if s == "n" or s == "N":
            return 0
        if s == "a" or s == "A":
            return 1
        if s == "c" or s == "C":
            return 2
        if s == "g" or s == "G":
            return 3
        if s == "t" or s == "T":
            return 4
        return 5

    def s_i_get(self, i, bCapital):
        if i == 0:
            #'Yes' if fruit == 'Apple' else 'No'
            return "N" if bCapital else "n"
        if i == 1:
            return "A" if bCapital else "a"
        if i == 2:
            return "C" if bCapital else "c"
        if i == 3:
            return "G" if bCapital else "g"
        if i == 4:
            return "T" if bCapital else "t"
        if i == 5:
            return "*"

    def j_i_get(self, i):
        j = i
        if i == 2 or i == 3:  # G,C
            return 1
        if i == 1 or i == 4:  # A,T
            return 2

    def nLetters_get(self):
        self.nLetters = [0, 0, 0, 0, 0, 0]
        for s1 in self.seq:
            i = self.i_s_get(s1)
            self.nLetters[i] += 1
        self.pLetters = [0, 0, 0, 0, 0, 0]
        self.nACGT = 0
        for i in range(1, 4 + 1):
            self.nACGT += self.nLetters[i]

        self.pPeriodicityE_exp = 0  # Exact
        self.pPeriodicityT_exp = 0  # Toleranted
        if self.nACGT > 0:
            self.pLetters[0] = float(self.nLetters[0]) / (self.nLetters[0] + self.nACGT)
            for i in range(1, 4 + 1):
                self.pLetters[i] = float(self.nLetters[i]) / self.nACGT
            self.pGC = (
                self.pLetters[self.i_s_get("G")] + self.pLetters[self.i_s_get("C")]
            )

        if self.nACGT > self.nPeriodMax:  # 20
            for i in range(1, 4 + 1):
                self.pPeriodicityE_exp += self.pLetters[i] * self.pLetters[i]
            p = self.pLetters[1] + self.pLetters[4]
            self.pPeriodicityT_exp = p * p + (1 - p) * (1 - p)

            self.pPeriodicityE = [1]
            self.pPeriodicityT = [1]
            for delta in range(1, self.nPeriodMax + 1):
                n = 0
                kE = 0
                kT = 0
                for i in range(0, len(self.seq) - delta):
                    i1 = i + delta
                    a = self.i_s_get(self.seq[i])
                    a1 = self.i_s_get(self.seq[i1])
                    if a > 0 and a < 5 and a1 > 0 and a1 < 5:
                        n += 1
                        if a == a1:
                            kE += 1
                            kT += 1
                        else:
                            if self.j_i_get(a) == self.j_i_get(a1):
                                kT += 1
                if n > 0:
                    self.pPeriodicityE.append(float(kE) / n)
                    self.pPeriodicityT.append(float(kT) / n)
                else:
                    self.pPeriodicityE.append(-1)
                    self.pPeriodicityT.append(-1)

    def s_nLetters_Shapka(self, bnLetters=True, bAll=True, bnACGT=True, bpLetters=True):
        s = ""
        bCapital = True
        iMin = 0 if bAll else 1
        iMax = 5 if bAll else 4
        if bnLetters:
            for i in range(iMin, iMax + 1):
                s += "\t" + "n" + self.s_i_get(i, bCapital)
        if bnACGT:
            s += "\t" + "nACGT"
        if bpLetters:
            for i in range(iMin, iMax + 1):
                s += "\t" + "p" + self.s_i_get(i, bCapital)
        s += "\t" + "pGC"
        return s

    def s_nLetters(self, bnLetters=True, bAll=True, bnACGT=True, bpLetters=True):
        s = ""
        bCapital = True
        iMin = 0 if bAll else 1
        iMax = 5 if bAll else 4
        if bnLetters:
            for i in range(iMin, iMax + 1):
                s += "\t" + str(self.nLetters[i])
        if bnACGT:
            s += "\t" + str(self.nACGT)
        if bpLetters:
            for i in range(iMin, iMax + 1):
                s += "\t" + str(self.pLetters[i])
        s += "\t" + str(self.pGC)
        return s

    def s_periodicity_Shapka(self):
        s = ""
        for delta in range(1, self.nPeriodMax + 1):
            s += "\t" + "pE" + str(delta)
        for delta in range(1, self.nPeriodMax + 1):
            s += "\t" + "pT" + str(delta)
        return s

    def s_periodicity(self):
        s = ""
        VovaMath = clVovaMath()
        bSignifOnly = True
        pValCutoff = 0.01
        for delta in range(1, self.nPeriodMax + 1):
            p = self.pPeriodicityE[delta]
            s0 = str(p)
            if bSignifOnly:
                p_e = self.pPeriodicityE_exp
                pVal = VovaMath.pEqFreq(p, p_e, self.nACGT)
                if pVal > pValCutoff:
                    s0 = ""
            s += "\t" + s0
        for delta in range(1, self.nPeriodMax + 1):
            p = self.pPeriodicityT[delta]
            s0 = str(p)
            if bSignifOnly:
                p_e = self.pPeriodicityT_exp
                pVal = VovaMath.pEqFreq(p, p_e, self.nACGT)
                if pVal > pValCutoff:
                    s0 = ""
            s += "\t" + s0
        return s

    def vvsPlet_make(self):
        self.vvsPlet = [[]]  # [["AA","AC",...,"TT"],["AAA","AAC",...,"TTT"],...]
        VovaMath = clVovaMath()
        for nPlet in range(2, self.nPletMax + 1):
            vCode = []
            vCodeMax = [4] * nPlet  # [4,4,4,..,4]
            vsPlet = []
            b, vCode = VovaMath.bCodeNext(vCode, nPlet, vCodeMax, False)
            while b:
                # print str(nPlet)+": "+str(vCode)+", vMax="+str(vCodeMax)
                sPlet = ""
                bCapital = True
                for i in range(nPlet):
                    sPlet += self.s_i_get(vCode[i], bCapital)
                vsPlet.append(sPlet)
                b, vCode = VovaMath.bCodeNext(vCode, nPlet, vCodeMax, False)
            self.vvsPlet.append(vsPlet)

    def vvpPlet_make(self):
        self.vvpPlet = [[]]  # [[p_AA,p_AC,...,p_TT],[p_AAA,p_AAC,...,p_TTT],...]
        self.vvpPlet_exp = [[]]

        # for nPlet in range(2,self.nPletMax+1):
        nPlet = 1
        for vsPlet in self.vvsPlet:
            nPlet += 1
            nn = 0
            vpPlet = []
            vpPlet_exp = []
            for sPlet in vsPlet:
                n = self.seq.count(
                    sPlet
                )  # number of times of presence of substring s in the sequence
                nn += n
                vpPlet.append(n)
                pPlet_exp = 1
                for s in sPlet:
                    i = self.i_s_get(s)
                    pPlet_exp *= self.pLetters[i]
                vpPlet_exp.append(pPlet_exp)
            if nn > 1:
                # for pPlet in vpPlet:
                for i in range(len(vpPlet)):
                    # print str(pPlet)+", "+str(n)
                    # pPlet=float(pPlet)/nn
                    vpPlet[i] = float(vpPlet[i]) / nn
                    # print str(pPlet)
            self.vvpPlet.append(vpPlet)
            self.vvpPlet_exp.append(vpPlet_exp)

    def s_Plet_Shapka(self):
        self.vvsPlet_make()
        s = ""
        nPlet = 1
        for vsPlet in self.vvsPlet:
            nPlet += 1
            for sPlet in vsPlet:
                s += "\t" + sPlet
        return s

    def s_Plet(self):
        self.vvsPlet_make()
        self.vvpPlet_make()
        VovaMath = clVovaMath()
        s = ""
        nPlet = 1
        bSignifOnly = True
        pValCutoff = 0.01
        i = 0
        for vpPlet in self.vvpPlet:
            nPlet += 1
            j = 0
            for pPlet in vpPlet:
                s0 = str(pPlet)
                if bSignifOnly:
                    p_e = self.vvpPlet_exp[i][j]
                    pVal = VovaMath.pEqFreq(pPlet, p_e, self.nACGT)
                    if pVal > pValCutoff:
                        s0 = ""
                s += "\t" + s0
                j += 1
            i += 1
        return s

    def split(self, end1, end2):  # s0,s1,s2= (split chimeras)
        n = len(self.seq)
        s0 = self.seq[0:end1]
        s1 = self.seq[end1:end2]
        s1 = self.seq[end2:end0]
        return s0, s1, s2

    def coorOnReversedSeq(self, coorStartFrom1):
        n = len(self.seq)
        return n - coorStartFrom1 + 1

    def reverseSeq(self):
        sRev = self.seq[::-1]  # copy of string in reverse order
        # s="abc"
        # s1=s[::-1]
        # print s
        # print s1
        # s="oO"
        # print s
        # print s1

        # A<->T, C<->G
        sRev = sRev.replace("A", "1")
        sRev = sRev.replace("T", "A")
        sRev = sRev.replace("1", "T")
        #
        sRev = sRev.replace("C", "1")
        sRev = sRev.replace("G", "C")
        sRev = sRev.replace("1", "G")
        return sRev

    def printToOpenedFile(self, f, nLettersPerRow=80):
        # not in use (long lines are hard for python)
        # usually newline=chr(10)="\n"=<LF> in Linux, chr(13)+chr(10)=<CR>+<LF> in windows
        s = self.seq
        while len(s) > 0:
            if len(s) <= nLettersPerRow:
                f.write(s + chr(10))  # "\n"
            else:
                s1 = s[0, nLettersPerRow]
                f.write(s1)
                f.write(chr(10))  # "\n"
                s = s[nLettersPerRow:]


class clNetBasedOnBlastRes:
    def __init__(
        self,
        sFileNameBlastResults_set,
        idOfFastaFileInUseToMapContigsWithoutMarkers_set,
        mySecCtgs_set=clSecCtgs(),
    ):
        self.sFileNameBlastResults = sFileNameBlastResults_set
        self.idOfFastaFileInUseToMapContigsWithoutMarkers = (
            idOfFastaFileInUseToMapContigsWithoutMarkers_set
        )
        self.mySecCtgs = mySecCtgs_set
        self.net = clNetVova()
        self.bNoFilesWithSequencesAreLoaded = False
        self.start()

    def start(self):
        f = open(self.sFileNameBlastResults, "r")
        self.net = clNetVova()
        self.bNoFilesWithSequencesAreLoaded = len(self.mySecCtgs.vCtg) < 1
        if not self.bNoFilesWithSequencesAreLoaded:
            i = 0
            for s in self.mySecCtgs.vCtgName:
                self.net.addNode(id=i, caption=s)
                i += 1
        sQ_prev = ""
        viDB = []
        iRow = 0
        nMaxInQ = 0
        for s in f:
            iRow += 1
            if iRow % 10000 == 1:
                print(
                    "netBasedOnBlastRes for "
                    + self.sFileNameBlastResults
                    + ": "
                    + str(iRow)
                    + " rows processed"
                )
            # if iRow>100000:
            # 	break
            if len(s) > 1:
                if s[0] != "#":
                    s = s[0 : len(s) - 1]  # cut \n
                    myBlastRes = clBlastRes()
                    myLineOfBlastRes = myBlastRes.clLineOfBlastRes(s)
                    sDB = myLineOfBlastRes.sDB
                    if myLineOfBlastRes.sQ != sQ_prev:
                        if sQ_prev != "":
                            self.processBlock(viDB, sQ_prev, nMaxInQ)
                            viDB = []
                            nMaxInQ = 0

                    if nMaxInQ < myLineOfBlastRes.startQ:
                        nMaxInQ = myLineOfBlastRes.startQ
                    if nMaxInQ < myLineOfBlastRes.endQ:
                        nMaxInQ = myLineOfBlastRes.endQ

                    if self.bNoFilesWithSequencesAreLoaded:
                        if not sDB in self.mySecCtgs.vCtgName:
                            self.mySecCtgs.vCtgName.append(sDB)
                            ctg = self.mySecCtgs.clSecCtg()
                            ctg.name = sDB
                            ctg.nameProcess(0)
                            self.mySecCtgs.vCtg.append(ctg)
                            self.net.addNode(id=self.net.nNodes, caption=sDB)
                    iDB = self.mySecCtgs.vCtgName.index(sDB)
                    if (
                        self.idOfFastaFileInUseToMapContigsWithoutMarkers == 1
                        or myLineOfBlastRes.nLen >= 500
                    ):
                        if not iDB in viDB:
                            viDB.append(iDB)
                    sQ_prev = myLineOfBlastRes.sQ
        self.processBlock(viDB, sQ_prev, nMaxInQ)
        f.close()
        # print "nNodes="+str(self.net.nNodes)+", nEdges="+str(self.net.nEdges)

        print("nNodes=" + str(self.net.nNodes) + ", nEdges=" + str(self.net.nEdges))

    def ClusteringAndReport(self):
        clusters, inCluster = self.net.singleLinkageClustering(2)

        sFileNameLog = "clustersBasedOnBlast"
        if self.idOfFastaFileInUseToMapContigsWithoutMarkers == 1:
            sFileNameLog += "Diploids.txt"
        if self.idOfFastaFileInUseToMapContigsWithoutMarkers == 2:
            sFileNameLog += "SolenopsisInvicta.txt"
        f = open(sFileNameLog, "w")
        k = 0
        f.write("k\tlenCluster\tsum\tlens\tctgs\tsPos\n")
        for cluster in clusters:
            nn = 0
            vn = []
            for i in cluster:
                n = self.mySecCtgs.vCtg[i].seqLength
                vn.append(n)
                nn += n
            lenCluster = len(cluster)
            if lenCluster > 1:
                k += 1
                # print str(k)+": sum="+str(nn)+", "+str(vn)
                svn = ""
                sctgs = ""
                sPos = ""
                vPos = []
                # vPos_update(self.mySecCtgs,vPos,iLG,x,vLGmarker,vmBad)
                for i in range(lenCluster):
                    if i > 0:
                        svn += "_"
                        sctgs += ","
                        sPos += "_"
                    svn += str(vn[i])
                    sctgs += self.mySecCtgs.vCtg[cluster[i]].name
                    sPos += self.mySecCtgs.vCtg[cluster[i]].sPos()
                    for pos in self.mySecCtgs.vCtg[cluster[i]].vPos:
                        vPos = self.mySecCtgs.vPos_update(
                            vPos, pos.iLG, pos.coor, pos.markersGood, pos.markersBad
                        )
                s = (
                    str(k)
                    + "\t"
                    + str(lenCluster)
                    + "\t"
                    + str(nn)
                    + "\t"
                    + svn
                    + "\t"
                    + sctgs
                    + "\t"
                    + sPos
                    + "\n"
                )
                f.write(s)

                if len(vPos) in range(1, 5 + 1):
                    for i in range(lenCluster):
                        if (
                            len(self.mySecCtgs.vCtg[cluster[i]].vPos) == 0
                            or self.mySecCtgs.vCtg[
                                cluster[i]
                            ].idOfFastaFileInUseToMapContigsWithoutMarkers
                            > 0
                        ):
                            self.mySecCtgs.vCtg[cluster[i]].vPos = vPos
                            self.mySecCtgs.vCtg[
                                cluster[i]
                            ].iBasedOnClusterOfBlastRes = (
                                self.idOfFastaFileInUseToMapContigsWithoutMarkers
                            )
                            self.mySecCtgs.vCtg[
                                cluster[i]
                            ].idOfFastaFileInUseToMapContigsWithoutMarkers = 0

        nSumMappedNotOne = 0
        nSumMappedOne = 0
        nSumMappedNotOneDirect = 0
        nSumMappedOneDirect = 0
        nSumMappedOneGoodsOnly = 0
        nSumMappedNotOneGoodsOnly = 0
        nSumMappedNotOneBlastSingle = 0
        nSumMappedOneBlastSingle = 0
        nSumMappedNotOneBlastClusters = 0
        nSumMappedOneBlastClusters = 0
        for ctg in self.mySecCtgs.vCtg:
            # poka
            # if ctg.idOfFastaFileInUseToMapContigsWithoutMarkers>0:
            # 	if len(ctg.vPos)>10:
            # 		ctg.idOfFastaFileInUseToMapContigsWithoutMarkers=0
            # 		ctg.vPos=[]

            # BasedOnBlastRes, not clusters
            if ctg.idOfFastaFileInUseToMapContigsWithoutMarkers > 0:
                if len(ctg.vPos) == 1:
                    nSumMappedOneBlastSingle += ctg.seqLength
                else:
                    nSumMappedNotOneBlastSingle += ctg.seqLength

            # clusters of blast results
            if ctg.iBasedOnClusterOfBlastRes > 0:
                if len(ctg.vPos) == 1:
                    nSumMappedOneBlastClusters += ctg.seqLength
                else:
                    nSumMappedNotOneBlastClusters += ctg.seqLength
            # based on good and bad markers:
            if (
                (ctg.iBasedOnClusterOfBlastRes == 0)
                and (ctg.idOfFastaFileInUseToMapContigsWithoutMarkers == 0)
                and (len(ctg.vPos) > 0)
            ):
                if len(ctg.vPos) == 1:
                    nSumMappedOneDirect += ctg.seqLength
                    if ctg.basedOnGoodMarkersOnly:
                        nSumMappedOneGoodsOnly += ctg.seqLength
                else:
                    if ctg.basedOnGoodMarkersOnly:
                        nSumMappedNotOneGoodsOnly += ctg.seqLength
                    nSumMappedNotOneDirect += ctg.seqLength
            # all
            if len(ctg.vPos) > 0:
                if len(ctg.vPos) == 1:
                    nSumMappedOne += ctg.seqLength
                else:
                    nSumMappedNotOne += ctg.seqLength

        s = "k=" + str(k) + "\n"
        s += (
            "nSumMappedOne="
            + str(nSumMappedOne)
            + ", nSumMappedNotOne="
            + str(nSumMappedNotOne)
            + "\n"
        )
        s += (
            "nSumMappedOneGoodsOnly="
            + str(nSumMappedOneGoodsOnly)
            + ", nSumMappedNotOneGoodsOnly="
            + str(nSumMappedNotOneGoodsOnly)
            + "\n"
        )
        s += (
            "nSumMappedOneDirect="
            + str(nSumMappedOneDirect)
            + ", nSumMappedNotOneDirect="
            + str(nSumMappedNotOneDirect)
            + "\n"
        )
        s += (
            "nSumMappedOneBlastSingle="
            + str(nSumMappedOneBlastSingle)
            + ", nSumMappedNotOneBlastSingle="
            + str(nSumMappedNotOneBlastSingle)
            + "\n"
        )
        s += (
            "nSumMappedOneBlastClusters="
            + str(nSumMappedOneBlastClusters)
            + ", nSumMappedNotOneBlastClusters="
            + str(nSumMappedNotOneBlastClusters)
            + "\n"
        )
        f.write(s)
        f.close()

        # k=16370,
        # nSumMappedOne=				119,279,027, nSumMappedNotOne=			52,767,084,
        # nSumMappedOneDirect=		107,605,576, nSumMappedNotOneDirect=	21,453,337,
        # nSumMappedOneBlastSingle=	5,291,068, nSumMappedNotOneBlastSingle=	28,043,095,
        # nSumMappedOneBlastClusters=6,382,383, nSumMappedNotOneBlastClusters=3,270,652
        print(s)

    def processBlock(self, viDB, sQ, nMaxInQ):
        # viDB = list of iDB in the block of blast results, each iDB is id of sequence from DB
        # sQ = quary name
        # nMaxInQ = length of quary (unobserved in file with results of blast)
        #
        # =1#poka
        n = len(viDB)
        if n > 1:
            print(sQ + ", n=" + str(n))
            ctgQ = self.mySecCtgs.clSecCtg()
            ctgQ.name = sQ

            # NODE_4099_length_20484_cov_2.15304 (like original)
            # Si_gnG.scaffold03952 (no info on length)
            # ctgQ.nameProcess(0)
            ctgQ.seqLength = nMaxInQ
            nnn = 0
            # print "len"
            for i in range(n):
                iDB = viDB[i]
                nnn += self.mySecCtgs.vCtg[iDB].seqLength

            if nnn < 1000:
                if nnn > ctgQ.seqLength * 20:
                    return
            else:
                if nnn > ctgQ.seqLength * 5:
                    return

            # print "vPos"
            vPos = []
            for i in range(n):
                iDB = viDB[i]
                for pos in self.mySecCtgs.vCtg[iDB].vPos:
                    vPos = self.mySecCtgs.vPos_update(
                        vPos, pos.iLG, pos.coor, pos.markersGood, pos.markersBad
                    )

            # print "pos upd"

            nPosMax = 5
            if nMaxInQ > 500000:  # 500 kbp
                nPosMax = 10
            if nMaxInQ > 1500000:  # 1.5 Mbp
                nPosMax = 15

            if len(vPos) in range(1, nPosMax + 1):
                for i in range(n):
                    iDB = viDB[i]
                    ctg = self.mySecCtgs.vCtg[iDB]
                    if (
                        len(ctg.vPos) == 0
                        and ctg.idOfFastaFileInUseToMapContigsWithoutMarkers == 0
                    ):
                        ctg.vPos = vPos
                        ctg.idOfFastaFileInUseToMapContigsWithoutMarkers = (
                            self.idOfFastaFileInUseToMapContigsWithoutMarkers
                        )
                    else:
                        if ctg.idOfFastaFileInUseToMapContigsWithoutMarkers > 0:
                            for pos in vPos:
                                # ctg.vPos=self.mySecCtgs.vPos_update(ctg.vPos,pos.iLG,pos.coor,pos.markersGood,pos.markersBad)
                                ctg.vPos = self.mySecCtgs.vPos_update(
                                    ctg.vPos, pos.iLG, pos.coor, [], []
                                )
                                if len(ctg.vPos) > nPosMax:
                                    f = open("logloglog.txt", "a")
                                    s = (
                                        sQ
                                        + "\t"
                                        + str(nMaxInQ)
                                        + "\t"
                                        + str(
                                            self.idOfFastaFileInUseToMapContigsWithoutMarkers
                                        )
                                        + "\t"
                                        + str(len(ctg.vPos))
                                        + "\t"
                                        + str(nPosMax)
                                        + "\n"
                                    )
                                    f.write(s)
                                    f.close()
                                    ctg.vPos = []
                                    ctg.idOfFastaFileInUseToMapContigsWithoutMarkers = (
                                        -1
                                    )
                                    break
            print("e")
            for i in range(n):
                iDB = viDB[i]
                for j in range(i + 1, n):
                    jDB = viDB[j]
                    # print "nNodes="+str(self.net.nNodes)+", iDB="+str(iDB)
                    if not self.net.node[iDB].bExistEdgeToNodeID(jDB):
                        e = self.net.clEdge()
                        e.get(
                            idStart=iDB,
                            idEnd=jDB,
                            val=1,
                            sc="black",
                            w=1,
                            sp="Solid",
                            sl=sQ,
                        )
                        self.net.addEdge(e)


class clAssemblyMy:
    def __init__(
        self, SecCtgs=[], sAssemblyName="sAssemblyName", sPath=""
    ):  # self.sPath="C:\\Frenkel\\LTCPython\\VovaPy\\"
        self.SecCtgs = SecCtgs
        self.sAssemblyName = sAssemblyName

        self.vLGwithSeq = []  # array of clLGwithSeq()
        # self.nNNNaddAtleastSTANDARD=300#number of "N"s to add between merged sequences
        self.nNNNaddAtleastSTANDARD = 200  # Eyal 2021.05.30
        self.sumDoubleOrMore = 0
        self.sumAtLeastOne = 0
        self.sPath = sPath
        self.sChrNamingAndOrientationStrategy = ""

        # self.vLGwithSeq_make(vLG,sSeqAssemblyName)

    class clAssemblyElement:
        def __init__(
            self,
            iLG=-1,
            iCtg=-1,
            iPos=-1,
            coorOnLG_min=-1,
            coorOnLG_max=-1,
            aStart=-1,
            aEnd=-1,
            orientation=0,
            vsMarkers=[],
            vCoorOnCtg=[],
            vCoorOnLG=[],
            bFrom0=True,
            bToEndOfCtg=True,
        ):
            self.iLG = iLG
            self.iCtg = iCtg  # adress of sequence contig in self.SecCtgs.vCtg (the same ctg can be in several AssemblyElements)
            self.iPos = iPos  # index of position on genetic map (usually 0, but can be higher for contigs with multiple position)
            self.coorOnLG = 0.5 * (coorOnLG_min + coorOnLG_max)  # genetic map old
            self.coorOnLG_min = coorOnLG_min  # genetic map
            self.coorOnLG_max = coorOnLG_max  # genetic map
            self.posOfStartInChr = 0  # physical map
            self.aStart = aStart  # 0
            self.aEnd = aEnd  # partLength
            self.totalLengthOfCtg = aEnd  # should be partLength, poka tak

            self.bFrom0 = bFrom0
            self.bToEndOfCtg = bToEndOfCtg

            self.orientation = orientation
            self.vsMarkers = vsMarkers
            self.vCoorOnCtg = vCoorOnCtg
            self.vCoorOnLG = vCoorOnLG
            self.bOn = True
            self.layer = 0

        def lengthOnCtg(self):
            aStart = 0 if self.bFrom0 else self.aStart
            aEnd = self.totalLengthOfCtg if self.bToEndOfCtg else self.aEnd
            return aEnd - aStart

        def totalLengthOfCtg_set(self, totalLengthOfCtg_set, bUpdate_aStart_aEnd):
            self.totalLengthOfCtg = totalLengthOfCtg_set
            if bUpdate_aStart_aEnd:
                if self.bFrom0:
                    aStart = 0
                if self.bToEndOfCtg:
                    self.aEnd = self.totalLengthOfCtg

        def sShapka(self, bDetails=True):
            s1 = "iLG" + "\t" + "iCtg" + "\t" + "iPos" + "\t" + "orientation"
            s1 += "\t" + "coorOnLG_min" + "\t" + "coorOnLG_max"
            s1 += "\t" + "aStart" + "\t" + "aEnd"
            s1 += "\t" + "bFrom0" + "\t" + "bToEndOfCtg"
            if bDetails:
                s1 += "\t" + "vsMarkers"
                s1 += "\t" + "vCoorOnCtg"
                s1 += "\t" + "vCoorOnLG"
            else:
                s1 += "\t" + "len(vsMarkers"
            s1 += "\t" + "bOn"
            return s1

        def s(self, bDetails=True):
            s1 = (
                str(self.iLG)
                + "\t"
                + str(self.iCtg)
                + "\t"
                + str(self.iPos)
                + "\t"
                + str(self.orientation)
            )
            s1 += "\t" + str(self.coorOnLG_min) + "\t" + str(self.coorOnLG_max)
            s1 += "\t" + str(self.aStart) + "\t" + str(self.aEnd)
            s1 += "\t" + str(self.bFrom0) + "\t" + str(self.bToEndOfCtg)
            if bDetails:
                s1 += "\t" + str(self.vsMarkers)
                s1 += "\t" + str(self.vCoorOnCtg)
                s1 += "\t" + str(self.vCoorOnLG)
            else:
                s1 += "\t" + str(len(self.vsMarkers))
            s1 += "\t" + str(self.bOn)
            return s1

        def excludeOverlapsOnSecCtg(self, vAssemblyElement):  # lenOk,lenLayerMore0=
            def MyFunc(AssemblyElement):
                return AssemblyElement.vCoorOnCtg[0]

            vAssemblyElement.sort(key=MyFunc)
            AssemblyElement_prev = vAssemblyElement[0]
            iAssemblyElementOn = 0
            lenLayerMore0 = 0
            lenOk = 0
            for AssemblyElement in vAssemblyElement:
                b = False
                if AssemblyElement.bOn:
                    b = True
                    if iAssemblyElementOn > 0:
                        if AssemblyElement_prev.aEnd > AssemblyElement.aStart:
                            n_prev = len(AssemblyElement_prev.vsMarkers)
                            n = len(AssemblyElement.vsMarkers)
                            if (
                                AssemblyElement_prev.vCoorOnCtg[n_prev - 1]
                                <= AssemblyElement.vCoorOnCtg[0]
                            ):
                                AssemblyElement_prev.aEnd = (
                                    AssemblyElement_prev.vCoorOnCtg[n_prev - 1]
                                )
                                AssemblyElement.aStart = AssemblyElement.vCoorOnCtg[0]
                            else:
                                b = False
                                if (
                                    AssemblyElement.vCoorOnCtg[0]
                                    == AssemblyElement.vCoorOnCtg[n - 1]
                                ):
                                    AssemblyElement.bOn = False
                                else:
                                    AssemblyElement.aStart = AssemblyElement.vCoorOnCtg[
                                        0
                                    ]
                                    AssemblyElement.aEnd = AssemblyElement.vCoorOnCtg[
                                        n - 1
                                    ]
                                    AssemblyElement.layer = (
                                        AssemblyElement_prev.layer + 1
                                    )
                                    lenLayerMore0 += (
                                        AssemblyElement.aEnd - AssemblyElement.aStart
                                    )
                if AssemblyElement.bOn:
                    if b:
                        lenOk += AssemblyElement.aEnd - AssemblyElement.aStart
                    AssemblyElement_prev = AssemblyElement
                    iAssemblyElementOn += 1
            return lenOk, lenLayerMore0

        def printToFileFasta_v0(
            self, SecCtgs, f, bTheLast, nNNNaddAtleast
        ):  # nNNNadded=
            # to add "N"s after
            if bTheLast:
                nNNNaddAtleast = 0  # the last on chr
            iCtgOriginal = AssemblyElement.iCtg
            ctg = SecCtgs.vCtg[iCtgOriginal]
            nNNNadded = ctg.printSeqToFile(f, "", nNNNaddAtleast, False)
            return nNNNadded

        def printToFileFasta(
            self, SecCtgs, f, sNNN_current, iRowStart, iPosLast
        ):  # nNNNadded,nFromCtg,iRowStart,iRowEnd,iPosLast,bEndOfLineSymbolDone=
            # vSeq#
            #
            iCtgOriginal = self.iCtg
            # print str(iCtgOriginal)

            ctg = SecCtgs.vCtg[iCtgOriginal]
            if False:  # old version: hard long line for python
                sSeq = ctg.sSeq_get()
                sSeq = sSeq[self.aStart, sEnd]
                mySeq = clSeq()
                mySeq.seq = sSeq
                if self.orientation < 0:
                    mySeq.seq = mySeq.reverseSeq()
                # to add "N"s after
                mySeq.seq += sNNN_current
                mySeq.printToOpenedFile(f)

            # vSeq = array of selected sequences (already with added NNNN, excluded EndOfLine symbol and taking into account orientation)
            vSeq = []
            if self.orientation < 0:
                # to add "N"s after
                vSeq.append(sNNN_current)
            nInputed = 0
            mySeq = clSeq()
            for seq in ctg.seq:
                n = len(seq) - 1  # to exclude the last symbol chr(10)
                a0 = 0 if self.aStart - nInputed <= 0 else self.aStart - nInputed
                a1 = n if self.aEnd - nInputed >= n else self.aEnd - nInputed
                if a1 > a0:
                    # print str(a0)+" "+str(a1)
                    s = seq[int(a0) : int(a1)]
                    if self.orientation < 0:
                        mySeq.seq = s
                        s = mySeq.reverseSeq()
                    vSeq.append(s)
                nInputed += n
            if self.orientation >= 0:
                # to add "N"s after
                vSeq.append(sNNN_current)
            if self.orientation < 0:
                vSeq = reversed(
                    vSeq
                )  # standard function in Python making array in reverse order

            nLettersInRowStandard = 80
            iRowEnd = iRowStart
            nFromCtg = 0
            bEndOfLineSymbolDone = False
            for seq in vSeq:
                n = len(seq)
                if n + iPosLast < nLettersInRowStandard:  # we have room till end of row
                    f.write(seq)
                    iPosLast += n
                    nFromCtg += n
                    bEndOfLineSymbolDone = False
                else:
                    f.write(seq[0 : nLettersInRowStandard - iPosLast])
                    nFromCtg += nLettersInRowStandard - iPosLast
                    f.write(chr(10))  # ("\n")
                    bEndOfLineSymbolDone = True
                    iRowEnd += 1
                    seq = seq[nLettersInRowStandard - iPosLast :]
                    while len(seq) >= nLettersInRowStandard:
                        f.write(seq[0:nLettersInRowStandard])
                        nFromCtg += nLettersInRowStandard
                        f.write(chr(10))  # ("\n")
                        bEndOfLineSymbolDone = True
                        iRowEnd += 1
                        seq = seq[nLettersInRowStandard:]
                    if len(seq) > 0:
                        f.write(seq)
                        bEndOfLineSymbolDone = False
                    iPosLast = len(seq)
                    nFromCtg += iPosLast
            nFromCtg -= len(sNNN_current)
            # f.write(chr(10))#("\n")
            # bEndOfLineSymbolDone=True
            return len(sNNN_current), nFromCtg, iRowEnd, iPosLast, bEndOfLineSymbolDone

    class clLGwithSeq:
        def __init__(self):
            # self.LG=LG
            self.vAssemblyElement = []  # array of clAssemblyElement()
            self.totalLengthBp = 0
            self.totalLengthcM = 0
            self.name = ""  # my chromosome name
            self.orientation = 1

    def vLGwithSeq_make(
        self, vLG, sSeqAssemblyName
    ):  # ordered list of [iCtg,iPos,pos.iLG,pos.coor] (ordered based on genetic map)
        # use arrays ctg.vPos for each ctg in self.SecCtgs.vCtg:
        self.vLGwithSeq = []

        # inicialize self.vLGwithSeq
        for LG in vLG:
            nM = len(LG.vLGmarkerOrderedByCoorOnLG)
            if nM > 1:
                coorMin = LG.vLGmarkerOrderedByCoorOnLG[0].coorOnLG
                coorMax = LG.vLGmarkerOrderedByCoorOnLG[nM - 1].coorOnLG
            LGwithSeq = self.clLGwithSeq()
            LGwithSeq.LG = LG
            LGwithSeq.totalLengthcM = coorMax - coorMin
            self.vLGwithSeq.append(LGwithSeq)

        # LGwithSeq.vAssemblyElement
        iCtg = 0
        for ctg in self.SecCtgs.vCtg:
            iPos = 0
            for pos in ctg.vPos:
                iLG = pos.iLG
                # AssemblyElement=self.clAssemblyElement(iCtg,iPos,pos.coor)
                AssemblyElement = self.clAssemblyElement(
                    iLG, iCtg, iPos, pos.coor, pos.coor, 0, ctg.seqLength, 1
                )
                LGwithSeq = self.vLGwithSeq[iLG]
                LGwithSeq.vAssemblyElement.append(
                    AssemblyElement
                )  # the same ctg can be presented several times on LG due to markers having different coordinates
                iPos += 1
            iCtg += 1
        # sort LGwithSeq.vAssemblyElement by coor on genetic map
        def MyFunc1(AssemblyElement):
            return AssemblyElement.coorOnLG + 0.000001 * AssemblyElement.iCtg

        for LGwithSeq in self.vLGwithSeq:
            LGwithSeq.vAssemblyElement.sort(key=MyFunc1)
        # in this stage, the same ctg can be presented several times due to some different positions of ctg's markers on genetic map
        # already [at least, partialy] dealed in bAddPosition_get() of clSecCtgs()

        self.assemblyRun(False)

    def vLGwithSeq_make_new(
        self,
        vvAssemblyElementMap,
        vvAssemblyElementMapRef,
        vLength_cM,
        vLGname,
        bWithOrientationOnly,
    ):

        # use arrays ctg.vPos for each ctg in self.SecCtgs.vCtg:
        self.vLGwithSeq = []  # [iChr]

        # sort LGwithSeq.vAssemblyElement by coor on genetic map
        def MyFunc1(AssemblyElement):
            return (
                AssemblyElement.coorOnLG_min + 0.000001 * AssemblyElement.coorOnLG_max
            )

        self.vAssemblyElement_noOrientation = []
        self.vAssemblyElement_Q = []

        # vsChrNameToExclude=["LG26"]
        vsChrNameToExclude = []

        # inicialize self.vLGwithSeq
        iChr = 0
        for vAssemblyElement in vvAssemblyElementMapRef:  # by chromosomes
            vAssemblyElement.sort(key=MyFunc1)

            LGwithSeq = self.clLGwithSeq()
            LGwithSeq.LG = clLinkageGroup()
            LGwithSeq.LG.name = vLGname[iChr]
            LGwithSeq.vAssemblyElement = []
            LGwithSeq.totalLengthBp = 0
            nNonOrientation = 0
            if not (LGwithSeq.LG.name in vsChrNameToExclude):
                for AssemblyElement in vAssemblyElement:
                    if AssemblyElement.orientation == 0:
                        nNonOrientation += 1
                    if bWithOrientationOnly and AssemblyElement.orientation == 0:
                        self.vAssemblyElement_noOrientation.append(AssemblyElement)
                    else:
                        LGwithSeq.vAssemblyElement.append(AssemblyElement)
                        LGwithSeq.totalLengthBp += AssemblyElement.lengthOnCtg()
                LGwithSeq.totalLengthcM = vLength_cM[iChr]
            else:
                for AssemblyElement in vAssemblyElement:
                    self.vAssemblyElement_Q.append(AssemblyElement)
            self.vLGwithSeq.append(LGwithSeq)
            iChr += 1
            s = (
                str(iChr)
                + ": "
                + LGwithSeq.LG.name
                + " n="
                + str(len(LGwithSeq.vAssemblyElement))
            )
            s += ", LengthBp =" + str(LGwithSeq.totalLengthBp)
            s += ", Length_cM =" + str(LGwithSeq.totalLengthcM)
            s += ", nNonOrientation =" + str(nNonOrientation)
            s += ", nNoOrient till now =" + str(
                len(self.vAssemblyElement_noOrientation)
            )
            print(s)
            # print str(noOr)

        iPart = 0
        print("Q:")
        for vAssemblyElement in vvAssemblyElementMap:
            # print str(iPart)+" "+str(len(vAssemblyElement))
            for AssemblyElement in vAssemblyElement:
                if AssemblyElement.iLG < 0:
                    self.vAssemblyElement_Q.append(AssemblyElement)
                    # print str(AssemblyElement.iCtg)+"->"+str(AssemblyElement.iLG)
            iPart += 1
        print("nQ=" + str(len(self.vAssemblyElement_Q)))

        self.assemblyRun(True)

    def assemblyRun(self, bPrintOnlyTheMostRelevantFiles):

        # NB! .posOfStartInChr is calculated later, in function printAssemblyByChr() because it depends on amount of Ns
        # LGwithSeq.totalLengthBp
        self.sumAtLeastOne = 0
        self.sumDoubleOrMore = 0
        for LGwithSeq in self.vLGwithSeq:
            LGwithSeq.totalLengthBp = 0
            for AssemblyElement in LGwithSeq.vAssemblyElement:
                iPos = AssemblyElement.iPos
                AssemblyElement_lengthBp = AssemblyElement.lengthOnCtg()
                LGwithSeq.totalLengthBp += AssemblyElement_lengthBp
                if iPos == 0:
                    self.sumAtLeastOne += AssemblyElement_lengthBp
                if iPos > 0:
                    self.sumDoubleOrMore += AssemblyElement_lengthBp

        self.vLGwithSeq_make_NamesOfChromosomes()

        self.printAssemblyByChrReport()

        if not bPrintOnlyTheMostRelevantFiles:
            self.printAssemblyUnmapped()

        self.printAssemblyByChr(not bPrintOnlyTheMostRelevantFiles)

        if not bPrintOnlyTheMostRelevantFiles:
            self.printAssemblyByCtgWithDobaffkaToName()
            self.printMarkers()
            self.printMappingReport()
            self.print_mapped_gff(-1, -1, -1, "", False, True)
            self.printReportOnAllCtgs()

    def vLGwithSeq_make_NamesOfChromosomes(self):
        # names of chromosomes
        iChrNamingAndOrientationStrategy = 4
        if iChrNamingAndOrientationStrategy == 0:
            self.sChrNamingAndOrientationStrategy = (
                "BasedOnOriginalLGNameStartingFrom0_noOrdering"
            )
            # sort self.vLGwithSeq by physical length (on decreasing). here length is calculated without added Ns
            iLGwithSeq = 0
            for LGwithSeq in self.vLGwithSeq:
                LGwithSeq.name = "LG" + str(iLGwithSeq)  # starting from LG0
                iLGwithSeq += 1
        if iChrNamingAndOrientationStrategy == 1:
            self.sChrNamingAndOrientationStrategy = (
                "BasedOnLength_fromLongestToShortest"
            )
            # sort self.vLGwithSeq by physical length (on decreasing). here length is calculated without added Ns
            def MyFunc2(LGwithSeq):
                return LGwithSeq.totalLengthBp

            self.vLGwithSeq.sort(key=MyFunc2, reverse=True)
            #
            iLGwithSeq = 0
            for LGwithSeq in self.vLGwithSeq:
                LGwithSeq.name = "chr" + str(iLGwithSeq + 1)  # starting from Chr1
                iLGwithSeq += 1
        if iChrNamingAndOrientationStrategy == 2:
            self.sChrNamingAndOrientationStrategy = (
                "BasedOnPreviousNamingOfTheSameLinkageGroups"
            )
            # based on file: /cygdrive/c/Frenkel/LTCPython/VovaPy/20200531a/assemblyZeevByChrReport.txt
            # iChr	iLGoriginal	chr	lenPhys	lenGenet
            # 1	21	chr1	22957409	361.756522056
            # 2	15	chr2	18814069	341.424192654
            sFileNameNamingOfTheSameLinkageGroups = (
                "C:\\Frenkel\\LTCPython\\VovaPy\\20200531a\\assemblyZeevByChrReport.txt"
            )
            TableOfTxt = clTableOfTxt()
            TableOfTxt.readFromFile(sFileNameNamingOfTheSameLinkageGroups, True, False)
            iLGwithSeq = 0
            for LGwithSeq in self.vLGwithSeq:
                iLGoriginal = LGwithSeq.LG.id  # should be equal to iLGwithSeq, 0-26
                iRow = TableOfTxt.iRow_get(
                    str(iLGoriginal), 1
                )  # iLGoriginal=0 => iRow=9-1=8 (9	0	chr9	11577644	207.233558229)
                LGwithSeq.name = TableOfTxt.rows[iRow].vCellText[
                    2
                ]  # iLGoriginal=0 => "chr9"
                # "chr"+str(iLGwithSeq+1)
                iLGwithSeq += 1
        if iChrNamingAndOrientationStrategy == 3:
            self.sChrNamingAndOrientationStrategy = "BasedOnMapOfBesan"
            sFileNameNamingOfTheSameLinkageGroups = "C:\\Frenkel\\Privman\\GeneticMapping\\GeneticMapByBesan_2020\\newNamesAndOrientationForMyLG.txt"
            # i	sPart	chr	newOrient
            # 0	LG1	chr08	1
            # 1	LG2	chr12	1
            # 2	LG3	chr13	-1

            TableOfTxt = clTableOfTxt()
            TableOfTxt.readFromFile(sFileNameNamingOfTheSameLinkageGroups, True, False)
            TableOfTxt.vColText_make(1)  # original my names
            iLGwithSeq = 0
            for LGwithSeq in self.vLGwithSeq:
                iLGoriginal = LGwithSeq.LG.id  # should be equal to iLGwithSeq, 0-26
                print(LGwithSeq.LG.name)
                # iRow=iLGoriginal
                iRow = TableOfTxt.iRow_get(LGwithSeq.LG.name, 1)
                # "LG"+str(iLGwithSeq+1)
                LGwithSeq.name = TableOfTxt.rows[iRow].vCellText[
                    2
                ]  # iLGoriginal=0 => sLG=LG1 => "chr08"
                print(LGwithSeq.name)
                LGwithSeq.orientation = int(
                    TableOfTxt.rows[iRow].vCellText[3]
                )  # 1 or -1
                iLGwithSeq += 1

            # sort by names
            def MyFunc1(LGwithSeq):
                # chr01->1
                s = LGwithSeq.name[3:]
                if s[0] == "0":
                    s = s[1:]
                return int(s)

            self.vLGwithSeq.sort(key=MyFunc1)

            def MyFunc2(AssemblyElement):
                return -(
                    AssemblyElement.coorOnLG_min
                    + 0.000001 * AssemblyElement.coorOnLG_max
                )

            # sort by taking into account orientation
            for LGwithSeq in self.vLGwithSeq:
                if LGwithSeq.orientation < 0:
                    LGwithSeq.vAssemblyElement.sort(key=MyFunc2)
        if iChrNamingAndOrientationStrategy == 4:  # 20211006
            # names of chromosomes are already ok: chr01,...,chr26 (no chr20)
            for LGwithSeq in self.vLGwithSeq:
                LGwithSeq.name = LGwithSeq.LG.name

            # sort by names
            def MyFunc1(LGwithSeq):
                # chr01->1
                s = LGwithSeq.name[3:]
                if s[0] == "0":
                    s = s[1:]
                return int(s)

            self.vLGwithSeq.sort(key=MyFunc1)

    def printAssemblyByChrReport(self):
        sFileNameReport = (
            self.sPath + self.sAssemblyName + ".ChrReport.txt"
        )  # old: "assemblyZeevByChrReport.txt"
        f = open(sFileNameReport, "w")
        s = "iChr\tiLGoriginal\tmyOrientation\tchr-myLG\tchr\tlenPhys\tlenGenet\n"
        f.write(s)
        iLGwithSeq = 0
        totalLengthBp = 0
        totalLengthcM = 0
        for LGwithSeq in self.vLGwithSeq:
            iChr = iLGwithSeq + 1
            iLGoriginal = LGwithSeq.LG.id
            sChrName = LGwithSeq.name + "-" + LGwithSeq.LG.name + "\t" + LGwithSeq.name
            s = (
                str(iChr)
                + "\t"
                + str(iLGoriginal)
                + "\t"
                + str(LGwithSeq.orientation)
                + "\t"
                + sChrName
            )
            s += (
                "\t"
                + str(LGwithSeq.totalLengthBp)
                + "\t"
                + str(LGwithSeq.totalLengthcM)
                + "\n"
            )
            totalLengthBp += LGwithSeq.totalLengthBp
            totalLengthcM += LGwithSeq.totalLengthcM
            f.write(s)
            iLGwithSeq += 1
        # iCtg=0

        if False:
            lenPhys = 0
            nUnmapped = 0
            for ctg in self.SecCtgs.vCtg:
                if len(ctg.vPos) == 0:
                    nUnmapped += 1
                    lenPhys += ctg.seqLength
                # iCtg+=1
            s = "\t\t\tsumAtLeastOne\t" + str(self.sumAtLeastOne)
            f.write(s + "\n")
            s = "\t\t\tsumDoubleOrMore\t" + str(self.sumDoubleOrMore)
            f.write(s + "\n")
        # "iChr\tiLGoriginal\tmyOrientation\tchr-myLG\tchr\
        s = "\t\t\t\tsumByChr\t" + str(totalLengthBp) + "\t" + str(totalLengthcM)
        f.write(s + "\n")
        lenPhys = 0
        nUnmapped = 0
        for AssemblyElement in self.vAssemblyElement_noOrientation:
            lenPhys += AssemblyElement.lengthOnCtg()
            nUnmapped += 1
        for AssemblyElement in self.vAssemblyElement_Q:
            lenPhys += AssemblyElement.lengthOnCtg()
            nUnmapped += 1
        s = "\t\t\t\tunmapped\t" + str(lenPhys) + "\t" + str(nUnmapped) + "\n"
        f.write(s)
        f.close()

    def printAssemblyUnmapped(self):
        sFileNameFastaUnmapped = self.sPath + "assemblyZeevUnmapped.fasta"
        f = open(sFileNameFastaUnmapped, "w")
        for ctg in self.SecCtgs.vCtg:
            if len(ctg.vPos) == 0:
                ctg.printSeqToFile(f, "", 0, True)
        f.close()

    def printAssemblyByChr(self, bFullCtg=True):
        # bFullCtg - not in use
        print("printAssemblyByChr...")
        sFileNameFastaChr = (
            self.sPath + self.sAssemblyName + ".fasta"
        )  # old: "assemblyZeevByChr.fasta"
        sFileNameFastaChr_log = sFileNameFastaChr + ".log"

        sNNN = ""
        nNNNaddAtleast = self.nNNNaddAtleastSTANDARD
        for i in range(nNNNaddAtleast):
            sNNN += "N"

        # vsChrNoNeed=["chr20","chr27"]#Eyal: exclude from considereation
        vsChrNoNeed = []

        f = open(sFileNameFastaChr, "w")
        fCtg = open(sFileNameFastaChr_log, "w")
        iLGwithSeq = 0
        iRowStart = 0
        iRowEnd = 0

        # report shapka
        AssemblyElement = self.clAssemblyElement()
        s = (
            "iLG"
            + "\t"
            + "LGname"
            + "\t"
            + "iAE"
            + "\t"
            + "ctg"
            + "\t"
            + "nFromCtg"
            + "\t"
            + AssemblyElement.sShapka()
            + "\t"
            + "iRowStart"
            + "\t"
            + "iRowEnd"
        )
        fCtg.write(s + "\n")

        # seq of chromosomes -> fasta
        # AssemblyElement.posOfStartInChr
        # report
        for LGwithSeq in self.vLGwithSeq:
            iPosLast = 0
            if not (LGwithSeq.name in vsChrNoNeed):

                # chr name
                f.write(">" + LGwithSeq.name + chr(10))  # "\n"
                print(LGwithSeq.name)
                iRowStart += 1

                nAssemblyElement = len(LGwithSeq.vAssemblyElement)
                iAssemblyElement = 0
                for AssemblyElement in LGwithSeq.vAssemblyElement:
                    bTheLast = iAssemblyElement == nAssemblyElement - 1

                    # seq
                    # nNNNadded=AssemblyElement.printToFileFasta_v0(self.SecCtgs,f,bTheLast,nNNNaddAtleast)
                    sNNN_current = "" if bTheLast else sNNN
                    (
                        nNNNadded,
                        nFromCtg,
                        iRowEnd,
                        iPosLast,
                        bEndOfLineSymbolDone,
                    ) = AssemblyElement.printToFileFasta(
                        self.SecCtgs, f, sNNN_current, iRowStart, iPosLast
                    )

                    # for report
                    iCtgOriginal = AssemblyElement.iCtg
                    ctg = self.SecCtgs.vCtg[iCtgOriginal]
                    s = (
                        str(iLGwithSeq)
                        + "\t"
                        + LGwithSeq.name
                        + "\t"
                        + str(iAssemblyElement)
                        + "\t"
                        + ctg.name
                        + "\t"
                        + str(nFromCtg)
                        + "\t"
                        + AssemblyElement.s()
                        + "\t"
                        + str(iRowStart)
                        + "\t"
                        + str(iRowEnd)
                    )
                    fCtg.write(s + "\n")
                    print(ctg.name)

                    # for next ctg
                    iRowStart = iRowEnd
                    if bTheLast:
                        # end of seq
                        if not bEndOfLineSymbolDone:
                            f.write(chr(10))  # "\n"
                            iRowStart += 1
                    else:
                        AssemblyElementNext = LGwithSeq.vAssemblyElement[
                            iAssemblyElement + 1
                        ]
                        AssemblyElementNext.posOfStartInChr = (
                            AssemblyElement.posOfStartInChr
                            + AssemblyElement.lengthOnCtg()
                            + nNNNadded
                        )
                    iAssemblyElement += 1
                iLGwithSeq += 1

        # seq of nonMapped or nonOriented(if not allowed) -> fasta
        nbpUnmapped = 0
        # print len()
        iAssemblyElement = 0
        for AssemblyElement in self.vAssemblyElement_noOrientation:
            # seq name
            sName = (
                "noOrient_"
                + self.SecCtgs.vCtg[AssemblyElement.iCtg].name
                + "_"
                + str(self.SecCtgs.vCtg[AssemblyElement.iCtg].seqLength)
            )
            f.write(">" + sName + chr(10))  # "\n"
            print(sName)
            iRowStart += 1

            # seq
            (
                nNNNadded,
                nFromCtg,
                iRowEnd,
                iPosLast,
                bEndOfLineSymbolDone,
            ) = AssemblyElement.printToFileFasta(self.SecCtgs, f, "", iRowStart, 0)

            # for report
            iCtgOriginal = AssemblyElement.iCtg
            ctg = self.SecCtgs.vCtg[iCtgOriginal]
            s = (
                "-1"
                + "\t"
                + sName
                + "\t"
                + str(iAssemblyElement)
                + "\t"
                + ctg.name
                + "\t"
                + str(nFromCtg)
                + "\t"
                + AssemblyElement.s()
                + "\t"
                + str(iRowStart)
                + "\t"
                + str(iRowEnd)
            )
            fCtg.write(s + "\n")
            iRowStart = iRowEnd

            # end of seq
            if not bEndOfLineSymbolDone:
                f.write(chr(10))  # "\n"
                iRowStart += 1

            nbpUnmapped += nFromCtg
            iAssemblyElement += 1
        for AssemblyElement in self.vAssemblyElement_Q:
            # seq name
            sName = (
                "unMap_"
                + self.SecCtgs.vCtg[AssemblyElement.iCtg].name
                + "_"
                + str(self.SecCtgs.vCtg[AssemblyElement.iCtg].seqLength)
            )
            if (
                AssemblyElement.aStart != 0
                or AssemblyElement.aEnd
                != self.SecCtgs.vCtg[AssemblyElement.iCtg].seqLength
            ):
                sName += (
                    "_"
                    + str(-AssemblyElement.iLG)
                    + "___from"
                    + str(int(AssemblyElement.aStart))
                    + "_to"
                    + str(int(AssemblyElement.aEnd))
                    + "_len"
                    + str(int(AssemblyElement.lengthOnCtg()))
                )
            f.write(">" + sName + chr(10))  # "\n"
            print(sName)
            iRowStart += 1

            # seq
            (
                nNNNadded,
                nFromCtg,
                iRowEnd,
                iPosLast,
                bEndOfLineSymbolDone,
            ) = AssemblyElement.printToFileFasta(self.SecCtgs, f, "", iRowStart, 0)

            # for report
            iCtgOriginal = AssemblyElement.iCtg
            ctg = self.SecCtgs.vCtg[iCtgOriginal]
            s = (
                "-1"
                + "\t"
                + sName
                + "\t"
                + str(iAssemblyElement)
                + "\t"
                + ctg.name
                + "\t"
                + str(nFromCtg)
                + "\t"
                + AssemblyElement.s()
                + "\t"
                + str(iRowStart)
                + "\t"
                + str(iRowEnd)
            )
            fCtg.write(s + "\n")
            iRowStart = iRowEnd

            # end of seq
            if not bEndOfLineSymbolDone:
                f.write(chr(10))  # "\n"
                iRowStart += 1

            nbpUnmapped += nFromCtg
            iAssemblyElement += 1
        f.close()
        fCtg.write("nbpUnmapped=" + "\t" + str(nbpUnmapped) + "\n")
        fCtg.close()
        print("printAssemblyByChr...Done")

    def printAssemblyByCtgWithDobaffkaToName(self):
        sFileName = self.sPath + "assemblyZeevByCtgWithDobaffkaToName.fasta"
        f = open(sFileName, "w")
        for LGwithSeq in self.vLGwithSeq:
            for AssemblyElement in LGwithSeq.vAssemblyElement:
                # +"_LG_"+str(iLG+1)
                sDobaffka = (
                    "___copy_"
                    + str(AssemblyElement.iPos + 1)
                    + "_"
                    + LGwithSeq.name
                    + "_coor_"
                    + str(AssemblyElement.coorOnLG)
                )
                iCtg = AssemblyElement.iCtg
                ctg = self.SecCtgs.vCtg[iCtg]
                ctg.printSeqToFile(f, sDobaffka, 0, True)
        f.close()

    def printMarkers(self):
        sFileNameReportOnMarkers = self.sPath + "assemblyZeevByMarkerReport.txt"
        sFileNameReportOnMarkersOldNames = (
            self.sPath + "assemblyZeevByMarkerReportOldNames.txt"
        )
        f5 = open(sFileNameReportOnMarkers, "w")
        f6 = open(sFileNameReportOnMarkersOldNames, "w")

        # shapka
        s = "marker\tbGood\tiLG\tchr\tcoorGenet\tstartCtgOnChr\tindexOnPath"
        f5.write("im\t" + s + "\n")
        f6.write("nameBesan\t" + s + "\tcoorOnCtg\tcoorOnChr\n")

        def addMarker(
            f5, f6, im, vLGmarker, bGood, iLG, coor, sChrName, posOfStartInChr
        ):
            for LGmarker in vLGmarker:
                if LGmarker.LGid == iLG and abs(LGmarker.coorOnLG - coor) <= 3:
                    im += 1
                    s = (
                        LGmarker.m.sMarker
                        + "\t"
                        + str(bGood)
                        + "\t"
                        + str(iLG)
                        + "\t"
                        + sChrName
                        + "\t"
                        + str(LGmarker.coorOnLG)
                        + "\t"
                        + str(posOfStartInChr)
                        + "\t"
                        + str(LGmarker.indexOnPath)
                    )
                    f5.write(str(im) + "\t" + s + "\n")

                    # old names
                    #
                    # self.PrivmanCtgIndex=-1
                    # self.vPrivmanvPosOnCtg=[]
                    # N631P17133
                    for x in LGmarker.m.vPrivmanvPosOnCtg:
                        sMarkerNameBesan = (
                            "N" + str(LGmarker.m.PrivmanCtgIndex) + "P" + str(x)
                        )
                        f6.write(
                            sMarkerNameBesan
                            + "\t"
                            + s
                            + "\t"
                            + str(x)
                            + "\t"
                            + str(x + posOfStartInChr)
                            + "\n"
                        )
            return im

        im = 0
        for LGwithSeq in self.vLGwithSeq:  # on all linkage groups
            iLG = LGwithSeq.LG.id
            sChrName = LGwithSeq.name
            for (
                AssemblyElement
            ) in LGwithSeq.vAssemblyElement:  # on all contigs in sequence assembly
                iCtg = AssemblyElement.iCtg
                ctg = self.SecCtgs.vCtg[iCtg]
                vLGmarker = []
                vLGmarkerGood = ctg.vLGmarker
                vLGmarkerBad = ctg.vLGmarkerBad
                coor = AssemblyElement.coorOnLG  # genetic coor on linkage group
                posOfStartInChr = (
                    AssemblyElement.posOfStartInChr
                )  # physical coor on chr
                im = addMarker(
                    f5,
                    f6,
                    im,
                    vLGmarkerGood,
                    True,
                    iLG,
                    coor,
                    sChrName,
                    posOfStartInChr,
                )
                im = addMarker(
                    f5,
                    f6,
                    im,
                    vLGmarkerBad,
                    False,
                    iLG,
                    coor,
                    sChrName,
                    posOfStartInChr,
                )
        f5.close()
        f6.close()

    def printMappingReport(self):
        sFileNameFastaMappingReport = self.sPath + "MappingReport.txt"
        f = open(sFileNameFastaMappingReport, "w")

        s = "i\tctg\tlen\tcopy\tnCopies"
        s += "\tiLG\tchr\tcoor"
        s += "\tposOfStartInChr\tbyGood\tbyBad"
        s += "\tindexBlastClusters\tindexBlastStars"
        s += "\trefMapped\trefUnmapped"
        s += "\tsPosAll"
        f.write(s + "\n")
        iq = 0
        for LGwithSeq in self.vLGwithSeq:
            iLG = LGwithSeq.LG.id
            sChrName = LGwithSeq.name
            for AssemblyElement in LGwithSeq.vAssemblyElement:
                iq += 1
                iCtg = AssemblyElement.iCtg
                ctg = self.SecCtgs.vCtg[iCtg]
                nPos = len(ctg.vPos)
                iPos = AssemblyElement.iPos
                coor = AssemblyElement.coorOnLG
                posOfStartInChr = AssemblyElement.posOfStartInChr
                s = (
                    str(iq)
                    + "\t"
                    + ctg.name
                    + "\t"
                    + str(ctg.seqLength)
                    + "\t"
                    + str(iPos + 1)
                    + "\t"
                    + str(nPos)
                )
                s += "\t" + str(iLG) + "\t" + sChrName + "\t" + str(coor)
                s += (
                    "\t"
                    + str(posOfStartInChr)
                    + "\t"
                    + str(ctg.basedOnGoodMarkersOnly)
                    + "\t"
                    + str(ctg.basedOnBadMarkersOnly)
                )
                s += (
                    "\t"
                    + str(ctg.iBasedOnClusterOfBlastRes)
                    + "\t"
                    + str(ctg.idOfFastaFileInUseToMapContigsWithoutMarkers)
                )
                s += (
                    "\t"
                    + ctg.s_vSyntheny(ctg.vPosOnRefGenomeMapped)
                    + "\t"
                    + ctg.s_vSyntheny(ctg.vPosOnRefGenomeNonMapped)
                )
                s += "\t" + ctg.sPosAll()
                f.write(s + "\n")
        # print "sum="+str(self.sumAtLeastOne)+", sumDoubleOrMore="+str(self.sumDoubleOrMore)
        f.close()

    def print_mapped_gff(
        self, iLGtoSelect, coorStart, coorEnd, sDobaffka, bSelect, bFirst
    ):
        sFileName = (
            self.sPath + "Mapped.gff" if not bSelect else self.sPath + "SelectedChr.gff"
        )
        f = open(sFileName, "w") if bFirst else open(sFileName, "a")

        # shapka
        sPrint = ""
        if len(sDobaffka) > 0:
            sPrint = sDobaffka + "\t"
        s = sPrint + "i\tctg\tlen\tcopy\tnCopies"
        s += "\tiLG\tchr\tcoor"
        s += "\tposOfStartInChr"
        f.write(s + "\n")

        iq = 0
        for LGwithSeq in self.vLGwithSeq:
            iLG = LGwithSeq.LG.id
            if iLGtoSelect == -1 or iLG == iLGtoSelect:
                sChrName = LGwithSeq.name
                for AssemblyElement in LGwithSeq.vAssemblyElement:
                    iq += 1
                    iCtg = AssemblyElement.iCtg
                    ctg = self.SecCtgs.vCtg[iCtg]
                    nPos = len(ctg.vPos)
                    iPos = AssemblyElement.iPos
                    coor = AssemblyElement.coorOnLG
                    if iLGtoSelect == -1 or ((coor >= coorStart) and (coor <= coorEnd)):
                        posOfStartInChr = AssemblyElement.posOfStartInChr
                        s = (
                            str(iq)
                            + "\t"
                            + ctg.name
                            + "\t"
                            + str(ctg.seqLength)
                            + "\t"
                            + str(iPos + 1)
                            + "\t"
                            + str(nPos)
                        )
                        s += "\t" + str(iLG) + "\t" + sChrName + "\t" + str(coor)
                        s += "\t" + str(posOfStartInChr) + "\t"
                        # print "5023: nLineOf_gff="+str(len(ctg.vLineOf_gff))
                        for LineOf_gff in ctg.vLineOf_gff:
                            s1 = LineOf_gff.sBasedOnNewAssembly(
                                sChrName, posOfStartInChr
                            )
                            sPrint = ""
                            if len(sDobaffka) > 0:
                                sPrint = sDobaffka + "\t"
                            sPrint += s + "\t" + s1
                            f.write(sPrint + "\n")
        # print "sum="+str(self.sumAtLeastOne)+", sumDoubleOrMore="+str(self.sumDoubleOrMore)
        f.close()

    def printReportOnAllCtgs(self):
        sFileName = self.sPath + "ReportOnAllCtgs.txt"
        f = open(sFileName, "w")

        s = "i\tctg\tlen\tnCopies"
        s += "\tbyGood\tbyBad"
        s += "\tindexBlastClusters\tindexBlastStars"
        s += "\trefMapped\trefUnmapped"
        f.write(s + "\n")

        iq = 0
        for ctg in self.SecCtgs.vCtg:
            nPos = len(ctg.vPos)
            s = str(iq) + "\t" + ctg.name + "\t" + str(ctg.seqLength) + "\t" + str(nPos)
            s += (
                "\t"
                + str(ctg.basedOnGoodMarkersOnly)
                + "\t"
                + str(ctg.basedOnBadMarkersOnly)
            )
            s += (
                "\t"
                + str(ctg.iBasedOnClusterOfBlastRes)
                + "\t"
                + str(ctg.idOfFastaFileInUseToMapContigsWithoutMarkers)
            )
            s += (
                "\t"
                + ctg.s_vSyntheny(ctg.vPosOnRefGenomeMapped)
                + "\t"
                + ctg.s_vSyntheny(ctg.vPosOnRefGenomeNonMapped)
            )
            f.write(s + "\n")
            iq += 1
        f.close()


class clPilonResults:
    def __init__(self):
        self.vCtg = []

    class clPilonCtg:
        def __init__(self):
            self.name = ""
            self.len = 0
            self.nReads = -1
            self.confLen = 0
            self.coverage = 0
            self.minCoverageDepth = 5
            self.nSNP = 0
            self.nAmbig = 0
            self.nIns = 0
            self.nIns_bp = 0
            self.nDel = 0
            self.nDel_bp = 0
            self.bpCorrected = 0
            self.vLCR = []  # Large collapsed regions
            self.vBreakNoSol = []  # breaks
            self.vBreakNoSolLong101 = []  # breaks
            self.vBreakFixed = []  # breaks

        class clInterval:
            def __init__(self, start, end):
                self.start = start
                self.end = end

    def statIntervals(self, vInterval):  # n,lenSum,N50,L50,lenMax
        vv = []
        for interval in vInterval:
            vv.append(abs(interval.end - interval.start) + 1)
        VovaMath = clVovaMath()
        if len(vv) == 0:
            return 0, 0, 0, 0, 0
        if len(vv) == 1:
            return 1, vv[0], vv[0], 1, vv[0]
        nn, ll = VovaMath.NandL(vv, False, 50)
        return len(vv), sum(vv), nn, ll, max(vv)

    def statIntervals_sShapka(self, sInt):
        # n,lenSum,N50,L50,lenMax
        s = (
            "\t"
            + sInt
            + "_n"
            + "\t"
            + sInt
            + "_sum"
            + "\t"
            + sInt
            + "_N50"
            + "\t"
            + sInt
            + "_L50"
            + "\t"
            + sInt
            + "_max"
        )
        return s

    def statIntervals_s(self, vInterval):
        # n,lenSum,N50,L50,lenMax
        n, lenSum, N50, L50, lenMax = self.statIntervals(vInterval)
        s = (
            "\t"
            + str(n)
            + "\t"
            + str(lenSum)
            + "\t"
            + str(N50)
            + "\t"
            + str(L50)
            + "\t"
            + str(lenMax)
        )
        return s

    def readFromFile(self, sFileName="", sFileNameFasta=""):
        if sFileName == "":
            # sFileName="C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\300.slurm-11600305.out"
            # sFileName="C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\300-500_till_tig00002001_slurm-11600762.out"
            sFileName = "C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\300-500.slurm-11606062.out"

        SecCtgs = clSecCtgs()
        # sFileNameFasta=""
        sFileNameFasta = "C:\\Frenkel\\Privman\\PacBio202008\\canu\\asm.contigs.fasta"  # >tig00000002
        # sFileNameFasta="C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\300-500.pilon.fasta"#>tig00000002_pilon
        if len(sFileNameFasta) > 0:
            SecCtgs.readFromFastaFile(sFileNameFasta, 2)

        f = open(sFileName, "r")
        bStarted = False
        ctg = self.clPilonCtg()
        ctgSum = self.clPilonCtg()
        for s in f:
            if len(s) > 10:
                if s[0:10] == "Processing":
                    # Processing tig00000002:1-10662
                    ss = s.split("\n")
                    ss = ss[0].split(" ")
                    ss = ss[1].split(":")
                    sName = ss[0]
                    ss = ss[1].split("-")
                    seqLen = int(ss[1])
                    if bStarted:
                        self.vCtg.append(ctg)
                        ctg = self.clPilonCtg()
                    bStarted = True
                    ctg.name = sName
                    ctg.len = seqLen
                else:
                    if bStarted:
                        if s[0:11] == "Total Reads":
                            # Total Reads: 5950, Coverage: 56, minDepth: 3
                            ss = s.split("\n")
                            ss = ss[0].split(" ")
                            sR = ss[2]  # 5950,
                            sR = sR[0 : len(sR) - 1]  # 5950
                            ctg.nReads = int(sR)
                            sR = ss[4]  # 56,
                            sR = sR[0 : len(sR) - 1]  # 56
                            ctg.coverage = int(sR)
                            ctg.minCoverageDepth = int(ss[6])
                        if s[0:9] == "Confirmed":
                            # Confirmed 10064 of 10662 bases (94.39%)
                            ss = s.split(" ")
                            ctg.confLen = int(ss[1])  # 10064
                        if s[0:9] == "Corrected":
                            # Corrected 16 snps; 2 ambiguous bases; corrected 2 small insertions totaling 3 bases, 6 small deletions totaling 16 bases
                            ss = s.split(" ")
                            ctg.nSNP = int(ss[1])  # 16
                            ctg.nAmbig = int(ss[3])  # 2
                            ctg.nIns = int(ss[7])  # 2
                            ctg.nIns_bp = int(ss[11])  # 3
                            ctg.nDel = int(ss[13])  # 6
                            ctg.nDel_bp = int(ss[17])  # 16
                            ctg.bpCorrected = ctg.nSNP + ctg.nIns_bp + ctg.nDel_bp
                        if s[0:5] == "Large":
                            # Large collapsed region: tig00000033:440-10666 size 10227
                            ss = s.split(":")
                            ss = ss[2].split(" ")
                            ss = ss[0].split("-")
                            # print s
                            posStart = int(ss[0])
                            posEnd = int(ss[1])
                            ctg.vLCR.append(ctg.clInterval(posStart, posEnd))
                        if s[0:3] == "fix":
                            ## Attempting to fix local continuity breaks
                            # fix break: tig00000033:1875-1898 1840 -88 +95 BreakFix
                            # print s
                            ss = s.split(":")
                            ss = ss[2].split(" ")
                            ss = ss[0].split("-")
                            if len(ss) > 1:
                                posStart = int(ss[0])
                                posEnd = int(ss[1])
                                ctg.vBreakFixed.append(ctg.clInterval(posStart, posEnd))
                        if s[0:5] == "# fix":
                            ## fix break: tig00000033:24295-24368 0 -0 +0 NoSolution TandemRepeat 240
                            ## fix break: tig00000033:38352 0 -0 +0 NoSolution
                            ss = s.split(":")
                            ss = ss[2].split(" ")
                            ss = ss[0].split("-")
                            if len(ss) > 1:
                                posStart = int(ss[0])
                                posEnd = int(ss[1])
                                ctg.vBreakNoSol.append(ctg.clInterval(posStart, posEnd))
                                if posEnd - posStart + 1 > 300:
                                    ctg.vBreakNoSolLong101.append(
                                        ctg.clInterval(posStart + 51, posEnd - 51)
                                    )
        if ctg.nReads >= 0:
            self.vCtg.append(ctg)
        f.close()
        f = open(sFileName + ".statVova.txt", "w")

        def sShapka(SecCtgs):
            s = "iCtg" + "\t" + "ctg" + "\t" + "len"
            s += "\t" + "nReads"
            s += "\t" + "coverage"
            s += "\t" + "minCoverageDepth"
            s += "\t" + "confLen"
            s += "\t" + "NonconfLen"
            s += "\t" + "procNonconfLen"

            s += "\t" + "nSNP"
            s += "\t" + "nAmbig"
            s += "\t" + "nIns"
            s += "\t" + "nIns_bp"
            s += "\t" + "nDel"
            s += "\t" + "nDel_bp"
            s += "\t" + "bpCorrected"
            # n,lenSum,N50,L50
            s += self.statIntervals_sShapka("NF101")
            s += self.statIntervals_sShapka("vLCR")
            s += self.statIntervals_sShapka("NF")
            s += self.statIntervals_sShapka("Fix")

            if len(SecCtgs.vCtgName) > 0:
                # iCtg=SecCtgs.vCtgName.index(ctg.name)
                Seq = clSeq()
                # Seq.seq=SecCtgs.vCtg[iCtg].sSeq_get()
                # Seq.nLetters_get()
                s += Seq.s_nLetters_Shapka()
                s += Seq.s_periodicity_Shapka()
                s += Seq.s_Plet_Shapka()
            return s

        def sCtg(ctg, s, SecCtgs):
            s += "\t" + ctg.name + "\t" + str(ctg.len)
            s += "\t" + str(ctg.nReads)
            s += "\t" + str(ctg.coverage)
            s += "\t" + str(ctg.minCoverageDepth)
            s += "\t" + str(ctg.confLen)
            s += "\t" + str(ctg.len - ctg.confLen)
            s += "\t" + str(float(ctg.len - ctg.confLen) / ctg.len * 100)

            s += "\t" + str(ctg.nSNP)
            s += "\t" + str(ctg.nAmbig)
            s += "\t" + str(ctg.nIns)
            s += "\t" + str(ctg.nIns_bp)
            s += "\t" + str(ctg.nDel)
            s += "\t" + str(ctg.nDel_bp)
            s += "\t" + str(ctg.bpCorrected)
            # s+="\t"+str()
            s += self.statIntervals_s(ctg.vBreakNoSolLong101)
            s += self.statIntervals_s(ctg.vLCR)
            s += self.statIntervals_s(ctg.vBreakNoSol)
            s += self.statIntervals_s(ctg.vBreakFixed)

            if ctg.name in SecCtgs.vCtgName:
                iCtg = SecCtgs.vCtgName.index(ctg.name)
                Seq = clSeq()
                Seq.seq = SecCtgs.vCtg[iCtg].sSeq_get()
                Seq.nLetters_get()
                s += Seq.s_nLetters()  # _Shapka(s_nLetters_Shapka(
                s += Seq.s_periodicity()
                s += Seq.s_Plet()
            return s

        # s+="\t"+""
        # s+="\t"+""
        s = sShapka(SecCtgs)
        f.write(s + "\n")
        iCtg = 0
        lenTotal = 0
        for ctg in self.vCtg:
            iCtg += 1
            s = sCtg(ctg, str(iCtg), SecCtgs)
            ctgSum.len += ctg.len
            print("iCtg=" + str(iCtg) + ", len=" + str(ctg.len) + "...")
            ctgSum.nReads += ctg.nReads
            ctgSum.coverage += ctg.coverage * ctg.nReads
            ctgSum.minCoverageDepth += ctg.minCoverageDepth * ctg.nReads
            ctgSum.confLen += ctg.confLen

            ctgSum.nSNP += ctg.nSNP
            ctgSum.nAmbig += ctg.nAmbig
            ctgSum.nIns += ctg.nIns
            ctgSum.nIns_bp += ctg.nIns_bp
            ctgSum.nDel += ctg.nDel
            ctgSum.nDel_bp += ctg.nDel_bp
            ctgSum.bpCorrected += ctg.bpCorrected
            # ctgSum.+=ctg.

            f.write(s + "\n")
            lenTotal += ctg.len
        ctgSum.coverage = float(ctgSum.coverage) / ctgSum.len
        ctgSum.minCoverageDepth = float(ctgSum.minCoverageDepth) / ctgSum.len
        s = sCtg(ctgSum, "Total", SecCtgs)
        f.write(s + "\n")

        s = "confLen/len" + "\t" + str(float(ctgSum.confLen) / ctgSum.len * 100)
        f.write(s + "\n")
        s = "SNPs/kbp" + "\t" + str(float(ctgSum.nSNP) / ctgSum.len * 1000)
        f.write(s + "\n")
        s = "bp/SNP" + "\t" + str(float(ctgSum.len) / ctgSum.nSNP)
        f.write(s + "\n")
        s = "ambig/10Mbp" + "\t" + str(float(ctgSum.nAmbig) / ctgSum.len * 10000000)
        f.write(s + "\n")
        s = "nIns/10Mbp" + "\t" + str(float(ctgSum.nIns) / ctgSum.len * 10000000)
        f.write(s + "\n")
        s = "nIns_bp/10Mbp" + "\t" + str(float(ctgSum.nIns_bp) / ctgSum.len * 10000000)
        f.write(s + "\n")
        s = "nDel/10Mbp" + "\t" + str(float(ctgSum.nDel) / ctgSum.len * 10000000)
        f.write(s + "\n")
        s = "nDel_bp/10Mbp" + "\t" + str(float(ctgSum.nDel_bp) / ctgSum.len * 10000000)
        f.write(s + "\n")
        s = (
            "bpCorrected/10Mbp"
            + "\t"
            + str(float(ctgSum.bpCorrected) / ctgSum.len * 10000000)
        )
        f.write(s + "\n")
        # s="nCtg"+"\t"+str(len(self.vCtg))
        # f.write(s+"\n")
        # s="lenTotal"+"\t"+str(lenTotal)
        # f.write(s+"\n")
        f.close()


class clReferenceGenome:
    def __init__(
        self, sOriginalData_set="", sData_set=""
    ):  # originalDataIndex_set=0,dataIndex_set=0)
        self.vChromosome = []  # array of self.clChromosome()
        self.vSeqCtgName = (
            []
        )  # array of string to simplify search chromosome by the name of sequence contig

        self.originalDataIndex = -1  # originalDataIndex_set#0=Cnig_gn1,1=Cnig_gn2
        self.originalDataName = ""
        self.originalDataFasta = clSecCtgs()

        self.dataIndex = -1  # dataIndex_set#0=Formica,1#=Cnig_gn1
        self.name = ""
        self.dataFasta = clSecCtgs()  # ReferenceGenome

        self.sFileNameBlastResMeDB = ""  # original data Q
        # self.sFileNameBlastResMeQ=""#original data DB
        self.sFolderOutput = ""

        self.ReferenceGenome_start(sOriginalData_set, sData_set)

    class clChromosome:
        def __init__(self):
            self.sNameChr = ""
            self.sNameSeq = ""
            self.lenMbp = 0
            self.GCproc = 0
            self.vBlockOfSyntheny = []

        class clBlockOfSyntheny:  # iLG,coor=
            def __init__(self):
                coorStart = 0
                coorEnd = 0
                iLG = -1
                coorOnLGstart = 0
                coorOnLGend = 0

            def posOnGeneticMapBasedOnRefGenome(self, coorOnRef):
                mmm = clVovaMath()
                coor = mmm.yByLin(
                    self.coorStart,
                    self.coorOnLGstart,
                    self.coorEnd,
                    self.coorOnLGend,
                    coorOnRef,
                )
                return self.iLG, coor

            def s_get(self):
                s = ""
                s += "\t" + str(self.coorStart)
                s += "\t" + str(self.coorEnd)
                s += "\t" + str(self.iLG)
                s += "\t" + str(self.coorOnLGstart)
                s += "\t" + str(self.coorOnLGend)
                return s

            def sShapka_get(self):
                s = ""
                s += "\tcoorStart"
                s += "\tcoorEnd"
                s += "\tiLG"
                s += "\tcoorOnLGstart"
                s += "\tcoorOnLGend"
                return s

    def Chromosome_get(self, sNameChr, sNameSeq, lenMbp, GCproc):
        Chromosome = self.clChromosome()
        Chromosome.sNameChr = sNameChr
        Chromosome.sNameSeq = sNameSeq
        Chromosome.lenMbp = lenMbp
        Chromosome.GCproc = GCproc
        return Chromosome

    def ReferenceGenome_start(self, sOriginalData_set, sData_set):
        # specific for my Lab
        PrivmanLab = clPrivmanLab()
        # myData=PrivmanLab.MyData
        # iFasta=myData.iFastaByName(sName)
        # "Cnig_gn1","Formica"

        vChromosome = []
        if (
            sOriginalData_set == "" or sOriginalData_set == "Cnig_gn1"
        ):  #   in genetic mapping
            self.originalDataIndex = 0
            self.originalDataName = "Cnig_gn1"
            self.sFolderOutput = "C:\\Frenkel\\Privman\\Cnig_gn1\\"
            self.originalDataFasta = PrivmanLab.SecCtgsByName(
                self.originalDataName, True
            )
        if sOriginalData_set == "Cnig_gn2":  # Cnig_gn2   in GWAS
            self.originalDataIndex = 1
            self.originalDataName = "Cnig_gn2"
            self.sFolderOutput = "C:\\Frenkel\\Privman\\Cnig_gn2\\"
            self.originalDataFasta = PrivmanLab.SecCtgsByName(
                self.originalDataName, True
            )
        if sOriginalData_set == "asm":  # asm assembly of PacBio
            self.originalDataIndex = 2
            self.originalDataName = "asm"
            # self.sFolderOutput="C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\"
            self.sFolderOutput = "C:\\Frenkel\\Privman\\Privman\\PacBio202008\\canu\\"
            self.originalDataFasta = PrivmanLab.SecCtgsByName(
                self.originalDataName, True
            )
        print(
            "ReferenceGenome_start: sOriginalData_set="
            + sOriginalData_set
            + ", originalDataFasta="
            + self.originalDataFasta.fasta
        )
        # print PrivmanLab.MyData.vsFasta_name
        # print "iFasta="+str(PrivmanLab.MyData.iFastaByName(sOriginalData_set))

        if sData_set == "" or sData_set == "Formica":  # Formica
            self.dataIndex = 0
            self.name = "Formica"
            self.dataFasta = PrivmanLab.SecCtgsByName(self.name, True)
            if self.originalDataName == "Cnig_gn1":
                self.sFileNameBlastResMeDB = "C:\\Frenkel\\Privman\\Cnig_gn1\\res_Cnig_gn1_vs_FormicaSelysi_e70.out"  # Formica=DB, Cnig_gn1=Q
            if self.originalDataName == "asm":
                self.sFileNameBlastResMeDB = "C:\\Frenkel\\Privman\\PacBio202008\\canu\\res_asm.contigs_vs_Formica_e70.out"  # Formica=DB, asm=Q
            # self.sFileNameBlastResMeQ=""
            self.sFolderOutput = "C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\"

            # based on https://www.ncbi.nlm.nih.gov/genome/36601
            # sNameChr,sNameSeq,lenMbp,GCproc
            vChromosome.append(self.Chromosome_get("Chr1", "CM020805.1", 15.35, 36.7))
            vChromosome.append(self.Chromosome_get("Chr2", "CM020806.1", 11.94, 36))
            vChromosome.append(self.Chromosome_get("Chr3", "CM020807.1", 14.14, 36))
            vChromosome.append(self.Chromosome_get("Chr4", "CM020808.1", 12.77, 34.4))
            vChromosome.append(self.Chromosome_get("Chr5", "CM020809.1", 11.09, 35.1))
            vChromosome.append(self.Chromosome_get("Chr6", "CM020810.1", 9.14, 35.3))
            vChromosome.append(self.Chromosome_get("Chr7", "CM020811.1", 8.4, 36.9))
            vChromosome.append(self.Chromosome_get("Chr8", "CM020812.1", 7.76, 35.5))
            vChromosome.append(self.Chromosome_get("Chr9", "CM020813.1", 9.49, 36.8))
            vChromosome.append(self.Chromosome_get("Chr10", "CM020814.1", 12.78, 36.4))
            vChromosome.append(self.Chromosome_get("Chr11", "CM020815.1", 7.94, 35))
            vChromosome.append(self.Chromosome_get("Chr12", "CM020816.1", 8.82, 35.6))
            vChromosome.append(self.Chromosome_get("Chr13", "CM020817.1", 10.07, 35))
            vChromosome.append(self.Chromosome_get("Chr14", "CM020818.1", 7.73, 35.6))
            vChromosome.append(self.Chromosome_get("Chr15", "CM020819.1", 9.02, 36.3))
            vChromosome.append(self.Chromosome_get("Chr16", "CM020820.1", 7.43, 35.8))
            vChromosome.append(self.Chromosome_get("Chr17", "CM020821.1", 7.92, 35.9))
            vChromosome.append(self.Chromosome_get("Chr18", "CM020822.1", 7.06, 35.1))
            vChromosome.append(self.Chromosome_get("Chr19", "CM020823.1", 5.14, 35.3))
            vChromosome.append(self.Chromosome_get("Chr20", "CM020824.1", 5.75, 36.5))
            vChromosome.append(self.Chromosome_get("Chr21", "CM020825.1", 7.29, 35.6))
            vChromosome.append(self.Chromosome_get("Chr22", "CM020826.1", 5.98, 34.8))
            vChromosome.append(self.Chromosome_get("Chr23", "CM020827.1", 4.59, 37.3))
            vChromosome.append(self.Chromosome_get("Chr24", "CM020828.1", 5.46, 33.5))
            vChromosome.append(self.Chromosome_get("Chr25", "CM020829.1", 6.24, 36))
            vChromosome.append(self.Chromosome_get("Chr26", "CM020830.1", 3.58, 36.4))
            vChromosome.append(self.Chromosome_get("Chr27", "CM020831.1", 4.15, 35.7))
            vChromosome.append(self.Chromosome_get("MT", "CM020864.1", 0.02, 16.7))
            vChromosome.append(self.Chromosome_get("Un", "Unmapped", 63.42, 38.1))
        if sData_set == "Cnig_gn1":
            self.dataIndex = 1
            self.name = "Cnig_gn1"
            if self.originalDataName == "Cnig_gn2":
                # not in use
                # self.sFileNameBlastResMeQ="C:\\Frenkel\\Privman\\Cnig_gn2\\res_Cnig_gn1_vs_Cnig_gn2_e149.out"#Cnig_gn2 = DB, Cnig_gn1=Q
                self.sFileNameBlastResMeDB = "C:\\Frenkel\\Privman\\Cnig_gn2\\res_Cnig_gn2_vs_Cnig_gn1_e150p.out.std"  # Cnig_gn2 = Q, Cnig_gn1=DB
            # vChromosome - ne gotovo
        if sData_set == "asm":
            self.dataIndex = 2
            self.name = "asm"
            if self.originalDataName == "Cnig_gn1":
                self.sFileNameBlastResMeDB = "C:\\Frenkel\\Privman\\PacBio202008\\canu\\res_Cnig_ng1_vs_asm.contigs_e150.out"  # Cnig_gn1 = Q, asm=DB
            if self.originalDataIndex == 1:  # Cnig_gn2
                self.sFileNameBlastResMeDB = "C:\\Frenkel\\Privman\\Cnig_gn2\\res_Cnig_gn2_vs_asm_e150.out"  # Cnig_gn2 = Q, asm=DB
            # vChromosome - ne gotovo
        if sData_set == "Cnig_gn3a.contigs":  # "300-500.pilon":
            self.dataIndex = 3
            self.name = "Cnig_gn3a.contigs"
            if self.originalDataName == "Cnig_gn1":
                self.sFileNameBlastResMeDB = "C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\res_Cnig_ng1_vs_300-500.pilon_e150.out"  # Cnig_gn1 = Q, 300-500.pilon=DB
        if sData_set == "Cnig_gn3.contigs":
            self.dataIndex = 4
            self.name = "Cnig_gn3.contigs"
            if self.originalDataName == "Cnig_gn1":
                self.sFileNameBlastResMeDB = "C:\\Frenkel\\Privman\\Cnig_gn3\\res_Cnig_ng1_vs_selected3.300-500pilon_e150.out"  # Cnig_gn1 = Q, selected3.300-500pilon=DB

        # if sData_set=="<newAssembly>":
        # 	self.dataIndex=???
        # 	self.name="<newAssembly>"
        # 	if self.originalDataName=="Cnig_gn1":
        # 		self.sFileNameBlastResMeDB="<blastResFile>"#Cnig_gn1 = Q, <newAssembly>=DB

        self.vChromosome = vChromosome

        self.vSeqCtgName = []
        for Chromosome in vChromosome:
            self.vSeqCtgName.append(Chromosome.sNameSeq)

        self.attachMarkersToAnotherAssembly_simple___sFileOut = (
            self.sFolderOutput
            + "markers_"
            + self.originalDataName
            + "_on_"
            + self.name
            + ".txt"
        )  # my markers on reference genome(all markers, not only good and bad)
        self.attachMarkersToAnotherAssembly_simple___sFileOut1 = (
            self.sFolderOutput
            + "markers_"
            + self.originalDataName
            + "_on_"
            + self.name
            + "_nCopies.txt"
        )

    def iChromosome_get(self, sNameSeq):
        if not (sNameSeq in self.vSeqCtgName):
            n = len(self.vSeqCtgName)
            self.vSeqCtgName.append(sNameSeq)
            self.vChromosome.append(
                self.Chromosome_get("Un" + str(n), sNameSeq, -1, -1)
            )
            return n
        return self.vSeqCtgName.index(sNameSeq)

    def notInUse___readFromFile(self):
        pass

    def notInUse___posOnFormicaMinMax(self, idLG, coor):
        pass

    def posOnGeneticMapBasedOnRefGenome(self, sNameSeq, coorOnRef):  # iLG,coor=
        iCtgRef = self.iChromosome_get(sNameSeq)
        vBlockOfSyntheny = self.vChromosome[iCtgRef].vBlockOfSyntheny
        for BlockOfSyntheny in vBlockOfSyntheny:
            if (
                coorOnRef >= BlockOfSyntheny.coorStart
                and coorOnRef <= BlockOfSyntheny.coorEnd
            ):
                return BlockOfSyntheny.posOnGeneticMapBasedOnRefGenome(coorOnRef)
        return -1, 0  # not found

    def addBlock(self, sNameSeq, coorStart, coorEnd, iLG, coorOnLGstart, coorOnLGend):
        iCtgRef = self.iChromosome_get(sNameSeq)
        BlockOfSyntheny = self.vChromosome[iCtgRef].clBlockOfSyntheny()
        BlockOfSyntheny.coorStart = coorStart
        BlockOfSyntheny.coorEnd = coorEnd
        BlockOfSyntheny.iLG = iLG
        BlockOfSyntheny.coorOnLGstart = coorOnLGstart
        BlockOfSyntheny.coorOnLGend = coorOnLGend
        self.vChromosome[iCtgRef].vBlockOfSyntheny.append(BlockOfSyntheny)
        print(
            str(iCtgRef)
            + " "
            + sNameSeq
            + " "
            + str(len(self.vChromosome[iCtgRef].vBlockOfSyntheny))
        )

    def printToFile_Chromosome_vBlockOfSyntheny(self):
        sFileName = "ReferenceGenome_" + self.name + ".txt"
        f = open(sFileName, "w")

        s = "Chr" + "\t" + "NameSeq" + "\t" + "lenMbp" + "\t" + "nBlocks"
        s += (
            "\t"
            + "iBlock"
            + "\t"
            + "length"
            + "\t"
            + "procOfChrLen"
            + "\t"
            + "procOfChrLenComul"
        )
        s += self.vChromosome[0].vBlockOfSyntheny[0].sShapka_get()
        f.write(s + "\n")

        for Chromosome in self.vChromosome:
            lenChr = Chromosome.lenMbp * 1000000
            iBlock = 0
            nn = 0
            for BlockOfSyntheny in Chromosome.vBlockOfSyntheny:
                s1 = BlockOfSyntheny.s_get()
                lengthBpOfBlock = (
                    abs(BlockOfSyntheny.coorEnd - BlockOfSyntheny.coorStart) + 1
                )
                nn += lengthBpOfBlock

                s = (
                    Chromosome.sNameChr
                    + "\t"
                    + Chromosome.sNameSeq
                    + "\t"
                    + str(Chromosome.lenMbp)
                    + "\t"
                    + str(len(Chromosome.vBlockOfSyntheny))
                )
                s += (
                    "\t"
                    + str(iBlock + 1)
                    + "\t"
                    + str(lengthBpOfBlock)
                    + "\t"
                    + str(float(lengthBpOfBlock) / lenChr * 100)
                    + "%"
                    + "\t"
                    + str(float(nn) / lenChr * 100)
                    + "%"
                )
                s += s1
                f.write(s + "\n")

                iBlock += 1
        f.close()

    def readFromFile_Chromosome_vBlockOfSyntheny(self):
        for Chromosome in self.vChromosome:
            Chromosome.vBlockOfSyntheny = []
            print(Chromosome.sNameChr)
        sFileName = "ReferenceGenome_" + self.name + ".txt"
        f = open(sFileName, "r")
        iRow = 0
        for s in f:
            if len(s) > 1 and iRow > 0:
                s = s[0 : len(s) - 1]  # cut \n
                ss = s.split("\t")
                sNameSeq = ss[1]
                coorStart = int(ss[8])
                coorEnd = int(ss[9])
                iLG = int(ss[10])
                coorOnLGstart = float(ss[11])
                coorOnLGend = float(ss[12])
                self.addBlock(
                    sNameSeq, coorStart, coorEnd, iLG, coorOnLGstart, coorOnLGend
                )
            iRow += 1
        f.close()

    def attachMarkersToAnotherAssembly(self, vLG):
        print("attachMarkersToAnotherAssembly...")

        # ne gotovo
        sSeqOriginalForMarkers
        sSeqAssemblyName

        sFileNameFasta1 = ""
        index1 = -1
        sFileNameFasta2 = ""
        index2 = -1
        sDobaffka = ""
        sFileNameBlastRes = ""

        sFileNameFasta1 = "C:\\Frenkel\\Privman\\Cnig_gn1\\gg_Cnig_gn1.txt"
        index1 = 0

        iData = 2
        if iData == 0:
            sFileNameFasta2 = "C:\\Frenkel\\Privman\\Cnig_gn2\\gg_Cnig_gn2.txt"
            index2 = 1

            sFileNameBlastRes = (
                "C:\\Frenkel\\Privman\\Cnig_gn2\\res_Cnig_gn1_vs_Cnig_gn2_e149.out"
            )
            sDobaffka = "Cnig_gn2"
        if iData == 1:
            sFileNameFasta2 = "C:\\Frenkel\\Privman\\Cnig_gn1\\gg_Cnig_gn1_pacbio_1.txt"
            index2 = 0

            sFileNameBlastRes = "C:\\Frenkel\\Privman\\Cnig_gn1\\res_Cnig_gn1_vs_Cnig_gn1_pacbio_1_e150.out"
            sDobaffka = "Cnig_gn1_pacbio_1"
        if iData == 2:
            sFileNameFasta2 = "C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\genome_assemblies_genome_fasta\\ncbi-genomes-2020-05-04\\gg_FormicaSelysi.txt"
            index2 = 2

            sFileNameBlastRes = (
                "C:\\Frenkel\\Privman\\Cnig_gn1\\res_Cnig_gn1_vs_FormicaSelysi_e70.out"
            )
            sDobaffka = "FormicaSelysi"
        if iData == 3:
            # sFileNameBlastResults="C:\\Frenkel\\Privman\\PacBio202008\\canu\\res_Cnig_ng1_vs_asm.contigs_e150.out"
            # sFileNameFastaQ="C:\\Frenkel\\Privman\\Cnig_gn1\\SPades_M4B_K13-123_28_2_2017_B.scaffolds.fasta"
            # sFileNameFastaDB="C:\\Frenkel\\Privman\\PacBio202008\\canu\\asm.contigs.fasta"
            sFileNameFasta2 = (
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\asm.contigs.fasta"
            )
            index2 = 2

            # ?
            sFileNameBlastRes = (
                "C:\\Frenkel\\Privman\\Cnig_gn1\\res_Cnig_gn1_vs_FormicaSelysi_e70.out"
            )
            sDobaffka = "FormicaSelysi"
        if iData == 4:
            sFileNameFasta2 = (
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\300-500.pilon.fasta"
            )
            index2 = 2
            # ?
            sFileNameBlastResults = "C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\res_pilon_vs_formica_v1_e70.out"
            sDobaffka = "FormicaSelysi"
        fasta1 = clSecCtgs()
        fasta1.readFromFastaFile(sFileNameFasta1, index1)
        fasta1.readCoorFromLGs(vLG, self, sSeqOriginalForMarkers, sSeqAssemblyName)

        fasta2 = clSecCtgs()
        fasta2.readFromFastaFile(sFileNameFasta2, index2)

        myBlastRes = clBlastRes()
        sFileName1 = (
            "attachMarkersToAnotherAssembly__markersOnNotUniqueIntervals_"
            + sDobaffka
            + ".txt"
        )
        f1 = open(sFileName1, "w")
        s = "i_of_nn" + "\t" + "nn" + "\t" + "ctgDB"
        s += "\t" + "coorOnCtgDB"
        s += "\t" + "marker" + "\t" + "iLG" + "\t" + "coorOnLG(cM)"
        f1.write(s + "\n")

        f = open(sFileNameBlastRes, "r")
        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        markersOnRefGenome = []
        bPrintDetails = False
        while bContinue:
            iBlock += 1
            if bPrintDetails:
                if iBlock % 100 == 1:
                    print("attachMarkersToAnotherAssembly..." + str(iBlock))
            LinesOfBlastRes = myBlastRes.clLinesOfBlastRes(
                sFirstStringOfBlockOfFastaResult, f
            )
            sFirstStringOfBlockOfFastaResult = (
                LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
            )
            bContinue = LinesOfBlastRes.bNotTheLastBlock
            self.attachMarkersToAnotherAssembly___processBlock(
                LinesOfBlastRes, f1, fasta1, fasta2, markersOnRefGenome
            )
        f.close()
        f1.close()

        # print "nNodes="+str(net.nNodes)+", nEdges="+str(net.nEdges)
        sFileName = "attachMarkersToAnotherAssembly_" + sDobaffka + ".txt"
        f = open(sFileName, "w")
        s = "ctg\tlen\tnPos\tPos\tmarkersGood"
        f.write(s + "\n")
        for ctg in fasta2.vCtg:
            sMarkers = ""
            for LGmarker in ctg.vLGmarker:
                if len(sMarkers) > 0:
                    sMarkers += ","
                sMarkers += LGmarker.m.sMarker
            s = ctg.name
            s += "\t" + str(ctg.seqLength)
            s += "\t" + str(len(ctg.vPos))
            s += "\t" + ctg.sPos()
            s += "\t" + sMarkers
            f.write(s + "\n")
        f.close()
        print("attachMarkersToAnotherAssembly...Finished. See two files:")
        print("1. " + sFileName1)
        print("2. " + sFileName)
        return markersOnRefGenome

    def attachMarkersToAnotherAssembly___processBlock(
        self, LinesOfBlastRes, f1, fasta1, fasta2, markersOnRefGenome
    ):
        iQ = fasta1.vCtgName.index(LinesOfBlastRes.sQ)  # iCtg in Cnig_gn1

        vsDB = LinesOfBlastRes.vsDB_get()
        vnLen = LinesOfBlastRes.vnLen_get()
        vstartQ = LinesOfBlastRes.vstartQ_get()
        vendQ = LinesOfBlastRes.vendQ_get()
        vstartDB = LinesOfBlastRes.vstartDB_get()
        vendDB = LinesOfBlastRes.vendDB_get()

        iDB = -1
        sDB_prev = ""
        n = len(vsDB)
        # vvsDB=[]
        for LGmarker in fasta1.vCtg[iQ].vLGmarker:
            vPrivmanvPosOnCtg = LGmarker.m.vPrivmanvPosOnCtg
            posOnCtgMin = min(vPrivmanvPosOnCtg)
            posOnCtgMax = max(vPrivmanvPosOnCtg)

            # vsDB1 = array of contigs from DB (with no repeats) overlapping with our ctg in the place of marker
            vsDB1 = []
            vcoorDB = []  # only one position of marker on sDB, len(vcoorDB)=len(vsDB1)
            for i in range(n):
                sDB = vsDB[i]
                if not (sDB in vsDB1):
                    startQ = vstartQ[i]
                    endQ = vendQ[i]
                    posOnCtgMinOVLP = min([startQ, endQ])
                    posOnCtgMaxOVLP = max([startQ, endQ])
                    startDB = vstartDB[i]
                    endDB = vendDB[i]
                    bOk = True
                    if posOnCtgMax < posOnCtgMinOVLP or posOnCtgMin > posOnCtgMaxOVLP:
                        bOk = False
                    if bOk:
                        vsDB1.append(sDB)
                        b = (endQ - startQ) * (posOnCtgMax - posOnCtgMin) < 0
                        d = posOnCtgMin - startQ
                        coorDB = startDB + d
                        if b:
                            coorDB = startDB - d
                        vcoorDB.append(coorDB)
            # vvsDB.append([vsDB1,vcoorDB])

            """
					#vLGmarkerOnOverlap
					vLGmarkerOnOverlap=[]
					#o=(nLen>3000 or nLen>0.5*fasta1.vCtg[iQ].seqLength or nLen>0.5*fasta2.vCtg[iDB].seqLength)
					#if iQ>=0 and iDB>=0 and o:
					for LGmarker in fasta1.vCtg[iQ].vLGmarker:
						vPrivmanvPosOnCtg=LGmarker.m.vPrivmanvPosOnCtg
						posOnCtgMin=min(vPrivmanvPosOnCtg)
						posOnCtgMax=max(vPrivmanvPosOnCtg)
						posOnCtgMinOVLP=min([startQ,endQ])
						posOnCtgMaxOVLP=max([startQ,endQ])
						bOk=True
						if posOnCtgMax<posOnCtgMinOVLP or posOnCtgMin>posOnCtgMaxOVLP:
							bOk=False
						if bOk:
							vLGmarkerOnOverlap.append(LGmarker)
					
					#update:
					#fasta2.vCtg[iDB].vLGmarker
					#fasta2.vCtg[iDB].vPos
					for LGmarker in vLGmarkerOnOverlap:
						if sDB!=sDB_prev:
							iDB=fasta2.vCtgName.index(sDB) #iCtg in Cnig_gn2
							sDB_prev=sDB
						if not LGmarker in fasta2.vCtg[iDB].vLGmarker:
							#LG=vLG[LGmarker.LGid]
							iLG=LGmarker.LGid
							coor=LGmarker.coorOnLG
							fasta2.vCtg[iDB].vLGmarker.append(LGmarker)
							fasta2.vCtg[iDB].vPos=fasta2.vPos_update(fasta2.vCtg[iDB].vPos,iLG,coor,[],[])
			"""
            iLG = LGmarker.LGid
            coor = LGmarker.coorOnLG
            # update:
            # fasta2.vCtg[iDB].vLGmarker
            # fasta2.vCtg[iDB].vPos
            if len(vsDB1) == 1:
                sDB = vsDB1[0]
                iDB = fasta2.vCtgName.index(sDB)  # iCtg in Cnig_gn2
                if not LGmarker in fasta2.vCtg[iDB].vLGmarker:
                    # LG=vLG[LGmarker.LGid]
                    fasta2.vCtg[iDB].vLGmarker.append(LGmarker)
                    fasta2.vCtg[iDB].vPos = fasta2.vPos_update(
                        fasta2.vCtg[iDB].vPos, iLG, coor, [], []
                    )
                markersOnRefGenome.append(
                    [iDB, sDB, vcoorDB[0], LGmarker]
                )  # [iDB,sDB,coorDB,LGmarker]
            # 247 markers have two or more positions on Cnig_gn2
            sMarkers = LGmarker.m.sMarker
            i = 0
            nn = len(vsDB1)
            for sDB in vsDB1:
                s = str(i + 1) + "\t" + str(nn) + "\t" + sDB
                s += "\t" + str(vcoorDB[i])
                s += "\t" + sMarkers + "\t" + str(iLG) + "\t" + str(coor)
                f1.write(s + "\n")
                i += 1

    def attachMarkersToAnotherAssembly___notInUse_readFromFile(self, fastaDB):
        # not in use

        sFileName = "C:\\Frenkel\LTCPython\VovaPy\attachMarkersToAnotherAssembly__markersOnNotUniqueIntervals_FormicaSelysi.txt"
        f = open(sFileName, "r")
        vvv = []
        i = 0
        for s in f:
            if len(s) > 1:
                s = s[0 : len(s) - 1]  # cut \n
                ss = s.split("\t")
                # s=str(i+1)+"\t"+str(nn)+"\t"+sDB
                # s+="\t"+str(vcoorDB[i])
                # s+="\t"+sMarkers+"\t"+str(iLG)+"\t"+str(coor)
                if i > 0:  # not shapka
                    if int(ss[1]) == 1:  # markers with unique positions only
                        iDB = fastaDB.vCtgName.index(ss[2])
                        coorDB = int(ss[3])
                        sMarkers = ss[4]
                        iLG = int(ss[5])
                        coorOnLG = float(ss[6])
                        q = [iDB, coorDB, sMarkers, iLG, coorOnLG]
                        vvv.append(q)
                i += 1
        f.close()

        def MyFunc(q):
            return q[0] + 0.000000001 * q[1]

        vvv.sort(key=MyFunc)

        def processBlock(iDB, vcoorDB, iLG, vcoorOnLG, vvvv):
            pass

        iDB = -1
        vcoorDB = []
        iLG = -1
        vcoorOnLG = []
        coorOnLG = -1
        i = 0
        vvvv = []
        for q in vvv:
            if q[0] != iDB or q[3] != iLG or abs(q[4] - coorOnLG) >= 20:
                if i > 0:
                    processBlock(iDB, vcoorDB, iLG, vcoorOnLG, vvvv)
                else:
                    iDB = q[0]
                    iLG = q[3]
                    coorOnLG = q[4]
                    vcoorDB = []
                    vcoorOnLG = []
            i += 1
        processBlock(iDB, vcoorDB, iLG, vcoorOnLG, vvvv)

        return vvv

    def attachMarkersToAnotherAssembly__makeBlocksOfRefGenome(
        self, vLG, markersOnRefGenome
    ):
        # [iDB,sDB,vcoorDB[i],LGmarker]
        def MyFunc(q):
            return q[0] + 0.000000001 * q[2]

        markersOnRefGenome.sort(key=MyFunc)
        n = len(markersOnRefGenome)

        def processSelected(selected):
            print("")
            for q in selected:
                # ","+LGmarker.m.sMarker+"]"+
                print(
                    "q:"
                    + str(q[0])
                    + ","
                    + q[1]
                    + ","
                    + str(q[2])
                    + ","
                    + str(q[3].LGid)
                    + ","
                    + str(q[3].coorOnLG)
                    + ","
                    + str(q[3].indexOnPath)
                )

            nSelected = len(selected)
            if nSelected == 0:
                print("Empty block?!")
                return
            if nSelected == 1:
                # self.addBlock("CM020805.1",1900,11900,3,10,20)
                q = selected[0]
                self.addBlock(q[1], q[2], q[2], q[3].LGid, q[3].coorOnLG, q[3].coorOnLG)
                return
            if nSelected == 2:
                # self.addBlock("CM020805.1",1900,11900,3,10,20)
                q = selected[0]
                q1 = selected[1]
                self.addBlock(
                    q[1], q[2], q1[2], q[3].LGid, q[3].coorOnLG, q1[3].coorOnLG
                )
                return
            if nSelected == 3:
                q = selected[0]
                q1 = selected[1]
                q2 = selected[2]
                if (q2[3].coorOnLG - q1[3].coorOnLG) * (
                    q1[3].coorOnLG - q[3].coorOnLG
                ) > 0:
                    self.addBlock(
                        q[1], q[2], q1[2], q[3].LGid, q[3].coorOnLG, q1[3].coorOnLG
                    )
                    self.addBlock(
                        q[1], q1[2], q2[2], q[3].LGid, q1[3].coorOnLG, q2[3].coorOnLG
                    )
                else:
                    minCoor = min([q[3].coorOnLG, q1[3].coorOnLG, q2[3].coorOnLG])
                    maxCoor = max([q[3].coorOnLG, q1[3].coorOnLG, q2[3].coorOnLG])
                    self.addBlock(q[1], q[2], q2[2], q[3].LGid, minCoor, maxCoor)
                return
            if nSelected > 3:
                """
                q=selected[0]
                q1=selected[1]
                q2=selected[2]
                d1=q2[3].coorOnLG-q1[3].coorOnLG
                d2=q1[3].coorOnLG-q[3].coorOnLG
                if d1*d2>0:
                        self.addBlock(q[1],q[2],q1[2],q[3].LGid,q[3].coorOnLG,q1[3].coorOnLG)
                else:
                        if d2>0:
                                self.addBlock(q[1],q[2],q1[2],q[3].LGid,q1[3].coorOnLG,q1[3].coorOnLG-0.0001)
                        else:
                                self.addBlock(q[1],q[2],q1[2],q[3].LGid,q1[3].coorOnLG,q1[3].coorOnLG+0.0001)
                """
                d = selected[nSelected - 2][3].coorOnLG - selected[1][3].coorOnLG
                bPlus = d >= 0
                qPrev = selected[0]
                coorPrev = qPrev[3].coorOnLG
                # correct coordinates on genetic map for markers not on path
                if qPrev[3].indexOnPath < 0:
                    if bPlus:
                        if coorPrev >= selected[1][3].coorOnLG:
                            coorPrev = selected[1][3].coorOnLG - 0.0001
                    else:
                        if coorPrev <= selected[1][3].coorOnLG:
                            coorPrev = selected[1][3].coorOnLG + 0.0001
                for i in range(0, nSelected - 1):
                    q = selected[i + 1]
                    if (abs(q[3].coorOnLG - qPrev[3].coorOnLG) >= 10) or (
                        i == nSelected - 2
                    ):
                        coor = q[3].coorOnLG
                        # correct coordinates on genetic map for markers not on path
                        if q[3].indexOnPath < 0:
                            if bPlus:
                                if coor <= selected[nSelected - 2][3].coorOnLG:
                                    coor = selected[nSelected - 2][3].coorOnLG + 0.0001
                            else:
                                if coor >= selected[nSelected - 2][3].coorOnLG:
                                    coor = selected[nSelected - 2][3].coorOnLG - 0.0001
                        self.addBlock(q[1], qPrev[2], q[2], q[3].LGid, coorPrev, coor)
                        qPrev = q
                        coorPrev = qPrev[3].coorOnLG
                """
				q=selected[nSelected-1]
				q1=selected[nSelected-2]
				q2=selected[nSelected-3]
				d1=q2[3].coorOnLG-q1[3].coorOnLG
				d2=q1[3].coorOnLG-q[3].coorOnLG
				if d1*d2>0:
					self.addBlock(q[1],q[2],q1[2],q[3].LGid,q[3].coorOnLG,q1[3].coorOnLG)
				else:
					if d2>0:
						self.addBlock(q[1],q[2],q1[2],q[3].LGid,q1[3].coorOnLG,q1[3].coorOnLG-0.0001)
					else:
						self.addBlock(q[1],q[2],q1[2],q[3].LGid,q1[3].coorOnLG,q1[3].coorOnLG+0.0001)
				"""
            return

        i = 0
        iDBprev = -1
        iLGprev = -1
        coorPrev = -1
        selected = []
        qPrev = markersOnRefGenome[0]
        bqPrev = False
        for q in markersOnRefGenome:
            bNewBlock = False
            if i == 0:
                bNewBlock = True
            else:
                if (
                    iDBprev != q[0]
                    or iLGprev != q[3].LGid
                    or abs(coorPrev - q[3].coorOnLG) > 10
                ):
                    bNewBlock = True
                    if bqPrev:
                        selected.append(qPrev)
                    processSelected(selected)
                    selected = []
            if bNewBlock:
                selected.append(q)
                bqPrev = False
            else:
                if q[3].indexOnPath >= 0:
                    selected.append(q)
                    bqPrev = False
                else:
                    qPrev = q
                    bqPrev = True
            iDBprev = q[0]
            iLGprev = q[3].LGid
            coorPrev = q[3].coorOnLG
            i += 1
        if bqPrev:
            selected.append(qPrev)
        processSelected(selected)

        self.printToFile_Chromosome_vBlockOfSyntheny()

    # def make_based_on_marker_names(self,Genotypes):
    # 	MarkersWithMultiplePos=clMarkersWithMultiplePos()
    def attachMarkersToAnotherAssembly_simple(self, Genotypes, MarkersWithMultiplePos):
        # Genotypes: clGenotypes()
        # used to
        # 1. map markers from Cnig_gn2(original for GWAS) to Cnig_gn1(reference, i.e., self)
        # or
        # 2. map markers from Cnig_gn1(original for genetic mapping based on 117 males) to new assemblies(reference, i.e., self)
        #
        # Output file 1: (only for markers in overlaps found by BLAST)
        # shapka: iMarker markerName iCopy nCopies ctg_Cnig_gn1 coor_Cnig_gn1 lengthOverlap
        #
        # Output file 2: (for all markers)
        # shapka: iMarker markerName nCopies
        #
        #
        # names of ctg of marker: scaffold1|size1555347 (GWAS markers are on Cnig_gn2 contigs)
        # name of marker: scaffold22|size714790___151541
        # name from DB: NODE_343_length_67353_cov_2.59656 (reference genome is Cnig_gn1)

        # poka new/ in Future it can be loaded and updated

        print("attachMarkersToAnotherAssembly_simple...")
        myBlastRes = clBlastRes()

        fasta1 = self.originalDataFasta  # e.g., Cnig_gn2
        print("originalDataFasta file is " + self.originalDataFasta.fasta)

        if len(self.dataFasta.vCtgName) == 0:
            # self.name="Formica"
            self.dataFasta = PrivmanLab.SecCtgsByName(self.name, True)

        iMapOriginal = len(MarkersWithMultiplePos.vsMapName)  # 0
        MarkersWithMultiplePos.addMap(self.originalDataName)
        vsPartName = self.originalDataFasta.vCtgName
        MarkersWithMultiplePos.vvsPartName.append(vsPartName)

        iMap = len(MarkersWithMultiplePos.vsMapName)
        MarkersWithMultiplePos.addMap(self.name)
        vsPartName = self.dataFasta.vCtgName
        MarkersWithMultiplePos.vvsPartName.append(vsPartName)

        LinkageGroup = clLinkageGroup()
        id = 0
        vCopies = []  # [iMarker]
        sNamePrev = ""
        for m in Genotypes.vMarker:
            vCopies.append([])
            if m.sMarker == sNamePrev:
                MarkerWithMultiplePos = MarkersWithMultiplePos.vMarkerWithMultiplePos[
                    id - 1
                ]
                MarkerWithMultiplePos.vvPosOnMap[iMapOriginal][0].iType += 1
            else:
                LGmarker = LinkageGroup.clMarkerOfLG()  # No real LG here
                LGmarker.m = m

                m.id = id
                ss = m.sMarker.split("___")  # NODE_13_length_173790_cov_2.7937___8823
                sCtg = ss[0]  # NODE_13_length_173790_cov_2.7937
                coor = int(ss[1])  # 8823

                iCtg = fasta1.vCtgName.index(sCtg)
                ctg = fasta1.vCtg[iCtg]  # original contig (e.g., from Cnig_gn2)
                ctg.vLGmarker.append(LGmarker)

                m.vPrivmanvPosOnCtg = [coor]

                MarkerWithMultiplePos = MarkersWithMultiplePos.clMarkerWithMultiplePos()
                MarkerWithMultiplePos.sName = m.sMarker
                MarkerWithMultiplePos.sName_sourse = self.originalDataName  # poka
                MarkersWithMultiplePos.addMarker(
                    MarkerWithMultiplePos
                )  # here we also resize vvPosOnMap but we need the name (to add for faster search)
                iType = 0  # original marker
                MarkerWithMultiplePos.addPosOnMap(iMapOriginal, iCtg, coor, iType)
                id += 1
            sNamePrev = m.sMarker
        # fasta1.readCoorFromLGs(vLG,ReferenceGenome,sSeqOriginalForMarkers,sSeqAssemblyName)

        print(
            "len(MarkersWithMultiplePos.vMarkerWithMultiplePos)="
            + str(len(MarkersWithMultiplePos.vMarkerWithMultiplePos))
        )

        f = open(
            self.sFileNameBlastResMeDB, "r"
        )  # reference genome (e.g., Cnig_gn1) is DB

        # Output file 1: (only for markers in overlaps found by BLAST)
        sFileOut = self.attachMarkersToAnotherAssembly_simple___sFileOut

        # poka not in use
        # sFileNameCtg_Cnig_gn1_onMyAssembly="C:\\Frenkel\\LTCPython\\VovaPy\\20200531a\\MappingReport.txt"

        f1 = open(sFileOut, "w")
        s = "iMarker" + "\t" + "marker"
        s += "\t" + "iCopy" + "\t" + "nCopies"
        s += "\t" + "ctgDB" + "\t" + "coorOnCtgDB" + "\t" + "lengthOverlap"
        f1.write(s + "\n")

        iMarker = 0
        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        # markersOnRefGenome=[]
        bPrintDetails = False
        while bContinue:
            iBlock += 1
            if bPrintDetails:
                if iBlock % 100 == 1:
                    print("attachMarkersToAnotherAssembly_simple..." + str(iBlock))
            LinesOfBlastRes = myBlastRes.clLinesOfBlastRes(
                sFirstStringOfBlockOfFastaResult, f
            )
            sFirstStringOfBlockOfFastaResult = (
                LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
            )
            bContinue = LinesOfBlastRes.bNotTheLastBlock

            iCtg = fasta1.vCtgName.index(LinesOfBlastRes.sQ)  # iCtg in Cnig_gn2
            # self.attachMarkersToAnotherAssembly___processBlock(iQ,vsDB,vnLen,vstartQ,vendQ,vstartDB,vendDB,f1,fasta1,fasta2,markersOnRefGenome)

            # reference genome is Q
            vsDB = LinesOfBlastRes.vsDB_get()  # contig names from in Cnig_gn1
            vnLen = LinesOfBlastRes.vnLen_get()
            vstartQ = LinesOfBlastRes.vstartQ_get()
            vendQ = LinesOfBlastRes.vendQ_get()
            vstartDB = LinesOfBlastRes.vstartDB_get()
            vendDB = LinesOfBlastRes.vendDB_get()
            LinesOfBlastRes.makeArrays()

            n = len(vsDB)
            ctg = fasta1.vCtg[iCtg]  # in Cnig_gn2
            for LGmarker in ctg.vLGmarker:
                # poka
                MarkerWithMultiplePos = MarkersWithMultiplePos.vMarkerWithMultiplePos[
                    LGmarker.m.id
                ]

                coor = LGmarker.m.vPrivmanvPosOnCtg[
                    0
                ]  # physical position on ctg from assembly in Cnig_gn2
                qqq = []
                for i in range(n):
                    if coor >= vstartQ[i] and coor <= vendQ[i]:
                        # coorDB=self.attachMarkersToAnotherAssembly_simple___coorDB(coor,vstartQ[i],vstartDB[i],vendDB[i])
                        # LinesOfBlastRes.makeArrays()
                        coorDB = LinesOfBlastRes.LinesOfBlastRes[i].coorDB_get(coor, -1)
                        i_vsDB = vsDB.index(
                            vsDB[i]
                        )  # index in vsDB (i_vsDB <= i: unique => "=", else the most significant (first in the list))
                        qqq.append(
                            [i_vsDB, coorDB, vnLen[i]]
                        )  # [index in vsDB, coor on ctg from Cnig_gn1, length of overlap]

                # select from qqq only the longest overlap for each ctg from Cnig_gn1
                def MyFunc(q):
                    return (
                        q[0] * 1000000000 - q[2]
                    )  # i_vsDB*100000000 - <length of overlap>

                qqq.sort(key=MyFunc)
                qqqq = []
                i_vsDB_done = -1
                for q in qqq:
                    i_vsDB = q[0]
                    if i_vsDB > i_vsDB_done:
                        qqqq.append(q)
                        i_vsDB_done = i_vsDB

                nCopies = len(
                    qqqq
                )  # number of contigs from Cnig_gn1 covering the marker (from Cnig_gn2)
                if nCopies > 0:
                    # vCopies[LGmarker.m.id]
                    for iCopy in range(nCopies):
                        q = qqqq[iCopy]
                        sCtgNameDB = vsDB[q[0]]
                        coorOnCtgDB = q[1]
                        lengthOfOverlap_ctgQ_ctgDB = q[2]

                        vCopies[LGmarker.m.id].append(
                            [iCtg, sCtgNameDB, coorOnCtgDB]
                        )  # [iCtg in Cnig_gn2, name of ctg from Cnig_gn1, coor on ctg from Cnig_gn1]
                        s = str(iMarker) + "\t" + LGmarker.m.sMarker
                        s += "\t" + str(iCopy) + "\t" + str(nCopies)
                        s += (
                            "\t"
                            + sCtgNameDB
                            + "\t"
                            + str(coorOnCtgDB)
                            + "\t"
                            + str(lengthOfOverlap_ctgQ_ctgDB)
                        )
                        f1.write(s + "\n")

                        if not (sCtgNameDB in self.dataFasta.vCtgName):
                            print(str(self.dataFasta.vCtgName))
                        iCtg1 = self.dataFasta.vCtgName.index(sCtgNameDB)
                        iType = (
                            nCopies - 1
                        )  # number of copies found by blast-1 => 0 is ok
                        MarkerWithMultiplePos.addPosOnMap(
                            iMap, iCtg1, coorOnCtgDB, iType
                        )
                        # print MarkerWithMultiplePos.sName
                        # print "len(self.vvPosOnMap[iMap])="+str(len(MarkerWithMultiplePos.vvPosOnMap[iMap]))
                        # print "nPosMax="+str(MarkerWithMultiplePos.nPosMax)
                iMarker += 1
        f.close()
        f1.close()

        # Output file 2: (for all markers)
        # shapka: iMarker markerName nCopies
        sFileOut1 = self.attachMarkersToAnotherAssembly_simple___sFileOut1
        f1 = open(sFileOut1, "w")

        s = "iMarker" + "\t" + "marker" + "\t" + "nCopies"
        f1.write(s + "\n")

        n = len(Genotypes.vMarker)
        for i in range(n):
            s = (
                str(i)
                + "\t"
                + Genotypes.vMarker[i].sMarker
                + "\t"
                + str(len(vCopies[i]))
            )
            f1.write(s + "\n")
        f1.close()
        print("attachMarkersToAnotherAssembly_simple...Finished. see two files")
        print("1: " + sFileOut)
        print("2: " + sFileOut1)
        return MarkersWithMultiplePos


class clTestsVova:
    def test_netBasedOnBlastRes_ClusteringAndReport(self):
        # sFileNameBlast="C:\\Frenkel\\Privman\\Cnig_gn1\\res_diploid_vs_Cnig_gn1_e150.out"
        sFileNameBlast = "C:\\Frenkel\\Privman\\Cnig_gn1\\res_Solenopsis_invicta_vs_Cnig_gn1_e30.out"  # results of BLAST vs Solenopsis_invicta
        myNetBasedOnBlastRes = clNetBasedOnBlastRes(sFileNameBlast, 2)
        myNetBasedOnBlastRes.ClusteringAndReport()

    def test_vvSortedAndNoOutLiersIfNeed(self):
        VovaMath = clVovaMath()
        VovaMath.vvSortedAndNoOutLiersIfNeed([], 20)
        VovaMath.vvSortedAndNoOutLiersIfNeed([], 40)
        VovaMath.vvSortedAndNoOutLiersIfNeed([], 60)

    def test_trait(self):
        tt = clTrait()
        tt.test()

    def test_makeListOfAllPermutation_test(self):
        mmm = clVovaMath()
        mmm.makeListOfAllPermutation_test()

    def test_readFromFastaFile(self):
        fasta = clSecCtgs()
        sFileNameFasta = "C:\\Frenkel\\Privman\\Cnig_gn1\\SPades_M4B_K13-123_28_2_2017_B.scaffolds.fasta"
        fasta.readFromFastaFile(sFileNameFasta, 0)

    def test_printSeqFromIntervalAllCandidates(self, fasta):
        iLG = 0
        coorStartInclude = 0
        coorEndNotInclude = 20
        sFileName = "primer0.txt"
        bFirst = True
        fasta.printSeqFromIntervalAllCandidates(
            iLG, coorStartInclude, coorEndNotInclude, sFileName, bFirst
        )

    def test_blockOfBlastResults_intervalsOnQ(self):
        pass

    def test_vqValuesFDR(self):
        mmm = clVovaMath()
        n = 1000
        vp = [
            1,
            0.5,
            0.25,
            0.125,
            0.0625,
            0.03125,
            0.015625,
            0.0075,
            0.003,
            0.002,
            0.001,
        ]
        vp = [0.01, 0.001, 0.0001, 0.00001, 0.00001, 0.00001, 0.00001, 0.001]
        vq = mmm.vqValuesFDR(vp, n)
        print(str(n))
        print(str(vp))
        print(str(vq))

    def test_ReferenceGenome(self):
        ReferenceGenome = clReferenceGenome("Cnig_gn1", "Formica")
        # ReferenceGenome.addBlock(sNameSeq,coorStart,coorEnd,iLG,coorOnLGstart,coorOnLGend)
        ReferenceGenome.addBlock("CM020805.1", 1900, 11900, 3, 10, 20)
        ReferenceGenome.addBlock("CM020805.1", 10000, 30000, 2, 8.7, 36.5)
        ReferenceGenome.addBlock("CM020816.1", 100, 1000100, 1, 100, 0)
        ReferenceGenome.printToFile_Chromosome_vBlockOfSyntheny()
        ReferenceGenome.readFromFile_Chromosome_vBlockOfSyntheny()
        ReferenceGenome.addBlock("CM020816.1", 100, 1000100, 1, 100, 0)
        # ReferenceGenome.printToFile_Chromosome_vBlockOfSyntheny()

    def test_MultiQTL_fromTable(self):
        MultiQTL = clMultiQTL()
        MultiQTL.start()

    def test_MultiQTL_permTestChrom(self):
        MultiQTL = clMultiQTL()
        ChromTrait = MultiQTL.clChromTrait()
        VovaMath = clVovaMath()
        vp = []
        for i in range(20):
            p = ChromTrait.testBySimul()
            vp.append(p)
        print("mean=" + str(VovaMath.mean(vp)))

    def test_TableOfTxt(self):
        TableOfTxt = clTableOfTxt()
        sFileName = "C:\\Frenkel\\Privman\\Aparna\\markers_on_asm.txt"
        # /cygdrive/c/Frenkel/Privman/Aparna/drafts/markers117males_Cnig_gn1_on_asm.txt
        bShapka = True
        bFirstColNoNeedToRead = True
        TableOfTxt.readFromFile(sFileName, bShapka, bFirstColNoNeedToRead)
        print("nRows=" + str(TableOfTxt.nRows))
        TableOfTxt.printToFile(sFileName + ".txt", bShapka)
        iCol = 3
        textCol = "tig00001985"
        iCol = 0
        textCol = "NODE_34_length_131713_cov_2.61718___48737"
        iRows = TableOfTxt.iRows_get(textCol, iCol)
        print(str(iRows))
        print(str(TableOfTxt.vColText))
        iRow = TableOfTxt.iRow_get(textCol, iCol)
        print("iRow=" + str(iRow))

    def testCurrent(self):
        print("testing started")
        # self.test_trait()
        # self.test_vqValuesFDR()
        # self.test_readFromFastaFile()

        # self.test_netBasedOnBlastRes_ClusteringAndReport()
        # self.test_vvSortedAndNoOutLiersIfNeed()

        # self.test_makeListOfAllPermutation_test()
        # self.test_blockOfBlastResults_intervalsOnQ()

        # self.test_ReferenceGenome()

        # self.test_MultiQTL_fromTable()
        # self.test_MultiQTL_permTestChrom()
        # test_blockOfBlastResults_intervalsOnQ(self)

        # self.test_TableOfTxt()
        print("testing finished")


class clGeneticMap:
    def __init__(self):
        self.vsMarkerName = []
        self.vMarker = []
        self.vChromosome = []
        self.vsChrNamingVersionName = ["default"]
        self.sNameOfMap = ""
        self.GenomeMapComparisonGraph_map = None
        self.vvsChrName = []
        # self.readBesan()

    class clChromosome:
        def __init__(self):
            self.id = -1
            self.vsName = []  # [iVersion]
            self.geneticLengthBasedOnSkeletonMarlers_cM = 0
            self.vMarker = []
            self.length = -1

        class clMarker:
            def __init__(self, sName, Chromosome, iType, coor):
                self.sName = sName
                self.Chromosome = Chromosome
                self.iType = iType  # 0 - skeleton, 1 - close to skeleton (about twin), 2 - added from up, 3 - added from down
                self.coor = coor

            def sCtg_posPhysOnCtg_get(self):
                # NODE_1870_POS_24325
                ss = self.sName.split("_")
                sCtg = ss[1]
                posPhysOnCtg = int(ss[3])
                return sCtg, posPhysOnCtg

        def readFromFileMultiPoint(self, sFileName, GeneticMap):
            # Skeletons marker	Missing	Segregation	Distance	Added marker	Missing	Segregation	Distance
            # ^
            # [NODE_580_POS_19465]	21	1.0:1.1	0
            # NODE_1870_POS_24325	11	1.0:1.1
            # 				NODE_383_POS_24945(up)	8	1.0:1.3	0.94
            TableOfTxt = clTableOfTxt()
            TableOfTxt.readFromFile(sFileName, True, False)
            iRow = 0
            coorOfPrevSkeletonMarker = 0
            # print self.vsName[0]+"\t"+sFileName
            for row in TableOfTxt.rows:
                # if iRow>0:
                s = row.vCellText[0]
                b = True
                if len(s) >= 1:
                    b = s[0] != "^"
                if b:
                    iType = 0
                    sMarkerName = row.vCellText[0]
                    sMissing = row.vCellText[1]
                    sSegregation = row.vCellText[2]
                    sDistToPrevSkeletonMarker = row.vCellText[3]
                    if sMarkerName == "":
                        iType = 2
                        sMarkerName = row.vCellText[4]
                        sMissing = row.vCellText[5]
                        sSegregation = row.vCellText[6]
                        sDistToPrevSkeletonMarker = row.vCellText[7]
                        if "(" in sMarkerName:
                            n = sMarkerName.index("(")
                            if sMarkerName[n + 1] != "u":
                                iType = 3
                            sMarkerName = sMarkerName[:n]
                    else:
                        if sMarkerName[0] == "[":
                            sMarkerName = sMarkerName[1 : len(sMarkerName) - 1]
                            iType = 1
                    DistToPrevSkeletonMarker = 0
                    if len(sDistToPrevSkeletonMarker) > 0:
                        DistToPrevSkeletonMarker = float(sDistToPrevSkeletonMarker)
                    coor = (
                        coorOfPrevSkeletonMarker + DistToPrevSkeletonMarker
                        if (iType != 3)
                        or ((iType == 3) and (DistToPrevSkeletonMarker < 0))
                        else coorOfPrevSkeletonMarker - DistToPrevSkeletonMarker
                    )
                    Marker = self.clMarker(sMarkerName, self, iType, coor)
                    GeneticMap.vsMarkerName.append(sMarkerName)
                    GeneticMap.vMarker.append(Marker)
                    self.vMarker.append(Marker)
                    # print sMarkerName+"\t"+str(iType)
                    if iType == 0:
                        coorOfPrevSkeletonMarker = coor
                        self.geneticLengthBasedOnSkeletonMarlers_cM = coor
                iRow += 1

        def addName1TillSymbol(
            self, sSymbolSplit="|"
        ):  # scaffold10|size6254774 -> scaffold10
            if len(self.vsName) == 1:
                self.vsName.append("")
            vs = self.vsName[0].split(sSymbolSplit)
            self.vsName[1] = vs[0]

    def readBesan(self):
        print("readBesan...")

        # read from file table of Besans chromosomes renaming
        self.readChrNaming()

        # read Besan's genetic map from the folder of original MultiPoint output txt files
        for Chromosome in self.vChromosome:
            s = Chromosome.vsName[
                0
            ]  # Version 0 of chromosome name (not ordered on size)
            # print s
            sFileName = (
                "C:\\Frenkel\\Privman\\GeneticMapping\\GeneticMapByBesan_2020\\byChr\\"
                + s
                + ".txt"
            )
            Chromosome.readFromFileMultiPoint(sFileName, self)

        # test
        for Chromosome in self.vChromosome:
            sChr = Chromosome.vsName[3]  # the last version
            print(
                sChr
                + ": len="
                + str(Chromosome.geneticLengthBasedOnSkeletonMarlers_cM)
                + ", nMarkersTotal="
                + str(len(Chromosome.vMarker))
            )
            # for Marker in Chromosome.vMarker:
            # 	if Marker.iType==0:
            # 		print Marker.sName+"\t"+str(Marker.coor)
        print("readBesan...Finished")

    def readChrNaming(self):
        sFileName = "C:\\Frenkel\\Privman\\GeneticMapping\\GeneticMapByBesan_2020\\LGs Names_pp.txt"
        # Previous Names	Distance	Names by cM	Names202105
        # LG23	402.02	LG1	chr01
        TableOfTxt = clTableOfTxt()
        TableOfTxt.readFromFile(sFileName, True, False)
        self.vsChrNamingVersionName = []
        for CellText in TableOfTxt.shapka.vCellText:
            self.vsChrNamingVersionName.append(CellText)
        iRow = 0
        for row in TableOfTxt.rows:
            Chromosome = self.clChromosome()
            Chromosome.id = iRow
            for CellText in row.vCellText:
                Chromosome.vsName.append(CellText)
            Chromosome.length = float(row.vCellText[1])
            self.vChromosome.append(Chromosome)
            # print Chromosome.vsName
            iRow += 1

    def iMarkerBy_sCtg_posPhysOnCtg(self, sCtg, posPhysOnCtg):
        # NODE_1870_POS_24325
        sMarker = "NODE_" + sCtg + "_POS_" + str(posPhysOnCtg)
        iMarker = (
            self.vsMarkerName.index(sMarker) if (sMarker in self.vsMarkerName) else -1
        )
        return iMarker, sMarker

    def readFromFileMultiPoint_vAlexandra202206(
        self, sFileName, sNameOfMap, iFormat=0, iFormatOut=0
    ):
        self.sNameOfMap = sNameOfMap

        def sPP(s, iFormat, iFormatOut):
            if iFormat == iFormatOut:
                return s
            if iFormat == 1 and iFormatOut == 0:
                # s1p1327199 -> scaffold1p1327199
                sNew = "scaffold" + s[1:]
                return sNew
            if iFormat == 0 and iFormatOut == 1:
                # scaffold1p1327199 -> s1p1327199
                ss = s.split("d")
                sNew = "s" + ss[1]
                return sNew
            if iFormat == 1 and iFormatOut == 2:
                # s2p592932 -> Scaffold2___592932
                ss = s.split("p")
                sNew = "Scaffold" + ss[0][1:] + "___" + ss[1]
                return sNew

        """
				
				 
		LG1
				 
				 
		T 0.00     S  s40p1220724  
		T 0.00     B  s40p1222258  
		T 17.86    S  s40p853201   
		  7.27     S  s40p679407   
		  11.65    S  s40p392509   
		  11.65    B  s40p401984   
		  23.08    S  s86p269965   
		  3.09     S  s86p282095   
		  8.75     S  s55p977740   
		  5.75     S  s55p793319   
		  2.78     S  s55p680094   
				 
				 
		"""
        self.vsMarkerName = []
        self.vMarker = []
        self.vChromosome = []

        TableOfTxt = clTableOfTxt()
        f = open(sFileName, "r")
        f1 = open(sFileName + "_mapControl.txt", "w")

        iChr = -1
        sChr = ""
        myChr = self.clChromosome()
        coor = 0
        for s in f:
            s1 = TableOfTxt.sWithoutChr10Chr13(s)
            s1 = TableOfTxt.sChangeAllTabsToSpace(s1)
            s1 = TableOfTxt.sNoFinishingSpaces(s1)
            s1 = TableOfTxt.sChangeGroupOfSpacesToSingleTab(s1)
            if s1 != "":
                ss = s1.split("\t")
                if len(ss) == 1:  # LG1
                    iChr += 1
                    sChr = ss[0]

                    myChr = self.clChromosome()
                    self.vChromosome.append(myChr)
                    myChr.id = iChr
                    myChr.vsName = [sChr]  # [iVersion]
                    coor = 0
                else:
                    # T 0.00     S  s40p1220724
                    sMarkerName = ss[3]

                    # s2p7594518 -> scaffold1p2459502
                    sMarkerName = sPP(sMarkerName, iFormat, iFormatOut)

                    dcoor = float(ss[1])

                    s_0 = ss[0]  # sometimes T. Vova: may be have twins?
                    s_2 = ss[2]
                    iType = (
                        -1
                    )  # 0 - skeleton, 1 - close to skeleton (about twin), 2 - added from up, 3 - added from down
                    if s_2 == "S":
                        iType = 0
                        coor += dcoor
                    if s_2 == "B":
                        iType = 1
                        # in the same coor like previous skeleton marker
                    myMarker = myChr.clMarker(sMarkerName, myChr, iType, coor)
                    s3 = (
                        myChr.vsName[0]
                        + "\t"
                        + s_0
                        + "\t"
                        + s_2
                        + "\t"
                        + sMarkerName
                        + "\t"
                        + str(coor)
                    )
                    f1.write(s3 + "\n")
                    myChr.vMarker.append(myMarker)
                    myChr.geneticLengthBasedOnSkeletonMarlers_cM = max(
                        myChr.geneticLengthBasedOnSkeletonMarlers_cM, coor
                    )
                    self.vsMarkerName.append(sMarkerName)
                    self.vMarker.append(myMarker)
        f.close()
        f1.close()
        print("ggg...")
        for myChr in self.vChromosome:
            print(
                myChr.vsName[0]
                + " "
                + str(myChr.geneticLengthBasedOnSkeletonMarlers_cM)
            )
        print("ggg...NNN")

    def readFromFile_coorControl(self, sFileName, sNameOfMap):
        self.sNameOfMap = sNameOfMap
        # LG	marker	genotypePhased	phase	idOnLG	indexOnPath	coorOnLG	idOnLG_closestOnPath	LG_privman	coor_privman
        # LG1	scaffold1p67320	1100100110110000001010100011010000000101100-010101110101101100111100110-10101110100111110010100111101110000001101100	0	0	1	0.00	-1		-1.00
        # LG1	scaffold1p363446	1100100110110000001010100011010000000101100-010101110101101100111100110010101110100111110010100111111110000001101110	1	1	2	1.79	-1		-1.00
        self.vsMarkerName = []
        self.vMarker = []
        self.vChromosome = []

        TableOfTxt = clTableOfTxt()
        TableOfTxt.readFromFile(sFileName, True, False)
        iChr = -1
        sChr = ""
        myChr = self.clChromosome()
        for row in TableOfTxt.rows:
            s = row.vCellText[0]
            if s != sChr:
                iChr += 1
                sChr = s

                myChr = self.clChromosome()
                self.vChromosome.append(myChr)
                myChr.id = iChr
                myChr.vsName = [sChr]  # [iVersion]
            sMarkerName = row.vCellText[1]
            # 2 genotype
            # 3 phase
            # 4 idOnLG
            # 5 indexOnPath
            # 6 coorOnLG
            coor = float(row.vCellText[6])
            indexOnPath = int(row.vCellText[5])
            iType = (
                -1
            )  # 0 - skeleton, 1 - close to skeleton (about twin), 2 - added from up, 3 - added from down
            if indexOnPath >= 0:
                iType = 0  # on path, skeleton
            if indexOnPath < 1:
                iType = 1  # not on path
            myMarker = myChr.clMarker(sMarkerName, myChr, iType, coor)
            myChr.vMarker.append(myMarker)
            myChr.geneticLengthBasedOnSkeletonMarlers_cM = max(
                myChr.geneticLengthBasedOnSkeletonMarlers_cM, coor
            )
            self.vsMarkerName.append(sMarkerName)
            self.vMarker.append(myMarker)

    def readFromTableSimple(self, sFileName, bShapka, sNameOfMap):
        self.sNameOfMap = sNameOfMap

        # LG	marker	coor
        self.vsMarkerName = []
        self.vMarker = []
        self.vChromosome = []

        TableOfTxt = clTableOfTxt()
        # readFromFile(self,sFileName,bShapka,bFirstColNoNeedToRead)
        TableOfTxt.readFromFile(sFileName, bShapka, False)
        iChr = -1
        sChr = ""
        myChr = self.clChromosome()
        for row in TableOfTxt.rows:
            s = row.vCellText[0]
            if s != sChr:
                iChr += 1
                sChr = s

                myChr = self.clChromosome()
                self.vChromosome.append(myChr)
                myChr.id = iChr
                myChr.vsName = [sChr]  # [iVersion]
            sMarkerName = row.vCellText[1]
            coor = float(row.vCellText[2])
            indexOnPath = -1  # unknown here
            iType = (
                -1
            )  # unknown here  #0 - skeleton, 1 - close to skeleton (about twin), 2 - added from up, 3 - added from down
            if indexOnPath >= 0:
                iType = 0  # on path, skeleton
            if indexOnPath < 1:
                iType = 1  # not on path
            myMarker = myChr.clMarker(sMarkerName, myChr, iType, coor)
            myChr.vMarker.append(myMarker)
            myChr.geneticLengthBasedOnSkeletonMarlers_cM = max(
                myChr.geneticLengthBasedOnSkeletonMarlers_cM, coor
            )
            self.vsMarkerName.append(sMarkerName)
            self.vMarker.append(myMarker)

    def readFromMarkerNames___Genotypes(
        self, myGenotypes, sNameOfMap="Contigs"
    ):  # ,iFormatMarkerName):
        self.sNameOfMap = sNameOfMap

        # from name of markers
        # 0 - scaffold1p3196252
        vsMarkerName = []
        for m in myGenotypes.vMarker:
            sMarkerName = m.sMarker
            vsMarkerName.append(sMarkerName)

        self.vsMarkerName = []
        self.vMarker = []
        self.vChromosome = []
        vsChr = []
        iChrFound = 0
        for sMarkerName in vsMarkerName:
            MarkerName = clMarkerName(sMarkerName)
            # sChr=""
            # coor=-1
            # if iFormatMarkerName==0:#scaffold1p3196252
            # 	ss=sMarkerName.split("p")
            # 	sChr=ss[0]
            # 	coor=int(ss[1])
            ##ScbnsAo_1___161534
            sChr, coor = MarkerName.sCtg_coor_get(True)

            if sChr != "":
                if not (sChr in vsChr):
                    vsChr.append(sChr)
                    myChr = self.clChromosome()
                    self.vChromosome.append(myChr)
                    myChr.id = iChrFound
                    myChr.vsName = [sChr]  # [iVersion]
                    iChrFound += 1
                iChr = vsChr.index(sChr)
                myChr = self.vChromosome[iChr]
                iType = 0  # physical position
                myMarker = myChr.clMarker(sMarkerName, myChr, iType, coor)
                myChr.vMarker.append(myMarker)
                myChr.geneticLengthBasedOnSkeletonMarlers_cM = max(
                    myChr.geneticLengthBasedOnSkeletonMarlers_cM, coor
                )
                self.vsMarkerName.append(sMarkerName)
                self.vMarker.append(myMarker)

    def readFromFile_MSTsoftware(self, sFileName, bDoubles=False, sNameOfMap="MST"):
        self.sNameOfMap = sNameOfMap
        # http://www.mstmap.org/
        """
		;number of linkage groups: 60
		;The size of the linkage groups are: 
		;		1	2	1	2	2	1	1	1	1	1	2	2	2	2	2	2	1	2	1	1	1	1	2	2	2	1	1	2	1	2	2	2	1	2	1	2	2	2	1	1	2	1	1	1	3	1783	4	3	3	11	4	7	3	9	21	4	3	3	4	3	
		;The number of bins in each linkage group: 
		;		1	2	1	2	2	1	1	1	1	1	2	1	2	2	1	1	1	2	1	1	1	1	1	2	1	1	1	1	1	2	2	2	1	2	1	1	2	1	1	1	1	1	1	1	2	1011	2	3	1	7	2	3	1	2	11	2	2	2	1	2	
		
		...
		
		
		;lowerbound:21.000 upperbound: 21.000 cost after initialization:21.000
		group lg1
		;BEGINOFGROUP
		scaffold2p4841581	0.000
		scaffold2p4711373	18.963
		;ENDOFGROUP
		"""

        self.vsMarkerName = []
        self.vMarker = []
        self.vChromosome = []

        TableOfTxt = clTableOfTxt()
        f = open(sFileName, "r")
        f1 = open(sFileName + "_mapControl.txt", "w")

        iChr = -1
        sChr = ""
        myChr = self.clChromosome()
        coor = 0
        stateIndex = 0
        s_0 = ""  # not in use here
        s_2 = ""  # not in use here
        for s in f:
            s1 = TableOfTxt.sWithoutChr10Chr13(s)
            # s1=TableOfTxt.sChangeAllTabsToSpace(s1)
            # s1=TableOfTxt.sNoFinishingSpaces(s1)
            # s1=TableOfTxt.sChangeGroupOfSpacesToSingleTab(s1)
            if s1 != "":
                if s1[0] == ";":
                    if len(s1) > 4:
                        s2 = s1[0:4]
                        if s2 == ";low":
                            stateIndex = 1
                        if s2 == ";BEG":
                            stateIndex = 2
                        if s2 == ";END":
                            stateIndex = 0
                else:
                    if stateIndex == 1:  # group lg1
                        ss = s1.split(" ")
                        iChr += 1
                        sChr = ss[1]  # lg1

                        myChr = self.clChromosome()
                        self.vChromosome.append(myChr)
                        myChr.id = iChr
                        myChr.vsName = [sChr]  # [iVersion]
                        # coor=0
                    if stateIndex == 2:  # scaffold2p4711373	18.963
                        ss = s1.split("\t")
                        sMarkerName = ss[0]  # scaffold2p4711373
                        coor = float(ss[1])  # 18.963
                        iType = 0
                        myMarker = myChr.clMarker(sMarkerName, myChr, iType, coor)

                        s3 = (
                            myChr.vsName[0]
                            + "\t"
                            + s_0
                            + "\t"
                            + s_2
                            + "\t"
                            + sMarkerName
                            + "\t"
                            + str(coor)
                        )
                        f1.write(s3 + "\n")
                        myChr.vMarker.append(myMarker)
                        myChr.geneticLengthBasedOnSkeletonMarlers_cM = max(
                            myChr.geneticLengthBasedOnSkeletonMarlers_cM, coor
                        )
                        self.vsMarkerName.append(sMarkerName)
                        self.vMarker.append(myMarker)
        f.close()
        f1.close()

        if bDoubles:
            vsMarkerNamePP = []
            vMarkerPP = []
            vChromosomePP = []
            iChr = 0
            for Chromosome in self.vChromosome:
                Marker0 = Chromosome.vMarker[0]
                sName = Marker0.sName[1:]
                if not (sName in vsMarkerNamePP):
                    myChr = self.clChromosome()
                    vChromosomePP.append(myChr)
                    myChr.id = iChr
                    iChr += 1
                    myChr.vsName = Chromosome.vsName
                    myChr.geneticLengthBasedOnSkeletonMarlers_cM = (
                        Chromosome.geneticLengthBasedOnSkeletonMarlers_cM
                    )
                    for Marker in Chromosome.vMarker:
                        sName = Marker.sName[1:]
                        if sName in vsMarkerNamePP:
                            print("readFromFile_MSTsoftware error: marker " + sName)
                        else:
                            myMarker = myChr.clMarker(
                                sName, myChr, Marker.iType, Marker.coor
                            )
                            myChr.vMarker.append(myMarker)
                            vsMarkerNamePP.append(sName)
                            vMarkerPP.append(myMarker)
            self.vsMarkerName = vsMarkerNamePP
            self.vMarker = vMarkerPP
            self.vChromosome = vChromosomePP
        print("ggg...")
        for myChr in self.vChromosome:
            print(
                myChr.vsName[0]
                + " "
                + str(myChr.geneticLengthBasedOnSkeletonMarlers_cM)
            )
        print("ggg...NNN")

    def testDistancesByChromosomes(self, sFileNameOut, Genotypes, bNotAll=True):
        # test distances
        print("testDistancesByChromosomes...")
        recVova = clRecombination()
        sFileNameDistControl = sFileNameOut  # sFileName+".distControl.txt"
        f = open(sFileNameDistControl, "w")
        s = (
            "marker1"
            + "\t"
            + "marker2"
            + "\t"
            + "ctg"
            + "\t"
            + "coor1"
            + "\t"
            + "coor2"
            + "\t"
            + "dPhys"
            + "\t"
            + "r"
            + "\t"
            + "dGenetic"
            + "\t"
            + "nIndsNotMissedInBoth"
        )
        f.write(s + "\n")

        sFileName = "graphProba___1.txt"
        file = open(sFileName, "w")
        s = "#clGenomeMapComparisonGraph"
        file.write(s + "\n")
        s = "for R	a	a	a	a	a	a	a	a	a	a	a	a	a	a	a	a	a	a	a	a	a"
        file.write(s + "\n")
        s = "xlim	0	100	10"
        file.write(s + "\n")
        s = "ylim	0	100	10"
        file.write(s + "\n")
        s = "#pairs of Markers:"
        file.write(s + "\n")

        lenMax = 100
        for Chromosome in self.vChromosome:
            if lenMax < Chromosome.geneticLengthBasedOnSkeletonMarlers_cM:
                lenMax = Chromosome.geneticLengthBasedOnSkeletonMarlers_cM
        for Chromosome in self.vChromosome:
            nm = len(Chromosome.vMarker)
            print("chromosome " + Chromosome.vsName[0] + ": " + str(nm) + " markers...")
            for im1 in range(nm):
                smName1 = Chromosome.vMarker[im1].sName
                coor1 = Chromosome.vMarker[im1].coor
                marker1 = Genotypes.marker_byName_get(smName1)
                for im2 in range(im1 + 1, nm):
                    smName2 = Chromosome.vMarker[im2].sName
                    coor2 = Chromosome.vMarker[im2].coor
                    marker2 = Genotypes.marker_byName_get(smName2)
                    # for m in Genotypes.vMarker:
                    # sCtg,coor=sCtg_coor_get(m.sMarker)
                    # for m1 in Genotypes.vMarker:
                    # sCtg1,coor1=sCtg_coor_get(m1.sMarker)
                    # if sCtg1==sCtg and coor1>coor:
                    # 	nR,nN,nMissed=recVova.nnn(m.g,m1.g,False)
                    nR, nN, nMissed = recVova.nnn(marker1.g, marker2.g, False)
                    r = recVova.rML(nR, nN)
                    dGenetic = recVova.distByR(r)
                    # s=m.sMarker+"\t"+m1.sMarker+"\t"+sCtg+"\t"+str(coor)+"\t"+str(coor1)+"\t"+str(coor1-coor)+"\t"+str(r)+"\t"+str(dGenetic)
                    s = (
                        smName1
                        + "\t"
                        + smName2
                        + "\t"
                        + Chromosome.vsName[0]
                        + "\t"
                        + str(coor1)
                        + "\t"
                        + str(coor2)
                        + "\t"
                        + str(coor2 - coor1)
                        + "\t"
                        + str(r)
                        + "\t"
                        + str(dGenetic)
                        + "\t"
                        + str(nN)
                    )
                    f.write(s + "\n")

                    # points	0.04383678373577004	0.04383678373577004	col	black	#ScbnsAo_1___161534_ScbnsAo_1___161534 Contigs ScbnsAo_1 161534    Contigs ScbnsAo_1 161534 0 0.0 0 2.1734462673134964 8008924
                    x = 100 * float(coor2 - coor1) / lenMax
                    y = 100 * float(r) * 2
                    b = True
                    if bNotAll:
                        if x < float(lenMax) / 5:  # float(lenMax)/10 and r<0.1:
                            p = 0.05
                            if coor2 - coor1 < 100000 and r > 0.1:
                                p = 1
                            b = random.random() <= p
                    if b:
                        if nN > 20 or r > 0.1:
                            s = (
                                "points\t"
                                + str(x)
                                + "\t"
                                + str(y)
                                + "\tcol\tblack\t#\t"
                                + s
                            )
                            file.write(s + "\n")
        f.close()

        # segments	0.0	86.71736008849638	100	86.71736008849638	col	blue	lwd	0.01	lty	solid
        s = "segments\t0\t0\t100\t0\tcol\tblack\tlwd\t0.01\tlty\tsolid\t#x"
        file.write(s + "\n")
        s = "segments\t0\t0\t0\t100\tcol\tblack\tlwd\t0.01\tlty\tsolid\t#y"
        file.write(s + "\n")
        # text	50.0	-5	Contigs	cex	0.65	pos	1	col	black
        s = "text\t0\t-5\t0\tcex\t0.65\tpos\t1\tcol\tblack"
        file.write(s + "\n")
        s = "text\t100\t-5\t" + str(lenMax) + "\tcex\t0.65\tpos\t1\tcol\tblack"
        file.write(s + "\n")
        s = "text\t-5\t0\t0\tcex\t0.65\tpos\t2\tcol\tblack"
        file.write(s + "\n")
        s = "text\t-5\t100\t0.5\tcex\t0.65\tpos\t2\tcol\tblack"
        file.write(s + "\n")
        file.close()
        print("testDistancesByChromosomes...")

    def printToFileTextFormat(self, sFileName):
        f = open(sFileName, "w")
        s = "LG\tmarker\tiType\tcoor"
        f.write(s + "\n")
        for Chromosome in self.vChromosome:
            for Marker in Chromosome.vMarker:
                s = (
                    Chromosome.vsName[0]
                    + "\t"
                    + Marker.sName
                    + "\t"
                    + str(Marker.iType)
                    + "\t"
                    + str(Marker.coor)
                )
                f.write(s + "\n")
        f.close()

    def GenomeMapComparisonGraph_map___make(self, GenomeMapComparisonGraph):
        # GenomeMapComparisonGraph=clGenomeMapComparisonGraph()
        self.GenomeMapComparisonGraph_map = GenomeMapComparisonGraph.clMap()
        self.GenomeMapComparisonGraph_map.get_fromGeneticMap(
            GenomeMapComparisonGraph, self.sNameOfMap, self
        )

    def addName1TillSymbol_allChromosoms(self, sSymbolSplit="|"):
        if len(self.vsChrNamingVersionName) == 1:
            self.vsChrNamingVersionName.append("TillSymbol")
        for Chromosome in self.vChromosome:
            Chromosome.addName1TillSymbol(sSymbolSplit)
        self.vvsChrName_make()

    def vvsChrName_make(self):
        self.vvsChrName = []
        i_sChrNamingVersionName = 0
        for sChrNamingVersionName in self.vsChrNamingVersionName:
            vsChrName = []
            for Chromosome in self.vChromosome:
                vsChrName.append(Chromosome.vsName[i_sChrNamingVersionName])
            self.vvsChrName.append(vsChrName)
            i_sChrNamingVersionName += 1

    def renameMarkersByChangingNameOfCtg(
        self, GeneticMapWithFullChrNaming
    ):  # scaffold10p75016 -> scaffold10|size6254774___75016
        GeneticMapWithFullChrNaming.addName1TillSymbol_allChromosoms("|")
        self.vsMarkerName = []
        for Marker in self.vMarker:
            sName = Marker.sName
            vs = sName.split("p")  # scaffold10p75016 -> ["scaffold10","75016"]
            iChr = GeneticMapWithFullChrNaming.vvsChrName[1].index(vs[0])
            sNamePP = (
                GeneticMapWithFullChrNaming.vvsChrName[0][iChr] + "___" + vs[1]
            )  # scaffold10|size6254774___75016
            Marker.sName = sNamePP
            self.vsMarkerName.append(sNamePP)


class clPrivmanLab:
    def __init__(self):
        self.MyData = self.clMyData()
        # print "egegey"

        self.MyData.vFasta_start()
        self.MyData.vBlastRes_start()
        # print "egegeyPP"

    class clMyData:
        def __init__(self):
            self.dataOn117males_sPath = "C:\\Frenkel\\LTCPython\\VovaPy\\"  # "C:\\Frenkel\\Privman\\GeneticMapping\\Cataglyphis_117males\\"
            self.dataOn117males_sPPPP_compressed = (
                self.dataOn117males_sPath + "gPP.txt"
            )  # Real data compressed
            self.dataOn117males_sPPPPmm_compressed = (
                self.dataOn117males_sPath + "gPP_fromCtgWithNoGoods.txt"
            )  # Real data from bad contigsOnly
            self.dataOn117males_sPPPP_noncompressed = (
                self.dataOn117males_sPath + "gPPnc.txt"
            )  # Real data compressed
            self.dataOn117males_sPPPPmm_noncompressed = (
                self.dataOn117males_sPath + "gPPnc_fromCtgWithNoGoods.txt"
            )  # Real data from bad contigsOnly

            self.vFasta = []
            self.vsFasta_name = []

            self.vBlastRes = []

        class clFasta:
            def __init__(
                self,
                name,
                sFileNameFasta,
                sFileNameFastaNoSeq,
                indexOfFormatSequenceName,
            ):
                self.index = -1
                self.name = name
                self.sFileNameFasta = sFileNameFasta
                self.sFileNameFastaNoSeq = sFileNameFastaNoSeq
                self.indexOfFormatSequenceName = indexOfFormatSequenceName

        class clBlastRes:
            def __init__(
                self, sName, iFastaQ, iFastaDB, iFormat, mLog_eVal, sFileNameBlastRes
            ):
                self.sName = sName
                self.iFastaQ = iFastaQ
                self.iFastaDB = iFastaDB
                self.iFormat = iFormat
                self.mLog_eVal = mLog_eVal
                self.sFileNameBlastRes = sFileNameBlastRes

        def addFasta(
            self, name, sFileNameFasta, sFileNameFastaNoSeq, indexOfFormatSequenceName
        ):
            Fasta = self.clFasta(
                name, sFileNameFasta, sFileNameFastaNoSeq, indexOfFormatSequenceName
            )
            Fasta.index = len(self.vsFasta_name)
            self.vFasta.append(Fasta)
            self.vsFasta_name.append(Fasta.name)

        def iFastaByName(self, sName):
            if sName == "" or not (sName in self.vsFasta_name):
                if sName == "":
                    print('iFastaByName: sName=""')
                if not (sName in self.vsFasta_name):
                    print(
                        'sName="'
                        + sName
                        + '" is not in list: '
                        + str(self.vsFasta_name)
                    )
                return -1
            return self.vsFasta_name.index(sName)

        def vFasta_start(self):
            # https://antgenomes.org/downloads/
            # https://www.antwiki.org/wiki/Formica_selysi
            # https://metazoa.ensembl.org/Solenopsis_invicta/Info/Index
            #
            # 0. all main genes of insects that should be presented only once (amino)
            self.addFasta(
                "genes_hymenoptera_odb10",
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\tblastn\\hymenoptera_odb10.fasta",
                "",
                -1,
            )

            # 1. assembly of Tal based on Illumina (500 and 300 bp, bult by using Spades software): cimeras, a lot of DNA from bacteria
            # based on https://blast.ncbi.nlm.nih.gov/Blast.cgi# (possible up to 1Mbp, hence one by one, ~10 minutes per 1 Mbp)
            # NB! in many places by errore I used "Cnig_ng1" instead of "Cnig_gn1"
            self.addFasta(
                "Cnig_gn1",
                "C:\\Frenkel\\Privman\\Cnig_gn1\\SPades_M4B_K13-123_28_2_2017_B.scaffolds.fasta",
                "C:\\Frenkel\\Privman\\Cnig_gn1\\gg_Cnig_gn1.txt",
                0,
            )

            # 2. Vespa from Tali (not ant)
            self.addFasta(
                "Vespa",
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\scaffolds_vespa_Tali.fasta",
                "",
                -1,
            )

            # 3. GAGA from Lucas
            self.addFasta(
                "Camponotus_fellah",
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\GAGA-0221_Camponotus_fellah.fasta",
                "",
                -1,
            )

            # 4. asm (based on all PacBio reads, assemblied by canu software)
            # /cygdrive/c/Frenkel/Privman/PacBio202008/canu/asm.contigs.fasta
            self.addFasta(
                "asm",
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\asm.contigs.fasta",
                "",
                2,
            )

            # 5. selected3 (based on PacBio reads >5kbp, assemblied by canu software)
            self.addFasta(
                "selected3",
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\selected3.contigs.fasta",
                "",
                -1,
            )

            # 6. formica_selysi (downloaded from NCBI)
            self.addFasta(
                "Formica",
                "C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\genome_assemblies_genome_fasta\\ncbi-genomes-2020-05-04\\GCA_009859135.1_ASM985913v1_genomic.fna",
                "",
                -1,
            )

            # 7. assembly of Tal based on Illumina, 10x and old BacBio (a lot of cimeras)
            # NB! in many places by errore I used "Cnig_ng2" instead of "Cnig_gn2"
            self.addFasta(
                "Cnig_gn2",
                "C:\\Frenkel\\Privman\\Cnig_gn2\\scaffolds_Cnig_gn2.fasta",
                "C:\\Frenkel\\Privman\\Cnig_gn2\\gg_Cnig_gn2.txt",
                1,
            )

            # 8. Cnig_gn3a.contigs (pilon results for asm (=300-500.pilon): (see 4.) polished by Pilon using Illumina reads 300 and 500 bp
            # not based on Selected3 => longer contigs but more chimeras
            self.addFasta(
                "Cnig_gn3a.contigs",
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\300-500.pilon.fasta",
                "",
                2,
            )

            # 9. formica_exsecta_assembled_transcriptome
            self.addFasta(
                "transcriptome_formica_exsecta",
                "C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\transcriptom\\formica_exsecta_assembled_transcriptome_v1.fasta",
                "",
                -1,
            )

            # 10. Cnig_gn3.contigs (based on PacBio2020.Selected3(5,000<all<50,000), polished by Pilon using Illumina reads (300 and 500))
            self.addFasta(
                "Cnig_gn3.contigs",
                "C:\\Frenkel\\Privman\\Cnig_gn3\\Cnig_gn3.contigs.fasta",
                "",
                -1,
            )
            # /cygdrive/c/Frenkel/Privman/Cnig_gn3/Cnig_gn3.contigs.fasta

            # 11. Cnig_gn3 (based on Cnig_gn3.contigs, mapped on genetic map, unmapped, unorientated and problematic contigs are excluded)
            self.addFasta(
                "Cnig_gn3",
                "C:\\Frenkel\\LTCPython\\VovaPy\\Cnig_gn3\\20210610\\Cnig_gn3.fasta",
                "",
                -1,
            )

            # 12. Cnig_gn3a (based on Cnig_gn3a.contigs, mapped on genetic map, include also unmapped, unorientated and problematic(multimapped) contigs)
            self.addFasta(
                "Cnig_gn3a",
                "C:\\Frenkel\\LTCPython\\VovaPy\\Cnig_gn3a\\20210612\\Cnig_gn3a.fasta",
                "",
                -1,
            )

            # 13. Solenopsis_invicta_ref (TrainingData for supergene sequncing: Solenopsis invicta)
            # >JAEQMK010000001.1 Solenopsis invicta isolate M01_SB chromosome 1, whole genome shotgun sequence
            self.addFasta(
                "Solenopsis_invicta_ref",
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\referenceGenome\\JAEQMK01.1.fsa_nt\\JAEQMK01.1.fsa_nt",
                "",
                2,
            )

            # 14. Solenopsis_invicta_bb (TrainingData for supergene sequncing: Solenopsis invicta, assembly based on B males)
            # >VDGJ01000001.1 Solenopsis invicta isolate BigB_t4 chromosome 1, whole genome shotgun sequence
            self.addFasta(
                "Solenopsis_invicta_bb",
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\VDGJ01.1.fsa_nt",
                "",
                2,
            )

            # 15. Solenopsis_invicta_b (TrainingData for supergene sequncing: Solenopsis invicta, assembly based on b males)
            # >VDGK01000001.1 Solenopsis invicta isolate littleb_t2_p chromosome 1, whole genome shotgun sequence
            self.addFasta(
                "Solenopsis_invicta_b",
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\VDGK01.1.fsa_nt",
                "",
                2,
            )

            # Good version of assemblies from Eyal (2021.08.02):
            # /data/home/privman/sharedprivman/assemblies/solenopsis/littleb.fna
            # /data/home/privman/sharedprivman/assemblies/solenopsis/ref_sinvgnHB.fna  (DB)

            # 16. Cnig_gn3a.1 (used Formica)
            self.addFasta(
                "Cnig_gn3a.1",
                "C:\\Frenkel\\LTCPython\\VovaPy\\20211004\\Cnig_gn3a.1\\Cnig_gn3a.1.fasta",
                "",
                -1,
            )

            # 17. Cnig_gn3.1 (used longer Cnig_gn3a.1)
            self.addFasta(
                "Cnig_gn3.1",
                "C:\\Frenkel\\LTCPython\\VovaPy\\20211004\\Cnig_gn3.1\\Cnig_gn3.1.fasta",
                "",
                -1,
            )

            # 18. JAJUXC (Cathagliphis 1 by Darras et al 2022)
            self.addFasta(
                "JAJUXC",
                "C:\\Frenkel\\Privman\\LabMeetingPaperDiscussion\\Darras_et_al_2022_CthaglipsisGenome\\JAJUXC01.1.fsa_nt",
                "",
                -1,
            )

            # 19. JAJUXE (Cathagliphis 2 by Darras et al 2022)
            self.addFasta(
                "JAJUXE",
                "C:\\Frenkel\\Privman\\LabMeetingPaperDiscussion\\Darras_et_al_2022_CthaglipsisGenome\\JAJUXE01.1.fsa_nt",
                "",
                -1,
            )

            # 20. Camponotus japonicus
            self.addFasta(
                "Camponotus_japonicus",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\GAGA-0200_SLR-superscaffolder_final_dupsrm_filt.softMasked.fasta",
                "",
                -1,
            )
            # 21. Camponotus cf. fedtschenkoi
            self.addFasta(
                "Camponotus_fedtschenkoi",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\GAGA-0361_SLR-superscaffolder_final_dupsrm_filt.softMasked.fasta",
                "",
                -1,
            )
            # 22. Camponotus sp. (First described as nicobarensis)
            self.addFasta(
                "Camponotus_nicobarensis",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\GAGA-0362_SLR-superscaffolder_final_dupsrm_filt.softMasked.fasta",
                "",
                -1,
            )
            # 23. Camponotus singularis
            self.addFasta(
                "Camponotus_singularis",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\GAGA-0396_SLR-superscaffolder_final_dupsrm_filt.softMasked.fasta",
                "",
                -1,
            )
            # 24. Camponotus_floridanus
            self.addFasta(
                "Camponotus_floridanus",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\NCBI-0005_Camponotus_floridanus_dupsrm_filt.softMasked.fasta",
                "",
                -1,
            )

            # 25. Lasius_niger
            self.addFasta(
                "Lasius_niger",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\GAGA-0491_SLR-superscaffolder_final_dupsrm_filt.fasta",
                "",
                -1,
            )

            # 26. proteins_Lasius_niger
            self.addFasta(
                "proteins_Lasius_niger",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\GCA_001045655.1_Lnig_protein.faa",
                "",
                -1,
            )

            # 27. Solenopsis_invicta (GAGA 2021.08.09)
            self.addFasta(
                "Solenopsis_invicta",
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Solenopsis_invicta\\NCBI-0002_Solenopsis_invicta_dupsrm_filt.softMasked.fasta",
                "",
                -1,
            )

            # 5 genomes to compare:
            #
            # 26. proteins_Lasius_niger
            #
            # 6. formica_selysi
            # 3. Camponotus_fellah
            # 17. Cnig_gn3.1
            # 25. Lasius_niger
            # 27. Solenopsis_invicta

            # .
            # self.addFasta("","","",-1)
            # .
            # self.addFasta("","","",-1)
            # .
            # self.addFasta("","","",-1)
            pass

        def addBlastRes(
            self, sName, sFastaQ, sFastaDB, iFormat, mLog_eVal, sFileNameBlastRes
        ):
            iFastaQ = self.iFastaByName(sFastaQ)
            iFastaDB = self.iFastaByName(sFastaDB)
            BlastRes = self.clBlastRes(
                sName, iFastaQ, iFastaDB, iFormat, mLog_eVal, sFileNameBlastRes
            )
            self.vBlastRes.append(BlastRes)

        def vBlastRes_start(self):
            # for test only
            # self.addBlastRes("test","","",-1,-1,"C:\\Frenkel\\Privman\\Cnig_gn1\\p.txt")

            # 0. Cnig_gn1_vs_Cnig_gn2
            self.addBlastRes(
                "Cnig_gn1_vs_Cnig_gn2",
                "Cnig_gn1",
                "Cnig_gn2",
                -1,
                149,
                "C:\\Frenkel\\Privman\\Cnig_gn2\\res_Cnig_gn1_vs_Cnig_gn2_e149.out",
            )

            # 1. hymenoptera_vs_Lucas e30
            self.addBlastRes(
                "hymenoptera_vs_Lucas",
                "genes_hymenoptera_odb10",
                "Camponotus_fellah",
                -1,
                30,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\tblastn\\res_hymenoptera_vs_GAGA_e30.out",
            )

            # 2. hymenoptera_vs_Cnig_ng1
            self.addBlastRes(
                "hymenoptera_vs_Cnig_ng1",
                "genes_hymenoptera_odb10",
                "Cnig_gn1",
                -1,
                30,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\tblastn\\res_hymenoptera_vs_Cnig_ng1_e30.out",
            )

            # 3. hymenoptera_vs_asm e30
            self.addBlastRes(
                "hymenoptera_vs_asm",
                "genes_hymenoptera_odb10",
                "asm",
                -1,
                30,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\tblastn\\res_hymenoptera_vs_asm_e30.out",
            )

            # 4. hymenoptera_vs_selected3 e30
            self.addBlastRes(
                "hymenoptera_vs_selected3",
                "genes_hymenoptera_odb10",
                "selected3",
                -1,
                30,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\tblastn\\res_hymenoptera_vs_selected3_e30.out",
            )

            # 5. hymenoptera_vs_vespaTali e30
            self.addBlastRes(
                "hymenoptera_vs_vespaTali",
                "genes_hymenoptera_odb10",
                "Vespa",
                -1,
                30,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\tblastn\\res_all_hymenoptera_vs_spades_30.out",
            )

            # 6. Cnig_ng1_vs_asm e150
            self.addBlastRes(
                "Cnig_ng1_vs_asm",
                "Cnig_gn1",
                "asm",
                -1,
                150,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\res_Cnig_ng1_vs_asm.contigs_e150.out",
            )

            # 7. Cnig_ng1_vs_formica e70
            self.addBlastRes(
                "Cnig_ng1_vs_formica",
                "Cnig_gn1",
                "Formica",
                -1,
                70,
                "C:\\Frenkel\\Privman\\Cnig_gn1\\res_Cnig_gn1_vs_FormicaSelysi_e70.out",
            )

            # 8. asm_vs_formica e70
            self.addBlastRes(
                "asm_vs_formica",
                "asm",
                "Formica",
                -1,
                70,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\res_asm.contigs_vs_Formica_e70.out",
            )

            # 9. transcriptome vs Cnig_gn3a.contigs
            self.addBlastRes(
                "transcriptome_vs_Cnig_gn3a.contigs",
                "transcriptome_formica_exsecta",
                "Cnig_gn3a.contigs",
                -1,
                70,
                "C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\transcriptom\\res_300-500.pilon_vs_transcriptome_v1_e70.out",
            )

            # 10. transcriptome vs Formica
            self.addBlastRes(
                "transcriptome_vs_Formica",
                "transcriptome_formica_exsecta",
                "Formica",
                -1,
                70,
                "C:\\Frenkel\\Privman\\Cnig_gn1\\formica_selysi\\transcriptom\\res_formica_vs_transcriptome_v1_e70.out",
            )

            # 11. hymenoptera_vs_Cnig_gn3.contigs3 e30
            self.addBlastRes(
                "hymenoptera_vs_Cnig_gn3.contigs",
                "genes_hymenoptera_odb10",
                "Cnig_gn3.contigs",
                -1,
                30,
                "C:\\Frenkel\\Privman\\Cnig_gn3\\res_all_hymenoptera_vs_selected3.300-500pilon_30.out",
            )

            # 12. Cnig_gn3a.contigs_vs_formica e70
            self.addBlastRes(
                "Cnig_gn3a.contigs_vs_formica",
                "Cnig_gn3a.contigs",
                "Formica",
                -1,
                70,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\res_pilon_vs_formica_v1_e70.out",
            )

            # 13. #Cnig_gn2 = Q, Cnig_gn1=DB
            self.addBlastRes(
                "Cnig_gn2_vs_Cnig_gn1",
                "Cnig_gn2",
                "Cnig_gn1",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Cnig_gn2\\res_Cnig_gn2_vs_Cnig_gn1_e150p.out.std",
            )

            # 14. #Cnig_gn2 = Q, asm=DB
            self.addBlastRes(
                "Cnig_gn2_vs_asm",
                "Cnig_gn2",
                "asm",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Cnig_gn2\\res_Cnig_gn2_vs_Cnig_gn1_e150p.out.std",
            )

            # 15. Cnig_gn1 = Q, Cnig_gn3a.contigs=DB
            self.addBlastRes(
                "Cnig_gn1_vs_Cnig_gn3a.contigs",
                "Cnig_gn1",
                "Cnig_gn3a.contigs",
                -1,
                150,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\polish\\res_Cnig_ng1_vs_300-500.pilon_e150.out",
            )

            # 16. Cnig_ng1_vs_selected3.300-500pilon (Cnig_gn3.contigs)
            self.addBlastRes(
                "Cnig_ng1_vs_selected3.300-500pilon",
                "Cnig_gn1",
                "Cnig_gn3.contigs",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Cnig_gn3\\res_Cnig_ng1_vs_selected3.300-500pilon_e150.out",
            )

            # 17. transcriptome_vs_Cnig_gn3.contigs
            self.addBlastRes(
                "transcriptome_vs_Cnig_gn3.contigs",
                "transcriptome_formica_exsecta",
                "Cnig_gn3.contigs",
                -1,
                70,
                "C:\\Frenkel\\Privman\\Cnig_gn3\\res_selected3.300-500pilon_vs_transcriptome_v1_e70.out",
            )

            # 18. transcriptome_vs_asm
            self.addBlastRes(
                "transcriptome_vs_asm",
                "transcriptome_formica_exsecta",
                "asm",
                -1,
                70,
                "C:\\Frenkel\\Privman\\PacBio202008\\canu\\res_asm_vs_transcriptome_v1_e70.out",
            )

            # 19. Cnig_gn1_vs_Cnig_gn3
            self.addBlastRes(
                "Cnig_gn1_vs_Cnig_gn3",
                "Cnig_gn1",
                "Cnig_gn3",
                -1,
                150,
                "C:\\Frenkel\\LTCPython\\VovaPy\\Cnig_gn3\\20210610\\res_Cnig_gn1_vs_Cnig_gn3_e150.txt",
            )

            # 20. Cnig_gn1_vs_Cnig_gn3a
            self.addBlastRes(
                "Cnig_gn1_vs_Cnig_gn3a",
                "Cnig_gn1",
                "Cnig_gn3a",
                -1,
                150,
                "C:\\Frenkel\\LTCPython\\VovaPy\\Cnig_gn3a\\20210612\\res_Cnig_gn1_vs_Cnig_gn3a_e150.txt",
            )

            # 21. Solenopsis_invicta_b_vs_B
            self.addBlastRes(
                "Solenopsis_invicta_b_vs_B",
                "Solenopsis_invicta_b",
                "Solenopsis_invicta_bb",
                -1,
                150,
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_b_vs_B_e150.txt",
            )

            # 22. Solenopsis_invicta_b_vs_ref
            self.addBlastRes(
                "Solenopsis_invicta_b_vs_ref",
                "Solenopsis_invicta_b",
                "Solenopsis_invicta_ref",
                -1,
                150,
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_b_vs_Ref_e150.txt",
            )

            # 23. Solenopsis_invicta_B_vs_ref
            self.addBlastRes(
                "Solenopsis_invicta_bb_vs_ref",
                "Solenopsis_invicta_bb",
                "Solenopsis_invicta_ref",
                -1,
                150,
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_bb_vs_Ref_e150.txt",
            )

            # 24. transcriptome_vs_ref
            self.addBlastRes(
                "transcriptome_vs_ref",
                "transcriptome_formica_exsecta",
                "Solenopsis_invicta_ref",
                -1,
                70,
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_Transcriptome_vs_Ref_e70.txt",
            )

            # 25. transcriptome_vs_b
            self.addBlastRes(
                "transcriptome_vs_b",
                "transcriptome_formica_exsecta",
                "Solenopsis_invicta_b",
                -1,
                70,
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_Transcriptome_vs_b_e70.txt",
            )

            # 26. transcriptome_vs_B
            self.addBlastRes(
                "transcriptome_vs_bb",
                "transcriptome_formica_exsecta",
                "Solenopsis_invicta_bb",
                -1,
                70,
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_Transcriptome_vs_bb_e70.txt",
            )

            # 27. Cnig_gn1_vs_Cnig_gn3a.1
            self.addBlastRes(
                "Cnig_gn1_vs_Cnig_gn3a.1",
                "Cnig_gn1",
                "Cnig_gn3a.1",
                -1,
                150,
                "C:\\Frenkel\\LTCPython\\VovaPy\\20211004\\Cnig_gn3a.1\\res_Cnig_gn1_vs_Cnig_gn3a.1_e150.txt",
            )

            # 28. transcriptome vs Cnig_gn3a.1
            self.addBlastRes(
                "transcriptome_vs_Cnig_gn3a.1",
                "transcriptome_formica_exsecta",
                "Cnig_gn3a.1",
                -1,
                70,
                "C:\\Frenkel\\LTCPython\\VovaPy\\20211004\\Cnig_gn3a.1\\res_transctiptome_vs_Cnig_gn3a.1_e70.txt",
            )

            # 29. Cnig_gn1_vs_Cnig_gn3.1
            self.addBlastRes(
                "Cnig_gn1_vs_Cnig_gn3.1",
                "Cnig_gn1",
                "Cnig_gn3.1",
                -1,
                150,
                "C:\\Frenkel\\LTCPython\\VovaPy\\20211004\\Cnig_gn3.1\\res_Cnig_gn1_vs_Cnig_gn3.1_e150.txt",
            )

            # 30. transcriptome vs Cnig_gn3.1
            self.addBlastRes(
                "transcriptome_vs_Cnig_gn3.1",
                "transcriptome_formica_exsecta",
                "Cnig_gn3.1",
                -1,
                70,
                "C:\\Frenkel\\LTCPython\\VovaPy\\20211004\\Cnig_gn3.1\\res_transctiptome_vs_Cnig_gn3.1_e70.txt",
            )

            # 31. for Aparna 20211012
            self.addBlastRes(
                "Cnig_gn3_vs_Cnig_gn3.1",
                "Cnig_gn3",
                "Cnig_gn3.1",
                -1,
                150,
                "C:\\Frenkel\\LTCPython\\VovaPy\\20211004\\Cnig_gn3.1\\res_Cnig_gn3_vs_Cnig_gn3.1_e150.txt",
            )

            # 32. Cnig_gn1_vs_JAJUXC
            self.addBlastRes(
                "Cnig_gn1_vs_JAJUXC",
                "Cnig_gn1",
                "JAJUXC",
                -1,
                150,
                "C:\\Frenkel\\Privman\\LabMeetingPaperDiscussion\\Darras_et_al_2022_CthaglipsisGenome\\res_Cnig_gn1_vs_JAJUXC_e150.txt",
            )

            # 33. transcriptome vs JAJUXC
            self.addBlastRes(
                "transcriptome_vs_JAJUXC",
                "transcriptome_formica_exsecta",
                "JAJUXC",
                -1,
                70,
                "C:\\Frenkel\\Privman\\LabMeetingPaperDiscussion\\Darras_et_al_2022_CthaglipsisGenome\\res_transcriptome_vs_JAJUXC_e150.txt",
            )

            # 34. Cnig_gn1_vs_JAJUXE
            self.addBlastRes(
                "Cnig_gn1_vs_JAJUXE",
                "Cnig_gn1",
                "JAJUXE",
                -1,
                150,
                "C:\\Frenkel\\Privman\\LabMeetingPaperDiscussion\\Darras_et_al_2022_CthaglipsisGenome\\res_Cnig_gn1_vs_JAJUXE_e150.txt",
            )

            # 35. transcriptome vs JAJUXE
            self.addBlastRes(
                "transcriptome_vs_JAJUXE",
                "transcriptome_formica_exsecta",
                "JAJUXE",
                -1,
                70,
                "C:\\Frenkel\\Privman\\LabMeetingPaperDiscussion\\Darras_et_al_2022_CthaglipsisGenome\\res_transcriptome_vs_JAJUXE_e150.txt",
            )

            # 36. Cnig_gn1_vs_Solinopsis_ref
            self.addBlastRes(
                "Cnig_gn1_vs_ref",
                "Cnig_gn1",
                "Solenopsis_invicta_ref",
                -1,
                70,
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\res_Cnig_ng1_vs_Ref_e70.txt",
            )

            # 37.
            self.addBlastRes(
                "transcriptome_vs_Camponotus_fedtschenkoi",
                "transcriptome_formica_exsecta",
                "Camponotus_fedtschenkoi",
                -1,
                100,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\res_formica_transcriptome_vs_Camponotus_fedtschenkoi_e100.txt",
            )
            # 38.
            self.addBlastRes(
                "transcriptome_vs_Camponotus_fellah",
                "transcriptome_formica_exsecta",
                "Camponotus_fellah",
                -1,
                100,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\res_formica_transcriptome_vs_Camponotus_fellah_e100.txt",
            )
            # 39.
            self.addBlastRes(
                "transcriptome_vs_Camponotus_floridanus",
                "transcriptome_formica_exsecta",
                "Camponotus_floridanus",
                -1,
                100,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\res_formica_transcriptome_vs_Camponotus_floridanus_e100.txt",
            )
            # 40.
            self.addBlastRes(
                "transcriptome_vs_Camponotus_japonicus",
                "transcriptome_formica_exsecta",
                "Camponotus_japonicus",
                -1,
                100,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\res_formica_transcriptome_vs_Camponotus_japonicus_e100.txt",
            )
            # 41.
            self.addBlastRes(
                "transcriptome_vs_Camponotus_nicobarensis",
                "transcriptome_formica_exsecta",
                "Camponotus_nicobarensis",
                -1,
                100,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\res_formica_transcriptome_vs_Camponotus_nicobarensis_e100.txt",
            )
            # 42.
            self.addBlastRes(
                "transcriptome_vs_Camponotus_singularis",
                "transcriptome_formica_exsecta",
                "Camponotus_singularis",
                -1,
                100,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\res_formica_transcriptome_vs_Camponotus_singularis_e100.txt",
            )

            # 43.
            self.addBlastRes(
                "pLasius_vs_pLasius",
                "proteins_Lasius_niger",
                "proteins_Lasius_niger",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\blastres\\res_protLasius_vs_protLasius_e150.txt",
            )
            # 44.
            self.addBlastRes(
                "pLasius_vs_formica",
                "proteins_Lasius_niger",
                "Formica",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\blastres\\res_protLasius_vs_FormicaSelysi_e150.txt",
            )
            # 45.
            self.addBlastRes(
                "pLasius_vs_Camponotus",
                "proteins_Lasius_niger",
                "Camponotus_fellah",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\blastres\\res_protLasius_vs_Camponotus_fellah_e150.txt",
            )
            # 46.
            self.addBlastRes(
                "pLasius_vs_Cataglyphis",
                "proteins_Lasius_niger",
                "Cnig_gn3.1",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\blastres\\res_protLasius_vs_Cataglyphis_e150.txt",
            )
            # 47.
            self.addBlastRes(
                "pLasius_vs_Lasius",
                "proteins_Lasius_niger",
                "Lasius_niger",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\blastres\\res_protLasius_vs_Lasius_niger_e150.txt",
            )
            # 48.
            self.addBlastRes(
                "pLasius_vs_Solenopsis",
                "proteins_Lasius_niger",
                "Solenopsis_invicta",
                -1,
                150,
                "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\blastres\\res_protLasius_vs_Solenopsis_invicta_e150.txt",
            )

            # 26. proteins_Lasius_niger
            #
            # 6. formica_selysi
            # 3. Camponotus_fellah
            # 17. Cnig_gn3.1
            # 25. Lasius_niger
            # 27. Solenopsis_invicta

            # .
            # self.addBlastRes("","","",-1,-1,"")

            # .
            # self.addBlastRes("","","",-1,-1,"")
            pass

        def iBlastResIndex_get(self, sFastaQ, sFastaDB):
            iBlastResIndex = -1
            if sFastaQ == "Cnig_gn1":
                if sFastaDB == "Cnig_gn2":
                    iBlastResIndex = 0
                if sFastaDB == "asm":
                    iBlastResIndex = 6
                if sFastaDB == "Formica":
                    iBlastResIndex = 7
                if sFastaDB == "Cnig_gn3a.contigs":
                    iBlastResIndex = 15
                if sFastaDB == "Cnig_gn3.contigs":  # selected3.300-500pilon
                    iBlastResIndex = 16
                if sFastaDB == "Cnig_gn3":
                    iBlastResIndex = 19
                if sFastaDB == "Cnig_gn3a":
                    iBlastResIndex = 20
                if sFastaDB == "Cnig_gn3a.1":
                    iBlastResIndex = 27
                if sFastaDB == "Cnig_gn3.1":
                    iBlastResIndex = 29
                if sFastaDB == "JAJUXC":
                    iBlastResIndex = 32
                if sFastaDB == "JAJUXE":
                    iBlastResIndex = 34
                if sFastaDB == "Solenopsis_invicta_ref":
                    iBlastResIndex = 36
            if sFastaQ == "Cnig_gn2":
                if sFastaDB == "Cnig_gn1":
                    iBlastResIndex = 13
                if sFastaDB == "asm":
                    iBlastResIndex = 14
            if sFastaQ == "genes_hymenoptera_odb10":
                if sFastaDB == "Camponotus_fellah":
                    iBlastResIndex = 1
                if sFastaDB == "Cnig_gn1":
                    iBlastResIndex = 2
                if sFastaDB == "asm":
                    iBlastResIndex = 3
                if sFastaDB == "selected3":
                    iBlastResIndex = 4
                if sFastaDB == "Vespa":
                    iBlastResIndex = 5
                if sFastaDB == "Cnig_gn3.contigs":
                    iBlastResIndex = 11
            if sFastaQ == "asm":
                if sFastaDB == "Formica":
                    iBlastResIndex = 8
            if sFastaQ == "Cnig_gn3a.contigs":
                if sFastaDB == "Formica":
                    iBlastResIndex = 12
            if sFastaQ == "Cnig_gn3":
                if sFastaDB == "Cnig_gn3.1":
                    iBlastResIndex = 31
            if sFastaQ == "transcriptome_formica_exsecta":
                if sFastaDB == "Cnig_gn3a.contigs":
                    iBlastResIndex = 9
                if sFastaDB == "Formica":
                    iBlastResIndex = 10
                if sFastaDB == "Cnig_gn3.contigs":
                    iBlastResIndex = 17
                if sFastaDB == "asm":
                    iBlastResIndex = 18
                if sFastaDB == "Solenopsis_invicta_ref":
                    iBlastResIndex = 24
                if sFastaDB == "Solenopsis_invicta_b":
                    iBlastResIndex = 25
                if sFastaDB == "Solenopsis_invicta_bb":
                    iBlastResIndex = 26
                if sFastaDB == "Cnig_gn3a.1":
                    iBlastResIndex = 28
                if sFastaDB == "Cnig_gn3.1":
                    iBlastResIndex = 30
                if sFastaDB == "JAJUXC":
                    iBlastResIndex = 33
                if sFastaDB == "JAJUXE":
                    iBlastResIndex = 35
                if sFastaDB == "Camponotus_fedtschenkoi":
                    iBlastResIndex = 37
                if sFastaDB == "Camponotus_fellah":
                    iBlastResIndex = 38
                if sFastaDB == "Camponotus_floridanus":
                    iBlastResIndex = 39
                if sFastaDB == "Camponotus_japonicus":
                    iBlastResIndex = 40
                if sFastaDB == "Camponotus_nicobarensis":
                    iBlastResIndex = 41
                if sFastaDB == "Camponotus_singularis":
                    iBlastResIndex = 42
            if sFastaQ == "Solenopsis_invicta_b":
                if sFastaDB == "Solenopsis_invicta_bb":
                    iBlastResIndex = 21
                if sFastaDB == "Solenopsis_invicta_ref":
                    iBlastResIndex = 22
            if sFastaQ == "Solenopsis_invicta_bb":
                if sFastaDB == "Solenopsis_invicta_ref":
                    iBlastResIndex = 23
            if sFastaQ == "proteins_Lasius_niger":
                if sFastaDB == "proteins_Lasius_niger":
                    iBlastResIndex = 43
                if sFastaDB == "Formica":
                    iBlastResIndex = 44
                if sFastaDB == "Camponotus_fellah":
                    iBlastResIndex = 45
                if sFastaDB == "Cnig_gn3.1":
                    iBlastResIndex = 46
                if sFastaDB == "Lasius_niger":
                    iBlastResIndex = 47
                if sFastaDB == "Solenopsis_invicta":
                    iBlastResIndex = 48
            return iBlastResIndex

        def genotypes_get(self, indexData):
            print("genotypes_get...index=" + str(indexData))
            g = clGenotypes()
            g.sPath = ""
            g.indexData = indexData
            g.sFileName_genotypesOfGoodMarkers_inFormatChr = ""
            g.sFileName_genotypesOfNotGoodMarkers_inFormatChr = ""
            if (
                (g.indexData == 0) or (g.indexData == 1) or (g.indexData == 2)
            ):  # original vcf (117 males, markers from Cnig_ng1 contigs)
                # 0 - compressed (united markers from the same contig with the same genotype)
                # 	compress names to: NODE_98_length_95375_cov_2.80994_B1_start30529,30547,46453,46453,47979
                # 2 - don't compress the markers (for statistics and genotypes data, not in use?)
                g.sPath = self.dataOn117males_sPath
                idType = 0  # we genotype males, males are haploid, a=0 or 1

                if (g.indexData == 0) or (g.indexData == 2):
                    # input:
                    sFileNameVCF = (
                        g.sPath + "males_nofilter.vcf"
                    )  # Real data Eyal (from Cataglyphis/117males/males_nofilter.vcf)
                    # output:
                    g.sFileName_genotypesOfGoodMarkers_inFormatChr = ""

                    nOfStateMin = 5  # markers with low polymorphysm (less than 5 copies of each of 2 alleles) are not interesting
                    nReadsMinBeSureNotHeterozygote = 6  # no need
                    bPrintStatistics = False
                    bPrintGenotypes = False
                    bCompress = True
                    if g.indexData == 0:
                        bCompress = True
                        g.sFileName_genotypesOfGoodMarkers_inFormatChr = (
                            self.dataOn117males_sPPPP_compressed
                        )
                        g.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
                            self.dataOn117males_sPPPPmm_compressed
                        )
                    if g.indexData == 2:
                        bCompress = False
                        g.sFileName_genotypesOfGoodMarkers_inFormatChr = (
                            self.dataOn117males_sPPPP_noncompressed
                        )
                        g.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
                            self.dataOn117males_sPPPPmm_noncompressed
                        )
                    print("---")
                    print(g.sFileName_genotypesOfGoodMarkers_inFormatChr)
                    print(g.sFileName_genotypesOfNotGoodMarkers_inFormatChr)
                    print("---")
                    # print str(bCompress)

                    g.readFromVCF_compress_statistics_printInMultiQTLformat(
                        sFileNameVCF,
                        bPrintStatistics,
                        bPrintGenotypes,
                        bCompress,
                        nOfStateMin,
                        nReadsMinBeSureNotHeterozygote,
                        idType,
                    )
                    # end
                if (
                    g.indexData == 1
                ):  # compressed simplified data on 117 males (see g.indexData=0)
                    g.sFileName_genotypesOfGoodMarkers_inFormatChr = (
                        self.dataOn117males_sPPPP_compressed
                    )  # g.sPath+"gPP.txt"#Real data compressed (117 males, markers from Cnig_ng1 contigs, compressed)
                    g.readFromFileSimple(
                        g.sFileName_genotypesOfGoodMarkers_inFormatChr,
                        False,
                        "",
                        idType,
                        True,
                        True,
                    )
            if (
                g.indexData == 3 or g.indexData == 4
            ):  # Pnina's data for GWAS, individuals, based on assembly Cnig_ng2
                g.sPath = "C:\\Frenkel\\Privman\\GWAS\\ind\\"
                idType = 4  # we genotype females, a=0(bb),1(bB),2(BB)
                nOfStateMin = 25  # markers with too low polymorphism (on genotypes) are not interesting
                g.sFileName_genotypesOfGoodMarkers_inFormatChr = (
                    g.sPath + "gPP" + str(nOfStateMin) + ".txt"
                )

                if g.indexData == 3:
                    sFileNameVCF = g.sPath + "wholeg_snpsmax2.vcf"
                    bPrintStatistics = True
                    bPrintGenotypes = True
                    nReadsMinBeSureNotHeterozygote = 6
                    g.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
                        g.sPath + "sFileNamePPPPmm.txt"
                    )  # no need
                    bCompress = False
                    g.readFromVCF_compress_statistics_printInMultiQTLformat(
                        sFileNameVCF,
                        bPrintStatistics,
                        bPrintGenotypes,
                        bCompress,
                        nOfStateMin,
                        nReadsMinBeSureNotHeterozygote,
                        idType,
                    )
                if g.indexData == 4:
                    g.readFromFileSimple(
                        g.sFileName_genotypesOfGoodMarkers_inFormatChr,
                        False,
                        "",
                        idType,
                        True,
                        True,
                    )
            if (
                g.indexData == 5 or g.indexData == 6
            ):  # Pnina's data for GWAS, colonies, based on assembly Cnig_ng2
                g.sPath = "C:\\Frenkel\\Privman\\GWAS\\pop\\"
                idType = 4  # we genotype females, a=0(bb),1(bB),2(BB)
                nOfStateMin = 25  # markers with too low polymorphism (on genotypes) are not interesting
                g.sFileName_genotypesOfGoodMarkers_inFormatChr = (
                    g.sPath + "gPP" + str(nOfStateMin) + ".txt"
                )

                if g.indexData == 5:
                    sFileNameVCF = g.sPath + "populations.snps.vcf"
                    bPrintStatistics = True
                    bPrintGenotypes = True
                    nReadsMinBeSureNotHeterozygote = 6
                    g.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
                        g.sPath + "sFileNamePPPPmm.txt"
                    )  # no need
                    bCompress = False
                    g.readFromVCF_compress_statistics_printInMultiQTLformat(
                        sFileNameVCF,
                        bPrintStatistics,
                        bPrintGenotypes,
                        bCompress,
                        nOfStateMin,
                        nReadsMinBeSureNotHeterozygote,
                        idType,
                    )
                if g.indexData == 6:
                    g.readFromFileSimple(
                        g.sFileName_genotypesOfGoodMarkers_inFormatChr,
                        False,
                        "",
                        idType,
                        True,
                        True,
                    )
            if g.indexData == 7:
                g.sPath = "C:\\Frenkel\\Privman\\Aparna\\"  # /cygdrive/c/Frenkel/Privman/Aparna/mGWAS.txt
                idType = 4  # we genotype females, a=0(bb),1(bB),2(BB)
                # nOfStateMin=-1#markers with too low polymorphism (on genotypes) are not interesting
                g.sFileName_genotypesOfGoodMarkers_inFormatChr = (
                    g.sPath + "mGWAS.txt"
                )  # "gPP"+str(nOfStateMin)+".txt"
                g.readFromFileSimple(
                    g.sFileName_genotypesOfGoodMarkers_inFormatChr,
                    False,
                    "",
                    idType,
                    True,
                    True,
                )
            if g.indexData == 8:  # Aparna data based on asm assembly
                g.sPath = "C:\\Frenkel\\Privman\\Aparna\\"
                idType = 4  # we genotype females, a=0(bb),1(bB),2(BB)
                nOfStateMin = (
                    -1
                )  # markers with too low polymorphism (on genotypes) are not interesting
                g.sFileName_genotypesOfGoodMarkers_inFormatChr = (
                    g.sPath + "gPP" + str(nOfStateMin) + ".txt"
                )
                sFileNameVCF = g.sPath + "diploid_filtered_vcf.recode.vcf"
                bPrintStatistics = True
                bPrintGenotypes = True
                nReadsMinBeSureNotHeterozygote = 6
                g.sFileName_genotypesOfNotGoodMarkers_inFormatChr = (
                    g.sPath + "sFileNamePPPPmm.txt"
                )  # no need
                bCompress = False
                g.readFromVCF_compress_statistics_printInMultiQTLformat(
                    sFileNameVCF,
                    bPrintStatistics,
                    bPrintGenotypes,
                    bCompress,
                    nOfStateMin,
                    nReadsMinBeSureNotHeterozygote,
                    idType,
                )
            # if g.indexData==9:
            return g, g.sPath

    def SecCtgsByName(self, sName, bNoSeq=False):  # myFasta=
        iFasta = self.MyData.iFastaByName(sName)
        if iFasta >= 0:
            return self.SecCtgsByIndex(iFasta, bNoSeq)
        return clSecCtgs()

    def SecCtgsByIndex(self, iFasta, bNoSeq=False):  # myFasta=
        Fasta = self.MyData.vFasta[iFasta]
        sFileNameFasta = Fasta.sFileNameFasta
        if bNoSeq:
            if Fasta.sFileNameFastaNoSeq != "":
                sFileNameFasta = Fasta.sFileNameFastaNoSeq
        indexOfFormatSequenceName = Fasta.indexOfFormatSequenceName
        myFasta = clSecCtgs()
        myFasta.readFromFastaFile(
            sFileNameFasta, indexOfFormatSequenceName, not (bNoSeq)
        )
        return myFasta

    def currentTask_buildGeneticMap(self):  # g,sPath,vLG
        # C:\Users\user>C:\Python27\python.exe C:\Frenkel\LTCPython\VovaPy\rec.py
        #
        #'{:1.2f}'.format(self.chi2)
        sPath = "C:\Frenkel\LTCPython\VovaPy\\"
        # sPath="C:\\Frenkel\\LTCPython\\VovaPy\\" ()
        # sFileName=sPath+"g.txt"#simple example data
        # sFileNameVCF=sPath+"gg.txt"#simple example data .vcf
        # sFileNameVCF=sPath+"males_nofilter.vcf"#Real data Eyal (from Cataglyphis/117males/males_nofilter.vcf)
        # sFileNamePPPP=sPath+"gPP.txt"#Real data compressed
        # sFileNamePPPPmm=sPath+"gPP_fromCtgWithNoGoods.txt"#Real data from bad contigsOnly
        sFileNameD = sPath + "sDist.txt"  # statistics on distances
        sFileNamePajek = sPath + "netPajek.net"  # Pajek
        sFileNamePajekPP = sPath + "netPajekPP.net"  # Pajek
        sFileNamePajekPPPP = sPath + "netPajekPPPP.net"  # Pajek
        # g.readFromFileSimple(sFileName,True,'\t',idType,True,True)

        idType = 0
        bProcessVCF = False  # True#
        bMatrixOfDist = False  # True#
        bSaveNetAllInPajekFormat = False  # True#
        bExcludeNodesCausingNonLinearClusters = False  # True
        iVariant = 1
        # 0 - new data vcf
        # 1 - data already checked and clustered

        g = clGenotypes()
        if iVariant == 0:
            bProcessVCF = True  #
            bSaveNetAllInPajekFormat = True  #
            bExcludeNodesCausingNonLinearClusters = True

        # bProcessVCF=True
        if bProcessVCF:
            nOfStateMin = 5  # markers with low polymorphysm (less than 5 copies of each of 2 alleles) are not interesting
            nReadsMinBeSureNotHeterozygote = 6  # no need
            idType = 0  # we genotype males, males are haploid, a=0 or 1
            bPrintStatistics = False
            bPrintGenotypes = False
            bCompress = True
            g, sPath = self.MyData.genotypes_get(0)
        if bMatrixOfDist:  # (statistics only)
            # g.readFromFileSimple(sFileNamePPPP,False,'',idType,True,True)
            g, sPath = self.MyData.genotypes_get(1)

            # g.printStatistics(sFileNameS,True,True)
            g.printNDist(sFileNameD, True, True)
        if bSaveNetAllInPajekFormat:
            # g.readFromFileSimple(sFileNamePPPP,False,'',idType,True,True)
            g, sPath = self.MyData.genotypes_get(1)
            dMax = 0.25
            g.printNetPajek(sFileNamePajek, dMax, True, True)
        bPajekTest = False  # True
        if bPajekTest:
            net = clNetVova()
            net.test(sFileNamePajek)

        bMap = False
        bMap = True
        if bMap:
            g, sPath = self.MyData.genotypes_get(1)
            BuildingGeneticMap = clBuildingGeneticMap(g, sPath)
            BuildingGeneticMap.bExcludeNodesCausingNonLinearClusters = (
                bExcludeNodesCausingNonLinearClusters
            )
            BuildingGeneticMap.sFileNamePajek = sFileNamePajek
            BuildingGeneticMap.sFileNamePajekPP = sFileNamePajekPP
            BuildingGeneticMap.index = 0
            BuildingGeneticMap.buildGeneticMap()
            vLG = BuildingGeneticMap.vLG
            return g, sPath, vLG

    def currentTask_AttachSequences(self, g, vLG):
        # mapping of seq ctg
        bAttachSequences = True
        bAttachSequences = False
        if bAttachSequences:
            sSeqOriginalForMarkers = "Cnig_gn1"

            fasta = clSecCtgs()
            sSeqAssemblyName = "Cnig_gn1"
            sSeqAssemblyName = "asm"
            sSeqAssemblyName = "Cnig_gn3a.contigs"
            sSeqAssemblyName = "Cnig_gn3.contigs"
            # sSeqAssemblyName=""
            fasta.attachSequences(
                vLG,
                g.sFileName_genotypesOfNotGoodMarkers_inFormatChr,
                sSeqOriginalForMarkers,
                sSeqAssemblyName,
            )

    def currentTask_QTLs(self, vLG):
        if False:
            t = clTrait()
            t.singleMarkerTestAllTraitsAllMarkers(vLG)

        if False:
            self.permTestAllTraitsAllCromosomes(vLG)

    def permTestAllTraitsAllCromosomes(self, vLG):
        t = clTrait()
        sFileNameTraitsAll = (
            "C:\\Frenkel\\Privman\\QTL\\allTraits\\allTraits.Original_vova.tra"
        )
        print("permTestAllTraitsAllCromosomes...")
        vTrait = t.vTraitFromFile(sFileNameTraitsAll)
        MultiQTL = clMultiQTL()
        ChromTrait = MultiQTL.clChromTrait()
        nPermutations = 1000  # 0
        nPermutations1 = 20000
        print("nLG=" + str(len(vLG)))
        f = open("pValOfAllChr.txt", "w")
        s = "iT\ttrait\tiChr\tnMarkers\tp"
        f.write(s + "\n")
        iTrait = 0
        bPrint = False
        for Trait in vTrait:
            # iLG=0
            # for LG in vLG:
            # 	print "iLG="+str(iLG)+", nMarkers="+str(LG.nMarkers)
            if True:
                p = ChromTrait.pForRealData(vLG, Trait, nPermutations, bPrint)
                # if p<0.1:
                # 	print "Long..."
                # 	p=ChromTrait.pForRealData(vLG,Trait,nPermutations1)
                # s="trait "+Trait.name+", iLG="+str(iLG)+": p="+str(p)
                s = str(iTrait) + "\t" + Trait.name + "\t" + str(p)
                print(s)
                # s=str(iTrait)+"\t"+Trait.name+"\t"+str(iLG)+"\t"+str(LG.nMarkers)+"\t"+str(p)
                f.write(s + "\n")
                # break
                # iLG+=1
            # iTrait+=1
            # break
        f.close()
        print("permTestAllTraitsAllCromosomes...Finished")

    def renameGenesOfTal(self):
        sFileName0 = "C:\\Frenkel\\Privman\\Cnig_gn1\\annotation\\maker_master_all.log.all.gff\\Cnig_gn1___genesOnly.gff"
        sFileName1 = "C:\\Frenkel\\Privman\\Cnig_gn1\\annotation\\maker_master_all.log.all.maker.proteins.fasta"
        sFileName2 = "C:\\Frenkel\\Privman\\Cnig_gn1\\annotation\\maker_master_all.log.all.maker.transcripts.fasta"
        sFileName0pp = "C:\\Frenkel\\Privman\\Cnig_gn1\\annotation\\maker_master_all.log.all.gff\\Cnig_gn1___genesOnly_.gff"
        sFileName1pp = "C:\\Frenkel\\Privman\\Cnig_gn1\\annotation\\maker_master_all.log.all.maker.proteins_.fasta"
        sFileName2pp = "C:\\Frenkel\\Privman\\Cnig_gn1\\annotation\\maker_master_all.log.all.maker.transcripts_.fasta"

        SecCtgs = clSecCtgs()
        ctg = SecCtgs.clSecCtg()
        LineOf_gff = ctg.clLineOf_gff("")

        def inFasta(sFileName, sFileNamepp, LineOf_gff):
            f = open(sFileName, "r")
            f1 = open(sFileNamepp, "w")
            for s in f:
                if len(s) > 0:
                    if s[0] == ">":
                        k = s.find(" ")
                        if k < 0:
                            print(s)
                        else:
                            s = ">" + LineOf_gff.transformNameOfGene(s[1:k]) + s[k:]
                            f1.write(s)
                    else:
                        f1.write(s)
            f1.close
            f.close

        # NODE_1_length_992370_cov_1.03732	maker	gene	22993	24354	.	-	.	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4;Name=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4
        # NODE_1_length_992370_cov_1.03732	maker	mRNA	22993	24354	1362	-	.	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1;Parent=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4;Name=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1;_AED=0.01;_eAED=0.01;_QI=0|-1|0|1|-1|0|1|0|453
        # NODE_1_length_992370_cov_1.03732	maker	exon	22993	24354	.	-	.	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1:exon:0;Parent=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1
        # NODE_1_length_992370_cov_1.03732	maker	CDS	22993	24354	.	-	0	ID=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1:cds;Parent=maker-NODE_1_length_992370_cov_1.03732-exonerate_protein2genome-gene-0.4-mRNA-1
        def inGff(sFileName, sFileNamepp, LineOf_gff):
            f = open(sFileName, "r")
            f1 = open(sFileNamepp, "w")
            for s in f:
                # k=s.find("est_gff")
                b = len(s) > 0
                if b:
                    ss = s.split("\t")
                    b = len(ss) > 2
                    if b:
                        b = ss[2] == "gene"
                if b:
                    # ss=s.split('\t')
                    # sCtg=ss[0]
                    # sAnn=ss[8]
                    k = s.find("ID")
                    s0 = s[:k]
                    s1 = s[k:]
                    ss = s1.split(";")
                    sNew = s0
                    i = 0
                    print(s)
                    for sss in ss:
                        print(sss)
                        if i > 0:
                            sNew += ";"
                        ke = sss.find("=")
                        if ke > 0:
                            if sss[:ke] in ["ID", "Name", "Parent"]:
                                ssss = sss[(ke + 1) :]
                                sd = ""
                                kd = sss.find(":")
                                if kd > 0:
                                    sd = sss[kd:]
                                    ssss = sss[(ke + 1) : kd]
                                sssspp = LineOf_gff.transformNameOfGene(ssss)
                                sNew += sss[: (ke + 1)] + sssspp + sd
                            else:
                                sNew += sss
                        else:
                            sNew += sss
                        i += 1
                    f1.write(sNew)
            f1.close
            f.close

        inFasta(sFileName1, sFileName1pp, LineOf_gff)
        inFasta(sFileName2, sFileName2pp, LineOf_gff)
        inGff(sFileName0, sFileName0pp, LineOf_gff)

    def selectAnnotatetGenesForQTLsFromTablesOnly(self):
        sFileName = "20200531a\\assemblyFastaAndGff\\Mapped.gff"
        vq = []
        f = open(sFileName, "r")
        iRow = 0
        for s in f:
            # print s
            if iRow > 0:
                ss = s.split("\t")
                iLG = int(ss[5])
                coor = float(ss[7])
                q = [s, iLG, coor]
                vq.append(q)
            iRow += 1
        f.close()

        # sFileName="QTLsBesan.txt"
        sFileName = "QTLs.txt"
        # sFileName_="QTLsBesan_.txt"
        sFileName_ = "QTLs_.txt"
        f = open(sFileName, "r")
        f1 = open(sFileName_, "w")
        iRow = 0
        for s in f:
            # 20	2Me-C30	4									10	26	16
            # print s
            if iRow > 0:
                ss = s.split("\t")
                iQTL = int(ss[0])
                sTrait = ss[1]
                iLG = int(ss[2])
                coorMin = float(ss[11])
                coorMax = float(ss[12])
                for q in vq:
                    if q[1] == iLG and q[2] >= coorMin and q[2] <= coorMax:
                        s = str(iQTL) + "\t" + sTrait + "\t" + q[0]
                        f1.write(s)
            iRow += 1
        f.close()
        f1.close()

    def PavelSopelkinDihaploidData(self):
        sFileName = "C:\\Frenkel\\HU\\PavelSopelkin\\dihaploid\\data.txt"
        g = clGenotypes()
        g.readFromFileDiHaploidF1xF1(sFileName)

        g.printStatistics(
            sFileName + "Statistics.txt", bPrint=False, bPrintDetails=False
        )
        g.printNDist(sFileName + "StatisticsDist.txt", True, True)
        dMax = 0.25
        g.printNetPajek(sFileName + "Pajek.net", dMax, True, True)

    def GWAS_(self):
        g = clGenotypes()
        sPath = ""
        bInd = True
        bVcf = False

        sFileNameIndNamesReal = ""
        indexData = 4
        if bInd:
            if bVcf:
                indexData = 3
            else:
                indexData = 4
            sFileNameIndNamesReal = sPath + "ind_indNames.txt"
        else:
            sFileNameIndNamesReal = sPath + "pop_indNames.txt"
            if bVcf:
                indexData = 5
            else:
                indexData = 6
        g, sPath = MyData.genotypes_get(indexData)

        dMax = 3000
        sFileNameLD = sPath + "LD_nOfStateMin" + str(nOfStateMin) + ".txt"
        vIndivids = []
        if g.nIndivids > 0:
            vIndivids = g.vMarker[0].vIndividsAll_get()
        # g.printLDchi2(vIndivids,sFileNameLD,dMax)
        ReferenceGenome = clReferenceGenome("Cnig_gn2", "Cnig_gn1")
        # ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)

        DataAnts = clDataAnts(g)
        DataAnts.readFromFile_indNames(sFileNameIndNamesReal)
        bF_IT_make = False
        DataAnts.nMissingData_make(True, bF_IT_make)

        vIndivids = DataAnts.vIndividsID_Smallest_nMissingData()
        pop_ofBests = DataAnts.subpop_get(vIndivids, "best from each colony")
        if bF_IT_make:
            pop_ofBests.F_IT_make(g)
        print(pop_ofBests.sText())

        dMax = 3000
        dMax = 200000
        sFileNameLD = (
            sPath + "LD_nOfStateMin_bestIndsFromColonies_" + str(nOfStateMin) + ".txt"
        )
        # g.printLDchi2(vIndivids,sFileNameLD,dMax,False)

        tr = clTrait()
        sPath = "C:\\Frenkel\\Privman\\GWAS\\ind\\"
        sFileName = sPath + "traits_Transformation2.txt"
        # sFileName=sPath+"traits_original.txt"
        vsIndName, vsTraitName, vvbVal, vvVal = tr.readTraitDataIndsAreRowsGWAS(
            sFileName
        )
        DataAnts.vTrait_ants(vsIndName, vsTraitName, vvbVal, vvVal)
        DataAnts.printTraitsOrderingByColonyAverageOrderingByVal(sPath)
        DataAnts.saveTraitsOfQTLmalesInFormatOfGWAS(vsTraitName, sPath, 2)

    def testFastaFile(self, iFasta):
        sFileNameFasta = ""
        sFileNameOut = ""

        sFileNameFasta = self.MyData.vFasta[iFasta].sFileNameFasta
        indexOfFormatSequenceName = self.MyData.vFasta[iFasta].indexOfFormatSequenceName

        sFileNameOut = sFileNameFasta + ".vovaReport"
        if sFileNameFasta != "":
            myFasta = clSecCtgs()
            myFasta.readFromFastaFile(sFileNameFasta, indexOfFormatSequenceName)
            myFasta.printReportOnFastaFile(sFileNameOut)
        print("testFastaFile...ok")

    def summaryOfBlastResults_byIndex(self, index):
        # see def vBlastRes_start()
        sFileNameBlastResults = self.MyData.vBlastRes[index].sFileNameBlastRes
        iQ = self.MyData.vBlastRes[index].iFastaQ
        iDB = self.MyData.vBlastRes[index].iFastaDB
        sFileNameFastaQ = self.MyData.vFasta[iQ].sFileNameFasta if iQ >= 0 else ""
        sFileNameFastaDB = self.MyData.vFasta[iDB].sFileNameFasta if iDB >= 0 else ""
        indexOfFormatSequenceNameQ = (
            self.MyData.vFasta[iQ].indexOfFormatSequenceName if iQ >= 0 else -1
        )
        indexOfFormatSequenceNameDB = (
            self.MyData.vFasta[iDB].indexOfFormatSequenceName if iDB >= 0 else -1
        )

        # 2 to cut name after first " " like in blast results
        indexOfFormatSequenceNameQ = 2
        indexOfFormatSequenceNameDB = 2

        self.summaryOfBlastResults(
            sFileNameBlastResults,
            sFileNameFastaQ,
            indexOfFormatSequenceNameQ,
            sFileNameFastaDB,
            indexOfFormatSequenceNameDB,
        )

    def summaryOfBlastResults(
        self,
        sFileNameBlastResults,
        sFileNameFastaQ,
        indexOfFormatSequenceNameQ,
        sFileNameFastaDB,
        indexOfFormatSequenceNameDB,
    ):
        # output: files with statistics on sequens contigs:
        # .summary0
        # .summaryQ
        # .summaryDB
        bPrint = True

        myFastaQ = clSecCtgs()
        myFastaDB = clSecCtgs()
        myFastaQ_nsDB = []
        myFastaQ_dCovered1 = []
        myFastaQ_dCovered2andMore = []
        myFastaDB_nsQ = []
        if sFileNameFastaQ != "":
            myFastaQ.readFromFastaFile(
                sFileNameFastaQ, indexOfFormatSequenceNameQ, False
            )  # 2 to cut name after first " " like in blast results
            iCtg = 0
            for ctgQ in myFastaQ.vCtg:
                myFastaQ_nsDB.append(0)
                myFastaQ_dCovered1.append(0)
                myFastaQ_dCovered2andMore.append(0)
                # ctgQ.name=ctgQ.
                # myFastaQ.vCtgName[iCtg]=ctgQ.name
                iCtg += 1
        if sFileNameFastaDB != "":
            myFastaDB.readFromFastaFile(
                sFileNameFastaDB, indexOfFormatSequenceNameDB, False
            )  # 2 to cut name after first " " like in blast results
            iCtg = 0
            for ctgDB in myFastaDB.vCtg:
                myFastaDB_nsQ.append(0)
                # ctgDB.name=
                # myFastaDB.vCtgName[iCtg]=ctgDB.name
                iCtg += 1

        sFileNameOutput = sFileNameBlastResults + ".summary0"
        sFileNameOutput2 = sFileNameBlastResults + ".summary0parts"
        f = open(sFileNameBlastResults, "r")
        f1 = open(sFileNameOutput, "w")
        f2 = open(sFileNameOutput2, "w")
        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        fasta1 = clSecCtgs()
        myBlastRes = clBlastRes()
        dCovered1 = 0  # total length of single sDB overlap
        dCovered2andMore = 0

        bLargeBlastResFile = True

        # shapka
        LinesOfBlastRes = myBlastRes.clLinesOfBlastRes("no need", f)
        OverlapOfQuaryWithSequencesOfDB = (
            myBlastRes.clOverlapOfQuaryWithSequencesOfDB()
        )  # LinesOfBlastRes.sQ
        OverlapOfQuaryWithSequencesOfDB.processBlockOfBlastResults(LinesOfBlastRes)
        s = OverlapOfQuaryWithSequencesOfDB.s_shapka()
        print(s)
        f1.write(s + "\n")

        if bLargeBlastResFile:
            exitCode = 1
            OverlapOfQuaryWithSequencesOfDB.processBlockOfBlastResults_simple_print_shapka(
                f2
            )
            while exitCode > 0:
                OverlapOfQuaryWithSequencesOfDB = (
                    myBlastRes.clOverlapOfQuaryWithSequencesOfDB()
                )  # LinesOfBlastRes.sQ
                # overlap=OverlapOfQuaryWithSequencesOfDB.clOverlapOfQuaryWithCtgOfDB("")#sDB - ne nado here
                (
                    exitCode,
                    sFirstStringOfBlockOfFastaResult,
                ) = OverlapOfQuaryWithSequencesOfDB.processBlockOfBlastResults_simple(
                    sFirstStringOfBlockOfFastaResult, f, myFastaQ
                )
                OverlapOfQuaryWithSequencesOfDB.processBlockOfBlastResults_simple_print(
                    f2
                )

                iBlock += 1
                if iBlock % 100 == 1:
                    print("summaryOfBlastResults..." + str(iBlock))
                # print "7367"

                # OverlapOfQuaryWithSequencesOfDB=myBlastRes.clOverlapOfQuaryWithSequencesOfDB(LinesOfBlastRes.sQ)
                # OverlapOfQuaryWithSequencesOfDB.processBlockOfBlastResults(LinesOfBlastRes)

                s = OverlapOfQuaryWithSequencesOfDB.s_get()
                print(s)
                f1.write(s + "\n")
                dCovered1 += OverlapOfQuaryWithSequencesOfDB.dCovered1
                dCovered2andMore += OverlapOfQuaryWithSequencesOfDB.dCovered2andMore

                if sFileNameFastaQ != "":
                    iCtgQ = myFastaQ.vCtgName.index(OverlapOfQuaryWithSequencesOfDB.sQ)
                    myFastaQ_dCovered1[
                        iCtgQ
                    ] = OverlapOfQuaryWithSequencesOfDB.dCovered1
                    myFastaQ_dCovered2andMore[
                        iCtgQ
                    ] = OverlapOfQuaryWithSequencesOfDB.dCovered2andMore
                    myFastaQ_nsDB[iCtgQ] = len(
                        OverlapOfQuaryWithSequencesOfDB.vsDBnoRepeats
                    )
                if sFileNameFastaDB != "":
                    for sDB in OverlapOfQuaryWithSequencesOfDB.vsDBnoRepeats:
                        iCtgDB = myFastaDB.vCtgName.index(sDB)
                        myFastaDB_nsQ[iCtgDB] += 1
        else:
            # older version but with more details

            while bContinue:
                iBlock += 1
                if iBlock % 100 == 1:
                    print("summaryOfBlastResults..." + str(iBlock))
                # print "7367"
                LinesOfBlastRes = []  # to free memory
                LinesOfBlastRes = myBlastRes.clLinesOfBlastRes(
                    sFirstStringOfBlockOfFastaResult, f
                )
                # print "7366: sQ="+LinesOfBlastRes.sQ
                # print "s="+LinesOfBlastRes.LinesOfBlastRes[0].s
                # print "n="+str(len(LinesOfBlastRes.LinesOfBlastRes))
                # print "sFromOld="+sFirstStringOfBlockOfFastaResult

                sFirstStringOfBlockOfFastaResult = (
                    LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
                )
                bContinue = LinesOfBlastRes.bNotTheLastBlock
                OverlapOfQuaryWithSequencesOfDB = (
                    myBlastRes.clOverlapOfQuaryWithSequencesOfDB(LinesOfBlastRes.sQ)
                )
                OverlapOfQuaryWithSequencesOfDB.processBlockOfBlastResults(
                    LinesOfBlastRes
                )

                s = OverlapOfQuaryWithSequencesOfDB.s_get()
                print(s)
                f1.write(s + "\n")
                dCovered1 += OverlapOfQuaryWithSequencesOfDB.dCovered1
                dCovered2andMore += OverlapOfQuaryWithSequencesOfDB.dCovered2andMore

                if sFileNameFastaQ != "":
                    iCtgQ = myFastaQ.vCtgName.index(OverlapOfQuaryWithSequencesOfDB.sQ)
                    myFastaQ_dCovered1[
                        iCtgQ
                    ] = OverlapOfQuaryWithSequencesOfDB.dCovered1
                    myFastaQ_dCovered2andMore[
                        iCtgQ
                    ] = OverlapOfQuaryWithSequencesOfDB.dCovered2andMore
                    myFastaQ_nsDB[iCtgQ] = len(
                        OverlapOfQuaryWithSequencesOfDB.vsDBnoRepeats
                    )
                if sFileNameFastaDB != "":
                    for sDB in OverlapOfQuaryWithSequencesOfDB.vsDBnoRepeats:
                        iCtgDB = myFastaDB.vCtgName.index(sDB)
                        myFastaDB_nsQ[iCtgDB] += 1
        s = (
            "nQ="
            + "{:,}".format(iBlock)
            + ", dCovered="
            + "{:,}".format(dCovered1 + dCovered2andMore)
        )
        s += (
            ": dCovered1="
            + "{:,}".format(dCovered1)
            + ", dCovered2andMore="
            + "{:,}".format(dCovered2andMore)
        )
        print(s)
        f1.write(s + "\n")

        f.close()
        f1.close()
        f2.close()

        if sFileNameFastaQ != "":
            sFileNameOutput = sFileNameBlastResults + ".summaryQ"
            f1 = open(sFileNameOutput, "w")
            s = (
                "ctg"
                + "\t"
                + "len"
                + "\t"
                + "dCovered1"
                + "\t"
                + "dCovered2andMore"
                + "\t"
                + "nsDB"
                + "\t"
                + "dCovered1"
                + "\t"
                + "dCovered2andMore"
            )
            f1.write(s + "\n")
            iCtg = 0
            lSum = 0
            nCtgWithOverlap = [0, 0, 0, 0, 0, 0, 0]  # 0,1,2,3,4,>=5,>=2
            for ctg in myFastaQ.vCtg:
                l = ctg.seqLength
                lSum += l
                d1 = myFastaQ_dCovered1[iCtg]
                d2 = myFastaQ_dCovered2andMore[iCtg]
                n = myFastaQ_nsDB[iCtg]
                # nCtgWithNoOverlap+=1
                nCtgWithOverlap[min(5, n)] += 1
                if n > 1:
                    nCtgWithOverlap[6] += 1
                v1 = float(d1) / l
                v2 = float(d2) / l
                s = (
                    ctg.name
                    + "\t"
                    + str(l)
                    + "\t"
                    + str(d1)
                    + "\t"
                    + str(d2)
                    + "\t"
                    + str(n)
                    + "\t"
                    + "{:.2f}".format(v1)
                    + "\t"
                    + "{:.2f}".format(v2)
                )
                # print s
                # f1.close()
                # return
                f1.write(s + "\n")
                iCtg += 1
            n = len(myFastaQ.vCtg)
            f1.write(
                "lSum"
                + "\t"
                + "{:,}".format(lSum)
                + "\t"
                + "nCtg"
                + "\t"
                + "{:,}".format(n)
                + "\n"
            )
            for k in range(5 + 1 + 1):
                s1 = str(k)
                if k == 5:
                    s1 = ">=5"
                if k == 6:
                    s1 = ">=2"
                f1.write(
                    "nCtgWithOverlap["
                    + s1
                    + "]"
                    + "\t"
                    + "{:,}".format(nCtgWithOverlap[k])
                    + "\t"
                    + "nCtgWithOverlap["
                    + s1
                    + "]/nCtg"
                    + "\t"
                    + "{:.4f}".format(float(nCtgWithOverlap[k]) / n)
                    + "\n"
                )

            f1.write(
                "dCovered"
                + "\t"
                + "{:,}".format(dCovered1 + dCovered2andMore)
                + "\t"
                + "dCovered/Len"
                + "\t"
                + "{:.6f}".format(float(dCovered1 + dCovered2andMore) / lSum)
                + "\n"
            )
            f1.write(
                "dCovered1"
                + "\t"
                + "{:,}".format(dCovered1)
                + "\t"
                + "dCovered1/Len"
                + "\t"
                + "{:.6f}".format(float(dCovered1) / lSum)
                + "\n"
            )
            f1.write(
                "dCovered2andMore"
                + "\t"
                + "{:,}".format(dCovered2andMore)
                + "\t"
                + "dCovered2andMore/Len"
                + "\t"
                + "{:.6f}".format(float(dCovered2andMore) / lSum)
                + "\n"
            )
            # f1.write(s+"\n")

            f1.close()
        if sFileNameFastaDB != "":
            sFileNameOutput = sFileNameBlastResults + ".summaryDB"
            f1 = open(sFileNameOutput, "w")
            s = "ctg" + "\t" + "len" + "\t" + "nsQ" + "\t" + "nsQ_perMb"
            f1.write(s + "\n")
            iCtg = 0

            nNoQ = 0
            lenNoQ = 0
            lenWithQ = 0
            pNoQ = 0
            nsQ_perMb = 0
            nsQ_perMb_withQ = 0
            lSum = 0
            nsQ = 0
            for ctg in myFastaDB.vCtg:
                l = ctg.seqLength
                lSum += l
                n = myFastaDB_nsQ[iCtg]
                if n == 0:
                    nNoQ += 1
                    lenNoQ += l
                else:
                    lenWithQ += l
                nsQ += n
                k = float(n * 1000000) / l
                s = (
                    ctg.name
                    + "\t"
                    + str(l)
                    + "\t"
                    + str(n)
                    + "\t"
                    + "{:,.5f}".format(k)
                )
                f1.write(s + "\n")
                iCtg += 1
            f1.write(
                "lSum"
                + "\t"
                + "{:,}".format(lSum)
                + "\t"
                + "nCtg"
                + "\t"
                + "{:,}".format(len(myFastaDB.vCtg))
                + "\n"
            )
            f1.write(
                "nNoQ" + "\t" + "{:,}".format(nNoQ) + "\n"
            )  # number of contigs with no overlaps
            f1.write(
                "lenNoQ" + "\t" + "{:,}".format(lenNoQ) + "\n"
            )  # genome length (contigs) with no overlaps
            f1.write(
                "pNoQ" + "\t" + "{:.4f}".format(float(lenNoQ) / lSum) + "\n"
            )  # part of genome length (contigs) with no overlaps
            f1.write(
                "nsQ_perMb"
                + "\t"
                + "{:,.3f}".format(float(nsQ * 1000000) / lSum)
                + "\n"
            )
            f1.write(
                "nsQ_perMb_withQ"
                + "\t"
                + "{:,.3f}".format(float(nsQ * 1000000) / lenWithQ)
                + "\n"
            )
            f1.close()

    def attachMarkersToAnotherAssembly_simple_run(
        self, sOriginalData_set, sData_set, iVersion=0
    ):  # ReferenceGenome,MarkersWithMultiplePos=
        # g=clGenotypes()
        # sPath="C:\\Frenkel\\LTCPython\\VovaPy\\"
        # sFileNamePPPP=sPath+"gPP.txt"#Real data compressed (117 males, markers from Cnig_ng1 contigs)
        # idType=0
        # g.readFromFileSimple(sFileNamePPPP,False,'',idType,True,True)
        print("vot...")
        MyData = self.MyData
        ReferenceGenome = clReferenceGenome("Cnig_gn1", "Formica")

        #
        if (
            sOriginalData_set == "Cnig_gn1" and sData_set == "asm" and iVersion == 0
        ):  # markers from 117 males to asm
            g, sPath = MyData.genotypes_get(0)
            ReferenceGenome = clReferenceGenome("Cnig_gn1", "asm")
            MarkersWithMultiplePos = (
                ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)
            )
        if (
            sOriginalData_set == "Cnig_gn2" and sData_set == "asm" and iVersion == 0
        ):  # markers from GWAS Pnina ind to asm
            g, sPath = MyData.genotypes_get(4)
            ReferenceGenome = clReferenceGenome("Cnig_gn2", "asm")
            MarkersWithMultiplePos = (
                ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)
            )
        if (
            sOriginalData_set == "Cnig_gn2" and sData_set == "asm" and iVersion == 1
        ):  # markers from GWAS Pnina pop to asm
            g, sPath = MyData.genotypes_get(6)
            ReferenceGenome = clReferenceGenome("Cnig_gn2", "asm")
            MarkersWithMultiplePos = (
                ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)
            )
        if (
            sOriginalData_set == "Aparna" and sData_set == "asm" and iVersion == 1
        ):  # markers based on GWAS Pnina (Aparna 2021.03.21)
            g, sPath = MyData.genotypes_get(7)
            ReferenceGenome = clReferenceGenome("Cnig_gn1", "asm")
            MarkersWithMultiplePos = (
                ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)
            )
        if (
            sOriginalData_set == "Aparna" and sData_set == "asm" and iVersion == 2
        ):  # markers based on GWAS Pnina (Aparna 2021.03.21)
            g, sPath = MyData.genotypes_get(8)
        if (
            sOriginalData_set == "Cnig_gn1" and sData_set == "Cnig_gn3a.contigs"
        ):  # markers from 117 males to c/Frenkel/Privman/PacBio202008/canu/polish/300-500.pilon.fasta
            g, sPath = MyData.genotypes_get(0)
            ReferenceGenome = clReferenceGenome("Cnig_gn1", "Cnig_gn3a.contigs")
            MarkersWithMultiplePos = (
                ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)
            )
        if (
            sOriginalData_set == "Cnig_gn1" and sData_set == "Cnig_gn3.contigs"
        ):  # markers from 117 males to c/Frenkel/Privman/PacBio202008/canu/polish/300-500.pilon.fasta
            g, sPath = MyData.genotypes_get(0)
            ReferenceGenome = clReferenceGenome("Cnig_gn1", "Cnig_gn3.contigs")
            MarkersWithMultiplePos = (
                ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)
            )
        # if index==???:#markers from 117 males to <newAssembly>
        # 	g,sPath=MyData.genotypes_get(0)
        # 	ReferenceGenome=clReferenceGenome("Cnig_gn1","<newAssembly>")
        # 	MarkersWithMultiplePos=ReferenceGenome.attachMarkersToAnotherAssembly_simple(g)
        return ReferenceGenome, MarkersWithMultiplePos

    def vcfAparnaUpdate(self):
        # based on file MappingReport.txt
        print("vcfAparnaUpdate...")

        # i	ctg	len	copy	nCopies	iLG	chr	coor	posOfStartInChr	byGood	byBad	indexBlastClusters	indexBlastStars	refMapped	refUnmapped	sPosAll
        # 1	tig00002008	4285506	1	1	15	chr1	0	0	True	False	0	0			[[15,0,33847],[15,0,132270],[15,0.0,75596],[15,0.0,6645],[15,0.0,113726],[15,0.970904292855,135614],[15,0.970904292855,152992],[15,1.96103565766,164520],[15,1.96103565766,230747],[15,2.9134454062,245790],[15,4.80046180534,303577],[15,5.7713660982,341960],[15,10.6138573977,436771],[15,10.6138573977,438320],[15,11.5942809671,443361],[15,12.5747045365,448666],[15,13.6858613758,467806],[15,13.6858613758,459484],[15,13.6858613758,493231],[15,15.0372949952,590880],[15,18.9997635779,679067],[15,21.752752437,747926],[15,21.752752437,778494],[15,24.5572257696,821098],[15,24.5572257696,830204],[15,26.4442421687,887424],[15,28.9447631974,970573],[15,28.9447631974,959415],[15,28.9447631974,972643],[15,30.9057988551,985102],[15,33.0566681093,1020018],[15,33.0566681093,1001756],[15,33.6004248191,1054811],[15,33.6033328262,1067781],[15,34.1678249485,1077527],[15,35.2789817878,1109135],[15,36.3428517101,1148144],[15,36.3428517101,1135364],[15,38.3431184408,1160870],[15,40.3635953577,1218998],[15,41.3737307236,1226752],[15,43.297044765,1338110],[15,44.2586128614,1390380],[15,44.7560651612,1425561],[15,45.2586461967,1470030],[15,45.2586461967,1490393],[15,46.2790897783,1501840],[15,46.2790897783,1630502],[15,46.2790897783,1528894],[15,46.2790897783,1535335],[15,48.259546683,1666882],[15,50.1289232866,1700597],[15,51.054875675,1777081],[15,51.054875675,1866940],[15,51.054875675,1725701],[15,51.054875675,1805992],[15,52.134013297,1871860],[15,54.3894443999,1936610],[15,56.6625631037,1999157],[15,56.6625631037,2054637],[15,56.6625631037,1981898],[15,57.7615084397,2177661],[15,59.5965767822,2327854],[15,59.5965767822,2275242],[15,60.0594713239,2393280],[15,60.5311834328,2411358],[15,63.444628839,2428871],[15,64.3970385875,2447242],[15,65.5081954268,2460462],[15,65.5081954268,2454377],[15,66.619352266,2570082],[15,66.619352266,2498814],[15,67.9527646201,2610638],[15,67.9527646201,2599409],[15,67.9527646201,2665224],[15,67.9527646201,2584519],[15,69.2861769742,2704840],[15,70.2036339076,2750028],[15,71.129586296,2762579],[15,72.0911543924,2773181],[15,72.0911543924,2852379],[15,72.0911543924,2807918],[15,74.0331460582,2920236],[15,74.0331460582,2945301],[15,77.0953273202,3000377],[15,77.0953273202,2977071],[15,78.2064841595,3102265],[15,78.2064841595,3024431],[15,78.2064841595,3074575],[15,78.7551126057,3149099],[15,78.7579262865,3127341],[15,79.2817944205,3259124],[15,80.2818277559,3292783],[15,80.2818277559,3347144],[15,81.8444549311,3593302],[15,81.8444549311,3445451],[15,81.8444549311,3418075],[15,81.8444549311,3665908],[15,81.8444549311,3532197],[15,81.8444549311,3557735],[15,81.8444549311,3642596],[15,83.1265764617,3751414],[15,83.1265764617,3804608],[15,83.1265764617,3773548],[15,83.1265764617,3697331],[15,84.237733301,3942088],[15,88.9140362015,4009708],[15,92.4242491352,4089795],[15,92.4242491352,4190722],[15,95.9344620688,4236711],[15,95.9344620688,4248694],[15,95.9344620688,4244091],[15,97.0708746227,4253945]]
        sPath = "C:\\Frenkel\\LTCPython\\VovaPy\\20210322\\"
        sFileNameFastaMappingReport = sPath + "MappingReport.txt"
        MappingReport = clTableOfTxt()
        bShapka = True
        bFirstColNoNeedToRead = True
        MappingReport.readFromFile(
            sFileNameFastaMappingReport, bShapka, bFirstColNoNeedToRead
        )
        # print "nRows="+str(TableOfTxt.nRows)
        # TableOfTxt.printToFile(sFileName+".txt",bShapka)
        # iCol=3
        # textCol="tig00001985"
        # iCol=0
        # textCol="NODE_34_length_131713_cov_2.61718___48737"
        # iRows=TableOfTxt.iRows_get(textCol,iCol)
        SecCtgs = clSecCtgs()
        SecCtg = SecCtgs.clSecCtg()

        sFileVcf = "C:\\Frenkel\\Privman\\Aparna\\diploid_filtered_vcf.recode.vcf"
        f = open(sFileVcf, "r")
        f_ph = open(sFileVcf + "ph.vcf", "w")
        f_g = open(sFileVcf + "g.vcf", "w")
        f_r = open(sFileVcf + "r.txt", "w")
        m = 0
        for s in f:
            if s[0] == "#":
                f_ph.write(s)
                f_g.write(s)
            else:
                m += 1
                ss = s.split("\t")
                iRows = MappingReport.iRows_get(ss[0], 0)
                sCtg = ""
                coor_ph = int(ss[1])
                coor_g = 0
                if len(iRows) == 0:
                    sCtg = ss[0]
                    coor_g = 0
                else:
                    SecCtg = SecCtgs.clSecCtg()
                    iRow = iRows[0]
                    sCtg = MappingReport.rows[iRow].vCellText[5]  # chr
                    coor_g = MappingReport.rows[iRow].vCellText[6]  # (cM)
                    posOfStartInChr = int(MappingReport.rows[iRow].vCellText[7])
                    if len(iRows) == 1:
                        coor_ph = posOfStartInChr + coor_ph
                    else:
                        SecCtg.vPosAll_get(
                            MappingReport.rows[iRow].vCellText[14]
                        )  # iLG,coor,coorOnCntg

                        def MyFunc1(q):
                            return q.coorOnCntg

                        SecCtg.vPosAll.sort(key=MyFunc1)

                        qq = []
                        lenCtg = 0
                        for iRow in iRows:
                            lenCtg = int(MappingReport.rows[iRow].vCellText[1])
                            iLG = int(MappingReport.rows[iRow].vCellText[4])
                            sChr = MappingReport.rows[iRow].vCellText[5]  # chr
                            posOfStartInChr = int(MappingReport.rows[iRow].vCellText[7])
                            coor_g = float(
                                MappingReport.rows[iRow].vCellText[6]
                            )  # (cM)
                            q = [iLG, sChr, posOfStartInChr, coor_g, coor_ph]
                            qq.append(q)

                        def MyFunc2(q):
                            return q[0] + 0.001 * q[3] + 0.001 * 0.000000001 * q[4]

                        qq.sort(key=MyFunc2)

                        def findMy(qq, iLG):
                            for q in qq:
                                if q[0] == iLG:
                                    return q

                        n = len(SecCtg.vPosAll)

                        d = lenCtg
                        iBest = 0
                        i = 0
                        for PosAll in SecCtg.vPosAll:
                            if abs(PosAll.coorOnCntg - coor_ph) < d:
                                iBest = i
                                d = abs(PosAll.coorOnCntg - coor_ph)
                            i += 1
                        iLG = SecCtg.vPosAll[iBest].iLG
                        q = findMy(qq, iLG)
                        sCtg = q[1]
                        coor_g = SecCtg.vPosAll[iBest].coor
                        posOfStartInChr = q[2]

                        bPos = True
                        iMin = iBest
                        iMax = iBest
                        i = 0
                        for PosAll in SecCtg.vPosAll:
                            if PosAll.iLG == iLG:
                                if iMin > i:
                                    iMin = i
                                if iMax < i:
                                    iMax = i
                            i += 1
                        if iMin < iMax:
                            # print "iMin="+str(iMin)+"  iMax="+str(iMax)+"  n="+str(len(SecCtg.vPosAll))+"  iBest="+str(iBest)
                            if (
                                SecCtg.vPosAll[iMax].coor - SecCtg.vPosAll[iMin].coor
                            ) * (
                                SecCtg.vPosAll[iMax].coorOnCntg
                                - SecCtg.vPosAll[iMin].coorOnCntg
                            ) < 0:
                                bPos = False
                        if bPos:
                            coor_ph = posOfStartInChr + coor_ph
                        else:
                            coor_ph = posOfStartInChr + lenCtg - coor_ph
                        """
						if coor_ph<=SecCtg.vPosAll[0].coorOnCntg:
							coor_g=SecCtg.vPosAll[0].coor
							iLG0=SecCtg.vPosAll[0].iLG
							q=findMy(qq,iLG0)
							posOfStartInChr=q[2]
							
							iMax=0
							i=0
							for PosAll in SecCtg.vPosAll:
								if SecCtg.vPosAll[i].iLG==iLG0:
									iMax=i
								i+=1
							bPos=True
							if (SecCtg.vPosAll[iMax].coorOnCntg-SecCtg.vPosAll[i].coorOnCntg)*(SecCtg.vPosAll[iMax].coor-SecCtg.vPosAll[i].coor)<0:
								bPos=False
							if iMax<n:
								lenCtg=SecCtg.vPosAll[]
							if bPos:
								coor_ph=posOfStartInChr+coor_ph
							else:
								coor_ph=posOfStartInChr+lenCtg-coor_ph
								
						"""
                s_ph = sCtg + "\t" + str(coor_ph)
                s_g = sCtg + "\t" + str(coor_g)

                k = len(ss) - 2
                for i in range(k):
                    s_ph += "\t" + ss[i + 2]
                    s_g += "\t" + ss[i + 2]
                f_ph.write(s_ph)
                f_g.write(s_g)

                s_r = ss[0] + "\t" + ss[1] + "\t" + sCtg
                f_r.write(s_r + "\n")
                if m % 10000 == 0:
                    print(str(m))
        f.close
        f_ph.close
        f_g.close
        f_r.close
        print("vcfAparnaUpdate...Finished")

    def makeFilePosOfAllMarkersOnAllMaps(
        self, sTask, vLG, sFileName_MarkersWithMultiplePos
    ):
        MarkersWithMultiplePos = clMarkersWithMultiplePos()
        #
        MyData = self.MyData
        if sTask == "Cnig_gn3.1":
            # I. markers from Cnig_gn1 and their physical positions
            MarkersWithMultiplePos.addMapFromFasta("Cnig_gn1")
            g, sPath = MyData.genotypes_get(0)
            vsMarkerWithNameOfSeqContigInTheName = g.vsMarkerName_get()
            MarkersWithMultiplePos.addMarkersWithNameOfSeqContigInTheName(
                vsMarkerWithNameOfSeqContigInTheName, "Cnig_gn1"
            )

            # II. transcriptome markers (here names only)
            MarkersWithMultiplePos.addMarkers_FastaOnly("transcriptome_formica_exsecta")

            # additional physical maps for these (I. and II.) markers
            MarkersWithMultiplePos.addMapFromFasta("Formica")
            MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3.contigs")
            MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3a.contigs")
            #
            # I.
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1", "Formica")
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "Cnig_gn1", "Cnig_gn3.contigs"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "Cnig_gn1", "Cnig_gn3a.contigs"
            )
            #
            # II.
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Formica"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Cnig_gn3.contigs"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Cnig_gn3a.contigs"
            )

            # genetic maps
            #
            # my:
            MarkersWithMultiplePos.addGeneticMap_from_vLG(vLG)
            #
            # Besan:
            GeneticMap_Besan = clGeneticMap()
            GeneticMap_Besan.readBesan()
            MarkersWithMultiplePos.addGeneticMap_from_geneticMap(
                GeneticMap_Besan, "Besan", 3, True
            )
            #
            # update genetic map by Besan's genetic map (chromosome name and orientation):
            MarkersWithMultiplePos.addGeneticMap_with_renamed_and_reoriented_chromosomes()

            # print to file
            MarkersWithMultiplePos.printToFile(sFileName_MarkersWithMultiplePos, True)
        if sTask == "Cnig_gn3":  # old
            MarkersWithMultiplePos.addMapFromFasta("Cnig_gn1")

            g, sPath = MyData.genotypes_get(0)
            vsMarkerWithNameOfSeqContigInTheName = g.vsMarkerName_get()
            MarkersWithMultiplePos.addMarkersWithNameOfSeqContigInTheName(
                vsMarkerWithNameOfSeqContigInTheName, "Cnig_gn1"
            )
            MarkersWithMultiplePos.addMarkers_FastaOnly("transcriptome_formica_exsecta")
            #
            MarkersWithMultiplePos.addMapFromFasta("asm")
            MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3a.contigs")
            MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3.contigs")
            MarkersWithMultiplePos.addMapFromFasta("Formica")
            #
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1", "asm")
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "Cnig_gn1", "Cnig_gn3a.contigs"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "Cnig_gn1", "Cnig_gn3.contigs"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1", "Formica")
            #
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Formica"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "asm"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Cnig_gn3a.contigs"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Cnig_gn3.contigs"
            )
            # MarkersWithMultiplePos.printToFile("test.txt",True)
            # if False:
            # MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1","asm")
            # MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1","Cnig_gn3.contigs")
            # MarkersWithMultiplePos.printToFile("test.txt",True)
            # if False:#if new
            if True:
                # if False:
                bExcludeNodesCausingNonLinearClusters = False
                sPath = "C:\Frenkel\LTCPython\VovaPy\\"
                sFileNamePajek = sPath + "netPajek.net"  # Pajek
                sFileNamePajekPP = sPath + "netPajekPP.net"  # Pajek
                g, sPath = self.MyData.genotypes_get(1)
                # vLG=g.buildGeneticMap(bExcludeNodesCausingNonLinearClusters,sFileNamePajek,sFileNamePajekPP,sPath)
                BuildingGeneticMap = clBuildingGeneticMap(g, sPath)
                BuildingGeneticMap.bExcludeNodesCausingNonLinearClusters = (
                    bExcludeNodesCausingNonLinearClusters
                )
                BuildingGeneticMap.sFileNamePajek = sFileNamePajek
                BuildingGeneticMap.sFileNamePajekPP = sFileNamePajekPP
                BuildingGeneticMap.index = 0
                BuildingGeneticMap.buildGeneticMap()
                vLG = BuildingGeneticMap.vLG
                MarkersWithMultiplePos.addGeneticMap_from_vLG(vLG)

                GeneticMap_Besan = clGeneticMap()
                GeneticMap_Besan.readBesan()
                MarkersWithMultiplePos.addGeneticMap_from_geneticMap(
                    GeneticMap_Besan, "Besan", 3, True
                )

                MarkersWithMultiplePos.printToFile(
                    sFileName_MarkersWithMultiplePos, True
                )
        if sTask == "Solenopsis_invicta":
            MarkersWithMultiplePos.addMarkers_FastaOnly("transcriptome_formica_exsecta")
            MarkersWithMultiplePos.addMapFromFasta("Solenopsis_invicta_ref")
            MarkersWithMultiplePos.addMapFromFasta("Solenopsis_invicta_bb")
            MarkersWithMultiplePos.addMapFromFasta("Solenopsis_invicta_b")
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Solenopsis_invicta_ref"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Solenopsis_invicta_bb"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Solenopsis_invicta_b"
            )
            MarkersWithMultiplePos.printToFile(sFileName_MarkersWithMultiplePos, True)

    def readFilePosOfAllMarkersOnAllMaps(
        self, sFileName_MarkersWithMultiplePos
    ):  # MarkersWithMultiplePos=
        MarkersWithMultiplePos = clMarkersWithMultiplePos()
        MarkersWithMultiplePos.readFromFile(sFileName_MarkersWithMultiplePos)
        return MarkersWithMultiplePos

    def anchor_sMap_To_sMap_run(self, MarkersWithMultiplePos):
        # not in use

        sMap = "Genetic"
        sMapRef = "Besan"
        sMap = "Formica"
        sMapRef = "Genetic"
        sMap = "asm"
        sMapRef = "Genetic"
        f = open("log_" + sMap + "_" + sMapRef + ".txt", "w")
        (
            vvAssemblyElementMap,
            vvAssemblyElementMapRef,
        ) = MarkersWithMultiplePos.anchor_sMap_To_sMap(sMap, sMapRef)
        s = str(len(vvAssemblyElementMap)) + " " + str(len(vvAssemblyElementMapRef))
        print(s)
        f.write(s + "\n")

        lenOksum = 0
        lenLayerMore0sum = 0
        iPart = 0
        iMap = MarkersWithMultiplePos.iMap(sMap)
        iMapRef = MarkersWithMultiplePos.iMap(sMapRef)
        for vAssemblyElementMap in vvAssemblyElementMap:

            for AssemblyElementMap in vAssemblyElementMap:
                s1 = (
                    MarkersWithMultiplePos.vMap[iMap]
                    .vPartOfMap[AssemblyElementMap.iCtg]
                    .name
                )
                s2 = (
                    MarkersWithMultiplePos.vMap[iMapRef]
                    .vPartOfMap[AssemblyElementMap.iLG]
                    .name
                )
                s = s1 + "\t" + s2 + "\t" + AssemblyElementMap.s(False)
                print(s)
                f.write(s + "\n")
            if len(vAssemblyElementMap) > 0:
                lenOk, lenLayerMore0 = vAssemblyElementMap[0].excludeOverlapsOnSecCtg(
                    vAssemblyElementMap
                )
                lenOksum += lenOk
                lenLayerMore0sum += lenLayerMore0
                s = s1 + "\t" + str(lenOksum) + "\t" + str(lenLayerMore0sum)
                print(s)
                f.write(s + "\n")
            iPart += 1

        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Genetic","Formica")
        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Besan","Formica")
        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Besan","Genetic")
        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Formica","Genetic")
        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Formica","Besan")

        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Cnig_gn3.contigs","Genetic",0,-1)
        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Cnig_gn3.contigs","Besan",0,-1)
        # MarkersWithMultiplePos.anchor_sMap_To_sMap("Cnig_gn3.contigs","Formica",0,-1)

        return

    def anchor_contigs_to_geneticMap_and_make_my_assembly(self):
        # assembled chromosomes based on new contig assembly and genetic map based on 117 males:
        # 0. run blastn of Cnig_gn1(quary) vs. new contig assembly (db)
        # 1. add fasta file of new assembly to def vFasta_start() (in clMyData() in clPrivmanLab())
        # 2. edit function ReferenceGenome_start() in clReferenceGenome(): add if sData_set=="<newAssembly>":...
        # 3. add to attachMarkersToAnotherAssembly_simple_run() (in clPrivmanLab())
        # 4. run self.attachMarkersToAnotherAssembly_simple_run() with new index
        # 5. set sSeqOriginalForMarkers and sSeqAssemblyName in running of attachSequences()
        # 6. edit attachSequences():  (ne gotovo, poka ne nado)
        # 7. no need to edit function readCoorFromLGs() of clSecCtgs()
        # 8. specify folder of output for new assembly in clAssemblyMy()
        # 9. set in vLGwithSeq_make():
        # 9a. bNamesOfChromosomesBasedOnLength_fromLongestToShortest
        # 9b. bNamesOfChromosomesBasedOnPreviousNamingOfTheSameLinkageGroups
        # 10. run self.currentTask()

        if False:  # test only
            sData_set = "contigs_20211004"
            sFileName_MarkersWithMultiplePos = (
                "MarkersWithMultiplePos_" + sData_set + ".txt"
            )
            MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(
                sFileName_MarkersWithMultiplePos
            )
            MarkersWithMultiplePos.addGeneticMap_with_renamed_and_reoriented_chromosomes()
            MarkersWithMultiplePos.printToFile(
                sFileName_MarkersWithMultiplePos + ".txt", True
            )
            return

        # sData_set="asm"
        # sData_set="Cnig_gn3a.contigs"
        # sData_set="Cnig_gn3.contigs"
        sData_set = "contigs_20211004"
        sFileName_MarkersWithMultiplePos = (
            "MarkersWithMultiplePos_" + sData_set + ".txt"
        )
        sFileName_MarkersWithMultiplePos_pp = (
            sFileName_MarkersWithMultiplePos + ".3a.1.txt"
        )
        sFileName_MarkersWithMultiplePos_pppp = (
            sFileName_MarkersWithMultiplePos + ".3a.1_and_3.1.txt"
        )

        # bAlreadyConstructed=False
        bAlreadyConstructed = True
        if not (bAlreadyConstructed):
            # sTask="Cnig_gn3"
            vLG = []
            sTask = "Cnig_gn3.1"
            if sTask == "Cnig_gn3.1":
                # build genetic map
                g, sPath, vLG = self.currentTask_buildGeneticMap()
            self.makeFilePosOfAllMarkersOnAllMaps(
                sTask, vLG, sFileName_MarkersWithMultiplePos
            )

        bAlradyDone = True
        if not bAlradyDone:
            MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(
                sFileName_MarkersWithMultiplePos
            )

            # add map
            bAdd_assembly_3a1 = False
            bAdd_assembly_3a1 = True
            if bAdd_assembly_3a1:
                MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3a.1")
                MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                    "Cnig_gn1", "Cnig_gn3a.1"
                )
                MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                    "transcriptome_formica_exsecta", "Cnig_gn3a.1"
                )
                MarkersWithMultiplePos.printToFile(
                    sFileName_MarkersWithMultiplePos_pp, True
                )
                return
        MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(
            sFileName_MarkersWithMultiplePos_pp
        )  #

        bControlOnly = True
        if bControlOnly:
            MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3.1")
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "Cnig_gn1", "Cnig_gn3.1"
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                "transcriptome_formica_exsecta", "Cnig_gn3.1"
            )
            MarkersWithMultiplePos.printToFile(
                sFileName_MarkersWithMultiplePos_pppp, True
            )
            return

        MarkersWithMultiplePos.build_AssemblyMy()
        if False:
            # old, not working input
            AssemblyMy_3 = clAssemblyMy(
                self.SecCtgsByName("Cnig_gn3.contigs", False), "Cnig_gn3"
            )
            AssemblyMy_F = clAssemblyMy(self.SecCtgsByName("Formica", False), "F")
            AssemblyMy_asm = clAssemblyMy(
                self.SecCtgsByName("asm", False), "asm_not_polished"
            )

    def makeMarkerPositionOnNewAssembly(self):
        sData_set = "Cnig_gn3.contigs"
        sFileName_MarkersWithMultiplePos = (
            "MarkersWithMultiplePos_" + sData_set + ".txt"
        )
        MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(
            sFileName_MarkersWithMultiplePos
        )
        MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3")
        MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3a")
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1", "Cnig_gn3")
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1", "Cnig_gn3a")
        MarkersWithMultiplePos.printToFile(
            sFileName_MarkersWithMultiplePos + "_pp.txt", True
        )

    def newPositionsOfMarkersInFile_vcf(self, bServer=True):
        # $ python test.py arg1 arg2 arg3
        # Argument List: ['test.py', 'arg1', 'arg2', 'arg3']
        vsArguments = sys.argv
        sFileName_vcf = "C:\\Frenkel\\Privman\\GeneticMapping\\Cataglyphis_117males\\males_nofilter.vcf"
        sFileName_blastRes = "C:\\Frenkel\\LTCPython\\VovaPy\\Cnig_gn3\\20210610\\res_Cnig_gn1_vs_Cnig_gn3_e150.txt"
        sOutputSuffix = "PP"
        i = 0
        for sArguments in vsArguments:
            if sArguments[0] == '"' or sArguments[0] == "'":
                vsArguments = sArguments[1 : len(sArguments) - 1]
            i += 1

        if len(vsArguments) > 1:
            sFileName_vcf = vsArguments[1]
            if len(vsArguments) > 2:
                sFileName_blastRes = vsArguments[2]
                if len(vsArguments) > 3:
                    if len(vsArguments[3]) > 0:
                        ssOutputSuffix = vsArguments[3]

        if bServer:
            if len(vsArguments) < 2:
                print(
                    "Usage: python vcfCtgAndCoorBasedOnBlast.py <genotypes.vcf> <resOfBlast.out> [<outputSuffix='PP'>]"
                )
                return

            if not os.path.isfile(sFileName_vcf):
                print('vcf file "' + sFileName_vcf + '" not found')
                return
            if not os.path.isfile(sFileName_blastRes):
                print('resOfBlast file "' + sFileName_blastRes + '" not found')
                return
            # example: C:\Python27\python.exe C:\Frenkel\LTCPython\VovaPy\rec.py C:\Frenkel\Privman\GeneticMapping\Cataglyphis_117males\males_nofilter.vcf C:\Frenkel\LTCPython\VovaPy\Cnig_gn3\20210610\res_Cnig_gn1_vs_Cnig_gn3_e150.txt PP
            # scp /cygdrive/c/Frenkel/LTCPython/VovaPy/rec.py zfrenkel1@hive01.haifa.ac.il:/data/home/privman/zfrenkel1/Vova/prog/
            # mv rec.py vcfCtgAndCoorBasedOnBlast.py
            # python vcfCtgAndCoorBasedOnBlast.py males_nofilter.vcf /data/home/privman/zfrenkel1/Vova/ants/Cataglyphis_assembles/Cnig_gn1/res_Cnig_gn1_vs_Cnig_gn3_e150.txt PP

        # Genetic mapping (.vcf based on Cnig_gn1)
        # NODE_99_length_95174_cov_2.74245        88290   141351  T       G       .       PA
        #
        #
        # Pnina (.vcf based on Cnig_gn2):
        #
        # ind:
        # scaffold68726|size414   220     .       T       C       6...
        # pop:
        # scaffold68594|size415   96      340109:147:-    C       T       .       PASS    NS=
        #
        #
        # Aparna (.vcf based on asm):
        # tig00000049     15616   45:80:- T       C       .       PASS    .       GT:DP:A

        print(sFileName_vcf)
        print(sFileName_blastRes)

        myBlastRes = clBlastRes()
        vsQ = myBlastRes.vsQ_get(sFileName_blastRes)
        print("len(vsQ)=" + str(len(vsQ)))

        f = open(sFileName_blastRes, "r")
        LinesOfBlastRes = myBlastRes.clLinesOfBlastRes("no need", f)

        sFirstStringOfBlockOfFastaResult = ""
        bContinue = True
        iBlock = 0
        # markersOnRefGenome=[]
        bPrintDetails = False
        sQ_prev = ""

        bProba = False
        if bProba:
            sMarkerCtg = "NODE_129347_length_312_cov_3.72487"
            coorCtgMarker = 10

            (
                LinesOfBlastRes,
                sQ_prev,
                sFirstStringOfBlockOfFastaResult,
                bContinue,
                iBlock,
            ) = myBlastRes.LinesOfBlastRes_for_sQ(
                sMarkerCtg,
                sQ_prev,
                LinesOfBlastRes,
                f,
                sFirstStringOfBlockOfFastaResult,
                bContinue,
                iBlock,
            )
            print("LinesOfBlastRes.sQ=" + LinesOfBlastRes.sQ)

            sCtgDB, coorCtgDB, qqqq = LinesOfBlastRes.sCtgDB_coorCtgDB_qqqq_get(
                coorCtgMarker
            )
            print(
                "sCtgDB="
                + str(sCtgDB)
                + ", coorCtgDB="
                + str(coorCtgDB)
                + ", len(qqqq)="
                + str(len(qqqq))
            )

            f.close()
        if not bProba:
            print("newPositionsOfMarkersInFile_vcf....")

            vsMarkerCtg = []  # [iCtg]
            vvMarker = (
                []
            )  # [iCtg]: [vCoor,vMarker] : vMarker[iCoor]=[sCtgDB,coorCtgDB,n]
            f_vcf = open(sFileName_vcf, "r")
            for s in f_vcf:
                # if iRow%10000==0:
                # 	print "newPositionsOfMarkersInFile_vcf...iRow="+str(iRow)
                if s[0] == "#":
                    # f_vcf_pp.write(s)
                    pass
                else:
                    # iRowNotShapka+=1
                    # ss=s.split("\t")
                    ss = s.split("\t")
                    if len(ss) > 5:
                        sMarkerCtg = ss[0]
                        sCoor = ss[1]
                        if len(sMarkerCtg) > 0 and len(sCoor) > 0:
                            coorCtgMarker = int(sCoor)
                            iMarkerCtg = len(vsMarkerCtg)
                            if sMarkerCtg in vsMarkerCtg:
                                iMarkerCtg = vsMarkerCtg.index(sMarkerCtg)
                            else:
                                vsMarkerCtg.append(sMarkerCtg)
                                vvMarker.append([[], []])
                            if not (coorCtgMarker in vvMarker[iMarkerCtg][0]):
                                vvMarker[iMarkerCtg][0].append(coorCtgMarker)
                                vvMarker[iMarkerCtg][1].append(["", -1, 0])
            f_vcf.close()
            print("newPositionsOfMarkersInFile_vcf....I.")

            # update vvMarker[iMarkerCtg][1][iCoor]
            sFirstStringOfBlockOfFastaResult = ""
            bContinue = True
            iBlock = 0
            while bContinue:
                iBlock += 1
                if bPrintDetails:
                    if iBlock % 100 == 1:
                        pass
                LinesOfBlastRes = myBlastRes.clLinesOfBlastRes(
                    sFirstStringOfBlockOfFastaResult, f
                )
                if LinesOfBlastRes.sQ in vsMarkerCtg:
                    iMarkerCtg = vsMarkerCtg.index(LinesOfBlastRes.sQ)
                    LinesOfBlastRes.makeArrays()
                    iCoor = 0
                    for coorCtgMarker in vvMarker[iMarkerCtg][0]:
                        (
                            sCtgDB,
                            coorCtgDB,
                            qqqq,
                        ) = LinesOfBlastRes.sCtgDB_coorCtgDB_qqqq_get(coorCtgMarker)
                        vvMarker[iMarkerCtg][1][iCoor] = [sCtgDB, coorCtgDB, len(qqqq)]
                        iCoor += 1
                sFirstStringOfBlockOfFastaResult = (
                    LinesOfBlastRes.sFirstStringOfNextBlockOfFastaResult
                )
                bContinue = LinesOfBlastRes.bNotTheLastBlock
            f.close()
            print("newPositionsOfMarkersInFile_vcf....II.")

            f_vcf = open(sFileName_vcf, "r")
            f_vcf_pp = open(sFileName_vcf + "_" + sOutputSuffix + ".vcf", "w")
            f_log = open(sFileName_vcf + "_" + sOutputSuffix + ".log", "w")
            iRow = 0
            iRowNotShapka = 0
            iMarker = 0
            iCtgQ_prev = -1
            f_log.write(
                "iRow"
                + "\t"
                + "iMarker"
                + "\t"
                + "sMarkerCtgQ"
                + "\t"
                + "coorQ"
                + "\t"
                + "sMarkerCtgDB"
                + "\t"
                + "coorDB"
                + "\t"
                + "nCtgDB"
                + "\n"
            )
            for s in f_vcf:
                if iRow % 10000 == 0:
                    print("newPositionsOfMarkersInFile_vcf...iRow=" + str(iRow))
                if s[0] == "#":
                    f_vcf_pp.write(s)
                else:
                    iRowNotShapka += 1
                    ss = s.split("\t")
                    if len(ss) > 5:
                        sMarkerCtg = ss[0]
                        if len(sMarkerCtg) > 0:
                            """
                            iCtgQ=vsQ.index(sMarkerCtg) if (sMarkerCtg in vsQ) else -1
                            print "iCtgQ("+sMarkerCtg+")="+str(iCtgQ)+" iCtgQ="+str(iCtgQ)+" iCtgQ_prev="+str(iCtgQ_prev)
                            if iCtgQ<iCtgQ_prev and iCtgQ>=0:
                                    #reopen file with blast results
                                    print "reopen"
                                    f.close()
                                    sFirstStringOfBlockOfFastaResult=""
                                    bContinue=True
                                    iBlock=0
                                    f=open(sFileName_blastRes,'r')
                            if iCtgQ>=0:
                                    iCtgQ_prev=iCtgQ

                            iMarker+=1
                            sCoor=ss[1]
                            if len(sCoor)>0:
                                    coorCtgMarker=int(sCoor)
                                    LinesOfBlastRes,sQ_prev,sFirstStringOfBlockOfFastaResult,bContinue,iBlock=myBlastRes.LinesOfBlastRes_for_sQ(sMarkerCtg,sQ_prev,LinesOfBlastRes,f,sFirstStringOfBlockOfFastaResult,bContinue,iBlock)
                                    sCtgDB,coorCtgDB,qqqq=LinesOfBlastRes.sCtgDB_coorCtgDB_qqqq_get(coorCtgMarker)
                                    sPP="not found"+"\t"+"no"
                                    if len(sCtgDB)>0:
                                            sPP=sCtgDB+"\t"+str(coorCtgDB)
                                            k=len(ss)-2
                                            for i in range(k):
                                                    sPP+="\t"+ss[i+2]
                                            f_vcf_pp.write(sPP)
                                    f_log.write(str(iRow)+"\t"+str(iMarker)+"\t"+sMarkerCtg+"\t"+sCoor+"\t"+sCtgDB+"\t"+str(coorCtgDB)+"\t"+str(len(qqqq))+"\n")
                            else:
                                    f_log.write("ERROR 2 in line "+str(iRow)+"\n")
                                    f_log.write(s)
                            """
                            sCoor = ss[1]
                            if len(sCoor) > 0:
                                iMarker += 1
                                coorCtgMarker = int(sCoor)
                                iMarkerCtg = vsMarkerCtg.index(sMarkerCtg)
                                iCoor = vvMarker[iMarkerCtg][0].index(coorCtgMarker)
                                sCtgDB = vvMarker[iMarkerCtg][1][iCoor][0]
                                coorCtgDB = vvMarker[iMarkerCtg][1][iCoor][1]
                                n = vvMarker[iMarkerCtg][1][iCoor][2]
                                sPP = "not found" + "\t" + "no"
                                if n > 0:
                                    sPP = sCtgDB + "\t" + str(coorCtgDB)
                                    k = len(ss) - 2
                                    for i in range(k):
                                        sPP += "\t" + ss[i + 2]
                                    f_vcf_pp.write(sPP)
                                f_log.write(
                                    str(iRow)
                                    + "\t"
                                    + str(iMarker)
                                    + "\t"
                                    + sMarkerCtg
                                    + "\t"
                                    + sCoor
                                    + "\t"
                                    + sCtgDB
                                    + "\t"
                                    + str(coorCtgDB)
                                    + "\t"
                                    + str(n)
                                    + "\n"
                                )
                            else:
                                f_log.write("ERROR 2 in line " + str(iRow) + "\n")
                                f_log.write(s)
                        else:
                            f_log.write("ERROR 1 in line " + str(iRow) + "\n")
                            f_log.write(s)
                    else:
                        f_log.write("ERROR 0 in line " + str(iRow) + "\n")
                        f_log.write(s)
                iRow += 1
            f_vcf.close()
            f_vcf_pp.close()
            f_log.close()
        f.close()
        print("newPositionsOfMarkersInFile_vcf....Finished")
        return

    def select_Chr16(self):
        print("select_Chr16...")
        vi = [13, 14, 15]
        vsPartOfSeqName = ["00016.1"]
        sDobaffka = "chr16"
        for i in vi:
            sFileNameFastaQ = self.MyData.vFasta[i].sFileNameFasta
            myFastaQ = clSecCtgs()
            myFastaQ.printSeqsBasedOnListOfName(
                vsPartOfSeqName, sDobaffka, sFileNameFastaQ
            )
            print("select_Chr16..." + str(i) + " of " + str(len(vi)))
        print("select_Chr16...")

    def aaaaa(self):
        sFileName = "C:\\Frenkel\\Privman\\Aparna\\20211012\\mmm.txt"
        sFileNamePP = sFileName + "pp.txt"
        MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(sFileName)
        MarkersWithMultiplePos.addMapFromFasta("Cnig_gn3")
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn3", "Cnig_gn3.1")
        MarkersWithMultiplePos.printToFile(sFileNamePP, True)

    def print_bim_file_forPnina_run(self):
        sData_set = "contigs_20211004"
        sFileName_MarkersWithMultiplePos = (
            "MarkersWithMultiplePos_" + sData_set + ".txt"
        )
        sFileName_MarkersWithMultiplePos_pppp = (
            sFileName_MarkersWithMultiplePos + ".3a.1_and_3.1.txt"
        )
        MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(
            sFileName_MarkersWithMultiplePos_pppp
        )
        MarkersWithMultiplePos.print_bim_file_forPnina()

    def printReportOnFastaFile_run(
        self, sFileNameFasta, sFileNameOut="", indexOfFormatSequenceName=-1
    ):
        if sFileNameOut == "":
            sFileNameOut = sFileNameFasta + ".reportVova.txt"
        myFasta = clSecCtgs()
        myFasta.readFromFastaFile(sFileNameFasta, indexOfFormatSequenceName)
        myFasta.printReportOnFastaFile(sFileNameOut)

    def add_JAJUXC_JAJUXE(self):
        sFileName = "C:\\Frenkel\\LTCPython\\VovaPy\\MarkersWithMultiplePos_contigs_20211004.txt.3a.1_and_3.1.txt"
        MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(sFileName)
        MarkersWithMultiplePos.addMapFromFasta("JAJUXC")
        MarkersWithMultiplePos.addMapFromFasta("JAJUXE")
        MarkersWithMultiplePos.addMapFromFasta("Solenopsis_invicta_ref")
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1", "JAJUXC")
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            "transcriptome_formica_exsecta", "JAJUXC"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults("Cnig_gn1", "JAJUXE")
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            "transcriptome_formica_exsecta", "JAJUXE"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            "Cnig_gn1", "Solenopsis_invicta_ref"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            "transcriptome_formica_exsecta", "Solenopsis_invicta_ref"
        )
        sFileNamePP = (
            "C:\\Frenkel\\LTCPython\\VovaPy\\MarkersWithMultiplePos_JAJUXC_JAJUXE.txt"
        )
        MarkersWithMultiplePos.printToFile(sFileNamePP, True)

    def testAssemblyByLDMap(self):
        g = clGenotypes()
        sFileNameVCF = "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\669di_minmaf0.01maxmis0.7minDP6.recode.vcf"
        g.readFromVCF_compress_statistics_printInMultiQTLformat(
            sFileNameVCF,
            bPrintStatistics=True,
            bPrintGenotypes=False,
            bCompress=False,
            nOfStateMin=150,
            nReadsMinBeSureNotHeterozygote=6,
            idType=4,
        )
        vIndivids = g.vMarker[0].vIndividsAll_get()
        nm = len(g.vMarker)
        im = 0
        i = 0
        sFileName = "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\LD_allSignif.txt"
        sFileName1 = "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\LD_farOnly.txt"
        f = open(sFileName, "w")
        f1 = open(sFileName1, "w")

        s = (
            "i"
            + "\t"
            + "ii"
            + "\t"
            + "m1Cnig_gn3.1_part"
            + "\t"
            + "m1Cnig_gn3.1_pos"
            + "\t"
            + "m2Cnig_gn3.1_part"
            + "\t"
            + "m2Cnig_gn3.1_pos"
            + "\t"
            + "X2"
            + "\t"
            + "p-val"
        )
        f.write(s + "\n")
        f1.write(s + "\n")

        for m in g.vMarker:
            ii = 0
            # for im1 in range(im+1,nm):
            for im1 in range(nm):
                m1 = g.vMarker[im1]
                X2, df, nExpMin, LD, LD_tag, r, p = m.compareWithMarkerLDchi2(
                    m1, vIndivids
                )  # X2,df,nExpMin, LD, LD_tag, r, p=
                # if (X2>2 and nExpMin>=5)or(p<0.01):
                if ((X2 > 40 and nExpMin >= 10) or (p < 0.0000001)) and (im != im1):
                    s = (
                        str(i)
                        + "\t"
                        + str(ii)
                        + "\t"
                        + m.sChr
                        + "\t"
                        + str(m.pos)
                        + "\t"
                        + m1.sChr
                        + "\t"
                        + str(m1.pos)
                        + "\t"
                        + str(X2)
                        + "\t"
                        + str(p)
                    )
                    print(s)
                    f.write(s + "\n")
                    if m.sChr != m1.sChr or abs(m.pos - m1.pos) > 3000000:
                        f1.write(s + "\n")
                    i += 1
                    ii += 1
            im += 1
        f.close
        f1.close

    def testAssemblyByGeneticMap(self):

        # read position of markers on physical and genetic maps
        sFileName = "C:\\Frenkel\\LTCPython\\VovaPy\\MarkersWithMultiplePos_contigs_20211004.txt.3a.1_and_3.1.txt"
        MarkersWithMultiplePos = self.readFilePosOfAllMarkersOnAllMaps(sFileName)
        iMapS = MarkersWithMultiplePos.iMap("Cnig_gn3.1")
        iMapG = MarkersWithMultiplePos.iMap("mapGenetic")

        if False:
            # test
            for PartOfMap in MarkersWithMultiplePos.vMap[iMapS].vPartOfMap:
                print(
                    PartOfMap.name
                    + " "
                    + str(PartOfMap.length)
                    + " "
                    + str(PartOfMap.lengthSumOfPrev)
                )
            for PartOfMap in MarkersWithMultiplePos.vMap[iMapG].vPartOfMap:
                print(
                    PartOfMap.name
                    + " "
                    + str(PartOfMap.length)
                    + " "
                    + str(PartOfMap.lengthSumOfPrev)
                )

        class clvMarkerWithPosGS:
            # extract markers: with unique physical position or with position on the genetic map
            class clMarkerWithPosGS:
                def __init__(
                    self,
                    sMarkerName,
                    iPartG,
                    sPartG,
                    coorG,
                    iTypeG,
                    iPartS,
                    sPartS,
                    coorS,
                    xS,
                    iTypeS,
                ):
                    self.sMarkerName = sMarkerName
                    self.iPartG = iPartG
                    self.sPartG = sPartG
                    self.coorG = coorG
                    self.iTypeG = iTypeG

                    self.iPartS = iPartS
                    self.sPartS = sPartS
                    self.coorS = coorS
                    self.xS = xS  # comulative on all previous chromosoms (like in Manhatten plot)
                    self.iTypeS = iTypeS

                def sShapka_get(self, sDobaffka=""):
                    s = "mName" + sDobaffka
                    s += (
                        "\t"
                        + "ichr"
                        + sDobaffka
                        + "\t"
                        + "chrG"
                        + sDobaffka
                        + "\t"
                        + "coorG"
                        + sDobaffka
                        + "\t"
                        + "iTypeG"
                        + sDobaffka
                    )
                    s += (
                        "\t"
                        + "ichrS"
                        + sDobaffka
                        + "\t"
                        + "chrS"
                        + sDobaffka
                        + "\t"
                        + "coorS"
                        + sDobaffka
                        + "\t"
                        + "coorSS"
                        + sDobaffka
                        + "\t"
                        + "iTypeS"
                        + sDobaffka
                    )
                    return s

                def s_get(self):
                    s = self.sMarkerName
                    s += (
                        "\t"
                        + str(self.iPartG)
                        + "\t"
                        + self.sPartG
                        + "\t"
                        + str(self.coorG)
                        + "\t"
                        + str(self.iTypeG)
                    )
                    s += (
                        "\t"
                        + str(self.iPartS)
                        + "\t"
                        + self.sPartS
                        + "\t"
                        + str(self.coorS)
                        + "\t"
                        + str(self.xS)
                        + "\t"
                        + str(self.iTypeS)
                    )
                    return s

            def __init__(self, MarkersWithMultiplePos, iMapG, iMapS):
                self.vMarkerWithPosS = (
                    []
                )  # no need to take position on genetic map into account
                self.vMarkerWithPosGS = []
                self.iMapG = iMapG
                self.iMapS = iMapS
                self.MarkersWithMultiplePos = MarkersWithMultiplePos
                self.read_from_MarkersWithMultiplePos()
                self.del_positionsS()
                self.estimatePosS_basedOnPosG()

            def read_from_MarkersWithMultiplePos(self):
                for m in self.MarkersWithMultiplePos.vMarkerWithMultiplePos:
                    sMarkerName = m.sName
                    iPartG = -1
                    sPartG = ""
                    coorG = -1
                    iTypeG = -1
                    #
                    iPartS = -1
                    sPartS = ""
                    coorS = -1
                    xS = -1
                    iTypeS = -1

                    if len(m.vvPosOnMap[self.iMapG]) == 1:
                        PosOnMapG = m.vvPosOnMap[self.iMapG][0]

                        iPartG = PosOnMapG.iPart
                        partG = self.MarkersWithMultiplePos.vMap[self.iMapG].vPartOfMap[
                            iPartG
                        ]
                        sPartG = partG.name
                        coorG = PosOnMapG.coor
                        iTypeG = PosOnMapG.iType

                    if len(m.vvPosOnMap[self.iMapS]) == 1:
                        PosOnMapS = m.vvPosOnMap[self.iMapS][0]

                        iPartS = PosOnMapS.iPart
                        partS = self.MarkersWithMultiplePos.vMap[self.iMapS].vPartOfMap[
                            iPartS
                        ]
                        sPartS = partS.name
                        coorS = PosOnMapS.coor
                        xS = partS.lengthSumOfPrev + PosOnMapS.coor
                        iTypeS = abs(PosOnMapS.iType)  # no need info on orientation
                    if iPartS >= 0:
                        MarkerWithPosS = self.clMarkerWithPosGS(
                            sMarkerName,
                            iPartG,
                            sPartG,
                            coorG,
                            iTypeG,
                            iPartS,
                            sPartS,
                            coorS,
                            xS,
                            iTypeS,
                        )
                        self.vMarkerWithPosS.append(MarkerWithPosS)
                    if iPartG >= 0 or iPartS >= 0:
                        MarkerWithPosGS = self.clMarkerWithPosGS(
                            sMarkerName,
                            iPartG,
                            sPartG,
                            coorG,
                            iTypeG,
                            iPartS,
                            sPartS,
                            coorS,
                            xS,
                            iTypeS,
                        )
                        self.vMarkerWithPosGS.append(MarkerWithPosGS)
                    """
					if len(m.vvPosOnMap[iMapS])==1:
						bMapped=False
							PosOnMapS=m.vvPosOnMap[iMapS][0]
							partS=MarkersWithMultiplePos.vMap[iMapS].vPartOfMap[PosOnMapS.iPart]
							if partS.name==partG.name:
								xS=partS.lengthSumOfPrev+PosOnMapS.coor
								#        0        1              2          3              4  5               6           7             8   9
								qMapped=[m.sName,PosOnMapG.iPart,partG.name,PosOnMapG.coor,xG,PosOnMapG.iType,partS.name,PosOnMapS.coor,xS,PosOnMapS.iType]
								bMapped=True
						if not bMapped:
							qMapped=[m.sName,PosOnMapG.iPart,partG.name,PosOnMapG.coor,xG,PosOnMapG.iType,partG.name,-1,-1,-1]
						#m.sMarker
						#print(str(qMapped))
						vqMapped.append(qMapped)
						n+=1
					"""
                print(
                    "nS="
                    + str(len(self.vMarkerWithPosS))
                    + ", nGS="
                    + str(len(self.vMarkerWithPosGS))
                )

            def del_positionsS(self):
                # no need markers from unmapped contigs where no genetic markers from the genetic map
                vMarkerWithPosGS_notOnChrS = []
                vOk = []
                for MarkerWithPosGS in self.vMarkerWithPosGS:
                    if MarkerWithPosGS.iPartS >= 0:
                        if (
                            MarkerWithPosGS.sPartS[0:3] != "chr"
                            and MarkerWithPosGS.iPartG < 0
                        ):
                            vMarkerWithPosGS_notOnChrS.append(MarkerWithPosGS)
                        else:
                            vOk.append(MarkerWithPosGS)
                    else:
                        vOk.append(MarkerWithPosGS)

                # def MyFunc11(MarkerWithPosGS):#sort by physical pos
                # 	return MarkerWithPosGS.iPartS*10000+MarkerWithPosGS.coorS
                # vMarkerWithPosGS_notOnChrS.sort(key=MyFunc11)

                n = len(self.MarkersWithMultiplePos.vMap[self.iMapS].vsPartName)
                vG = []
                vS = []
                for i in range(n):
                    vG.append([])
                    vS.append([])
                for MarkerWithPosGS in self.vMarkerWithPosGS:
                    if MarkerWithPosGS.iPartG >= 0 and MarkerWithPosGS.iPartS >= 0:
                        vG[MarkerWithPosGS.iPartS].append(MarkerWithPosGS)
                for MarkerWithPosGS in vMarkerWithPosGS_notOnChrS:
                    vS[MarkerWithPosGS.iPartS].append(MarkerWithPosGS)
                self.vMarkerWithPosGS = []
                for i in range(n):
                    if len(vG[i]) > 0:
                        MarkerWithPosGS_ok = vG[i][0]
                        for MarkerWithPosGS in vS[i]:
                            MarkerWithPosGS.iPartS = -1
                            MarkerWithPosGS.sPartS = ""
                            MarkerWithPosGS.coorS = -1
                            MarkerWithPosGS.xS = -1
                            MarkerWithPosGS.iTypeS = -1

                            MarkerWithPosGS.iPartG = MarkerWithPosGS_ok.iPartG
                            MarkerWithPosGS.sPartG = MarkerWithPosGS_ok.sPartG
                            MarkerWithPosGS.coorG = MarkerWithPosGS_ok.coorG
                            MarkerWithPosGS.iTypeG = 10
                            self.vMarkerWithPosGS.append(MarkerWithPosGS)
                for MarkerWithPosGS in vOk:
                    self.vMarkerWithPosGS.append(MarkerWithPosGS)
                print("nGS_LG=" + str(len(self.vMarkerWithPosGS)))

            def estimatePosS_basedOnPosG(
                self,
            ):  # for markers with position on the genetic map only
                n = len(
                    self.MarkersWithMultiplePos.vMap[self.iMapG].vsPartName
                )  # number of chromosomes
                vvG = []
                for i in range(n):
                    vvG.append([])
                for MarkerWithPosGS in self.vMarkerWithPosGS:
                    if MarkerWithPosGS.iPartG >= 0:
                        vvG[MarkerWithPosGS.iPartG].append(MarkerWithPosGS)

                # sort by genetic
                def MyFunc11(MarkerWithPosGS):
                    return MarkerWithPosGS.coorG

                myMath = clVovaMath()
                for i in range(n):
                    vvG[i].sort(key=MyFunc11)
                    iq = 0

                    coorS = -1
                    xS = -1
                    iPartS = -1
                    sPartS = ""
                    j = -1  # first missed index
                    k = -1  # last non-missed

                    for MarkerWithPosGS in vvG[i]:
                        if MarkerWithPosGS.iTypeS >= 0:
                            iPartS = MarkerWithPosGS.iPartS
                            sPartS = MarkerWithPosGS.sPartS
                            coorS = MarkerWithPosGS.coorS
                            xS = MarkerWithPosGS.xS
                            if j >= 0:
                                if k < 0:
                                    for ii in range(j, iq):
                                        MarkerWithPosGS1 = vvG[i][ii]
                                        MarkerWithPosGS1.iPartS = iPartS
                                        MarkerWithPosGS1.sPartS = sPartS
                                        MarkerWithPosGS1.coorS = coorS
                                        MarkerWithPosGS1.xS = xS
                                        MarkerWithPosGS1.iTypeS = -2
                                else:
                                    MarkerWithPosGS_k = vvG[i][k]
                                    coorS0 = MarkerWithPosGS_k.coorS
                                    xS0 = MarkerWithPosGS_k.xS
                                    g0 = MarkerWithPosGS_k.coorG
                                    g = MarkerWithPosGS.coorG
                                    for ii in range(j, iq):
                                        MarkerWithPosGS1 = vvG[i][ii]
                                        MarkerWithPosGS1.iPartS = iPartS
                                        MarkerWithPosGS1.sPartS = sPartS
                                        MarkerWithPosGS1.coorS = myMath.yByLin(
                                            g0, coorS0, g, coorS, MarkerWithPosGS1.coorG
                                        )
                                        MarkerWithPosGS1.xS = myMath.yByLin(
                                            g0, xS0, g, xS, MarkerWithPosGS1.coorG
                                        )
                                        MarkerWithPosGS1.iTypeS = -3
                            j = -1
                            k = iq
                        else:
                            if j < 0:
                                j = iq
                            MarkerWithPosGS.iPartS = iPartS
                            MarkerWithPosGS.sPartS = sPartS
                            MarkerWithPosGS.coorS = coorS
                            MarkerWithPosGS.xS = xS
                            MarkerWithPosGS.iTypeS = -4
                        iq += 1
                n1 = 0
                n2 = 0
                n3 = 0
                n4 = 0
                for MarkerWithPosGS in self.vMarkerWithPosGS:
                    if MarkerWithPosGS.iTypeS == -1:
                        n1 += 1
                    if MarkerWithPosGS.iTypeS == -2:
                        n2 += 1
                    if MarkerWithPosGS.iTypeS == -3:
                        n3 += 1
                    if MarkerWithPosGS.iTypeS == -4:
                        n4 += 1
                print(str(n1) + " " + str(n2) + " " + str(n3) + " " + str(n4))

            def select_genotypes(self, vsName, vMarkerWithPos, index):
                g = clGenotypes()
                sFileNameVCF = "C:\\Frenkel\\LTCPython\\VovaPy\\males_nofilter.vcf"  # Real data Eyal (from Cataglyphis/117males/males_nofilter.vcf)
                g.readFromVCF_compress_statistics_printInMultiQTLformat(
                    sFileNameVCF,
                    bPrintStatistics=True,
                    bPrintGenotypes=False,
                    bCompress=False,
                    nOfStateMin=40,
                    nReadsMinBeSureNotHeterozygote=6,
                    idType=0,
                )
                vIndivids = g.vMarker[0].vIndividsAll_get()
                nm = len(g.vMarker)  # not in use

                sFileName = (
                    "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\coorToStatistics"
                    + str(index)
                    + ".txt"
                )
                f = open(sFileName, "w")
                s = (
                    "mName" + "\t" + vMarkerWithPos[0].sShapka_get()
                )  # "chrG"+"\t"+"coorG"+"\t"+"coorGG"+"\t"+"iTypeG"+"\t"+"chrS"+"\t"+"coorS"+"\t"+"coorSS"+"\t"+"iTypeS"
                f.write(s + "\n")
                vi_in_vMarkerWithPos = []  # vim_in_vqMapped=[]
                for m in g.vMarker:
                    s = m.sMarker
                    im = -1
                    if m.sMarker in vsName:
                        im = vsName.index(m.sMarker)
                        # for i in range(4*2):
                        s += "\t" + vMarkerWithPos[im].s_get()  # str(vqMapped[im][i+2])
                    f.write(s + "\n")
                    vi_in_vMarkerWithPos.append(im)
                f.close
                return g, vIndivids, vi_in_vMarkerWithPos

            def filter_to_reduce_number_of_markers(
                self, g, vMarkerWithPos, vi_in_vMarkerWithPos
            ):  # vim_in_vMarker=
                im = 0
                vim_in_vMarker = []
                im_prev_ok = -1
                imq_prev_ok = -1
                for m in g.vMarker:
                    imq = vi_in_vMarkerWithPos[im]
                    if imq >= 0:  # in list vqMapped
                        MarkerWithPos = vMarkerWithPos[imq]
                        MarkerWithPos_prev = vMarkerWithPos[imq]  # poka tak
                        if (
                            MarkerWithPos.xS
                        ):  # vqMapped[imq][8]>0:#mapped to physical map directly or via genetic map
                            bNado = im_prev_ok < 0
                            if not (bNado):
                                MarkerWithPos_prev = vMarkerWithPos[imq_prev_ok]
                                if (
                                    MarkerWithPos_prev.sPartS != MarkerWithPos.sPartS
                                ):  # vqMapped[imq_prev_ok][6]!=vqMapped[imq][6]:
                                    bNado = True
                                if not (bNado):
                                    # if abs(vqMapped[imq_prev_ok][3]-vqMapped[imq][3])>=1 or abs(vqMapped[imq_prev_ok][7]-vqMapped[imq][7])>=100000:
                                    if (
                                        abs(
                                            MarkerWithPos_prev.coorG
                                            - MarkerWithPos.coorG
                                        )
                                        >= 1
                                        or abs(
                                            MarkerWithPos_prev.coorS
                                            - MarkerWithPos.coorS
                                        )
                                        >= 100000
                                    ):
                                        bNado = True
                            if bNado:
                                vim_in_vMarker.append(im)
                                if MarkerWithPos.iTypeS >= 0:  # vqMapped[imq][9]>=0:
                                    im_prev_ok = im
                                    imq_prev_ok = imq
                    im += 1
                nvim_in_vMarker = len(vim_in_vMarker)
                print("nMarkers_recPP=" + str(nvim_in_vMarker))
                return vim_in_vMarker

        def printFile_rec(index, vMarkerWithPosGS):
            vMarkerWithPos = []
            if index == 1:
                vMarkerWithPos = vMarkerWithPosGS.vMarkerWithPosS
            if index == 2:
                vMarkerWithPos = vMarkerWithPosGS.vMarkerWithPosGS

            # vsName
            def MyFunc(MarkerWithPos):
                return MarkerWithPos.sMarkerName

            vMarkerWithPos.sort(key=MyFunc)
            vsName = []
            for MarkerWithPos in vMarkerWithPos:
                vsName.append(MarkerWithPos.sMarkerName)

            g, vIndivids, vi_in_vMarkerWithPos = vMarkerWithPosGS.select_genotypes(
                vsName, vMarkerWithPos, index
            )
            vim_in_vMarker = vMarkerWithPosGS.filter_to_reduce_number_of_markers(
                g, vMarkerWithPos, vi_in_vMarkerWithPos
            )
            nvim_in_vMarker = len(vim_in_vMarker)

            # pair-wize recombination
            sFileName = (
                "C:\\Frenkel\\Privman\\NanoporeSequencingSupergene\\TrainingData\\recPP"
                + str(index)
                + ".txt"
            )
            f = open(sFileName, "w")
            # f1=open(sFileName1,'w')

            s = (
                "i"
                + "\t"
                + "im"
                + "\t"
                + "ii"
                + "\t"
                + "mName_1"
                + "\t"
                + "mName_2"
                + "\t"
                + "X2"
                + "\t"
                + "p"
                + "\t"
                + "rec"
                + "\t"
                + "d_cM"
            )
            # s+="\t"+"mName1"+"\t"+"ichr1"+"\t"+"chrG1"+"\t"+"coorG1"+"\t"+"coorGG1"+"\t"+"iTypeG1"+"\t"+"chrS1"+"\t"+"coorS1"+"\t"+"coorSS1"+"\t"+"iTypeS1"
            # s+="\t"+"mName2"+"\t"+"ichr2"+"\t"+"chrG2"+"\t"+"coorG2"+"\t"+"coorGG2"+"\t"+"iTypeG2"+"\t"+"chrS2"+"\t"+"coorS2"+"\t"+"coorSS2"+"\t"+"iTypeS2"
            s += "\t" + vMarkerWithPos[0].sShapka_get("1")
            s += "\t" + vMarkerWithPos[0].sShapka_get("2")
            f.write(s + "\n")
            # f1.write(s+"\n")
            myRec = clRecombination()

            imm = 0
            i = 0
            for im in vim_in_vMarker:
                m = g.vMarker[im]
                imq = vi_in_vMarkerWithPos[im]  # vim_in_vqMapped[im]
                ii = 0
                # for im1 in range(nm):
                for im1mm in range(imm + 1, nvim_in_vMarker):
                    im1 = vim_in_vMarker[im1mm]
                    m1 = g.vMarker[im1]
                    X2, df, nExpMin, LD, LD_tag, r, p, rec = m.compareWithMarkerLDchi2(
                        m1, vIndivids
                    )  # X2,df,nExpMin, LD, LD_tag, r, p=
                    # if (X2>2 and nExpMin>=5)or(p<0.01):
                    if p < 0.000001 and rec >= 0:  # 0.0000001
                        rec = min(rec, 1 - rec)
                        d_cM = myRec.distByR(rec)
                        imq1 = vi_in_vMarkerWithPos[im1]  # vim_in_vqMapped[im1]
                        s = (
                            str(i)
                            + "\t"
                            + str(imm)
                            + "\t"
                            + str(ii)
                            + "\t"
                            + m.sMarker
                            + "\t"
                            + m1.sMarker
                            + "\t"
                            + str(X2)
                            + "\t"
                            + str(p)
                            + "\t"
                            + str(rec)
                            + "\t"
                            + str(d_cM)
                        )
                        print(s)
                        # for iii in range(10):
                        # 	s+="\t"+str(vqMapped[imq][iii])
                        # for iii in range(10):
                        # 	s+="\t"+str(vqMapped[imq1][iii])
                        s += "\t" + vMarkerWithPos[imq].s_get()
                        s += "\t" + vMarkerWithPos[imq1].s_get()
                        f.write(s + "\n")
                        # if m.sChr!=m1.sChr or abs(m.pos-m1.pos)>3000000:
                        # 	#f1.write(s+"\n")
                        i += 1
                        ii += 1
                imm += 1
            f.close
            # f1.close

        vMarkerWithPosGS = clvMarkerWithPosGS(MarkersWithMultiplePos, iMapG, iMapS)
        printFile_rec(1, vMarkerWithPosGS)
        printFile_rec(2, vMarkerWithPosGS)
        return

    def selectPartsFromGffFiles(self):
        def oneChrPart(table, sTrait, sChr, sPart, sFolder, sCtg, coorStart, coorEnd):
            sFileName = sFolder + sTrait + "_" + sChr
            if sPart != "":
                sFileName += "_part" + sPart
            sFileName += ".gff"
            ###gff-version 3
            ##SOFTWARE INFO: GeMoMaPipeline 1.7.1; SIMPLE PARAMETERS: species: own; ID: Cf; weight: 1.0; species: own; ID: Hs; weight: 1.0; species: own; ID: Lh; weight: 1.0; species: own; ID: Si; weight: 1.0; species: own; ID: Pb; weight: 1.0; species: own; ID: Fe; weight: 1.0; species: own; ID: Ag; weight: 1.0; species: own; ID: Am; weight: 1.0; species: own; ID: Dm; weight: 1.0; species: own; ID: Nv; weight: 1.0; species: own; ID: Tc; weight: 1.0; tblastn: false; tag: mRNA; RNA-seq evidence: MAPPED; ERE.Stranded: FR_UNSTRANDED; ERE.ValidationStringency: LENIENT; ERE.use secondary alignments: true; ERE.coverage: false; ERE.minimum mapping quality: 40; ERE.minimum context: 1; denoise: DENOISE; DenoiseIntrons.maximum intron length: 15000; DenoiseIntrons.minimum expression: 0.01; DenoiseIntrons.context: 10; Extractor.upcase IDs: false; Extractor.repair: false; Extractor.Ambiguity: AMBIGUOUS; Extractor.discard pre-mature stop: true; Extractor.stop-codon excluded from CDS: false; Extractor.full-length: true; GeMoMa.reads: 1; GeMoMa.splice: true; GeMoMa.gap opening: 11; GeMoMa.gap extension: 1; GeMoMa.maximum intron length: 15000; GeMoMa.static intron length: true; GeMoMa.intron-loss-gain-penalty: 25; GeMoMa.e-value: 100.0; GeMoMa.contig threshold: 0.4; GeMoMa.region threshold: 0.9; GeMoMa.hit threshold: 0.9; GeMoMa.predictions: 10; GeMoMa.avoid stop: true; GeMoMa.approx: true; GeMoMa.protein alignment: true; GeMoMa.prefix: ; GeMoMa.timeout: 3600; GeMoMa.Score: ReAlign; GAF.common border filter: 0.75; GAF.maximal number of transcripts per gene: 2147483647; GAF.default attributes: tie,tde,tae,iAA,pAA,score; GAF.filter: start=='M' and stop=='*' and (isNaN(score) or score/aa>=0.75); GAF.sorting: evidence,score; GAF.alternative transcript filter: tie==1 or evidence>1; AnnotationFinalizer.UTR: NO; AnnotationFinalizer.rename: NO; AnnotationFinalizer.name attribute: true; predicted proteins: true; predicted CDSs: false; predicted genomic regions: true; output individual predictions: true; debug: true; restart: false; BLAST_PATH: ; MMSEQS_PATH: /data/home/privman/ypellen/MMseqs2/bin/
            ###sequence-region unMap_tig00002002_pilon_8661801_1___from185709_to3576404_len3390695 1 3390695
            # unMap_tig00002002_pilon_8661801_1___from185709_to3576404_len3390695	GAF	gene	18486	30609	.	+	.	ID=gene_14964;transcripts=1;complete=1;maxTie=0.5;maxEvidence=1;combinedEvidence=1
            f = open(sFileName, "w")
            bStarted = False
            bOk = False
            ir = 0
            n = 0
            for r in table.rows:
                if ir == 0:
                    s = r.s_get()
                    f.write(s + "\n")
                else:
                    s = r.vCellText[0]
                    if s[0:2] == "##":
                        # s=s[2:0]
                        vs = s.split(" ")
                        s = vs[1]
                        if s == sChr:
                            s = r.s_get()
                            f.write(s + "\n")
                            bStarted = True
                            print("+1")
                        else:
                            bStarted = False
                    else:
                        if bStarted:
                            if r.vCellText[2] == "gene":
                                x0 = int(r.vCellText[3])
                                x1 = int(r.vCellText[4])
                                if max(x0, x1) < coorStart or min(x0, x1) > coorEnd:
                                    bOk = False
                                else:
                                    bOk = True
                            if bOk:
                                s = r.s_get()
                                f.write(s + "\n")
                                n += 1
                ir += 1
            f.close
            return n

        def makeFile_toSelectPP():
            sFileNameToSelectTable = "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\toSelect_.txt"
            # trait	LG	part	chr3a.1	Cnig_gn3a.1_min	Cnig_gn3a.1_max	chr3.1	Cnig_gn3.1_min	Cnig_gn3.1_max
            # C25	chr06	1	chr06	0	1577629	chr06	0	564629

            sFileNameToSelectTable1 = "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\toSelect_PP.txt"

            sFileNameQTLs = "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\toSelectGenet.txt"
            # chr	Loc_min	Loc_med	Loc_max
            # chr06	0	21.06	43.2

            sFileNameMaps = (
                "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\ttt.txt"
            )
            # markerBesan	Besan_part	Besan_pos	Besan_iType	mapGenetic_part	mapGenetic_pos	mapGenetic_iType	Cnig_gn3a.1_part	Cnig_gn3a.1_pos	Cnig_gn3a.1_iType	Cnig_gn3.1_part	Cnig_gn3.1_pos	Cnig_gn3.1_iType
            # N2045P26535	chr01	0	0	chr01	1.562627175	0	chr01	110372	0	chr01	111830	0

            tableQTLs = clTableOfTxt()
            tableQTLs.readFromFile(sFileNameQTLs, True, False)

            tableMaps = clTableOfTxt()
            tableMaps.readFromFile(sFileNameMaps, True, False)

            f = open(sFileNameToSelectTable, "w")
            f1 = open(sFileNameToSelectTable1, "w")

            s = "trait	LG	part	chr3a.1	Cnig_gn3a.1_min	Cnig_gn3a.1_max	chr3.1	Cnig_gn3.1_min	Cnig_gn3.1_max"
            f.write(s + "\n")
            s = "trait	LG	part	chr3a.1	Cnig_gn3a.1_min	Cnig_gn3a.1_med	Cnig_gn3a.1_max	chr3.1	Cnig_gn3.1_min	Cnig_gn3.1_med	Cnig_gn3.1_max"
            f1.write(s + "\n")

            def func1(tableMaps, sChr, coor, bMin, tol=1):
                sChr3p1 = ""
                coor3p1 = -1
                for r in tableMaps.rows:
                    if r.vCellText[4] == sChr:
                        if coor < 1 and bMin:
                            sChr3p1T = r.vCellText[7]
                            if len(sChr3p1T) > 3:
                                if (
                                    sChr3p1T[:3] == "chr"
                                    or sChr3p1T
                                    == "unMap_tig00002002_pilon_8661801_1___from185709_to3576404_len3390695"
                                ):
                                    sChr3p1, coor3p1 = sChr3p1T, 0
                                    return sChr3p1, coor3p1, -1
                        if abs(float(r.vCellText[5]) - coor) < tol:
                            print(r.s_get())
                            sChr3p1T = r.vCellText[10]
                            if len(sChr3p1T) > 3 and (sChr3p1 == "" or not bMin):
                                coor3p1T = int(r.vCellText[11])
                                if sChr3p1T[:3] == "chr":
                                    sChr3p1, coor3p1 = sChr3p1T, coor3p1T
                if coor3p1 < 0:
                    sChr3p1, coor3p1, tol = func1(tableMaps, sChr, coor, bMin, tol + 1)
                return sChr3p1, coor3p1, tol

            def func1a(tableMaps, sChr, coor, bMin, tol=1):
                sChr3ap1 = ""
                coor3ap1 = -1
                for r in tableMaps.rows:
                    if r.vCellText[4] == sChr:
                        if coor < 1 and bMin:
                            sChr3ap1T = r.vCellText[7]
                            if len(sChr3ap1T) > 3:
                                if (
                                    sChr3ap1T[:3] == "chr"
                                    or sChr3ap1T
                                    == "unMap_tig00002002_pilon_8661801_1___from185709_to3576404_len3390695"
                                ):
                                    sChr3ap1, coor3ap1 = sChr3ap1T, 0
                                    return sChr3ap1, coor3ap1, -1
                        if abs(float(r.vCellText[5]) - coor) < tol:
                            print(r.s_get())
                            sChr3ap1T = r.vCellText[7]
                            if len(sChr3ap1T) > 3 and (sChr3ap1 == "" or not bMin):
                                coor3ap1T = int(r.vCellText[8])
                                if (
                                    sChr3ap1T[:3] == "chr"
                                    or sChr3ap1T
                                    == "unMap_tig00002002_pilon_8661801_1___from185709_to3576404_len3390695"
                                ):
                                    sChr3ap1, coor3ap1 = sChr3ap1T, coor3ap1T
                if coor3ap1 < 0:
                    sChr3ap1, coor3ap1, tol = func1a(
                        tableMaps, sChr, coor, bMin, tol + 1
                    )
                return sChr3ap1, coor3ap1, tol

            # from my Old genetic map to my new genetic map
            def newChr(sChr):
                if sChr == "chr20":
                    return "chr09"
                return sChr

            def newCoor(sChrOld, coor):
                if sChrOld == "chr20":
                    return coor
                if sChrOld == "chr09":
                    return coor + 140
                return coor

            # QTL version of Besan's genetic map (not provided for all)
            def geneticMapPos(sChrOld, coorOld):
                sFileNameQQQ = (
                    "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\qqq.txt"
                )
                tableQQQ = clTableOfTxt()
                tableQQQ.readFromFile(sFileNameQQQ, True, False)

                """
				LG NAME	CHS		MARKERS	(cM)	Besan_part	Besan_pos	Besan_iType	mapGenetic_part	mapGenetic_pos
				LG6	C25	p1	N9255P5416	0	chr06	0	0	chr06	0
							N14199P1665	4.266	chr06	0	0	chr06	0
							N5860P3013	21.06	chr06	15.62	0	chr06	15.70952165
							N5666P9121	22.04	chr06	16.6	0	chr06	16.15052589
							N2135P2020	31.68	chr06	18.56	0	chr06	27.49256144
				LG6	C25	p2	N2949P16061	73.04	chr06	55.17	0	chr06	67.3461899
							N4781P669	76.86	chr06	58.97	0	chr06	71.26977068
							N3650P6077	77.83	chr06	59.94	0	chr06	72.25019425
							N4562P9631	80.69					
							N1038P41012	81.62					
							N1038P3497	83.62					
							N1908P14666	88.74	chr06	70.82	0	chr06	80.06566227
				"""

                sChr = newChr(sChrOld)

                it = 0
                d0 = -100000000
                d1 = 100000000
                x0 = 0
                x1 = 100000000
                y0 = 0
                y1 = 100000000
                for r in tableQQQ.rows:
                    if r.vCellText[8] != "" and r.vCellText[5] == sChrOld:

                        x = float(r.vCellText[4])
                        y = float(r.vCellText[9])
                        d = x - coorOld
                        print(r.s_get() + str([x, d, x1, d1, x0, d0]))
                        if d >= 0:
                            if d < d1:
                                x1 = x
                                y1 = y
                                d1 = d
                            else:
                                if d0 < -99999999:
                                    x0 = x
                                    y0 = y
                        else:
                            if d > d0:
                                x0 = x
                                y0 = y
                                d0 = d
                                print(str(d0))
                    it += 1
                myMath = clVovaMath()
                coor = myMath.yByLin(x0, y0, x1, y1, coorOld)
                print(str([sChrOld, coorOld, sChr, coor, x0, y0, x1, y1]))
                # a=1/0
                return sChr, coor

            for r in tableQTLs.rows:
                sChrOld = r.vCellText[0]
                sChr = newChr(sChrOld)
                vcoor = []
                for i in range(3):
                    vcoor.append(float(r.vCellText[i + 1]))
                bMyOldMap = False
                if bMyOldMap:
                    sChr = newChr(sChrOld)
                    print(r.s_get())
                    for i in range(3):
                        vcoor[i] = newCoor(sChrOld, vcoor[i])
                else:
                    # QTL version of Besan's genetic map (not provided for all)
                    for i in range(3):
                        sChr, vcoor[i] = geneticMapPos(sChrOld, vcoor[i])
                vsChr3p1 = []
                vsChr3ap1 = []
                vcoor3p1 = []
                vcoor3ap1 = []
                vtol = []
                for i in range(3):
                    sChr3p1, coor3p1, tol = func1(tableMaps, sChr, vcoor[i], i < 2)
                    sChr3ap1, coor3ap1, tola = func1a(tableMaps, sChr, vcoor[i], i < 2)
                    vsChr3p1.append(sChr3p1)
                    vsChr3ap1.append(sChr3ap1)
                    vcoor3p1.append(coor3p1)
                    vcoor3ap1.append(coor3ap1)
                    vtol.append(tola)
                    vtol.append(tol)
                s = "trait	LG	part"
                s1 = "trait	LG	part"
                s += "\t" + vsChr3ap1[0]
                s1 += "\t" + vsChr3ap1[0]
                for i in range(3):
                    if i != 1:
                        s += "\t" + str(vcoor3ap1[i])
                    s1 += "\t" + str(vcoor3ap1[i])
                s += "\t" + vsChr3p1[0]
                s1 += "\t" + vsChr3p1[0]
                for i in range(3):
                    if i != 1:
                        s += "\t" + str(vcoor3p1[i])
                    s1 += "\t" + str(vcoor3p1[i])
                s1 += "\t" + str(vtol)
                f.write(s + "\n")
                f1.write(s1 + "\n")
            f.close()
            f1.close()

        makeFile_toSelectPP()
        return

        sFileNameToSelectTable = (
            "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\toSelect.txt"
        )
        sFileNameGff1 = "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\Cnig_gn3.1\\final_annotation_3.1.gff"
        sFileNameGff2 = "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\Cnig_gn3a.1\\final_annotation_3a.1.gff"
        sFolderName1 = (
            "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\Cnig_gn3.1\\"
        )
        sFolderName2 = (
            "C:\\Frenkel\\Privman\\QTL\\selected_basedOnBesanAndYoann\\Cnig_gn3a.1\\"
        )

        tableTraits = clTableOfTxt()
        # trait	LG	part	chr3a.1	Cnig_gn3a.1_min	Cnig_gn3a.1_max	chr3.1	Cnig_gn3.1_min	Cnig_gn3.1_max
        # C25	chr06	1	chr06	0	1577629	chr06	0	564629
        tableTraits.readFromFile(sFileNameToSelectTable, True, False)

        table1 = clTableOfTxt()
        table1.readFromFile(sFileNameGff1, False, False)
        table2 = clTableOfTxt()
        table2.readFromFile(sFileNameGff2, False, False)
        for r in tableTraits.rows:
            sTrait = r.vCellText[0]
            sChr = r.vCellText[1]
            sPart = r.vCellText[2]
            print(sTrait + " " + sChr + " " + sPart + ":")

            sCtg2 = r.vCellText[3]
            coorStart2 = int(r.vCellText[4])
            coorEnd2 = int(r.vCellText[5])

            sCtg1 = r.vCellText[6]
            coorStart1 = int(r.vCellText[7])
            coorEnd1 = int(r.vCellText[8])

            n1 = oneChrPart(
                table1, sTrait, sChr, sPart, sFolderName1, sCtg1, coorStart1, coorEnd1
            )
            n2 = oneChrPart(
                table2, sTrait, sChr, sPart, sFolderName2, sCtg2, coorStart2, coorEnd2
            )
            print(str(n1) + " " + str(n2))

    def geneticMap_Alexandra_1(self):  # genetic map for camponotus
        Genotypes = clGenotypes()
        # Genotypes.readFromFileSimple(sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
        sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\camponotus_MP.txt"
        sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\"
        Genotypes.readFromFileSimple(sFileName, False, "\t", 0, True, True)
        bFirst = True

        def sCtg_coor_get(s):
            # scaffold39p2193284
            ss = s.split("p")
            return ss[0], int(ss[1])

        if bFirst:
            sFileNameS = (
                sFileName + "_statisticsOnMarkers.txt"
            )  # statistics for Real data
            Genotypes.printStatistics(sFileNameS, True, True)
            sFileNameD = sFileName + "_distMatrix.txt"
            Genotypes.printNDist(sFileNameD, True, True)
            # dMax=0.18
            # sFileNamePajek=sFileName+"_PajekAll0p18.txt"
            # sFileNamePajekPP=sFileName+"_PajekAll0p18_pp.txt"
            dMax = 0.25
            sFileNamePajek = sFileName + "_PajekAll0p25.txt"
            sFileNamePajekPP = sFileName + "_PajekAll0p25_pp.txt"
            Genotypes.printNetPajek(sFileNamePajek, dMax, True, True)
            # NB! to view this file in my program (Visual Basic LTC) need to add manually number of edges and change .txt to .net

            bExcludeNodesCausingNonLinearClusters = True  # False#

            # buildGeneticMap(self,bExcludeNodesCausingNonLinearClusters,sFileNamePajek,sFileNamePajekPP,sPath,sPath1=self.sPath,bCoorPrivman=True)
            # vLG=Genotypes.buildGeneticMap(bExcludeNodesCausingNonLinearClusters,sFileNamePajek,sFileNamePajekPP,sPath,sPath,False)
            BuildingGeneticMap = clBuildingGeneticMap(g, sPath)
            BuildingGeneticMap.bExcludeNodesCausingNonLinearClusters = (
                bExcludeNodesCausingNonLinearClusters
            )
            BuildingGeneticMap.sFileNamePajek = sFileNamePajek
            BuildingGeneticMap.sFileNamePajekPP = sFileNamePajekPP
            BuildingGeneticMap.index = 1
            BuildingGeneticMap.buildGeneticMap()
            vLG = BuildingGeneticMap.vLG
            print("nLG=" + str(len(vLG)))
            for LG in vLG:
                print(LG.name + ": nM=" + str(LG.nMarkers))

        def testDistances(ggg, sFileName, g):  # slow
            # test distances
            recVova = clRecombination()
            sFileNameDistControl = sFileName + ".distControl.txt"
            f = open(sFileNameDistControl, "w")
            s = (
                "marker1"
                + "\t"
                + "marker2"
                + "\t"
                + "ctg"
                + "\t"
                + "coor1"
                + "\t"
                + "coor2"
                + "\t"
                + "dPhys"
                + "\t"
                + "r"
                + "\t"
                + "dGenetic"
            )
            f.write(s + "\n")
            for m in g.vMarker:
                sCtg, coor = sCtg_coor_get(m.sMarker)
                for m1 in g.vMarker:
                    sCtg1, coor1 = sCtg_coor_get(m1.sMarker)
                    if sCtg1 == sCtg and coor1 > coor:
                        nR, nN, nMissed = recVova.nnn(m.g, m1.g, False)
                        r = recVova.rML(nR, nN)
                        dGenetic = recVova.distByR(r)
                        s = (
                            m.sMarker
                            + "\t"
                            + m1.sMarker
                            + "\t"
                            + sCtg
                            + "\t"
                            + str(coor)
                            + "\t"
                            + str(coor1)
                            + "\t"
                            + str(coor1 - coor)
                            + "\t"
                            + str(r)
                            + "\t"
                            + str(dGenetic)
                        )
                        f.write(s + "\n")
            f.close()

        testDistances(self, sFileName, Genotypes)

    def geneticMap_Alexandra_2(self):  # genetic map for Lasius
        Genotypes = clGenotypes()
        # Genotypes.readFromFileSimple(sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
        sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\20220728\\populations.snps.vcf"
        sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\vova\\"
        # Genotypes.readFromFileSimple(sFileName,False,"\t",0,True,True)
        # readFromFileVCF(self,sFileName,bPrint=False,bPrintDetails=False,nOfStateMin=15,nReadsMinBeSureNotHeterozygote=6,idType=0)
        Genotypes.readFromFileVCF(
            sFileName,
            bPrint=True,
            bPrintDetails=False,
            nOfStateMin=15,
            nReadsMinBeSureNotHeterozygote=6,
            idType=4,
            ploidy=0,
        )

        bFirst = False  # True
        sFileNameS = sPath + "s.txt"  # statistics for Real data
        # dMax=0.18
        # sFileNamePajek=sFileName+"_PajekAll0p18.txt"
        # sFileNamePajekPP=sFileName+"_PajekAll0p18_pp.txt"
        dMax = 0.25
        sFileNamePajek = sFileName + "_PajekAll0p25.txt"
        sFileNamePajekPP = sFileName + "_PajekAll0p25_pp.txt"
        if bFirst:
            Genotypes.printNetPajek(sFileNamePajek, dMax, True, True)
            Genotypes.printStatistics(sFileNameS, True, True)
            Genotypes.printGenotypes(sPath + "g.txt", True, True, True)  # 0,1,2

            sFileNameD = sFileName + "_distMatrix.txt"
            Genotypes.printNDist(sFileNameD, True, True)
        # NB! to view this file in my program (Visual Basic LTC) need to add manually number of edges and change .txt to .net

        bExcludeNodesCausingNonLinearClusters = True  # False#

        # buildGeneticMap(self,bExcludeNodesCausingNonLinearClusters,sFileNamePajek,sFileNamePajekPP,sPath,sPath1=self.sPath,bCoorPrivman=True)
        # vLG=Genotypes.buildGeneticMap(bExcludeNodesCausingNonLinearClusters,sFileNamePajek,sFileNamePajekPP,sPath,sPath,False)
        BuildingGeneticMap = clBuildingGeneticMap(g, sPath)
        BuildingGeneticMap.bExcludeNodesCausingNonLinearClusters = (
            bExcludeNodesCausingNonLinearClusters
        )
        BuildingGeneticMap.sFileNamePajek = sFileNamePajek
        BuildingGeneticMap.sFileNamePajekPP = sFileNamePajekPP
        BuildingGeneticMap.index = 1
        BuildingGeneticMap.buildGeneticMap()
        vLG = BuildingGeneticMap.vLG
        print("nLG=" + str(len(vLG)))
        for LG in vLG:
            print(LG.name + ": nM=" + str(LG.nMarkers))

        # GeneticMaps/Nylanderia fulva/nyfulN.gq20maxmiss80maf05.recode.vcf
        #

    def geneticMap_Alexandra_3(self):  # genetic map for Formica glacialis
        Genotypes = clGenotypes()
        sData = "camponotus_202205"
        sData = "Camponotus_fellah"
        # sData="Formica glacialis"
        # sData="Nylanderia fulva"
        if sData == "camponotus_202205" or sData == "Camponotus_fellah":
            if sData == "camponotus_202205":
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\camponotus_MP.txt"
                sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\"
                Genotypes.readFromFileSimple(sFileName, False, "\t", 0, True, True)
            if sData == "Camponotus_fellah":
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\camponotus_final.vcf"
                sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\VCF\\"
                Genotypes.readFromFileVCF(
                    sFileName,
                    bPrint=True,
                    bPrintDetails=False,
                    nOfStateMin=15,
                    nReadsMinBeSureNotHeterozygote=6,
                    idType=0,
                    ploidy=0,
                )

            # bFirst=True#False#False#
            dMax = 0.25
            BuildingGeneticMap = clBuildingGeneticMap(Genotypes, sPath)
            BuildingGeneticMap.index = 1
            bFirst = True  # False#False#
            BuildingGeneticMap.bExcludeNodesCausingNonLinearClusters = True  # False#
        if sData == "Formica glacialis":
            # Genotypes.readFromFileSimple(sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
            sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\fglac.gq20.maf10.maxmiss80.mappable.recode.vcf.recode.vcf"
            sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\"
            # Genotypes.readFromFileSimple(sFileName,False,"\t",0,True,True)
            # readFromFileVCF(self,sFileName,bPrint=False,bPrintDetails=False,nOfStateMin=15,nReadsMinBeSureNotHeterozygote=6,idType=0)
            Genotypes.readFromFileVCF(
                sFileName,
                bPrint=True,
                bPrintDetails=False,
                nOfStateMin=15,
                nReadsMinBeSureNotHeterozygote=6,
                idType=5,
                ploidy=0,
            )

            dMax = 0.25
            BuildingGeneticMap = clBuildingGeneticMap(Genotypes, sPath)
            BuildingGeneticMap.index = 1
            bFirst = False  # True#False#
            BuildingGeneticMap.bExcludeNodesCausingNonLinearClusters = False
        if sData == "Nylanderia fulva":
            # Genotypes.readFromFileSimple(sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
            sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Nylanderia fulva\\nyfulN.gq20maxmiss80maf05.recode.vcf"
            sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Nylanderia fulva\\"
            # Genotypes.readFromFileSimple(sFileName,False,"\t",0,True,True)
            # readFromFileVCF(self,sFileName,bPrint=False,bPrintDetails=False,nOfStateMin=15,nReadsMinBeSureNotHeterozygote=6,idType=0)
            Genotypes.readFromFileVCF(
                sFileName,
                bPrint=True,
                bPrintDetails=False,
                nOfStateMin=15,
                nReadsMinBeSureNotHeterozygote=6,
                idType=5,
                ploidy=0,
            )

            dMax = 0.25
            BuildingGeneticMap = clBuildingGeneticMap(Genotypes, sPath)
            BuildingGeneticMap.index = 1
            BuildingGeneticMap.Clustering_cutoff = 0.1
            BuildingGeneticMap.NodeTest_cutoff = 0.1
            BuildingGeneticMap.NodeTest_cutoffParallel = 0.20
            BuildingGeneticMap.cutoffVerticesLinked = 0.1
            BuildingGeneticMap.Net_cutoff = 0.15
            bFirst = False  # True#False#
            BuildingGeneticMap.bExcludeNodesCausingNonLinearClusters = True

            # sPath="C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Nylanderia fulva\\15\\"
            # BuildingGeneticMap=clBuildingGeneticMap(Genotypes,sPath)
            # BuildingGeneticMap.Clustering_cutoff=0.15
            # BuildingGeneticMap.NodeTest_cutoff=0.1
            # BuildingGeneticMap.NodeTest_cutoffParallel=0.20
            # BuildingGeneticMap.cutoffVerticesLinked=0.07
            # BuildingGeneticMap.Net_cutoff=0.2

        # x=1/0
        BuildingGeneticMap.startStandard(bFirst, dMax)
        # BuildingGeneticMap.buildGeneticMap()
        # vLG=BuildingGeneticMap.vLG

    class clMapsAlexandra:
        def __init__(self, sData):
            self.readMaps(sData)

        def readMaps(self, sData):
            GenomeMapComparisonGraph = clGenomeMapComparisonGraph()
            self.Genotypes = clGenotypes()
            if sData == "Camponotus":
                # marker names in genotypes in format scaffold1p1327199
                # self.sPath="C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\res20220915\\"

                # Alex
                #
                # (no need)
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\20220703\\Result file_Sk&Ext.txt"
                self.GM_0 = clGeneticMap()
                self.GM_0.readFromFileMultiPoint_vAlexandra202206(
                    sFileName, "Alex_0", 1, 0
                )  # s1p1327199 -> scaffold1p1327199
                self.GM_0.printToFileTextFormat(self.sPath + "Alex_0.txt")
                self.GM_0.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
                #
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\20220705\\Result file_Sk&Ext.txt"  # some more markers => longer maps
                self.GM_1 = clGeneticMap()
                self.GM_1.readFromFileMultiPoint_vAlexandra202206(
                    sFileName, "Alex_1", 1, 0
                )
                self.GM_1.printToFileTextFormat(self.sPath + "Alex_1.txt")
                self.GM_1.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
                #
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\20220705\\Result file_Sk.txt"  # skeleton markers only
                self.GM_2 = clGeneticMap()
                self.GM_2.readFromFileMultiPoint_vAlexandra202206(
                    sFileName, "Alex_2", 1, 0
                )
                self.GM_2.printToFileTextFormat(self.sPath + "Alex_2.txt")
                self.GM_2.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)

                self.sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\"

                # physical map (contigs):
                # scaffold1p1327199
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\camponotus_MP.txt"
                # Genotypes.readFromFileSimple(sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
                self.Genotypes.readFromFileSimple(sFileName, False, "\t", 0, True, True)
                # 2030 markers (2*2030=4060 for MST)
                # 116 individuals
                #
                self.physMap = clGeneticMap()
                self.physMap.readFromMarkerNames___Genotypes(
                    self.Genotypes, "Contigs"
                )  # ,0)
                self.physMap.printToFileTextFormat(self.sPath + "GM_phys.txt")
                self.physMap.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
                #
                # GM_Vova
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\CoorControl.txt"
                self.GM_Vova = clGeneticMap()
                self.GM_Vova.readFromFile_coorControl(sFileName, "Vova")
                self.GM_Vova.printToFileTextFormat(self.sPath + "GM_Vova.txt")
                self.GM_Vova.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )

                #'/cygdrive/c/Frenkel/Privman/Alexandra/GeneticMaps/'
                # by MST software
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\map_file_2022_Sep_17-13_52_20.txt"  # map_file_2022_Sep_15-11_55_10.txt"
                self.GM_MST = clGeneticMap()
                self.GM_MST.readFromFile_MSTsoftware(
                    sFileName, bDoubles=True, sNameOfMap="MST"
                )
                self.GM_MST.printToFileTextFormat(self.sPath + "GM_MST.txt")
                self.GM_MST.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
            if (
                sData == "Camponotus_fellah"
            ):  # the same like "Camponotus" but directly from .vcf file
                self.sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\VCF\\"

                # scaffold10|size6254774___75016
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\camponotus_final.vcf"
                self.Genotypes.readFromFileVCF(
                    sFileName,
                    bPrint=True,
                    bPrintDetails=False,
                    nOfStateMin=15,
                    nReadsMinBeSureNotHeterozygote=6,
                    idType=0,
                    ploidy=0,
                )

                self.physMap = clGeneticMap()
                self.physMap.readFromMarkerNames___Genotypes(
                    self.Genotypes, "Contigs"
                )  # ,0)
                self.physMap.printToFileTextFormat(self.sPath + "GM_phys.txt")
                self.physMap.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )

                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\VCF\\CoorControl.txt"
                self.GM_Vova = clGeneticMap()
                self.GM_Vova.readFromFile_coorControl(
                    sFileName, "Vova"
                )  # scaffold1|size19413119___1700327
                self.GM_Vova.printToFileTextFormat(self.sPath + "GM_Vova.txt")
                self.GM_Vova.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )

                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\20220705\\Result file_Sk&Ext.txt"  # some more markers => longer maps
                self.GM_1 = clGeneticMap()
                self.GM_1.readFromFileMultiPoint_vAlexandra202206(
                    sFileName, "Alex_1", 1, 0
                )  # s10p75016 -> scaffold10p75016
                self.GM_1.renameMarkersByChangingNameOfCtg(
                    self.physMap
                )  # scaffold10p75016 -> scaffold10|size6254774___75016
                self.GM_1.printToFileTextFormat(self.sPath + "Alex_1.txt")
                self.GM_1.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)

            if sData == "Lasius":
                # marker names in format Scaffold1___1873261
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\20220728\\populations.snps.vcf"
                self.Genotypes.readFromFileVCF(
                    sFileName,
                    bPrint=True,
                    bPrintDetails=False,
                    nOfStateMin=0,
                    nReadsMinBeSureNotHeterozygote=0,
                    idType=4,
                    ploidy=0,
                )
                #
                self.sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\vova\\"

                # Alex:
                # males
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\maps\\males\\Result file_Sk&Ext.txt"
                self.GM_1 = clGeneticMap()
                # s2p592932 -> Scaffold1___1873261
                self.GM_1.readFromFileMultiPoint_vAlexandra202206(
                    sFileName, "Alex_males", 1, 2
                )
                self.GM_1.printToFileTextFormat(self.sPath + "GM_Alex_males.txt")
                self.GM_1.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
                #
                # both
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\maps\\malesAndWorkers\\Result file_Sk&Ext (1).txt"
                self.GM_2 = clGeneticMap()
                self.GM_2.readFromFileMultiPoint_vAlexandra202206(
                    sFileName, "Alex_both", 1, 2
                )
                self.GM_2.printToFileTextFormat(self.sPath + "GM_Alex_both.txt")
                self.GM_2.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
                #
                # workers
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\20220728\\Result file_Sk&Ext.txt"
                self.GM_3 = clGeneticMap()
                self.GM_3.readFromFileMultiPoint_vAlexandra202206(
                    sFileName, "Alex_workers", 1, 2
                )
                self.GM_3.printToFileTextFormat(self.sPath + "GM_Alex_workers.txt")
                self.GM_3.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
                #
                # GM_Lasius_Vova
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\vova\\CoorControl.txt"
                self.GM_Vova = clGeneticMap()
                self.GM_Vova.readFromFile_coorControl(sFileName, "Vova")
                self.GM_Vova.printToFileTextFormat(self.sPath + "GM_Vova.txt")
                self.GM_Vova.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
            if sData == "Formica glacialis":
                # physical map (contigs):
                # ScbnsAo_1___161534
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\g.txt"
                # Genotypes.readFromFileSimple(sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
                self.Genotypes.readFromFileSimple(sFileName, False, "", 0, True, True)
                # 4667 markers (2*4667=9334 for MST)
                # nIndivids=62
                #
                self.sPath = (
                    "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\"
                )
                #
                self.physMap = clGeneticMap()
                self.physMap.readFromMarkerNames___Genotypes(
                    self.Genotypes, "Contigs"
                )  # ,0)
                self.physMap.printToFileTextFormat(self.sPath + "GM_phys.txt")
                self.physMap.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
                # self.GMC_physMap=GenomeMapComparisonGraph.clMap()
                # self.GMC_physMap.get_fromGeneticMap(GenomeMapComparisonGraph,"physMap",self.physMap)

                #
                # GM_Vova
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\CoorControl.txt"
                self.GM_Vova = clGeneticMap()
                self.GM_Vova.readFromFile_coorControl(sFileName, "Vova")
                self.GM_Vova.printToFileTextFormat(self.sPath + "GM_Vova.txt")
                self.GM_Vova.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
                # self.GMC_Vova=GenomeMapComparisonGraph.clMap()
                # self.GMC_Vova.get_fromGeneticMap(GenomeMapComparisonGraph,"Vova",self.GM_Vova)

                # by MST software
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\MST_results\\map_file_2022_Sep_15-12_52_22.txt"  # map_file_2022_Sep_15-11_55_10.txt"
                self.GM_MST = clGeneticMap()
                self.GM_MST.readFromFile_MSTsoftware(
                    sFileName, bDoubles=True, sNameOfMap="MST"
                )
                self.GM_MST.printToFileTextFormat(self.sPath + "GM_MST.txt")
                self.GM_MST.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
                # self.GMC_MST=GenomeMapComparisonGraph.clMap()
                # self.GMC_MST.get_fromGeneticMap(GenomeMapComparisonGraph,"MST based map",self.GM_MST)

                # from Alan Brelsford <Alan.Brelsford@ucr.edu> Date: Sun, Sep 18, 2022 at 10:19 AM
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\mapFrom.txt"
                self.GM_1 = clGeneticMap()
                self.GM_1.readFromTableSimple(sFileName, True, "Alan")
                self.GM_1.printToFileTextFormat(self.sPath + "GM_1.txt")
                self.GM_1.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
                # self.GMC_1=GenomeMapComparisonGraph.clMap()
                # self.GMC_1.get_fromGeneticMap(GenomeMapComparisonGraph,"Alan Brelsford",self.GM_1)
            if sData == "Nylanderia fulva":
                # physical map (contigs):
                # ScbnsAo_1___161534
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Nylanderia fulva\\g.txt"
                # Genotypes.readFromFileSimple(sFileName,bIndNames,sSep,idType,bPrint=False,bPrintDetails=False)
                self.Genotypes.readFromFileSimple(sFileName, False, "", 0, True, True)
                # 3352 markers (2*3352=6704 markers for MST)
                # 46 individuals
                #
                self.sPath = (
                    "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Nylanderia fulva\\"
                )
                #
                self.physMap = clGeneticMap()
                self.physMap.readFromMarkerNames___Genotypes(
                    self.Genotypes, "Contigs"
                )  # ,0)
                self.physMap.printToFileTextFormat(self.sPath + "GM_phys.txt")
                self.physMap.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
                # self.GMC_physMap=GenomeMapComparisonGraph.clMap()
                # self.GMC_physMap.get_fromGeneticMap(GenomeMapComparisonGraph,"physMap",self.physMap)

                #
                # GM_Vova
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Nylanderia fulva\\CoorControl.txt"
                self.GM_Vova = clGeneticMap()
                self.GM_Vova.readFromFile_coorControl(sFileName, "Vova")
                self.GM_Vova.printToFileTextFormat(self.sPath + "GM_Vova.txt")
                self.GM_Vova.GenomeMapComparisonGraph_map___make(
                    GenomeMapComparisonGraph
                )
                # self.GMC_Vova=GenomeMapComparisonGraph.clMap()
                # self.GMC_Vova.get_fromGeneticMap(GenomeMapComparisonGraph,"Vova",self.GM_Vova)

                # #by MST software
                # sFileName="C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Formica glacialis\\MST_results\\map_file_2022_Sep_15-12_52_22.txt"#map_file_2022_Sep_15-11_55_10.txt"
                # self.GM_MST=clGeneticMap()
                # self.GM_MST.readFromFile_MSTsoftware(sFileName,bDoubles=True,sNameOfMap="MST")
                # self.GM_MST.printToFileTextFormat(self.sPath+"GM_MST.txt")
                # self.GMC_MST=GenomeMapComparisonGraph.clMap()
                # self.GMC_MST.get_fromGeneticMap(GenomeMapComparisonGraph,"MST based map",self.GM_MST)

                # from Alan Brelsford <Alan.Brelsford@ucr.edu> Date: Sun, Sep 18, 2022 at 10:19 AM
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Nylanderia fulva\\mapFrom.txt"
                self.GM_1 = clGeneticMap()
                self.GM_1.readFromTableSimple(sFileName, True, "Alan")
                self.GM_1.printToFileTextFormat(self.sPath + "GM_1.txt")
                self.GM_1.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
                # self.GMC_1=GenomeMapComparisonGraph.clMap()
                # self.GMC_1.get_fromGeneticMap(GenomeMapComparisonGraph,"Alan Brelsford",self.GM_1)

    def Alexandra_map_test___compare3maps(self):
        # need to put the results to here:
        # https://drive.google.com/drive/folders/1uFGz3Zj_8fgKgDGGTQydcF_5UrCQwMO0?usp=sharing

        def testLinkages___run(GeneticMap, sMap=""):
            # here we can use values avaliable within external function Alexandra_map_test___compare3maps:
            # sData, myMaps
            cutOffToShow = 0.3
            if sData == "Camponotus":
                cutOffToShow = 0.2
            if sData == "Nylanderia fulva":
                cutOffToShow = 0.12
            bReorderingAndReorientationMap2 = False
            if sMap == "":
                sMap = GeneticMap.sNameOfMap
            if sMap == "Contigs":  # physMap,phys
                bReorderingAndReorientationMap2 = True
            GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                myMaps.Genotypes,
                GeneticMap,
                sMap,
                bReorderingAndReorientationMap2=bReorderingAndReorientationMap2,
                cutOffToShow=cutOffToShow,
            )

        def detailedComparisonOfTwoMaps___run(GeneticMap1, GeneticMap2):  # (on x, on y)
            # similar to GenomeMapComparisonGraph_2maps___runSimple()
            vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                myMaps.Genotypes, GeneticMap1, GeneticMap2, 0, 0, 0
            )

            iType = 0  # oxford
            bAll_and_intialOrientation = True
            GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                GeneticMap1.GenomeMapComparisonGraph_map,
                GeneticMap2.GenomeMapComparisonGraph_map,
                vmarker,
                iType,
                bAll_and_intialOrientation,
            )

            sMap1 = GeneticMap1.sNameOfMap
            sMap2 = GeneticMap2.sNameOfMap
            sFileName = (
                myMaps.sPath
                + "TableOfMarkers_byMaps_"
                + sMap1
                + "_vs_"
                + sMap2
                + ".txt"
            )
            GenomeMapComparisonGraph.printTableOfMarkers(sFileName)
            sFileName = myMaps.sPath + "TableOfMaps_" + sMap1 + "_vs_" + sMap2 + ".txt"
            GenomeMapComparisonGraph.printTableOfMaps(sFileName)

        GenomeMapComparisonGraph = clGenomeMapComparisonGraph()
        sData = "Camponotus"
        # sData="Lasius"
        sData = "Formica glacialis"
        sData = "Nylanderia fulva"
        sData = "Camponotus_fellah"

        if False:  # sData=="Lasius":
            index = 3
            myMaps = self.clMapsAlexandra(sData)
            if index == 1:  # Lasius: males vs. mix
                sPathOutput = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\maps"
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(
                    "Males",
                    "Mix",
                    myMaps.GM_LasiusMales_Alex,
                    myMaps.GM_LasiusMix_Alex,
                    sPathOutput,
                )
            if index == 2:  # Lasius: males vs. workers
                sPathOutput = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\20220728"
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(
                    "Males",
                    "Workers",
                    myMaps.GM_LasiusMales_Alex,
                    myMaps.GM_LasiusWorkers_Alex,
                    sPathOutput,
                )
            if index == 3:  # Lasius: Vova vs. mix
                sPathOutput = (
                    "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\vova"
                )
                # s56p949025 -> Scaffold56___949025
                for Marker in myMaps.GM_LasiusMix_Alex.vMarker:
                    s = Marker.sName[1:]
                    ss = s.split("p")
                    Marker.sName = "Scaffold" + ss[0] + "___" + ss[1]
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(
                    "Vova",
                    "MixAlexandra",
                    myMaps.GM_Lasius_Vova,
                    myMaps.GM_LasiusMix_Alex,
                    sPathOutput,
                )

                sFileName = sPathOutput + "\\TableOfMarkers_byMaps_vova_vs_Alex.txt"
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName, Genotypes)
        if (
            sData == "Camponotus"
            or sData == "Camponotus_fellah"
            or sData == "Formica glacialis"
            or sData == "Nylanderia fulva"
        ):

            myMaps = self.clMapsAlexandra(sData)
            sTask = "testLinkages"
            sTask = "detailed comparison of two maps"
            if sTask == "testLinkages":
                index = 1
                if index == 0:  # testDistancesByChromosomes
                    sFileNameOut = myMaps.sPath + "testDistancesByChromosomes.txt"
                    myMaps.physMap.testDistancesByChromosomes(
                        sFileNameOut, myMaps.Genotypes
                    )
                if index == 1:  # TestLinkages: Vova
                    testLinkages___run(myMaps.GM_Vova, "Vova")
                if index == 2:  # TestLinkages: Physical
                    testLinkages___run(myMaps.physMap, "Contigs")
                if index == 3:  # TestLinkages: MST
                    testLinkages___run(myMaps.GM_MST, "MST")
                if index == 4:  # TestLinkages: Alan or Alex
                    testLinkages___run(myMaps.GM_1)
            if sTask == "detailed comparison of two maps":
                index = 4
                if index == 1:  # detailed comparison: vova vs Phys
                    detailedComparisonOfTwoMaps___run(myMaps.GM_Vova, myMaps.physMap)
                if index == 2:  # detailed comparison: MST vs Phys
                    detailedComparisonOfTwoMaps___run(myMaps.GM_MST, myMaps.physMap)
                if index == 3:  # detailed comparison: MST vs Vova
                    detailedComparisonOfTwoMaps___run(myMaps.GM_MST, myMaps.GM_Vova)
                if index == 4:  # detailed comparison: 1 vs Vova
                    detailedComparisonOfTwoMaps___run(myMaps.GM_1, myMaps.GM_Vova)
                if index == 5:  # detailed comparison: 1 vs physMap
                    detailedComparisonOfTwoMaps___run(myMaps.GM_1, myMaps.physMap)
                if index == 6:  # detailed comparison: 1 vs 2
                    detailedComparisonOfTwoMaps___run(myMaps.GM_1, myMaps.GM_2)

    def OLDAlexandra_map_testOLD___compare3maps(self):
        def testLinkages___run(GeneticMap, sMap):
            cutOffToShow = 0.3
            if sData == "Camponotus":
                cutOffToShow = 0.2
            if sData == "Nylanderia fulva":
                cutOffToShow = 0.12
            bReorderingAndReorientationMap2 = False
            if sMap == "Contigs":
                bReorderingAndReorientationMap2 = True
            GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                myMaps.Genotypes,
                GeneticMap,
                sMap,
                bReorderingAndReorientationMap2=bReorderingAndReorientationMap2,
                cutOffToShow=cutOffToShow,
            )

        GenomeMapComparisonGraph = clGenomeMapComparisonGraph()
        sData = "Camponotus"
        # sData="Lasius"
        sData = "Formica glacialis"
        sData = "Nylanderia fulva"
        if False:  # sData=="Camponotus":
            index = 4
            myMaps = self.clMapsAlexandra(sData)
            if index == 0:  # detailed comparison: vova vs Alexandra20220703
                vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                    myMaps.Genotypes,
                    myMaps.GM_Camponotus_Vova,
                    myMaps.GM_Camponotus_Alex_1,
                    0,
                    1,
                    0,
                )

                iType = 0  # oxford
                bAll_and_intialOrientation = True
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                    myMaps.GMC_Camponotus_Vova,
                    myMaps.GMC_Camponotus_Alex_1,
                    vmarker,
                    iType,
                    bAll_and_intialOrientation,
                )

                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\20220705\\TableOfMarkers_byMaps_vova_vs_Alex.txt"
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName)
                sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\20220705\\TableOfMaps.txt"
                GenomeMapComparisonGraph.printTableOfMaps(sFileName)
            if (
                index == 1
            ):  # Figure only: Alexandra20220705SkeletonOnly vs Alexandra20220705
                vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                    myMaps.Genotypes,
                    myMaps.GM_Camponotus_Alex_1,
                    myMaps.GM_Camponotus_Alex_2,
                    1,
                    1,
                    0,
                )

                iType = 0  # oxford
                bAll_and_intialOrientation = True
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                    myMaps.GMC_Camponotus_Alex_1,
                    myMaps.GMC_Camponotus_Alex_2,
                    vmarker,
                    iType,
                    bAll_and_intialOrientation,
                )
            if index == 2:  # TestLinkages: Alex
                cutOffToShow = 0.3
                GeneticMap = myMaps.GM_Camponotus_Alex_1
                sMap = "Alex0705"
                indexMarkerNameTransform = 1
                GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                    myMaps.Genotypes,
                    GeneticMap,
                    sMap,
                    indexMarkerNameTransform,
                    cutOffToShow,
                )
            if index == 3:  # TestLinkages: Vova
                GeneticMap = myMaps.GM_Camponotus_Vova
                sMap = "Vova"
                indexMarkerNameTransform = 0
                cutOffToShow = 0.3
                GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                    myMaps.Genotypes,
                    GeneticMap,
                    sMap,
                    indexMarkerNameTransform,
                    cutOffToShow,
                )
            if index == 4:  # TestLinkages: MST
                GeneticMap = myMaps.GM_Camponotus_MST0
                sMap = "MST"
                indexMarkerNameTransform = 0
                cutOffToShow = 0.3
                GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                    myMaps.Genotypes,
                    GeneticMap,
                    sMap,
                    indexMarkerNameTransform,
                    cutOffToShow,
                )

        if sData == "Lasius":
            index = 3
            myMaps = self.clMapsAlexandra(sData)
            if index == 1:  # Lasius: males vs. mix
                sPathOutput = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\maps"
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(
                    "Males",
                    "Mix",
                    myMaps.GM_LasiusMales_Alex,
                    myMaps.GM_LasiusMix_Alex,
                    sPathOutput,
                )
            if index == 2:  # Lasius: males vs. workers
                sPathOutput = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\from\\20220728"
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(
                    "Males",
                    "Workers",
                    myMaps.GM_LasiusMales_Alex,
                    myMaps.GM_LasiusWorkers_Alex,
                    sPathOutput,
                )
            if index == 3:  # Lasius: Vova vs. mix
                sPathOutput = (
                    "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\Lasius_202207\\vova"
                )
                # s56p949025 -> Scaffold56___949025
                for Marker in myMaps.GM_LasiusMix_Alex.vMarker:
                    s = Marker.sName[1:]
                    ss = s.split("p")
                    Marker.sName = "Scaffold" + ss[0] + "___" + ss[1]
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(
                    "Vova",
                    "MixAlexandra",
                    myMaps.GM_Lasius_Vova,
                    myMaps.GM_LasiusMix_Alex,
                    sPathOutput,
                )

                sFileName = sPathOutput + "\\TableOfMarkers_byMaps_vova_vs_Alex.txt"
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName, Genotypes)
        if (
            sData == "Formica glacialis"
            or sData == "Camponotus"
            or sData == "Nylanderia fulva"
        ):
            myMaps = self.clMapsAlexandra(sData)

            index = 0
            if index == 0:
                print("privet")
                testLinkages___run(myMaps.GM_Vova, "Vova")
                x = 1 / 0
            # https://drive.google.com/drive/folders/1uFGz3Zj_8fgKgDGGTQydcF_5UrCQwMO0?usp=sharing

            cutOffToShow = 0.3
            if sData == "Camponotus":
                cutOffToShow = 0.2
            if sData == "Nylanderia fulva":
                cutOffToShow = 0.12

            if index == 1:  # TestLinkages: Vova
                GeneticMap = myMaps.GM_Vova
                sMap = "Vova"
                GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                    myMaps.Genotypes, GeneticMap, sMap, cutOffToShow=cutOffToShow
                )
            if index == 2:  # TestLinkages: Physical
                GeneticMap = myMaps.physMap
                sMap = "Contigs"
                GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                    myMaps.Genotypes,
                    GeneticMap,
                    sMap,
                    bReorderingAndReorientationMap2=True,
                    cutOffToShow=cutOffToShow,
                )
            if index == 3:  # testDistancesByChromosomes
                sFileNameOut = myMaps.sPath + "testDistancesByChromosomes.txt"
                myMaps.physMap.testDistancesByChromosomes(
                    sFileNameOut, myMaps.Genotypes, cutOffToShow=cutOffToShow
                )
            if index == 4:  # detailed comparison: vova vs Phys
                vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                    myMaps.Genotypes, myMaps.GM_Vova, myMaps.physMap, 0, 0, 0
                )

                iType = 0  # oxford
                bAll_and_intialOrientation = True
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                    myMaps.GMC_Vova,
                    myMaps.GMC_physMap,
                    vmarker,
                    iType,
                    bAll_and_intialOrientation,
                )

                sFileName = myMaps.sPath + "TableOfMarkers_byMaps_vova_vs_phys.txt"
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName)
                sFileName = myMaps.sPath + "TableOfMaps_vova_vs_phys.txt"
                GenomeMapComparisonGraph.printTableOfMaps(sFileName)
            if index == 5:  # TestLinkages: MST
                GeneticMap = myMaps.GM_MST
                sMap = "MST"
                GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                    myMaps.Genotypes, GeneticMap, sMap, cutOffToShow=cutOffToShow
                )
            if index == 6:  # detailed comparison: MST vs Phys
                vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                    myMaps.Genotypes, myMaps.GM_MST, myMaps.physMap, 0, 0, 0
                )

                iType = 0  # oxford
                bAll_and_intialOrientation = True
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                    myMaps.GMC_MST,
                    myMaps.GMC_physMap,
                    vmarker,
                    iType,
                    bAll_and_intialOrientation,
                )

                sFileName = myMaps.sPath + "TableOfMarkers_byMaps_MST_vs_phys.txt"
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName)
                sFileName = myMaps.sPath + "TableOfMaps_MST_vs_phys.txt"
                GenomeMapComparisonGraph.printTableOfMaps(sFileName)
            if index == 7:  # detailed comparison: MST vs Vova
                vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                    myMaps.Genotypes, myMaps.GM_MST, myMaps.GM_Vova, 0, 0, 0
                )

                iType = 0  # oxford
                bAll_and_intialOrientation = True
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                    myMaps.GMC_MST,
                    myMaps.GMC_Vova,
                    vmarker,
                    iType,
                    bAll_and_intialOrientation,
                )

                sFileName = myMaps.sPath + "TableOfMarkers_byMaps_MST_vs_Vova.txt"
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName)
                sFileName = myMaps.sPath + "TableOfMaps_MST_vs_Vova.txt"
                GenomeMapComparisonGraph.printTableOfMaps(sFileName)
            if index == 8:  # TestLinkages: Alan
                GeneticMap = myMaps.GM_1
                sMap = myMaps.GMC_1.caption
                GenomeMapComparisonGraph.TestLinkagesForSingleGeneticMap(
                    myMaps.Genotypes, GeneticMap, sMap, cutOffToShow=cutOffToShow
                )
            if index == 9:  # detailed comparison: 1 vs Vova
                vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                    myMaps.Genotypes, myMaps.GM_1, myMaps.GM_Vova, 0, 0, 0
                )

                iType = 0  # oxford
                bAll_and_intialOrientation = True
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                    myMaps.GMC_1,
                    myMaps.GMC_Vova,
                    vmarker,
                    iType,
                    bAll_and_intialOrientation,
                )

                sMap1 = myMaps.GMC_1.caption
                sFileName = (
                    myMaps.sPath + "TableOfMarkers_byMaps_" + sMap1 + "_vs_Vova.txt"
                )
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName)
                sFileName = myMaps.sPath + "TableOfMaps_" + sMap1 + "_vs_Vova.txt"
                GenomeMapComparisonGraph.printTableOfMaps(sFileName)
            if index == 10:  # detailed comparison: 1 vs physMap
                vmarker = GenomeMapComparisonGraph.vmarker_namesFromGenotypes_posOnTwoGeneticMaps___get(
                    myMaps.Genotypes, myMaps.GM_1, myMaps.physMap, 0, 0, 0
                )

                iType = 0  # oxford
                bAll_and_intialOrientation = True
                GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___run(
                    myMaps.GMC_1,
                    myMaps.GMC_physMap,
                    vmarker,
                    iType,
                    bAll_and_intialOrientation,
                )

                sMap1 = myMaps.GMC_1.caption
                sFileName = (
                    myMaps.sPath + "TableOfMarkers_byMaps_" + sMap1 + "_vs_physMap.txt"
                )
                GenomeMapComparisonGraph.printTableOfMarkers(sFileName)
                sFileName = myMaps.sPath + "TableOfMaps_" + sMap1 + "_vs_physMap.txt"
                GenomeMapComparisonGraph.printTableOfMaps(sFileName)

    def Camponotus_genomes_comparison(self):
        MarkersWithMultiplePos = clMarkersWithMultiplePos()
        #
        # MyData=self.MyData
        # sFileName="C:\\Frenkel\\Privman\\Cnig_gn1\\formica_exsecta\\formica_exsecta_assembled_transcriptome_v1.fasta"
        MarkersWithMultiplePos.addMapFromFasta("transcriptome_formica_exsecta")
        MarkersWithMultiplePos.addMarkers_Dist(
            "transcriptome_formica_exsecta", x0=50, d=1000
        )
        sOriginalDataName = "transcriptome_formica_exsecta"
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            sOriginalDataName, "Camponotus_fedtschenkoi"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            sOriginalDataName, "Camponotus_fellah"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            sOriginalDataName, "Camponotus_floridanus"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            sOriginalDataName, "Camponotus_japonicus"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            sOriginalDataName, "Camponotus_nicobarensis"
        )
        MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
            sOriginalDataName, "Camponotus_singularis"
        )
        sPath = (
            "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\genomes\\"
        )
        """
		vsFastaRes=[]
		vsFastaRes.append(sPath+"res_formica_transcriptome_vs_Camponotus_fedtschenkoi_e100.txt")
		vsFastaRes.append(sPath+"res_formica_transcriptome_vs_Camponotus_fellah_e100.txt")
		vsFastaRes.append(sPath+"res_formica_transcriptome_vs_Camponotus_floridanus_e100.txt")
		vsFastaRes.append(sPath+"res_formica_transcriptome_vs_Camponotus_japonicus_e100.txt")
		vsFastaRes.append(sPath+"res_formica_transcriptome_vs_Camponotus_nicobarensis_e100.txt")
		vsFastaRes.append(sPath+"res_formica_transcriptome_vs_Camponotus_singularis_e100.txt")
		"""
        # "Camponotus_fellah"
        "c/Frenkel/Privman/Alexandra/GeneticMaps/"
        # /cygdrive/c/Frenkel/Privman/Alexandra/GeneticMaps/camponotus_202205/vova202209/VCF/CoorControl.txt
        sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\VCF\\CoorControl.txt"
        GM_Vova = clGeneticMap()  # Camponotus_fellah genetic map
        GM_Vova.readFromFile_coorControl(
            sFileName, "Vova"
        )  # scaffold1|size19413119___1700327
        #
        MarkersWithMultiplePos.addMarkersWithNameOfSeqContigInTheName(
            GM_Vova.vsMarkerName, "Camponotus_fellah"
        )
        MarkersWithMultiplePos.addGeneticMap_from_geneticMap(GM_Vova, "GM_Vova")
        iMapOk = MarkersWithMultiplePos.iMap("Camponotus_fellah")
        iMapToImpute = MarkersWithMultiplePos.iMap("GM_Vova")
        MarkersWithMultiplePos.imputation(
            iMapOk, iMapToImpute
        )  # put more physicalmarkers to genetic map

        sFileName = sPath + "fff.txt"
        MarkersWithMultiplePos.printToFile(sFileName, True)

        viMap = []
        vbMapProven = []
        vsMap = [
            "GM_Vova",
            "Camponotus_fellah",
            "Camponotus_fedtschenkoi",
            "Camponotus_floridanus",
            "Camponotus_japonicus",
            "Camponotus_nicobarensis",
            "Camponotus_singularis",
        ]
        for sMap in vsMap:
            iMap = MarkersWithMultiplePos.iMap(sMap)
            viMap.append(iMap)
            vbMapProven.append(False)
        MarkersWithMultiplePos.searchForProvenDifferencesBetweenTheMaps(
            viMap, vbMapProven, sPath
        )
        return

        GenomeMapComparisonGraph = clGenomeMapComparisonGraph()
        return

        # ne nado
        sMap1 = "GM_Vova"
        # sMap2="Camponotus_fellah"
        sMap2 = "Camponotus_fedtschenkoi"
        # sMap2="GM_Vova"
        GM1 = MarkersWithMultiplePos.GeneticMap__get(sMap1)
        GM2 = MarkersWithMultiplePos.GeneticMap__get(sMap2)
        # GM1.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
        # GM2.GenomeMapComparisonGraph_map___make(GenomeMapComparisonGraph)
        # GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(sMap1,sMap1,GM1,GM1,sPath)
        # GenomeMapComparisonGraph.GenomeMapComparisonGraph_2maps___runSimple(sMap1,sMap2,GM1,GM2,sPath)

        vsMap = ["GM_Vova", "Camponotus_fellah", "Camponotus_fedtschenkoi"]
        vsMap = [
            "GM_Vova",
            "Camponotus_fellah",
            "Camponotus_fedtschenkoi",
            "Camponotus_floridanus",
            "Camponotus_japonicus",
            "Camponotus_nicobarensis",
            "Camponotus_singularis",
        ]
        vsMap = [
            "Camponotus_fellah",
            "Camponotus_fedtschenkoi",
            "Camponotus_floridanus",
            "Camponotus_japonicus",
            "Camponotus_nicobarensis",
            "Camponotus_singularis",
        ]
        # vsMap=["GM_Vova","Camponotus_fedtschenkoi"]
        # GenomeMapComparisonGraph.GenomeMapComparisonGraph_severalMaps(MarkersWithMultiplePos,vsMap,viReordering_and_reorientation=[])
        GenomeMapComparisonGraph.GenomeMapComparisonGraphOxford_severalMaps(
            MarkersWithMultiplePos,
            vsMap,
            vsColor=[],
            viReordering_and_reorientation=[],
            vbChromosomes=[],
        )

    def Five_genomes_comparison(self):
        MarkersWithMultiplePos = clMarkersWithMultiplePos()
        #
        # MyData=self.MyData
        # sFileName="C:\\Frenkel\\Privman\\Cnig_gn1\\formica_exsecta\\formica_exsecta_assembled_transcriptome_v1.fasta"
        # MarkersWithMultiplePos.addMapFromFasta("proteins_Lasius_niger")
        MarkersWithMultiplePos.addMarkers_FastaOnly("proteins_Lasius_niger")
        # return
        sOriginalDataName = "proteins_Lasius_niger"
        vsGenome = [
            "Formica",
            "Camponotus_fellah",
            "Cnig_gn3.1",
            "Lasius_niger",
            "Solenopsis_invicta",
        ]
        # vsGenome=["Formica"]
        for sGenome in vsGenome:
            MarkersWithMultiplePos.addMapFromFasta(sGenome)
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                sOriginalDataName, sGenome
            )
        sPath = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\blastres\\"

        if False:
            # "Camponotus_fellah"
            "c/Frenkel/Privman/Alexandra/GeneticMaps/"
            # /cygdrive/c/Frenkel/Privman/Alexandra/GeneticMaps/camponotus_202205/vova202209/VCF/CoorControl.txt
            sFileName = "C:\\Frenkel\\Privman\\Alexandra\\GeneticMaps\\camponotus_202205\\vova202209\\VCF\\CoorControl.txt"
            GM_Vova = clGeneticMap()  # Camponotus_fellah genetic map
            GM_Vova.readFromFile_coorControl(
                sFileName, "Vova"
            )  # scaffold1|size19413119___1700327
            #
            MarkersWithMultiplePos.addMarkersWithNameOfSeqContigInTheName(
                GM_Vova.vsMarkerName, "Camponotus_fellah"
            )
            MarkersWithMultiplePos.addGeneticMap_from_geneticMap(GM_Vova, "GM_Vova")
            iMapOk = MarkersWithMultiplePos.iMap("Camponotus_fellah")
            iMapToImpute = MarkersWithMultiplePos.iMap("GM_Vova")
            MarkersWithMultiplePos.imputation(
                iMapOk, iMapToImpute
            )  # put more physicalmarkers to genetic map

        sFileName = sPath + "fff.txt"
        MarkersWithMultiplePos.printToFile(sFileName, True)
        # return

        if False:
            viMap = []
            vbMapProven = []
            vsMap = [
                "GM_Vova",
                "Camponotus_fellah",
                "Camponotus_fedtschenkoi",
                "Camponotus_floridanus",
                "Camponotus_japonicus",
                "Camponotus_nicobarensis",
                "Camponotus_singularis",
            ]
            for sMap in vsMap:
                iMap = MarkersWithMultiplePos.iMap(sMap)
                viMap.append(iMap)
                vbMapProven.append(False)
            MarkersWithMultiplePos.searchForProvenDifferencesBetweenTheMaps(
                viMap, vbMapProven, sPath
            )
            return

        GenomeMapComparisonGraph = clGenomeMapComparisonGraph()
        vsMap = vsGenome
        GenomeMapComparisonGraph.GenomeMapComparisonGraphOxford_severalMaps(
            MarkersWithMultiplePos,
            vsMap,
            vsColor=[],
            viReordering_and_reorientation=[],
            vbChromosomes=[],
        )

    def pairOfGenome_comparison_simple_run(self, filesNames):
        sDataGenes = "transcriptome_formica_exsecta"
        sDataGenome1 = "Camponotus_floridanus"
        sDataGenome2 = "Camponotus_japonicus"
        sFileNameFasta_genes = filesNames[0]
        sFileNameFasta_Genome1 = filesNames[1]
        sFileNameFasta_Genome2 = filesNames[2]
        sFileNameBlast_Genome1 = filesNames[3]
        sFileNameBlast_Genome2 = filesNames[4]

        sPath = ""

        self.pairOfGenome_comparison_simple(
            sDataGenes,
            sDataGenome1,
            sDataGenome2,
            sFileNameFasta_genes,
            sFileNameFasta_Genome1,
            sFileNameFasta_Genome2,
            sFileNameBlast_Genome1,
            sFileNameBlast_Genome2,
            sPath,
        )

    def pairOfGenome_comparison_simple(
        self,
        sDataGenes,
        sDataGenome1,
        sDataGenome2,
        sFileNameFasta_genes,
        sFileNameFasta_Genome1,
        sFileNameFasta_Genome2,
        sFileNameBlast_Genome1,
        sFileNameBlast_Genome2,
        sPath,
    ):
        MarkersWithMultiplePos = clMarkersWithMultiplePos()
        MarkersWithMultiplePos.addMarkers_FastaOnly(
            sDataGenes, bTillFirstSpaceOnly=True, sFileNameFasta=sFileNameFasta_genes
        )

        sOriginalDataName = sDataGenes
        vsGenome = [sDataGenome1, sDataGenome2]
        vsFileNameFasta_Genome = [sFileNameFasta_Genome1, sFileNameFasta_Genome2]
        vsFileNameBlast = [sFileNameBlast_Genome1, sFileNameBlast_Genome2]
        iGenome = 0
        for sGenome in vsGenome:
            MarkersWithMultiplePos.addMapFromFasta(
                sGenome, vsFileNameFasta_Genome[iGenome]
            )
            MarkersWithMultiplePos.addPhysicalMap_byBlastResults(
                sOriginalDataName,
                sGenome,
                vsFileNameBlast[iGenome],
                sFileNameFasta_genes,
            )
            iGenome += 1
        sFileName = sPath + "fff.txt"
        MarkersWithMultiplePos.printToFile(sFileName, True)

        GenomeMapComparisonGraph = clGenomeMapComparisonGraph()
        vsMap = vsGenome
        GenomeMapComparisonGraph.GenomeMapComparisonGraphOxford_severalMaps(
            MarkersWithMultiplePos,
            vsMap,
            vsColor=[],
            viReordering_and_reorientation=[],
            vbChromosomes=[],
        )

    def test_Haldane(self):
        Recombination = clRecombination()
        f = open("Haldane.txt", "w")
        for i in range(200):
            s = str(i) + "\t" + str(Recombination.rByDist(i))
            f.write(s + "\n")
        f.close()

    def vovaCurrentRun(self, filesName):
        print("privet Vova")

        # g,sPath,vLG=self.currentTask_buildGeneticMap()

        # self.renameGenesOfTal()
        # self.selectAnnotatetGenesForQTLsFromTablesOnly()
        # self.PavelSopelkinDihaploidData()
        # self.GWAS_()

        # 2021.03
        # self.testFastaFile(10)
        #
        # index=0
        # index=11
        # index=9
        index = 22
        # self.summaryOfBlastResults_byIndex(index)
        # self.select_Chr16()
        # self.makeMarkerPositionOnNewAssembly()

        # self.makeFilePosOfAllMarkersOnAllMaps("Solenopsis_invicta",[],"MarkersWithMultiplePos_Solenopsis_invicta.txt")

        # sss=self.SecCtgsByName("asm",False)
        # print str(len(sss.vCtg[0].seq[0]))

        # self.anchor_contigs_to_geneticMap_and_make_my_assembly()
        # self.aaaaa()
        # self.print_bim_file_forPnina_run()

        # self.vcfAparnaUpdate()
        # self.newPositionsOfMarkersInFile_vcf(False)

        # 2021.04.08
        # PilonResults=clPilonResults()
        # PilonResults.readFromFile()

        # 2021.09.30
        # TwoBlastResFormat0=clTwoBlastResFormat0()
        # self.add_JAJUXC_JAJUXE()
        # self.testAssemblyByLDMap()

        # self.testAssemblyByGeneticMap()

        # self.selectPartsFromGffFiles()

        # self.geneticMap_Alexandra_1()
        # self.geneticMap_Alexandra_2()
        # self.geneticMap_Alexandra_3()

        # sFileNameFasta=self.MyData.vFasta[17].sFileNameFasta
        # self.printReportOnFastaFile_run(sFileNameFasta)

        # GenomeMapComparisonGraph=clGenomeMapComparisonGraph()
        # GenomeMapComparisonGraph.test()
        # self.test_Haldane()

        # self.Alexandra_map_test___compare3maps()
        # self.Camponotus_genomes_comparison()
        # self.Five_genomes_comparison()
        self.pairOfGenome_comparison_simple_run(filesName)

        print("poka Vova")


def startComparison(filesNames):
    test = clTestsVova()
    test.testCurrent()
    vmanLab = clPrivmanLab()
    vmanLab.vovaCurrentRun(filesNames)


def sort_by_x(arrays):
    return sorted(arrays, key=lambda x: x[0][0])


def sort_by_y(arrays):
    return sorted(arrays, key=lambda x: x[0][1])


# bNotForMe=True

bNotForMe = False
"""
if not bNotForMe:
	test=clTestsVova()
	test.testCurrent()
	PrivmanLab=clPrivmanLab()
	PrivmanLab.vovaCurrentRun(filesName)
    
else:
	PrivmanLab=clPrivmanLab()
	PrivmanLab.newPositionsOfMarkersInFile_vcf(True)
"""
filesNames = ["", "", "", "", ""]

app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()
widget.setWindowTitle("GnMap")
widget.setWindowIcon(QtGui.QIcon("icon.png"))
window = Window()

t1 = threading.Thread(target=WindowInit, args=(window,))
t2 = threading.Thread(target=startComparison, args=(filesNames,))

ui = UI(filesNames)
widget.addWidget(ui)


widget.setMinimumHeight(900)
widget.setMinimumWidth(1400)
widget.show()

app.exec_()

