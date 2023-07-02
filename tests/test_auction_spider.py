from datetime import date, datetime

import pytest

from src.models.auction_status import AuctionStatus
from src.nedradv.spiders.auctions import AuctionsSpider


@pytest.mark.parametrize(
    argnames=['deadline_string', 'expected_date'],
    argvalues=[
        ('до 29 августа 2023 года', date(2023, 8, 29)),
        ('протокол от 28.06.2023', date(2023, 6, 28)),
        ('протокол от 14.06.2023', date(2023, 6, 14)),
        ('протокол от 18.04.2023', date(2023, 4, 18)),
        ('№1670 от 14.12.2021', date(2021, 12, 14)),
        ('нет сведений', None),
        ('до 2 января 2021', date(2021, 1, 2)),
        ('протокол от 02.01.2023', date(2023, 1, 2)),
    ],
)
def test_parse_deadline_date(
    spider: AuctionsSpider, deadline_string: str, expected_date: date
):
    result = spider.parse_deadline_date(deadline_string)
    assert result == expected_date


@pytest.mark.parametrize(
    argnames=['auction_status_string', 'expected_enum'],
    argvalues=[
        ('Аннулирован', AuctionStatus.VOIDED),
        ('Закрыт', AuctionStatus.CLOSED),
        ('Открыт', AuctionStatus.OPEN),
        ('Отмена', AuctionStatus.CANCELED),
        ('Перенос', AuctionStatus.TRANSFER),
        ('Приостановлен', AuctionStatus.SUSPENDED),
        ('нет сведений', AuctionStatus.NO_DATA),
    ],
)
def test_parse_auction_status(auction_status_string: str, expected_enum: AuctionStatus):
    result = AuctionStatus(auction_status_string)
    assert result is expected_enum


def test_parse_auction_id(spider: AuctionsSpider):
    result = spider.parse_auction_id(
        'https://nedradv.ru/nedradv/ru/find_aucc?obj=2daff8ecf59464b8d45e50117335aafb'
    )
    assert result == '2daff8ecf59464b8d45e50117335aafb'


@pytest.mark.parametrize(
    argnames=['expected_date', 'auction_status', 'text'],
    argvalues=[
        (
            date(2023, 10, 2),
            AuctionStatus.OPEN,
            'Электронная площадка «ЭТП ГПБ» (www.etpgpb.ru), оператором которой является ООО «Электронная торговая площадка ГПБ». Дата — 2 октября 2023, в 11:00 (по московскому времени).',
        ),
        (
            date(2022, 12, 26),
            AuctionStatus.CANCELED,
            '26 декабря 2022',
        ),
        (
            date(2023, 6, 19),
            AuctionStatus.OPEN,
            'Электронная площадка «ЭТП ГПБ» (www.etpgpb.ru), оператором которой является ООО «Электронная торговая площадка ГПБ». Дата — 19 июня 2023 года, в 00:09 (время московское).',
        ),
    ],
)
def test_parse_auction_datetime(
    spider: AuctionsSpider,
    expected_date: datetime,
    auction_status: AuctionStatus,
    text: str,
):
    result = spider.parse_auction_datetime(text, auction_status)
    assert result == expected_date


@pytest.mark.parametrize(
    argnames=['expected', 'text'],
    argvalues=[
        (135206.0, '135 206 руб. (сто тридцать пять тысяч двести шесть)'),
        (130721.0, '130 721 (сто тридцать тысяч семьсот двадцать один)'),
        (
            108407370.0,
            '108 407 370 (сто восемь миллионов четыреста семь тысяч триста семьдесят)',
        ),
        (75000.0, '75 000 (семьдесят пять тысяч)'),
        (
            1676594739.06,
            '1 676 594 739,06 (один миллиард шестьсот семьдесят шесть миллионов пятьсот девяносто четыре тысячи семьсот тридцать девять рублей и 06 копеек)',
        ),
        (1.25, '1,25'),
    ],
)
def test_parse_auction_fee(spider: AuctionsSpider, expected: float, text: str):
    result = spider.parse_auction_fee(text)
    assert result == expected
