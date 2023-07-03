from pydantic import BaseModel, Extra


class AuctionBase(BaseModel):
    class Config:
        extra = Extra.forbid


class AuctionCreate(AuctionBase):
    class Config(AuctionBase.Config):
        ...


class AuctionUpdate(AuctionBase):
    class Config(AuctionBase.Config):
        ...


class AuctionDB(BaseModel):
    class Config:
        orm_mode = True
