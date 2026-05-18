FROM python:3.11-slim

WORKDIR /app

# Copy and install fair_toolkit from the repo root (build context = repo root)
COPY fair_toolkit/ ./fair_toolkit/
COPY pyproject.toml README.md LICENSE ./
RUN pip install --no-cache-dir -e "."

# Install API-specific dependencies
COPY webapp/api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy API source
COPY webapp/api/ ./

# Create tables and start server
CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
