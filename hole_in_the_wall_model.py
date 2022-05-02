"""

"""
from deep_pose.body import Body
import csv
import numpy as np

class HoleInTheWallGame:
    """
    """

    BODY_ESTIMATION = Body('deep_pose/body_pose_model.pth')

    def __init__(self, mask_paths, csv_paths):
        self._joint_positions = {}
        self._joint_candidates = []
        self._joint_subsets = []

    @property
    def joint_candidates(self):
        """
        """
        return self._joint_candidates

    @property
    def joint_subsets(self):
        """
        """
        return self._joint_subsets

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