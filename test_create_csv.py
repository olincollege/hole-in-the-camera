"""
Test functions for the create_csv.py script.
"""

import os
import csv
from create_csv import analyze_image, write_to_csv

def test_analyze_image_none():
    nonexistant_image = "not_an_image.png"
    assert analyze_image(nonexistant_image) == {}

def test_analyze_image_keys_size():
    test_image_name = "first_mask"
    assert len(analyze_image(test_image_name).keys()) == 18

def test_analyze_image_values():
    test_image_name = "first_mask"
    test_joint_positions = analyze_image(test_image_name)
    for _, value in test_joint_positions.items():
        if len(value) != 2:
            assert False
        if value[0] < -1 or value[0] > 640 or value[1] < -1 or value[1] > 480:
            assert False
    assert True

def test_write_to_csv_exists():
    test_joint_positions = {}
    test_csv_name = "test"
    write_to_csv(test_csv_name, test_joint_positions)
    csv_exists = os.path.exists(f'mask_joint_positions/{test_csv_name}.csv')
    if csv_exists:
        os.remove(f'mask_joint_positions/{test_csv_name}.csv')
    assert csv_exists

def test_write_to_csv_no_joints():
    test_joint_positions = {}
    test_csv_name = "test"
    write_to_csv(test_csv_name, test_joint_positions)
    with open(f'mask_joint_positions/{test_csv_name}.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count = sum(1 for row in csv_reader)
    os.remove(f'mask_joint_positions/{test_csv_name}.csv')
    assert row_count == 0

def test_write_to_csv_one_joint():
    test_joint_positions = {'0': [0, 0]}
    test_csv_name = "test"
    write_to_csv(test_csv_name, test_joint_positions)
    with open(f'mask_joint_positions/{test_csv_name}.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count = sum(1 for row in csv_reader)
    os.remove(f'mask_joint_positions/{test_csv_name}.csv')
    assert row_count == 1

def test_write_to_csv_one_joint_values():
    test_joint_positions = {'0': [0, 0]}
    test_csv_name = "test"
    write_to_csv(test_csv_name, test_joint_positions)
    with open(f'mask_joint_positions/{test_csv_name}.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        joint_counter = 0
        for row in csv_reader:
            if row[0] != str(joint_counter) or row[1] !=\
                str(test_joint_positions[str(joint_counter)][0]) or\
                row[2] != str(test_joint_positions[str(joint_counter)][1]):
                assert False
            joint_counter += 1
    os.remove(f'mask_joint_positions/{test_csv_name}.csv')
    assert True

def test_write_to_csv_eighteen_joints():
    test_joint_positions = analyze_image('first_mask')
    test_csv_name = "test"
    write_to_csv(test_csv_name, test_joint_positions)
    with open(f'mask_joint_positions/{test_csv_name}.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count = sum(1 for row in csv_reader)
    os.remove(f'mask_joint_positions/{test_csv_name}.csv')
    assert row_count == 18

def test_write_to_csv_eighteen_joint_values():
    test_joint_positions = analyze_image('first_mask')
    test_csv_name = "test"
    write_to_csv(test_csv_name, test_joint_positions)
    with open(f'mask_joint_positions/{test_csv_name}.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        joint_counter = 0
        for row in csv_reader:
            if row[0] != str(joint_counter) or row[1] !=\
                str(test_joint_positions[str(joint_counter)][0]) or\
                row[2] != str(test_joint_positions[str(joint_counter)][1]):
                assert False
            joint_counter += 1
    os.remove(f'mask_joint_positions/{test_csv_name}.csv')
    assert True
