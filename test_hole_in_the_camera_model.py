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
        if not csv[-4:] == ".csv":
            assert False
    assert True


def test_initialization_mask_shape():
    """
    Tests that the mask has the correct shape.
    """
    test_model = HoleInTheCameraGame()
    for image, _ in test_model.mask_and_joints:
        if np.shape(image) != (480, 640, 3):
            assert False
    assert True


def test_initialization_mask_values():
    """
    Tests that the mask has correct RGB values.
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
    after a few trials.
    """
    test_model = HoleInTheCameraGame()
    for _ in range(3):
        test_model.get_mask_and_joints()
    assert test_model.num_holes_remaining() == 4


def test_num_holes_remaining_all_trials_elapsed():
    """
    Tests that the number of holes remaining is 0 after all trials are done.
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
    Tests that the joint returned by get_mask_and_joints is
    a valid joint.
    """
    test_model = HoleInTheCameraGame()
    _, joint = test_model.get_mask_and_joints()
    assert os.path.exists(joint)


def test_get_mask_and_joints_mask_shape():
    """
    Tests that the mask has the correct shape.
    """
    test_model = HoleInTheCameraGame()
    mask, _ = test_model.get_mask_and_joints()
    assert np.shape(mask) == (480, 640, 3)


def test_get_mask_and_joints_mask_values():
    """
    Tests that the mask has correct RGB values.
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
    test_image = cv2.imread("images/poses/first_mask.png")[:, 0:325, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_candidates) == 7


def test_analyze_frame_half_upper_num_joint_subsets():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, :325, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets) == 1


def test_analyze_frame_half_upper_first_joint_subset():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, :325, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets[0]) == 20


def test_analyze_frame_other_half_upper_joint_candidates():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_candidates) == 7


def test_analyze_frame_other_half_upper_num_joint_subsets():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets) == 1


def test_analyze_frame_other_half_upper_first_joint_subset():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")[:, 350:, :]
    test_model.analyze_frame(test_image)
    assert len(test_model.joint_subsets[0]) == 20


def test_parse_for_joint_positions_black_image():
    test_model = HoleInTheCameraGame()
    test_image = np.zeros([480, 640, 3])
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    assert test_model.joint_positions == {}


def test_parse_for_joint_positions_white_image():
    test_model = HoleInTheCameraGame()
    test_image = np.ones([480, 640, 3]) * 255
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    assert test_model.joint_positions == {}


def test_parse_for_joint_positions_no_legs_joints_detected():
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


def test_compute_accuracy_same_image_total_score():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.total_score == 100.0


def test_compute_accuracy_same_image_trial_score():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.trial_score == 100.0


def test_compute_accuracy_same_image_total_score_three_trials():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.total_score == 300.0


def test_compute_accuracy_same_image_trial_score_three_trials():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.trial_score == 100.0


def test_computer_accuracy_diff_image_total_score():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.total_score < 70


def test_computer_accuracy_diff_image_trial_score():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.trial_score < 70


def test_computer_accuracy_diff_image_total_score_three_trials():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.total_score < 210


def test_computer_accuracy_diff_image_trial_score_three_trials():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    for _ in range(3):
        test_model.analyze_frame(test_image)
        test_model.parse_for_joint_positions()
        test_model.compute_accuracy(test_csv)
    assert test_model.trial_score < 70


def test_check_win_same_image():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/first_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert test_model.check_win()


def test_check_win_diff_image():
    test_model = HoleInTheCameraGame()
    test_image = cv2.imread("images/poses/second_mask.png")
    test_csv = "mask_joint_positions/first_mask.csv"
    test_model.analyze_frame(test_image)
    test_model.parse_for_joint_positions()
    test_model.compute_accuracy(test_csv)
    assert not test_model.check_win()


def test_check_win_two_iterations():
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
