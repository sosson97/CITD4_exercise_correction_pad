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

files = ["r0e0ns1",
"r0e0ns2",
"r0e0ns3",
"r0e0ws1",
"r0e0ws2",
"r0e0ws3",
"r0e1ns1",
"r0e1ns2",
"r0e1ws1",
"r0e1ws2",
"r0e1ws3",
"r1e0ns1",
"r1e0ns2",
"r1e0ns3",
"r1e0ns4",
"r1e0ws1",
"r1e0ws2",
"r1e0ws3",
"r1e1ns1",
"r1e1ns2",
"r1e1ns3",
"r1e1ws1",
"r1e1ws2",
"r1e1ws3"]

for filename in files:
	json_dir = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\code\\json\\" + filename
	j = JsonParser()
	count = len(os.listdir(json_dir))
	print(count)
	video = j.parse(filename, count , json_dir, "pushup", None)
	vp = VideoProcessor(video)
	vp.compute_left_arm_angle_with_floor(0.5)
	vp.dump_csv()

