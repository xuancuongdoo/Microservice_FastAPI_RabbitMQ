# Microservice with FastAPI Apps

This is a microservice consisting of two FastAPI apps that communicate with each other through RabbitMQ. The services can be started using Docker Compose.

## Prerequisites

Make sure you have the following installed on your system:
- Docker
- Docker Compose

#1. Clone this repository to your local machine:

```bash
git clone <repository-url>
cd <project-directory>
docker-compose up -d
```

This command will start the FastAPI apps, the RabbitMQ message broker, and any other required services defined in the docker-compose.yml file. The services will run in detached mode (-d flag), allowing them to run in the background.

Verify that the microservice is running.
Open your web browser and visit the following URLs:

App 1: http://localhost:8000
App 2: http://localhost:8002

##Please let me know if there's anything else I can assist you with!



