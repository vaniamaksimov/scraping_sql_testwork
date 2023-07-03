from datetime import date

from pydantic import BaseModel, Extra

from src.models.holder import AuctionHolder
from src.models.region import Region
from src.models.status import AuctionStatus


class AuctionBase(BaseModel):
    class Config:
        extra = Extra.forbid


class AuctionCreate(AuctionBase):
    area: str
    site_id: str

    region: Region | None = None
    status: AuctionStatus
    auction_date: date
    deadline: date
    participation_fee: float

    auction_holder: AuctionHolder

    class Config(AuctionBase.Config):
        ...


class AuctionUpdate(AuctionBase):
    area: str
    site_id: str

    region: Region | None = None
    status: AuctionStatus
    auction_date: date
    deadline: date
    participation_fee: float

    auction_holder: AuctionHolder

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
