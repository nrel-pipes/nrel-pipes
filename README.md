# PIPES CLI Client

## Package Installation

For each Python project, normally we recommend to create a virtual environment for isolation, and install the package and its dependencies into it. The virtual environment could be created by using tools, like `virtualenv`, `conda`, `pipenv`, or Python's built-in `venv` module, based on your own flavor.

### Python Environment
* Python >= 3.7

Create a virtual Python environment using a tool you prefer, like `conda`, `virtualenv`, or `pipenv`, etc.
Then install this `pipes` client package and its dependecy `pipes_core`.

### Install Packages
After active your Python virtual environment, then you can install directly from the repository,

#### PIPES Client
```bash
$ pip install git+https://github.com/nrel-pipes/pipes-client.git@develop
```

Or you can install in editable after clone it,
```bash
$ git clone https://github.com/nrel-pipes/pipes-client.git
$ pip install -e .
```

#### PIPES Core

The PIPES client depends on [PIPES Core](https://github.com/nrel-pipes/pipes-core), so need to install it

```
$ pip install git+https://github.com/nrel-pipes/pipes-core.git@feature/project-init
```

Or you can install editable after clone it,
```bash
$ git clone https://github.com/nrel-pipes/pipes-core.git
$ git checkout feature/project-init
$ pip install -e .
```


## PIPES Service Setup

```bash
$ git submodule add https://github.com/nrel-pipes/pipes-protobufs.git pipes-protobufs
```

Note that in `.gitmodules`, a git branch is specified during the development. And, use the
command below to update submodule if need,

```bash
$ git submodule update --init --recursive
```

If it does not work, then try:

```bash
$ git submodule update --init --recursive --remote
```

Change to the root direcory of the repository, and populate gRPC client code using command below,

```bash
$ ./build_grpc.sh
```

## Command Reference

The PIPES CLI is a unified tool to manage the PIPES pipelines.

Synopsis

```bash
$ pipes <command-group> <subcommand> [parameters]
```

Command Groups

Use `--help` (boolean) option to check help text information of commmands and
subcommands. For example,

```bash
$ pipes --help
Usage: pipes [OPTIONS] COMMAND [ARGS]...

  PIPES CLI client

Options:
  --help  Show this message and exit.

Commands:
  config    config CLI client
  dataset   dataset operation commands
  model     model operation commands
  pipeline  pipeline operation commands
  project   project operation commands
```

For example

```bash
$ pipes project --help
```

### 1. Config Commands

The subcommands included:

* `pipes config service`
* `pipes config session`

### 2. Project Commands

Initialize project
```bash
$ pipes project create-project -f tests/data/templates/test_project.toml
```

Check project run progress
```bash
$ pipes project check-project-run-progress -p test1 -r 1
```

### 3. Model Commands

Create model run
```bash
$ pipes model list-models -p test1 -r 1
$ pipes model create-model-run -p test1 -r 1 -m dsgrid -f tests/data/templates/test_model_run.toml
```

Check model run progress
```bash
$ pipes model check-model-run-progress -p test1 -r 1 -m dsgrid -x model-run-1
```

Close a model run
```bash
$ pipes model close-model-run -p test1 -r 1 -m dsgrid -x model-run-1
```


### 4. Dataset Commands

Get checkin TOML template
```bash
$ pipes dataset get-checkin-template  --system ESIFRepoAPI
```

Checkin dataset
```bash
$ pipes dataset checkin-dataset -p test1 -r 1 -m dsgrid -x model-run-1 -f tests/data/templates/test_dataset.toml
```

### 5. Handoff Commands

Plan tasks into handoff
```bash
$ pipes handoff plan-tasks -f tests/data/templates/test_tasks.toml -p test1 -r 1 -m dsgrid -x model-run-1
```

Get Task information from handoff
```bash
$ pipes handoff get-task -p test1 -r 1 -m dsgrid -x model-run-1 -h handoff_id1 -i trans_1
```

List Tasks from handoff
```bash
$ pipes handoff list-tasks -p test1 -r 1 -m dsgrid -x model-run-1 -h handoff_id1 -t visualization
```

Create task vertex
```bash
$ pipes handoff create-tasks -p test1 -r 1 -m dsgrid -x model-run-1 -f tests/data/templates/test_qaqc.toml --task-pass
```

Get task status
```bash
$ pipes handoff get-task-status -p test1 -r 1 -m dsgrid -x model-run-1 -t check-wind
```

Update task status
```bash
$ pipes handoff update-task-status -p test1 -r 1 -m dsgrid -x model-run-1 -t check-wind --task-fail
```


### 6. Service Context

Get user context
```bash
$ pipes login
```
Choose a selection based on CLI prompts, and setup CLI session.

List modeling teams in PIPES
```bash
$ pipes service list-modeling-teams
```

Add new user to PIPES
```
$ pipes service add-user -u username -e test@example.gov -f first -l last
```
