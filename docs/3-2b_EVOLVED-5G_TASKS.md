# EVOLVED-5G specific tasks:

The following is a list of tasks specifically tailored for use on the EVOLVED-5G H2020 project. Configuration
values for these tasks can be set in the `evolved5g.yml` file at the root of the ELCM folder.

## Evolved5g.JenkinsJob

Initiates the execution of a Jenkins pipeline in the CI/CD infrastructure. The returned job ID will be published
as a variable for use later in the same experiment. Configuration values:

- Instance: Address of the instance where the pipeline will be launched.
- Job: Kind of job to launch.
- GitUrl: URL of the GitHub repository that contains the NetApp code.
- GitBranch: Repository branch that will be used by the pipeline.
- Version: Pipeline version, defaults to `'1.0'`
- PublishKey: Name of the key that will be used for storing the returned job id, defaults to `JenkinsJobId`

## Evolved5g.JenkinsStatus

Checks the status of the specified pipeline, and publishes the obtained value for later use in the same experiment.
Configuration values:

- JobId: Pipeline to check. Can be expanded from a previous JenkinsJob using `'@[Params.JenkinsJobId]'`.
- PublishKey: Name of the key that will be used for storing the returned status, defaults to `JenkinsJobStatus`

## Evolved5g.NefLoop

Starts/stops one of the UE movement loops configured in the NEF emulator. Configuration values:

- Supi: Supi of the UE to start/stop moving.
- Action: One of [`Start`, `Stop`], on any capitalization. Defaults to `Start`.
