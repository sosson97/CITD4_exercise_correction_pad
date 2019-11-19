from json_parser import JsonParser
from video_processor import VideoProcessor
from feedback import FeedbackSystem
from pathlib import Path
import subprocess
import os, re, sys
import time

openpose_demo_path = "../openpose/build/examples/openpose/openpose.bin"
camera_offset = 0
json_dir = "../json/output"
model_dir = "../openpose/models"

# 3. Give feedback
"""
try: 
	j = JsonParser()
	print("Start 3 push-up")
	video = j.parse(None, 100 , json_dir, "front", None)
	fds.feedback_kmeans(video)
	handler.terminate()
except:
	print("Exception Occured")
	handler.terminate()
"""



""" 
Qt GUI Part
"""

from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout\
		, QVBoxLayout, QWidget, QLabel, QStackedWidget, QSizePolicy
from PyQt5.QtGui import QFont, QWindow
from PyQt5.QtCore import QSize, Qt
from subprocess import Popen
from functools import partial

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 800

     


class OpenPoseWidget(QWidget):
    def __init__(self, exer, view):
        super(OpenPoseWidget, self).__init__()
        self.main_layout = QHBoxLayout()
        self.op_layout = QHBoxLayout()
        self.control_layout = QVBoxLayout()

        self.start_control = 0

        # op_layout
        op_tmp = QLabel('Please push Start button')
        op_tmp.setAlignment(Qt.AlignCenter)

        self.op_layout.addWidget(op_tmp)

        # contorl_layout
        sub1_layout = QHBoxLayout() 
        sub2_layout = QVBoxLayout()

        start = QPushButton('Start')
        stop = QPushButton('Stop')
        start.setFixedSize(QSize(150,75))
        stop.setFixedSize(QSize(150,75))
        start.clicked.connect(partial(self.run_op_screen, exer, view))
        stop.clicked.connect(partial(self.stop_op_screen))
        
        sub1_layout.addWidget(start)
        sub1_layout.addWidget(stop)

        label1 = QLabel("You choose " + exer + "_" + view + " mode." )
        label1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        label2 = QLabel("Please push Start button to run CVPosture." + \
                        "\nIt may take a few seconds to load.")
        label2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        font = QFont('Arial', 13)
        label1.setFont(font)
        label2.setFont(font)

        sub2_layout.addWidget(label1)
        sub2_layout.addWidget(label2)

        self.control_layout.addLayout(sub1_layout)
        self.control_layout.addLayout(sub2_layout)

        # main_layout
        self.main_layout.addLayout(self.op_layout)
        self.main_layout.addLayout(self.control_layout)

        self.setLayout(self.main_layout)

    def run_op_screen(self, exer, view):
        if self.start_control is 1:
            return

        # clear op_layout
        self.start_control = 1
        for i in reversed(range(self.op_layout.count())):
            self.op_layout.itemAt(i).widget().setParent(None)

        # run OpenPose
        for f in os.listdir(json_dir):
            os.remove(os.path.join(json_dir, f))

        self.op_handler = subprocess.Popen([openpose_demo_path, "--camera=" + str(camera_offset), "--net_resolution=128x128", "--write_json=" + json_dir, "--model_folder=" + model_dir, "--number_people_max=1"], shell=False)

        # add widget!
        winid = self.get_op_winid()
        while winid is -1:
            winid = self.get_op_winid() 
        op_window = QWindow.fromWinId(winid)
        op_window.setFlags(Qt.FramelessWindowHint)
        op_widget = QWidget.createWindowContainer(op_window)
        self.op_layout.addWidget(op_widget)

    def stop_op_screen(self):
        if self.start_control is 0:
            return
        
        self.op_handler.terminate()
        self.start_control = 0
        for i in reversed(range(self.op_layout.count())):
            self.op_layout.itemAt(i).widget().setParent(None)
        
        op_tmp = QLabel('Please push Start button')
        op_tmp.setAlignment(Qt.AlignCenter)
        self.op_layout.addWidget(op_tmp)




    def get_op_winid(self):
        tmp1w = open("tmp1", "w")
        tmp1r = open("tmp1", "r")
        tmp2w = open("tmp2", "w")
        tmp2r = open("tmp2", "r")

        subprocess.call(['wmctrl', '-lp'], stdout=tmp1w)
        subprocess.call(['grep', 'OpenPose'], stdin=tmp1r, stdout=tmp2w)
        l = tmp2r.readline().split()
       
        out = 0
        if (len(l) is 0):
            out = -1
        else:
            out = int(l[0], base=16)


        tmp1w.close()
        tmp1r.close()
        tmp2w.close()
        tmp2r.close()
        return out


class MenuWidget(QWidget):
    def __init__(self):
        super(MenuWidget, self).__init__()
        self.main_layout = QVBoxLayout()
        self.stack_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        
        self.stack = QStackedWidget()

        self.buttons = []
        

        """ title design """
        title_widget = QWidget()
        title_layout = QVBoxLayout()
        title = QLabel('Welcome to CVPosture')
        title.setAlignment(Qt.AlignCenter)
        font = QFont('Arial', 25)
        title.setFont(font)
 
        expl1 = QLabel('This app will correct your posture using modern Computer Vision technique')
        expl2 = QLabel('Please choose one option you want to be checked')
        font = QFont('Arial', 17)
        expl1.setFont(font)
        expl2.setFont(font)

        title_layout.addWidget(title)
        title_layout.addWidget(expl1)
        title_layout.addWidget(expl2)
        title_widget.setLayout(title_layout)

        """ Stack generation"""
        self.stack.addWidget(title_widget)


        """ Button Install """
        # define 4 types of button
        
        types = [('pushup', 'left'), ('pushup', 'front'), ('squat', 'left'), ('squat', 'front')]
        for i, ty in enumerate(types):
            exer = ty[0]
            view = ty[1]
            self.stack.addWidget(OpenPoseWidget(exer,view))

            if exer == 'pushup':
                name = 'PUSH UP'
            if exer == 'squat':
                name = 'SQUAT'
            
            bt_name = name + ' - ' + view + ' view'

            bt = QPushButton(bt_name)
            bt.clicked.connect(partial(self.display, i+1))
            bt.setFixedSize(QSize(200,100))
            self.buttons.append(bt)

        for bt in self.buttons:
            self.button_layout.addWidget(bt)

        self.stack_layout.addWidget(self.stack)

        self.main_layout.addLayout(self.stack_layout)
        self.main_layout.addLayout(self.button_layout)

        # main layout
        self.setLayout(self.main_layout)
        self.resize(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.setWindowTitle("CVPosture")
        self.show()

    def display(self, i):
        self.stack.setCurrentIndex(i)


if __name__ == "__main__":
    app = QApplication([])
    
    menu = MenuWidget() 
    app.exec_()

