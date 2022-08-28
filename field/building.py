from .base import ObjectBase


class Building(ObjectBase):

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self.price = "g1000"

    def information(self):
        return "Main Building Type Object."


class MainBuilding(Building):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
