import json
import time
import warnings
import keyboard
import win32api, win32con
import pyautogui


from selenium import webdriver
from keyboard_play import set_options, click, autorization, get_cursor_pos

username_info = json.load(open("./resources/user_info.txt"))

def run(game_url: str):
    warnings.filterwarnings("ignore")
    driver = webdriver.Chrome(options=set_options())
    username = username_info['username']
    password = username_info['password']
    autorization(driver, username, password)
    driver.get(game_url)
    board = driver.find_element_by_xpath('//cg-board')
    while (1):
        pass

# run('https://lichess.org/N2gaFQCT')

if __name__ == '__main__':
    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    while True:
        a = win32api.GetKeyState(0x01)
        b = win32api.GetKeyState(0x02)

        if a != state_left:  # Button state changed
            state_left = a
            print(a)
            if a < 0:
                print('Left Button Pressed')
            else:
                print('Left Button Released')

        if b != state_right:  # Button state changed
            state_right = b
            print(b)
            if b < 0:
                print('Right Button Pressed')
            else:
                print('Right Button Released')
        time.sleep(0.001)