# declares the shared sqlalchemy base all models inherit from

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
