"""
This code demonstrates simple learning and feedback process for wrong push-up posture.  
For the intermediate presentations use only. 
"""
from json_parser import JsonParser
from video_processor import VideoProcessor
from feedback import FeedbackSystem
from pathlib import Path
import subprocess
import os, re

openpose_demo_path = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose\\bin\\OpenPoseDemo.exe"
camera_offset = 1
video_name = "flare1"
json_dir = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\code\\json\\" + video_name
model_dir = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose-1.5.1-binaries-win64-only_cpu-python-flir-3d\\openpose\\models"




tys = ["elbow", "arm", "shoulder"]
for ty in tys:
	fds = FeedbackSystem()
	fds.load("demo_front_" + ty + "_model", "front")

	# 2. Run Openpose Webcam Mode


	# 3. Give feedback
	j = JsonParser()
	count = len(os.listdir(json_dir)) 
	video = j.parse(video_name,  count, json_dir, "front", None)
	result = fds.feedback_kmeans(video, ty)
	print(result)