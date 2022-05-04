from dataclasses import dataclass, field
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DATETIME
from sqlalchemy.orm import validates
from uuid import uuid4

from .types import GUID


def read_only_validator(cls, k, v):
    """
    Raise an error if an update to a read-only field is requested.
    :param k: The attribute name.
    :param v: The value to be validated.
    :return:
    """
    if getattr(cls, k):
        raise ValueError(f'{k} cannot be modified.')
    return v


@dataclass
class GUIDMixin(object):
    __sa_dataclass_metadata_key__ = 'sa'
    id: str = field(default=None, metadata={'sa': Column(GUID, default=uuid4, nullable=False, primary_key=True)})

    @validates('id')
    def read_only(self, k, v):
        return read_only_validator(self, k, v)


@dataclass
class TimestampMixin(object):
    __sa_dataclass_metadata_key__ = 'sa'
    created_on: datetime = field(default=None, metadata={
        'sa': Column(DATETIME, default=datetime.utcnow(), nullable=False)})
    updated_on: datetime = field(default=None, metadata={
        'sa': Column(DATETIME, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)})

    @validates('created_on')
    def read_only(self, k, v):
        return read_only_validator(self, k, v)


class Updatable(object):
    def update(self, update: dict):
        for k, v in update.items():
            if hasattr(self, k):
                setattr(self, k, v)
