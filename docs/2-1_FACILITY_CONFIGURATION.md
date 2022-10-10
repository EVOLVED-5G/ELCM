# Facility Configuration (Platform registry)

The exposed capabilities and functionality of the facility are defined by a set of files distributed in 4 folders
inside the root of the ELCM instance. These are:

- TestCases: Contains information about the available test cases that can be run by the facility.
- UEs: Contains specific actions required for using and releasing specific equipment of the facility during the
  execution of test cases.
- Resources: Contains the definition of certain equipment that can only be used by one experiment at a time.
- Scenarios: Additional configuration values that can be set during the deployment of a network slice.

## TestCases and UEs

The contents of the `UEs` and `TestCases` sub-folder describe the behavior of the 5Genesis Platform when an Experiment
execution request is received. These folders will be automatically generated (empty) if they do not exist. The ELCM will
load the contents of every `yml` file contained in these folders on startup and whenever the `Reload facility` button on
the web dashboard is pressed. The dashboard will also display a validation log (`Facility log`) which can be used in
order to detect errors on a TestCase or UE configuration.

#### Task definition fields:

- `Order`: Only for Top-Level Tasks ([Experiment Composition, Top-Level Tasks and Children](/docs/3-1a-COMPOSITION.md)).
Tasks are ordered using these values (low to high) during the Composition.
- `Task`: Task type identifier
- `Label`: Custom label to use for identifying the task inside the execution logs. Auto-generated if not specified.
- `Requirements`: List of platform resources required for the execution of the task
([Resources, Scenarios and Network Slices ](/docs/2-4_RESOURCE_SCENARIO_NS.md))
- `Config`: Dictionary of parameters for the task. These depend on the specific task type defined.
- `Children`: A list of task definitions (empty by default). How a task makes use of this information depends on the
specific task type.

### UEs
The files on the `UEs` folder describe the actions to perform when a certain UE is included in the `Experiment 
descriptor` received as part of the request (for example, initializing or configuring the UE). The `Composer` will
add the actions defined for every UE to the Tasks list. The following is an example of a yaml file that configures a
UE:

````yaml
TestUE:
    - Order: 1
      Task: Run.Dummy
      Requirements: [UE1]
      Config:
        Message: This is a dummy entity initialization
    - Order: 10
      Task: Run.Dummy
      Config:
        Message: This is a dummy entity closure
```` 

The name of the UE will be extracted from the initial key on the dictionary (not the name of the file). This key 
contains a list of every action to perform, described by the relative `Order` in which to run, the `Task` to perform 
(which correspond to the different Tasks defined in the `Executor.Tasks` package) and `Config` dictionary, which is 
different for every task and optionally a list of `Requirements`. These requirements correspond to the resources 
defined for the facility. (See "Facility resources" here 
[Resources, Scenarios and Network Slices ](/docs/2-4_RESOURCE_SCENARIO_NS.md)). Additional information about the
available tasks can be seen in [General Tasks](/docs/3-2a_GENERAL_TASKS.md).

> More information about the composition process can be found in
> [Experiment Composition, Top-Level Tasks and Children](/docs/3-1a-COMPOSITION.md).

### TestCases
Similarly to the UEs, the files in the ´TestCases´ folder define the actions required in order to execute a certain 
test case. The exact format of the TestCase depends on the specific version used, though most of the fields are shared.
New TestCases should be defined using the latest format available, which would support the most complete feature set.
However, for convenience, compatibility with older versions will be retained for as long as possible.

The version of the TestCase file is selected by setting the `Version` field to the corresponding value. If this field
is not present, the file will be processed as a V1 TestCase.

##### - V2 TestCase (`Version: 2`)

TestCases using this format explicitly specify all the information in separate fields. This means that all keys in the
root must have one of a set of specific values. This means that, instead of specifying the name of the TestCase as the
key value of the sequence of actions, it is set by using the `Name` field. It is not possible to define multiple
TestCases in a single file. The following is an example V2 TestCase:

````yaml
Version: 2
Name: Slice Creation
Sequence:
    - Order: 5
      Task: Run.SingleSliceCreationTime
      Config:
        ExperimentId: "@{ExperimentId}"
        WaitForRunning: True
        Timeout: 60
        SliceId: "@{SliceId}"
Standard: True
Distributed: False
Dashboard: {}
````

##### - V1 TestCase (`Version: 1` or missing)

TestCases using this format follow the same approach as for UE files. The following is an example V1 TestCase:

````yaml
Slice Creation:
    - Order: 5
      Task: Run.SingleSliceCreationTime
      Config:
        ExperimentId: "@{ExperimentId}"
        WaitForRunning: True
        Timeout: 60
        SliceId: "@{SliceId}"
Standard: True
Distributed: False
Dashboard: {}
````
