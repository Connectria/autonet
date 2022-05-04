from dataclasses import dataclass, field
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import String, VARCHAR
from sqlalchemy.orm import relationship
from .types import GUID
from .mixins import GUIDMixin, TimestampMixin, Updatable

from .base import mapper_registry


@mapper_registry.mapped
@dataclass
class Users(GUIDMixin, TimestampMixin, Updatable):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('username'),
    )
    __sa_dataclass_metadata_key__ = 'sa'

    username: str = field(default=None, metadata={'sa': Column(String(32), nullable=False)})
    email: str = field(default=None, metadata={'sa': Column(String(64), nullable=False)})
    description: str = field(default=None, metadata={'sa': Column(VARCHAR(300))})

    tokens: ['Tokens'] = field(
        default_factory=list,
        metadata={'sa': lambda: relationship('Tokens', cascade='all, delete, delete-orphan', backref='user')}
    )


@mapper_registry.mapped
@dataclass
class Tokens(GUIDMixin, TimestampMixin, Updatable):
    __tablename__ = 'tokens'
    __sa_dataclass_metadata_key__ = 'sa'

    user_id: str = field(default=None, metadata={'sa': Column('user_id', GUID, ForeignKey('users.id'), nullable=False)})
    description: str = field(default=None, metadata={'sa': Column(VARCHAR(300))})
    token: str = field(default=None, metadata={'sa': Column('token', VARCHAR(130), nullable=False)})

    # user: Users = field(
    #     default_factory=list, metadata={'sa': lambda: relationship('Users', back_populates='tokens')}
    # )
