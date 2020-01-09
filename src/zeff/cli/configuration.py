# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff commandline configuration."""
__author__ = """Lance Finn Helsten <lanhel@zeff.ai>"""
__copyright__ = """Copyright © 2019, Ziff, Inc. — All Rights Reserved"""
__license__ = """
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__all__ = ["Configuration", "load_configuration"]


import sys
import dataclasses
import pathlib
import importlib
from configparser import ConfigParser, ExtendedInterpolation, ParsingError


class ConfigurationValidationException(Exception):
    """Exception that occurs while validating a configuration."""

    def __init__(self, cause, message):
        """Create new exception.

        :param cause: The exception that caused this exception to be thrown.

        :param message: The message associated with this exception.
        """
        super().__init__()
        self.cause = cause
        self.message = message

    def __str__(self):
        """Return message string for exception."""
        return self.message


@dataclasses.dataclass(init=False)
class Server:
    """Server configuration section."""

    server_url: str
    org_id: str
    user_id: str

    def __init__(self, config):
        self.server_url = config.get("server", "server_url")
        self.org_id = config.get("server", "org_id")
        self.user_id = config.get("server", "user_id")

    def validate(self):
        """Validate type and values of properties.

        This may convert properties to correct types (e.g. str to type).
        """

    def update(self, options):
        """Update configuration from command line options."""
        self.server_url = getattr(options, "server_url", self.server_url)
        self.org_id = getattr(options, "org_id", self.org_id)
        self.user_id = getattr(options, "user_id", self.user_id)

    def set_options(self, section):
        """Set options in the ConfigParser section."""
        section["server_url"] = self.server_url
        section["org_id"] = self.org_id
        section["user_id"] = self.user_id


@dataclasses.dataclass(init=False)
class Records:
    """Records configuration section."""

    # pylint: disable=too-many-instance-attributes

    datasetid: str
    dataset_title: str
    dataset_desc: str
    records_config_generator: object
    records_config_arg: str
    record_builder: object
    record_builder_arg: str
    record_validator: type

    def __init__(self, config):
        self.datasetid = config.get("records", "datasetid")
        self.dataset_title = config.get("records", "datatset_title", fallback="")
        self.dataset_desc = config.get("records", "dataset_desc", fallback="")
        self.records_config_generator = config.get(
            "records", "records_config_generator"
        )
        self.records_config_arg = config.get("records", "records_config_arg")
        self.record_builder = config.get("records", "record_builder")
        self.record_builder_arg = config.get("records", "record_builder_arg")
        self.record_validator = config.get("records", "record_validator")

    def validate(self):
        """Validate type and values of properties.

        This may convert properties to correct types (e.g. str to type).
        """

        def convert_mclass(attrname):
            path = getattr(self, attrname)
            if not path or not isinstance(path, str):
                return
            try:
                m_name, c_name = path.rsplit(".", 1)
                module = importlib.import_module(m_name)
                # logging.debug("Found module `%s`", m_name)
                value = getattr(module, c_name)
                setattr(self, attrname, value)
            except ValueError as err:
                raise ConfigurationValidationException(
                    err,
                    "Required value for [records]{0} missing or incorrect format: ``{1}``.".format(
                        attrname, path
                    ),
                )
            except ModuleNotFoundError as err:
                raise ConfigurationValidationException(
                    err,
                    "[records]{0} module `{1}` not found in PYTHONPATH={2}".format(
                        attrname, m_name, sys.path
                    ),
                )
            except AttributeError as err:
                raise ConfigurationValidationException(
                    err,
                    "[records]{0} class `{1}` not found in {2}".format(
                        attrname, c_name, m_name
                    ),
                )

        convert_mclass("records_config_generator")
        convert_mclass("record_builder")
        convert_mclass("record_validator")

    def update(self, options):
        """Update configuration from command line options."""
        self.datasetid = getattr(options, "datasetid", self.datasetid)
        self.records_config_generator = getattr(
            options, "records_config_generator", self.records_config_generator
        )
        self.records_config_arg = getattr(
            options, "records_config_arg", self.records_config_arg
        )
        self.record_builder = getattr(options, "record_builder", self.record_builder)
        self.record_builder_arg = getattr(
            options, "record_builder_arg", self.record_builder_arg
        )
        self.record_validator = getattr(
            options, "record_validator", self.record_validator
        )

    def set_options(self, section):
        """Set options in the ConfigParser section."""

        def path(obj):
            if isinstance(obj, str):
                return obj
            else:
                return f"{obj.__module__}.{obj.__name__}"

        section["datasetid"] = self.datasetid
        section["records_config_generator"] = path(self.records_config_generator)
        section["records_config_arg"] = self.records_config_arg
        section["record_builder"] = path(self.record_builder)
        section["record_builder_arg"] = self.record_builder_arg
        section["record_validator"] = path(self.record_validator)


@dataclasses.dataclass(init=False)
class Configuration:
    """CLI configuration.

    This loads from the ``zeff.conf`` configuration file and converts to
    typed objects for ease of use.

    :property server.server_url: The Zeff Cloud REST server URL.

    :property server.org_id: Organization ID for use in authentication.

    :property server.user_id: User ID  for use in authentication.

    :property records.datasetid: Dataset that defines where records
        should be uplaoded.

    :property records.records_config_generator: Class to construct
        the generator for building configuration values to be sent
        to the record builder.

    :property records.records_config_arg: Single argument to be given to the
        ``records_config_generator`` when created.

    :property records.record_builder: Class to construct the record builder.

    :property records.record_builder_arg: Single argument to be given to the
        ``record_builder`` when created.

    :property records.record_validator: Class to construct a record validator.
    """

    server: Server
    records: Records

    def __init__(self, config):
        """Create a configuration object from a ConfigParser object."""
        self.server = Server(config)
        self.records = Records(config)
        self.validate()

    def validate(self):
        """Validate type and values of properties.

        This may convert properties to correct types (e.g. str to type).
        """
        self.server.validate()
        self.records.validate()

    def update(self, options):
        """Update configuration from command line options."""
        self.server.update(options)
        self.records.update(options)
        self.validate()

    def write(self, filepointer):
        """Write configuration to file readable by ConfigParser."""
        self.validate()
        config = ConfigParser()
        for field in dataclasses.fields(self):
            config.add_section(field.name)
            obj = getattr(self, field.name)
            obj.set_options(config[field.name])
        config.write(filepointer)


def load_configuration() -> Configuration:
    """Load configuration from standard locations.

    Configuration files will be loaded in the following order such that
    values in later files will override those in earlier files:

        1. ``/etc/zeff.conf``
        2. ``${HOME}/.config/zeff/zeff.conf``
        3. ``${PWD}/zeff.conf``

    Variable substitution is available where a variable is of the form
    ``${section:option}``. If section is omitted then the current section
    will be used and then from the default section. In the default
    section there are some pre-defined values:

        ``${HOME}``
            Home directory of the user.

        ``${PWD}``
            The current working directory the application was started in.
    """

    config = ConfigParser(
        strict=True,
        allow_no_value=False,
        delimiters=["="],
        comment_prefixes=["#"],
        interpolation=ExtendedInterpolation(),
        defaults={"HOME": str(pathlib.Path.home()), "PWD": str(pathlib.Path.cwd())},
    )
    try:
        config.read(
            [
                pathlib.Path(__file__).parent / "configuration_default.conf",
                pathlib.Path("/etc/zeff.conf"),
                pathlib.Path.home() / ".config" / "zeff" / "zeff.conf",
                pathlib.Path.cwd() / "zeff.conf",
            ]
        )
    except ParsingError as err:
        sys.exit(err)

    return Configuration(config)
