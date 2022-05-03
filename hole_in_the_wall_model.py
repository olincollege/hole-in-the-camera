"""

"""
from deep_pose.body import Body
import csv
import numpy as np
import cv2 as cv
import pdb
import random

class HoleInTheWallGame:
    """
    """

    BODY_ESTIMATION = Body('deep_pose/body_pose_model.pth')
    path_mask = "images/masks/"
    path_csv = "mask_joint_positions/"
    CSV_PATHS = ["pose_test_1.csv"]
    JOINT_FITS = []
    for joints_csv in CSV_PATHS:
        with open(f'{path_csv}{joints_csv}', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                JOINT_FITS.append(row)

    def __init__(self):
        self.masks = []
        self._MASK_PATHS = ["new_mask.png"]
        for mask in self._MASK_PATHS:
            frame = cv.imread(f'{self.path_mask}{mask}')
            cv.cvtColor(frame, cv.COLOR_BGR2RGB, frame)
            frame = cv.resize(frame, (640, 480))
            self.masks.append(frame)
        self._joint_positions = {}
        self._joint_candidates = []
        self._joint_subsets = []
        self._score = 0

    def get_mask(self):
        mask_index = random.randint(0, len(self.masks)-1)
        random_mask = self.masks[mask_index]
        self.masks.pop(mask_index)
        return random_mask

    def analyze_frame(self, frame):
        self._joint_candidates, self._joint_subsets = self.BODY_ESTIMATION(frame)

    def parse_for_joint_positions(self):
        for index, value in enumerate(self._joint_subsets[0]):
            if value >= 0:
                self._joint_positions[f'{index}'] = [self._candidate[int(value)][0], self._joint_candidates[int(value)][1]]
            else:
                self._joint_positions[f'{index}'] = [-1, -1]
            if index >= 17:
                break
    
    def compute_accuracy(self, saved_csv_for_mask):
        accuracy = 0
        joint_fits = []
        joint_counts = 0

        with open(saved_csv_for_mask, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                joint_fits.append(row)
        for joint in joint_fits:
            if joint[0] in self._joint_positions.keys() and self._joint_positions[joint[0]][1] != '-1':
                joint_counts += 1
                reference_joint_position = np.array([int(float(joint[1])), int(float(joint[2]))])
                user_joint_position = np.array(self._joint_positions[joint[0]])

                distance = np.linalg.norm(reference_joint_position - user_joint_position)

                if distance < 20:
                    accuracy +=1
                elif distance < 30:
                    accuracy += .5
                elif distance < 40:
                    accuracy += 0.25
        return accuracy/joint_counts
    
    def check_win(self,score):
        if score >= 0.5:
            return True
        return False