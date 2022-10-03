# Facility resources

It is possible to define a set of available local resources. These resources can be specified as requirements for the
execution of each kind of task inside a test case.

Resources are defined by including a YAML file in the `Resources` folder. The contents of these files are as follows:
- `Id`: Resource ID. This id must be unique to the facility and will be used to identify the resource on the test cases.
- `Name`: Name of the resource (visible on the ELCM dashboard).
- `Icon`: Resource icon (visible on the ELCM dashboard). Uses Font Awesome (only free icons)
[(Available icons)](https://fontawesome.com/icons?d=gallery&m=free), defaults to `fa-cash-register`.

Required resources are configured per task. When an experiment execution is received, the ELCM will generate a list of
all the required resources. When an experiment starts, all these resources will be *locked* and the execution of other
experiments with common requirements will be blocked until the running experiment finishes and their resources are
released.

# Scenarios and Network Slice deployment

A scenario is a collection of configuration values that are used to further customize the behavior of a deployed
slice. These values are defined as YAML files contained in the `Scenarios` folder, where each file contains a
dictionary with a single key (that defines the name of the Scenario). The value for this key is a second
dictionary that contains the collection of values that are to be customized by the Scenario.

When the experiment requests the deployment of a Network Slice the ELCM will create a NEST description. The NEST created
by the ELCM has 3 main parts:
 - A reference to a base slice descriptor, which must be available in the Katana Slice Manager.
 - A collection of values that are to be overridden from the base slice descriptor, taken from the selected Scenario.
 - A possibly empty list of references to Network Services that are to be included as part of the Network Slice.

A generated NEST has the following format:
````json5
{
  "base_slice_descriptor": {
    "base_slice_des_id": "<Base Slice Descriptor reference>"
    // Values from the selected Scenario are included here
  },
  "service_descriptor": {
    "ns_list": [
      {
        "nsd-id": "<Network Service ID>",
        "placement": "<Network Service Location>",
      } //, [...]
    ]  
  }
} 
````

For more information about Network Slice deployment refer to the
[Katana Slice Manager documentation](https://github.com/medianetlab/katana-slice_manager/tree/master/katana-schemas)
