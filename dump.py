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

files = ["output"]

for filename in files:
	json_dir = "../json/" + filename
	j = JsonParser()
	count = len(os.listdir(json_dir))
	print(count)
	video = j.parse(None, count , json_dir, "pushup", None)
	vp = VideoProcessor(video)
	vp.compute_left_elbow_angle(0.5)
	vp.dump_csv()

