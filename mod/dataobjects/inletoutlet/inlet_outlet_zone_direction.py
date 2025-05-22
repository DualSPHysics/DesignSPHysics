class InletOutletZone3DDirection():
    def __init__(self,direction=None) -> None:
        if direction is None:
            direction = [0.0,0.0, 0.0]
        self.direction: list = direction

    def save_values(self, values):
        self.direction = values["direction"]

class InletOutletZone2DDirection():
    def __init__(self,direction=None) -> None:
        if direction is None:
            direction:list = [0.0, 0.0]
        self.direction = direction

    def save_values(self, values):
        self.direction = values["direction"]