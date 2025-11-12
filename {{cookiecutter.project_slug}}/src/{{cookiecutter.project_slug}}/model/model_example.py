from sqlalchemy import (
    Column,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Model(Base):
    __tablename__ = "little_table"

    __table_args__ = (
        PrimaryKeyConstraint("id", "key", name="pk_key"),
    )

    id = Column(string, nullable=False)
    key = Column(String, nullable=False)
    
    
