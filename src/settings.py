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

# NEAT-Inverted pendulum Training.
import pygame
NEATIP_EVENT_END_TRAINING_STEP = pygame.USEREVENT
NEATIP_TRAINING_STEPS = 30 # 15
NEATIP_MAX_TIME_ALIVE = 20 # seconds
NEATIP_INITIAL_ANGLE = -20 # sexagesimals with the vertical
NEATIP_LIMIT_ANGLE = 30 # [-x,x]
