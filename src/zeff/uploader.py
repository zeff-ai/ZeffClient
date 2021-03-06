# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff upload records to Zeff Cloud dataset."""
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
__all__ = ["Uploader"]

import logging
from .zeffcloud import ZeffCloudResourceMap
from .cloud.exception import ZeffCloudException
from .cloud.dataset import Dataset

LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


class Uploader:
    """Generator that will yield successfully uploaded records."""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-arguments

    def __init__(self, upstream, server_url, org_id, user_id, dataset_id):
        """Create new uploader.

        :param upstream: Generator of records to be uploaded.

        :param server_url: Root URL to the Zeff Cloud API server.

        :param org_id: The organization id for authorization access.

        :param user_id: The user id for authorization access.

        :param dataset_id: The dataset id that all uploads will be sent to.
        """
        self.server_url = server_url
        self.org_id = org_id
        self.user_id = user_id
        self.dataset_id = dataset_id
        self.upstream = upstream

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=server_url, org_id=org_id, user_id=user_id
        )
        self.dataset = Dataset(self.dataset_id, self.resource_map)

    def __iter__(self):
        """Return this object."""
        return self

    def __next__(self):
        """Return the next item from the container."""
        while True:
            try:
                record = next(self.upstream)
                return self.dataset.add_record(record)
            except ZeffCloudException as err:
                LOGGER_UPLOADER.exception(err)
