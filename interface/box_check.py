from kivy.uix.image import Image

from configuration import BOX_SIZE


class BoxChecker(Image):

    def __init__(self, widget, **kwargs):
        super().__init__(**kwargs)
        self.size = (BOX_SIZE, BOX_SIZE)
        self.allow_stretch = True
        self.widget = widget
        self.already = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.already is False:
                self.already = True
                self.open()
            else:
                self.already = False
                self.close()
        return super().on_touch_down(touch)

    def open(self):
        pass

    def close(self):
        pass
