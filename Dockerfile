# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to reduce the size of the Docker image
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libcairo-gobject2 \
    gstreamer1.0-tools \
    libsoup-3.0-0 \
    libgstreamer1.0-0 \
    libatomic1 \
    libxslt1.1 \
    libwoff1 \
    libvpx7 \
    libevent-2.1-7 \
    libopus0 \
    libgstreamer-plugins-base1.0-0 \
    libharfbuzz-icu0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libflite1 \
    libflite-dev \
    libgles2-mesa \
    libx264-160 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
