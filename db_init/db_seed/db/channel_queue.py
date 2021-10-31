from typing import Text
from sqlalchemy import Column, Enum, Text
from sqlalchemy.dialects import postgresql

from .base import Base


class ChannelQueue(Base):
    __tablename__ = "ChannelQueue"
    channel_link = Column("link", Text, primary_key=True)
    status = Column(Enum("ok", "error", "processing", "to_process"), default="to_process")
