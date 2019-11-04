import pygame
import time

# you must match sampling rate / bit / channel number in pre_init
pygame.mixer.pre_init(44100, 16, 1, 4096)
pygame.mixer.init()

while True:
	pygame.mixer.Sound("test.wav").play()
	time.sleep(3)
