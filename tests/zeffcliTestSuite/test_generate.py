# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff CLI test suite."""
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

import sys
import os
import io
import types
import pathlib
from . import chdir
import pytest
import zeff.cli
from zeff.cli.upload import upload
from zeff.cli.train import train
from zeff.cli.predict import predict


def test_upload_generate(chdir):
    args = [
        "upload",
        "--no-train",
        "--dry-run=validate",
        "--records-config-generator=tests.zeffcliTestSuite.generator.MockGenerator",
        f"--records-config-arg={pathlib.Path.cwd() / 'db.sqlite3'}",
        "--record-builder=tests.zeffcliTestSuite.builder.MockBuilder",
    ]
    options = zeff.cli.parse_commandline(args)
    upload(options)

    # Setup mock server to recieve upload


@pytest.mark.skip(reason="Need mock Zeff Cloud to test")
def test_train_generate():
    dirpath = os.path.dirname(__file__)
    options = types.SimpleNamespace(action="start")
    strio = io.StringIO()
    sys.stdout = strio
    train(options)


def test_predict_generate(chdir):
    args = [
        "predict",
        "--dry-run=validate",
        "--records-config-generator=tests.zeffcliTestSuite.generator.MockGenerator",
        f"--records-config-arg={pathlib.Path.cwd() / 'db.sqlite3'}",
        "--record-builder=tests.zeffcliTestSuite.builder.MockBuilder",
    ]
    options = zeff.cli.parse_commandline(args)
    upload(options)

    # Setup mock server to recieve predict
