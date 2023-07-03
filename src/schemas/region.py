from pydantic import BaseModel, Extra


class RegionBase(BaseModel):
    class Config:
        extra = Extra.forbid


class RegionCreate(RegionBase):
    class Config(RegionBase.Config):
        ...


class RegionUpdate(RegionBase):
    class Config(RegionBase.Config):
        ...


class RegionDB(BaseModel):
    class Config:
        orm_mode = True
