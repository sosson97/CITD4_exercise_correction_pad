from feedback import FeedbackSystem



#label format [partial range, elbow flare, wide]
pr = 0
ef = 1
w = 0


min_dic = {}
max_dic = {}

min_dic["arm"]=70
max_dic["arm"]=76
min_dic["elbow"]=5
max_dic["elbow"]=180
min_dic["shoulder"]=94
max_dic["shoulder"]=120



tys = ["arm", "elbow", "shoulder"]

for ty in tys:
    fds = FeedbackSystem()
    fds.load("demo_front_" + ty + "_model", "front")
    fds.manual_learn([min_dic[ty], max_dic[ty]], [pr,ef,w])
    fds.save("demo_front_" + ty + "_model", "front")

