# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to reduce the size of the Docker image
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the setup script and execute it
COPY setup.sh .
RUN chmod +x setup.sh
RUN ./setup.sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
