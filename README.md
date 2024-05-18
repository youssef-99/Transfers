# Transfers

## Setup

### Prerequisites

- **Docker**: Ensure Docker is installed on your system.
- **Docker Compose**: Ensure Docker Compose is installed on your system.
- **Git**: Ensure Git is installed for version control.

### Clone the Repository

```bash
git clone git@github.com:youssef-99/Transfers.git
cd Transfers
```

## Environment Variables
Create a .env file in the ./app/app/ directory with the following content:

```env
DEBUG=true
SECRET_KEY=changeme
ALLOWED_HOSTS=127.0.0.1,0.0.0,localhost
```

## Build and Run the Application
Build the Docker containers

```bash
docker-compose build
```

Run the containers:
```bash
docker-compose up -d
```
