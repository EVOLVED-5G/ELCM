from Task import Task
from Helper import Level
from Composer import TaskDefinition
from Experiment import Expander
from Executor import Verdict


class SequenceBase(Task):
    def __init__(self, name, logMethod, parent, params):
        super().__init__(name, parent, params, logMethod, None)

    def runOne(self, child: TaskDefinition, labelPrefix: str):
        taskInstance = child.GetTaskInstance(self.Log, self.parent, Expander.ExpandDict(child.Params, self.parent))
        taskInstance.Label = f'{labelPrefix}.{taskInstance.Label}' if taskInstance.Label is not None else labelPrefix
        try:
            taskInstance.Start()
        except Exception as e:
            taskInstance.params['Verdict'] = Verdict.Error
            self.Log(Level.Error, str(e))


class Sequence(SequenceBase):
    def __init__(self, logMethod, parent, params):
        super().__init__("Sequence", logMethod, parent, params)

    def Run(self):
        if len(self.Children) == 0:
            self.Log(Level.WARNING, f"Skipping execution: no children defined.")
            return

        for index, child in enumerate(self.Children, start=1):
            self.runOne(child, f'Seq{index}')


class Repeat(SequenceBase):
    def __init__(self, logMethod, parent, params):
        super().__init__("Repeat", logMethod, parent, params)
        self.paramRules = {'Times': (None, True)}

    def Run(self):
        if len(self.Children) == 0:
            self.Log(Level.WARNING, f"Skipping execution: no children defined.")
            return

        for iteration in range(self.params['Times']):
            for index, child in enumerate(self.Children, start=1):
                self.runOne(child, f'It{iteration}Seq{index}')
