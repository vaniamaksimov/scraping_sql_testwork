from datetime import date

from pydantic import BaseModel, Extra

from src.models.holder import AuctionHolder
from src.models.status import AuctionStatus
from src.schemas.holder import HolderDB
from src.schemas.region import RegionDB


class AuctionBase(BaseModel):
    class Config:
        extra = Extra.forbid


class AuctionCreate(AuctionBase):
    area: str
    site_id: str

    region_id: int | None = None
    status: AuctionStatus
    auction_date: date
    deadline: date
    participation_fee: float

    auction_holder_id: int

    class Config(AuctionBase.Config):
        ...


class AuctionUpdate(AuctionBase):
    area: str
    site_id: str

    region_id: int | None = None
    status: AuctionStatus
    auction_date: date
    deadline: date
    participation_fee: float

    auction_holder_id: int

    class Config(AuctionBase.Config):
        ...


class AuctionDB(BaseModel):
    id: int
    area: str
    site_id: str
    region_id: int | None
    status: AuctionStatus
    auction_date: date
    deadline: date
    participation_fee: float
    auction_holder_id: int

    class Config:
        orm_mode = True
