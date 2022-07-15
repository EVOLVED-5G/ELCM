from Task import Task
from Helper import Level
from time import sleep


class Repeat(Task):
    def __init__(self, logMethod, parent, params):
        super().__init__("Repeat", parent, params, logMethod, None)

    def Run(self):
        pass
