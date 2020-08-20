from typing import Optional, TypeVar, Type, Generic, List, Union
from models.base import Pageable
from settings import settings
from db.mongo import get_db
from bson import ObjectId

ModelType = TypeVar("ModelType")


def sort_spec(field, dir):
    if field is not None:
        return [(field, dir)]
    else:
        return None


def ID(id: Union[str, ObjectId]) -> Union[str, ObjectId]:
    """ casting to ObjectId when possible, otherwise using string """
    return ObjectId(id) if ObjectId.is_valid(id) else id


class CRUDBase(Generic[ModelType]):

    def __init__(
            self, model: Type[ModelType], coll: str, db=settings.APP_DB):
        self._model = model
        self._db = db
        self._coll = get_db(self._db)[coll]

    async def create(self, obj: ModelType) -> Union[str, ObjectId]:
        doc = obj.to_mongo()
        return (await self._coll.insert_one(doc)).inserted_id

    async def read(self, id: str) -> Optional[ModelType]:
        id = ID(id)
        doc = await self._coll.find_one({"_id": id})
        return doc and self._model(**doc)

    def read_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            sort_by: str = None,
            direction: int = 1,
            raw: bool = False) -> List[Union[ModelType, dict]]:
        return self.search_multi(
            skip=skip, limit=limit, sort_by=sort_by, direction=direction,
            raw=raw)

    async def search_multi(
            self,
            spec: dict = {},
            skip: int = 0,
            limit: int = 100,
            sort_by: str = None,
            direction: int = 1,
            raw: bool = False) -> List[Union[ModelType, dict]]:

        cur = self._coll.find(
            spec, skip=skip, limit=limit, sort=sort_spec(sort_by, dir))
        docs = await cur.to_list(length=None)  # use limit in find()

        return docs if raw else list(map(lambda x: self._model(**x), docs))
    
    async def update(self, obj: ModelType) -> bool:
        id = ID(obj.id)
        res = await self._coll.replace_one({"_id": id}, obj.to_mongo())
        return res.acknowledged

    async def delete(self, id: str) -> bool:
        id = ID(id)
        return (await self._coll.delete_one({"_id": id})).acknowledged

    async def count(self) -> int:
        return (await self._coll.count_documents({}))

    async def read_page(
            self,
            skip: int = 0,
            limit: int = 100,
            sort_by: str = None,
            direction: int = 1) -> Pageable[ModelType]:
        
        docs = await self._coll.find(
            skip=skip, limit=limit, sort=sort_spec(sort_by, direction)
        ).to_list(None)
        
        data = list(map(lambda x: self._model(**x), docs))
    
        return Pageable[ModelType](count=await self.count(), data=data)
