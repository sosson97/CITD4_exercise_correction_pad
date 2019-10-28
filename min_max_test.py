from json_parser import JsonParser
from video_processor import VideoProcessor
from feedback import FeedbackSystem

j = JsonParser()
video = j.parse("flare3", 200, "json/learn", "front", [0,0])
vp = VideoProcessor(video)
angles = vp.compute_left_elbow_angle(0.4)
fs = FeedbackSystem()
out = fs.min_max(angles)
print(out)

