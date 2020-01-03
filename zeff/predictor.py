# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff build, and upload record for Zeff Cloud to make a prediction."""
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
__all__ = ["Predictor"]

import logging
from .zeffcloud import ZeffCloudResourceMap
from .cloud.exception import ZeffCloudException, ZeffCloudModelException
from .cloud.dataset import Dataset
from .cloud.model import Model
from .cloud.training import TrainingStatus

LOGGER_UPLOADER = logging.getLogger("zeffclient.record.uploader")


class Predictor:
    """Upload a record to make prediction and report results.

    :param upstream: Generator of records to be uploaded.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-arguments

    def __init__(self, upstream, server_url, org_id, user_id, dataset_id, version):
        """Create a generator that will use a record to infer a prediction.

        :param upstream: The upstream record generator.

        :param server_url: The URL to the server that has the model.

        :param org_id: Organization ID for authorization to the model.

        :param user_id: User ID for authorization to the model.

        :param dataset_id: The dataset ID that contains the model.

        :param version: The model version to make inferences against. The
            default is the latest trained version.
        """
        self.upstream = upstream

        info = ZeffCloudResourceMap.default_info()
        self.resource_map = ZeffCloudResourceMap(
            info, root=server_url, org_id=org_id, user_id=user_id
        )
        dataset = Dataset(dataset_id, self.resource_map)
        if version is None:
            self.model = None
            for model in dataset.models():
                if model.status is not TrainingStatus.complete:
                    continue
                elif self.model is None:
                    self.model = model
                elif self.model.version < model.version:
                    self.model = model
            if self.model is None:
                raise ZeffCloudModelException("No completed models available")
        else:
            self.model = Model(dataset, version)

    def __iter__(self):
        """Return this object."""
        return self

    def __next__(self):
        """Return the next item from the container."""
        while True:
            try:
                record = next(self.upstream)
                ret = self.model.add_record(record)
                if ret is not None:
                    return ret
            except ZeffCloudException as err:
                LOGGER_UPLOADER.exception(err)
            except ZeffCloudModelException as err:
                LOGGER_UPLOADER.error(err)
                raise StopIteration()
