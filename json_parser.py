# json_parser.py
"""
1. This file has two classes FrameInfo and JsonParser
2. JsonParser class which parses raw json file from OpenPose to concrete data structure. 
3. Output data structure is FrameInfo type and can be used by other module of project.
"""


# import list
import sys
from pathlib import Path
import os
import time
import json
# import end

class FrameInfo():
    def __init__(self, frame_no, confidence_levels, point_locations):
        self.frame_no = frame_no
        self.confidence_levels = confidence_levels
        self.point_locations = point_locations
    def get_frame_no(self):
        return self.frame_no
    def get_confidence_level(self, i):
        if i >= len(self.confidence_level):
            return -1
        return self.confidence_levels[i]
    def get_point_location(self, i):
        if i >= len(self.point_locations):
            return -1
        return self.point_locations[i]
    def get_label(self, i):
        if i >= len(self.label):
            return -1
        return self.label[i]

class VideoInfo():
    def __init__(self, view, label)
        self.view = view
        self.label = label
        self.frames = []
    def get_frame_len(self):
        return len(self.frames)
    def get_frame(self, i):
        if i >= len(self.frames):
            return -1
        return self.frames[i]
    def append_frame(self, fi):
        last_frame_no = self.get_frame(self.get_frame_len()-1).get_frame_no()
        new_frame_no = fi.get_frame_no()
        if last_frame_no >= new_frame_no:
            print("Error: wrong frame number appended")
            return
        self.frames.append(fi)
    



class JsonParser():
    def parse(self, source, limit_frame_no, directory, view, label):
        """
        Description:
            parse() returns a list of FrameInfo containing information of frames of  given input source(video or webcam)

        Args:
            source : video_name or webcam if None 
            limit_frame_no : maximum frame number that will be processed.
            directory : directory path of stored json output
            view : ...
            label : labelling for current input. It currently has only 2 features: 0 elbow flare, 1 not all the way down and up 

        Returns: 
            A VideoInfo"""
        if (limit_frame_no > 999):
            sys.exit("JsonParser doesn't support limit_frame_no larger than 999") 
    
    
        video = VideoInfo(view, label)
        for i in range(limit_frame_no):
            filename = None
            str_i = str(i)
            
            # determine filename
            if (i < 10):
                if (source is None):
                    filename = "000000000000" + str_i
                else:
                    filename = source + "_000000000000" + str_i + "_keypoints.json"
            if (i < 100):
                if (source is None):
                    filename = "00000000000" + str_i + "_keypoints.json"
                else:
                    filename = source + "_00000000000" + str_i + "_keypoints.json"
            else:
                if (source is None):
                    filename = "0000000000" + str_i + "_keypoints.json"
                else:
                    filename = source + "_0000000000" + str_i + "_keypoints.json"
            
            # set file path and check it exists
            filepath = Path(os.path.join(directory, filename))
            # blocking until this file generated
            # timeout 10 seconds
            timeout_count = 0
            while not filepath.is_file():
                time.sleep(1)
                timeout_count = timeout_count+1
                if timeout_count > 10:
                    error_msg = "JsonParser timeout in " + str(filepath)
                    sys.exit(error_msg)
            
            # open the file and gather information
            f = open(filepath, "r")
            jf = json.load(f)
            f.close()
     
            if not jf['people']:
                # this frame didn't capture any information
                continue
            


            point_source = jf['people'][0]['pose_keypoints_2d']
            confidence_levels = []
            point_locations = []
            
            num_points = int(len(point_source)/3)
            for j in range(num_points):
                point_locations.append((int(point_source[j*3]), int(point_source[j*3+1])))
                confidence_levels.append(point_source[j*3+2])
            
            fi = FrameInfo(i, confidence_levels, point_locations)
            video.append_frame(fi)
            
            # iteration done
        return video
            
