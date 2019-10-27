# video_processor.py
"""
1. This file contains a class VideoProcessor.
2. It gets a VideoInfo as an argument and prcoesses it using implemented operations.
3. All video processing functions should be implemented here.
4. After executing a processing function, the result will be stored in self.result and can be dumped to csv file using dump_csv function.
5. self.result is cleared before every execution.
"""


# import list
import csv
import math
import os
from pathlib import Path
import numpy as np

# import end

class VideoProcessor():
    def __init__(self, vi):
        self.video = vi
        self.result = []
        self.last_operation = ""
    def clear_result(self):
        self.result = []
    def dump_csv(self, dir=None):
        filename = self.video.get_name() + "_" +  self.last_operation + ".csv" 
        cur_path = Path(os.getcwd())
        path = None
        if dir is None:
            path = cur_path.joinpath(filename)
        else:
            dir_path = Path(dir)
            if dir_path.is_absolute():
                path = dir_path.joinpath(filename)
            else:
                path = cur_path.joinpath(dir_path).joinpath(filename) 
        with open(path, "wb") as f:
            writer = csv.writer(f, delimiter=',')
            for line in self.result:
                writer.writerow(line)


    # processing function
    def compute_left_elbow_angle(self, confidence_threshold=0.8):
        self.clear_result() 

        # for each frame
        fixed_7 = None
        for i in range(self.video.get_frame_len()):
            frame = self.video.get_frame(i)
            point_num_list = [5,6]
            
            if not frame.check_confidence(point_num_list, confidence_threshold):
                # pass this frame
                continue
            
            if fixed_7 is None:
                point_num_list = [7]
                if not frame.check_confidence(point_num_list, confidence_threshold):
                    # pass this frame
                    continue
                else:
                    fixed_7 = frame.get_point_location(7)
            
            point_5 = np.array(frame.get_point_location(5))
            point_6 = np.array(frame.get_point_location(6))
            point_7 = fixed_7

            vector_56 = np.array(point_5 - point_6)
            vector_76 = np.array(point_7 - point_6)
            
            vector_56_dot_vector_76 = vector_56[0]*vector_76[0] + vector_56[1]*vector_76[1]
            vector_56_norm = np.linalg.norm(vector_56)
            vector_76_norm = np.linalg.norm(vector_76)
            
            if (vector_56_norm > 0) and (vector_76_norm > 0):
                left_angle = math.acos(vector_56_dot_vector_76 / (vector_56_norm * vector_76_norm)) * 180 / math.pi
            else:
                left_angle = 0 
            
            self.result.append((frame.get_frame_no(), left_angle))

        self.last_operation = "left_elbow_angle"
        return self.result
     
    # processing function
    def compute_left_shoulder_angle(self, confidence_threshold=0.8):
        self.clear_result() 

        # for each frame
        for i in range(self.video.get_frame_len()):
            frame = self.video.get_frame(i)
            point_num_list = [1,5,6]
            
            if not frame.check_confidence(point_num_list, confidence_threshold):
                # pass this frame
                continue
            
           
            point_1 = np.array(frame.get_point_location(1))
            point_5 = np.array(frame.get_point_location(5))
            point_6 = np.array(frame.get_point_location(6))

            vector_15 = np.array(point_1 - point_5)
            vector_65 = np.array(point_6 - point_5)
            
            vector_15_dot_vector_65 = vector_15[0]*vector_65[0] + vector_15[1]*vector_65[1]
            vector_15_norm = np.linalg.norm(vector_15)
            vector_65_norm = np.linalg.norm(vector_65)
            
            if (vector_15_norm > 0) and (vector_65_norm > 0):
                left_angle = math.acos(vector_15_dot_vector_65 / (vector_15_norm * vector_65_norm)) * 180 / math.pi
            else:
                left_angle = 0 
            
            self.result.append((frame.get_frame_no(), left_angle))

        self.last_operation = "left_shoulder_angle"
        return self.result

