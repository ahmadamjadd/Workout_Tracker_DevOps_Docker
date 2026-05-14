# Workout Tracker - DevOps

This project is a containerized workout logging app built for DevOps coursework. A React frontend lets users add workout entries and view workout history, a FastAPI backend stores and serves workout data, and PostgreSQL runs as the persistent database in the deployed environments.

## Overview

The project is split into three runtime layers:

- Frontend: React + Vite + Axios
- Backend: Python + FastAPI + SQLAlchemy
- Database: PostgreSQL in Docker, SQLite for automated backend tests

The application flow is simple:

1. The user submits a workout in the browser.
2. The frontend sends the request to the FastAPI API.
3. The backend writes the workout to the database.
4. The frontend fetches the updated workout list and displays it.

## What Runs Where

- Local development: frontend and backend can run from source, with the backend pointed at a local database or SQLite for testing.
- Testing environment: GitHub Actions runs linting and unit tests, then deploys the tested images to the testing EC2 instance.
- Staging environment: GitHub Actions builds and deploys the staging images to the staging EC2 instance when code is pushed to `main` or when the workflow is run manually.

## Application Components

- Frontend source: [frontend/src/App.jsx](frontend/src/App.jsx)
- Frontend styling: [frontend/src/App.css](frontend/src/App.css)
- Backend API: [backend/main.py](backend/main.py)
- Backend tests: [backend/test_main.py](backend/test_main.py)
- Docker Compose deployment: [compose.yml](compose.yml)

## API Behavior

The backend exposes two routes:

- `GET /workouts/` returns all saved workout records.
- `POST /workouts/` creates a new workout record.

The frontend reads the API URL from `VITE_API_URL`. If the variable is not set, it falls back to `http://127.0.0.1:8000/workouts/` for local use.

## CI/CD Architecture

This repository uses two GitHub Actions workflows:

- Testing workflow: runs on pull requests to `main` and can also be triggered manually.
- Staging workflow: runs on push to `main` and can also be triggered manually.

### Testing Workflow Flow

The testing workflow is defined in [TestingEnvWorkflow.yml](.github/workflows/TestingEnvWorkflow.yml).

1. A pull request to `main` starts the workflow, or a developer can trigger it manually with `workflow_dispatch`.
2. GitHub Actions checks out the repository.
3. The backend job starts a PostgreSQL service container inside the GitHub runner.
4. The backend dependencies are installed.
5. Backend linting runs with `flake8`.
6. Backend unit tests run with `pytest`.
7. The frontend job sets up Node.js 22.
8. Frontend dependencies are installed.
9. Frontend linting runs with `npm run lint`.
10. Frontend tests run with `npm run test`.
11. If any check fails, the failure notification job sends an email and stops before deployment.
12. If all checks pass, GitHub Actions configures AWS credentials.
13. GitHub Actions logs in to Amazon ECR.
14. Docker images are built and tagged for the testing environment.
15. The backend image is pushed to ECR as the testing tag.
16. The frontend image is built with `VITE_API_URL` pointing to the testing EC2 public IP and then pushed to ECR.
17. GitHub Actions connects to the testing EC2 instance over SSH.
18. The EC2 instance runs `docker compose pull` and `docker compose up -d` to fetch the latest images from ECR and restart the containers.
19. Old images are pruned and system logs are trimmed.
20. A success or failure email is sent after deployment.

### Staging Workflow Flow

The staging workflow is defined in [StagingEnvWorkflow.yml](.github/workflows/StagingEnvWorkflow.yml).

1. A push to `main` starts the workflow, or a developer can trigger it manually with `workflow_dispatch`.
2. GitHub Actions checks out the repository.
3. AWS credentials are configured.
4. GitHub Actions logs in to Amazon ECR.
5. Docker images are built for the staging environment.
6. The frontend image is built with `VITE_API_URL` pointing to the staging EC2 public IP.
7. The backend and frontend staging images are pushed to ECR.
8. GitHub Actions connects to the staging EC2 instance over SSH.
9. The staging server runs `docker compose pull` and `docker compose up -d`.
10. The workflow verifies that the app is reachable and writes the staging URL to the workflow summary.

## AWS Flow

### Amazon ECR

ECR stores the versioned Docker images for each environment.

- `workout-backend:testing`
- `workout-frontend:testing`
- `workout-backend:staging`
- `workout-frontend:staging`

The GitHub Actions runners build the images and push them to ECR. The EC2 instances do not rebuild the app from source; they pull the approved images from ECR and run them.

### EC2 Instances

There are separate EC2 instances for testing and staging.

- The testing EC2 instance runs the deployment that is validated by QA after pull requests.
- The staging EC2 instance runs the post-merge deployment from `main`.
- Both instances use Docker Compose to run the multi-container stack.

### Docker Compose on EC2

The deployed stack contains three containers:

- PostgreSQL database container
- FastAPI backend container
- React frontend container served by Apache

The backend container uses the database service name as the host, so the API can connect to PostgreSQL inside the Compose network.

## Local Development

### Backend

Install dependencies and run the API:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend reads these environment variables for PostgreSQL:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_DB`
- `DATABASE_URL`

### Frontend

Install dependencies and start the Vite dev server:

```bash
cd frontend
npm install
npm run dev
```

If the backend is not running on the default local address, set `VITE_API_URL` before starting the frontend.

## Testing

### Backend Tests

The backend tests use SQLite so they stay isolated from PostgreSQL during CI.

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

## Notes

- Backend startup creates database tables automatically.
- The frontend UI is responsive and uses the app styling already present in the source.
- The GitHub Actions workflows are the source of truth for how testing and staging deployments happen.

## License

This project was created for academic coursework. Add a license if you plan to publish or reuse it publicly.
