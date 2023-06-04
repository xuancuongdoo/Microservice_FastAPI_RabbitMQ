Microservice with 2 FastAPI Apps and RabbitMQ
This microservice consists of two FastAPI apps that communicate with each other through RabbitMQ. To get started, you can use Docker Compose to run the microservice:

docker-compose up -d
Directory Structure
redis_fast,
├─ .DS_Store,
├─ README.md,
└─ project,
   ├─ .env,
   ├─ __init__.py,
   ├─ build,
   │  └─ docker,
   │     ├─ Dockerfile.inventory,
   │     └─ Dockerfile.payment,
   ├─ docker-compose.yml,
   ├─ inventory,
   │  ├─ __pycache__,
   │  │  ├─ main.cpython-311.pyc,
   │  │  └─ main.cpython-39.pyc,
   │  ├─ consumer.py,
   │  └─ main.py,
   ├─ payment,
   │  ├─ __init__.py,
   │  ├─ __pycache__,
   │  │  ├─ consumer.cpython-311.pyc,
   │  │  ├─ consumer.cpython-39.pyc,
   │  │  ├─ db.cpython-311.pyc,
   │  │  ├─ db.cpython-39.pyc,
   │  │  ├─ main.cpython-311.pyc,
   │  │  └─ main.cpython-39.pyc,
   │  ├─ db.py,
   │  ├─ main.py,
   │  └─ sender.py,
   ├─ requirements.txt,
   └─ setup.py,
How to Run the Microservice
To run the microservice, you can use Docker Compose:

docker-compose up -d
This command will start the services defined in the docker-compose.yml file in detached mode, meaning that they will run in the background. You can then access the apps at the following URLs:

Inventory app: http://localhost:8000
Payment app: http://localhost:8002
Troubleshooting
If you encounter any issues while running the microservice, here are some troubleshooting tips:

Make sure you have Docker and Docker Compose installed on your machine.
Check that the ports defined in the docker-compose.yml file are not already in use by other applications on your machine.
If you're having trouble with RabbitMQ, try accessing the management GUI at http://localhost:15672 using the credentials guest and guest.
