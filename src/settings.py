# General var.
OBJ_SURFACE = None
TRAIN_CALLBACK = None
TRAIN_MODE = ''

# Debug
SHOW_DEBUG_SHAPES = True
SHOW_ACTOR_RECT = False

# Application size
APP_WIDTH = 800
APP_HEIGHT = 600
APP_FPS = 60

# FPGA simulation
FPGA_TOTAL_FOOD = 40
FPGA_TOTAL_POISON = 10
FPGA_TOTAL_VEHICLES = 15
FPGA_POISON_HP_BONUS = -50
FPGA_FOOD_HP_BONUS = 10
FPGA_VEHICLE_INIT_HEALTH = 100
FPGA_SPEED_VEHICLE_BURN_HP = 0.01 #hp/ms -> 10 hp/s

import pygame

# NEAT Inverted pendulum Training.
NEAT_IP_EVENT_END_TRAINING_STEP = pygame.USEREVENT
NEAT_IP_TRAINING_STEPS = 30 # 15
NEAT_IP_MAX_TIME_ALIVE = 20 # seconds
NEAT_IP_INITIAL_ANGLE = -20 # sexagesimals with the vertical
NEAT_IP_LIMIT_ANGLE = 30 # [-x,x]

# NEAT Dycicle Training.
NEAT_DYCICLE_TRAINING_STEPS = 100 # 15
NEAT_DYCICLE_EVENT_END_TRAINING_STEP = pygame.USEREVENT + 1
NEAT_DYCICLE_MAX_TIME_ALIVE = 20

# B2D
B2D_PPM = 20 # pixels per meter
B2D_CAT_BITS_GROUND = 0x0001
B2D_CAT_BITS_CAR = 0x0002
B2D_CAT_BITS_BAR = 0x0004

# NEAT Double inverted pendulum Training.
NEAT_DIP_TRAINING_STEPS = 100 # 15
NEAT_DIP_EVENT_END_TRAINING_STEP = pygame.USEREVENT + 2
NEAT_DIP_MAX_TIME_ALIVE = 60
NEAT_DIP_LIMIT_ANGLE = 45 # [-x,x]

# Walker
NEAT_WALKER_TRAINING_STEPS = 50 # 15
NEAT_WALKER_MAX_TIME_ALIVE = 15
NEAT_WALKER_EVENT_END_TRAINING_STEP = pygame.USEREVENT + 3

# NEAT TIP
NEAT_TIP_TRAINING_STEPS = 100 # 15
NEAT_TIP_EVENT_END_TRAINING_STEP = pygame.USEREVENT + 4
NEAT_TIP_MAX_TIME_ALIVE = 25
NEAT_TIP_LIMIT_ANGLE = 45 # [-x,x]
