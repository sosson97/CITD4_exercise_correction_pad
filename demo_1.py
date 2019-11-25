"""
This code demonstrates simple learning and feedback process for wrong push-up posture.  
For the intermediate presentations use only. 
"""
from json_parser import JsonParser
from feedback import FeedbackSystem
from pathlib import Path
import os

# 1. learning FeedbackSystem with pre-labelled push-up data
fds = FeedbackSystem()
j = JsonParser()

#label format [partial range or not, elbow flare or not, wide or not]
videos_with_label = [
("r0e0ns1", [0,0,0]), 
("r0e0ns2", [0,0,0]), 
("r0e0ns3", [0,0,0]), 
("r0e0ws1", [0,0,1]), 
("r0e0ws2", [0,0,1]), 
("r0e0ws3", [0,0,1]), 
("r0e1ns1", [0,1,0]), 
("r0e1ns2", [0,1,0]), 
("r0e1ws1", [0,1,1]), 
("r0e1ws2", [0,1,1]), 
("r0e1ws3", [0,1,1]), 
("r1e0ns1", [1,0,0]), 
("r1e0ns2", [1,0,0]), 
("r1e0ns3", [1,0,0]), 
("r1e0ns4", [1,0,0]), 
("r1e0ws1", [1,0,1]), 
("r1e0ws2", [1,0,1]), 
("r1e0ws3", [1,0,1]), 
("r1e1ns1", [1,1,0]), 
("r1e1ns2", [1,1,0]), 
("r1e1ns3", [1,1,0]), 
("r1e1ws1", [1,1,1]), 
("r1e1ws2", [1,1,1]), 
("r1e1ws3", [1,1,1])]

tys = ["elbow", "shoulder", "arm"]
for ty in tys:
	for video_with_label in videos_with_label:
	    path = Path("../json/" + video_with_label[0])
	    print(str(path))
	    count = len(os.listdir(path))
	    video = j.parse(video_with_label[0], count , path, "front", video_with_label[1])
	    fds.learn(video, ty, threshold=0.5)

	fds.save("demo_front_" + ty + "_model", "front");
