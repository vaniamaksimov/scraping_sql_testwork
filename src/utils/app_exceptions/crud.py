from typing import Protocol


class MessageMixin(Protocol):
    message: str


class BaseCrudError(MessageMixin, Exception):
    ...


class InvalidAttrNameError(BaseCrudError):
    ...


class InvalidOperatorError(BaseCrudError):
    def __init__(self, operator: str, *args: object) -> None:
        self.message = f'Недопустимый оператор {operator}'
