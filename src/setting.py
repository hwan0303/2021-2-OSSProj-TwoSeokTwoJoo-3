import os
import sys
import random
import pygame
from pygame import display
from pygame import mixer
from pygame import Rect
from pygame import Surface
from pygame import time
from pygame import transform
from pygame.locals import RESIZABLE, RLEACCEL

mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
display.set_caption("Milk Dragon's Adventure by_MilkDragon")
gamer_name = ''
scr_size = (width, height) = (800, 400)
FPS = 60
gravity = 0.65
font = pygame.font.Font('DungGeunMo.ttf', 32)
full_screen = False
monitor_size = (monitor_width, monitor_height) = (display.Info().current_w,
                                                  display.Info().current_h)
background_col = (235, 235, 235)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 200, 0)
orange = (255, 127, 0)
blue = (0, 0, 225)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_orange = (255, 215, 0)
high_score = 0
resized_screen = display.set_mode((scr_size), RESIZABLE)
screen = resized_screen.copy()
resized_screen_center = (0, 0)
r_width = resized_screen.get_width()
r_height = resized_screen.get_height()
button_offset = 0.18
clock = time.Clock()
on_pushtime = 0
off_pushtime = 0
dino_size = [44, 47]
object_size = [40, 40]
ptera_size = [46, 40]
collision_immune_time = 500
shield_time = 2000
speed_up_limit = 700
bgm_on = True
jump_sound = mixer.Sound('sprites/jump.wav')
die_sound = mixer.Sound('sprites/die.wav')
check_point_sound = mixer.Sound('sprites/checkPoint.wav')


# background_music = pygame.mixer.Sound('sprites/t-rex_bgm1.mp3')
# HERE: REMOVE SOUND!!
# pygame.mixer.music.load('sprites/t-rex_bgm1.mp3')


# 게임 내에 text를 넣을때 쓰는 함수
def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)


def text_objects(text, font):
    text_surface = font.render(text, True, (black))
    return text_surface, text_surface.get_rect()


# 게임 내 image를 넣을 때 쓰는 함수
def load_image(name, sizex=-1, sizey=-1, color_key=None):
    full_name = os.path.join('sprites', name)
    img = pygame.image.load(full_name)
    img = img.convert()
    if color_key is not None:
        if color_key == -1:
            color_key = img.get_at((0, 0))
        img.set_colorkey(color_key, RLEACCEL)
    if sizex != -1 or sizey != -1:
        img = transform.scale(img, (sizex, sizey))
    return (img, img.get_rect())


def load_sprite_sheet(sheet_name, nx, ny,
                      scalex=-1, scaley=-1, color_key=None):
    full_name = os.path.join('sprites', sheet_name)
    sheet = pygame.image.load(full_name)
    sheet = sheet.convert()
    sheet_rect = sheet.get_rect()
    sprites = []
    sizex = sheet_rect.width / nx
    sizey = sheet_rect.height / ny
    for i in range(0, ny):
        for j in range(0, nx):
            rect = Rect((j * sizex, i * sizey, sizex, sizey))
            img = Surface(rect.size)
            img = img.convert()
            img.blit(sheet, (0, 0), rect)
            if color_key is not None:
                if color_key == -1:
                    color_key = img.get_at((0, 0))
                img.set_colorkey(color_key, RLEACCEL)
            if scalex != -1 or scaley != -1:
                img = transform.scale(img, (scalex, scaley))
            sprites.append(img)
    sprite_rect = sprites[0].get_rect()
    return sprites, sprite_rect


def disp_gameover_msg(gameover_img):
    gameover_rect = gameover_img.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height * 0.35
    screen.blit(gameover_img, gameover_rect)

def disp_gameover_buttons(btn_restart, btn_save, btn_exit):
    btn_restart_rect = btn_restart.get_rect()
    btn_save_rect = btn_save.get_rect()
    btn_exit_rect = btn_exit.get_rect()
    btn_restart_rect.centerx = width * 0.25
    btn_save_rect.centerx = width * 0.5
    btn_exit_rect.centerx = width * 0.75
    btn_restart_rect.centery = height * 0.5
    btn_save_rect.centery = height * 0.5
    btn_exit_rect.centery = height * 0.5
    screen.blit(btn_restart, btn_restart_rect)
    screen.blit(btn_save, btn_save_rect)
    screen.blit(btn_exit, btn_exit_rect)

def disp_intro_buttons(btn_start, btn_board, btn_option):
    btn_start_rect = btn_start.get_rect()
    btn_board_rect = btn_board.get_rect()
    btn_option_rect = btn_option.get_rect()
    btn_start_rect.centerx = width * 0.72
    btn_board_rect.centerx = width * 0.72
    btn_option_rect.centerx = width * 0.72
    btn_start_rect.centery = height * 0.5
    btn_board_rect.centery = height * (0.5 + button_offset)
    btn_option_rect.centery = height * (0.5 + 2 * button_offset)
    screen.blit(btn_start, btn_start_rect)
    screen.blit(btn_board, btn_board_rect)
    screen.blit(btn_option, btn_option_rect)


def check_scr_size(eventw, eventh):
    if (eventw < width and eventh < height) or (eventw < width) or (eventh < height):
        # 최소해상도
        resized_screen = display.set_mode((scr_size), RESIZABLE)
    else:
        if (eventw / eventh) != (width / height):
            # 고정화면비
            adjusted_height = int(eventw / (width / height))
            resized_screen = display.set_mode((eventw, adjusted_height), RESIZABLE)


def full_screen_issue():
    global scr_size
    resized_screen = display.set_mode((scr_size), RESIZABLE)
    resized_screen = display.set_mode((scr_size), RESIZABLE)


def extract_digits(number):
    if number > -1:
        digits = []
        i = 0
        while ((number / 10) != 0):
            digits.append(number % 10)
            number = int(number / 10)
        digits.append(number % 10)
        for i in range(len(digits), 5):
            digits.append(0)
        digits.reverse()
        return digits


def resize(name, w, h, color):
    global width, height, resized_screen
    print("resized_screen: (", resized_screen.get_width(),
          ",", resized_screen.get_height(), ")")
    return (name, w * resized_screen.get_width() // width,
            h * resized_screen.get_height() // height, color)


def text_size(size):
    font = pygame.font.Font('DungGeunMo.ttf', size)
    return font
