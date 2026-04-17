# Agent Guide

This file provides guidance to coding agent when working with code in this project repository.

## 1. Project Overview

**nrel-pipes** is the CLI wrapper for the **PIPES** platform — **P**ipeline for **I**ntegrated **P**rojects in **E**nergy **S**ystems. PIPES is a project management, data management, and workflow management layer for integrated modeling teams.

This Python [Click](https://click.palletsprojects.com/en/stable/) application serves as a CLI interface that
consumes the REST APIs exposed by the PIPES API server (built with FastAPI). Key capabilities surfaced through the UI include:


- **Workspace management** — create, update, and track projects and project runs
- **Model management** — manage models and catalog models (including IFAC variants)
- **Dataset management** — manage catalog datasets, uploads, and sharing
- **Pipeline visualization** — interactive DAG pipeline view (ReactFlow + Dagre)
- **Schedule view** — Gantt chart for project milestones and timelines
- **Team & access management** — teams, access groups, and user administration
- **Handoffs** — data handoff tracking between models within a project
- **Authentication** — AWS Cognito-based login, registration, password flows, and JWT token management


## 2. Architecture

The CLI entry point is `wrapper/__init__.py`, which dynamically imports and executes `pipes.cli.main:main`. The `pipes=wrapper:main` entry point (setup.py) routes all `pipes` shell commands here.

### `pipes/` — the main package

**`pipes/cli/`** — Click command groups, one file per resource (`project.py`, `team.py`, `dataset.py`, etc.). Each CLI command validates the session token, then delegates to a corresponding client method. The `main.py` assembles all command groups.

**`pipes/client/`** — HTTP client layer. `PipesClient` is assembled via multiple inheritance from resource-specific mixins (`ProjectClient`, `DatasetClient`, etc.), all extending `PipesClientBase` (`base.py`). `PipesClientBase` holds the `get/post/put/patch` methods and reads the Bearer token from `Session`.

**`pipes/config/`** — `ClientConfig` (pydantic-settings) reads `~/.pipes/config` (a dotenv-style file). Three server targets are defined: `local`, `dev`, `prod`. Config is initialized interactively via `pipes config init`.

**`pipes/auth.py`** — Uses `boto3` to call AWS Cognito (`USER_PASSWORD_AUTH`) and get an access token. `validate_session_token()` checks JWT expiry without signature verification.

**`pipes/session.py`** — `Session` persists the Cognito JWT to `~/.pipes/session` as JSON via `FileBasedSessionManager`. The CLI checks session validity before every command group.

**`pipes/template/`** — TOML templates for creating resources (projects, models, datasets, tasks). CLI commands expose `pipes <resource> template` to copy these defaults to disk.

### `pipes_sdk/` — standalone SDK (separate package)

An older/experimental SDK (`PipesClient` in `pipes_sdk/client.py`) with direct API calls. Not wired into the CLI; exists for programmatic use without the CLI session model.

### `pipes/sdk/` — thin wrapper

`pipes/sdk/core.py` contains a stub `PIPES` class that wraps `PipesClient`. Mostly unimplemented stubs.

### Data model hierarchy

Resources follow a strict nesting: **Project → ProjectRun → Model → ModelRun → Dataset/Task**. Most API calls require the full chain of parent names as query parameters (`project`, `projectrun`, `model`, `modelrun`).

## 3. Configuration

The CLI stores config at `~/.pipes/config` (dotenv format) and session tokens at `~/.pipes/session` (JSON). Run `pipes config init` to bootstrap. Switch server environments with `pipes server conf`.

## 4. Commands

### Devevelopment Commands
```bash
# Install for development
pip install -e .

# Run all tests
pytest

# Run a single test file
pytest tests/cli/test_config/test_session.py

# Run a specific test
pytest tests/cli/test_config/test_config.py::test_config

# Lint
make lint           # runs flake8 + black --check
make lint/flake8    # flake8 only
make lint/black     # black check only

# Run tests via tox (multiple Python versions)
tox

# Code coverage
make coverage
```

### CLI Commands

Please look into `pipes` commands for this project @README.md


## 5. Tests

Tests are under `tests/cli/`. They use Click's `CliRunner` and `unittest.mock.patch` to mock `questionary` prompts. Integration tests require `USERNAME` and `PASSWORD` env vars (loaded via `dotenv`).
