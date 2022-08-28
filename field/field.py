from configuration import COLS, ROWS, WINDOW_WIDTH, WINDOW_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image


class GameField(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = get_color_from_hex("#55FF88")
        self.size = WORLD_WIDTH, WORLD_HEIGHT
        self.pos = ((WINDOW_WIDTH / 2) - (WORLD_WIDTH / 2),
                    (WINDOW_HEIGHT / 2) - (WORLD_HEIGHT / 2))
        self.old_width = self.size[0]
        self.old_height = self.size[1]
        self.all_variable()
        self.bind(pos=self.change_all_pos, size=self.change_all_size)

    def all_variable(self):
        self.moved = False
        self.adder = 2
        self.minimum_size = 0.8
        self.maximum_size = 4
        self.minimum_pos = 0.2
        self.block_width = (self.width/(self.width/(self.width / COLS)))
        self.block_height = (self.height/(self.height/(self.height / ROWS)))
        self.grab_x = None
        self.grab_y = None
        self.current_hold = None
        self.revert_widget = None

    def check_revert_widget(self):
        if self.revert_widget is not None:
            self.revert_widget.old_x, self.revert_widget.old_y = self.revert_widget.old_position
            self.revert_widget.update_position()
            self.revert_widget = None

    def change_all_pos(self, *_):
        for children in self.children:
            children.update_position()

    def change_all_size(self, *_):
        self.block_width = (self.width/(self.width/(self.width / COLS)))
        self.block_height = (self.height/(self.height/(self.height / ROWS)))

    def change_field_size(self, adder=None):
        if adder is not None:
            self.adder = adder
        if self.check_field_size():
            self.old_width = self.width
            self.old_height = self.height
            self.width *= self.adder
            self.height *= self.adder
            self.x += ((self.old_width - self.width) / 2)
            self.y += ((self.old_height - self.height) / 2)
            for children in self.children:
                children.update_size()
                children.old_x *= self.adder
                children.old_y *= self.adder
                children.update_position()
            self.check_field_pos()

    def check_field_size(self):
        width = (self.width * self.adder) / WORLD_WIDTH
        height = (self.height * self.adder) / WORLD_HEIGHT
        if (width < self.minimum_size or width > self.maximum_size
                or height < self.minimum_size or height > self.maximum_size):
            return False
        return True

    def check_field_pos(self):
        max_x = self.width * self.minimum_pos
        max_r = WINDOW_WIDTH - max_x
        max_y = self.height * self.minimum_pos
        max_t = WINDOW_HEIGHT - max_y
        if (self.x > max_x):
            self.x = max_x
        elif (self.right < max_r):
            self.right = max_r
        if (self.y > max_y):
            self.y = max_y
        elif (self.top < max_t):
            self.top = max_t

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for children in self.children:
                if children.collide_point(*touch.pos):
                    break
            else:
                for box in self.parent.all_box.children:
                    if box.collide_point(*touch.pos):
                        break
                else:
                    self.grab_x = touch.x - self.x
                    self.grab_y = touch.y - self.y
                    touch.grab(self)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.moved = True
            self.x = touch.x - self.grab_x
            self.y = touch.y - self.grab_y
            self.check_field_pos()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            if self.moved is False:
                self.check_revert_widget()
                self.parent.all_box.remove_widget(self.parent.stack)
            self.moved = False
            self.grab_x = None
            self.grab_y = None
            touch.ungrab(self)
        return super().on_touch_up(touch)
