from pydantic import BaseModel, Extra


class RegionBase(BaseModel):
    class Config:
        extra = Extra.forbid


class RegionCreate(RegionBase):
    name: str

    class Config(RegionBase.Config):
        ...


class RegionUpdate(RegionBase):
    name: str

    class Config(RegionBase.Config):
        ...


class RegionDB(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
