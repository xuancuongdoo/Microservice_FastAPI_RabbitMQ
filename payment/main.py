from fastapi import FastAPI,  BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from db import *
from fastapi import Depends, Request
from typing import List
import requests
from pydantic import BaseModel
from fastapi import HTTPException

import time
from sender import send_order_complete_message
import httpx
from httpx import ConnectError
import asyncio
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)


class OrderCreate(BaseModel):
    product_id: str
    quantity: int


class OrderOut(BaseModel):
    id: str
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Config:
        orm_mode = True


@app.get("/orders/")
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


@app.get("/orders/{pk}")
async def retrieve_order(pk: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == pk).first()
    return order


@app.post("/orders/")
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_async_db)):
    product_id = order.product_id
    order_quantity = order.quantity
    res = requests.get(f"http://fastapi_inventory:8000/products/{product_id}")

    if res.status_code == 200 and res.headers["content-type"].strip().startswith("application/json"):
        data = res.json()
        product_data = jsonable_encoder(data)

        if not product_data:
            return JSONResponse(status_code=404, content={"detail": "Product not found"})

        if (product_data['quantity'] <= 0) and (product_data['quantity'] - order_quantity) <= 0:
            return JSONResponse(status_code=404, content={"detail": "Not in stock"})

        fee = product_data['price'] * 0.5
        total = fee + product_data['price']

        new_order = Order(
            id='OrderNo{}'.format(product_id),
            product_id=product_id,
            price=product_data['price'],
            fee=fee,
            total=total,
            quantity=order_quantity,
            status='pending',
        )
        await order_complete(new_order, db)
        async with db.begin():
            db.add(new_order)
            db.flush()

        return new_order

    return JSONResponse(status_code=404, content={"detail": "Product not found"})


async def order_complete(order: Order, db: Session):
    if order.quantity > 0:
        order.status = 'complete'

    # send_order_complete_message(order.id, order.quantity)


