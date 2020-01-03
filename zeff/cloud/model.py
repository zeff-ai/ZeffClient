# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Zeff Cloud Model access."""
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

import logging
import datetime
from .exception import ZeffCloudException, ZeffCloudModelException
from .resource import Resource
from .record import Record
from .training import TrainingStatus


LOGGER = logging.getLogger("zeffclient.record.uploader")


class Model(Resource):
    """Model in the Zeff Cloud API."""

    def __init__(self, dataset, version: int):
        """Load a model version from Zeff Cloud.

        :param dataset: The containing Dataset.

        :param version: Model version to load from Zeff Cloud API.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        super().__init__(dataset.resource_map)
        self.dataset = dataset
        self.dataset_id = dataset.dataset_id

        tag = self.dataset.dataset_type.model_tag
        resp = self.request(tag, dataset_id=dataset.dataset_id, version=version)
        if resp.status_code not in [200]:
            raise ZeffCloudException(resp, type(self), str(version), "load")
        self.__data = resp.json()["data"]
        assert self.__data["datasetId"] == dataset.dataset_id
        assert self.version == version

    @property
    def version(self) -> int:
        """Return the model version."""
        return int(self.__data["version"])

    @property
    def comments(self) -> str:
        """Return comments on this model version."""
        value = self.__data["comments"]
        return str(value) if value is not None else ""

    @property
    def status(self) -> TrainingStatus:
        """Return training status of this model."""
        value = self.__data["status"]
        return TrainingStatus(value if value is not None else "unknown")

    @property
    def progress(self) -> float:
        """Return progress, [0.0, 1.0], of model training session."""
        value = self.__data["percentComplete"]
        return float(value) if value is not None else 0.0

    @property
    def created_timestamp(self) -> datetime.datetime:
        """Return the timestamp when this model was created."""
        value = self.__data["createdAt"]
        if value is not None:
            ret = datetime.datetime.fromisoformat(value)
        else:
            ret = datetime.datetime.min
        return ret

    @property
    def updated_timestamp(self) -> datetime.datetime:
        """Return last updated timestamp of model training session status."""
        value = self.__data["updatedAt"]
        if value is not None:
            ret = datetime.datetime.fromisoformat(value)
        else:
            ret = self.created_timestamp
        return ret

    def records(self):
        """Return iterator over all records in the model.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        tag = self.dataset.dataset_type.model_list_tag
        resp = self.request(tag, dataset_id=self.dataset.dataset_id)
        if resp.status_code not in [200]:
            raise ZeffCloudException(resp, type(self), self.version, "list records")
        return (Record(self, d["recordId"]) for d in resp.json().get("data", []))

    def add_record(self, record):
        """Add a record to this model.

        :param record: The record data structure to be added.

        :raises ZeffCloudException: Exception in communication with Zeff Cloud.
        """
        if self.status is not TrainingStatus.complete:
            raise ZeffCloudModelException("Model training incomplete", model=self)
        tag = self.dataset.dataset_type.model_record_add_tag
        data = self.add_resource(record, record.name, "recordId", tag)
        return Record(self, data["recordId"])
