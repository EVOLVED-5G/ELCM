# Experiment Descriptor format

```text
{
  "Application": <str, may be null>
  "Automated": <bool>, 
  "ExclusiveExecution": <bool>, 
  "ExperimentType": <str>, 
  "Extra": <Object[str, str], may be empty>, 
  "NSs": <Array[Array[str]], (nsd id, vim location) pairs. May be empty>, 
  "Parameters": <Object[str, str], may be empty>,
  "Remote": <str, may be null>,
  "RemoteDescriptor": <Descriptor. Same format as an Experiment Descriptor, but without the “RemoteDescriptor” field. May be null>,
  "ReservationTime": <int, may be null>, 
  "Scenario": <str, may be null>,
  "Slice": <str, may be null>
  "TestCases": <Array[str]>,
  "UEs": <Array[str], may be empty>
  "Version": <str>
}
```