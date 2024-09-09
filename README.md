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

Validate the configuration, you can ping the server,
```bash
$ pipes server ping
```

If you see `pong` in console, then the config works!


For developers or testers, if you need local or dev server, then switch the server by running this,
```bash
$ pipes server conf
? Choose the PIPES server: (Use arrow keys)
 » [prod] https://pipes-api.nrel.gov
   [dev] https://pipes-api-dev.nrel.gov
   [local] http://localhost:8080
```


## CLI Commands

The PIPES CLI is a unified tool to manage the PIPES projects and pipelines.

Synopsis

```bash
$ pipes <command-group> <subcommand> [parameters]
```

The client requires user to login before calling the commands below.

```bash
$ pipes login
```


### 1. Project

1.1 Create project from given TOML file
```bash
$ pipes project create -f tests/data/templates/test_project.toml
```

Please note that the project name should be unique. If it's already exists, then
need to change the project name.

1.2 List all your projects with basic info,
```bash
$ pipes project list
```

1.2 Get detailed project by name
```bash
$ pipes project get -p <project-name>
```

1.3 Get the project owner info
```bash
$ pipes project get -p <project-name> --owner
```

### 2. Project Run

2.1 List all project runs under given project
```bash
$ pipes projectrun list -p <project-name>
```

### 3. Model

3.1 List all models under given project and project run
```bash
$ pipes model list -p <project-name> -r <project-run-name>
```


### 4. Model Run

4.1 List all model runs under given context
```bash
$ pipes modelrun list -p <project-name> -r <project-run-name> -m <model-name>
```


### 5. Dataset

5.1 List all datasets under given context
```bash
$ pipes dataset list -p <project-name> -r <project-run-name> -m <dataset-name> -x <model-run-name>
```

### 6. Task

6.1 List all tasks under given context
```bash
$ pipes task list -p <project-name> -r <project-run-name> -m <dataset-name> -x <model-run-name>
```

### 7. Handoff

7.1 List all handoffs under given context
```bash
$ TODO:
```

### 8. Team

8.1 List all modeling teams under given project,
```bash
$ pipes team list -p <project-name>
```

8.2 Get one team info with given project name and team name
```bash
$ pipes team get -p <project-name> -t <team-name>
```

8.3 Create a new team under given project
Get a team creation template,
```bash
$ pipes team template -t team-creation
```
Edit the template and provide all team information

Then, create the team from template,
```bash
$ pipes team create -p <project-name> -f team-creation.toml
```

### 9. User

9.1 List all users [Admin required]
```bash
$ pipes user list
```

9.2 Get a user by username (email)
```bash
$ pipes user get -u <email>
```

9.3 Create a new user in PIPES
```bash
$ pipes user create -u <email> -f <first-name> -l <last-name> -o <organization>
```

## Technical Support
The CLI client is still under development mode, more commands will be available soon!

If any issue encountered, feel free to reach out to Jianli Gu (jianli.gu@nrel.gov).
