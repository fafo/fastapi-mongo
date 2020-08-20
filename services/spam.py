from models.base import SpamItem
from services.crud import CRUDBase


class CRUDSpam(CRUDBase[SpamItem]):
    pass


crudspam = CRUDSpam(SpamItem, "spam")