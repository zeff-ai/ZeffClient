# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff test suite."""
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

import os
import pathlib
import urllib.parse
import pytest

from zeff.recordgenerator import entry_generator, file_generator, directory_generator


def test_entries():
    path = pathlib.Path.cwd()
    entries = [p.name for p in path.iterdir() if not p.name.startswith(".")]
    for entry in (os.path.basename(p) for p in entry_generator(path)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0


def test_file_entries():
    path = pathlib.Path.cwd()
    entries = [p for p in path.iterdir() if p.is_file()]
    entries = [p.name for p in entries if not p.name.startswith(".")]
    for entry in (os.path.basename(p) for p in file_generator(path)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0


def test_dir_entries():
    path = pathlib.Path.cwd()
    entries = [p for p in path.iterdir() if p.is_dir()]
    entries = [p.name for p in entries if not p.name.startswith(".")]
    for entry in (os.path.basename(p) for p in directory_generator(path)):
        assert entry in entries
        entries.remove(entry)
    assert len(entries) == 0
