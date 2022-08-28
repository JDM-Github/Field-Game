from configuration import COLS, ROWS
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
# from kivy.animation import Animation

from field import GameField, Building, Obstacle
from interface import BoxStack
from resources import Energy, Gem, Gold


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_variable()
        self.all_widget()
        self.display_resource()
        self.setup_window()
        self.start_loop()

    def start_loop(self):
        self.start_clock = Clock.schedule_interval(
            lambda _: self.game_loop(), 1.0/60.0)

    def game_loop(self):
        self.check_input()

    def setup_window(self):
        self._move_key()
        self._keyboard = Window.request_keyboard(self._keyboard_close, self)
        self._keyboard.bind(
            on_key_down=self._keyboard_down_key, on_key_up=self._keyboard_up_key)

    def _keyboard_close(self):
        self._keyboard.unbind(
            on_key_down=self._keyboard_down_key, on_key_up=self._keyboard_up_key)
        self._keyboard = None

    def _keyboard_down_key(self, _, key, *__):
        if key[1] == "w":
            self.move_up = True
            self.move_down = False
        elif key[1] == "a":
            self.move_left = True
            self.move_right = False
        elif key[1] == "s":
            self.move_down = True
            self.move_up = False
        elif key[1] == "d":
            self.move_right = True
            self.move_left = False
        elif key[1] == "z":
            # self.field.check_revert_widget()
            # self.field.adder = 1.1
            # self.field.change_field_size()
            self.zoom_in = True
            self.zoom_out = False
        elif key[1] == "x":
            # self.field.check_revert_widget()
            # self.field.adder = 0.9
            # self.field.change_field_size()
            self.zoom_in = False
            self.zoom_out = True

    def _keyboard_up_key(self, _, key, *__):
        if key[1] == "w":
            self.move_up = False
        elif key[1] == "a":
            self.move_left = False
        elif key[1] == "s":
            self.move_down = False
        elif key[1] == "d":
            self.move_right = False
        elif key[1] == "z":
            self.zoom_in = False
        elif key[1] == "x":
            self.zoom_out = False

    def _move_key(self):
        self.zoom_in = False
        self.zoom_out = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def check_input(self):
        if self.zoom_in:
            self.field.check_revert_widget()
            self.field.adder = 1.01
            self.field.change_field_size()
        elif self.zoom_out:
            self.field.check_revert_widget()
            self.field.adder = 0.99
            self.field.change_field_size()
        if self.move_up:
            self.field.y -= 10
            self.field.check_field_pos()
        elif self.move_down:
            self.field.y += 10
            self.field.check_field_pos()
        if self.move_left:
            self.field.x += 10
            self.field.check_field_pos()
        elif self.move_right:
            self.field.x -= 10
            self.field.check_field_pos()

    def all_variable(self):
        ...

    def all_widget(self):
        self.all_box = Widget()
        self.stack = BoxStack()

        self.field = GameField()
        self.field.change_field_size(2)
        self.add_building()
        self.add_widget(self.field)
        self.add_widget(self.all_box)

    def display_resource(self):
        self.gold_ = Gold()
        self.energy_ = Energy()
        self.gem_ = Gem()

        self.add_widget(self.gold_)
        self.add_widget(self.energy_)
        self.add_widget(self.gem_)

    def add_building(self, position=None, size=None, color=None, type_=None):
        if type_ is None:
            self.field.add_widget(Building(
                position=position, size=size, color=None,
                block_width=self.get_block_size("width"), block_height=self.get_block_size("height"),
                field_pos=self.field.pos))

    def get_block_size(self, block):
        if block == "width":
            return self.field.width/(self.field.width/(self.field.width / COLS))
        elif block == "height":
            return self.field.height/(self.field.height/(self.field.height / ROWS))
