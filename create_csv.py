"""
Create csv files representing joints positions for each mask.
"""
import csv
import cv2
from deep_pose.body import Body
import os

BODY_ESTIMATION = Body("deep_pose/body_pose_model.pth")

MASK_NAMES = [
    "first_mask",
    "second_mask",
    "third_mask",
    "fourth_mask",
    "fifth_mask",
    "sixth_mask",
    "seventh_mask",
]

def analyze_image(image_name):
    """
    This function analyzes a given image and returns the joint positions
    found within it as a dictionary.

    Args:
        image_name (str): The name of the image to analyze.
    Returns:
        joint_positions (dict): A dictionary where each key is a string number
            corresponding to a joint and each value is the pixel location of
            the joint in the image, [-1, -1] if it is not found.
    """
    joint_positions = {}
    if os.path.exists(f"images/poses/{image_name}.png"):
        image = cv2.imread(f"images/poses/{image_name}.png")
        candidate, subset = BODY_ESTIMATION(image)

        for index, value in enumerate(subset[0]):
            if value >= 0:
                joint_positions[f"{index}"] = [
                    candidate[int(value)][0],
                    candidate[int(value)][1],
                ]
            else:
                joint_positions[f"{index}"] = [-1, -1]
            if index >= 17:
                break
    return joint_positions

def write_to_csv(csv_name, joint_positions):
    """
    This function writes the found joint positions to a csv file with the same
    name.

    Args:
        csv_name (str): The name of the new csv file.
        joint_positions (dict): A dictionary where each key is a string number
            corresponding to a joint and each value is the pixel location of
            the joint in the image, [-1, -1] if it is not found.
    """
    with open(f"mask_joint_positions/{csv_name}.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            for key, value in joint_positions.items():
                csv_writer.writerow([key, value[0], value[1]])

def main():
    """
    This is the main runner function to create csv files.
    """
    for file_name in MASK_NAMES:
        joint_positions = analyze_image(file_name)
        write_to_csv(file_name, joint_positions)

if __name__ == "__main__":
    main()
