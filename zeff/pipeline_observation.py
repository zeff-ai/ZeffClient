# -*- coding: utf-8 -*-
#  ____     __  __  ___ _ _         _
# |_  /___ / _|/ _|/ __| (_)___ _ _| |_
#  / // -_)  _|  _| (__| | / -_) ' \  _|
# /___\___|_| |_|  \___|_|_\___|_||_\__|
#
"""Reporter is a protocol that allows tracking of records in the pipeline."""
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
__all__ = [
    "pipeline_add_observer",
    "pipeline_remove_observer",
    "PipelinePhase",
    "PipelineLevel",
]

import enum
import datetime
import logging
from typing import Any, List


class PipelinePhase(enum.Enum):
    """Phase of record processing pipeline to observe."""

    Generate = logging.getLogger("zeffclient.record.generator")
    Build = logging.getLogger("zeffclient.record.builder")
    Validate = logging.getLogger("zeffclient.record.validator")
    Upload = logging.getLogger("zeffclient.record.uploader")


class PipelineLevel(enum.Enum):
    """Level of record processing events to observe."""

    Critical = logging.CRITICAL
    Error = logging.ERROR
    Warning = logging.WARNING
    Info = logging.INFO
    Debug = logging.DEBUG


def pipeline_add_observer(observer, phase: PipelinePhase, level: PipelineLevel):
    """Add an observer to watch pipeline events.

    This allows an event driven observation of the record generation,
    build, validate, and upload phases.

    :param observer: A observer object that will accept a single parameter
        of type PipelineEvent.

    :param phase: The PipelinePhase for events that should be delivered to
        the ``observer``.

    :param level: The minimum level for events that should be delivered to
        the ``observer``.
    """
    logger = phase.value
    handlers = [h for h in logger.handlers if isinstance(h, PipelineHandler)]
    if not handlers:
        handler = PipelineHandler(phase)
        logger.addHandler(handler)
        handlers = [handler]
    handlers[0].add_observer(observer, level)


def pipeline_remove_observer(observer, phase: PipelinePhase, level: PipelineLevel):
    """Remove an observer that is watching pipeline events.

    This will remove all instances of ``observer`` that is watching a
    given ``phase`` and minimum ``level``.

    :param observer: A observer object that will accept a single parameter
        of type PipelineEvent.

    :param phase: The PipelinePhase for events that should be delivered to
        the ``observer``.

    :param level: The minimum level for events that should be delivered to
        the ``observer``.
    """
    logger = phase.value
    handlers = [h for h in logger.handlers if isinstance(h, PipelineHandler)]
    if not handlers:
        return
    handlers[0].remove_observer(observer, level)


class PipelineEvent:
    """Represents an event in the ZeffClient pipeline.

    The pipeline will generate record configuration, build a record
    from the configuration, validate the record, and then upload the
    record to Zeff Cloud.
    """

    def __init__(self, phase: PipelinePhase, record: logging.LogRecord):
        self.__phase = phase
        self.__record = record

    def __str__(self):
        return f"{self.timestamp.isoformat()} [{self.phase.name}] {self.level.name}: {self.message}"

    @property
    def timestamp(self) -> datetime.datetime:
        """When the event was emitted."""
        return datetime.datetime.fromtimestamp(self.__record.created)

    @property
    def phase(self) -> PipelinePhase:
        """Pipeline phase that generated this event."""
        return self.__phase

    @property
    def level(self) -> PipelineLevel:
        """Pipeline level for this event."""
        for level in PipelineLevel:
            if level.value <= self.__record.levelno:
                return level
        return PipelineLevel.Debug

    @property
    def message(self) -> str:
        """Message that is part of the event."""
        return self.__record.getMessage()


class PipelineHandler(logging.Handler):
    """Logging handler for pipeline observation.

    When an observer is added to a phase then an object of this type
    will be added to the associated logger in order to receive
    log records from which events will be created.

    This allows the normall logging system to be used in an observable
    manner.
    """

    def __init__(self, phase: PipelinePhase):
        super().__init__(level=logging.DEBUG)
        self.phase = phase
        self.observers: List[Any] = []

    def add_observer(self, observer, level: PipelineLevel):
        """Add observer to this handler."""
        self.observers.append((observer, level))

    def remove_observer(self, observer, level: PipelineLevel):
        """Remove observer from this handler."""
        elems = [t for t in self.observers if t[0] == observer and t[1] == level]
        for elem in elems:
            self.observers.remove(elem)

    def emit(self, record):
        event = PipelineEvent(self.phase, record)
        for observer in (
            observer
            for observer, level in self.observers
            if level.value <= record.levelno
        ):
            observer(event)
