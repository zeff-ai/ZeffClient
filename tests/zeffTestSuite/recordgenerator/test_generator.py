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

from zeff.recordgenerator import generate


class mock_record:
    def __init__(self, url):
        self.url = url


def mock_builder(url):
    return mock_record(url)


def test_generate():
    urls = [
        "file://a/b/c",
        "http://example.com/x/y?spam=eggs",
        "gopher://example.com/rabbit/elmer",
    ]
    for record in generate(urls, mock_builder):
        assert record.url in urls
