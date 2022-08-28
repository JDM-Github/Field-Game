from kivy.uix.stacklayout import StackLayout
from configuration import BOX_SIZE, WINDOW_WIDTH


class BoxStack(StackLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "lr-tb"
        self.bind(children=self.change_size)

    def change_size(self, *_):
        size = 0
        for _ in self.children:
            size += BOX_SIZE
        self.size = (size, size)
        self.pos = ((WINDOW_WIDTH/2)-(self.width/2), 10)
