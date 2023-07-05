from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.settings import settings
from src.models.status import AuctionStatus

if TYPE_CHECKING:
    from src.models.holder import AuctionHolder
    from src.models.region import Region


class Auction(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area: Mapped[str] = mapped_column(String(settings.app.max_string_length))
    site_id: Mapped[str] = mapped_column(
        String(settings.app.max_string_length), unique=True, index=True
    )

    region_id: Mapped[int] = mapped_column(
        ForeignKey('region.id', name='fk_auction_region'), nullable=True
    )
    region: Mapped[Optional['Region']] = relationship(
        back_populates='auctions', lazy='selectin'
    )

    status: Mapped[AuctionStatus] = mapped_column(Enum(AuctionStatus))
    auction_date: Mapped[date] = mapped_column(Date)
    deadline: Mapped[date] = mapped_column(Date, nullable=True)
    participation_fee: Mapped[float] = mapped_column(Float, nullable=True)

    auction_holder_id: Mapped[int] = mapped_column(
        ForeignKey('auctionholder.id', name='fk_auction_asuctionholder')
    )
    auction_holder: Mapped['AuctionHolder'] = relationship(
        back_populates='auctions', lazy='selectin'
    )

    def __init__(
        self,
        area: str,
        site_id: str,
        status: AuctionStatus,
        auction_date: date,
        auction_holder_id: int,
        participation_fee: float | None = None,
        deadline: date | None = None,
        region_id: int | None = None,
    ):
        self.area = area
        self.site_id = site_id
        self.status = status
        self.auction_date = auction_date
        self.deadline = deadline
        self.participation_fee = participation_fee
        self.auction_holder_id = auction_holder_id
        self.region_id = region_id
