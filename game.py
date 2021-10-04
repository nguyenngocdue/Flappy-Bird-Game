import pygame, sys, random
# Create defention for game
def draw_floor():
    screen.blit(floor, (floor_x_pos,650))
    screen.blit(floor, (floor_x_pos + 432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_dispkay(game_sate):
    if game_sate == 'main game':
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)
    if game_sate == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'SHigh core: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,620))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

        
#############################################################
#control sound suitable for game
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2,buffer=512) 
pygame.init()
#set background game
screen = pygame.display.set_mode((432,768))
#Set FPS
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 40)
#Load Image
bg = pygame.image.load('assets/background-night.png').convert()
# fill image on Screen
bg = pygame.transform.scale2x(bg)

# Add Floor
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#Create bird

#Create animate for bird
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_list = [bird_down,bird_mid, bird_up]# 0,1,2
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.transform.scale2x(bird)
#bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()

#crete timer for bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

#tạo rectangle cho con chim
bird_rect = bird.get_rect(center = (100,384))

#gravity of bird
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

#creare pipe
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]


#crete timer for pipe:
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200,300,400]

# Create finish screen
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png'))
game_over_rect = game_over_surface.get_rect(center = (216,384))

#Add sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#tạo vòng lập để lặp background image
while True:
    #tạo sự kiện pygame diễn ra
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #tạo phím thoát
            pygame.quit()
            sys.exit() # video system not initialized
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0 # get origin bird at y = 0
                bird_movement =-11 # move up bird -y
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                #reset pipe and bird
                pipe_list.clear()
                bird_rect.center =(100,384)
                bird_movement = 0
                score = 0
            #create event animation bird
            if event.type == birdflap:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird, bird_rect = bird_animation()


        #Create event timer: pipe
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

        # Add image on sreen
        screen.blit(bg,(0,0))

        #Out game
        if game_active:
            #brid
            bird_movement += gravity
            rotated_bird = rotate_bird(bird)
            #move bird go down Oy
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird,bird_rect)
            game_active = check_collision(pipe_list)

            #Pipes
            pipe_list = move_pipe(pipe_list)
            draw_pipe(pipe_list)
            score += 0.01
            score_dispkay('main game')
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown =100
        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_dispkay('game over')

        #Create Floor
        floor_x_pos -= 1
        draw_floor()
        if  floor_x_pos <= -432:
            floor_x_pos = 0

        pygame.display.update() # display on your screen
        #Set FPS
        clock.tick(60)

 
