# PIPES Clients

## Package Installation

Create a virtual Python environment using tools, like `conda`, `virtualenv`, `pipenv`, or Python `venv` module.

For example, by using Python `venv` module,
```bash
$ python3 -m venv venv
```

Then activate it,
```bash
$ source venv/bin/activate
```

Next, install this package from the remote repository,
```bash
$ pip install git+https://github.com/nrel-pipes/nrel-pipes.git@develop
```

Or you can clone and install it locally,
```bash
$ git clone https://github.com/nrel-pipes/nrel-pipes.git
$ pip install -e .
```

Validate the installation,

```bash
$ pipes --help
```

## Client Config

The client needs to be configured before running any command, run the following command first.
```bash
$ pipes config init
```

If you like to check the configuration, run the following command,
```bash
$ pipes config show
```

For developers, if you need local server for development, then switch the server by running this,
```bash
$ pipes server update
```

Validate the configuration, you can ping the server,
```bash
$ pipes server ping
```

If you see `pong` in console, then the config works!


## CLI Commands

The PIPES CLI is a unified tool to manage the PIPES projects and pipelines.

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
  ...
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
