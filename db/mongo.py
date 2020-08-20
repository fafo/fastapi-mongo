from motor import motor_asyncio
from settings import settings


_client = motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_URI, uuidRepresentation="standard"
)

def get_db(db_name) -> motor_asyncio.AsyncIOMotorDatabase:
    return _client[db_name]
