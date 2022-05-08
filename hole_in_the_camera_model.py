"""
This is the model for the hole in the camera game. This script relies on a
public github repository (pytorch-openpose) in order to analyze inputted camera
frames for human body positions. Open Pose is a machine learning algorithm
that can analyze an image for joint positions in terms of pixel locations for
each joint. This repository can be found at this link:
https://github.com/Hzzone/pytorch-openpose
"""
import csv
import random
import cv2 as cv
import numpy as np
from deep_pose.body import Body

class HoleInTheCameraGame:
    """
    Hole in the wall game model with helper functions that dictate gameflow.

    Attributes:
        BODY_ESTIMATION (Body): Body estimation object from open pose.
        MASK_NAMES (list): List of names of each mask, represented as strings.
        _mask_and_joints (list): List of tuples, where each tuple contains the
            string file path to the mask that a user should fit into and a
            string file path to the csv that stores the joint positions users
            need to match.
        _joint_positions (dict): Dictionary of joint positions, where each key
            is an integer representing a joint (joint to integer conversions
            can be found in the openpose github) and each value is a list of
            doubles representing the pixel location of a joint on a given
            image.
        _joint_candidates (list): 2-D list of all joints, their positions, and
            the confidence of the open pose neural network, for every joint
            detected within the image inputted to open pose.
        _joint_subsets (list): 2-D list of all the joints associated with each
            person detected within the inputted image. This list contains joint
            indexes, separated by person, within the joint_candidates list and
            can be parsed to determine all the joints for each person.
        _trial_score (double): The computed score of the user's fit for the
            most recently played trial in the game.
        _total_score (double): The computer score of the user's fit for all
            trials played up to the current condition of the game.
    """

    # Instance of Body class from open pose that will be used to analyze frames.
    BODY_ESTIMATION = Body('deep_pose/body_pose_model.pth')

    # List of each mask that will be available for users to play with.
    MASK_NAMES = ['first_mask', 'second_mask', 'third_mask',
                  'fourth_mask', 'fifth_mask', 'sixth_mask', 'seventh_mask']

    def __init__(self):
        """
        This is the constructor for the HoleInTheCamera class. The constructor
        creates _mask_and_joints based on the class attribute of all the mask
        names, initializes the variables that map joint positions to empty
        lists/dictionaries and initializes the score variables to 0.
        """
        # Assembles tuples that store paths to the image mask and the joint
        # positions csv and stores them to a list.
        self._mask_and_joints = []
        for mask in self.MASK_NAMES:
            # Each image can be found in the images/masks folder.
            frame = cv.imread(f'images/masks/{mask}.png')
            # By default. OpenCV stores images as BGR and need to be converted
            # to properly display them in pygame.
            cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            # Images need to be resized to ensure images fit the screen.
            frame = cv.resize(frame, (640, 480))
            joints = f'mask_joint_positions/{mask}.csv'
            self._mask_and_joints.append((frame, joints))
        self._joint_positions = {}
        self._joint_candidates = []
        self._joint_subsets = []
        self._total_score = 0
        self._trial_score = 0

    @property
    def joint_positions(self):
        """
        Return the joint_positions dictionary stored by this HoleInTheCamera
        instance.
        """
        return self._joint_positions

    @property
    def joint_candidates(self):
        """
        Return the joint_candidates list stored by this HoleInTheCamera
        instance.
        """
        return self._joint_candidates

    @property
    def joint_subsets(self):
        """
        Return the joint_subsets list stored by this HoleInTheCamera instance.
        """
        return self._joint_subsets

    @property
    def mask_and_joints(self):
        """
        Return the mask_and_joints list stored by this HoleInTheCamera
        instance.
        """
        return self._mask_and_joints

    @property
    def total_score(self):
        """
        Return the total_score value stored by this HoleInTheCamera instance.
        """
        return self._total_score

    @property
    def trial_score(self):
        """
        Return the trial_score value stored by this HoleInTheCamera instance
        for the most recent game trial.
        """
        return self._trial_score

    def num_holes_remaining(self):
        """
        This function computes the number of masks remaining for the user to
        play with, which corresponds to the length of the _mask_and_joints
        variable.

        Returns:
            (int): The number of masks remaining to be played.
        """
        return len(self._mask_and_joints)

    def get_mask_and_joints(self):
        """
        This function randomly selects and returns a mask to the game runner
        to be displayed in the next trial for the user.

        Returns:
            (str): A string that represents the path to the mask that the user
                will have to fit into next.
            (str): A string that represents the path to the joint positions csv
                that will be used to test the accuracy of a user's fit.
        """
        # If there is only one mask left, automatically assign the index to be
        # returned to 0.
        if len(self._mask_and_joints) == 1:
            index = 0
        else:
            index = random.randint(0, len(self._mask_and_joints)-1)
        random_mask_and_joint = self._mask_and_joints[index]
        # Remove the mask and joint tuple from the list to ensure that it isn't
        # replayed during the same game iteration.
        self._mask_and_joints.pop(index)
        return random_mask_and_joint[0], random_mask_and_joint[1]

    def analyze_frame(self, frame):
        """
        This function analyzes the inputted frame for potential joints and
        stores them to _joint_candidates and _joint_subsets by calling the
        open pose object within this class.

        Args:
            frame (numpy.ndarray): A 3-D numpy array that represents the RGB
                values of the frame to be analyzed by open pose. This frame
                array should be of size 480x640x3.
        """
        self._joint_candidates, self._joint_subsets = self.BODY_ESTIMATION(
            frame)

    def parse_for_joint_positions(self):
        """
        This function is called after a frame is analyzed and potential joints
        are populated to _joint_candidates and _joint_subsets. This function
        assumes only one person is in the camera frame during analysis and
        parses through _joint_candidates and _joint_subsets and assembles them
        into one dictionary. If a joint was not found in the image, it is
        mapped to [-1, -1].
        """
        if len(self.joint_subsets) > 0:
            for index, value in enumerate(self._joint_subsets[0]):
                # Value will be -1 if the joint is not present in the image.
                if value >= 0:
                    self._joint_positions[f'{index}'] = [
                        self._joint_candidates[int(value)][0], self._joint_candidates[int(value)][1]]
                else:
                    self._joint_positions[f'{index}'] = [-1, -1]
                # After 16, the _joint_subsets variable contains information
                # about the data and accuracy, but is not useful for mapping
                # joint positions so it is ignored.
                if index > 16:
                    break

    def compute_accuracy(self, saved_csv_for_mask):
        """
        This function computes how accurately a user was able to fit into the
        mask they were presented with based on the joint positions csv.

        Args:
            saved_csv_for_mask (str): A path to the csv file that contains the
                joint positions that the user should have matched in order to
                have had a successful trial.
        """
        accuracy = 0
        joint_fits = []
        joint_counts = 0

        # Reads and stores the saved joint positions to compare against the
        # user's joint positions.
        with open(saved_csv_for_mask, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                joint_fits.append(row)
        for joint in joint_fits:
            # Ensures that comparisons are only made with joints that are
            # present.
            if joint[0] in self._joint_positions.keys() and\
                self._joint_positions[joint[0]][1] != '-1':
                joint_counts += 1
                reference_joint_position = np.array(
                    [int(float(joint[1])), int(float(joint[2]))])
                user_joint_position = np.array(self._joint_positions[joint[0]])
                # Calculates the Euclidian distance (in pixels) between the
                # saved joint positions and the user's joint positions.
                distance = np.linalg.norm(
                    reference_joint_position - user_joint_position)

                # Gives users a score based on how well they fit, where a
                # perfect match (distance is less than 20 pixels) corresponds
                # to a perfect score.
                if distance < 30:
                    accuracy += 1
                elif distance < 40:
                    accuracy += .5
                elif distance < 50:
                    accuracy += 0.25
        # Updates the _total_score and _trial_score variables with the results
        # of this trial.
        self._total_score += accuracy/joint_counts * 100
        self._trial_score = accuracy/joint_counts * 100

    def check_win(self):
        """
        This function determines if the most recent trial was a successful
        trial for the user and should be run after compute_accuracy.

        Returns:
            (bool): True if the user was successful in their last trial and
                false if they weren't.
        """
        if self._trial_score >= 70:
            return True
        return False
