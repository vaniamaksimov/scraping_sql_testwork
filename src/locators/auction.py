from typing import assert_never

from attr import dataclass

from src.locators.base import BaseLocators
from src.models.auction_status import AuctionStatus
from src.utils.app_types import XPATH


@dataclass
class AuctionListLocators(BaseLocators):
    auctions_table: XPATH = '//tbody[@class="g-color-black-opacity-0_6"]/tr'
    row_auction_link: XPATH = './td[1]/a/@href'
    row_auction_area: XPATH = './td[2]/a/text()'
    row_auction_region: XPATH = './td[3]/a/text()'
    row_auction_status: XPATH = './td[4]/a/text()'
    current_page: XPATH = '//a[@class="safeparam u-pagination-v1__item u-pagination-v1-4 g-rounded-50 g-pa-7-14 u-pagination-v1-4--active"]/text()'
    next_page = (  # noqa:E731
        lambda current_page: f'//a[@class="safeparam u-pagination-v1__item u-pagination-v1-4 g-rounded-50 g-pa-7-14 "][contains(text(), {int(current_page)+1})]/@href'
    )


@dataclass
class AuctionPageLocators(BaseLocators):
    auction_fee: XPATH = '//dt[contains(text(),"Взнос за участие в аукционе")]/following-sibling::dd/text()'
    auction_holder: XPATH = (
        '//dt[contains(text(),"Организатор")]/following-sibling::dd/text()'
    )

    @staticmethod
    def auction_deadline_text(auction_status: AuctionStatus) -> XPATH:
        match auction_status:
            case AuctionStatus.OPEN:
                return '//dt[contains(text(),"Срок подачи заявок")]/following-sibling::dd/text()'
            case AuctionStatus.CLOSED:
                return '//dt[contains(text(),"Приказ об утверждении")]/following-sibling::dd/text()'
            case (
                AuctionStatus.VOIDED
                | AuctionStatus.CANCELED
                | AuctionStatus.TRANSFER
                | AuctionStatus.SUSPENDED
                | AuctionStatus.NO_DATA
            ):
                return '//dt[contains(text(),"Приказ об отмене (переносе, аннулировании)")]/following-sibling::dd/text()'
            case None:
                raise ValueError
            case _ as unreachable:
                assert_never(unreachable)

    @staticmethod
    def auction_date(auction_status: AuctionStatus) -> XPATH:
        match auction_status:
            case AuctionStatus.OPEN:
                return '//dt[contains(text(),"Место и время проведения")]/following-sibling::dd/text()'
            case (
                AuctionStatus.VOIDED
                | AuctionStatus.CLOSED
                | AuctionStatus.CANCELED
                | AuctionStatus.TRANSFER
                | AuctionStatus.SUSPENDED
                | AuctionStatus.NO_DATA
            ):
                return '//h1/text()[string-length() > 1]'
            case None:
                raise ValueError
            case _ as unreachable:
                assert_never(unreachable)
