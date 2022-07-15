from Task import Task
from Helper import Level
from threading import Thread
from Composer import TaskDefinition
from Experiment import Expander
from Executor import Verdict


class ChildInfo:
    def __init__(self, definition: TaskDefinition):
        self.Thread = None
        self.TaskDefinition = definition
        self.TaskInstance = None


class Parallel(Task):
    def __init__(self, logMethod, parent, params):
        super().__init__("Parallel", parent, params, logMethod, None)

    def Run(self):
        if len(self.Children) == 0:
            self.Log(Level.WARNING, f"Skipping parallel execution: no children defined.")
            return

        self.Log(Level.INFO, f"Starting parallel execution ({len(self.Children)} children)")

        children: [ChildInfo] = []

        for index, child in enumerate(self.Children, start=1):
            if child.Label is None:
                child.Label = f"Br{index}"

            info = ChildInfo(child)
            info.TaskInstance = child.GetTaskInstance(
                self.Log, self.parent, Expander.ExpandDict(child.Params, self.parent))
            info.Thread = Thread(target=self.runChild, args=(info.TaskInstance,))
            children.append(info)

            info.Thread.start()
            self.Log(Level.DEBUG, f"Started branch {index}: {child.Label}")

        for index, info in enumerate(children, start=1):
            info.Thread.join()
            self.Log(Level.DEBUG, f"Branch {index} ({info.TaskDefinition.Label}) joined")

        self.Log(Level.INFO, f"Finished execution of all child tasks")

    def runChild(self, taskInstance: Task):
        try:
            taskInstance.Start()
        except Exception as e:
            taskInstance.params['Verdict'] = Verdict.Error
            self.Log(Level.Error, str(e))
