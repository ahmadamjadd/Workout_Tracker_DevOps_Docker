from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import datetime
import os

# --- Database Setup (Updated for PostgreSQL) ---
# We use environment variables so Docker can inject the correct values
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
# Default to localhost for local Pytest, overridden by docker-compose
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "workout_db")

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)

engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- SQLAlchemy Model (Remains same) ---
class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    exercise_name = Column(String, index=True)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)


# --- Pydantic Schemas (Remains same) ---
class WorkoutCreate(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    weight: float


class WorkoutResponse(WorkoutCreate):
    id: int
    date: datetime.datetime

    class Config:
        from_attributes = True


# --- FastAPI App Initialization ---
app = FastAPI(title="Workout Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# --- API Endpoints ---
@app.post("/workouts/", response_model=WorkoutResponse)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(**workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@app.get("/workouts/", response_model=list[WorkoutResponse])
def read_workouts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    workouts = db.query(Workout).offset(skip).limit(limit).all()
    return workouts
