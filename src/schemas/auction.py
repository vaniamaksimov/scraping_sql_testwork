from datetime import date

from pydantic import BaseModel, Extra

from src.models.status import AuctionStatus


class AuctionBase(BaseModel):
    class Config:
        extra = Extra.forbid


class AuctionCreate(AuctionBase):
    area: str
    site_id: str

    region_id: int | None = None
    status: AuctionStatus
    auction_date: date
    deadline: date | None = None
    participation_fee: float | None = None

    auction_holder_id: int | None = None

    class Config(AuctionBase.Config):
        ...


class AuctionUpdate(AuctionBase):
    area: str
    site_id: str

    region_id: int | None = None
    status: AuctionStatus
    auction_date: date
    deadline: date | None = None
    participation_fee: float | None = None

    auction_holder_id: int | None = None

    class Config(AuctionBase.Config):
        ...


class AuctionDB(BaseModel):
    id: int
    area: str
    site_id: str
    region_id: int | None
    status: AuctionStatus
    auction_date: date
    deadline: date | None
    participation_fee: float | None
    auction_holder_id: int | None

    class Config:
        orm_mode = True
