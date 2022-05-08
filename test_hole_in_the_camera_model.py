"""
Tests for the HoleInTheCameraGame class
"""

import os
import cv2
import numpy as np
from hole_in_the_camera_model import HoleInTheCameraGame


def test_initialization_mask_and_joints_length():
    """
    Tests that the mask_and_joints list has the correct number of elements.
    """
    test_model = HoleInTheCameraGame()
    assert len(test_model.mask_and_joints) == 7


def test_initialization_joints_file_paths():
    """
    Tests that the joint files are the correct file type.
    """
    test_model = HoleInTheCameraGame()
    for _, csv in test_model.mask_and_joints:
        # all paths to csv files should end in .csv
        if not csv[-4:] == ".csv":
            assert False
    assert True


def test_initialization_mask_shape():
    """
    Tests that each mask has the correct shape.
    """
    test_model = HoleInTheCameraGame()
    for image, _ in test_model.mask_and_joints:
        if np.shape(image) != (480, 640, 3):
            assert False
    assert True


def test_initialization_mask_values():
    """
    Tests that each mask has realistic RGB values.
    """
    test_model = HoleInTheCameraGame()
    for image, _ in test_model.mask_and_joints:
        if np.mean(image) >= 255 or np.mean(image) <= 0:
            assert False
    assert True


def test_num_holes_remaining_start():
    """
    Tests that the number of holes remaining is 7 at the start.
    """
    test_model = HoleInTheCameraGame()
    assert test_model.num_holes_remaining() == 7


def test_num_holes_remaining_three_trials_elapsed():
    """
    Tests that the number of holes remaining decreases correctly
    after three trials.
    """
    test_model = HoleInTheCameraGame()
    for _ in range(3):
        test_model.get_mask_and_joints()
    # after three iterations, the mask_and_joints length should also decrement
    # by 3
    assert test_model.num_holes_remaining() == 4


def test_num_holes_remaining_all_trials_elapsed():
    """
    Tests that the number of holes remaining is 0 after seven trials are done.
    """
    test_model = HoleInTheCameraGame()
    for _ in range(7):
        test_model.get_mask_and_joints()
    assert test_model.num_holes_remaining() == 0


def test_get_mask_and_joints_joint_path():
    """
    Tests that the joint path is the correct file type.
    """
    test_model = HoleInTheCameraGame()
    _, joint = test_model.get_mask_and_joints()
    assert joint[-4:] == ".csv"


def test_get_mask_and_joints_joint_exists():
    """
    Tests that the joint file returned by get_mask_and_joints is
    a valid file.
    """
    test_model = HoleInTheCameraGame()
    _, joint = test_model.get_mask_and_joints()
    assert os.path.exists(joint)


def test_get_mask_and_joints_mask_shape():
    """
    Tests that the returned mask has the correct shape.
    """
    test_model = HoleInTheCameraGame()
    mask, _ = test_model.get_mask_and_joints()
    assert np.shape(mask) == (480, 640, 3)


def test_get_mask_and_joints_mask_values():
    """
    Tests that the mask has realistic RGB values.
    """
    test_model = HoleInTheCameraGame()
    mask, _ = test_model.get_mask_and_joints()
    assert np.mean(mask) < 255 and np.mean(mask) > 0


def test_analyze_frame_black_image_joint_candidates():
    """
    Tests that deep pose does not find any joints
    for an empty black image.
    """
    test_model = HoleInTheCameraGame()
    # creates an all black image
    test_image = np.zeros([480, 640, 3])
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_candidates) == 0


def test_analyze_frame_black_image_joint_subsets():
    """
    Tests that deep pose does not return any joint subsets
    for an empty black image.
    """
    test_model = HoleInTheCameraGame()
    test_image = np.zeros([480, 640, 3])
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets) == 0


def test_analyze_frame_white_image_joint_candidates():
    """
    Tests that deep pose does not find any joints
    for a white image.
    """
    test_model = HoleInTheCameraGame()
    # creates an all white image
    test_image = np.ones([480, 640, 3]) * 255
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_candidates) == 0


def test_analyze_frame_white_image_joint_subsets():
    """
    Tests that deep pose does not return any joint subsets
    for a white image.
    """
    test_model = HoleInTheCameraGame()
    test_image = np.ones([480, 640, 3]) * 255
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets) == 0


def test_analyze_frame_no_legs_joint_candidates():
    """
    Tests that deep pose does not find extra joints
    for a mask containing only the upper body of a person.
    """
    test_model = HoleInTheCameraGame()
    # reads a stored image used to create game masks
    test_image = cv2.imread("images/poses/first_mask.png")
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_candidates) == 14


def test_analyze_frame_no_legs_num_joint_subsets():
    """
    Test that deep pose only finds one person's joint subset
    when there's only one person in the image.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets) == 1


def test_analyze_frame_no_legs_first_joint_subset():
    """
    Test that the only joint subset found by deep pose contains all
    expected information, including 17 joint positions and three
    values about the accuracy of the fit.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets[0]) == 20


def test_analyze_frame_half_upper_joint_candidates():
    """
    Tests that deep pose does not find extra joints
    for a mask containing only the upper body of a person.
    """
    test_model = HoleInTheCameraGame()
    # splits the image in half to test behavior on a cut off person
    test_image = cv2.imread("images/poses/first_mask.png")[:, 0:325, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_candidates) == 7


def test_analyze_frame_half_upper_num_joint_subsets():
    """
    Tests that deep pose only found one joint subset for an image
    with only half a person.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, :325, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets) == 1


def test_analyze_frame_half_upper_first_joint_subset():
    """
    Test that the only joint subset found by deep pose contains all
    expected information, including 17 joint positions and three
    values about the accuracy of the fit.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, :325, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets[0]) == 20


def test_analyze_frame_other_half_upper_joint_candidates():
    """
    Tests that deep pose only found one joint subset for an image
    with only the other half a person.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_candidates) == 7


def test_analyze_frame_other_half_upper_num_joint_subsets():
    """
    Tests that deep pose only found one joint subset for an image
    with only the other half a person.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets) == 1


def test_analyze_frame_other_half_upper_first_joint_subset():
    """
    Test that the only joint subset found by deep pose contains all
    expected information, including 17 joint positions and three
    values about the accuracy of the fit.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets[0]) == 20


def test_parse_for_joint_positions_black_image():
    """
    Test that when analyzing the deep pose result, there are no joint
    positions that can be found or parsed for in a black image.
    """
    test_model = HoleInTheCameraGame()
    test_image = np.zeros([480, 640, 3])
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    assert test_model.joint_positions == {}


def test_parse_for_joint_positions_white_image():
    """
    Test that when analyzing the deep pose result, there are no joint
    positions that can be found or parsed for in a white image.
    """
    test_model = HoleInTheCameraGame()
    test_image = np.ones([480, 640, 3]) * 255
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    assert test_model.joint_positions == {}


def test_parse_for_joint_positions_no_legs_joints_detected():
    """
    Test that when analyzing and parsing through the deep pose result, the
    joints that are expected to be missing (9, 10, 11, 12 as these are the leg
    joint) are mapped to a [-1, -1] position and the others are not mapped to
    [-1, -1].
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    for key, value in test_model.joint_positions.items():
        if key in ["9", "10", "12", "13"]:
            if value != [-1, -1]:
                assert False
        else:
            if value == [-1, -1]:
                assert False
    assert True


def test_parse_for_joint_positions_no_legs_found_joint_positions():
    """
    Test for when analyzing the parsing through the deep pose result, the
    existing joints (joints not in the legs) are mapped to positions that lie
    within the pixel bounds of the inputted image.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    for key, value in test_model.joint_positions.items():
        if key not in ["9", "10", "12", "13"]:
            if value[0] > 640 or value[0] < 0 or value[1] > 480 or value[1] < 0:
                assert False
    assert True


def test_parse_for_joint_positions_half_upper_joints_detected():
    """
    Test that when analyzing and parsing through the deep pose result, the
    joints that are expected to be missing (1, 5, 6, 7, 8, 9, 10, 11, 12, 13,
    18 as these are the leg joint or upper body joints that are not included in
    the inputted image) are mapped to a [-1, -1] position and the others are
    not mapped to [-1, -1].
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, :325, :]
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    for key, value in test_model.joint_positions.items():
        if key in ["1", "5", "6", "7", "8", "9", "10", "11", "12", "13", "17"]:
            if value != [-1, -1]:
                assert False
        else:
            if value == [-1, -1]:
                assert False
    assert True


def test_parse_for_joint_positions_half_upper_found_joint_positions():
    """
    Test for when analyzing the parsing through the deep pose result, the
    existing joints (joints not in the legs or half of the upper body) are
    mapped to positions that lie within the pixel bounds of the inputted image.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, :325, :]
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    for key, value in test_model.joint_positions.items():
        if key not in ['1', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                       '17']:
            if value[0] > 640 or value[0] < 0 or value[1] > 480 or value[1] < 0:
                assert False
    assert True


def test_parse_for_joint_positions_other_half_upper_joints_detected():
    """
    Test that when analyzing and parsing through the deep pose result, the
    joints that are expected to be missing (0, 2, 3, 4, 8, 9, 10, 11, 12, 13,
    14, 15, 16 as these are the leg joint or upper body joints that are not
    included in the inputted image) are mapped to a [-1, -1] position and the
    others are not mapped to [-1, -1].
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    for key, value in test_model.joint_positions.items():
        if key in ['0', '2', '3', '4', '8', '9', '10', '12', '13', '14', '15',
                   '16']:
            if value != [-1, -1]:
                assert False
        else:
            if value == [-1, -1]:
                assert False
    assert True


def test_parse_for_joint_positions_other_half_upper_found_joint_positions():
    """
    Test for when analyzing the parsing through the deep pose result, the
    existing joints (joints not in the legs or half of the upper body) are
    mapped to positions that lie within the pixel bounds of the inputted image.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    for key, value in test_model.joint_positions.items():
        if key not in ['0', '2', '3', '4', '8', '9', '10', '12', '13', '14',
                       '15', '16']:
            if value[0] > 640 or value[0] < 0 or value[1] > 480 or value[1] < 0:
                assert False
    assert True

def test_compute_accuracy_white_image_total_score():
    """
    Test that the computed fit accuracy is 0 when a white image is analyzed and
    compared to existing joint positions. Based on this computed accuracy, the
    total score should be updated to be 0.
    """
    test_model = HoleInTheCameraGame()
    test_image = np.ones([480, 640, 3]) * 255
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.total_score == 0

def test_compute_accuracy_white_image_trial_score():
    """
    Test that the computed fit accuracy is 0 when a white image is analyzed and
    compared to existing joint positions. Based on this computed accuracy, the
    trial score should be updated to be 0.
    """
    test_model = HoleInTheCameraGame()
    test_image = np.ones([480, 640, 3]) * 255
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.trial_score == 0

def test_compute_accuracy_same_image_total_score():
    """
    Test that when an image is analyzed and compared to against joint positions
    obtained from the same image, the accuracy is a 100% match and the total
    score is updated to reflect such (100).
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.total_score == 100.0


def test_compute_accuracy_same_image_trial_score():
    """
    Test that when an image is analyzed and compared to against joint positions
    obtained from the same image, the accuracy is a 100% match and the trial
    score is updated to reflect such (100).
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.trial_score == 100.0


def test_compute_accuracy_same_image_total_score_three_trials():
    """
    Test that when an image is analyzed and compared to against joint positions
    obtained from the same image, the accuracy is a 100% match three times in a
    row. This is reflected in the total score as it is updated three times with
    a score of 100, yielding a total score of 300.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.total_score == 300.0


def test_compute_accuracy_same_image_trial_score_three_trials():
    """
    Test that when an image is analyzed and compared to against joint positions
    obtained from the same image, the accuracy is a 100% match three times in a
    row. For the trial score, this should only reflect 100 as it stores the
    most recent trial score.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.trial_score == 100.0


def test_computer_accuracy_diff_image_total_score():
    """
    Test that when an image is analyzed and compared to against a different
    image's joint positions, the accuracy is below 70%. This simulates a failed
    trial of the real game where a user's position is different than the
    expected position. This is reflected by the total score being less than 70.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.total_score < 70


def test_computer_accuracy_diff_image_trial_score():
    """
    Test that when an image is analyzed and compared to against a different
    image's joint positions, the accuracy is below 70%. This simulates a failed
    trial of the real game where a user's position is different than the
    expected position. This is reflected by the trial score being less than 70.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.trial_score < 70


def test_computer_accuracy_diff_image_total_score_three_trials():
    """
    Test that when an image is analyzed and compared to against a different
    image's joint positions, the accuracy is below 70%. This is done three
    different times to ensure that total score is properly updated and has
    a value less than the passing value for three total iterations.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.total_score < 210


def test_computer_accuracy_diff_image_trial_score_three_trials():
    """
    Test that when an image is analyzed and compared to against a different
    image's joint positions three different times, the accuracy is below 70%
    and the trial score only stores the accuracy of the most recent trial.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.trial_score < 70


def test_check_win_same_image():
    """
    This function checks to make sure the model correctly determines a win when
    an image is analyzed against joints generated from the same exact image.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.check_win()


def test_check_win_diff_image():
    """
    This function checks to make sure the model correctly determines a loss
    when an image is analyzed against joints generated from a different image.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert not test_model.check_win()


def test_check_win_two_iterations():
    """
    Tests to make sure the check_win function correctly determines a win
    followed by a loss in succession.
    """
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    if not test_model.check_win():
        assert False
    test_image = cv2.imread("images/poses/second_mask.png")
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    if test_model.check_win():
        assert False
    assert True
