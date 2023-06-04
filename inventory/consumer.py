import pika
from fastapi import FastAPI
import json
from main import Product

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
dchannel.queue_declare(queue='order_complete')
channel.queue_bind(queue='order_complete', exchange='my_exchange', routing_key='order_complete')


def process_order_complete_message(channel, method, properties, body):
    message = json.loads(body)
    order_id = message['order_id']
    order_quantity = message['order_quantity']

    # Perform the quantity deduction logic
    product_id = order_id  # Replace with the actual product ID associated with the order
    product = Product.get(product_id)
    if product:
        if product.quantity < order_quantity:
            print(f"Insufficient quantity in inventory for order: {order_id}")
        else:
            product.quantity -= order_quantity
            product.save()
            print(f"Deducted quantity from inventory for order: {order_id}")
    else:
        print(f"Product not found for order: {order_id}")


# Start consuming messages from the queue
channel.basic_consume(queue='order_complete', on_message_callback=process_order_complete_message)

# Run the consumer indefinitely
channel.start_consuming()