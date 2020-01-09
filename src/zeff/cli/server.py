# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff commandline server access."""
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


def subparser_server(parser, config):
    """Add CLI arguments necessary for accessing a server."""

    parser.add_argument(
        "--server-url",
        default=config.server.server_url,
        help=f"""Zeff Cloud REST server URL (default: `{config.server.server_url}`).""",
    )
    parser.add_argument(
        "--org-id",
        default=config.server.org_id,
        help="""Organization id for access to Zeff Cloud (default: ``org_id``
            in configuration).""",
    )
    parser.add_argument(
        "--user-id",
        default=config.server.user_id,
        help="""user id for access to Zeff Cloud (default: ``user_id`` in
            configuration).""",
    )
