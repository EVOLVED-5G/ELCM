from sys import maxsize
from typing import Mapping, Dict
from Helper import Log
from typing import List


class ActionInformation:
    def __init__(self):
        self.Order = maxsize  # Default to the lowest order
        self.TaskName = ''
        self.Label = None
        self.Config = {}
        self.Requirements: List[str] = []
        self.Children: List[ActionInformation] = []

    @classmethod
    def FromMapping(cls, data: Mapping, isFirstLevel: bool):
        res = ActionInformation()
        try:
            res.TaskName = data.get('Task', None)
            if res.TaskName is None:
                raise KeyError('Missing "Task" field')

            res.Order = data.get('Order', None)
            if res.Order is None and isFirstLevel:
                raise KeyError('Missing "Order" on a first level task')
            elif res.Order is not None and not isFirstLevel:
                raise KeyError('"Order" cannot be defined on a child task (uses list order)')

            res.Requirements = data.get('Requirements', [])
            if len(res.Requirements) > 0 and not isFirstLevel:
                raise KeyError('"Requirements" cannot be defined on a child task')

            res.Config = data.get('Config', {})
            res.Label = data.get('Label', None)
            children = data.get('Children', [])
            for index, child in enumerate(children, start=1):
                action, maybeError = ActionInformation.FromMapping(child, isFirstLevel=False)
                if action is not None:
                    action.Order = index
                    res.Children.append(action)
                else:
                    return None, f'Facility: Incorrect definition of child task: {maybeError} (Data="{child}")'
            return res, None
        except KeyError as e:
            message = f'Facility: Incorrect definition of task: {e} (Data="{data}")'
            Log.E(message)
            return None, message

    def __str__(self):
        label = '' if self.Label is None else f'({self.Label})'
        children = ', '.join(str(c) for c in self.Children)
        children = '' if len(children) == 0 else f'; Children: ({children})'
        return f'{self.TaskName}{label} [Order: {self.Order}; Config: {self.Config}{children}]'

    @staticmethod
    def DummyAction(config: Dict):
        res = ActionInformation()
        res.TaskName = 'Run.Dummy'
        res.Config = config
        return res

    @staticmethod
    def MessageAction(severity: str, message: str):
        res = ActionInformation()
        res.TaskName = 'Run.Message'
        res.Config = {
            'Severity': severity,
            'Message': message
        }
        return res
