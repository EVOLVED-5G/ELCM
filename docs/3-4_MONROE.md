# MONROE experiments:

The ELCM is able to handle the execution of experiments using a [MONROE](https://github.com/MONROE-PROJECT) node. This
functionality requires:

- A physical or virtual MONROE node that is prepared to be controlled by the
  [TAP agent](https://github.com/MONROE-PROJECT/monroe-experiment-core/tree/master/schedulers/tap-agent)
- An OpenTAP instance configured with the required TAP instrument and steps for controlling the MONROE TAP agent
  (available as part of the [5Genesis TAP plugins](https://github.com/5genesis/TAP-plugins)), and has network
  connectivity with the MONROE node

This repository includes the files required for handling the execution of MONROE experiments, however, a small
preparation is needed before they can be used:

- The `MONROE_Base.TapPlan` file is a pre-configured TAP testplan that contains the required steps and external
  parameters required for controlling the MONROE TAP agent. Open this file using OpenTAP and confirm that no issues
  appear in the log. In particular:
    - Check that all steps where loaded successfully (should be 9 in total)
    - Check that the necessary result listeners are enabled in the `Set execution metadata` step
    - Check that your MONROE instrument is selected in all MONROE steps (`Start/List/Stop experiment`)
  > Errors stating that a result listener is missing or that the testplan version is below the one in use can be
  > ignored.
- Save the test plan and, if necessary, move it to another location. Note the absolute path of the file.
- Edit the `TestCases/MONROE_Base.yml` file. This is a special TestCase definition that is used for handling the
  execution of MONROE experiments and will not appear as a normal test case for experimenters. Change the `<<Replace
  with the location of your MONROE_Base testplan.>>` placeholder with the absolute path of `MONROE_Base.TapPlan`.
