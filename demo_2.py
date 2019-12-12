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


openpose_demo_path = "build/examples/openpose/openpose.bin"
camera_offset = 0
json_dir = "../json/output"
model_dir = "models"

for f in os.listdir(json_dir):
	os.remove(os.path.join(json_dir, f))

# 2. Run Openpose Webcam Mode
handler = subprocess.Popen([openpose_demo_path, "--disable_blending=false","--camera=" + str(camera_offset), "--net_resolution=128x128", "--write_json=" + json_dir, "--model_folder=" + model_dir, "--number_people_max=1"], shell=False)


print("Start 3 push-up")
tys = ["elbow", "arm", "shoulder"]
for ty in tys:
    fds = FeedbackSystem()
    fds.load("demo_front_" + ty + "_model", "front")

    # 3. Give feedback
    #try: 
    j = JsonParser()
    video = j.parse(None, 60 , json_dir, "front", None)
    result = fds.feedback_kmeans(video, ty)
    print(result)
    handler.terminate()
    #except:
    #    print("Exception Occured")
    #    handler.terminate()

