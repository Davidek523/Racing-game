import pygame
import time
import math
from utils import *
pygame.font.init()

# to do list:
# obstacles and speed pads
# pitstop
# tire change

GRASS = scale_image(pygame.image.load('Game Folder/data/backgrounds/desert_details.png'), 50)
TRACK = scale_image(pygame.image.load('Game Folder/data/backgrounds/green_pixel_track.png'), 0.7)

TRACK_BORDER = scale_image(pygame.image.load('Game Folder/data/backgrounds/green_pixel_border_fixed.png'), 0.7)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

PIT_STOP = scale_image(pygame.image.load('Game Folder/data/backgrounds/gas_station.png'), 0.7)
PIT_STOP_POS = (0, 0)
PIT_STOP_MASK = pygame.mask.from_surface(PIT_STOP)

ROAD_CONE_1 = scale_image(pygame.image.load('Game Folder/data/props/road_cone.png'), 2)
ROAD_CONE_1_POS = (30, 80)
ROAD_CONE_MASK = pygame.mask.from_surface(ROAD_CONE_1)

ROAD_CONE_2_POS = (226, 80)
ROAD_CONE_3_POS = (520, 85)
ROAD_CONE_4_POS = (655, 150)
ROAD_CONE_5_POS = (500, 195)
ROAD_CONE_6_POS = (440, 325)
ROAD_CONE_7_POS = (310, 315)
ROAD_CONE_8_POS = (165, 320)
ROAD_CONE_9_POS = (160, 457)
ROAD_CONE_10_POS = (643, 620)
ROAD_CONE_11_POS = (485, 665)
ROAD_CONE_12_POS = (199, 620)
ROAD_CONE_13_POS = (25, 415)


FINISH = scale_image(pygame.image.load('Game Folder/data/props/finish_line.png'), 3)
FINISH_LINE_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (29, 280)

PLAYER_CAR = scale_image(pygame.image.load('Game Folder/data/players/blue_car.png'), 1.7)

ENEMY_CAR = scale_image(pygame.image.load('Game Folder/data/npc/enemy_car.png'), 1.7)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Great Race")

MAIN_FONT = pygame.font.SysFont("grand9kpixelregular", 35)

FPS = 60
PATH = [(57, 163), (125, 85), (418, 67), (685, 65), (765, 126), (677, 177), (525, 173), (433, 247), (448, 398), (372, 458), (304, 390), (307, 237), (243, 184), (160, 239), (153, 487), (233, 564), (507, 551), (553, 478), (553, 380), (649, 338), (751, 385), (673, 471), (677, 541), (745, 607), (677, 659), (383, 671), (163, 659), (69, 618), (60, 529), (64, 304)]

class GameInfo:
    LEVELS = 5

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def tire_handling(self):
        self.level += 1
        self.started = False
        car_player.reset()

    def next_level(self):
        self.level += 1
        self.started = False
        car_player.reset()

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS
    
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.img = self.IMG
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backwards(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    IMG = PLAYER_CAR
    START_POS = (25, 250)

    def __init__(self, max_vel, rotation_vel):
        super().__init__(max_vel, rotation_vel)
        self.current_point = 0
        self.initail_max_vel = max_vel
        self.vel = max_vel
        self.max_vel = max_vel

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def tire_handling(self, level):
        self.reset()
        self.max_vel = 3 - (level - 1) * 0.1
        if self.max_vel < 1:
            self.max_vel = 1
        self.vel = self.max_vel
        self.current_point = 0

    def hard_tire(self):
        self.vel = self.initail_max_vel
        self.max_vel = self.initail_max_vel
        self.current_point = 0

    def medium_tire(self):
        self.vel = self.initail_max_vel
        self.max_vel = 3 * 0.97
        self.current_point = 0

    def soft_tire(self):
        self.vel = self.initail_max_vel
        self.max_vel = 3 * 0.87
        self.current_point = 0


class ComputerCar(AbstractCar):
    IMG = ENEMY_CAR
    START_POS = (55, 250)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # DRAWS POINTS FOR AI PATH
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return
        
        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0


def draw(win, images, car_player, enemy, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f'Lap: {game_info.level}', 1, (0, 0, 0))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(f'Time: {game_info.get_level_time()} s', 1, (0, 0, 0))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = MAIN_FONT.render(f'Speed: {round(car_player.vel, 1)} m/s', 1, (0, 0, 0))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    car_player.draw(win)
    enemy.draw(win)
    pygame.display.update()

def move_player(car_player):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        car_player.rotate(left=True)
    if keys[pygame.K_d]:
        car_player.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        car_player.move_forward()
    if keys[pygame.K_s]:
        moved = True
        car_player.move_backwards()

    if not moved:
        car_player.reduce_speed()

def handle_collision(car_player, enemy, game_info):
    if car_player.collide(TRACK_BORDER_MASK) != None:
        car_player.bounce()

    if car_player.collide(PIT_STOP_MASK, *PIT_STOP_POS) != None:
        blit_text_center(WIN, MAIN_FONT, f'Choose tire: 1. Soft 2. Medium 3. Hard')
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            car_player.soft_tire()
        if keys[pygame.K_2]:
            car_player.medium_tire()
        if keys[pygame.K_3]:
            car_player.hard_tire()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_1_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_2_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_3_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_4_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_5_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_6_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_7_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_8_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_9_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_10_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_11_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_12_POS) != None:
        car_player.bounce()

    if car_player.collide(ROAD_CONE_MASK, *ROAD_CONE_13_POS) != None:
        car_player.bounce()

    computer_finish_poi_collide = enemy.collide(FINISH_LINE_MASK, *FINISH_POS)
    if computer_finish_poi_collide != None:
            blit_text_center(WIN, MAIN_FONT, 'YOU LOSE!')
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.reset()
            car_player.reset()
            enemy.reset()

    player_finish_poi_collide = car_player.collide(FINISH_LINE_MASK, *FINISH_POS)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            car_player.bounce()
        else:
            game_info.next_level()
            enemy.reset()
            enemy.next_level(game_info.level)
            car_player.tire_handling(game_info.level)


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (PIT_STOP, PIT_STOP_POS), (ROAD_CONE_1, ROAD_CONE_1_POS), (ROAD_CONE_1, ROAD_CONE_2_POS), (ROAD_CONE_1, ROAD_CONE_3_POS), (ROAD_CONE_1, ROAD_CONE_4_POS), (ROAD_CONE_1, ROAD_CONE_5_POS), (ROAD_CONE_1, ROAD_CONE_6_POS), 
          (ROAD_CONE_1, ROAD_CONE_7_POS), (ROAD_CONE_1, ROAD_CONE_8_POS), (ROAD_CONE_1, ROAD_CONE_9_POS), (ROAD_CONE_1, ROAD_CONE_10_POS), (ROAD_CONE_1, ROAD_CONE_11_POS), (ROAD_CONE_1, ROAD_CONE_12_POS), (ROAD_CONE_1, ROAD_CONE_13_POS)]
car_player = PlayerCar(3, 3)
enemy = ComputerCar(2, 3, PATH)
game_info = GameInfo()


while run:
    clock.tick(FPS)

    draw(WIN, images, car_player, enemy, game_info)

    # while car_player.collide(PIT_STOP_MASK, *PIT_STOP_POS) != None:
    #     blit_text_center(WIN, MAIN_FONT, f'Choose tire: 1. Soft 2. Medium 3. Hard')
    #     pygame.display.update()
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_1]:
    #         car_player.soft_tire()
    #     if keys[pygame.K_2]:
    #         car_player.medium_tire()
    #     if keys[pygame.K_3]:
    #         car_player.hard_tire()

    while not game_info.started:
        blit_text_center(WIN, MAIN_FONT, f"Press any key to start lap {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT
                break

            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # MAKES THE PATH FOR THE AI CAR
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pos = pygame.mouse.get_pos()
        #     enemy.path.append(pos)

    move_player(car_player)
    enemy.move()

    handle_collision(car_player, enemy, game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, 'YOU WIN!')
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        car_player.reset()
        enemy.reset()

# print(enemy.path)
pygame.quit()