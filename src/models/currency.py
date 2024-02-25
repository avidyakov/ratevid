from sqlalchemy import Column, DateTime, Numeric, String, Text, func

from . import Base


class Currency(Base):
    __tablename__ = "currencies"
    __table_args__ = {"schema": "app"}

    codename = Column(String, primary_key=True)
    rate = Column(Numeric)
    name = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', codename='{self.codename}')"
        )
