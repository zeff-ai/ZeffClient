# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff subcommand to train a machine."""
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
__all__ = ["train_subparser"]

import sys
import errno
from time import sleep
from tqdm import tqdm
from zeff.zeffcloud import ZeffCloudResourceMap
from zeff.cloud.exception import ZeffCloudException
from zeff.cloud.dataset import Dataset
from zeff.cloud.training import TrainingStatus
from .server import subparser_server


def train_subparser(subparsers, config):
    """Add the ``train`` sub-system as a subparser for argparse.

    :param subparsers: The subparser to add the train sub-command.
    """

    parser = subparsers.add_parser("train", help="""Control training sessions.""")
    parser.add_argument(
        "--records-datasetid",
        default=config.records.datasetid,
        help="""Dataset id to access for training.""",
    )
    subparser_server(parser, config)
    parser.set_defaults(func=train)

    actions = parser.add_subparsers(
        help="Send commands for training sessions on the specified dataset."
    )

    action_status = actions.add_parser(
        "status", help="Display status of current training session."
    )
    action_status.add_argument(
        "--continuous",
        default=False,
        action="store_true",
        help="Continuously display the status of the training session.",
    )
    action_status.set_defaults(action=Trainer.status)

    action_start = actions.add_parser(
        "start", help="Start or restart a training session."
    )
    action_start.set_defaults(action=Trainer.start)

    action_stop = actions.add_parser("stop", help="Stop the current training session.")
    action_stop.set_defaults(action=Trainer.stop)


def train(options):
    """Entry point for train subcommand."""
    if not options.records_datasetid:
        print("Unknown dataset id to access for training.", file=sys.stderr)
        sys.exit(errno.EINVAL)
    trainer = Trainer(options)
    options.action(trainer)


class Trainer:
    """Controller for dataset training."""

    def __init__(self, options):
        """Create new trainier controller."""
        self.options = options
        self.server_url = options.server_url
        self.org_id = options.org_id
        self.user_id = options.user_id
        self.dataset_id = options.records_datasetid

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=self.server_url, org_id=self.org_id, user_id=self.user_id
        )
        try:
            self.dataset = Dataset(self.dataset_id, self.resource_map)
        except ZeffCloudException as err:
            print("Error:", err, file=sys.stderr)
            sys.exit(errno.ENOENT)

    def status(self):
        """Print current status to stream."""

        def tstamp():
            return f"{tstate.updated_timestamp.strftime('%c')}"

        if self.options.continuous:

            def desc_str():
                return f"{tstate.status} ({tstamp()})"

            tstate = self.dataset.training_status
            pbar = tqdm(
                desc=desc_str(),
                total=100,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
            )
            while tstate.status is not TrainingStatus.complete:
                pbar.set_description(desc_str())
                pbar.update(tstate.progress)
                sleep(1.0)
                tstate = self.dataset.training_status
            pbar.close()
        else:
            tstate = self.dataset.training_status
            if tstate.status is TrainingStatus.unknown:
                print(f"Unknown training status")
            elif tstate.status is TrainingStatus.queued:
                print(f"Queued as of {tstamp()}")
            elif tstate.status is TrainingStatus.started:
                print(f"Started on {tstamp()}")
            elif tstate.status is TrainingStatus.progress:
                print(f"Progress {tstate.progress:.2%} as of {tstamp()}")
            elif tstate.status is TrainingStatus.complete:
                print(f"Completed on {tstamp()}")

    def start(self):
        """Start or restart the current training session."""
        try:
            self.dataset.start_training()
        except ZeffCloudException as err:
            print("Error:", err, file=sys.stderr)
            sys.exit(errno.ENOENT)

    def stop(self):
        """Stop the current training session."""
        try:
            self.dataset.stop_training()
        except ZeffCloudException as err:
            print("Error:", err, file=sys.stderr)
            sys.exit(errno.ENOENT)
