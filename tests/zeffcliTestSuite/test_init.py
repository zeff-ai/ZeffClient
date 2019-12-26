"""Zeff CLI test suite."""

import sys
import os
from pathlib import Path
from configparser import ConfigParser
from unittest.mock import MagicMock, patch
import re
import pytest
import zeff.cli
from zeff.cli.init import init_project, Project
from zeff.cloud import Dataset
from . import chdir, sys_path


@pytest.fixture(scope="session")
def zeff_configuration():
    from configparser import ConfigParser

    config = ConfigParser()
    config.add_section("server")
    config.set("server", "server_url", "https://example.com/zeffcloud")
    config.set("server", "org_id", "example_orgid_0123456789abcdef")
    config.set("server", "user_id", "example_userid_0123456789abcdef")
    config.add_section("records")
    config.set("records", "datasetid", "")
    config.set("records", "records_config_generator", "")
    config.set("records", "records_config_arg", "")
    config.set("records", "record_builder", "")
    config.set("records", "record_builder_arg", "")
    config.set("records", "record_validator", "zeff.validator.RecordValidator")
    return zeff.cli.Configuration(config)


def configuration_mock():
    config = ConfigParser(
        strict=True, allow_no_value=False, delimiters=["="], comment_prefixes=["#"]
    )
    config.add_section("server")
    config.set("server", "server_url", "https://example.com/mock")
    config.set("server", "org_id", "example_orgid_mock")
    config.set("server", "user_id", "example_userid_mock")
    config.add_section("records")
    config.set("records", "datasetid", "mock.dataset_id")
    config.set("records", "records_config_generator", "generator.MockGenerator")
    config.set("records", "records_config_arg", "${PWD}/generator_arg_mock")
    config.set("records", "record_builder", "builder.MockBuilder")
    config.set("records", "record_builder_arg", "${PWD}/builder_arg_mock")
    config.set("records", "record_validator", "validator.MockValidator")
    return config


def mock_user_input(prompt=None):
    mo = re.match(r"(?P<pstr>.+?) \[(?P<dstr>.*?)\]\?", prompt)
    assert mo is not None, f"Invalid prompt: `{prompt}`"
    response = {
        "Server URL": "https://example.com/mock",
        "Organization ID": "example_orgid_mock",
        "User ID": "example_userid_mock",
        "Dataset Title": "dataset_mock",
        "Dataset Description": "dataset_description_mock",
        "Configuration generator python name": "generator.MockGenerator",
        "Configuration generator init argument": str(Path.cwd() / "generator_arg_mock"),
        "Record builder python name": "builder.MockBuilder",
        "Record builder init argument": str(Path.cwd() / "builder_arg_mock"),
        "Record validator python name": "validator.MockValidator",
    }
    return response[mo.groupdict()["pstr"]]


def assert_zeff_conf():
    required = configuration_mock()
    path = Path.cwd() / "zeff.conf"
    config = ConfigParser(
        strict=True, allow_no_value=False, delimiters=["="], comment_prefixes=["#"]
    )
    config.read([path])
    for section in required.sections():
        for option in required.options(section):
            assert config.get(section, option) == required.get(section, option)


def test_init_new_project(tmpdir, chdir, sys_path, zeff_configuration):
    """Initialize a new project and verify files and contents."""
    tmpdir.chdir()
    sys.path.append(tmpdir.strpath)
    env = {}
    args = ["init", "generic"]
    options = zeff.cli.parse_commandline(args, config=zeff_configuration)
    with patch("builtins.input", new=mock_user_input) as mock_input:
        with patch("zeff.cloud.dataset.Dataset.create_dataset") as create:
            dataset = MagicMock(spec=Dataset)
            dataset.dataset_id = "mock.dataset_id"
            create.return_value = dataset
            init_project(options)
            assert_zeff_conf()


def test_init_existing_project(tmpdir, chdir, zeff_configuration):
    """Run init on existing project and verify files and contents."""
    tmpdir.chdir()
    sys.path.append(tmpdir.strpath)
    env = {}
    args = ["init", "generic"]
    options = zeff.cli.parse_commandline(args, config=zeff_configuration)
    with patch("builtins.input", new=mock_user_input) as mock_input:
        with patch("zeff.cloud.dataset.Dataset.create_dataset") as create:
            dataset = MagicMock(spec=Dataset)
            dataset.dataset_id = "mock.dataset_id"
            create.return_value = dataset
            init_project(options)

    def change_user_input(prompt=None):
        mo = re.match(r"(?P<pstr>.+?) \[(?P<dstr>.*?)\]\?", prompt)
        assert mo is not None, f"Invalid prompt: `{prompt}`"
        response = {
            "Configuration generator init argument": str(
                Path.cwd() / "generator_arg_mock"
            ),
            "Record builder init argument": str(Path.cwd() / "builder_arg_mock"),
        }
        return response.get(mo.groupdict()["pstr"], "")

    with patch("builtins.input", new=change_user_input) as mock_input:
        with patch("zeff.cloud.dataset.Dataset.create_dataset") as create:
            dataset = MagicMock(spec=Dataset)
            dataset.dataset_id = "mock.dataset_id"
            create.return_value = dataset
            init_project(options)
            assert_zeff_conf()
