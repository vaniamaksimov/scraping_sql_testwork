import scrapy


class AuctionsSpider(scrapy.Spider):
    name = "auctions"
    allowed_domains = ["nedradv.ru"]
    start_urls = ["https://nedradv.ru/nedradv/ru/auction"]

    def parse(self, response):
        # '//div[@class="col-lg-9 g-mb-50 g-mb-0--lg"]//tbody[@class="g-color-black-opacity-0_6"]//tr'  Список ссылок
        pass
