# Variable expansion

It's possible to expand the value of some variables enclosed by @{ }. (Use quotes where required in order to generate
valid YAML format). Available values are:
- `@{ExecutionId}`: Experiment execution ID (unique identifier)
- `@{SliceId}`, `@{DeployedSliceId}`: ID of the slice deployed by the Slice Manager during the PreRun stage
- `@{TempFolder}`: Temporal folder exclusive to the current executor, it's deleted when the experiment finishes.
- `@{Application}`: The `Application` field from the Experiment Descriptor
- `@{JSONParameters}`: The `Parameters` dictionary from the Experiment Descriptor, in JSON format (a single line string)
- `@{ReservationTime}`: The `ReservationTime` field of the Experiment Descriptor (minutes), or 0 if not defined
- `@{ReservationTimeSeconds}`: Same as above, but converted to seconds.
- `@{TapFolder}`: Folder where the (Open)TAP executable is located (as configured in `config.yml`)
- `@{TapResults}`: Folder where the (Open)TAP results are saved (as configured in `config.yml`)

Separate values from the `Parameters` dictionary can also be expanded using the following expressions:
- `@[Params.key]`: The value of `key` in the dictionary, or `<<UNDEFINED>>` if not found
- `@[Params.key:default]`: The value of `key` in the dictionary, or `default` if not found

> A keen reader may notice that these expressions are very similar to the ones defined for `Run.Publish`: They are 
> implemented together, but use different dictionaries when looking for values. When an expression does not include 
> a '.' the ELCM will fall back to looking at the Publish values (the default for Release A). If the collection 
> is not 'Publish' or 'Params', the expression will be replaced by `<<UNKNOWN GROUP {collection}>>`

# Task and execution verdicts

Each task that is part of an experiment is able to indicate a `Verdict` that defines in a concise way
the final status that was reached after its execution. This way, a task may reach a verdict of `Pass`,
if every action was completed successfully and the results were as expected, or an `Error` verdict if
it was impossible to complete the execution.

Similarly, an experiment execution is also able to reach a certain verdict, which in this case is the
**verdict with the highest severity among all executed tasks**. The severity and description of the
available verdicts can be seen below:

| Severity | Name           | Description                                                          |
|----------|----------------|----------------------------------------------------------------------|
| 0        | `NotSet`       | No verdict                                                           |
| 1        | `Pass`         | Execution completed and all values within required limits            |
| 2        | `Inconclusive` | Execution completed, but insufficient results or too close to limits |
| 3        | `Fail`         | Execution completed, but results outside the limits                  |
| 4        | `Cancel`       | Execution incomplete due to user request                             |
| 5        | `Error`        | Execution incomplete due to an error                                 |

For example, if an experiment consists on two tasks, and they reach verdicts of `Inconclusive` and `Pass`, then the
whole execution is considered `Inconclusive`.

The ELCM will automatically assign the `Cancel` verdict to any execution that receives a cancellation request
(however this verdict is free to use by any task that considers this necessary). In case of error, the selected
verdict is configurable:
 - Globally, by setting the `VerdictOnError` value on `config.yml` (`Error` by default).
 - Per task, by setting a particular `VerdictOnError` value in the parameters of the task.

> Handling of verdicts in the ELCM is based on the same concept in
> [OpenTAP](https://docs.opentap.io/Developer%20Guide/Test%20Step/#verdict) 
