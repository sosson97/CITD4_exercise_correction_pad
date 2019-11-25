# feedback.py
"""
1. This file contains FeedbackSystem class which has several feedback functions
"""

from pathlib import Path
from video_processor import VideoProcessor
from sklearn.cluster import KMeans
import numpy as np
import pickle
import sys

class FeedbackSystem():
    def __init__(self):
        self.front_data = []
        self.left_data = []
        self.div_zero = 0

    def save(self, filename, view):
        with open(filename, "wb") as f:
            if view == "front":
                pickle.dump(self.front_data, f)
            elif view == "left":
                pickle.dump(self.left_data, f)
            else:
                sys.exit("Error: Wrong view type is given")
    def load(self, filename, view):
        with open(filename, "rb") as f:
            if view == "front":
                self.front_data = pickle.load(f)
            elif view == "left":
                self.left_data = pickle.load(f)
            else:
                sys.exit("Error: Wrong view type is given")



    def min_max(self, mat, view, ty):
        """
        Description: Find 3 local minimum and maximum from angle graph then return their average repectively as a tuple
        """
        mins = []
        maxs = []
       
        for i in range(len(mat)):
            if (i < 5) or (i > len(mat) - 5):
                continue
            cur_angle = mat[i][1]
            
            # filter error data
            if cur_angle == 0:
                continue
            
            # threshold
            min_threshold = 360
            max_threshold = 0
            if view == "front" and ty == "elbow":
                min_threshold = 80
                max_threshold = 130
            elif view == "front" and ty == "shoulder":
                min_threshold = 120
                max_threshold = 120 
            elif view == "front" and ty == "arm":
                min_threshold = 180
                max_threshold = 0
            elif view == "left":
                min_threshold = 90
                max_threshold = 130
            elif view == "squat":
                min_threshold = 100
                max_threshold = 100
            else:
                sys.exit("Error: Wrong view type is given")

            if view == "squat":
                is_local_minima = (cur_angle <= mat[i-1][1] or mat[i-1][1] == 0) and \
                (cur_angle <= mat[i-2][1] or mat[i-2][1] == 0) and \
                (cur_angle <= mat[i-3][1] or mat[i-3][1] == 0) and \
                (cur_angle <= mat[i-4][1] or mat[i-4][1] == 0) and \
                (cur_angle <= mat[i-5][1] or mat[i-5][1] == 0) and \
                (cur_angle <= mat[i-6][1] or mat[i-6][1] == 0) and \
                (cur_angle <= mat[i-7][1] or mat[i-7][1] == 0) and \
                (cur_angle <= mat[i+1][1] or mat[i+1][1] == 0) and \
                (cur_angle <= mat[i+2][1] or mat[i+2][1] == 0) and \
                (cur_angle <= mat[i+3][1] or mat[i+3][1] == 0) and \
                (cur_angle <= mat[i+4][1] or mat[i+4][1] == 0) and \
                (cur_angle <= mat[i+5][1] or mat[i+5][1] == 0) and \
                (cur_angle <= mat[i+6][1] or mat[i+6][1] == 0) and \
                (cur_angle <= mat[i+7][1] or mat[i+7][1] == 0) and \
                cur_angle <= min_threshold 
            else:
                is_local_minima = (cur_angle <= mat[i-1][1] or mat[i-1][1] == 0) and \
                (cur_angle <= mat[i-2][1] or mat[i-2][1] == 0) and \
                (cur_angle <= mat[i-3][1] or mat[i-3][1] == 0) and \
                (cur_angle <= mat[i-4][1] or mat[i-4][1] == 0) and \
                (cur_angle <= mat[i+1][1] or mat[i+1][1] == 0) and \
                (cur_angle <= mat[i+2][1] or mat[i+2][1] == 0) and \
                (cur_angle <= mat[i+3][1] or mat[i+3][1] == 0) and \
                (cur_angle <= mat[i+4][1] or mat[i+4][1] == 0) and \
                cur_angle <= min_threshold 

            if is_local_minima:
                is_dup = 0
                for entry in mins:
                    if entry == cur_angle:
                        is_dup = 1
                if not is_dup:
                    mins.append(cur_angle)

            if view == "squat":
                is_local_maxima = (cur_angle >= mat[i-1][1]) and \
                (cur_angle >= mat[i-2][1]) and \
                (cur_angle >= mat[i-3][1]) and \
                (cur_angle >= mat[i-4][1]) and \
                (cur_angle >= mat[i-5][1]) and \
                (cur_angle >= mat[i+1][1]) and \
                (cur_angle >= mat[i+2][1]) and \
                (cur_angle >= mat[i+3][1]) and \
                (cur_angle >= mat[i+4][1]) and \
                (cur_angle >= mat[i+5][1]) and \
                cur_angle >= max_threshold
            else:
                is_local_maxima = (cur_angle >= mat[i-1][1]) and \
                (cur_angle >= mat[i-2][1]) and \
                (cur_angle >= mat[i-3][1]) and \
                (cur_angle >= mat[i+1][1]) and \
                (cur_angle >= mat[i+2][1]) and \
                (cur_angle >= mat[i+3][1]) and \
                cur_angle >= max_threshold
            
            if is_local_maxima:
                is_dup = 0
                for entry in maxs:
                    if entry == cur_angle:
                        is_dup = 1
                if not is_dup:
                    maxs.append(cur_angle)


            # end point
            if len(mins) >= 3 and len(maxs) >= 3:
                break
        print(mins)
        print(maxs)
        if (len(mins) is 0) or (len(maxs) is 0):
            self.div_zero = 1
            return 0
        return [sum(mins)/len(mins), sum(maxs)/len(maxs)]

    def learn(self, video, threshold=0.8):
        vp = VideoProcessor(video)
        if vp.get_video_view() == "front": # you need 5-dimensional data in front case
            elbow_angle_result = vp.compute_left_elbow_angle(threshold)
            shoulder_angle_result = vp.compute_left_shoulder_angle(threshold)
            arm_angle_result = vp.compute_left_arm_angle_with_floor(threshold)

            min_max_1 = self.min_max(elbow_angle_result, "front", "elbow")
            min_max_2 = self.min_max(shoulder_angle_result , "front", "shoulder")
            min_max_3 = self.min_max(arm_angle_result, "front", "arm")
            
            if (self.div_zero is 1):
                    print("training data is erronous, div-zero happend. This data is not added")
                    self.div_zero = 0
                    return
            #only min is used for shoulder angle
            min_max = min_max_1 + [min_max_2[0]] + min_max_3
            self.front_data.append(((min_max), vp.get_video_label()))
        elif vp.get_video_view() == "left":
            angle_result = vp.compute_left_elbow_angle(threshold)
            min_max = self.min_max(angle_result, "left")
            self.left_data.append(((min_max), vp.get_video_label()))
        elif vp.get_video_view() == "squat":
            angle_result = vp.compute_left_knee_angle(threshold)
            min_max = self.min_max(angle_result, "squat")
            self.left_data.append(((min_max), vp.get_video_label()))
        else:
            sys.exit("Error: Wrong view type is given")
        print(video.get_name() + " has been successfully learned.")
    def feedback_kmeans(self, video, threshold=0.8):
        # input video may have None label
        vp = VideoProcessor(video)
        if vp.get_video_view() == "front": # you need 6-dimensional data in front case
            elbow_angle_result = vp.compute_left_elbow_angle(threshold)
            shoulder_angle_result = vp.compute_left_shoulder_angle(threshold)
            arm_angle_result = vp.compute_left_arm_angle_with_floor(threshold)

            min_max_1 = self.min_max(elbow_angle_result, "front", "elbow")
            min_max_2 = self.min_max(shoulder_angle_result , "front", "shoulder")
            min_max_3 = self.min_max(arm_angle_result, "front", "arm")
            
            if (self.div_zero is 1):
                    sys.exit("training data is erronous, div-zero happend")

            min_max = min_max_1 + [min_max_2[0]] + min_max_3

            training_data = [t[0] for t in self.front_data] 
            
            # expect two clusters; one for full reps, another one for partial reps
            km = KMeans(n_clusters=8, random_state=0).fit(np.array(training_data))
            
            cluster = km.predict(np.array([np.array(min_max)]))
            #label format [partial range or not, elbow flare or not, wide or not]
            
            # majority voting
            labels = km.labels_
            training_labels = [t[1] for t in self.front_data] 
            positive_labels_num = [0, 0, 0]
            negative_labels_num = [0, 0, 0]
            for i in range(len(labels)):
                if labels[i] == cluster:
                    print(str(i))
                    print(training_labels[i])
                    for j in range(len(positive_labels_num)):
                        if training_labels[i][j] == 1:
                            positive_labels_num[j] = positive_labels_num[j] + 1
                        else:
                            negative_labels_num[j] = negative_labels_num[j] + 1
            result = []
            for i in range(len(positive_labels_num)):
                result.append(positive_labels_num[i] > negative_labels_num[i])

            return result