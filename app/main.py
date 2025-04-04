from fastapi import FastAPI
from app.api import menu, category, item, item_offer, order

app = FastAPI(title="iHungry Open Delivery API")

for router, prefix, tag in [
    (menu.router, "/menu", "Menu"),
    (category.router, "/category", "Category"),
    (item.router, "/item", "Item"),
    (item_offer.router, "/item-offer", "ItemOffer"),
    (order.router, "/order", "Order"),
]:
    app.include_router(router, prefix=prefix, tags=[tag])


@app.get("/")
def root():
    return {"message": "Welcome to the iHungry Open Delivery API!"}
