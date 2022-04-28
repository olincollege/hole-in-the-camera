import pygame
import cv2
# set up colors
BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE = (50, 50, 200)
BLUE_BACKGROUND = (153,204,255)

# initialize pygame
pygame.init()

# create game window, title, and icon
screen = pygame.display.set_mode((640,480), pygame.RESIZABLE)
pygame.display.set_caption("Hole in the Camera")
icon = pygame.image.load(r'/home/jiayuan/hole-in-the-camera/gameicon.png')
pygame.display.set_icon(icon)


# create function to display text in game window
font = pygame.font.SysFont("Helvetica", 40)
def display_text(texts):
    y_offset = 0
    background = pygame.image.load(r'/home/jiayuan/hole-in-the-camera/background.png')
    screen.blit(background,(0,0))
    for text in texts:
        font_width, font_height = font.size(text)
        image = font.render(text, True, WHITE, BLACK)
        screen.blit(image, (20, 200+y_offset))
        y_offset += font_height
    pygame.display.update()

# display first welcoming text
welcome_text = ["Welcome to Hole in the Camera!", "Press any key to continue."]
display_text(welcome_text)

# create first game loop to display instructions
running = True
while running:
    events = pygame.event.get()
    for event in events:
        # get any key to display instructions
        if event.type == pygame.KEYDOWN:
            display_text(["Instructions"])
            running = False
        # close window if quit botton is pressed
        if event.type == pygame.QUIT:
            pygame.quit()

# create second game loop (this part I don't understand)
running = True
while running:
    events = pygame.event.get()
    for event in events:
       if event.type == pygame.KEYDOWN:
        running = False
       if event.type == pygame.QUIT:
        pygame.quit()

# create vidow stream
cap = cv2.VideoCapture(0)

# create third game loop to display video and time countdown
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