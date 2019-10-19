from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel
import logging

logging.basicConfig(
    level=1,
    format="%(asctime)-15s %(levelname)-8s %(message)s",
    filename='test.log'
)
app = FastAPI()

class Item(BaseModel):
    #request_ID: str
    #description: str = None
    item_list: List[str]


@app.get("/")
def read_root():
    return {"Prediction API": "Welcome!"}


@app.post("/predict_next")
async def read_item(items:Item): #List[int] = Query(None,description="LIst of item ids as used in training")):
    '''
    Predict the next item. Dummy function to return the last element
    :param items: list of items encoded as item ids
    :return:
    '''
    print(items)
    items_str = ','.join(items.item_list)
    logging.debug("received items: "+items_str)
    await log_session(items_str)
    return {"next_item": items.item_list[-1]}

async def log_session(items):
    logging.debug("save to sessions_items.log")
    f = open("session_items.log","a")
    f.write(items+'\n')
    f.close()