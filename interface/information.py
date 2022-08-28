from kivy.uix.image import Image
from kivy.uix.label import Label
from .box_check import BoxChecker

from configuration import WINDOW_WIDTH, WINDOW_HEIGHT


class Information(BoxChecker):

    def __init__(self, widget, **kwargs):
        super().__init__(widget, **kwargs)
        self.source = "assets/InfoSprite.png"

    def display_info(self):
        self.info_holder = Image(size=(WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.5))
        self.info_holder.color = (0, 0, 0, 1)
        self.info_holder.center = self.info_holder.size
        self.info_holder.opacity = 0.5
        self.label = Label(text=self.widget.information())
        self.label.center = self.info_holder.center
        self.info_holder.add_widget(self.label)
        self.add_widget(self.info_holder)

    def open(self):
        self.display_info()

    def close(self):
        if hasattr(self, "info_holder"):
            self.remove_widget(self.info_holder)
