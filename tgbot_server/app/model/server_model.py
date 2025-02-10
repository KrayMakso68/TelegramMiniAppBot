from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.model.base_model import BaseModel


class Country(Base):
    __tablename__ = 'countries'

    code: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    servers = relationship("Server", back_populates="country_rel")


class Server(BaseModel):
    __tablename__ = 'servers'

    name: Mapped[str] = mapped_column(String, nullable=False)
    panel_url: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    subscribe_url: Mapped[str] = mapped_column(String, nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), ForeignKey("countries.code"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    country_rel = relationship("Country", back_populates="servers")
    subscriptions = relationship("Subscription", back_populates="server_rel")
