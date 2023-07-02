from src.crud.base import CrudBase
from src.models.auction import Auction
from src.schemas.session import SessionCreate, SessionUpdate


class AuctionCrud(CrudBase[Auction, SessionCreate, SessionUpdate]):
    ...


session_crud = AuctionCrud(Auction)
