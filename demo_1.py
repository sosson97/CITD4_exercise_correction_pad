"""
This code demonstrates simple learning and feedback process for wrong push-up posture.  
For the intermediate presentations use only. 
"""
from json_parser import JsonParser
from feedback import FeedbackSystem
from pathlib import Path


# 1. learning FeedbackSystem with pre-labelled push-up data
fds = FeedbackSystem()
j = JsonParser()
front_videos_with_label = [("correct1", 1), ("correct2", 1), ("correct3", 0), ("flare1", 1), ("flare2", 0), ("flare3", 0)]
for video_with_label in front_videos_with_label:
    path = Path("../json/" + video_with_label[0])
    video = j.parse(video_with_label[0], 200 , path, "front", video_with_label[1])
    fds.learn(video)

fds.save("demo_front_model", "front");
