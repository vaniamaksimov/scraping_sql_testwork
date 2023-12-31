# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter

from src.core.database import AsyncSessionLocal
from src.crud.auction import auction_crud
from src.crud.holder import holder_crud
from src.crud.region import region_crud
from src.schemas.auction import AuctionCreate, AuctionUpdate
from src.schemas.holder import HolderCreate
from src.schemas.region import RegionCreate


class NedradvPipeline:
    async def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        async with AsyncSessionLocal() as session:
            parsed_item = ItemAdapter(item)
            db_auction = await auction_crud.get(
                session, site_id=parsed_item['auction_site_id']
            )
            db_holder = None
            if parsed_item['auction_holder']:
                db_holder = await holder_crud.get(
                    session, name=parsed_item['auction_holder']
                )
                if not db_holder:
                    db_holder = await holder_crud.create(
                        session, HolderCreate(name=parsed_item['auction_holder'])
                    )
            region_db = None
            if parsed_item['auction_region']:
                region_db = await region_crud.get(
                    session=session, name=parsed_item['auction_region']
                )
                if not region_db:
                    region_db = await region_crud.create(
                        session, RegionCreate(name=parsed_item['auction_region'])
                    )
            if db_auction:
                await auction_crud.update(
                    session,
                    db_auction,
                    AuctionUpdate(
                        area=parsed_item['auction_area'],
                        site_id=parsed_item['auction_site_id'],
                        region_id=region_db.id,
                        status=parsed_item['auction_status'],
                        auction_date=parsed_item['auction_date'],
                        deadline=parsed_item['auction_deadline'],
                        participation_fee=parsed_item['auction_patricipation_fee'],
                        auction_holder_id=db_holder.id,
                    ),
                )
            else:
                await auction_crud.create(
                    session,
                    AuctionCreate(
                        area=parsed_item['auction_area'],
                        site_id=parsed_item['auction_site_id'],
                        region_id=region_db.id if region_db else None,
                        status=parsed_item['auction_status'],
                        auction_date=parsed_item['auction_date'],
                        deadline=parsed_item['auction_deadline'],
                        participation_fee=parsed_item['auction_patricipation_fee'],
                        auction_holder_id=db_holder.id if db_holder else None,
                    ),
                )
        return item
