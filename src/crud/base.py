from typing import Generic, assert_never

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.app_exceptions.crud import InvalidAttrNameError, InvalidOperatorError
from src.utils.app_types import CreateSchemaType, ModelType, UpdateSchemaType
from src.utils.operator import Operator


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType) -> None:
        self.model = model

    async def get(self, session: AsyncSession, **kwargs) -> ModelType:
        statement = self._make_statement(**kwargs)
        database_object = await session.execute(statement)
        return database_object.scalars().first()

    async def create(self, session: AsyncSession, schema: CreateSchemaType) -> ModelType:
        database_object = self.model(**schema.dict())
        session.add(database_object)
        await session.commit()
        await session.flush(database_object)
        return database_object

    async def update(
        self,
        session: AsyncSession,
        database_object: ModelType,
        schema: UpdateSchemaType,
    ) -> ModelType:
        object_data = {
            col.name: getattr(database_object, col.name)
            for col in database_object.__table__.columns
        }
        update_data = schema.dict(exclude_unset=True)
        for field_data_name in object_data:
            if field_data_name in update_data:
                setattr(
                    database_object, field_data_name, update_data.get(field_data_name)
                )
        session.add(database_object)
        await session.commit()
        await session.flush(database_object)
        return database_object

    async def remove(self, session: AsyncSession, database_object: ModelType):
        await session.delete(database_object)
        return database_object

    def _make_statement(self, **kwargs):
        stmt = select(self.model)
        for collumn_name, value in kwargs.items():
            operator = None
            if '__' in collumn_name:
                collumn_name, operator = collumn_name.split('__')
                if operator not in Operator.lst():
                    raise InvalidOperatorError(operator)
            if collumn_name not in self.model.__table__.columns:
                raise InvalidAttrNameError(collumn_name, self.model)
            match operator:
                case Operator.EQUAL:
                    stmt = stmt.where(getattr(self.model, collumn_name) == value)
                case Operator.NOTEQUAL:
                    stmt = stmt.where(getattr(self.model, collumn_name) != value)
                case Operator.GREATER:
                    stmt = stmt.where(getattr(self.model, collumn_name) > value)
                case Operator.GREATEREQUAL:
                    stmt = stmt.where(getattr(self.model, collumn_name) >= value)
                case Operator.LESS:
                    stmt = stmt.where(getattr(self.model, collumn_name) < value)
                case Operator.LESSEQUAL:
                    stmt = stmt.where(getattr(self.model, collumn_name) <= value)
                case Operator.LIKE:
                    stmt = stmt.where(
                        getattr(self.model, collumn_name).like(f'%{value}%')
                    )
                case Operator.ILIKE:
                    stmt = stmt.where(
                        getattr(self.model, collumn_name).ilike(f'%{value}%')
                    )
                case Operator.ISNULL:
                    if value:
                        stmt = stmt.where(getattr(self.model, collumn_name) is None)
                    else:
                        stmt = stmt.where(getattr(self.model, collumn_name) is not None)
                case None:
                    stmt = stmt.where(getattr(self.model, collumn_name) == value)
                case _ as unreachable:
                    assert_never(unreachable)
        return stmt
