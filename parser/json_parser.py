import cv2
import numpy as np
import json
#'right', 'front'
view = 'right'
num_points = 25


filenames = []
for i in range(100):
	str_i = None
	if (i < 10):
		str_i = "0" + str(i)
	else:
		str_i = str(i)
	filenames.append("pushup8_0000000000" + str_i + "_keypoints.json")
point4 = None
point7 = None

for input_filename in filenames:
	with open(input_filename, "r") as f:
		jf = json.load(f)
		point_source = jf['people'][0]['pose_keypoints_2d']
		points = []
		for i in range(num_points):
			points.append((int(point_source[i*3]), int(point_source[i*3 + 1])))
		
		if point4 is None:
			point4 = points[4]
		if point7 is None:
			point7 = points[7]

		img = np.zeros([1080,1920,3], np.uint8)
		if view is 'front':
			cv2.line(img, points[1], points[2], (0,255,0), thickness=5)
			cv2.line(img, points[2], points[3], (0,255,0),thickness=5)
			cv2.line(img, points[3], point4, (0,255,0),thickness=5)
			cv2.line(img, points[1], points[5], (0,255,0),thickness=5)
			cv2.line(img, points[5], points[6], (0,255,0),thickness=5)
			cv2.line(img, points[6], point7, (0,255,0),thickness=5)
		elif view is 'right':
			cv2.line(img, points[1], points[2], (0,255,0), thickness=5)
			cv2.line(img, points[2], points[3], (0,255,0),thickness=5)
			cv2.line(img, points[3], point4, (0,255,0),thickness=5)
			cv2.line(img, points[1], points[8], (0,255,0),thickness=5)
			cv2.line(img, points[8], points[9], (0,255,0),thickness=5)
			cv2.line(img, points[9], points[10], (0,255,0),thickness=5)
			cv2.line(img, points[10], points[11], (0,255,0),thickness=5)
			
		cv2.imshow('img',img)
		cv2.waitKey(10)


