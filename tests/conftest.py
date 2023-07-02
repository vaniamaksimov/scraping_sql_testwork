import pytest

from src.nedradv.spiders.auctions import AuctionsSpider


@pytest.fixture
def spider() -> AuctionsSpider:
    return AuctionsSpider()
