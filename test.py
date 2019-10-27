from json_parser import JsonParser
j = JsonParser()
l = j.parse(None, 1, "./", "front")
print(l[0].get_frame_no())
print(l[0].get_confidence_level(0))
