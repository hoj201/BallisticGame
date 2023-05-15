import pygame, sys
from pygame.locals import *
from math import *
import numpy as np


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


pygame.init()

FPS = 60  # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0, 32)
pygame.display.set_caption('Ballistic Game')

backgroundImg = pygame.image.load('images/background.png')
cannonBaseImg = pygame.image.load('images/cannonBase.png')
cannonImg = pygame.image.load('images/cannonTube.png')
ballImg = pygame.image.load('images/cannonBall.png')
targetImg = pygame.image.load('images/target.png')
yayImg = pygame.image.load('images/yay.jpeg')

# positions of the cannon parts
cannonBasePos = np.array((15, 478))
cannonPos = np.array((-5, 450))
ballPos = np.array((22, 478))
targetPos = np.array((500, 478))

# make the cannon horizontal
cannonImg = pygame.transform.rotate(cannonImg, -15)

# set the default cannon angle
ang = 0.0 # 0.59  # 45
cannonMovImg = rot_center(cannonImg, ang)

# blit the images
DISPLAYSURF.blit(backgroundImg, (0, 0))
DISPLAYSURF.blit(cannonMovImg, cannonPos)
DISPLAYSURF.blit(ballImg, ballPos)
DISPLAYSURF.blit(cannonBaseImg, cannonBasePos)
DISPLAYSURF.blit(targetImg, targetPos)

# set the physical quantities
t = 0  # time
s = ballPos  # space
v0 = np.zeros(2)  # velocity
v = v0
vm = 478.0251144  # initial speed
launched = False  # ball shoted
target_hit = False
tol = 20
# the main game loop
while True:
    dt = fpsClock.tick(FPS)  # dt = t_now - t_previous
    if launched:
        t = t + dt / 250.0  # updated time
        a = np.array((0.0, 9.8))  # acceleration
        v = v0 + a * t  # velocity
        vm = sqrt(np.dot(v, v))
        s0 = ballPos  # initial position
        s = s0 + v0 * t + a * t * t / 2
        if s[1] >= 486:  # if hit the ground
            launched = False

    if np.dot(s - targetPos, s - targetPos) < tol ** 2:
        launched = False
        target_hit = True

    #  set informations to print
    font = pygame.font.Font(None, 30)

    text_ang = font.render("angle = %d" % ang, 1, (10, 10, 10))
    text_ang_pos = (0, 540)

    text_vm = font.render("vm = %.1f m/s" % vm, 1, (10, 10, 10))
    text_vm_pos = (0, 560)

    text_vx = font.render("vx = %.1f m/s" % v[0], 1, (10, 10, 10))
    text_vx_pos = (0, 580)

    text_vy = font.render("vy = %.1f m/s" % v[1], 1, (10, 10, 10))
    text_vy_pos = (0, 600)

    text_x = font.render("x = %.1f m" % s[0], 1, (10, 10, 10))
    text_x_pos = (0, 620)

    text_y = font.render("y = %.1f m" % s[1], 1, (10, 10, 10))
    text_y_pos = (0, 640)

    text_t = font.render("t = %.1f s" % t, 1, (10, 10, 10))
    text_t_pos = (0, 660)

    # blit the new scene
    DISPLAYSURF.blit(backgroundImg, (0, 0))
    DISPLAYSURF.blit(cannonMovImg, cannonPos)
    DISPLAYSURF.blit(ballImg, s)
    DISPLAYSURF.blit(cannonBaseImg, cannonBasePos)
    DISPLAYSURF.blit(text_t, text_t_pos)
    DISPLAYSURF.blit(text_vx, text_vx_pos)
    DISPLAYSURF.blit(text_vy, text_vy_pos)
    DISPLAYSURF.blit(text_vm, text_vm_pos)
    DISPLAYSURF.blit(text_x, text_x_pos)
    DISPLAYSURF.blit(text_y, text_y_pos)
    DISPLAYSURF.blit(text_ang, text_ang_pos)
    DISPLAYSURF.blit(targetImg, targetPos)
    if target_hit:
        DISPLAYSURF.blit(yayImg, (DISPLAY_WIDTH//2, DISPLAY_HEIGHT//2))


    # take care of events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:  # space key to launch
                ballPos = (22, 478)
                s = ballPos
                t = 0
                launched = True
                # set the initial velocity
                v0 = np.array((vm * cos(radians(ang)), -vm * sin(radians(ang))))

    keystate = pygame.key.get_pressed()

    if keystate[K_LEFT]:  # rotate conterclockwise
        ang += 2
        if ang > 90:
            ang = 90
        cannonMovImg = rot_center(cannonImg, ang)

    if keystate[K_RIGHT]:  # rotate clockwise
        ang -= 2
        if ang < 0:
            ang = 0
        cannonMovImg = rot_center(cannonImg, ang)

    if keystate[K_UP]:  # increase initial speed
        vm += 2

    if keystate[K_DOWN]:  # decrease initial speed
        vm -= 2

    # display actual scene
    pygame.display.flip()
