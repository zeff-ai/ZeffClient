# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff subcommand to manage dataset models."""
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
__all__ = ["models_subparser"]

import sys
import errno
from zeff.zeffcloud import ZeffCloudResourceMap
from zeff.cloud.dataset import Dataset
from .server import subparser_server


def models_subparser(subparsers, config):
    """Add the ``models`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the models sub-command.
    """

    parser = subparsers.add_parser("models", help="""Manage dataset models.""")
    parser.add_argument(
        "--records-datasetid",
        default=config.records.datasetid,
        help="""Dataset id for set of models to manage.""",
    )
    subparser_server(parser, config)
    parser.set_defaults(func=models)

    actions = parser.add_subparsers(help="Commands to manage models.")

    action_list = actions.add_parser("list", help="List all models in the dataset.")
    action_list.set_defaults(action=Models.list)


def models(options):
    """Entry point for models subcommand."""
    if not options.records_datasetid:
        print("Unknown dataset id for managing models.", file=sys.stderr)
        sys.exit(errno.EINVAL)
    controller = Models(options)
    options.action(controller)


class Models:
    """Controller for dataset models management."""

    # pylint: disable=too-few-public-methods

    def __init__(self, options):
        """Create new models manager."""
        self.options = options
        self.server_url = options.server_url
        self.org_id = options.org_id
        self.user_id = options.user_id
        self.dataset_id = options.records_datasetid

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=self.server_url, org_id=self.org_id, user_id=self.user_id
        )
        self.dataset = Dataset(self.dataset_id, self.resource_map)

    def list(self):
        """List all models in the dataset."""
        for model in self.dataset.models():
            print(
                f"{model.version:3d} {model.status} {model.updated_timestamp.strftime('%c')}"
            )
