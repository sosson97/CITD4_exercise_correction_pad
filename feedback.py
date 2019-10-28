# feedback.py
"""
1. This file contains FeedbackSystem class which has several feedback functions
"""


class FeedbackSystem():
    def min_max(self, mat):
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
            
            
            is_local_minima = (cur_angle < mat[i-1][1] or mat[i-1][1] == 0) and \
            (cur_angle < mat[i-2][1] or mat[i-2][1] == 0) and \
            (cur_angle < mat[i-3][1] or mat[i-3][1] == 0) and \
            (cur_angle < mat[i+1][1] or mat[i+1][1] == 0) and \
            (cur_angle < mat[i+2][1] or mat[i+2][1] == 0) and \
            (cur_angle < mat[i+3][1] or mat[i+3][1] == 0) and \
            cur_angle < 50

            if is_local_minima:
                mins.append(cur_angle)

            is_local_maxima = (cur_angle > mat[i-1][1]) and \
            (cur_angle > mat[i-2][1]) and \
            (cur_angle > mat[i-3][1]) and \
            (cur_angle > mat[i+1][1]) and \
            (cur_angle > mat[i+2][1]) and \
            (cur_angle > mat[i+3][1]) and \
            cur_angle > 120
            
            if is_local_maxima:
                maxs.append(cur_angle)


            # end point
            if len(mins) >= 3 and len(maxs) >= 3:
                break
        print(mins)
        print(maxs)
        return (sum(mins)/len(mins), sum(maxs)/len(maxs))

    def min_max_k_means():
        return

