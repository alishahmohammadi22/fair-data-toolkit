"""init_db.py — run once on container startup to create all tables."""
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)
print("Database tables created (or already exist).")
