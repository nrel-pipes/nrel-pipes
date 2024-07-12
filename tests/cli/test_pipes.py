#!/usr/bin/env python

"""Tests for `pipes` package."""

import json
import os
import pytest
import click
from dotenv import load_dotenv
from click.testing import CliRunner
from pipes_cmd.cli import cli as pipes_cli
from unittest.mock import patch

load_dotenv()

@click.group()
def main():
    """Main entry point for the CLI."""
    pass

main.add_command(pipes_cli.config)
# main.add_command(pipes_cli.session)
main.add_command(pipes_cli.project)

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture(autouse=True)
def test_session_command(runner):
    with patch('questionary.text') as mock_text, patch('questionary.password') as mock_password:
        mock_text.return_value.ask.return_value = os.environ['USERNAME']
        mock_password.return_value.ask.return_value = os.environ['PASSWORD']
        result = runner.invoke(main, ['config', 'session'])
        assert result.exit_code == 0
        assert 'token' in result.output
        print(result.output)

def test_config(runner):
    with patch('questionary.select') as mock_select:
        mock_select.return_value.ask.return_value = "[localhost] http://localhost:8080/"
        result = runner.invoke(main, ['config', 'server'])
        print(f"{result.output}")  # Print the output for debugging
        assert result.exit_code == 0
        assert 'Data' in result.output
        assert 'http://localhost:8080/' in result.output

def test_command_line_interface(runner):
    """Test the CLI."""
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert "Main entry point for the CLI" in result.output
    help_result = runner.invoke(main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

def test_project_create_and_get(runner):
    resp_project_get = runner.invoke(
        main,
        ["project", "get-project", "-n", "click_functional_test"]
    )
    assert resp_project_get.exit_code == 0
    result_project_get = json.loads(resp_project_get.output)
    print(result_project_get)

if __name__ == "__main__":
    runner = CliRunner()
    # Testing the config
    test_config(runner=runner)
    test_session_command(runner=runner)
    test_project_create_and_get(runner=runner)
    test_command_line_interface(runner=runner)
