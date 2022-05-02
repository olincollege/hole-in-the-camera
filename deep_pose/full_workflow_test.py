import numpy as np
import util
from body import Body
import pdb
import cv2 as cv
import csv
import pygame
import copy

new_contour = False

body_estimation = Body('deep_pose/body_pose_model.pth')

mask_image = cv.imread("body_pose.png")
mask_image = cv.resize(mask_image, (640, 480))
candidate, subset = body_estimation(mask_image)
canvas = copy.deepcopy(mask_image)
canvas = util.draw_bodypose(canvas, candidate, subset)
joint_positions = {}
for index, value in enumerate(subset[0]):
    if value >= 0:
        joint_positions[f'{index}'] = [candidate[int(value)][0], candidate[int(value)][1]]
    else:
        joint_positions[f'{index}'] = [-1, -1]
    if index >= 17:
        break
with open('pose_test_one.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    for key, value in joint_positions.items():
        csv_writer.writerow([key, value[0], value[1]])

# pdb.set_trace()

# create vidow stream
cap = cv.VideoCapture(-1)

# create third game loop to display video and time countdown
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
# set up colors
BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE = (50, 50, 200)
BLUE_BACKGROUND = (153,204,255)
SIZE = (640, 480)

# initialize pygame
pygame.init()

# create game window, title, and icon
screen = pygame.display.set_mode((640,480), pygame.RESIZABLE)
pygame.display.set_caption("Hole in the Camera")
icon = pygame.image.load(r'gameicon.png')
pygame.display.set_icon(icon)
font = pygame.font.SysFont("Helvetica", 40)
isTrue, oriImg = cap.read()
mask = cv.imread("new_mask.png")
mask = cv.resize(mask, SIZE)
while running:
    isTrue, oriImg = cap.read()
    oriImg = cv.cvtColor(oriImg, cv.COLOR_BGR2RGB)
    display = cv.bitwise_and(mask, oriImg)
    screen = pygame.display.set_mode((display.shape[1], display.shape[0]))
    new_surf = pygame.transform.rotate(
        pygame.surfarray.make_surface(display), -90)
    screen.blit(new_surf, (0, 0))
    events = pygame.event.get()

    counting_time = pygame.time.get_ticks() - start_time
    counting_string = f'{10-counting_time//500}'
    counting_text = font.render(str(counting_string), 1, (255,255,255))
    counting_rect = counting_text.get_rect(bottomright = screen.get_rect().bottomright)
    screen.blit(counting_text, counting_rect)

    pygame.display.update()

    if 5000 - counting_time < 0:
        final_frame = oriImg
        # send frame to be processed
        # then determine next trial
        running = False

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
cap.release()
candidate, subset = body_estimation(oriImg)
canvas = copy.deepcopy(oriImg)
canvas = util.draw_bodypose(canvas, candidate, subset)

# plt.imshow(canvas[:, :, [2, 1, 0]])
# plt.axis('off')
# plt.show()

joint_positions = {}
for index, value in enumerate(subset[0]):
    if value >= 0:
        joint_positions[f'{index}'] = [candidate[int(value)][0], candidate[int(value)][1]]
    else:
        joint_positions[f'{index}'] = [-1, -1]
    if index >= 17:
        break


if new_contour:
    with open('pose_test_one.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for key, value in joint_positions.items():
            csv_writer.writerow([key, value[0], value[1]])
else:
    accuracy = 0
    joint_fits = []
    joint_counts = 0
    with open('pose_test_one.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            joint_fits.append(row)
    for joint in joint_fits:
        if joint[0] in joint_positions.keys() and joint_positions[joint[0]][1] != -1 and joint[1] != '-1':
            joint_counts += 1
            a = np.array([int(float(joint[1])), int(float(joint[2]))])
            b = np.array(joint_positions[joint[0]])
            dist = np.linalg.norm(a-b)
            print(dist)
            if dist < 20:
                accuracy += 1
            elif dist < 30:
                accuracy += .5
            elif dist < 40:
                accuracy += .25
    print(accuracy/joint_counts)
