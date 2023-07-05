import re
from datetime import date

import dateparser
import scrapy
from scrapy.http.response.html import HtmlResponse

from src.locators.auction import AuctionListLocators, AuctionPageLocators
from src.models.status import AuctionStatus
from src.nedradv.items import NedradvItem
from src.utils.re_patterns import Patterns


class AuctionsSpider(scrapy.Spider):
    name = "auctions"
    allowed_domains = ["nedradv.ru"]
    start_urls = ["https://nedradv.ru/nedradv/ru/auction"]

    async def parse(self, response: HtmlResponse):
        auctions_table = response.xpath(AuctionListLocators.auctions_table)
        for row in auctions_table:
            auction_link = row.xpath(AuctionListLocators.row_auction_link).get()
            auction_id = self.parse_auction_id(auction_link)
            auction_area = row.xpath(AuctionListLocators.row_auction_area).get()
            auction_region = row.xpath(AuctionListLocators.row_auction_region).get()
            auction_status = AuctionStatus(
                row.xpath(AuctionListLocators.row_auction_status)
                .get()
                .strip()
                .split()[0]
                .removeprefix(',')
                .removesuffix(',')
            )
            if auction_link:
                yield response.follow(
                    auction_link,
                    callback=self.scrape_auction_data,
                    cb_kwargs=dict(
                        auction_id=auction_id,
                        auction_area=auction_area.strip() if auction_area else None,
                        auction_region=auction_region.strip() if auction_region else None,
                        auction_status=auction_status,
                    ),
                )
        next_page = await self.search_for_next_page(response)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    async def search_for_next_page(self, response: HtmlResponse) -> str | None:
        current_page_number = response.xpath(AuctionListLocators.current_page).get()
        if current_page_number:
            return response.xpath(
                AuctionListLocators.next_page(current_page_number)
            ).get()

    async def scrape_auction_data(
        self,
        response: HtmlResponse,
        auction_id: str,
        auction_area: str,
        auction_region: str | None,
        auction_status: AuctionStatus,
    ):
        start_datetime_text = (
            response.xpath(AuctionPageLocators.auction_date(auction_status)).get().strip()
        )
        deadline_text = response.xpath(
            AuctionPageLocators.auction_deadline_text(auction_status)
        ).get()
        auction_fee_text = response.xpath(AuctionPageLocators.auction_fee).get()
        auction_holder = response.xpath(AuctionPageLocators.auction_holder).get()
        data = {
            'auction_site_id': auction_id,
            'auction_area': auction_area,
            'auction_region': auction_region,
            'auction_status': auction_status,
            'auction_date': self.parse_auction_datetime(
                start_datetime_text, auction_status
            ),
            'auction_deadline': self.parse_deadline_date(deadline_text.strip())
            if deadline_text
            else None,
            'auction_patricipation_fee': self.parse_auction_fee(auction_fee_text.strip())
            if auction_fee_text
            else None,
            'auction_holder': auction_holder.strip() if auction_holder else None,
        }
        yield NedradvItem(data)

    def parse_auction_id(self, auction_link: str) -> str | None:
        match = re.search(Patterns.auction_id, auction_link)
        if match:
            return match.group(1)

    def parse_auction_datetime(
        self, start_datetime_text: str, auction_status: AuctionStatus
    ) -> date:
        if auction_status is AuctionStatus.OPEN:
            auction_date = re.search(Patterns.auction_date, start_datetime_text).group(1)
            auction_time = re.search(Patterns.auction_time, start_datetime_text).group(1)
            auction_datetime = dateparser.parse(
                ' '.join([auction_date, auction_time])
            ).date()
        else:
            auction_datetime = dateparser.parse(start_datetime_text).date()
        return auction_datetime

    def parse_deadline_date(self, deadline_text: str) -> date | None:
        match = re.search(Patterns.auction_deadline, deadline_text)
        if not match:
            return
        deadline_str = match.group(0)
        return dateparser.parse(deadline_str, settings={'DATE_ORDER': 'DMY'}).date()

    def parse_auction_fee(self, auction_fee_text: str) -> float:
        match = re.search(Patterns.auction_fee, auction_fee_text)
        if not match:
            return
        return float(match.group(0).replace(' ', '').replace(',', '.'))
