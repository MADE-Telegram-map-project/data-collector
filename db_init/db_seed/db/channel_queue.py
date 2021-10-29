from sqlalchemy import Column, BigInteger, Enum
from sqlalchemy.dialects import postgresql

from .base import Base


class ChannelQueue(Base):
    __tablename__ = "ChannelQueue"
    channel_id = Column("channel_id", BigInteger, primary_key=True)
    status = Column(Enum("ok", "error", "processing", "to_process"), default="to_process")
