from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)


redis = get_redis_connection(

    host='redis-13694.c277.us-east-1-3.ec2.cloud.redislabs.com',
    port=13694,
    password="h0pkVuxecvuPVIflGmfI1VglVATZi99B",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity,
    }


@app.get('/products/{pk}')
async def get(pk: str):
    return Product.get(pk=pk)


@app.post('/products')
def create(product: Product):
    return product.save()


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
