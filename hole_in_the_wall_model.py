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
    MASK_NAMES = ['first_mask', 'first_mask']

    def __init__(self):
        self._mask_and_joints = []
        for mask in self.MASK_NAMES:
            frame = cv.imread(f'images/masks/{mask}.png')
            cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            frame = cv.resize(frame, (640, 480))
            joints = f'mask_joint_positions/{mask}.csv'
            self._mask_and_joints.append((frame, joints))
        self._joint_positions = {}
        self._joint_candidates = []
        self._joint_subsets = []
        self._total_score = 0
        self._trial_score = 0

    @property
    def total_score(self):
        return self._total_score
        
    @property
    def trial_score(self):
        return self._trial_score
    
    def num_holes_remaining(self):
        return len(self._mask_and_joints)

    def get_mask_and_joints(self):
        index = random.randint(0, len(self._mask_and_joints)-1)
        random_mask_and_joint = self._mask_and_joints[index]
        self._mask_and_joints.pop(index)
        return random_mask_and_joint[0], random_mask_and_joint[1]

    def analyze_frame(self, frame):
        self._joint_candidates, self._joint_subsets = self.BODY_ESTIMATION(frame)

    def parse_for_joint_positions(self):
        for index, value in enumerate(self._joint_subsets[0]):
            if value >= 0:
                self._joint_positions[f'{index}'] = [self._joint_candidates[int(value)][0], self._joint_candidates[int(value)][1]]
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
        self._total_score += accuracy/joint_counts * 100
        self._trial_score = accuracy/joint_counts * 100
    
    def check_win(self):
        if self._trial_score >= 50:
            return True
        return False