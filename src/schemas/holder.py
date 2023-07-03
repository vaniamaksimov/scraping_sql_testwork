from pydantic import BaseModel, Extra


class HolderBase(BaseModel):
    class Config:
        extra = Extra.forbid


class HolderCreate(HolderBase):
    name: str

    class Config(HolderBase.Config):
        ...


class HolderUpdate(HolderBase):
    name: str

    class Config(HolderBase.Config):
        ...


class HolderDB(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
