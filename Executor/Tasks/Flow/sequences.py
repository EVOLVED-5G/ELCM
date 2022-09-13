from Task import Task
from Helper import Level
from Composer import TaskDefinition
from Experiment import Expander
from Executor import Verdict
from typing import Dict
import re


class SequenceBase(Task):
    def __init__(self, name, logMethod, parent, params):
        super().__init__(name, parent, params, logMethod, None)

    def Run(self):
        if len(self.Children) == 0:
            self.Log(Level.WARNING, f"Skipping execution: no children defined.")
            return

        self.runMany()

    def runMany(self):
        raise NotImplementedError

    def runOne(self, child: TaskDefinition, labelPrefix: str, flowState: Dict):
        taskInstance = child.GetTaskInstance(
            self.Log, self.parent, Expander.ExpandDict(child.Params, self.parent, flowState))
        taskInstance.Label = f'{labelPrefix}.{taskInstance.Label}' if taskInstance.Label is not None else labelPrefix
        try:
            taskInstance.Start()
            self.parent.params.update(taskInstance.Vault)  # Propagate any published values
        except Exception as e:
            taskInstance.Verdict = Verdict.Error
            self.Log(Level.Error, str(e))

        self.Verdict = Verdict.Max(self.Verdict, taskInstance.Verdict)


class Sequence(SequenceBase):
    def __init__(self, logMethod, parent, params):
        super().__init__("Sequence", logMethod, parent, params)

    def runMany(self):
        for index, child in enumerate(self.Children, start=1):
            self.runOne(child, f'Seq{index}', {})


class Repeat(SequenceBase):
    def __init__(self, logMethod, parent, params):
        super().__init__("Repeat", logMethod, parent, params)
        self.paramRules = {'Times': (None, True)}

    def runMany(self):
        for iteration in range(self.params['Times']):
            flowState = {'Iter0': iteration, 'Iter1': iteration + 1}

            for index, child in enumerate(self.Children, start=1):
                self.runOne(child, f'It{iteration}Seq{index}', flowState)


class While(SequenceBase):
    def __init__(self, logMethod, parent, params):
        super().__init__("While", logMethod, parent, params)
        self.paramRules = {'Key': (None, True),
                           'Pattern': (None, False),
                           'Negate': (False, False),
                           'MaxIterations': (None, False)}

    def runMany(self):
        key = self.params["Key"]
        pattern = self.params["Pattern"]
        negate = self.params["Negate"]
        maxIterations = self.params["MaxIterations"]

        regex = re.compile(pattern) if pattern is not None else None
        collection = self.parent.Params
        matchPattern = f"match regex '{pattern}'"
        condition = f"'{key}' {('does not ' if negate else '')} {('exist' if pattern is None else matchPattern)}"

        goOn = True
        iteration = 0
        while goOn:
            if maxIterations is None or iteration < maxIterations:
                if key in collection.keys():
                    if regex is None:
                        conditionIsVerified = True
                    else:
                        value = str(collection[key])
                        conditionIsVerified = (regex.match(value) is not None)
                else:
                    conditionIsVerified = False

                goOn = not conditionIsVerified if negate else conditionIsVerified

                if goOn:
                    self.Log(Level.INFO, f"Condition ({condition}) verified. Starting iteration {iteration}")

                    flowState = {'Iter0': iteration, 'Iter1': iteration + 1}

                    for index, child in enumerate(self.Children, start=1):
                        self.runOne(child, f'It{iteration}Seq{index}', flowState)

                else:
                    self.Log(Level.INFO, f"Condition ({condition}) not verified. While loop finalized.")
            else:
                self.Log(Level.INFO, f"Maximum number of iterations ({maxIterations}) reached. While loop finalized.")
                goOn = False

            iteration += 1


