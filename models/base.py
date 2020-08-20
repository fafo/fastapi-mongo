from pydantic import BaseModel, Field, ValidationError
from pydantic.generics import GenericModel
from typing import Optional, TypeVar, List, Generic
from datetime import datetime
import json

from bson import ObjectId


class ObjectIdStr(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        return ObjectId(v) if ObjectId.is_valid(v) else v


class ObjectIdStrict(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if ObjectId.is_valid(v):
            return ObjectId(v)
        else:
            raise ValidationError()


class ConfigTemplate:
    allow_population_by_field_name = True
    json_encoders = {ObjectId: lambda x: str(x)}


class MongoModel(BaseModel):

    Config = ConfigTemplate

    id: Optional[ObjectIdStr] = Field(None, alias="_id")

    def to_mongo(self):
        doc = self.dict(by_alias=True)
        if doc["_id"] is None:
            del doc["_id"]
        return doc


T = TypeVar("T")


class Pageable(GenericModel, Generic[T]):
    count: int
    data: List[T]

    Config = ConfigTemplate


class SpamItemCreate(BaseModel):
    name: str = Field(..., title="test field")
    date: datetime = Field(default_factory=datetime.now)


class SpamItem(SpamItemCreate, MongoModel):
    pass


if __name__ == "__main__":
    # example

    item = SpamItem(id=ObjectId(), name="Ciao")
    print(item)
    print("1 dict:", item.dict(by_alias=True))
    print("1 json:", item.json())
    print("1 mongo:", item.to_mongo())
    print("1 parse:", SpamItem(**json.loads(item.json())).dict(by_alias=True))

    item2 = SpamItem(name="Ciao 2", date=datetime.now())
    print("2 mongo:", item2.to_mongo())
    
