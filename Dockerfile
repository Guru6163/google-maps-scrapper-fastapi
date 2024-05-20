# Use the official Python image from the Docker Hub
FROM python:3.9-slim

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
    libgdk3.0-cil-dev \
    libsoup-3.0-0 \
    libgstreamer1.0-0 \
    libatomic1 \
    libxslt1.1 \
    libwoff1 \
    libvpx7 \
    libevent-2.1-7 \
    libopus0 \
    libgstallocators-1.0-0 \
    libgstapp-1.0-0 \
    libgstbase-1.0-0 \
    libgstpbutils-1.0-0 \
    libgstaudio-1.0-0 \
    libgsttag-1.0-0 \
    libgstvideo-1.0-0 \
    libgstgl-1.0-0 \
    libgstcodecparsers-1.0-0 \
    libgstfft-1.0-0 \
    libharfbuzz-icu0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libflite1 \
    libflite1-dev \
    libgles2-mesa \
    libx264-155 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Install Playwright and other Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Copy the content of the local src directory to the working directory
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
