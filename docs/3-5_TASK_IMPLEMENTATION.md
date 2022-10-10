# Implementing additional tasks:

The ELCM is designed to be extensible, and thus, it is possible to easily integrate additional tasks. The basic steps
for defining a new task are:

1. Create a new Python file with a descriptive name, for example `compress_files.py`. This file must be saved in the
`/Execitor/Task/Run` subfolder of the ELCM

2. In this file, define a new class, for example `CompressFiles`, which inherits from `Task`. The constructor of this
class must have the signature displayed below:
    ```python
        class CompressFiles(Task):
        def __init__(self, logMethod, parent, params):
            super().__init__("Compress Files", parent, params, logMethod, None)
    ```
    In general, the parameters received in the constructor will be sent directly to the superclass, along with a Task
name (in the first parameter). The last parameter is an optional "Condition" method. If the `callable` passed in this
parameter evaluates to False, the execution of the Task will be skipped.

3. Override the `Run` method of the Task class. If this method is not overridden, a `NotImplementedError` will be raised
at runtime. See below for a list of inherited fields and methods.

4. In order to make the new Task available for use during an experiment execution, it is necessary to add a new import
directive to `/Executor/Tasks/Run/__init__.py`. In our example: `from .compress_files import CompressFiles`

After restarting the ELCM, the new Task will be available for use when defining new experiments. The Task identifier,
in this example, is `Run.CompressFiles`. The complete code of this example can be seen it the
`Executor\Run\compress_file.py` file. Other tasks in that folder can also be used as reference.

## Available fields:

- `self.name`: Contains the name of the Task.
- `self.parent`: Contains a reference to the Executor that called the task. Using this reference a Task can gain
access to additional information about the Experiment.
- `self.params`: Contains a dictionary with the parameters of the Task, expanded following the procedure described
in [Variable Expansion and Execution Verdict](/docs/3-3_VARIABLE_EXPANSION_VERDICT.md).
- `self.paramRules`: Set of validation rules to automatically apply on the parameters before the execution of the
task, with the following format: ```Dict[<ParameterName>: (<Default>, <Mandatory>)]```. If `<ParameterName>` has not
been defined, but it's not `<Mandatory>`, then it is assigned the `<Default>` value. If it's `<Mandatory` an exception
is generated and the task is aborted.
- `self.Label`: Task identifier, either auto-generated or specified within the TestCase definition.
- `self.Children`: List of child tasks.
- `self.Verdict`: Current verdict of the task.

## Available methods:

- `self.Publish(key, value)`: Saves a value under the key identifier. This value can be retrieved by Tasks that are
executed later in the same experiment execution (via parameter expansion as part of their own self.params dictionary).
- `self.SetVerdictOnError()`: Helper method for setting the task verdict to the correct value in case of error
(this is, the value specified in the `VerdictOnError` task parameter.)
- `self.GetVerdictFromName(name) -> Verdict`: Helper method for retrieving an (enum) Verdict instance from a str.

## Overridable methods:

- `self.inDepthSanitizeParams() -> bool`: Allows the implementation of additional parameter sanitization after the
initial validation described above (in `self.paramRules`). It is expected to return a boolean value where 'True'
means all validation is correct and 'False' indicates an error. Returns 'True' if not overridden.