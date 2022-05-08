"""
This script uses OpenPose to create joint position csvs based on the images in
the images/poses directory.
"""
import csv
import cv2
from deep_pose.body import Body

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

for file_name in MASK_NAMES:
    image = cv2.imread(f"images/poses/{file_name}.png")
    # pdb.set_trace()
    candidate, subset = BODY_ESTIMATION(image)

    joint_positions = {}
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

    with open(f"mask_joint_positions/{file_name}.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        for key, value in joint_positions.items():
            csv_writer.writerow([key, value[0], value[1]])
