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
        try:
            self.runMany()
        except Exception as e:
            self.Log(Level.ERROR, str(e))
            raise e

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
            self.Log(Level.ERROR, str(e))

        self.Verdict = Verdict.Max(self.Verdict, taskInstance.Verdict)

    @staticmethod
    def regexConditionText(key, pattern, negate) -> str:
        matchPattern = f"match regex '{pattern}'"
        return f"'{key}' {('does not ' if negate else '')} {('exist' if pattern is None else matchPattern)}"

    @staticmethod
    def regexConditionIsTrue(key, collection, regex) -> bool:
        if key in collection.keys():
            if regex is None:
                return True
            else:
                value = str(collection[key])
                return regex.match(value) is not None
        return False


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
        conditionText = self.regexConditionText(key, pattern, negate)

        goOn = True
        iteration = 0
        while goOn:
            if maxIterations is None or iteration < maxIterations:
                conditionIsTrue = self.regexConditionIsTrue(key, self.parent.Params, regex)
                goOn = not conditionIsTrue if negate else conditionIsTrue

                if goOn:
                    self.Log(Level.INFO, f"Condition ({conditionText}) verified. Starting iteration {iteration}")

                    flowState = {'Iter0': iteration, 'Iter1': iteration + 1}

                    for index, child in enumerate(self.Children, start=1):
                        self.runOne(child, f'It{iteration}Seq{index}', flowState)

                else:
                    self.Log(Level.INFO, f"Condition ({conditionText}) not verified. While loop finalized.")
            else:
                self.Log(Level.INFO, f"Maximum number of iterations ({maxIterations}) reached. While loop finalized.")
                goOn = False

            iteration += 1


class Select(SequenceBase):
    def __init__(self, logMethod, parent, params):
        super().__init__("Select", logMethod, parent, params)
        self.paramRules = {'Conditions': (None, True)}

    def inDepthSanitizeParams(self):
        def _className(instance): return type(instance).__name__

        conditions = self.params["Conditions"]

        if not isinstance(conditions, list):
            self.Log(Level.ERROR, f"Invalid 'Conditions' type: expected list, got {_className(conditions)}. Aborting")
            return False

        numConditions = len(conditions)
        numChildren = len(self.Children)
        if numConditions > numChildren or numConditions < numChildren-1:
            self.Log(Level.ERROR, f"Invalid number of conditions ({numConditions}): Must be the same or one less than "
                                  f"child tasks ({numChildren}). Aborting")

        for index, condition in enumerate(conditions):
            errorPrefix = f"Invalid condition in position {index}:"
            if not isinstance(condition, dict):
                self.Log(Level.ERROR, f'{errorPrefix} Expected a dictionary, got {_className(condition)}. Aborting')
                return False

            evaluate = "Evaluate" in condition.keys()
            key = "Key" in condition.keys()

            if evaluate == key:
                if evaluate:
                    self.Log(Level.ERROR, f"{errorPrefix} Only one of 'Evaluate` and 'Key' can be defined "
                                          f"at the same time. Aborting")
                else:
                    self.Log(Level.ERROR, f"{errorPrefix} Either of 'Evaluate` or 'Key' must be defined. Aborting")
                return False
        return True

    def runMany(self):
        conditions = self.params["Conditions"]

        needle = None
        conditionText = None
        for index, condition in enumerate(conditions):
            evaluate = condition.get("Evaluate", None)

            if evaluate is not None:
                try:
                    if eval(evaluate) is True:
                        needle = index
                        conditionText = f"Expression '{evaluate}' (expanded) is True"
                        break
                except Exception as e:
                    self.Log(Level.DEBUG, f"Exception while evaluating expression '{evaluate}' ({e}): "
                                          f"Condition will be considered as not verified. Moving on.")
            else:
                key = condition["Key"]
                pattern = condition.get("Pattern", None)
                negate = condition.get("Negate", False)
                regex = re.compile(pattern) if pattern is not None else None

                verified = self.regexConditionIsTrue(key, self.parent.Params, regex)
                verified = not verified if negate else verified

                if verified:
                    needle = index
                    conditionText = self.regexConditionText(key, pattern, negate)
                    break

        else:  # Nothing verified, check if there is a default branch
            if len(conditions) < len(self.Children):
                needle = len(self.Children) - 1
                conditionText = "None of the previous conditions are verified (default)"

        if needle is not None:
            self.Log(Level.INFO, f'Condition "{conditionText}" verified for branch {needle}. Executing.')
            flowState = {'Branch': needle}
            self.runOne(self.Children[needle], f'Case{needle}', flowState)
        else:
            self.Log(Level.INFO, "Conditions not verified for any branch. Nothing executed.")
