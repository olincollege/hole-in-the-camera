import pygame
import cv2

BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE = (50, 50, 200)

pygame.init()
screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)
font = pygame.font.SysFont(None, 54)

def display_text(texts):
    y_offset = 0
    screen.fill(WHITE)
    for text in texts:
        font_width, font_height = font.size(text)
        image = font.render(text, True, BLUE)
        screen.blit(image, (200, 200+y_offset))
        y_offset += font_height
    pygame.display.update()

welcome_text = ["Welcome to Hole in the Camera!", "Press any key to continue."]
display_text(welcome_text)

running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            display_text(["Instructions"])
            running = False
        if event.type == pygame.QUIT:
            pygame.quit()

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            running = False
        if event.type == pygame.QUIT:
            pygame.quit()

cap = cv2.VideoCapture(0)

running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
while running:
    _, frame = cap.read()
    screen = pygame.display.set_mode((frame.shape[1], frame.shape[0]))
    new_surf = pygame.transform.rotate(
        pygame.surfarray.make_surface(frame), -90)
    screen.blit(new_surf, (0, 0))
    events = pygame.event.get()

    counting_time = pygame.time.get_ticks() - start_time
    counting_string = f'{30-counting_time//100}'
    counting_text = font.render(str(counting_string), 1, (255,255,255))
    counting_rect = counting_text.get_rect(bottomright = screen.get_rect().bottomright)
    screen.blit(counting_text, counting_rect)

    pygame.display.update()

    if 3000 -counting_time < 0:
        final_frame = frame
        # send frame to be processed
        # then determine next trial
        display_text(["Timer Done"])
        running = False

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
pygame.time.delay(10000)