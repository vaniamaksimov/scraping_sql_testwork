import re
from datetime import date, datetime

import dateparser
import scrapy
from scrapy.http.response.html import HtmlResponse

from src.nedradv.items import NedradvItem
from src.utils.re_patterns import Patterns


class AuctionsSpider(scrapy.Spider):
    name = "auctions"
    allowed_domains = ["nedradv.ru"]
    start_urls = ["https://nedradv.ru/nedradv/ru/auction"]

    async def parse(self, response: HtmlResponse):
        auctions_table = response.xpath('//tbody[@class="g-color-black-opacity-0_6"]/tr')
        for row in auctions_table:
            auction_link = row.xpath('./td[1]/a/@href').get()
            auction_id = re.search(Patterns.auction_id, auction_link).group(1)
            auction_area = row.xpath('./td[2]/a/text()').get().strip()
            auction_region = row.xpath('./td[3]/a/text()').get().strip()
            auction_status = row.xpath('./td[4]/a/text()').get().strip()
            yield response.follow(
                auction_link,
                callback=self.scrape_auction_data,
                cb_kwargs=dict(
                    auction_id=auction_id,
                    auction_area=auction_area,
                    auction_region=auction_region,
                    auction_status=auction_status,
                ),
            )
        next_page = await self.search_for_next_page(response)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    async def search_for_next_page(self, response: HtmlResponse) -> str | None:
        current_page_number: str | None = response.xpath(
            '//a[@class="safeparam u-pagination-v1__item'
            ' u-pagination-v1-4 g-rounded-50 g-pa-7-14 u-pagination-v1-4--active"]/text()'
        ).get()
        if current_page_number:
            current_page_number = int(current_page_number)
            return response.xpath(
                '//a[@class="safeparam u-pagination-v1__item'
                ' u-pagination-v1-4 g-rounded-50 g-pa-7-14 "]'
                f'[contains(text(), {current_page_number+1})]/@href'
            ).get()

    async def scrape_auction_data(
        self,
        response: HtmlResponse,
        auction_id: str,
        auction_area: str,
        auction_region: str,
        auction_status: str,
    ):
        start_datetime_text = (
            response.xpath(
                '//dt[contains(text(),"Место и время проведения")]/following-sibling::dd/text()'
            )
            .get()
            .strip()
        )
        deadline_text = (
            response.xpath(
                '//dt[contains(text(),"Срок подачи заявок")]/following-sibling::dd/text()'
            )
            .get()
            .strip()
        )
        auction_fee_text = (
            response.xpath(
                '//dt[contains(text(),"Стартовый платеж")]/following-sibling::dd/text()'
            )
            .get()
            .strip()
        )
        auction_holder = (
            response.xpath(
                '//dt[contains(text(),"Организатор")]/following-sibling::dd/text()'
            )
            .get()
            .strip()
        )
        data = {
            'auction_site_id': auction_id,
            'auction_area': auction_area,
            'auction_region': auction_region,
            'auction_status': auction_status,
            'auction_date': self.parse_auction_datetime(start_datetime_text),
            'auction_deadline': self.parse_deadline_date(deadline_text),
            'auction_patricipation_fee': self.parse_auction_fee(auction_fee_text),
            'auction_holder': auction_holder,
        }
        yield NedradvItem(data)

    def parse_auction_datetime(self, start_datetime_text: str) -> datetime:
        auction_date = re.search(Patterns.auction_date, start_datetime_text).group(1)
        auction_time = re.search(Patterns.auction_time, start_datetime_text).group(1)
        auction_timezone = re.search(
            Patterns.auction_timezone, start_datetime_text
        ).group(1)
        auction_datetime = dateparser.parse(' '.join([auction_date, auction_time]))
        auction_timezone
        return auction_datetime

    def parse_deadline_date(self, deadline_text: str) -> date:
        match = re.search(Patterns.auction_deadline, deadline_text)
        if not match:
            return
        deadline_str = match.group(0)
        return dateparser.parse(deadline_str, settings={'DATE_ORDER': 'DMY'}).date()

    def parse_auction_fee(self, auction_fee_text: str) -> int:
        ...


# 'Электронная площадка «ЭТП ГПБ» (www.etpgpb.ru), оператором которой является ООО «Электронная торговая площадка ГПБ». Дата — 2 октября 2023, в 11:00 (по московскому времени).'
# auction_date = re.search(Patterns.auction_date, text).group(1)
# auction_time = re.search(Patterns.auction_time, text).group(1)
# auction_timezone = re.search(Patterns.auction_timezone, text).group(1)
