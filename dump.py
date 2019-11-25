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

filename = "ref_left"
json_dir = "D:\\OneDrive\\OneDrive - postech.ac.kr\\2019 Fall\\창의설계4\\code\\json\\" + filename

j = JsonParser()
video = j.parse(filename, 200 , json_dir, "pushup", None)
vp = VideoProcessor(video)
vp.compute_left_elbow_angle(0.2)
vp.dump_csv()
