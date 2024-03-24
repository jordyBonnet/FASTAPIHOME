from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every
from pushbullet_functions import PushbulletFunctions

database_uri = f"sqlite:///./test.db?check_same_thread=False"
sessionmaker = FastAPISessionMaker(database_uri)

app = FastAPI()

pb = PushbulletFunctions()

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None
#     date: 

@app.get("/")
def read_root():
    return {"msg": "FASTAPIHOME"}

# @repeat_every(seconds=60 * 60)  # 1 hour
# def remove_expired_tokens_task() -> None:
#     with sessionmaker.context_session() as db:
#         remove_expired_tokens(db=db)

@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # in seconds (60sec * 60min * 24h = 1 day)
def glass_trash_day_notifiction():
    """ scheduled (day by day) notification for glass trash day"""
    with sessionmaker.context_session() as db:
        pb.send_notification_by_pushbullet(db=db)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}