import pygame, sys


def draw_floor():
    screen.blit(floor, (floor_x_pos,600))
    screen.blit(floor, (floor_x_pos + 432,600))


pygame.init()
#set background game
screen = pygame.display.set_mode((432,768))

#Set FPS
clock = pygame.time.Clock()
#Load Image
bg = pygame.image.load('assets/background-night.png').convert()
# fill image on Screen
bg = pygame.transform.scale2x(bg)

# Add Floor
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#Create bird
bird = pygame.image.load('assets/yellowbird-midflap.png').convert()
bird = pygame.transform.scale2x(bird)
#tạo rectangle cho con chime
bird_rect = bird.get_rect(center = (100,384))

#tạo vòng lập để lặp background image
while True:
    #tạo sự kiện pygame diễn ra
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #tạo phím thoát
            pygame.quit()
            sys.exit() # video system not initialized
        # Add image on sreen
        screen.blit(bg,(0,0))

        #Create Floor
        floor_x_pos -= 1
        draw_floor()
        if  floor_x_pos <= -432:
            floor_x_pos = 0

        pygame.display.update() # display on your screen
        #Set FPS
        clock.tick(120)

#tạo ra con bird


