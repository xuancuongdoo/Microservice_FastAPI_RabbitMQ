import pika
from fastapi import FastAPI
import json

app = FastAPI()

rabbitmq_host = 'rabbitmq'
rabbitmq_port = 5672
rabbitmq_user = 'myuser'
rabbitmq_password = 'mypassword'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    )
)
channel = connection.channel()

channel.queue_declare(queue='order_complete')


def send_order_complete_message(order_id: str, quantity: int):
    routing_key = 'order_complete'
    message = {'order_id': order_id, 'order_quantity': quantity}
    channel.basic_publish(
        exchange='', routing_key=routing_key, body=json.dumps(message))
    print(f"[x] Sent message to queue '{routing_key}': {message}")
