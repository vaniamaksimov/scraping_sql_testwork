from src.crud.base import CrudBase
from src.models.region import Region
from src.schemas.session import SessionCreate, SessionUpdate


class RegionCrud(CrudBase[Region, SessionCreate, SessionUpdate]):
    ...


session_crud = RegionCrud(Region)
