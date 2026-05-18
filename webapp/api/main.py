from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routers import assessments, indicators


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FAIR Toolkit API",
    version="0.1.0",
    description="REST API for FAIR Data Maturity Assessment",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(indicators.router, prefix="/api/indicators", tags=["Indicators"])
app.include_router(assessments.router, prefix="/api/assessments", tags=["Assessments"])


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok", "version": "0.1.0"}
