import pytest

from src.locators.auction import AuctionListLocators, AuctionPageLocators
from src.models.status import AuctionStatus
from src.utils.app_types import Xpath


@pytest.mark.parametrize(
    argnames=['auction_status', 'expected_xpath'],
    argvalues=[
        (
            AuctionStatus.OPEN,
            '//dt[contains(text(),"Место и время проведения")]'
            '/following-sibling::dd/text()',
        ),
        (AuctionStatus.VOIDED, '//h1/text()[string-length() > 1]'),
        (AuctionStatus.CLOSED, '//h1/text()[string-length() > 1]'),
        (AuctionStatus.CANCELED, '//h1/text()[string-length() > 1]'),
        (AuctionStatus.TRANSFER, '//h1/text()[string-length() > 1]'),
        (AuctionStatus.SUSPENDED, '//h1/text()[string-length() > 1]'),
        (AuctionStatus.NO_DATA, '//h1/text()[string-length() > 1]'),
    ],
)
def test_auction_page_locators_auction_date(
    auction_status: AuctionStatus, expected_xpath: Xpath
):
    xpath = AuctionPageLocators.auction_date(auction_status)
    assert xpath == expected_xpath


def test_auction_list_locators_next_page():
    xpath = AuctionListLocators.next_page('1')
    assert (
        xpath == '//a[@class="safeparam u-pagination-v1__item u-pagination-v1-4'
        ' g-rounded-50 g-pa-7-14 "][contains(text(), 2)]/@href'
    )
