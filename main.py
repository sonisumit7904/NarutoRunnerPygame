import pygame
import sys
import random

pygame.init()
# main display surface
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("First Pygame from Sumit! ^_^")

bg_music = pygame.mixer.Sound('./audio/music.wav')
bg_music.play(loops = -1)


# Sprite Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1_surf = pygame.image.load('./graphics/NR3.png').convert_alpha()
        player_walk1_surf = pygame.transform.rotozoom(player_walk1_surf,0,0.75)
        player_walk2_surf = pygame.image.load('./graphics/NR2.png').convert_alpha()
        player_walk2_surf = pygame.transform.rotozoom(player_walk2_surf,0,0.75)
        
        self.player_walk_list = [player_walk1_surf,player_walk2_surf]
        self.player_jump_surf = pygame.image.load('./graphics/NR4.png').convert_alpha()
        self.player_jump_surf = pygame.transform.rotozoom(self.player_jump_surf,0,0.75)

        self.player_index = 0
        # self.player_surface = player_walk_list[0]
        # self.player_rectangle = player_surface.get_rect(midbottom = (80,300))

        self.image = self.player_walk_list[0]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

        # Jump Sound
        self.jump_sound = pygame.mixer.Sound('./audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump_surf
        else:
            self.player_index+=0.1
            if self.player_index>=len(self.player_walk_list):self.player_index = 0
            self.image = self.player_walk_list[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20
        # MouseDown to Jump on player
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.rect.bottom==300:
                    self.jump_sound.play()                    
                    self.gravity=-20

    def apply_gravity(self):
        self.gravity+=1
        self.rect.y +=self.gravity
        if(self.rect.bottom > 300) : self.rect.bottom = 300
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

player = pygame.sprite.GroupSingle()
player.add(Player())



class Obstackle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly1_surface = pygame.image.load('./graphics/shur.png').convert_alpha()
            fly2_surface = pygame.image.load('./graphics/s2.png').convert_alpha()
            self.surf_list = [fly1_surface,fly2_surface]
            self.y_pos = 200
        else:
            snail1_surface = pygame.image.load('./graphics/SL3.png').convert_alpha()
            snail1_surface = pygame.transform.rotozoom(snail1_surface,0,0.75)

            snail2_surface = pygame.image.load('./graphics/SL2.png').convert_alpha()
            snail2_surface = pygame.transform.rotozoom(snail2_surface,0,0.75)

            self.surf_list = [snail1_surface,snail2_surface]
            self.y_pos = 300
        
        self.animation_index = 0
        self.image = self.surf_list[int(self.animation_index)]
        self.rect = self.image.get_rect(midbottom=(random.randint(900,1200),self.y_pos))

    def animation_state(self):
        self.animation_index+=0.1
        if(self.animation_index>=len(self.surf_list)) : self.animation_index=0
        self.image = self.surf_list[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x-=10
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

obstackle_group = pygame.sprite.Group()

# display score time
def display_score():
    # pygame.time.get_ticks() = time from when pygame started first time, in Miliseconds
    current_time = (pygame.time.get_ticks() - start_time)//1000
    score_surface = score_font.render(f'Score: {current_time}',False,(64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(800/2,50))

    # screen.blit(score_surface,(250,50))
    # pygame.draw.rect(screen,'#c0e8ec',score_rectangle)
    # pygame.draw.rect(screen,'#c0e8ec',score_rectangle,width=10)

    screen.blit(score_surface,score_rectangle)

    return current_time

obstackle_rec_list = []
def obstackle_movement(obstackle_rec_list):
    if obstackle_rec_list:
        for obstackle_rec in obstackle_rec_list:
            obstackle_rec.x-=5
            if(obstackle_rec.bottom == 300):
                screen.blit(snail_surface,obstackle_rec)
            else:
                screen.blit(fly_surface,obstackle_rec)
            # print(obstackle_rec_list)
        # copying only x>-100 items to list
        obstackle_rec_list = [obstackle_rec for obstackle_rec in obstackle_rec_list if obstackle_rec.x > -100]
        # print(obstackle_rec_list)
        return obstackle_rec_list 
    else:
        return []

# Check collision
def player_collision(player_rectangle,obstackle_rec_list):
    if obstackle_rec_list:
        for obstackle_rec in obstackle_rec_list:
            if player_rectangle.colliderect(obstackle_rec): return False
    return True

# Check collision with sprite
def collision_sprite():
    # pygame.sprite.spritecollide(sprite,group,bool) -> single sprite to check collision with group of sprites, and delete that sprite from the group, if collision or not is given by bool
    if pygame.sprite.spritecollide(player.sprite,obstackle_group,False):
        # Obstackle Reset
        obstackle_group.empty()
        player.sprite.rect.bottom = 300
        return False
    else:
        return True

# Player animation
def player_animation():
    global player_surface, player_index
    if player_rectangle.bottom < 300:
        player_surface = player_jump_surf
    else:
        player_index+=0.1
        if player_index>=len(player_walk_list):player_index = 0
        player_surface = player_walk_list[int(player_index)]
# controls fps, or how much the game will update max times, in a second
clock = pygame.time.Clock()
# text font
score_font = pygame.font.Font('./font/Pixeltype.ttf',50)


# individual surface to be put inside main surface
sky_surface = pygame.image.load('./graphics/bg.png').convert()
sky_surface = pygame.transform.rotozoom(sky_surface,0,1.5)
ground_surface = pygame.image.load('./graphics/ground.png').convert()

# convert -> convert into format which is easy for pygame to render, convert_alpha -> respect alpha values, where tranparency should be there, but convert takes that like white
# Snail
# # snail_rectangle = snail_surface.get_rect(midbottom =(800,300))
# snail1_surface = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
# snail2_surface = pygame.image.load('./graphics/snail/snail2.png').convert_alpha()
# snail_surf_list = [snail1_surface,snail2_surface]
# snail_surf_index = 0
# snail_surface = snail_surf_list[0]

# # Fly
# fly1_surface = pygame.image.load('./graphics/Fly/Fly1.png')
# fly2_surface = pygame.image.load('./graphics/Fly/Fly2.png')
# fly_surf_list = [fly1_surface,fly2_surface]
# fly_surf_index = 0
# fly_surface = fly_surf_list[0]

# # player_surface -> contains image info, player_rectangle-> contains position info
# player_walk1_surf = pygame.image.load('./graphics/Player/player_walk_1.png')
# player_walk2_surf = pygame.image.load('./graphics/Player/player_walk_2.png')
# player_walk_list = [player_walk1_surf,player_walk2_surf]
# player_jump_surf = pygame.image.load('./graphics/Player/jump.png')
# player_index = 0
# player_surface = player_walk_list[0]
# player_rectangle = player_surface.get_rect(midbottom = (80,300))

# INTRO SCREEN PLAYER
player_stand = pygame.image.load('./graphics/NL1.png').convert_alpha()
# transform.rotozoom(surface, angle to rotate, scaling factor)
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rec = player_stand.get_rect(center = (400,200))

#INTRO INSTRUCTION
intro1_surface = score_font.render("Pixel Runner!",False, (64, 64, 64))
intro1_rect = intro1_surface.get_rect(center=(400,50))

intro2_surface = score_font.render("Press Space to Start!",False, (64, 64, 64))
intro2_rect = intro2_surface.get_rect(center=(400,350))


# Gravity
player_gravity=0

# start time, for activating the game 
start_time = 0

# Game Active
game_active = False

# score
score = 0

# Timer Event, make it a pygame userevent, always add +1 , +2 ,etc so as not to interfere with already existing event of pygame
# set timer which executes event obstackle_timer every 1400 miliseconds
obstackle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstackle_timer,1400)
# Snail and Fly timer
snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,200)
fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,100)

while True:
    # handle pygame closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # check only if GAME ACTIVE
        if game_active:
            # if event.type == pygame.MOUSEMOTION:
            #     print(event.pos)
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     print("mouseDown")
            # if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.collidepoint(event.pos):
            #     if player_rectangle.bottom==300:
            #         player_gravity=-20
            #         print("Collide")
            # if event.type == pygame.KEYDOWN:
            #     if(event.key == pygame.K_SPACE) and player_rectangle.bottom==300:
            #         player_gravity=-20
            #         print('jump event')
            # if event.type == pygame.KEYUP:
            #     if(event.key == pygame.K_SPACE):
            #         print('Keyup event')
            if event.type == obstackle_timer:
                obstackle_group.add(Obstackle(random.choice(['fly','snail','snail'])))
                # print("obstackle_timer")
                # if random.randint(0,2):
                #     obstackle_rec_list.append(snail_surface.get_rect(midbottom=(random.randint(900,1100),300)))
                # else:
                #     obstackle_rec_list.append(fly_surface.get_rect(midbottom = (random.randint(900,1100),200)))
            # Snail surface change with snail timer
            # if event.type == snail_timer:
            #     snail_surf_index = not(snail_surf_index)
            #     snail_surface = snail_surf_list[snail_surf_index]
            # # Fly surface change with fly timer
            # if event.type == fly_timer:
            #     # changing 0 to 1 or 1 to 0
            #     fly_surf_index = not(fly_surf_index)
            #     fly_surface = fly_surf_list[fly_surf_index]
            
        else:
            # RESTART
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                game_active=True
                start_time = pygame.time.get_ticks()


    if game_active:
        #draw out elements
        # snail_rectangle.left-=10
        # if snail_rectangle.left <-100 : snail_rectangle.left=800
            
        # player_rectangle.left+=5
        # if player_rectangle.left >900 : player_rectangle.left=-100
            

        # blit = block transfer, put test_surface on top of screen surface at distance x =200 and y= 100 from top left corner
        screen.blit(sky_surface,(-100,0))
        screen.blit(ground_surface,(0,285))
        # Score
        score = display_score()
        
        # Obstackle Movement
        # screen.blit(snail_surface,(snail_x_pos,250))
        # screen.blit(snail_surface,snail_rectangle)
        # obstackle_rec_list = obstackle_movement(obstackle_rec_list)

        
        # snail is on top of score , on top of ground, on top of sky_surface
        # pygame.draw.ellipse(screen,'Brown',pygame.Rect(player_rectangle.left,player_rectangle.top,player_rectangle.width+30,player_rectangle.height+20))


        # gravity for player
        # player_animation()
        # player_gravity+=1
        # player_rectangle.y +=player_gravity
        # if(player_rectangle.bottom > 300) : player_rectangle.bottom=300
        # if(player_rectangle.top < ) : player_rectangle.bottom=300    
        # screen.blit(player_surface,player_rectangle)

        # PlayerClass draw on screen
        player.draw(screen)
        player.update()

        obstackle_group.draw(screen)
        obstackle_group.update()
        # pygame.draw.line(screen,'Red',(0,0),pygame.mouse.get_pos(),width=10)

        # if(player_rectangle.colliderect(snail_rectangle)):
        # mouse_pos = pygame.mouse.get_pos()
        # get mouse position
        # check if mouse is on player_rectangle, return true else false
        # if(player_rectangle.collidepoint(mouse_pos)):   
            # print("collision")
            # print(pygame.mouse.get_pressed())
        # else:
        #     print("NO Collision")


        # Keys
        # keys = pygame.key.get_pressed()
        # if(keys[pygame.K_SPACE]):
        #     print('jump')


        # COLLISION WITH SNAIL AND GAME OVER
        # if snail_rectangle.colliderect(player_rectangle):
        #     game_active=False
        # game_active = player_collision(player_rectangle,obstackle_rec_list)
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(intro1_surface,intro1_rect)
        screen.blit(player_stand,player_stand_rec)

        # Reset Obstackle
        # snail_rectangle.left = 800
        # obstackle_rec_list.clear()
        # player_rectangle.midbottom=(80,300)
        # player_gravity=0

        final_score_surf = score_font.render(f'Your Score : {score}',False,(64, 64, 64))
        final_score_surf_rec = final_score_surf.get_rect(center=(400,350))

        if(score == 0): screen.blit(intro2_surface,intro2_rect)
        else : screen.blit(final_score_surf,final_score_surf_rec)



    # update everything on display
    pygame.display.update()
    # update max 60 times in 1 second, 60fps
    clock.tick(60)