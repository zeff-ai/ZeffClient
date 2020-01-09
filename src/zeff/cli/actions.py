# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff commandline argparse custom actions."""
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

import argparse
import importlib


class NamedClassObjectAction(argparse.Action):
    """Converts a string into a python class object if it exists."""

    # pylint: disable=too-few-public-methods

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """See argparse.Action."""

        if "default" in kwargs and isinstance(kwargs["default"], type):
            clazz = kwargs["default"]
            path = ".".join([clazz.__module__, clazz.__name__])
            kwargs["help"] = kwargs["help"].replace("%(default)s", path)
        else:
            kwargs["help"] = kwargs["help"].replace("%(default)s", "")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parse, namespace, values, option_string=None):
        """See argparse.Action."""

        try:
            m_name, c_name = values.rsplit(".", 1)
            module = importlib.import_module(m_name)
            obj = getattr(module, c_name)
            if not isinstance(obj, (type)):
                raise TypeError(
                    f"``{values}`` must a class object not ``{type(obj)}``."
                )
            setattr(namespace, self.dest, obj)
        except ValueError:
            raise ValueError(f"Argument ``{values}`` is not in class path format.")


class NamedCallableObjectAction(argparse.Action):
    """Converts a string into a python callable object if it exists."""

    # pylint: disable=too-few-public-methods

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """See argparse.Action."""

        if "default" in kwargs and isinstance(kwargs["default"], type):
            clazz = kwargs["default"]
            path = ".".join([clazz.__module__, clazz.__name__])
            kwargs["help"] = kwargs["help"].replace("%(default)s", path)
        else:
            kwargs["help"] = kwargs["help"].replace("%(default)s", "")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parse, namespace, values, option_string=None):
        """See argparse.Action."""

        try:
            m_name, c_name = values.rsplit(".", 1)
            module = importlib.import_module(m_name)
            obj = getattr(module, c_name)
            if not callable(obj):
                raise TypeError(
                    f"``{values}`` must a callable object not ``{type(obj)}``."
                )
            setattr(namespace, self.dest, obj)
        except ValueError:
            raise ValueError(f"Argument ``{values}`` is not in class path format.")
