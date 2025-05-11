from sqlalchemy import String, DECIMAL, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import Base, BaseModel


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
    password_enc: Mapped[str] = mapped_column(String, nullable=False)
    subscription_url: Mapped[str] = mapped_column(String, nullable=False)
    month_price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), default=0.00)
    country_code: Mapped[str] = mapped_column(String(2), ForeignKey("countries.code"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    country_rel = relationship("Country", back_populates="servers")
    subscriptions = relationship("Subscription", back_populates="server_rel")
