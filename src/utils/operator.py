from enum import StrEnum


class Operator(StrEnum):
    EQUAL = 'eq'
    NOTEQUAL = 'neq'
    GREATER = 'ge'
    GREATEREQUAL = 'geq'
    LESS = 'le'
    LESSEQUAL = 'leq'
    LIKE = 'like'
    ILIKE = 'ilike'
    ISNULL = 'isnull'

    @classmethod
    def lst(cls) -> list[str]:
        return list(map(lambda key: key.value, cls))
