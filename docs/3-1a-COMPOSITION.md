# Experiment Composition

An experiment can be defined as a collection of tasks run by the ELCM that are identified by the same Execution ID.
The exact type and order of these tasks is defined by the information contained within the Experiment Descriptor,
that can refer to any of the Test Cases and UEs defined in the
[Facility Configuration](/docs/2-1_FACILITY_CONFIGURATION.md).

By using the information contained in all these entities, the ELCM generates the list of actions that form the
experiment, in a process know as 'Experiment Composition'. At this point, it is important to introduce a distinction
between two different kinds of tasks:

- **Top-Level Tasks**: Top-Level Tasks are those defined as direct members of the `Sequence` list of a V2 TestCase,
or inside the list identified by the UE or (V1) TestCase name. These tasks are always run in a sequence and can
define an `Order` value.

- **Child Tasks**: Child Tasks are defined inside the `Children` field of either a Top-Level or another Child task.
These tasks cannot define their own `Order`, and their execution is controlled by the logic defined in their Parent
task.

The composition process only affects to Top-Level tasks, which are considered as an indivisible action along with
their tree of child tasks: During the composition, all of the task definitions included in any of the UEs and
TestCases that are part of the Experiment Descriptor are included in a single sequence, which is then ordered
according to the `Order` field of each Top-Level task.

> If an experiment contains multiple tasks with the same `Order` value, then, these tasks will be planned together in
> their expected position, but the order between then is unspecified.

### Composition example

Assuming that an Experiment Descriptor that specify one UE (*SampleUE*) and two TestCases (*Sample1* and *Sample2*) is
received. And assuming that these contain the following Task Definitions:

#### SampleUE:

```yaml
SampleUE:
  - Order: 1
    Task: Run.Message
    Config: {Message: "UE Initialization"}
  - Order: 100
    Task: Run.Message
    Config: {Message: "UE Closure"}
```

#### Sample1:

```yaml
Sequence:
  - Order: 20
    Task: Flow.Sequence
    Children:
      - Task: Run.Message
        Config: {Message: "Sample1 - First child"}
      - Task: Run.Message
        Config: {Message: "Sample1 - Second child"}
```

#### Sample2:

```yaml
Sequence:
  - Order: 10
    Task: Flow.Sequence
    Children:
      - Task: Run.Message
        Config: {Message: "Sample2 - First child"}
      - Task: Run.Message
        Config: {Message: "Sample2 - Second child"}
```
Then, the execution of this experiment would result in the following log messages:

````text
UE Initialization
Sample2 - First child
Sample2 - Second child
Sample1 - First child
Sample1 - Second child
UE Closure
````


