from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app1 = FastAPI()


class Item(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=50)
    price: float = Field(gt=0)
    in_stock: bool
    

Items: list[Item] = []


@app1.get("/items")
def get_items():
    return Items


@app1.get("/items/{item_id}")
def get_item(item_id: UUID):
    for item in Items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app1.post("/items")
def create_item(item: Item):
    Items.append(item)
    return {"created": item}


@app1.put("/items/{item_id}")
def update_item(item_id: UUID, new_item: Item):
    for index, item in enumerate(Items):
        if item.id == item_id:
            Items[index] = new_item
            return {"updated": new_item}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app1.patch("/items/{item_id}")
def patch_item(item_id: UUID, name: str | None = None, price: float | None = None, in_stock: bool | None = None):
    for index, item in enumerate(Items):
        if item.id == item_id:
            if name is not None:
                item.name = name
            if price is not None:
                item.price = price
            if in_stock is not None:
                item.in_stock = in_stock
            Items[index] = item
            return {"patched": item}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")


@app1.delete("/items/{item_id}")
def delete_item(item_id: UUID):
    for index, item in enumerate(Items):
        if item.id == item_id:
            deleted = Items.pop(index)
            return {"deleted": deleted}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

