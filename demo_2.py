"""
This code demonstrates simple learning and feedback process for wrong push-up posture.  
For the intermediate presentations use only. 
"""
from json_parser import JsonParser
from video_processor import VideoProcessor
from feedback import FeedbackSystem
from pathlib import Path
import subprocess

openpose_demo_path = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose\\bin\\OpenPoseDemo.exe"
camera_offset = 0
json_dir = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\code\\json\\output"
model_dir = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose\\models"
fds = FeedbackSystem()
fds.load("demo_front_model", "front")

# 2. Run Openpose Webcam Mode
handler = subprocess.Popen([openpose_demo_path, "--camera=" + str(camera_offset), "--net_resolution=128x128", "--write_json=" + json_dir, "--model_folder=" + model_dir], shell=False)

# 3. Give feedback
j = JsonParser()
print("Start 3 push-up")
video = j.parse(None, 100 , json_dir, "front", None)
handler.terminate()
fds.feedback_kmeans(video)

