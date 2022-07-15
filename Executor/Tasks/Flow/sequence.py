from Task import Task
from Helper import Level
from time import sleep


class Sequence(Task):
    def __init__(self, logMethod, parent, params):
        super().__init__("Sequence", parent, params, logMethod, None)

    def Run(self):
        pass
