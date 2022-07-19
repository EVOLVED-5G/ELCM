from Task import Task
from Helper import Level
from Composer import TaskDefinition
from Experiment import Expander
from Executor import Verdict
from typing import Dict


class SequenceBase(Task):
    def __init__(self, name, logMethod, parent, params):
        super().__init__(name, parent, params, logMethod, None)

    def runOne(self, child: TaskDefinition, labelPrefix: str, flowState: Dict):
        taskInstance = child.GetTaskInstance(
            self.Log, self.parent, Expander.ExpandDict(child.Params, self.parent, flowState))
        taskInstance.Label = f'{labelPrefix}.{taskInstance.Label}' if taskInstance.Label is not None else labelPrefix
        try:
            taskInstance.Start()
            self.parent.params.update(taskInstance.Vault)  # Propagate any published values
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
            self.runOne(child, f'Seq{index}', {})


class Repeat(SequenceBase):
    def __init__(self, logMethod, parent, params):
        super().__init__("Repeat", logMethod, parent, params)
        self.paramRules = {'Times': (None, True)}

    def Run(self):
        if len(self.Children) == 0:
            self.Log(Level.WARNING, f"Skipping execution: no children defined.")
            return

        for iteration in range(self.params['Times']):
            flowState = {'Iter0': iteration, 'Iter1': iteration + 1}

            for index, child in enumerate(self.Children, start=1):
                self.runOne(child, f'It{iteration}Seq{index}', flowState)
