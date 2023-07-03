from typing import TypeAlias, TypeVar

from pydantic import BaseModel

from src.core.database import Base

Xpath: TypeAlias = str
ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
