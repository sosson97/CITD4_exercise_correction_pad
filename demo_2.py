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

openpose_demo_path = "../openpose/build/examples/openpose/openpose.bin"
camera_offset = 0
json_dir = "../json/output"
model_dir = "../openpose/models"

fds = FeedbackSystem()
fds.load("demo_front_model", "front")
for f in os.listdir(json_dir):
	os.remove(os.path.join(json_dir, f))

# 2. Run Openpose Webcam Mode
handler = subprocess.Popen([openpose_demo_path, "--disable_blending=true","--camera=" + str(camera_offset), "--net_resolution=128x128", "--write_json=" + json_dir, "--model_folder=" + model_dir, "--number_people_max=1"], shell=False)


# 3. Give feedback
#try: 
j = JsonParser()
print("Start 3 push-up")
video = j.parse(None, 20 , json_dir, "front", None)
fds.feedback_kmeans(video)
handler.terminate()
#except:
#	print("Exception Occured")
#		handler.terminate()

