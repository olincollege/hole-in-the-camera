"""
"""

from deep_pose.body import Body
import pdb
from hole_in_the_wall_model import HoleInTheWallGame
import numpy as np
import os


def test_initialization_deep_pose_model():
    test_model = HoleInTheWallGame()
    assert type(test_model.BODY_ESTIMATION) == Body

def test_initialization_mask_and_joints_length():
    test_model = HoleInTheWallGame()
    assert len(test_model.mask_and_joints) == 5

def test_initialization_joints_file_paths():
    test_model = HoleInTheWallGame()
    for _, csv in test_model.mask_and_joints:
        if not csv[-4:] == '.csv':
            assert False
    assert True

def test_initialization_mask_shape():
    test_model = HoleInTheWallGame()
    for image, _ in test_model.mask_and_joints:
        if np.shape(image) != (480, 640, 3):
            assert False
    assert True

def test_initialization_mask_values():
    test_model = HoleInTheWallGame()
    for image, _ in test_model.mask_and_joints:
        if np.mean(image) >= 255 or np.mean(image) <= 0:
            assert False
    assert True

def test_num_holes_remaining_start():
    test_model = HoleInTheWallGame()
    assert test_model.num_holes_remaining() == 5

def test_num_holes_remaining_three_trials_elapsed():
    test_model = HoleInTheWallGame()
    for _ in range(3):
        test_model.get_mask_and_joints()
    assert test_model.num_holes_remaining() == 2

def test_num_holes_remaining_all_trials_elapsed():
    test_model = HoleInTheWallGame()
    for _ in range(5):
        test_model.get_mask_and_joints()
    assert test_model.num_holes_remaining() == 0

def test_get_mask_and_joints_joint_path():
    test_model = HoleInTheWallGame()
    _, joint = test_model.get_mask_and_joints()
    assert joint[-4:] == '.csv'

def test_get_mask_and_joints_joint_exists():
    test_model = HoleInTheWallGame()
    _, joint = test_model.get_mask_and_joints()
    assert os.path.exists(joint)

def test_get_mask_and_joints_mask_shape():
    test_model = HoleInTheWallGame()
    mask, joints = test_model.get_mask_and_joints()
    assert np.shape(mask) == (480, 640, 3)

def test_get_mask_and_joints_mask_values():
    test_model = HoleInTheWallGame()
    mask, _ = test_model.get_mask_and_joints()
    assert np.mean(mask) < 255 and np.mean(mask) > 0