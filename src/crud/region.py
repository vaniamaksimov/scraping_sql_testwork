from src.crud.base import CrudBase
from src.models.region import Region
from src.schemas.region import RegionCreate, RegionUpdate


class RegionCrud(CrudBase[Region, RegionCreate, RegionUpdate]):
    ...


region_crud = RegionCrud(Region)
