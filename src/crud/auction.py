from src.crud.base import CrudBase
from src.models.auction import Auction
from src.schemas.auction import AuctionCreate, AuctionUpdate


class AuctionCrud(CrudBase[Auction, AuctionCreate, AuctionUpdate]):
    ...


auction_crud = AuctionCrud(Auction)
