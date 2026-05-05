# PIPES Client

## 1. Package Installation

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

## 2. Client Config

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


## 3. CLI Commands

The PIPES CLI is a unified tool to manage the PIPES projects and pipelines.

Synopsis

```bash
$ pipes <command-group> <subcommand> [parameters]
```

The client requires user to login before calling the commands below.

```bash
$ pipes login
```


### 3.1 Project

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

### 3.2 Project Run

List all project runs under given project
```bash
$ pipes projectrun list -p <project-name>
```

### 3.3 Model

List all models under given project and project run
```bash
$ pipes model list -p <project-name> -r <project-run-name>
```


### 3.4 Model Run

List all model runs under given context
```bash
$ pipes modelrun list -p <project-name> -r <project-run-name> -m <model-name>
```


### 3.5 Dataset

List all datasets under given context
```bash
$ pipes dataset list -p <project-name> -r <project-run-name> -m <dataset-name> -x <model-run-name>
```

### 3.6 Task

List all tasks under given context
```bash
$ pipes task list -p <project-name> -r <project-run-name> -m <dataset-name> -x <model-run-name>
```

### 3.7 Handoff

List all handoffs under given context
```bash
$ TODO:
```

### 3.8 Team

3.8.1 List all modeling teams under given project,
```bash
$ pipes team list -p <project-name>
```

3.8.2 Get one team info with given project name and team name
```bash
$ pipes team get -p <project-name> -t <team-name>
```

3.8.3 Create a new team under given project
Get a team creation template,
```bash
$ pipes team template -t team-creation
```
Edit the template and provide all team information

Then, create the team from template,
```bash
$ pipes team create -p <project-name> -f team-creation.toml
```

### 3.9 User

3.9.1 List all users [Admin required]
```bash
$ pipes user list
```

3.9.2 Get a user by username (email)
```bash
$ pipes user get -u <email>
```

3.9.3 Create a new user in PIPES
```bash
$ pipes user create -u <email> -f <first-name> -l <last-name> -o <organization>
```


## 4. AI Coding Setup

This section provides guidance to setup AI coding agent and framework to assist the development of PIPES project.

### 4.1 Coding Assitant

There are many popular AI coding assistants, such as `Claude Code`, `GitHub Copilot`, `OpenAI Codex`,
`Gemini Coding Assistant` and so on. At NLR, we use Claude Code as coding assistant through Amazon Bedrock, please follow the steps below to setup.

**Install Claude Code**

https://code.claude.com/docs/en/quickstart

**Config the Models**
The initial models we setup are ANTHROPIC_MODEL=Sonnet4.6, ANTHROPIC_SMALL_FAST_MODEL=Haiku4.5.

Export the env variables below in your terminal session:


```text
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION='<aws-region>'
export ANTHROPIC_MODEL='<the-main-sonnet-model>'
export ANTHROPIC_SMALL_FAST_MODEL='<the-fast-haiku-model>'
```

These exports could be put into .bash_profile/.bashrc or .zshrc in user home dir, depending on the shell used on your machine.

**Set SSO credentials (Need to do everyday)**

Use NLR SSO login and find `pipes-llm-developer`under AWS account.

Click Access Keys and get SSO credentials, then paste into terminal session as well for exporting the AWS credentials.

Note: The SSO session would last for 8 hours, after that need to copy and paste new Access keys as credentials.

**Test Claude Code**

Start claude code by running claude command,

```bash
$ claude
```

### 4.2 Agentic Skills/Frameworks

Install agentic skills and frameworks to enhance Claude Code coding capability.

Enter claude code, and install plugins

```bash
/plugin
```

The following skills and frameworks are recommended:

* `superpowers`
* `context7`

Also, we need to install `openspec` for this project,

```bash
$ npm install -g @fission-ai/openspec@latest
```

Then navigate to the project root directory and initialize:

```bash
$ openspec init
```

## 5. Coding Workflow

PIPES adopts a hybrid spec-driven, test-driven development workflow using two complementary tools:

- **[OpenSpec](https://github.com/fission-ai/openspec)** — the planning layer. Structures feature proposals, spec deltas, design decisions, and task breakdowns before any code is written.
- **[Superpowers](https://github.com/obra/superpowers)** — the execution layer. A composable skill library for Claude Code that enforces TDD (RED-GREEN-REFACTOR), systematic debugging, and structured code review.

### Workflow Overview

```
Feature Request
      │
      ▼
 1. /opsx:propose       ← OpenSpec: create proposal, spec deltas, design, tasks
      │
      ▼
 2. Review & refine     ← Team reviews proposal.md, design.md, tasks.md
      │
      ▼
 3. /writing-plans      ← Superpowers: break tasks into TDD-ready steps
      │
      ▼
 4. /test-driven-development  ← Superpowers: implement each task RED→GREEN→REFACTOR
      │
      ▼
 5. /verification-before-completion  ← Superpowers: evidence-based sign-off
      │
      ▼
 6. /opsx:archive       ← OpenSpec: mark change complete, update base specs
```

### Step-by-Step Guide

**Step 1 — Propose (OpenSpec)**

Inside Claude Code, run:

```
/opsx:propose <change-name>
```

OpenSpec reads the codebase and existing specs, then generates a structured change under `openspec/changes/<change-name>/`:

```
openspec/changes/<change-name>/
├── proposal.md    # Rationale, objectives, scope
├── specs/         # Spec deltas — before/after requirement diffs
├── design.md      # Technical architecture and decisions
└── tasks.md       # Numbered implementation checklist (1.1, 1.2, 2.1 ...)
```

**Step 2 — Review**

Before writing any code, review `proposal.md`, `design.md`, and the spec deltas. Edit any of these files freely — OpenSpec is "fluid not rigid". The spec delta is the primary review artifact: it shows exactly what requirements are changing.

**Step 3 — Plan tasks (Superpowers)**

Once the proposal is agreed on, activate TDD-style planning:

```
/writing-plans
```

This breaks each item in `tasks.md` into bite-sized steps following the pattern: write failing test → verify failure → implement minimally → verify passing → commit.

**Step 4 — Implement with TDD (Superpowers)**

For each task, enforce RED-GREEN-REFACTOR:

```
/test-driven-development
```

Key rules the skill enforces:
- **RED**: Write one failing test first. Run it. Confirm it fails for the right reason.
- **GREEN**: Write the minimum code to make it pass. No extras.
- **REFACTOR**: Improve clarity while keeping all tests green.
- Any production code written before a failing test exists must be deleted entirely.

Run `tox` after each task to confirm nothing is broken.

**Step 5 — Verify (Superpowers)**

Before marking work done, run:

```
/verification-before-completion
```

This blocks "I think it works" claims and requires evidence (test output, manual checks) before closing a task.

**Step 6 — Archive (OpenSpec)**

Once all tasks are done and `tox` passes:

```
/opsx:archive
```

This moves the change to `openspec/changes/archive/` with a date prefix and updates the base specs, so future proposals have an accurate picture of the codebase.

### Quick Reference

| Situation | Tool | Command |
|---|---|---|
| Propose a new feature or fix | OpenSpec | `/opsx:propose <name>` |
| Resume in-progress work | OpenSpec | `/opsx:continue` |
| Break proposal into TDD steps | Superpowers | `/writing-plans` |
| Implement a task with TDD | Superpowers | `/test-driven-development` |
| Debug a failing test systematically | Superpowers | `/systematic-debugging` |
| Sign off on a completed task | Superpowers | `/verification-before-completion` |
| Archive a completed change | OpenSpec | `/opsx:archive` |


## 5. Technical Support
The CLI client is still under development mode, more commands will be available soon!

If any issue encountered, feel free to reach out to Jianli Gu (jianli.gu@nrel.gov).
