"""
This code demonstrates simple learning and feedback process for wrong push-up posture.  
For the intermediate presentations use only. 
"""
from json_parser import JsonParser
from video_processor import VideoProcessor
from feedback import FeedbackSystem
from pathlib import Path
import subprocess

openpose_demo_path = Path("")
camera_offset = 1
json_dir = Path("")

fds = FeedbackSystem()
fds.load("demo_front_model", "front")

# 2. Run Openpose Webcam Mode
subprocess.Popen([openpose_demo_path, "--camera=" + str(camera_offset), "--net_resolution=128x128", "-write_json=" + json_dir], shell=False)

# 3. Give feedback
j = JsonParser()
print("Start 3 push-up")
video = j.parse(video_with_label[0], 100 , path, "front", video_with_label[1])
fds.feedback_kmeans(video)

