import json
import math
import time
import schedule
import requests
from lxml import html
from lxml import etree
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import warnings
import os
import win32api, win32con
import regex

import pynput
import keyboard

chromedriver_autoinstaller.install()

keyboard_keys = json.load(open("    ./resources/keyboard_config.txt"))
names_of_figures = keyboard_keys.keys()
list_of_keys = keyboard_keys.values()
print(list_of_keys)
print(names_of_figures)
chess_figures = ['pawn', 'right beat', 'left beat', 'queen', 'left rook', 'right rook', 'king', 'left knight', 'right knight', 'bishop']
board_coordinate_dict = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

key_to_figure = dict(zip(list_of_keys, chess_figures))

side_enum = {
    "left": 0,
    "right": 1
}

board_x = 0
board_y = 0
board_width = 0
board_height = 0
margin_param = 0.5
cell_size = [0, 0]
list_of_coord = [[]]
x_position_to_number = {}
y_position_to_number = {}


def click(x, y):
    win32api.SetCursorPos((x, y))
    # time.sleep(0.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def margin_to_center(pos: list):
    return int(pos[0] + board_x + margin_param * board_width / 8), int(
        pos[1] + board_y + margin_param * board_height / 8)


def determine_vert(position):
    for i in range(0, 8):
        if position[0] <= list_of_coord[0][i][0]:
            return i


def get_figure_position(driver, type_of_figure: str):
    tmp_pawns = driver.find_elements_by_xpath(f'//piece[@class="{type_of_figure}"]')
    parse_white_pawns = [i.get_attribute("style") for i in tmp_pawns]
    white_pawns = []
    for pawn in parse_white_pawns:
        white_pawns.append([int(float(i)) for i in regex.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)px', pawn)])
    # print(white_pawns)

    return white_pawns


def set_options():
    option = Options()
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    # option.add_argument("--headless")
    option.add_argument("--disable-infobars")
    option.add_argument("--kiosk")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    return option


def autorization(driver, username, password):
    driver.get('https://lichess.org/login')
    username_form = driver.find_element_by_id('form3-username')
    password_form = driver.find_element_by_id('form3-password')
    username_form.send_keys(username)
    password_form.send_keys(password)
    driver.find_element_by_xpath("//div[@class='one-factor']/button").click()
    time.sleep(0.2)

def get_cursor_pos():
    x, y = win32api.GetCursorPos()
    return x, y

# returns 0 if cell is black, 1 otherwise
def get_cell_number(cursor_position, board_pos):
    x, y = 0, 0
    for i in range(1, 8):
        if cursor_position[1] > board_pos[i - 1][0][1] and cursor_position[1] < board_pos[i][0][1]:
            y = 8 - i
    for i in range(1, 8):
        if cursor_position[0] > board_pos[0][i - 1][0] and cursor_position[0] > board_pos[0][i][0]:
            x = i
    return x, y


def run_analyser(game_url: str):
    global board_x, board_y, board_width, board_height, cell_size, list_of_coord
    warnings.filterwarnings("ignore")

    driver = webdriver.Chrome(options=set_options())
    autorization(driver, 'KappaGolden', '192204DeN')
    driver.get(game_url)
    board = driver.find_element_by_xpath('//cg-board')

    board_location = board.location
    board_size = board.size
    board_width = board_size["width"]
    board_height = board_size["height"]
    board_x = board_location["x"]
    board_y = board_location["y"]
    cell_size = (board_width / 8, board_height / 8)
    board_pos = [[(int(i * board_width / 8 + board_x), int(j * board_height / 8 + board_y)) for i in range(0, 8)]
                     for j in range(0, 8)]
    print('board_coords: ', board_pos)
    time.sleep(1)


    color_flag = 'black'
    try:
        if driver.find_elements_by_xpath('//div[@class= "cg-wrap orientation-white manipulable"]'):
            color_flag = "white"
    except NoSuchElementException:
        color_flag = 'black'
    print(color_flag)
    while test_key_listener(driver, color_flag) == True:
        pass
    time.sleep(1)


    while (1):
        keyboard_key = keyboard.read_key()
        current_cursor_pos = get_cursor_pos()
        if keyboard_key in list_of_keys:
            print(f'pressed key is: {keyboard_key}')
            tokens = key_to_figure[keyboard_key].split(' ')

            if (len(tokens) == 2):
                figure = tokens[1]
                num_of_figure = side_enum[tokens[0]]
                coord = get_figure_position(driver, color_flag + ' ' + figure)

                if len(coord) == 0:
                    print('no figure')
                    continue
                try:
                    print(
                        f'{figure} in position: {(coord[num_of_figure][0] + board_x + int(cell_size[0] / 2), coord[num_of_figure][1] + board_y + int(cell_size[1] / 2))}')
                    click(coord[num_of_figure][0] + board_x + int(cell_size[0] / 2),
                          coord[num_of_figure][1] + board_y + int(cell_size[1] / 2))
                except IndexError:
                    print("There is no figure")
                print('Figure is not exist')
            if (len(tokens) == 1):
                figure = tokens[0]
                if figure == 'beat':  # not implemented yet
                    print('beat')
                    continue
                coord = get_figure_position(driver, color_flag + ' ' + figure)
                if len(coord) == 0:
                    print('no figure')
                    continue

                if figure == 'bishop':
                    cell_num = get_cell_number(get_cursor_pos(), board_pos)
                    cell_color = (cell_num[0] + cell_num[1]) % 2

                    # now we must get position bishop on black cell
                    first_bishop_num = get_cell_number((coord[0][0] + board_x + int(cell_size[0] / 2), coord[0][1] + board_y + int(cell_size[1] / 2)), board_pos)
                    first_bishop_color = (first_bishop_num[0] + first_bishop_num[1]) % 2
                    if first_bishop_color == cell_color:
                        print('got it')
                        click(coord[0][0] + board_x + int(cell_size[0] / 2), coord[0][1] + board_y + int(cell_size[1] / 2))
                    else:
                        click(coord[1][0] + board_x + int(cell_size[0] / 2), coord[1][1] + board_y + int(cell_size[1] / 2))

                if figure == 'pawn':
                    cursor_pos = get_cursor_pos()
                    x, y = get_cell_number(cursor_pos, board_pos)
                    number = 0
                    try:
                        for pawn in coord:
                            pawn_x, pawn_y = get_cell_number((pawn[0] + board_x + int(cell_size[0] / 2),  pawn[1] + board_y + int(cell_size[1] / 2)), board_pos)
                            if pawn_x == x:
                                break
                            number += 1
                        click(coord[number][0] + board_x + int(cell_size[0] / 2), coord[number][1] + board_y + int(cell_size[1] / 2))
                    except IndexError:
                        print('pawn is not exist')


                if figure == 'king':
                    if len(coord) == 0:
                        print('no king')
                        continue
                    click(coord[0][0] + board_x + int(cell_size[0] / 2), coord[0][1] + board_y + int(cell_size[1] / 2))
                if figure == 'queen':
                    if len(coord) == 0:
                        print('no queen')
                        continue
                    click(coord[0][0] + board_x + int(cell_size[0] / 2), coord[0][1] + board_y + int(cell_size[1] / 2))

            click(*current_cursor_pos)

                #     f'{figure} in position: {(coord[0][0] + board_x + int(cell_size[0] / 2), coord[0][1] + board_y + int(cell_size[1] / 2))}')
                # click(coord[0][0] + board_x + int(cell_size[0] / 2), coord[0][1] + board_y + int(cell_size[1] / 2))
        else:
            pass  # dont handle other keys

        # time.sleep(0.1)


def test_key_listener(driver, color: str):
    def on_press(key):
        mouse_position = win32api.GetCursorPos()


if __name__ == '__main__':
    run_analyser('https://lichess.org/N2gaFQCT')
