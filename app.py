import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)


@app.get("/store")
def get_stores():
   return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
   store_data = request.get_json()
   if "name" not in store_data:
      abort(400, message="Bad request. Ensure 'name' is included in your JSON payload")
   for store in stores:
      if store_data["name"] == stores.keys():
         abort(400, message =f"Store already exists")
   store_id = uuid.uuid4().hex
   store = {**store_data, "id": store_id}
   stores[store_id] = store
   return store, 201

@app.post("/item")
def create_item():
   item_data = request.get_json()
   if(
      "price" not in item_data
      or "store_id" not in item_data
      or "name" not in item_data
   ):
      abort(
         400,
         message = "Bad request. Ensure 'price', 'store_id, and 'name' are included in your JSON payload"
      )
   for item in items.values():
      if(
         item_data["name"] == item["name"]
         and item_data["store_id"] == item["store_id"]
      ):
         abort(400, message = f"Item already exists.")
   
   if item_data["store_id"] not in stores:
      abort(404, message="Store not found")
      
   item_id = uuid.uuid4().hex
   item = {**item_data, "item_id": item_id}
   items[item_id] = item
   
   return item, 201

@app.get("/items")
def get_items():
   return {"items": items}

@app.get("/items/<int:id>")
def get_items_by_id(id):
   try: 
      return items[id]
   except KeyError:
      abort(404, message="Item not found" )


@app.post("/store_select")
def get_items2():
   request_data = request.get_json()
   for store in stores:
      if request_data["name"] == store["name"]:
         return store["items"]
      
@app.get("/store/<string:store_id>")
def get_store(store_id):
   try:  
      return stores[store_id]
   except KeyError:
      abort(404, message="Store not found")
      
@app.delete("/del_item/<string:item_id>")
def del_item(item_id):
   try:
      del items[item_id]
      return {"message": "Item deleted"}
   except KeyError:
      abort(404, message="Item not found")
      
@app.delete("/del_store/<string:store_id>")
def del_store(store_id):
   try:
      del stores[store_id]
      return {"message": "Store deleted"}
   except KeyError:
      abort(404, message="Store not found")
         
@app.put("/update_item/<string:item_id>")
def update_item(item_id):
   item_data = request.get_json()
   if "price" not in item_data and "name" not in item_data:
      abort(400, message="Ensure 'name' and 'price' are included in your JSON payload")
     
   try: 
      item = items[item_id]
      item |= item_data
      
      return item
   except KeyError:
      abort(404, message="Item not found")