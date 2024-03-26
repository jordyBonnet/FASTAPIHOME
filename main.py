"""
Main FASTAPI app

uvicorn main:app --reload
"""

from fastapi import FastAPI
import daily_sports_events as dse
import glass_trash_day as gtd
# from pydantic import BaseModel
# from typing import Union

## section used for the scheduled function with FAST API utils 
# from fastapi_utils.session import FastAPISessionMaker
# from fastapi_utils.tasks import repeat_every
# database_uri = f"sqlite:///./test.db?check_same_thread=False"
# sessionmaker = FastAPISessionMaker(database_uri)

app = FastAPI()

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None
#     date: 

@app.get("/")
def read_root():
    return {"msg": "FASTAPIHOME"}

@app.get("/daily_sports_events")
def daily_sports_events():
    """
    send daily sports events via pushbullet to the user as a notification
    """
    dse.main()
    return {"message": 'daily sports events sent via pushbullet'}

@app.get("/glass_trash_day")
def glass_trash_day():
    """
    send pushbullet notification evening before glass trash day
    """
    gtd.main()
    return {"message": 'glass trash day sent via pushbullet'}


# # scheduled function from FAST API utils (no arguments allowed)
# @app.on_event("startup")
# @repeat_every(seconds=60 * 60 * 24)  # in seconds (60sec * 60min * 24h = 1 day)
# def glass_trash_day_notifiction():
#     """ scheduled (day by day) notification for glass trash day"""
#     with sessionmaker.context_session() as db:
#         pb.send_notification_by_pushbullet(db=db)

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}