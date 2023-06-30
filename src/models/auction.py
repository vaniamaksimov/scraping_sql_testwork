from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.settings import settings
from src.models.auction_status import AuctionStatus

if TYPE_CHECKING:
    from src.models.auction_holder import AuctionHolder
    from src.models.region import Region


class Auction(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area: Mapped[str] = mapped_column(String(settings.app.max_string_length))

    region_id: Mapped[int] = mapped_column(
        ForeignKey('region.id', name='fk_auction_region')
    )
    region: Mapped['Region'] = relationship(back_populates='auctions', lazy='selectin')

    status: Mapped[AuctionStatus] = mapped_column(Enum(AuctionStatus))
    auction_date: Mapped[date] = mapped_column(Date)
    deadline: Mapped[date] = mapped_column(Date)
    participation_fee: Mapped[int] = mapped_column(Integer)

    auction_holder_id: Mapped[int] = mapped_column(
        ForeignKey('auctionholder.id', name='fk_auction_asuctionholder')
    )
    auction_holder: Mapped['AuctionHolder'] = relationship(
        back_populates='auctions', lazy='selectin'
    )

    def __init__(
        self,
        area: str,
        region: 'Region',
        status: AuctionStatus,
        auction_date: date,
        deadline: date,
        participation_fee: int,
        auction_holder: 'AuctionHolder',
    ):
        self.area = area
        self.region = region
        self.status = status
        self.auction_date = auction_date
        self.deadline = deadline
        self.participation_fee = participation_fee
        self.auction_holder = auction_holder
