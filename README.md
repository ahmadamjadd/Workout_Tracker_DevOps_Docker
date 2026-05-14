# Workout Tracker - DevOps

A full-stack workout logging app built for DevOps coursework. The project lets a user add workout entries and view workout history through a React frontend backed by a FastAPI API and SQLAlchemy ORM.

## Overview

The application is split into three layers:

- Frontend: React with Vite and Axios
- Backend: Python FastAPI with SQLAlchemy
- Database: PostgreSQL in Docker, with SQLite used for automated tests

The UI is a single-page workout tracker that supports logging exercises, sets, reps, and weight, then displays the saved history in a table.

## Features

- Add a new workout entry from the browser
- View workout history in a table
- FastAPI REST endpoints for creating and reading workouts
- Docker-based deployment flow for backend, frontend, and database
- Automated backend and frontend testing through GitHub Actions

## Project Structure

```text
WorkoutApp_Docker/
├── compose.yml
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── test_main.py
└── frontend/
	├── Dockerfile
	├── package.json
	└── src/
		├── App.jsx
		├── App.css
		├── index.css
		└── main.jsx
```

## How It Works

The backend exposes two endpoints:

- `POST /workouts/` creates a workout record
- `GET /workouts/` returns the stored workout list

The frontend reads the API URL from `VITE_API_URL`. If that variable is not set, it falls back to `http://127.0.0.1:8000/workouts/` for local development.

## Requirements

- Python 3.12 or compatible Python 3 environment
- Node.js 22 or newer
- PostgreSQL for local backend development, or Docker for the full stack setup
- Docker and Docker Compose for containerized deployment

## Local Development

### Backend

Install dependencies and run the API:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

By default, the backend looks for PostgreSQL using these environment variables:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_DB`
- `DATABASE_URL`

If you want to use SQLite for ad hoc experimentation, set `DATABASE_URL` before starting the app.

### Frontend

Install dependencies and start the Vite dev server:

```bash
cd frontend
npm install
npm run dev
```

If the backend is running somewhere else, point the frontend at it with:

```bash
VITE_API_URL=http://your-backend-host:8000/workouts/
```

## Docker Deployment

The project includes a Compose setup for the testing/deployment environment:

- PostgreSQL runs as the database service
- The backend container serves the FastAPI app on port `8001`
- The frontend container serves the built React app on port `8080`

The `compose.yml` file used here is wired to the image flow used in CI/CD, so it is mainly intended for the deployment environment rather than a local build-from-source workflow.

## Testing

### Backend Tests

The backend tests use SQLite so they do not depend on PostgreSQL during test execution.

```bash
cd backend
pytest test_main.py
```

### Frontend Tests and Linting

```bash
cd frontend
npm run lint
npm run test
```

## CI/CD Workflow

The repository includes a GitHub Actions workflow that:

1. Lints and tests the backend
2. Lints and tests the frontend
3. Builds and pushes Docker images
4. Deploys the updated containers to the testing EC2 instance
5. Sends email notifications on success or failure

## API Summary

| Method | Route | Description |
| --- | --- | --- |
| GET | `/workouts/` | Fetch all saved workout records |
| POST | `/workouts/` | Create a new workout record |

## Notes

- Backend startup creates the database tables automatically.
- The frontend uses a simple glassmorphism-inspired interface with responsive layout and animation.
- Automated tests are designed to keep the SQLite test path separate from the PostgreSQL deployment path.

## License

This project was created for academic coursework. Add a license here if you plan to publish or reuse it publicly.
