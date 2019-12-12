from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QFont
from subprocess import Popen
from functools import partial

def on_button_clicked(ty, view):
    handler = Popen(["python3", "demo_2.py", ty, view])


app = QApplication([])
window = QWidget()
window.resize(800,600)

#layout = QVBoxLayout()

layout = QGridLayout()
label = QLabel('Welcome to CVPosture')
font = QFont('Arial', 15)
label.setFont(font)
# define 4 types of button
pushup_left_button = QPushButton('PUSH UP - left view')
pushup_left_button.clicked.connect(partial(on_button_clicked, "pushup", "left"))
pushup_left_button.resize(200,100)

pushup_front_button = QPushButton('PUSH UP - front view')
pushup_front_button.clicked.connect(partial(on_button_clicked, "pushup", "front"))

squat_left_button = QPushButton('SQUAT - left view')
squat_left_button.clicked.connect(partial(on_button_clicked, "squat", "left"))

squat_front_button = QPushButton('SQUAT - front view')
squat_front_button.clicked.connect(partial(on_button_clicked, "squat", "front"))


layout.addWidget(label)
layout.addWidget(pushup_left_button)
layout.addWidget(pushup_front_button)
layout.addWidget(squat_left_button)
layout.addWidget(squat_front_button)

window.setLayout(layout)
window.show()
app.exec_()


