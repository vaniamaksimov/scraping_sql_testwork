from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.settings import settings

if TYPE_CHECKING:
    from src.models.auction import Auction


class AuctionHolder(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(settings.app.max_string_length))
    auctions: Mapped[list['Auction']] = relationship(back_populates='auction_holder')

    def __init__(self, name: str, auctions: list['Auction'] = None):
        self.name = name
        self.auctions = auctions or []
