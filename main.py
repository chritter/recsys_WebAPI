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

recommend_num_items = 3

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

    # get recommended item...., then its url
    recommended_item_urls = items.item_list #[items.item_list[-1]]*recommend_num_items

    # write results to log file
    await log_session(items_str,recommended_item_urls)
    return {"next_item": recommended_item_urls}

async def log_session(items,recommended_item_urls):
    logging.debug("save to sessions_items.log")

    items_str_recom = ','.join(recommended_item_urls)
    f = open("session_items.log","a")
    # last urls written out into log file are the recommended items
    f.write(items+','+items_str_recom+'\n')
    f.close()