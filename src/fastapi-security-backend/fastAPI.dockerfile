# Use an official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the requirements first to leverage Docker cache
COPY ../requirements.txt .


# copying the fastapi instantiation file 
COPY main.py /app/main.py

COPY __init__.py /app/__init__.py

# Install dependencies including uvicorn explicitly
RUN pip install --no-cache-dir -r requirements.txt && pip install fastapi[standard]
    
# Expose the port FastAPI uses
EXPOSE 8000

# Start FastAPI using uvicorn
#CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
