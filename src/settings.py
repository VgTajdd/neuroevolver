## ========================================================================= ##
## Copyright (c) 2019 Agustin Durand Diaz.                                   ##
## This code is licensed under the MIT license.                              ##
## settings.py                                                               ##
## ========================================================================= ##

# General vars.
OBJ_SURFACE = None
TRAIN_CALLBACK = None
TRAIN_MODE = ''

# Debug vars.
SHOW_DEBUG_SHAPES = True
SHOW_ACTOR_RECT = False

# Application size.
APP_WIDTH = 800
APP_HEIGHT = 600
APP_FPS = 60

# FPGA simulation.
FPGA_TOTAL_FOOD = 40
FPGA_TOTAL_POISON = 10
FPGA_TOTAL_VEHICLES = 15
FPGA_POISON_HP_BONUS = -50
FPGA_FOOD_HP_BONUS = 10
FPGA_VEHICLE_INIT_HEALTH = 100
FPGA_SPEED_VEHICLE_BURN_HP = 0.01 #hp/ms -> 10 hp/s

import pygame

# NEAT Inverted pendulum.
NEAT_IP_EVENT_END_EVOLVING = pygame.USEREVENT
NEAT_IP_EVOLVING_STEPS = 30 # 15
NEAT_IP_MAX_TIME_ALIVE = 20 # seconds
NEAT_IP_INITIAL_ANGLE = -20 # sexagesimals with the vertical
NEAT_IP_LIMIT_ANGLE = 30 # [-x,x]
NEAT_IP_KEY = "neat_ip"

# NEAT Dycicle.
NEAT_DYCICLE_EVOLVING_STEPS = 100 # 15
NEAT_DYCICLE_EVENT_END_EVOLVING = pygame.USEREVENT + 1
NEAT_DYCICLE_MAX_TIME_ALIVE = 20
NEAT_DYCICLE_KEY = "neat_dycicle"

# B2D.
B2D_PPM = 20 # pixels per meter
B2D_CAT_BITS_GROUND = 0x0001
B2D_CAT_BITS_CAR = 0x0002
B2D_CAT_BITS_BAR = 0x0004

# NEAT Double inverted pendulum.
NEAT_DIP_EVOLVING_STEPS = 100 # 15
NEAT_DIP_EVENT_END_EVOLVING = pygame.USEREVENT + 2
NEAT_DIP_MAX_TIME_ALIVE = 60
NEAT_DIP_LIMIT_ANGLE = 45 # [-x,x]
NEAT_DIP_KEY = "neat_dip"

# Walker.
NEAT_WALKER_EVOLVING_STEPS = 50 # 15
NEAT_WALKER_MAX_TIME_ALIVE = 15
NEAT_WALKER_EVENT_END_EVOLVING = pygame.USEREVENT + 3
NEAT_WALKER_KEY = "neat_walker"

# NEAT TIP.
NEAT_TIP_EVOLVING_STEPS = 100 # 15
NEAT_TIP_EVENT_END_EVOLVING = pygame.USEREVENT + 4
NEAT_TIP_MAX_TIME_ALIVE = 25
NEAT_TIP_LIMIT_ANGLE = 45 # [-x,x]
NEAT_TIP_KEY = "neat_tip"

# Assets.
ASSETS_LOADED = False
IMAGES = {}
IMAGES_ALPHA = {}