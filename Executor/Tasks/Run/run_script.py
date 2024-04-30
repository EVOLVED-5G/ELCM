from Task import Task
from Helper import Cli
import platform


class RunScript(Task):
    def __init__(self, logMethod, parent, params):
        super().__init__("CLI Execute", parent, params, logMethod, None)
        self.paramRules = {
            'Parameters': (None, True),
            'CWD': (None, True)
        }

    def Run(self):
        parameters = self.params['Parameters']
        if platform.system() == 'Windows':
            pass

        cli = Cli(parameters, self.params['CWD'], self.Log)
        cli.Execute()
