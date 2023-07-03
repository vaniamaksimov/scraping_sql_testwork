from pydantic import BaseModel, Extra


class HolderBase(BaseModel):
    class Config:
        extra = Extra.forbid


class HolderCreate(HolderBase):
    class Config(HolderBase.Config):
        ...


class HolderUpdate(HolderBase):
    class Config(HolderBase.Config):
        ...


class HolderDB(BaseModel):
    class Config:
        orm_mode = True
