from .base import ObjectBase


class Obstacle(ObjectBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_price = "g7500"


class SmallTree(Obstacle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_price = "e7500"
