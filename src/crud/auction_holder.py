from src.crud.base import CrudBase
from src.models.auction_holder import AuctionHolder
from src.schemas.session import SessionCreate, SessionUpdate


class AuctionHolderCrud(CrudBase[AuctionHolder, SessionCreate, SessionUpdate]):
    ...


session_crud = AuctionHolderCrud(AuctionHolder)
