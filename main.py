from time import sleep
import keyboard
import json
from kivy.config import Config
from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
import codecs

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '500')

import keyboard_play

config = json.load(open("./resources/keyboard_config.txt"))
user_data = json.load(open("./resources/user_info.txt"))

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button, Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput


class MainFrame(BoxLayout):
    def __init__(self):
        super(MainFrame, self).__init__()


class ChessApp(App):
    fig_keys = DictProperty(config)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_text = 'Bind key to figure'

    @staticmethod
    def encrypt(password: str):
        return codecs.encode(password, 'rot_13')

    @staticmethod
    def decrypt(en_password):
        return codecs.decode(en_password, 'rot_13')

    def save_username(self):
        global user_data
        username = self.root.ids.username_input.text
        password = self.root.ids.password_input.text
        user_data["username"] = username
        user_data["password"] = password
        json.dump(user_data, open("./resources/user_info.txt", 'w'))

    def keyboard_listener(self, text):
        global config
        sleep(0.1)
        keyboard_key = keyboard.read_key()
        config[text] = keyboard_key
        self.fig_keys[text] = keyboard_key
        print(keyboard_key)
        json.dump(config, open("./resources/keyboard_config.txt", 'w'))

    def hide_pass(self):
        self.root.ids.password_input.password = not self.root.ids.password_input.password
        if self.root.ids.pass_hide_button.text == 'Hide':
            self.root.ids.pass_hide_button.text = 'Show'
        else:
            self.root.ids.pass_hide_button.text = 'Hide'

    def button_press(self, text):
        # with open("resources/keyboard_config", mode='w') as f:
        #     f.writelines(self.config)
        # print(self.config)
        pass

    def build(self):
        frame = MainFrame()
        return frame
    def run_browser(self):
        keyboard_play.run_analyser('https://lichess.org/N2gaFQCT')

if __name__ == '__main__':
    ChessApp().run()
