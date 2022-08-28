from random import randint
from configuration import WINDOW_WIDTH, WINDOW_HEIGHT
from kivy.metrics import dp, sp
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty


class Tank(Widget):

    value = NumericProperty(2_500)
    value_limit = NumericProperty(5_000)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (dp(250), dp(50))
        self.display_background()
        self.display_label()
        self.bind(value=self.update_label_text)
        self.bind(size=self.change_possize, pos=self.change_possize)

    def display_background(self):
        self.background = Image(opacity=0.5, color=(0, 0, 0, 1))
        self.background.size = self.size
        self.add_widget(self.background)

    def display_label(self):
        self.label = Label(
            text=f"{self.value}/{self.value_limit}  ", halign="right", valign="center", font_size=sp(16))
        self.label.bind(size=self.label.setter("text_size"))
        self.label.size = self.size
        self.add_widget(self.label)

    def display_progress(self, color):
        self.progress = Image(color=get_color_from_hex(color))
        self.progress.size = (
            self.width * (self.value / self.value_limit), self.height)
        self.progress.pos = self.pos
        self.add_widget(self.progress)
        self.remove_widget(self.label)
        self.add_widget(self.label)

    def change_possize(self, *_):
        self.label.size = self.size
        self.label.pos = self.pos
        self.background.size = self.size
        self.background.pos = self.pos
        if hasattr(self, "progress"):
            self.progress.height = self.height
            self.progress.pos = self.pos
            self.update_progress()

    def update_label_text(self, *_):
        self.label.text = f"{self.value:,}/{self.value_limit:,}  "

    def update_progress(self):
        self.progress.width = self.width * (self.value / self.value_limit)


class Gold(Tank):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extend_to = "g"
        self.value = randint(100, self.value_limit)
        self.pos = (WINDOW_WIDTH - (self.width + dp(20)),
                    WINDOW_HEIGHT - (self.height + dp(20)))
        self.display_progress("#dbcb1d")


class Energy(Tank):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extend_to = "e"
        self.value = randint(100, self.value_limit)
        self.pos = (WINDOW_WIDTH - (self.width + dp(20)),
                    WINDOW_HEIGHT - ((self.height + dp(20))*2))
        self.display_progress("#1dacdb")


class Gem(Tank):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 50
        self.background.color = get_color_from_hex("#12de2d")
        self.background.opacity = 0.5
        self.extend_to = "e"
        self.width = (dp(150))
        self.pos = (WINDOW_WIDTH - (self.width + dp(20)),
                    WINDOW_HEIGHT - ((self.height + dp(20))*3))

    def update_label_text(self, *_):
        self.label.text = f"{self.value:,}  "
