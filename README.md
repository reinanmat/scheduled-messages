# Scheduled Messages Application

This project is a distributed application for scheduling and managing messages. It consists of a FastAPI backend, a Next.js frontend, and a scheduler component, leveraging Dapr for building resilient, microservices-based applications.

## Features

- **Message Scheduling**: Schedule messages to be sent at a future date and time.
- **API**: A RESTful API for managing messages.
- **Web Interface**: A user-friendly web application for interacting with the system.
- **Distributed Architecture**: Utilizes Dapr for state management, pub/sub messaging, and actor model for scheduling.

## Technologies Used

- **Backend (API & Scheduler)**:
  - Python 3.10+
  - FastAPI: Web framework for the API.
  - SQLAlchemy: ORM for database interactions.
  - Alembic: Database migrations.
  - Dapr Python SDK: Integration with Dapr building blocks.
- **Frontend (Web)**:
  - Next.js: React framework for the web application.
  - React: JavaScript library for building user interfaces.
  - Tailwind CSS: Utility-first CSS framework for styling.
  - Radix UI: Headless UI components.
- **Database**:
  - PostgreSQL
- **Distributed Application Runtime**:
  - Dapr
- **Containerization**:
  - Docker & Docker Compose

## Prerequisites

Before running this project, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/): For running PostgreSQL and Dapr components.
- [Python 3.10+](https://www.python.org/downloads/):
- [Node.js](https://nodejs.org/en/download/) (LTS recommended) & [npm](https://www.npmjs.com/) (or [pnpm](https://pnpm.io/))
- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)
- [Dapr Runtime](https://docs.dapr.io/getting-started/install-dapr-selfhost/)
    *Ensure Dapr is initialized and running (e.g., `dapr init`).*

## Configuration and Execution

**Note**: The current setup process involves several manual steps across different components. While functional, it might seem a bit involved. The long-term goal is to streamline this process, allowing the entire application stack to be brought up with a single `docker compose up` command. This is a work in progress.


### 1. Environment Variables

Copy the `.env.example` file to `.env` in the project root and fill in the necessary details for your PostgreSQL database.

```bash
cp .env.example .env
```

### 2. Running with Docker Compose (PostgreSQL)

Start the PostgreSQL database using Docker Compose. This will also create the necessary Docker network.

```bash
docker compose up -d postgres
```

### 3. Database Migrations

Apply the database migrations using Alembic to set up the necessary tables.

```bash
# Ensure you are in the project root directory
# First, install python dependencies
uv pip install -e .
alembic upgrade head
```

### 4. Running Dapr Components and Applications

From the project root directory, run all Dapr applications and components defined in `dapr.yaml` and `components/`.

```bash
dapr run -f .
```

This command will start the `api` and `scheduler` applications with their respective Dapr sidecars, and also load the `pubsub-messages.yaml` and `statestore.yaml` components.

Alternatively, you can run each service individually in separate terminals. The commands are defined in `dapr.yaml`:

**For the API:**
```bash
dapr run --app-id api --app-port 8000 -- uvicorn api.app:app --port 8000
```

**For the Scheduler:**
```bash
dapr run --app-id scheduler --app-port 8001 -- uvicorn scheduler.app:app --port 8001
```

### 5. Running the Frontend (Web)

Navigate to the `web` directory and start the Next.js development server.

```bash
cd web
pnpm install # or npm install / yarn install
pnpm dev # or npm run dev / yarn dev
```

The web application will be accessible at `http://localhost:3000`.

## Project Structure

- `api/`: Contains the FastAPI backend application, including database models, schemas, and API endpoints.
- `web/`: Contains the Next.js frontend application.
- `scheduler/`: Contains the Dapr actor-based scheduler component responsible for processing scheduled messages.
- `common/`: Shared utilities, Dapr client, logging, and common schemas.
- `components/`: Dapr component YAML definitions (pubsub, statestore).
- `migrations/`: Alembic migration scripts for the database.
- `docker-compose.yaml`: Defines Docker services for PostgreSQL and Dapr components.
