import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np

import util
from body import Body
import pdb
import cv2 as cv
import csv

body_estimation = Body('deep_pose/body_pose_model.pth')

cap = cv2.VideoCapture(0)
isTrue, oriImg = cap.read()
# cv.imshow("video", oriImg)
cap.release()

candidate, subset = body_estimation(oriImg)
canvas = copy.deepcopy(oriImg)
canvas = util.draw_bodypose(canvas, candidate, subset)

all_hand_peaks = []

plt.imshow(canvas[:, :, [2, 1, 0]])
plt.axis('off')
plt.show()
# pdb.set_trace()

"""
TODO:
- compare stored dictionary fo joint positions to current trial
- options for oding this: raw do the pixels match up (lol not gonna work)
- or do find distance, score is proportional to the distance
- or implement a threshold
- also look out for data types in the csv file, no idea why the list is in a string lol
"""

joint_positions = {}

pdb.set_trace()

for index, value in enumerate(subset[0]):
    if value >= 0:
        joint_positions[f'{index}'] = [candidate[int(value)][0], candidate[int(value)][1]]
    if index >= 17:
        break



with open('pose_test_one.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    for key, value in joint_positions.items():
        csv_writer.writerow([key, value])

pdb.set_trace()