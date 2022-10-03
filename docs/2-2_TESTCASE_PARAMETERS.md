# TestCase parameters. Standard and Custom experiment. 

In order to control how each TestCase is handled by the 5GENESIS Portal and when using the Open APIs, several keys can
be added to the yaml description. These keys are:
 - `Standard`: Boolean. Indicates whether the TestCase is selectable from the list of Standard test cases. If not
   specified, this value defaults to 'False' if the `Custom` key is defined, 'True' otherwise.
 - `Custom`: List of strings. Indicates that the TestCase is a Custom test case and may accept parameters. If this
   value is set to an empty list ('[]') the test case is considered public and will appear on the list of Custom
   experiments for all users of the Portal. If the list contains one or more email addresses, the test case will be
   visible only to the users with matching emails.
 - `Parameters`: Dictionary of dictionaries, where each entry is defined as follows:
 ```yaml
"<Parameter Name>":
    Type: "String, used to guide the user as to what is the expected format"
    Description: "String, textual description of the parameter"
 ```

Parameters can be used to customize the execution of test cases. For example, a Test Case may be implemented using a
TAP test plan, that accepts an external parameter called 'Interval'. Using variable expansion the value of this
external parameter can be linked with the value of an 'Interval' (or a different name) parameter contained in the
experiment descriptor. 

It is also possible to define default values during variable expansion, which means that a Test Case can be defined
as 'Standard', where it will use the default values for all parameters, and 'Custom', where some values can be replaced
by the experimenter.

For more information see 'Variable expansion'
([Variable Expansion and Execution Verdict](/docs/3-3_VARIABLE_EXPANSION_VERDICT.md)).

> Parameters with the equal names from different test cases are considered to be **the same**: They will appear only
> once in the Portal when the user selects multiple test cases and will have the same value at run time. For example,
> if two different test cases define an 'Interval' parameter and are both included in the same experiment they will
> share the same value.
> - If it's necessary to configure these values separately please use different names.
> - If a parameter is defined in multiple test cases with different Type or Description a warning will be displayed on
> the ELCM interface. The information displayed on the Portal will correspond to one *(any one)* of the definitions.
