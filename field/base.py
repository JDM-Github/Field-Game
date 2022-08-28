from kivy.uix.image import Image
from kivy.utils import get_random_color, get_color_from_hex

from interface import Information

from configuration import (
    BLOCK_HEIGHT, BLOCK_WIDTH, COLS, ROWS)


class ObjectBase(Image):

    def __init__(self, position=[(COLS/2)-1, (ROWS/2)-1], size=[3, 3],
                 block_width=BLOCK_WIDTH, block_height=BLOCK_HEIGHT, color=None, field_pos=[0, 0], **kwargs):
        super().__init__(**kwargs)
        self.all_variable()
        self.color = get_random_color(1) \
            if color is None else get_color_from_hex(color)
        if size is None or 0 < size[0] <= 6 or 0 < size[1] <= 6:
            size = [3, 3]
        if position is None or 0 < position[0] <= COLS or 0 < position[1] <= ROWS:
            position = [(COLS/2)-(size[0]//2), (ROWS/2)-(size[1]//2)]
        self.size = block_width * size[0], block_height * size[1]
        self.pos = block_width * position[0], block_height * position[1]
        self.old_x, self.old_y = self.pos
        self.base_size = size
        self.update_position(field_pos)

    def all_variable(self):
        self.parent_widget = None
        self.old_position = None

    def update(self):
        self.update_position()

    def update_position(self, field=None):
        # Update X / Y Position Using Old X / Old Y and adding it's Parent Size, For accurate Repositioning.
        self.x = self.old_x + (self.parent.x if field is None else field[0])
        self.y = self.old_y + (self.parent.y if field is None else field[1])

    def update_size(self):
        self.width = self.parent.block_width * self.base_size[0]
        self.height = self.parent.block_height * self.base_size[1]

    def determine_position(self):
        # Check if Old X / Y is inside of World.
        if self.check_if_in_way():
            if self.parent.revert_widget is self:
                self.parent.revert_widget = None
            self.old_x = 0 if self.old_x < 0 else (
                self.parent.width - self.width if self.old_x + self.width > self.parent.width else self.old_x)
            self.old_y = 0 if self.old_y < 0 else (
                self.parent.height - self.height if self.old_y + self.height > self.parent.height else self.old_y)
            # Determine the position.
            self.old_x = self.parent.block_width * \
                round((self.old_x / (self.parent.width / COLS)) %
                      (self.parent.width / (self.parent.width / COLS)))
            self.old_y = self.parent.block_height * \
                round((self.old_y / (self.parent.height / ROWS)) %
                      (self.parent.height / (self.parent.height / ROWS)))
        self.update_position()

    def check_if_in_way(self):
        left_down = (self.x + (self.parent.block_width / 2),
                     self.y + (self.parent.block_height / 2))
        right_down = (self.right - (self.parent.block_width / 2),
                      self.y + (self.parent.block_height / 2))
        left_top = (self.x + (self.parent.block_width / 2),
                    self.top - (self.parent.block_height / 2))
        right_top = (self.right - (self.parent.block_width / 2),
                     self.top - (self.parent.block_height / 2))
        for base in self.parent.children:
            if base is not self:
                if (base.collide_point(*left_down)
                    or base.collide_point(*right_down)
                    or base.collide_point(*left_top)
                        or base.collide_point(*right_top)):
                    self.parent.revert_widget = self
                    return False
        return True

    def on_top_widget(self):
        self.parent_widget = self.parent
        self.parent.remove_widget(self)
        self.parent_widget.add_widget(self)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.parent.current_hold is None:
            for box in self.parent.parent.all_box.children:
                if box.collide_point(*touch.pos):
                    break
            else:
                self.parent.current_hold = self
                if self.parent.revert_widget is not self:
                    self.old_position = (self.old_x, self.old_y)
                    self.parent.check_revert_widget()
                self.open_box()
                self.on_top_widget()
                self.grab_x = touch.x - self.old_x
                self.grab_y = touch.y - self.old_y
                touch.grab(self)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.close_box()
            self.old_x = touch.x - self.grab_x
            self.old_y = touch.y - self.grab_y
            self.update_position()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.determine_position()
            self.parent.current_hold = None
            touch.ungrab(self)
        return super().on_touch_up(touch)

    def information(self):
        return "This is Main Object"

    def open_box(self):
        self.close_box()
        info = Information(self)
        self.parent.parent.stack.add_widget(info)

        self.parent.parent.all_box.add_widget(self.parent.parent.stack)

    def close_box(self):
        # self.info.close()
        self.parent.parent.stack.clear_widgets()
        self.parent.parent.all_box.remove_widget(self.parent.parent.stack)
