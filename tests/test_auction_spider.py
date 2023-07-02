from datetime import date

import pytest

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
