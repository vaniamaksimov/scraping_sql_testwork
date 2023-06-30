import enum


@enum.unique
class AuctionStatus(enum.StrEnum):
    VOIDED = 'Аннулирован'
    CLOSED = 'Закрыт'
    OPEN = 'Открыт'
    CANCELED = 'Отмена'
    TRANSFER = 'Перенос'
    SUSPENDED = 'Приостановлен'
    NO_DATA = 'нет сведений'
