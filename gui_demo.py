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
from PyQt5.QtGui import QFont, QWindow, QPixmap
from PyQt5.QtCore import QSize, Qt
from subprocess import Popen
from functools import partial

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720


class FeedbackMsg():
    def __init__(self, result_dict):
        self.result_dict = result_dict
        self.range = False
        self.elbowf = False
        self.wide = False
    def get_feedback_msg(self):
        msg = []
        tys = ["elbow", "arm", "shoulder"]
        if "elbow" in self.result_dict:  
            self.range = self.result_dict["elbow"]
        if "arm" in self.result_dict:
            self.elbowf = self.result_dict["arm"]
        if "shoulder" in self.result_dict: 
            self.wide = self.result_dict["shoulder"]
        
        # first element of msg is True when the posture was bad, otherwise False
        if self.range or self.elbowf:
            msg.append(True)
        else:
            msg.append(False)

        if self.range:
            msg.append("가동범위가 부족합니다. 끝까지 내려가주세요!")
        
        if self.elbowf:
            msg.append("팔꿈치에 무리가는 자세입니다. 팔꿈치가 바깥을 향하지 않도록 해주세요!")

        if self.wide:
            msg.append("가슴 근육을 타겟으로 하는 자세입니다.")
        else:
            msg.append("삼두를 타겟으로 하는 자세입니다.")

        return msg

    
        


class OpenPoseWidget(QWidget):
    def __init__(self, exer, view):
        super(OpenPoseWidget, self).__init__()
        self.main_layout = QHBoxLayout()
        self.op_layout = QVBoxLayout()
        self.control_layout = QVBoxLayout()

        self.start_control = 0

        # op_layout
        op_tmp = QLabel('Please push Start button')
        op_tmp.setAlignment(Qt.AlignCenter)

        self.op_layout.addWidget(op_tmp)

        # contorl_layout
        self.sub1_layout = QHBoxLayout() 
        self.sub2_layout = QVBoxLayout()

        start = QPushButton('Start')
        stop = QPushButton('Stop') 
        feedback = QPushButton('Feedback')

        font = QFont('Arial', 20)
        start.setFont(font)
        stop.setFont(font)
        feedback.setFont(font)



        start.setFixedSize(QSize(150,75))
        stop.setFixedSize(QSize(150,75))
        feedback.setFixedSize(QSize(150,75))
        
        start.clicked.connect(partial(self.run_op_screen, exer, view))
        stop.clicked.connect(partial(self.stop_op_screen))
        feedback.clicked.connect(partial(self.start_feedback))
        
        self.sub1_layout.addWidget(start)
        self.sub1_layout.addWidget(stop)
        self.sub1_layout.addWidget(feedback)

        msg = "" 
        if exer == 'squat':
            msg += "스쿼트를 선택하셨습니다.\n"
        else:
            msg += "푸쉬업을 선택하셨습니다.\n"

        msg += "영상 촬영을 시작하기 위해서 버튼을 눌러주세요. \n" + \
                "시작되는데 15초 가량 소요될 수 있습니다."

        label1 = QLabel(msg)
        label1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        font = QFont('Arial', 15)
        label1.setFont(font)

        self.exer_img = QLabel()
        if exer == 'squat':
            self.exer_img.setPixmap(QPixmap("../pictures/squat.JPG").scaledToWidth(320))
        else:
            self.exer_img.setPixmap(QPixmap("../pictures/pushup.JPG").scaledToWidth(320))

    
        self.exer_img.setAlignment(Qt.AlignCenter)


        self.sub2_layout.addWidget(self.exer_img)
        #self.sub2_layout.addWidget(label1)
        #self.sub2_layout.addWidget(label2)



        #self.control_layout.addLayout(self.sub1_layout)
        self.control_layout.addLayout(self.sub2_layout)

        
        right_layout = QVBoxLayout()
        right_layout.addLayout(self.op_layout)
        right_layout.addLayout(self.sub1_layout)

        # main_layout
        self.main_layout.addLayout(self.control_layout)
        self.main_layout.addLayout(right_layout)
        #self.main_layout.addLayout(self.op_layout)

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

        for i in reversed(range(self.sub2_layout.count())):
            self.sub2_layout.itemAt(i).widget().setParent(None)
        
        ready_img = QLabel()
        ready_img.setPixmap(QPixmap("../pictures/ready.JPG").scaledToWidth(320))
        ready_img.setAlignment(Qt.AlignCenter)
        self.sub2_layout.addWidget(ready_img)


       
    def stop_op_screen(self, msg=None):
        if self.start_control is 0:
            return
        
        self.op_handler.terminate()
        self.start_control = 0
        for i in reversed(range(self.op_layout.count())):
            self.op_layout.itemAt(i).widget().setParent(None)
        
        op_tmp = QLabel(msg if msg else 'Please push Start button')
        op_tmp.setAlignment(Qt.AlignCenter)
        
        """
        if msg:
            ox_img = QLabel()
            ox_img.setPixmap(QPixmap("test.png"))
            #ox_img.show()
            self.op_layout.addWidget(ox_img)
        """
        self.op_layout.addWidget(op_tmp)


    def start_feedback(self): 
        #time.sleep(5)
        #collect data 
        
        
        print("feedback start")
        print("GET READY")
        time.sleep(3)
        print("START")

        #for i in reversed(range(self.sub2_layout.count())):
        #    self.sub2_layout.itemAt(i).widget().setParent(None)
 
        #go_img = QLabel("GO")
        #go_img.setPixmap(QPixmap("../pictures/go.JPG").scaledToWidth(320))
        #go_img.setAlignment(Qt.AlignCenter)
        #self.sub2_layout.addWidget(go_img)




        start_point = len(os.listdir(json_dir))
        j = JsonParser(start_point=start_point)
   
        # incremental try
        frame_no_list = [i*10 for i in range(4,10)]
        err = 0
        
        tys = ["elbow", "arm", "shoulder"]
        result_dict = {} 
        

        for frame_no in frame_no_list:  
            print(str(frame_no) + " frame test")
            video = j.parse(None, frame_no , json_dir, "front", None)
            result_dict = {}
            err = 0 
            for ty in tys:
                print("doing " + ty)
                fds = FeedbackSystem()
                fds.load("demo_front_" + ty + "_model", "front")
                result, div_zero = fds.feedback_kmeans(video, ty, threshold=0.3)
                if div_zero:
                    err = 1
                else:
                    result_dict[ty] = result 

            if err is 0:
                break
            
        if err is 1:
            self.stop_op_screen("Posture is not detected. Please adjust webcam position") 
            return
         
        fdm = FeedbackMsg(result_dict)
        msg = fdm.get_feedback_msg()
        #self.op_handler.terminate()


        # now print out feedback msg
        #self.stop_op_screen("Result")
              
        need_cor = msg[0]
        cor_msg = msg[1:]

        #top_layout = QVBoxLayout() 
        #bottom_layout = QVBoxLayout()

        """ 
        for m in cor_msg:  
            op_tmp = QLabel(m)
            op_tmp.setAlignment(Qt.AlignCenter)
            self.op_layout.addWidget(op_tmp)
        """
        
        for i in reversed(range(self.sub2_layout.count())):
            self.sub2_layout.itemAt(i).widget().setParent(None)
       
        if need_cor:
            bad_img = QLabel()
            bad_img.setPixmap(QPixmap("../pictures/bad.JPG").scaledToWidth(260))
            bad_img.setAlignment(Qt.AlignCenter)
            self.sub2_layout.addWidget(bad_img)
        else:
            nice_img = QLabel()
            nice_img.setPixmap(QPixmap("../pictures/nice.JPG").scaledToWidth(260))
            nice_img.setAlignment(Qt.AlignCenter)
            self.sub2_layout.addWidget(nice_img)

        feedback_msg = ""
        for m in cor_msg:  
            feedback_msg += m + "\n"

        op_tmp = QLabel(feedback_msg)
        op_tmp.setAlignment(Qt.AlignCenter)
        op_tmp.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.sub2_layout.addWidget(op_tmp)

        """
        ox_img = QLabel()
        ox_img.setPixmap(QPixmap("test.png"))
        ox_img.show()
        top_layout.addWidget(ox_img)

        for m in cor_msg:  
            op_tmp = QLabel(m)
            op_tmp.setAlignment(Qt.AlignCenter)
            bottom_layout.addWidget(op_tmp)


        self.op_layout.addLayout(top_layout)
        self.op_layout.addLayout(bottom_layout)
        """


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
        title_layout = QHBoxLayout()
        img_layout = QVBoxLayout()
        hello_img = QLabel()
        hello_img.setPixmap(QPixmap("../pictures/hello.JPG").scaledToWidth(320))
       
        text_layout = QVBoxLayout()
        name = QLabel('안녕하세요! 저는 당신의 코치 YAS입니다.')
        font = QFont('Arial', 30)
        name.setFont(font)

        expl1 = QLabel('당신이 운동하는 모습을 보여주시면 피드백을 드릴게요.')
        expl2 = QLabel('교정하고 싶은 운동을 선택해주세요')
        font = QFont('Arial', 22)
        expl1.setFont(font)
        expl2.setFont(font)

        img_layout.addWidget(hello_img)
        text_layout.addWidget(name)
        text_layout.addWidget(expl1)
        text_layout.addWidget(expl2)
        
        title_layout.addLayout(img_layout)
        title_layout.addLayout(text_layout)


        title_widget.setLayout(title_layout)

        """ Stack generation"""
        self.stack.addWidget(title_widget)


        """ Button Install """
        # define 4 types of button
        
        types = [ ('pushup', 'front'), ('squat', 'left') ]
        for i, ty in enumerate(types):
            exer = ty[0]
            view = ty[1]
            self.stack.addWidget(OpenPoseWidget(exer,view))

            if exer == 'pushup':
                name = '푸쉬업'
            if exer == 'squat':
                name = '스쿼트'
            
            bt_name = name
            
            font = QFont('Arial', 20)
            bt = QPushButton(bt_name)
            bt.setFont(font)
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
        self.setWindowTitle("YAS")
        self.show()

    def display(self, i):
        self.stack.setCurrentIndex(i)


if __name__ == "__main__":
    app = QApplication([])
    
    menu = MenuWidget() 
    app.exec_()

