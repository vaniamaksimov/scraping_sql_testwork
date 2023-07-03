from src.crud.base import CrudBase
from src.models.holder import AuctionHolder
from src.schemas.holder import HolderCreate, HolderUpdate


class HolderCrud(CrudBase[AuctionHolder, HolderCreate, HolderUpdate]):
    ...


holder_crud = HolderCrud(AuctionHolder)
